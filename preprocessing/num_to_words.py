
# Convert numbers to words

import words
import re

def number_to_words(text):
    """Returns string by converting numerical values to its words equivalent
    Args: text - type - string 
    Returns: text - type - string
    """
   
    if isinstance(text, str):
        # break the string into words
        text = text.split()
        for index, word in enumerate(text):
            if re.match(r"\d+", word) is not None:
                per_to_word = []
                # split the word
                #print(word)
                word = word.lstrip('.')
                word = word.rstrip('.')
                #print(word)
                for character in word:
                    try:
                        if character == '.':
                            per_to_word.append("point")
                        else:
                            word = words.words(int(character))
                            per_to_word.append(word)
                    except ValueError:
                        continue
                #replace precent words to the index word was found on
                precent = ' '.join(per_to_word)
                text[index] = precent
       
            else:
                continue
    else:
        print("The provided input is of {} type insted of type string". format(type(text)))
        
    text = ' '.join(text)
    return text