from typing import List
from converter.pattern.conversion_strategy import ConversionStrategy
from common.data_types import DataTypes

class DecimalToHexConverter(ConversionStrategy):
    def convert(self, values: List[int], data_type: str) -> str:
        decimal_value = int(values[0])
        
        return self.value_to_hex_bytes(decimal_value, data_type)

    def value_to_hex_bytes(self, value: int, data_type: str) -> str:
        byte_list = []
        byte_mask = 0xFF

        loop_count = DataTypes.get_data_type_size(data_type)

        for _ in range(loop_count):
            byte_list.append(value & byte_mask)
            value >>= 8

        return ' '.join("0x" + f"{byte:02X}" + "," for byte in byte_list)
