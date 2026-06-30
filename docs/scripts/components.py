from style import (
    FONT,
    PRIMARY,
    PRIMARY_LIGHT,
    TEXT,
)

from icons import draw_icon


def add_text(
    dwg,
    text,
    x,
    y,
    size=22,
    color=TEXT,
    weight="normal",
    anchor="start",
):
    dwg.add(
        dwg.text(
            text,
            insert=(x, y),
            fill=color,
            font_size=size,
            font_family=FONT,
            font_weight=weight,
            text_anchor=anchor,
        )
    )


def add_title(
    dwg,
    title,
    subtitle,
    width,
):
    add_text(
        dwg,
        title,
        width / 2,
        70,
        size=40,
        color=PRIMARY,
        weight="bold",
        anchor="middle",
    )

    add_text(
        dwg,
        subtitle,
        width / 2,
        110,
        size=23,
        color=TEXT,
        anchor="middle",
    )

    dwg.add(
        dwg.line(
            start=(width / 2 - 65, 132),
            end=(width / 2 + 65, 132),
            stroke=PRIMARY,
            stroke_width=5,
            stroke_linecap="round",
        )
    )


def add_box(
    dwg,
    x,
    y,
    w,
    h,
    title,
    lines,
    icon,
    bullets=None,
):
    dwg.add(
        dwg.rect(
            insert=(x, y),
            size=(w, h),
            rx=18,
            ry=18,
            fill="white",
            stroke=PRIMARY,
            stroke_width=2,
        )
    )

    dwg.add(
        dwg.rect(
            insert=(x + 24, y + 18),
            size=(96, h - 36),
            rx=14,
            ry=14,
            fill=PRIMARY_LIGHT,
            stroke="none",
        )
    )

    draw_icon(
        dwg,
        icon,
        x + 72,
        y + h / 2,
        size=46,
    )

    add_text(
        dwg,
        title,
        x + 150,
        y + 40,
        size=25,
        color=PRIMARY,
        weight="bold",
    )

    for i, line in enumerate(lines):
        add_text(
            dwg,
            line,
            x + 150,
            y + 70 + i * 26,
            size=19,
            color=TEXT,
        )

    if bullets:
        divider_x = x + 455

        dwg.add(
            dwg.line(
                start=(divider_x, y + 22),
                end=(divider_x, y + h - 22),
                stroke="#BFC7CE",
                stroke_width=1.5,
            )
        )

        for i, bullet in enumerate(bullets):
            add_text(
                dwg,
                f"• {bullet}",
                divider_x + 30,
                y + 37 + i * 23,
                size=16,
                color=TEXT,
            )


def add_arrow(
    dwg,
    x,
    y1,
    y2,
):
    dwg.add(
        dwg.line(
            start=(x, y1),
            end=(x, y2 - 12),
            stroke=PRIMARY,
            stroke_width=3,
        )
    )

    dwg.add(
        dwg.polygon(
            points=[
                (x - 11, y2 - 12),
                (x + 11, y2 - 12),
                (x, y2 + 8),
            ],
            fill=PRIMARY,
        )
    )


def add_caption(
    dwg,
    width,
    number,
    text,
    y,
):
    add_text(
        dwg,
        f"Figura {number}.",
        width / 2,
        y,
        size=19,
        color=PRIMARY,
        weight="bold",
        anchor="middle",
    )

    add_text(
        dwg,
        text,
        width / 2,
        y + 28,
        size=17,
        color=TEXT,
        anchor="middle",
    )

def add_section_label(
    dwg,
    x,
    y,
    title,
    subtitle,
):
    from style import PRIMARY

    line_w = 170

    # línea superior
    dwg.add(
        dwg.line(
            start=(x - line_w / 2, y),
            end=(x + line_w / 2, y),
            stroke=PRIMARY,
            stroke_width=2,
        )
    )

    add_text(
        dwg,
        title,
        x,
        y + 34,
        size=22,
        color=PRIMARY,
        weight="bold",
        anchor="middle",
    )

    # línea inferior
    dwg.add(
        dwg.line(
            start=(x - line_w / 2, y + 52),
            end=(x + line_w / 2, y + 52),
            stroke=PRIMARY,
            stroke_width=2,
        )
    )

    add_text(
        dwg,
        subtitle,
        x,
        y + 82,
        size=16,
        color=PRIMARY,
        anchor="middle",
    )