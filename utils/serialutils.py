import serial
from typing import List


def get_serial_data(serial_port: serial.Serial) -> List[float] | None:
    try:
        values = serial_port \
            .readline() \
            .decode("utf-8") \
            .rstrip() \
            .split(",")

        return list(map(float, values))

    except ValueError:
        return None
