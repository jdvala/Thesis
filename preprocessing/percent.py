# numerical to word precent converter 

import re 



def precent_conversion(text):
    """Returns string by converting numerical percentage(5%) to words(five percentage)
    Args: text - type - string 
    Returns: text - type - string
    """
    num_dict = {0:'Zero', 1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine'}
    per_to_word = []
    if isinstance(text, str):
        # break the string into words
        text = text.split()
        for index, word in enumerate(text):
            if re.match(r"\d+\%", word) is not None:
                # split the word
                for character in word:
                    for key, value in num_dict.items():
                        try:
                            if key == int(character):
                                per_to_word.append(value)
                        except ValueError:
                            pass
                
                #replace precent words to the index word was found on
                precent = ' '.join(per_to_word)
                precent = precent+' precent'
                text[index] = precent
                
            else:
                continue
                
    else:
        print("The provided input is of {} type insted of type string". format(type(text)))
        
    return text
    