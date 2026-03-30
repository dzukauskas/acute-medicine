#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import workflow_runtime  # noqa: E402


class WorkflowRuntimeTests(unittest.TestCase):
    def test_load_repo_config_uses_tracked_defaults_without_local_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            repo_config = tmp_path / "repo_config.toml"
            local_config = tmp_path / "repo_config.local.toml"
            repo_config.write_text(
                "[obsidian]\nbase_dir = '~/Obsidian'\nvault_name = 'TrackedVault'\nlaunch_agent_prefix = 'lt.medbook.sync'\n",
                encoding="utf-8",
            )

            with (
                patch.object(workflow_runtime, "REPO_CONFIG_PATH", repo_config),
                patch.object(workflow_runtime, "REPO_LOCAL_CONFIG_PATH", local_config),
            ):
                config = workflow_runtime.load_repo_config()

        self.assertEqual(config["obsidian"]["vault_name"], "TrackedVault")

    def test_load_repo_config_merges_local_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            repo_config = tmp_path / "repo_config.toml"
            local_config = tmp_path / "repo_config.local.toml"
            repo_config.write_text(
                "[obsidian]\nbase_dir = '~/Obsidian'\nvault_name = 'TrackedVault'\nlaunch_agent_prefix = 'lt.medbook.sync'\n",
                encoding="utf-8",
            )
            local_config.write_text(
                "[obsidian]\nvault_name = 'LocalVault'\n",
                encoding="utf-8",
            )

            with (
                patch.object(workflow_runtime, "REPO_CONFIG_PATH", repo_config),
                patch.object(workflow_runtime, "REPO_LOCAL_CONFIG_PATH", local_config),
            ):
                config = workflow_runtime.load_repo_config()

        self.assertEqual(config["obsidian"]["base_dir"], "~/Obsidian")
        self.assertEqual(config["obsidian"]["vault_name"], "LocalVault")
        self.assertEqual(config["obsidian"]["launch_agent_prefix"], "lt.medbook.sync")
