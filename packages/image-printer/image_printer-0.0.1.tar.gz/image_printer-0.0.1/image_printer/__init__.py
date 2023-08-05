from typing import Any, List
import cv2
import os

DEFAULT_COLOR_CODE_FORMAT = "\033[38;2;{r};{g};{b}m{text}\033[0;00m"

# DEFAULT_GRAY_SCALE_SYMBOL_LIST = '@%#*+=-:. '  # 10 levels of gray
DEFAULT_GRAY_SCALE_SYMBOL_LIST = list('$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`". ')  # 70 levels of gray
DEFAULT_GRAY_SCALE_SYMBOL_LIST.reverse()


def color_text(r: int, g: int, b: int, text: str, color_code_format: str = DEFAULT_COLOR_CODE_FORMAT):
    return color_code_format.format(r=r, g=g, b=b, text=text)


def load_image(file_path: str, x_scale: float = 0.05, y_x_ratio: float = 2) -> Any:

    y_scale = x_scale * y_x_ratio

    image = cv2.imread(file_path)
    image = image[:, :, [2, 1, 0]]

    re_width = int(image.shape[1] * y_scale)
    re_height = int(image.shape[0] * x_scale)

    resized_image = cv2.resize(image, (re_width, re_height))

    return resized_image


def print_image(file_path: str, x_scale: float = 0.05, y_x_ratio: float = 2, gray_scale_symbol_list: List[str] = DEFAULT_GRAY_SCALE_SYMBOL_LIST):
    image = load_image(file_path, x_scale, y_x_ratio)
    os.system('cls')

    width = image.shape[1]
    height = image.shape[0]

    for j in range(height):

        for i in range(width):

            r, g, b = image[j, i]
            symbol_index = int((int(r) + int(g) + int(b)) / (255 * 3 / len(gray_scale_symbol_list))) - 1

            print(color_text(r, g, b, gray_scale_symbol_list[symbol_index]), end='')
        print()
