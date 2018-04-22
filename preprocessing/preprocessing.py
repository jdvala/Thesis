# General Preprocessing of text for creating word embeddings
# This will be only for english text and it will be extended for other languages 


import os
import sys
import nltk
import string
import re


# Removing puntuations

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

def number_to_words(text):
    """ Returns text without numbers but with the words

    Args: text - Type: String

    Return: text - Type: String
    """
    num_word_dict = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine'} 
    # Check if the provided argument is string or not

    if isinstance(text, str):
        # Break string into list of words
        temp_list = text.split()

        # Perform everything on this 'temp_list'
        # use regular expressions to find numbers(we are specifically using this trick to convert years in key points to its word form)
        # Example: 2002 becomes two zero zero two
        for index, word in enumerate(temp_list):
            if re.match(r"\d+", word) is not None:
                word_temp = word.split() # Split whole number in single digits Example: 2002 becomes 2,0,0,2
                words_list_temp =[]
                for digit in word_temp:  
                    digit = int(digit)      # Explicit conversion: Just to make sure things go smoothly
                    for key, value in num_word_dict.items():    # Iterate through the dict
                        if key == digit:                # If the key is equal to the digit 
                            words_list_temp.append(value)   # get the value of the digit and store it in the temp list
                        else:
                            continue
                temp_list[index] = "".join(words_list_temp)   # when the whole number is converted into its word form just replace it into the text 
            else:
                continue
    return text

with open('/home/jay/Thesis/Data_key_points/agriculture/Archivedsummaries/Production of EU statistics for permanent crops.txt', "r") as files:
    contents = files.readlines()

contents = ''.join(contents)

text = number_to_words(puntuations_removal(contents))


