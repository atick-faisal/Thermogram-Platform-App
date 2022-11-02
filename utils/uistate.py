import os
import cv2
import time
import numpy as np
import tkinter as tk
from PIL import Image
from serial import Serial
from typing import Callable
from threading import Thread
from numpy.typing import NDArray

from utils import Thermogram, get_serial_data


class UiState(Thread):
    def __init__(
        self,
        data_source: Serial,
        on_temperature_change: Callable[[NDArray[np.uint8]], None]
    ) -> None:
        super().__init__()
        self.data_source = data_source
        self.on_temperature_change = on_temperature_change
        self.data = [27.0] * 50
        self.thermogram = Thermogram.generate_thermogram(self.data)
        self.record = False
        self.daemon = True

    def run(self) -> None:
        while self.data_source.isOpen():
            self.data = get_serial_data(self.data_source)
            if self.data != None:
                self.thermogram = Thermogram.generate_thermogram(self.data)
                self.on_temperature_change(self.thermogram)
            time.sleep(1)

    def record_data(self, id, name, age, weigth, gender):
        path = os.path.join("data", id)
        if not os.path.exists(path):
            os.makedirs(path)

        demographics_path = os.path.join(path, f"INFO.txt")
        thermogram_path = os.path.join(path, f"Thermogram.png")
        temperature_path = os.path.join(path, f"Temperature.csv")

        with open(demographics_path, "w") as f:
            f.write(f"ID {id}\nNAME {name}\nAGE {age}\nWEIGHT {weigth}\nGENDER {gender}")

        with open(temperature_path, "w") as f:
            f.write(",\n".join(map(str, self.data)))

        image = Image.fromarray(self.thermogram)
        image.save(thermogram_path)
