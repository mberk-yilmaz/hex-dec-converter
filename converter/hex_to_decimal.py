from typing import List
from converter.pattern.conversion_strategy import ConversionStrategy
from common.data_types import DataTypes

class HexToDecimalConverter(ConversionStrategy):
    def convert(self, values: List[int], data_type: str) -> str:
        hex_values = [int(value, 16) for value in values]
        return self.hex_values_to_decimal(hex_values, data_type)

    def hex_values_to_decimal(self, hex_values: List[int], data_type: str) -> int:
        decimal_value = 0

        byte_shift = 8

        loop_count = DataTypes.get_data_type_size(data_type)

        for byte_idx in range(loop_count):
            decimal_value |= hex_values[byte_idx] << (byte_shift * byte_idx)
        
        return decimal_value
