from typing import Union
from converter.hex_to_decimal import HexToDecimalConverter
from converter.decimal_to_hex import DecimalToHexConverter
from common.conversion_types import ConversionTypes as conversion_types

class ConversionFactory:
    @staticmethod
    def get_strategy(conversion_type: conversion_types) -> Union[HexToDecimalConverter, DecimalToHexConverter]:
        if conversion_type == conversion_types.HEX_TO_DECIMAL.value:
            return HexToDecimalConverter()
        elif conversion_type == conversion_types.DECIMAL_TO_HEX.value:
            return DecimalToHexConverter()
        
        raise ValueError("Invalid conversion type")
