def parse_resp(data: bytes) ->  list:
    """
    Parse RESP (REdis Serialization Protocol) data.
    
    Args: 
        data (bytes): The RESP data to parse.
        
    Returns:
        list: A list of parsed RESP elements.
    """

    if not data.startswith(b'*'):
        raise ValueError("Invalid RESP data: must start with '*'")
    
    # Split the data into lines
    lines = data.split(b'\r\n')

    # Initialize an empty list to store the parsed elements
    parsed_elements = []

    if len(lines) < 3:
        raise ValueError("Invalid RESP data: not enough lines")
    
    # The first line indicates the number of elements
    num_elements = int(lines[0][1:])
    
    idx = 1

    while idx < len(lines) - 1:
        if lines[idx].startswith(b'$'):
            # This is a bulk string
            try:
                length = int(lines[idx][1:])
                value = lines[idx + 1]
                if len(value) != length:
                    raise ValueError("Length mismatch in RESP bulk string")
                parsed_elements.append(value.decode('utf-8'))
                idx += 2
            except (IndexError, ValueError):
                raise ValueError("Malformed RESP input")
        else:
            idx += 1
    
    # Check if the number of parsed elements matches the expected number
    if len(parsed_elements) != num_elements:
        raise ValueError("Invalid RESP data: number of elements does not match")
    return parsed_elements
