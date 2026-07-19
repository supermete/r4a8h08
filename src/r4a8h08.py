"""Main module."""
from pymodbus.client import ModbusSerialClient
import time
from serialmessage import *


class R4a8h08:
    """
    API to control the R4a8h08 device from eletechsup.
    """
    def __init__(self):
        self.bus = None
        self.node_id = None

        self._do = Message()
        self._di = Message()
        self._ai = Message()

        self.di1 = Signal(startbit=0, length=1, type=BOOL)
        self.di2 = Signal(startbit=1, length=1, type=BOOL)
        self.di3 = Signal(startbit=2, length=1, type=BOOL)
        self.di4 = Signal(startbit=3, length=1, type=BOOL)

        self.ai1 = Signal(startbit=0, length=16)
        self.ai2 = Signal(startbit=16, length=16)
        self.ai3 = Signal(startbit=32, length=16)
        self.ai4 = Signal(startbit=48, length=16)
        self.ai5 = Signal(startbit=64, length=16)
        self.ai6 = Signal(startbit=80, length=16)
        self.ai7 = Signal(startbit=96, length=16)
        self.ai8 = Signal(startbit=112, length=16)

        self.do1 = Signal(startbit=0, length=1, type=BOOL)
        self.do2 = Signal(startbit=1, length=1, type=BOOL)
        self.do3 = Signal(startbit=2, length=1, type=BOOL)
        self.do4 = Signal(startbit=3, length=1, type=BOOL)
        self.do5 = Signal(startbit=4, length=1, type=BOOL)
        self.do6 = Signal(startbit=5, length=1, type=BOOL)
        self.do7 = Signal(startbit=6, length=1, type=BOOL)
        self.do8 = Signal(startbit=7, length=1, type=BOOL)

        self._do.add(
            self.do1,
            self.do2,
            self.do3,
            self.do4,
            self.do5,
            self.do6,
            self.do7,
            self.do8,
        )

        self._di.add(
            self.di1,
            self.di2,
            self.di3,
            self.di4,
        )

        self._ai.add(
            self.ai1,
            self.ai2,
            self.ai3,
            self.ai4,
            self.ai5,
            self.ai6,
            self.ai7,
            self.ai8,
        )

    def start(self, node_id=1, baudrate=9600, port=None):
        self.node_id = node_id
        self.bus = ModbusSerialClient(baudrate=baudrate, port=port)
        self._do.write_callback = self.bus.write_coil
        self._do.read_callback = self.bus.read_coils
        self._do.arbitration_id = node_id
        self._do.type = TYPE_BITS

        self._di.read_callback = self.bus.read_discrete_inputs
        self._di.arbitration_id = node_id
        self._di.type = TYPE_BITS

        self._ai.read_callback = self.bus.read_input_registers
        self._ai.arbitration_id = node_id
        self._ai.type = TYPE_REGISTERS

        self.bus.connect()

    def stop(self):
        self.bus.close()


if __name__ == "__main__":
    device = R4a8h08()
    device.start(node_id=1, baudrate=9600, port='COM12')
    device.do8.phys = True
    time.sleep(1)
    device.do8.phys = False
    time.sleep(1)
    print(device.ai8.phys)
    device.stop()
