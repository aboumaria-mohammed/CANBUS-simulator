class CANMessage:
    def __init__(self, identifier, data, is_remote=False):
        self.SOF = 1  # Start of Frame (1 bit)
        self.identifier = format(identifier, '011b')  # 11-bit identifier
        self.RTR = '1' if is_remote else '0'  # Remote Transmission Request (1 bit)
        self.IDE = '0'  # Identifier Extension (1 bit)
        self.r0 = '0'  # Reserved bit (1 bit)

        if is_remote:
            # Remote frames don't contain data, just DLC
            self.DLC = format(0, '04b')  # Data Length Code (4 bits)
            self.data = '0' * 64  # Empty data field
        else:
            # Ensure data is exactly 8 bytes by padding with zeros
            padded_data = list(data)
            while len(padded_data) < 8:
                padded_data.append(0)

            self.DLC = format(8, '04b')  # Data Length Code (4 bits)
            self.data = ''.join(format(b, '08b') for b in padded_data)

        self.CRC = self._calculate_crc()  # CRC Field (15 bits)
        self.CRC_delimiter = '1'  # CRC delimiter (1 bit)
        self.ACK = '0'  # ACK slot (1 bit)
        self.ACK_delimiter = '1'  # ACK delimiter (1 bit)
        self.EOF = '1111111'  # End of Frame (7 bits)
        self.IFS = '111'  # Interframe Space (3 bits)

    def _calculate_crc(self):
        # CAN uses CRC-15 with polynomial x^15 + x^14 + x^10 + x^8 + x^7 + x^4 + x^3 + 1
        CRC_POLY = 0x4599  # Binary: 0100 0101 1001 1001

        # Get the message bits that are included in CRC calculation
        message = self.identifier + self.RTR + self.IDE + self.r0 + self.DLC + self.data

        # Initialize CRC register with zeros
        crc = 0

        # Process each bit of the message
        for bit in message:
            # XOR the MSB of the CRC register with the incoming bit
            msb = (crc >> 14) & 1
            next_bit = int(bit) ^ msb

            # Shift CRC register left by 1
            crc = (crc << 1) & 0x7FFF  # Keep only 15 bits

            # If next_bit is 1, XOR with polynomial
            if next_bit:
                crc ^= CRC_POLY

        # Return the final CRC as a 15-bit binary string
        return format(crc, '015b')

    def get_complete_frame(self):
        return (str(self.SOF) + self.identifier + self.RTR + self.IDE + self.r0 +
                self.DLC + self.data + self.CRC + self.CRC_delimiter +
                self.ACK + self.ACK_delimiter + self.EOF + self.IFS)

    def get_frame_parts(self):
        return {
            'SOF': str(self.SOF),
            'Identifier': self.identifier,
            'RTR': self.RTR,
            'IDE': self.IDE,
            'r0': self.r0,
            'DLC': self.DLC,
            'Data': self.data,
            'CRC': self.CRC,
            'CRC_delimiter': self.CRC_delimiter,
            'ACK': self.ACK,
            'ACK_delimiter': self.ACK_delimiter,
            'EOF': self.EOF,
            'IFS': self.IFS
        }

    def verify_crc(self):
        """Verify the CRC of the message"""
        # Calculate CRC of the message
        original_crc = self.CRC
        self.CRC = self._calculate_crc()
        is_valid = original_crc == self.CRC
        self.CRC = original_crc
        return is_valid