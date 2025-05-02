def encode_simple_string(msg: str) -> bytes:
    """
    Encode a simple string in RESP format.
    
    Args:
        msg (str): The message to encode.
        
    Returns:
        bytes: The encoded message in RESP format.
    """
    return f"+{msg}\r\n".encode('utf-8')

def encode_error(msg: str) -> bytes:
    """
    Encode an error message in RESP format.
    
    Args:
        msg (str): The error message to encode.
        
    Returns:
        bytes: The encoded error message in RESP format.
    """
    return f"-{msg}\r\n".encode('utf-8')

def encode_bulk_string(value: str) -> bytes:
    """
    Encode a bulk string in RESP format.
    
    Args:
        value (str): The value to encode.
        
    Returns:
        bytes: The encoded value in RESP format.
    """
    length = len(value)
    return f"${length}\r\n{value}\r\n".encode('utf-8')

def encode_nil() -> bytes:
    """
    Encode a nil value in RESP format.
    
    Returns:
        bytes: The encoded nil value in RESP format.
    """
    return b"$-1\r\n"

def encode_integer(value: int) -> bytes:
    """
    Encode an integer in RESP format.
    
    Args:
        value (int): The integer to encode.
        
    Returns:
        bytes: The encoded integer in RESP format.
    """
    return f":{value}\r\n".encode('utf-8')