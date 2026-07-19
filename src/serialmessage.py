import numpy

__author__ = "R. Soyding"

BOOL = 1
ENUM = 99
LITTLE_ENDIAN = 0
BIG_ENDIAN = 1
TYPE_BITS = 'bits'
TYPE_REGISTERS = 'registers'


class Message:
    def __init__(self, arbitration_id=0):
        self.length = 0
        self._payload = [0]
        self.signals = list()
        self.write_callback = None
        self.read_callback = None
        self.arbitration_id = arbitration_id
        self.type = TYPE_BITS

    def write(self, index, value):
        """
        Sends message with the write identifier.
        :return: None
        """
        if self.write_callback is not None:
            return self.write_callback(index, value, slave=self.arbitration_id)

    def read(self, signal):
        """
        Sends message with the read identifier and updates the signals with the received response.
        :return: None
        """
        if self.read_callback is not None:
            if self.type == TYPE_BITS:
                return self.read_callback(0, len(self.signals), slave=self.arbitration_id).bits[signal.startbit]
            else:
                return self.read_callback(0, len(self.signals), slave=self.arbitration_id).registers[self.signals.index(signal)]

    def add(self, *signals):
        # Todo: check that added signals don't overlap each other
        for signal in signals:
            assert isinstance(signal, Signal), "signal must be a Signal instance"
            signal.set_parent(self)
            self.signals.append(signal)

            self.length += 1
            if len(self._payload) < ((signal.startbit + signal.length) // 8):
                self._payload += [0] * (((signal.startbit + signal.length) // 8) - len(self._payload))

            self._update_signal_in_payload(signal)

    def clear(self):
        for signal in reversed(self.signals):
            signal.clear()
            self.signals.remove(signal)
        self._payload = [0] * (self.length // 8)

    def get_dlc(self):
        return len(self._payload)

    @property
    def payload(self):
        self.update()
        return self._payload

    def update(self):
        for signal in self.signals:
            self._update_signal_in_payload(signal)

    def _update_signal_in_payload(self, signal):
        """Update the message payload with the signal's value"""
        byte_index = 0

        val = signal.value
        startbit = signal.startbit
        # Get the index of the first byte to be modified
        while startbit // 8 > 0:
            byte_index += 1
            startbit -= 8

        # calculate the mask for the first byte to modify
        if signal.length <= 8 - startbit :
            mask = int(f"0b{'1' * signal.length}", 2)
        else:
            mask = int(f"0b{'1' * (8 - startbit)}", 2)
        mask = (0xFF ^ (mask << startbit))

        # The remaining of startbit can be used to shift the value now
        if startbit > 0:
            val <<= numpy.uint32(startbit)

        # if big endian, we start by the msb and we shift to the lsb
        if signal.endianness == BIG_ENDIAN:
            shift = (signal.length // 8)
            if signal.length % 8 == 0:
                shift -= 1
        else:
            shift = 0
        # Cut val in 8 bits chunks and put it at the right index in payload
        bitlength = signal.length
        while bitlength // 8 > 0:
            try:
                self._payload[byte_index] &= numpy.uint8(mask)
                self._payload[byte_index] |= (val >> (shift * 8)) & 0xff
            except Exception as e:
                raise Exception(f"Signal do not fit in the message. DLC might be too small.\n{e}")
            bitlength -= 8
            byte_index += 1
            if signal.endianness == BIG_ENDIAN:
                shift -= 1
            else:
                shift += 1

            if bitlength >= 8:
                mask = 0
            elif bitlength > 0:
                mask = int(f"0b{'1' * (8 - bitlength)}{'0' * bitlength}", 2)

        # if bitlength is not 0 put the last chunk in payload too as there are some bits of data left in val
        if bitlength > 0 and byte_index < 8:
            self._payload[byte_index] &= (mask & 0xFF)
            self._payload[byte_index] |= ((val >> (shift * 8)) & 0xFF)


class Signal:
    def __init__(self, startbit=0, length=1, factor=1, offset=0, endianness=BIG_ENDIAN, signed=False, type=0, enum=None):
        self.startbit = startbit
        self.length = length
        self.factor = factor
        self.value = 0
        self.parent = None
        self.signed = signed
        self.offset = offset
        self.endianness = endianness
        self.type = type
        self.enum = enum

    def clear(self):
        self.parent = None

    @property
    def raw(self):
        """
        Get raw value of the signal
        :return: raw value of the signal
        """
        if self.parent is not None:
            try:
                self.parent.read(self)
            except TypeError as msg:
                raise Exception(f"Error while trying to communicate with the device.\n{msg}")

        return self.value

    @property
    def phys(self):
        """
        Get physical value of the signal
        :return: physical value of the signal
        """
        if self.parent is not None:
            try:
                self.value = self.parent.read(self)
            except TypeError as msg:
                raise Exception(f"Error while trying to communicate with the device.\n{msg}")

        return self.value

    @raw.setter
    def raw(self, value):
        """
        Set the raw value of the signal
        :param value: raw value to be set
        :return: None
        """
        self.value = int(value + self.offset) & int(f"0b{'1' * self.length}", 2)

        if self.parent is not None:
            try:
                self.parent.write(self.startbit, value)
            except TypeError as msg:
                raise Exception(f"Error while trying to communicate with the device.\n{msg}")


    @phys.setter
    def phys(self, value):
        """
        Set the physical value of the signal (applies factor or enum depending on signal's type)
        :param value: physical value to be set
        :return: None
        """
        if self.type == ENUM:
            if value in self.enum.values():
                for key in self.enum:
                    if self.enum[key] == value:
                        self.value = key
                        break
                else:
                    return  # don't send anything if value is not valid
        else:
            if self.signed:
                if self.length <= 8:
                    value = numpy.uint8(round(value / float(self.factor)))
                elif self.length <= 16:
                    value = numpy.uint16(round(value / float(self.factor)))
                elif self.length <= 32:
                    value = numpy.uint32(round(value / float(self.factor)))
                elif self.length <= 64:
                    value = numpy.uint64(round(value / float(self.factor)))
                self.value = ((value + self.offset) & int(f"0b{'1' * self.length}", 2))
            else:
                self.value = round((int(value / float(self.factor)) + self.offset) & int(f"0b{'1' * self.length}", 2))

        if self.parent is not None:
            try:
                self.parent.write(self.startbit, self.value)
            except TypeError as msg:
                raise Exception(f"Error while trying to communicate with the device.\n{msg}")

    def set_parent(self, message):
        self.parent = message


if __name__ == "__main__":
    msg_3c2 = Message(0x3c2)
    csm_fail = Signal(startbit=8, length=1)
    sig1 = Signal(startbit=0, length=8)
    msg_3c2.add(csm_fail)
    msg_3c2.add(sig1)

    csm_fail.raw = 1
    sig1.raw = 0xff

    print(csm_fail.raw)
    print(msg_3c2.payload)
