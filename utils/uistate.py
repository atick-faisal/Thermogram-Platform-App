import numpy as np
import tkinter as tk
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
        self.record = False
        self.daemon = True

    def run(self) -> None:
        data = get_serial_data(self.data_source)
        thermogram = Thermogram.generate_thermogram(data)
        self.on_temperature_change(thermogram)

    def record_data():
        pass
