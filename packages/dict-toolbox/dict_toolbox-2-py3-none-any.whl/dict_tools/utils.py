from typing import ByteString, Dict, Iterable, Mapping, Text


def decode(value):
    if isinstance(value, ByteString):
        return value.decode()
    elif isinstance(value, Text):
        return value
    elif isinstance(value, (Mapping, Dict)):
        return decode_dict(value)
    elif isinstance(value, Iterable):
        return value.__class__(decode(x) for x in value)
    else:
        return value


def decode_dict(data: Dict[bytes, bytes]) -> Dict[str, str]:
    """
    Recursively decode all byte-strings found in a dictionary
    """
    return {decode(key): decode(value) for key, value in data.items()}
