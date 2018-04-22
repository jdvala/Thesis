# Punctuation removing function 


import string 

def puntuations_removal(text):
    """ Returns string after removing all the puntuations
        Args: text - type: String

        Return: text - type: String

    """
    # Check whether the provide argument is string or not

    if isinstance(text, str):
        translator = str.maketrans('','',string.punctuation)
        text = text.translate(translator)
    else:
        print("The provided input is of {} type insted of type string".format(type(text)))

    return text