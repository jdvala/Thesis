# This preprocessing is intended for english
# coding: utf-8

import os
import sys
import re
import string
from nltk.corpus import stopwords
import spacy
from nltk.tokenize import sent_tokenize


def sentences(list_):
    """Returns sentence tokenized text list"""
    
    text = ''.join(list_)

    # Sentence tokenize with help of sent_tokenize from nltk  
    sentence = sent_tokenize(text)

    return sentence
    
def remove(text):
    
    t = re.sub(r"(\d+\.\d+)","",text)
    #t = re.sub(r"(\d+th?|st?|nd?|rd?)","", t)
    t = re.sub(r"\d{2}.\d{2}.\d{4}","",t)
    t = re.sub(r"\d{2}\/\d{2}\/\d{4}","",t)
    t = re.sub(r"\d{2}(\/|\.)\d{2}(\/|\.)\d{2}","",t)
    t = re.sub(r"($|€|¥|₹|£)","",t)
    t = re.sub(r"(%)","",t)
    t = re.sub(r"\d+","",t)
    t = re.sub(r"\n","",t)
    t = re.sub(r"\xa0", "", t)
    return t




def pun(text):
    table = str.maketrans("","", string.punctuation)
    t = text.translate(table)
    return t


nlp = spacy.load('en')



def lemmatizer(text):        
    sent = []
    doc = nlp(text)
    for word in doc:
        sent.append(word.lemma_)
    return " ".join(sent)


def extras(sentences):

    t = re.sub(r"\"|\—|\'|\’","",sentences)
    word_list = t.split()
    for index, word in enumerate(word_list):
        if len(word) <=1:
            del word_list[index]
    
    t = ' '.join(word_list)

    return t




# Stop word removal
def stop_word(sentence):
    list_ = []
    stop_words = stopwords.words('english')
    words_list = sentence.split()
    for word in words_list:
        if word not in stop_words:
            list_.append(word)
        
    return ' '.join(list_)




def main():
    
    path = '/home/jay/Data_Pre/preprocessed/'
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                topic = root.split(os.path.sep)[-2]
                subtopic = root.split(os.path.sep)[-1]
                title = file
                dir_path = path+topic+'/'+subtopic+'/'+file

                with open(os.path.join(root, file), 'r') as contents:
                    contents = contents.read()

                # Joining the lines to make text block 

                contents = ''.join(contents)
                print("Starting to preprocess file: {}". format(dir_path))
                # Sentence tokenize the text
                sent_tokenized = sentences(contents)

                # Removing stop words
                t1 = [lemmatizer(sent) for sent in sent_tokenized]

                # lemmatization 
                t2 = [stop_word(sent) for sent in t1]

                # Removing all the unecessary things from the text 
                t3 = [remove(line) for line in t2]

                # Removing punctuations
                t4 =[pun(line.lower()) for line in t3]

            
                t5 = [extras(sent) for sent in t4]

                print("Preprocessing done for file: {}".format(dir_path))
                print("Saving File")
                path_to_write = '/home/jay/Ready/'+topic+'/'+subtopic
                try:
                    os.stat(path_to_write)
                except:
                    os.makedirs(path_to_write)

                with open(path_to_write+'/'+file, "w") as file_to_save:
                    file_to_save.write("\n".join(t5))



if __name__ == "__main__":
    main()
