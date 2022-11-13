import os
import cv2
import numpy as np
from typing import List
from numpy.typing import NDArray
from matplotlib.pyplot import cm
from sklearn.neighbors import KNeighborsRegressor


WIDTH = 960
HEIGHT = 720
MIN_TEMP = 20.0
MAX_TEMP = 30.0
TEMP_RANGE = MAX_TEMP - MIN_TEMP
AUTO_ADJUST = True

KNN = KNeighborsRegressor(3)

SENSOR_X = np.array([
    727, 778, 670, 805, 754, 698, 642, 816, 747, 693, 642,
    786, 722, 674, 777, 701, 756, 700, 747, 663, 747, 699,
    639, 727, 656, 235, 290, 183, 317, 260, 208, 156, 319,
    268, 213, 143, 287, 239, 176, 259, 185, 262, 204, 299,
    211, 320, 266, 214, 306, 234
])

SENSOR_Y = np.array([
    94, 124, 123, 185, 175, 174, 184, 245, 243, 244, 249,
    308, 305, 313, 368, 368, 442, 441, 507, 508, 569, 555,
    571, 620, 622, 91, 120, 119, 180, 170, 168, 180, 245,
    240, 240, 242, 307, 299, 304, 363, 366, 437, 436, 502,
    503, 568, 551, 563, 618, 616
])

TRAIN_X = np.stack([SENSOR_X, SENSOR_Y], axis=1)

X1 = np.repeat(np.arange(WIDTH), HEIGHT)
X2 = np.tile(np.arange(HEIGHT), WIDTH)

TEST_X = np.stack([X1, X2], axis=1)

TEMPLATE_PATH = os.path.join(os.getcwd(), "assets", "template.png")
TEMPLATE = cv2.imread(TEMPLATE_PATH, cv2.IMREAD_GRAYSCALE)
MASK = TEMPLATE == 255

BLUR_SIZE = 101


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

        if AUTO_ADJUST:
            MIN_TEMP = np.median(temperature) - 2.5
            MAX_TEMP = np.median(temperature) + 2.5
            TEMP_RANGE = MAX_TEMP - MIN_TEMP

        temperature[temperature < MIN_TEMP] = MIN_TEMP
        temperature[temperature > MAX_TEMP] = MAX_TEMP
        temperature = ((temperature - MIN_TEMP) / TEMP_RANGE)

        KNN.fit(TRAIN_X, temperature)
        thermogram = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        thermogram[X2, X1, :] = cm.jet(KNN.predict(TEST_X))[:, :-1] * 255
        thermogram = cv2.GaussianBlur(thermogram, (BLUR_SIZE, BLUR_SIZE), 0)
        thermogram[MASK, :] = 0

        return thermogram
