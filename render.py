import io

import cairo
from PIL import Image


def get_font_pos(x, y, side, extents):
    return (side - extents.width) / 2 + x * side, (extents.height + side) / 2 + y * side


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


class SudokuImage:
    def __init__(self, matrix, resolution=(512, 512), color=(0, 0, 0), font="JetBrains Mono Light", font_size=0.1):
        self.matrix = matrix
        self.resolution = resolution
        self.color, self.font, self.font_size = color, font, font_size

    def display(self):
        with cairo.ImageSurface(cairo.FORMAT_ARGB32, *self.resolution) as surface:
            self.draw(surface)
            with io.BytesIO() as f:
                surface.write_to_png(f)
                with Image.open(f) as image:
                    image.show()

    def draw(self, surface):
        context = cairo.Context(surface)
        context.scale(*self.resolution)
        context.set_source_rgb(*self.color)
        context.select_font_face(self.font)

        draw_lines(context)
        draw_numbers(context, self.matrix, self.font_size)


def main():
    k = 2
    size = (k * 630, k * 630)
    matrix = [[2, 5, 6, 4, 7, 3, 8, 9, 1], [3, 4, 9, {8, 1, 5}, {8, 5}, {1, 5}, 7, 2, 6], [8, 7, 1, {9, 2}, {9, 2}, 6, 3, 4, 5], [{9, 4, 5}, {9, 2}, {5, 7}, {9, 2, 5, 7}, 6, 8, {9, 2, 4}, 1, 3], [{9, 5}, 1, {5, 7}, {2, 3, 5, 7, 9}, 4, {9, 2, 5, 7}, {9, 2, 6}, 8, {9, 2, 7}], [6, {8, 9, 2}, 3, {1, 2, 9, 7}, {9, 2}, {1, 2, 9, 7}, {9, 2, 4}, 5, {9, 2, 4, 7}], [1, 3, 2, {8, 9, 5, 6}, {8, 9, 5}, {9, 5}, {9, 4, 5}, 7, {8, 9, 4}], [{9, 5}, {8, 9}, {8, 5}, {2, 3, 5, 7, 8, 9}, {2, 3, 5, 8, 9}, 4, {1, 2, 5, 9}, 6, {8, 9, 2}], [7, 6, 4, {8, 9, 2, 5}, 1, {9, 2, 5}, {9, 2, 5}, 3, {8, 9, 2}]]
    image = SudokuImage(matrix, size, font_size=0.1)
    image.display()


if __name__ == '__main__':
    main()
