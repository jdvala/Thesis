# Date preprocesing Utility

import re


def date_remove(text):
    """Returns text without dates in them
    
    Args: text - type - str
    
    Returns text - type - str
    """
    if isinstance(text, str):
        # just split the damm list into words
        words = text.split()
        
        for index, word in enumerate(words):
            if re.search(r"\d{2}.\d{2}.\d{4}",word) is not None:    # date in dd.mm.yyyy format
                del words[index] # remove the date
            elif re.search(r"\d{2}\/\d{2}\/\d{4}",word) is not None:    # date in dd/mm/yyyy format
                del words[index] # remove the date
            elif re.search(r"\d{2}(\/|\.)\d{2}(\/|\.)\d{2}",word) is not None:    # date in dd/mm/yy format or dd.mm.yy
                del words[index] # remove the date
            else:
                continue
            
    else:
        print("The provided input is of {} type insted of type string".format(type(text)))
    
    # Joining the text before returning
    text = ' '.join(words)
    
    return text
