def crc16_modbus(data):
    """
    Calculate the CRC16 for a data array for Modbus RTU.
    :param data: The data array (excluding the CRC).
    :return: CRC16 as a tuple of two bytes.
    """
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return [crc & 0xFF, (crc >> 8 ) & 0xFF]

# Example usage for relay ID 0 ON (to verify the function)
relay0_ON_example = [0, 6, 0, 0, 0, 255]
relay0_ON_crc = crc16_modbus(relay0_ON_example)
print(f"Calculated CRC for relay0_ON_example: {relay0_ON_crc}, expected: [200, 91]")