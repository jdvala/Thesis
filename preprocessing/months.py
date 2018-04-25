

def months(text):
    """Returns text without dates in them
    
    Args: text - type - str
    
    Returns text - type - str
    """
    if isinstance(text, str):
        # just split the damm list into words
        words = text.split()

        for index, word in enumerate(words):
            if word == "January" or word =="JANUARY" or word == "JAN" or word == "jan" or word == "Jan":
                del words[index]
            elif word == "February" or word =="FEBRUARY" or word == "FEB" or word == "feb" or word == "Feb":
                del words[index]
            elif word == "March" or word =="MARCH" or word == "MAR" or word == "mar" :
                del words[index]
            elif word == "April" or word =="APRIL" or word == "APR" or word == "apr" :
                del words[index]
            elif word == "May" or word =="MAY":
                del words[index]
            elif word == "June" or word =="JUNE" or word == "Jun" or word == "jun" :
                del words[index]
            elif word == "July" or word =="July" or word == "jul" or word == "Jul" :
                del words[index]
            elif word == "August" or word =="AUGUST" or word == "AUG" or word == "aug" :
                del words[index]
            elif word == "September" or word =="SEPTEMBER" or word == "SEP" or word == "sep" :
                del words[index]
            elif word == "October" or word =="OCTOBER" or word == "OCT" or word == "oct" :
                del words[index]
            elif word == "November" or word =="NOVEMBER" or word == "NOV" or word == "nov" :
                del words[index]
            elif word == "December" or word =="DECEMBER" or word == "Dec" or word == "dec" :
                del words[index]

    text =' '.join(words)
    return text 