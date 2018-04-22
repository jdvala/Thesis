# Removing Numbers


import string


def num_remove(text):
    """Returns string without numbers
    
    Args: text - type - string 
    
    Returns: text - type - string
    """
    if isinstance(text, str):
        translator_numbers = str.maketrans('','',string.digits)
        text = text.translate(translator_numbers)
    else:
        print("The provided input is of {} type insted of type string". format(type(text)))
        
    return text
    