#!/usr/bin/env python3
from __future__ import annotations

import shlex
import subprocess
from pathlib import Path
from typing import Sequence


SHORT_TIMEOUT_SECONDS = 30
DEFAULT_TIMEOUT_SECONDS = 300
LONG_TIMEOUT_SECONDS = 900


class WorkflowSubprocessError(RuntimeError):
    """Raised when a workflow subprocess times out or exits unsuccessfully."""


def format_command(args: Sequence[str | Path]) -> str:
    return shlex.join(str(arg) for arg in args)


def format_failure_message(
    phase: str,
    args: Sequence[str | Path],
    returncode: int,
    stdout: str | None = None,
    stderr: str | None = None,
) -> str:
    details: list[str] = []
    if stderr and stderr.strip():
        details.append(f"stderr:\n{stderr.rstrip()}")
    if stdout and stdout.strip() and stdout.strip() != (stderr or "").strip():
        details.append(f"stdout:\n{stdout.rstrip()}")

    message = (
        f"{phase} failed with exit code {returncode} while running "
        f"`{format_command(args)}`."
    )
    if details:
        message += "\n" + "\n".join(details)
    return message


def run_subprocess(
    args: Sequence[str | Path],
    *,
    phase: str,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    capture_output: bool = False,
    text: bool = False,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
    normalized_args = [str(arg) for arg in args]
    try:
        return subprocess.run(
            normalized_args,
            capture_output=capture_output,
            text=text,
            timeout=timeout,
            cwd=str(cwd) if cwd is not None else None,
        )
    except subprocess.TimeoutExpired as exc:
        raise WorkflowSubprocessError(
            f"{phase} timed out after {timeout}s while running "
            f"`{format_command(normalized_args)}`."
        ) from exc


def run_checked_subprocess(
    args: Sequence[str | Path],
    *,
    phase: str,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    capture_output: bool = False,
    text: bool = False,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
    completed = run_subprocess(
        args,
        phase=phase,
        timeout=timeout,
        capture_output=capture_output,
        text=text,
        cwd=cwd,
    )
    if completed.returncode != 0:
        stdout = completed.stdout if isinstance(completed.stdout, str) else None
        stderr = completed.stderr if isinstance(completed.stderr, str) else None
        raise WorkflowSubprocessError(
            format_failure_message(
                phase,
                args,
                completed.returncode,
                stdout=stdout,
                stderr=stderr,
            )
        )
    return completed
