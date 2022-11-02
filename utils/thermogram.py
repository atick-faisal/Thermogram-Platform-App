import cv2
import numpy as np
from typing import List
from numpy.typing import NDArray
from matplotlib.pyplot import cm


WIDTH = 32
HEIGHT = 25
MIN_TEMP = 27.0
MAX_TEMP = 37.0
TEMP_RANGE = MAX_TEMP - MIN_TEMP

# CMAP = np.array([
#     [0, 51, 251],
#     [5, 164, 246],
#     [2, 244, 255],
#     [1, 245, 251],
#     [0, 253, 198],
#     [4, 250, 122],
#     [77, 253, 1],
#     [177, 253, 3],
#     [247, 254, 1],
#     [255, 176, 0],
#     [250, 68, 3]
# ])

SENSOR_X = np.array([
    24, 26, 22, 27, 25, 23, 21, 27, 25, 23, 21, 26, 24, 22, 26, 23, 25,
    23, 25, 22, 25, 23, 21, 24, 22,  8, 10,  6, 11,  9,  7,  5, 11,  9,
    7,  5, 10,  8,  6,  9,  6,  9,  7, 10,  7, 11,  9,  7, 10,  8
])

SENSOR_Y = np.array([
    3,  4,  4,  6,  6,  6,  6,  8,  8,  8,  8, 10, 10, 10, 12, 12, 15,
    15, 17, 17, 19, 19, 19, 21, 21,  3,  4,  4,  6,  6,  6,  6,  8,  8,
    8,  8, 10, 10, 10, 12, 12, 15, 15, 17, 17, 19, 19, 19, 21, 21
])


class Thermogram(object):

    @staticmethod
    def apply_brightness_contrast(
        image: NDArray[np.uint8],
        brightness: int = 64,
        contrast: int = 32
    ) -> NDArray[np.uint8]:
        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                highlight = 255
            else:
                shadow = 0
                highlight = 255 + brightness
            alpha_b = (highlight - shadow) / 255
            gamma_b = shadow

            buffer = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)
        else:
            buffer = image.copy()

        if contrast != 0:
            f = 131 * (contrast + 127) / (127 * (131 - contrast))
            alpha_c = f
            gamma_c = 127 * (1 - f)

            buffer = cv2.addWeighted(buffer, alpha_c, buffer, 0, gamma_c)

        return buffer

    @staticmethod
    def interpolate(image: NDArray, scale: int = 30) -> NDArray[np.uint8]:
        return cv2.resize(
            image,
            dsize=None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_LINEAR
        )

    @staticmethod
    def gaussian_blur(image: NDArray, ksize: int = 7) -> NDArray[np.uint8]:
        return cv2.GaussianBlur(image, (ksize, ksize), 0) * 3

    @staticmethod
    def average_blur(image: NDArray, ksize: int = 31) -> NDArray[np.uint8]:
        return cv2.blur(image, ksize=(ksize, ksize))

    @staticmethod
    def generate_thermogram(
        temperature: NDArray[np.float32] | List[float]
    ) -> NDArray[np.uint8]:
        temperature = np.array(temperature, dtype=np.float32)
        temperature[temperature < MIN_TEMP] = MIN_TEMP
        temperature[temperature > MAX_TEMP] = MAX_TEMP

        # temperature = ((temperature - MIN_TEMP) / TEMP_RANGE) * 10.0
        # temperature = temperature.astype(np.int8)

        temperature = ((temperature - MIN_TEMP) / TEMP_RANGE)

        thermogram = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        # thermogram[SENSOR_Y, SENSOR_X, :] = CMAP[temperature]

        for i in range(temperature.size):
            thermogram[SENSOR_Y[i], SENSOR_X[i], :] = \
                np.array(cm.jet(temperature[i]))[:-1] * 255

        thermogram = Thermogram.gaussian_blur(thermogram)
        thermogram = Thermogram.interpolate(thermogram)
        thermogram = Thermogram.average_blur(thermogram)
        thermogram = Thermogram.apply_brightness_contrast(thermogram)

        return thermogram
