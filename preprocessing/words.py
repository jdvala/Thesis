
# Words for number hard way

###############################################
# Only to be used with num_to_words
###############################################
def words(digit):
    """ Returns string after removing all the puntuations
        Args: digit - type: iny
        Return: word - type: String

    """
    word = ""
    # Check whether the provide argument is int or not

    if isinstance(digit, int):
        if digit == 0:
            word = 'Zero'
        elif digit == 1:
            word = 'One'
        elif digit == 2:
            word = 'Two'
        elif digit == 3:
            word = 'Three'
        elif digit == 4:
            word = 'Four'
        elif digit == 5:
            word = 'Five'
        elif digit == 6:
            word = 'Six'
        elif digit == 7:
            word = 'Seven'
        elif digit == 8:
            word = 'Eight'
        elif digit == 9:
            word = 'Nine'
        else:
            pass      
    else:
        print("The provided input is of {} type insted of type int".format(type(digit)))

    return word