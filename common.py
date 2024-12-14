from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

DIRECTIONS_RDLU = ((0, 1), (1, 0), (0, -1), (-1, 0))
DIRECTIONS_WITH_DIAG = ((0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1))


def handle_solution(solution: any, expected_output: Optional[int] = None):
    if expected_output:
        assert expected_output == solution, f"Expected solution is {expected_output}. Got {solution}"
        print("[OK]")
        return

    print(solution)
    return solution


def read_input_as_matrix(input_path: str) -> List[List[str]]:
    with open(input_path) as f:
        lines = f.readlines()
        return [list(line.removesuffix("\n")) for line in lines]


def read_input_as_string(input_path: str) -> str:
    with open(input_path) as f:
        return f.read()


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
        return [line.removesuffix("\n") for line in lines]


def is_in_board(rows, cols, row, col):
    return 0 <= row < rows and 0 <= col < cols


def add_2d_vectors(vec1: Tuple[int, int], vec2: Tuple[int, int]) -> Tuple[int, int]:
    return (vec1[0] + vec2[0], vec1[1] + vec2[1])


def multiply_2d_vector(vec1: Tuple[int, int], m: int):
    return (m * vec1[0], m * vec1[1])


def string_to_image(
    text,
    output_path,
    font_path=None,
    font_size=12,
    image_size=(2000, 2000),
    bg_color="white",
    text_color="black",
):

    img = Image.new("RGB", image_size, color=bg_color)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()

    line_spacing = font_size + 5  # Space between lines

    lines = text.split("\n")
    x, y = 10, 10
    for line in lines:
        draw.text((x, y), line, fill=text_color, font=font)
        y += line_spacing

    img.save(output_path)
    print(f"Image saved to {output_path}")
