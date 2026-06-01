import sys

import cv2
import numpy as np


def get_kernels():
    kernels = {
        "original": np.array([
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ], dtype=np.float32),

        "blur": np.ones((3, 3), dtype=np.float32) / 9.0,

        "gaussian_blur": np.array([
            [1, 2, 1],
            [2, 4, 2],
            [1, 2, 1]
        ], dtype=np.float32) / 16.0,

        "sharpen": np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ], dtype=np.float32),

        "sobel_x": np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ], dtype=np.float32),

        "sobel_y": np.array([
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ], dtype=np.float32),

        "edge_detection": np.array([
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]
        ], dtype=np.float32),

        "emboss": np.array([
            [-2, -1, 0],
            [-1, 1, 1],
            [0, 1, 2]
        ], dtype=np.float32),
    }

    return kernels


def apply_filter(image, kernel):
    return cv2.filter2D(image, -1, kernel)


def draw_text(image, text):
    output = image.copy()

    cv2.putText(
        output,
        text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 0),
        2
    )

    return output


def main():
    image = cv2.imread('lena.png')

    kernels = get_kernels()
    filter_names = list(kernels.keys())
    index = 0

    print("Key control")
    print("n: next filter")
    print("p: previous filter")
    print("q or ESC: quit")

    while True:
        filter_name = filter_names[index]
        kernel = kernels[filter_name]

        filtered = apply_filter(image, kernel)
        display = draw_text(filtered, f"Filter: {filter_name}")

        cv2.imshow("Image Filter", display)

        key = cv2.waitKey(0) & 0xFF

        if key == ord('q') or key == 27:
            break
        elif key == ord('n'):
            index = (index + 1) % len(filter_names)
        elif key == ord('p'):
            index = (index - 1) % len(filter_names)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
