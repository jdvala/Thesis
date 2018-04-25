# Removing Numbers


import string
import re

def num_remove(text):
    """Returns string without numbers
    
    Args: text - type - string 
    
    Returns: text - type - string
    """
    
    if isinstance(text, str):

        # remove floats
        text = text.replace(re.findall(r"(\d+\.\d+)", text, flags=re.I), "")

        # remove ordinals

        text = text.replace(re.findall(r"(\d+th?|st?|nd?|rd?)",text, flags=re.I),"")


        # Just to make sure, standard number removal trick
        translator_numbers = str.maketrans('','',string.digits)
        text = text.translate(translator_numbers)
    else:
        print("The provided input is of {} type insted of type string". format(type(text)))
        
    return text
    