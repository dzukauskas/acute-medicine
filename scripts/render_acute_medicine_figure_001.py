#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/dzukauskas/Projects/Acute Medicine")
OUT = ROOT / "books/acute-medicine/lt/figures/001-figure-1-1-advanced-life-support.png"

# This script is the single source of truth for figure 1.1.
# Do not keep a parallel unsynced draw.io file for the same figure.

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size=size)


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    *,
    fill: str,
    body_font: ImageFont.FreeTypeFont,
    spacing: int = 6,
) -> None:
    left, top, right, bottom = box
    bbox = draw.multiline_textbbox((0, 0), text, font=body_font, spacing=spacing, align="center")
    x = left + (right - left - (bbox[2] - bbox[0])) / 2
    y = top + (bottom - top - (bbox[3] - bbox[1])) / 2
    draw.multiline_text((x, y), text, font=body_font, fill=fill, spacing=spacing, align="center")


def draw_round_box(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    *,
    fill: str,
    outline: str | None = None,
    radius: int = 28,
    width: int = 4,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow_head(
    draw: ImageDraw.ImageDraw,
    tip: tuple[int, int],
    *,
    direction: str,
    color: str,
    size: int = 24,
) -> None:
    x, y = tip
    if direction == "down":
        points = [(x, y), (x - size, y - size), (x + size, y - size)]
    elif direction == "up":
        points = [(x, y), (x - size, y + size), (x + size, y + size)]
    elif direction == "left":
        points = [(x, y), (x + size, y - size), (x + size, y + size)]
    elif direction == "right":
        points = [(x, y), (x - size, y - size), (x - size, y + size)]
    else:
        raise ValueError(direction)
    draw.polygon(points, fill=color)


def polyline(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[int, int]],
    *,
    color: str,
    width: int = 10,
    end_arrow: str | None = None,
) -> None:
    draw.line(points, fill=color, width=width, joint="curve")
    if end_arrow:
        arrow_head(draw, points[-1], direction=end_arrow, color=color, size=max(16, width * 2))


def wrap_to_width(
    draw: ImageDraw.ImageDraw,
    text: str,
    *,
    body_font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    words = text.split()
    if not words:
        return [""]

    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        bbox = draw.textbbox((0, 0), candidate, font=body_font)
        if bbox[2] - bbox[0] <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def text_block(
    draw: ImageDraw.ImageDraw,
    *,
    x: int,
    y: int,
    width: int,
    header: str,
    items: list[str],
    header_font: ImageFont.FreeTypeFont,
    item_font: ImageFont.FreeTypeFont,
    fill: str = "#111111",
    gap: int = 12,
    item_gap: int = 8,
) -> None:
    draw.multiline_text((x, y), header, font=header_font, fill=fill, spacing=6)
    header_bbox = draw.multiline_textbbox((x, y), header, font=header_font, spacing=6)
    current_y = header_bbox[3] + gap
    for item in items:
        wrapped = wrap_to_width(draw, item, body_font=item_font, max_width=width - 24)
        lines = [f"\u2022 {wrapped[0]}"] + [f"  {line}" for line in wrapped[1:]]
        text = "\n".join(lines)
        draw.multiline_text((x, current_y), text, font=item_font, fill=fill, spacing=4)
        item_bbox = draw.multiline_textbbox((x, current_y), text, font=item_font, spacing=4)
        current_y += (item_bbox[3] - item_bbox[1]) + item_gap


def main() -> None:
    w, h = 1800, 2550
    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)

    blue = "#0c5a92"
    dark_blue = "#0b4f84"
    light_blue = "#92aed3"
    pale_blue = "#cfd8ea"
    red = "#f2553d"
    pale_red = "#f5d0c1"
    green = "#72a85e"
    pale_green = "#dce9da"
    yellow = "#f6e88a"
    orange_line = "#f4a28b"
    green_line = "#9ec792"
    yellow_line = "#ead86a"

    draw.rounded_rectangle((40, 40, w - 40, h - 40), radius=40, fill="white", outline=blue, width=16)

    title_font = font(56, bold=True)
    box_font_large = font(44, bold=True)
    box_font_medium = font(38, bold=True)
    box_font_small = font(28, bold=True)
    box_font_tiny = font(22, bold=False)
    header_font = font(38, bold=True)
    item_font = font(24, bold=False)
    item_font_small = font(22, bold=False)

    draw_centered_text(
        draw,
        (200, 80, w - 200, 170),
        "Suaugusiojo specialusis gaivinimas",
        fill=blue,
        body_font=title_font,
    )

    badge = [(150, 230), (340, 230), (340, 390), (245, 470), (150, 390)]
    draw.polygon(badge, outline=blue, fill="white", width=5)
    draw_centered_text(
        draw,
        (165, 260, 325, 380),
        "U\u017etikrinkite\nsavo saug\u0105",
        fill=blue,
        body_font=font(28, bold=True),
    )

    top_box = (460, 230, 1275, 370)
    cpr_box = (460, 475, 1275, 615)
    assess_box = (460, 690, 1275, 820)
    shockable_box = (110, 940, 570, 1080)
    shock_box = (110, 1150, 570, 1310)
    resume_left_box = (110, 1380, 570, 1570)
    rosc_box = (620, 1085, 1110, 1255)
    nonshock_box = (1160, 940, 1690, 1080)
    resume_right_box = (1160, 1390, 1690, 1570)
    call_box = (1325, 400, 1665, 575)

    draw_round_box(draw, top_box, fill=dark_blue, radius=8)
    draw_centered_text(
        draw,
        top_box,
        "Nereaguoja ir\nnekv\u0117puoja normaliai",
        fill="white",
        body_font=box_font_large,
    )

    draw_round_box(draw, cpr_box, fill=light_blue)
    draw_centered_text(
        draw,
        cpr_box,
        "Gaivinimas 30 : 2\nPrijunkite defibriliatori\u0173 / monitori\u0173",
        fill="#111111",
        body_font=box_font_medium,
    )

    draw_round_box(draw, assess_box, fill=light_blue)
    draw_centered_text(draw, assess_box, "\u012evertinkite ritm\u0105", fill="#111111", body_font=box_font_large)

    draw_round_box(draw, call_box, fill=pale_blue)
    draw_centered_text(
        draw,
        call_box,
        "Kviesti gaivinimo\nkomand\u0105 / GMP",
        fill="#111111",
        body_font=font(30, bold=True),
    )

    draw_round_box(draw, shockable_box, fill=red, radius=0)
    draw_centered_text(
        draw,
        shockable_box,
        "DEFIBRILIUOTINAS\n(SV / skilvelin\u0117 tachikardija\nbe pulso)",
        fill="white",
        body_font=font(30, bold=True),
    )

    draw_round_box(draw, shock_box, fill=pale_red)
    draw_centered_text(draw, shock_box, "1 i\u0161krova", fill="#111111", body_font=box_font_large)

    draw_round_box(draw, resume_left_box, fill=pale_red)
    draw_centered_text(
        draw,
        resume_left_box,
        "Nedelsiant t\u0119sti\ngaivinim\u0105 2 min.",
        fill="#111111",
        body_font=font(34, bold=True),
    )

    draw_round_box(draw, rosc_box, fill=yellow, radius=0)
    draw_centered_text(
        draw,
        rosc_box,
        "Spontanin\u0117s\nkraujotakos atsik\u016brimas\n(ROSC)",
        fill="#111111",
        body_font=font(28, bold=True),
    )

    draw_round_box(draw, nonshock_box, fill=green, radius=0)
    draw_centered_text(
        draw,
        nonshock_box,
        "NEDEFIBRILIUOTINAS\n(PEA / asistolija)",
        fill="white",
        body_font=font(34, bold=True),
    )

    draw_round_box(draw, resume_right_box, fill=pale_green)
    draw_centered_text(
        draw,
        resume_right_box,
        "Nedelsiant t\u0119sti\ngaivinim\u0105 2 min.",
        fill="#111111",
        body_font=font(34, bold=True),
    )

    polyline(draw, [(868, 370), (868, 475)], color=light_blue, width=12, end_arrow="down")
    polyline(draw, [(868, 615), (868, 690)], color=light_blue, width=12, end_arrow="down")
    polyline(draw, [(868, 370), (868, 490), (1325, 490)], color=light_blue, width=12, end_arrow="right")

    polyline(draw, [(460, 755), (340, 755), (340, 940)], color=orange_line, width=10, end_arrow="down")
    polyline(draw, [(840, 820), (840, 1085)], color=yellow_line, width=10, end_arrow="down")
    polyline(draw, [(1275, 755), (1425, 755), (1425, 940)], color=green_line, width=10, end_arrow="down")

    polyline(draw, [(340, 1080), (340, 1150)], color=orange_line, width=10, end_arrow="down")
    polyline(draw, [(340, 1310), (340, 1380)], color=orange_line, width=10, end_arrow="down")
    polyline(draw, [(230, 1570), (70, 1570), (70, 755), (460, 755)], color=orange_line, width=10, end_arrow="right")

    polyline(draw, [(1425, 1080), (1425, 1390)], color=green_line, width=10, end_arrow="down")
    polyline(draw, [(1535, 1570), (1750, 1570), (1750, 755), (1275, 755)], color=green_line, width=10, end_arrow="left")

    text_block(
        draw,
        x=80,
        y=1600,
        width=700,
        header="U\u017etikrinkite kokybi\u0161kus\nkr\u016btin\u0117s l\u0105stos paspaudimus ir:",
        items=[
            "skirkite deguon\u012f",
            "naudokite bangos formos kapnografij\u0105",
            "pa\u017eangiai u\u017etikrinus kv\u0117pavimo takus, t\u0119skite nepertraukiamus paspaudimus",
            "kuo labiau trumpinkite pertraukas",
            "u\u017etikrinkite venin\u0119 arba intraosin\u0119 prieig\u0105",
            "adrenalin\u0105 skirkite kas 3-5 min.",
            "amjodaron\u0105 skirkite po 3 i\u0161krov\u0173",
            "nustatykite ir koreguokite gr\u012f\u017etamas prie\u017eastis",
        ],
        header_font=header_font,
        item_font=item_font_small,
        item_gap=4,
    )

    text_block(
        draw,
        x=930,
        y=1600,
        width=710,
        header="Nustatykite ir koreguokite\ngr\u012f\u017etamas prie\u017eastis",
        items=[
            "hipoksija",
            "hipovolemija",
            "hipo-/hiperkalemija ir kiti metaboliniai sutrikimai",
            "hipotermija",
            "tromboz\u0117 - koronarin\u0117 arba plautin\u0117",
            "\u012ftampos pneumotoraksas",
            "\u0161irdies tamponada",
            "toksinai",
            "svarstykite ultragars\u0105 gr\u012f\u017etamoms prie\u017eastims nustatyti",
        ],
        header_font=header_font,
        item_font=item_font_small,
        item_gap=4,
    )

    text_block(
        draw,
        x=80,
        y=2010,
        width=700,
        header="Svarstyti",
        items=[
            "koronarin\u0119 angiografij\u0105 / perkutanin\u0119 koronarin\u0119 intervencij\u0105",
            "mechaninius paspaudimus perve\u017eimui ar gydymui palengvinti",
            "ekstrakorporin\u012f gaivinim\u0105",
        ],
        header_font=header_font,
        item_font=item_font,
        item_gap=5,
    )

    text_block(
        draw,
        x=930,
        y=2010,
        width=710,
        header="Po ROSC",
        items=[
            "atlikite ABCDE \u012fvertinim\u0105",
            "palaikykite SpO2 94-98 % ir normokapnij\u0105",
            "atlikite 12 derivacij\u0173 EKG",
            "nustatykite ir gydykite prie\u017east\u012f",
            "taikykite temperat\u016bros kontrol\u0119",
        ],
        header_font=header_font,
        item_font=item_font,
        item_gap=5,
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="PNG")
    print(OUT)


if __name__ == "__main__":
    main()
