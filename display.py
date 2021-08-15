import io

import cairo
from PIL import Image


FONT = "JetBrains Mono Lightfdsgs"


def display_sudoku(matrix, resolution):
    with cairo.ImageSurface(cairo.FORMAT_ARGB32, *resolution) as surface:
        draw(surface, resolution, matrix)
        with io.BytesIO() as f:
            surface.write_to_png(f)
            with Image.open(f) as image:
                image.show()


def draw(surface, resolution, matrix):
    context = cairo.Context(surface)
    context.scale(*resolution)
    context.select_font_face(FONT)

    draw_lines(context)
    draw_numbers(context, matrix, font_size=0.1)


def draw_lines(ctx):
    for i in range(0, 10):
        if i % 3:
            ctx.set_line_width(0.003)
        else:
            ctx.set_line_width(0.009)
        i /= 9
        # horizontal
        ctx.move_to(0, i)
        ctx.line_to(1, i)
        # vertical
        ctx.move_to(i, 0)
        ctx.line_to(i, 1)

        ctx.stroke()


def draw_numbers(ctx, matrix, font_size):
    ctx.set_font_size(font_size)
    for y in range(9):
        for x in range(9):
            value = matrix[y][x]
            if isinstance(value, int):
                ctx.set_font_size(font_size)
                ctx.move_to(*get_font_pos(x, y, 1 / 9, ctx.text_extents(str(value))))
                ctx.show_text(str(value))
            elif isinstance(value, set):
                ctx.set_font_size(font_size / 3)
                for index, value in enumerate(sorted(value)):
                    _x, _y = get_font_pos(index % 3, index // 3, 1 / 27, ctx.text_extents(str(value)))
                    ctx.move_to(_x + x / 9, _y + y / 9)
                    ctx.show_text(str(value))
    ctx.stroke()


def get_font_pos(x, y, side, extents):
    return (side - extents.width) / 2 + x * side, (extents.height + side) / 2 + y * side
