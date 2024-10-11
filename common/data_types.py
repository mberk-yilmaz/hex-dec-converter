from enum import Enum

class DataTypes(Enum):
    # text - sizeof
    UINT16 = ("uint16", 2)
    UINT32 = ("uint32", 4)

    def __new__(cls, name, size):
        obj = object.__new__(cls)
        obj._value_ = name
        obj.size = size
        return obj

    ## Return the size of the data type.
    @staticmethod
    def get_data_type_size(data_type: str) -> int:
        data_type = data_type.casefold()
        if data_type == DataTypes.UINT32.name.casefold():
            return DataTypes.UINT32.size
        elif data_type == DataTypes.UINT16.name.casefold():
            return DataTypes.UINT16.size
        else:
            raise ValueError(f"Unsupported data type: {data_type}")