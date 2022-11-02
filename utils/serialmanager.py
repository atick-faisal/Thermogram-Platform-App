import time
import serial
import warnings

from serial.tools.list_ports import comports


class SerialPort:
    def __init__(
        self, baud_rate: int,
        port_name: str = None,
        auto_detect: bool = True
    ):
        self.baud_rate = baud_rate
        self.port_name = port_name
        if auto_detect:
            self.port_name = self.auto_detect_serial_port()

    def auto_detect_serial_port(self) -> str:
        ports = [
            p.device
            for p in comports()
            if "CP2102" in p.description
        ]
        if not ports:
            raise IOError("no device found!")
        if len(ports) > 1:
            warnings.warn("multiple devices found - using the first")

        return ports[0]

    def open(self) -> serial.Serial:
        ser = serial.Serial(
            port=self.port_name,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
            xonxoff=0,
            rtscts=0
        )

        print("initializing serial port ... ", end="")
        ser.dtr = False
        time.sleep(1)
        ser.reset_input_buffer()
        ser.dtr = True
        time.sleep(1)
        print("done!")

        return ser
