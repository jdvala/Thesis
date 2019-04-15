# update - added document ID, file_names, multiple labels

import os
import sys
import pickle
# import frenchpreprocessing as fr
# import spanishpreprocessing as es
# import englishpreprocessing as en
from collections import Counter
from operator import itemgetter
import pandas as pd


def get_raw_data(path):
    """Gets the raw data"""
    data_en = []
    data_de = []
    label_en = []
    label_de = []

    # File Name
    file_name = []

    for root, dirs, files in os.walk(path):
        l = root.split(os.path.sep)[-2]
        for file in files:
            if l == 'Data':
                pass
            elif file.endswith('.txt') and file!='success.txt' and file!='failure.txt' and file!='log.txt':
                print('Processing File: {}'.format(file))
                try:

                    with open(os.path.join(root,file), 'r', encoding="utf8") as fileHandle:
                        content = fileHandle.read()
                        
                        english = content.split('\n\n\n')[0]
                        german = content.split('\n\n\n')[1]

                        # a liitle more preprocessing english
                        _a = [word.replace('–', '') for word in english.split()]
                        _a = [word.replace('’s', '') for word in english.split()]
                        _a = [word.replace('’', '') for word in english.split()]
                        _a = [word for word in _a if len(word)>1]
                        
                        # a liitle more preprocessing german
                        _b = [word.replace('–', '') for word in german.split()]
                        _b = [word.replace('’s', '') for word in german.split()]
                        _b = [word.replace('’', '') for word in german.split()]
                        _b = [word for word in _b if len(word)>1]


                        data_en.append(' '.join(_a)+'\n\n\n'+' '.join(_b)+'\n\n\n')
                        label_en.append(l)
                        #data_de.append(' '.join(_b))
                        label_de.append(l)
                        file_name.append(file)
                except:
                    print('Problem with File: {}'.format(file))
    return data_en, label_en, label_de, file_name



# def preprocess(data, language):
#     """preprocess the data"""
    
#     toreturn = []
    
#     if isinstance(data, list):
#         for _doc in data:
#             if language == 'EN':
#                 toreturn.append(en.main(_doc))
#             if language == 'ES':
#                 toreturn.append(es.main(_doc))
#             elif language == 'FR':
#                 toreturn.append(fr.main(_doc))
#             else:
#                 toreturn.append(_doc)
        
#     else:
#         raise TypeError("Type Error: Something wrong")
    
#     return toreturn      

def remove_duplicate(doc, label, file_name):

    # non duplicate data
    de_non_duplicated_data = list(set(doc))

    # Lets take a look at some of the duplicates and then verify that they were actually put into the right category
    # before that we can count the number of instances in each class
    class_distribution = Counter(label)

    # Removing Duplicates from Major Class and putting it into the minor class

    non_duplicate_data = []
    non_duplicate_label = []

    # List for storing docuent ID
    doc_id = []
    file_name_ = []
    multiple_label = []

    # Combined List
    combined_data = []


    """
    When spliting the data into test and train set, we loss track of the doc_id, file names and multiple labels, for that reason, there will be a list 
    which will be a combined one containing data in the following manner

    combined_data = [english_data+\n\n\n+german_data+\n\n\n+file_name+\n\n\n+doc_id+\n\n\n+multiple_labels]

    """

    for index, non_duplicate in enumerate(de_non_duplicated_data):
         # create two list to hold label and data
        tmp_data =[]
        tmp_file_name = ''
        tmp_label=[]
        tmp_doc_id = ''

        for duplicate_data, duplicate_label, _file_name in zip(doc, label, file_name):
            if duplicate_data == non_duplicate:
                tmp_label.append(duplicate_label)
                tmp_file_name = _file_name

        if len(tmp_label)>1:
            # get the number of documents in these categories
            # find the min 
            for_min =[]
            for i, _l in enumerate(tmp_label):
                for_min.append(class_distribution[_l])

                # get the min from for_min
                min_index = min(enumerate(for_min), key=itemgetter(1))[0] 

                # now populate the list 

            non_duplicate_data.append(non_duplicate)
            non_duplicate_label.append(tmp_label[min_index])
            tmp_doc_id = 'doc_{}'.format(index)
            doc_id.append('doc_{}'.format(index))
            file_name_.append(tmp_file_name)
            multiple_label.append(tmp_label)

            # For the combined_data
            combined_data.append(non_duplicate.split('\n\n\n')[0]+'\n\n\n'+non_duplicate.split('\n\n\n')[1]+'\n\n\n'+tmp_file_name+'\n\n\n'+tmp_doc_id+'\n\n\n'+' '.join(tmp_label))



    #         print(non_duplicate_label)
    #         print(tmp_label)   
        elif len(tmp_label) == 1:
            non_duplicate_data.append(non_duplicate)
            non_duplicate_label.append(tmp_label[0])
            tmp_doc_id = 'doc_{}'.format(index)
            doc_id.append('doc_{}'.format(index))
            file_name_.append(tmp_file_name)
            multiple_label.append(tmp_label)
            combined_data.append(non_duplicate.split('\n\n\n')[0]+'\n\n\n'+non_duplicate.split('\n\n\n')[1]+'\n\n\n'+tmp_file_name+'\n\n\n'+tmp_doc_id+'\n\n\n'+' '.join(tmp_label))


    return non_duplicate_data, non_duplicate_label, doc_id, file_name_, multiple_label, combined_data


def main():
    
    path_list = ['/media/jay/Jay/2019/Main/Data_Classification/New/processed']
    
    #lang = ['EN', 'DE','ES', 'FR']
    
    for path in path_list:
        
        data_en, label_en ,label_de, file_name = get_raw_data(path)
        
        # preprocessing the data
        # as preprocessing is already done.
        #data_ = preprocess(data, lang)
        
        # get the duplicates out
        non_duplicate_data_en, non_duplicate_label_en, doc_id, file_names, multiple_labels, _combine_data = remove_duplicate(data_en, label_en, file_name)
        
        #non_duplicate_data_de, non_duplicate_label_de = remove_duplicate(data_de, label_de)
        
        
    return non_duplicate_data_en, non_duplicate_label_en, doc_id, file_names, multiple_labels, _combine_data #non_duplicate_data_de,non_duplicate_label_de


data_en, label_en, doc_id_, file_names_, _multiple_labels, _combined_data_ = main()

with open(os.path.join(os.getcwd(),'en-de-data.pkl'),'wb') as data_:
    pickle.dump(data_en,data_)

with open(os.path.join(os.getcwd(),'en-de-label.pkl'),'wb') as label_:
    pickle.dump(label_en,label_)

with open(os.path.join(os.getcwd(),'doc_ids.pkl'),'wb') as data_id:
    pickle.dump(doc_id_,data_id)

with open(os.path.join(os.getcwd(),'file_names.pkl'),'wb') as file_:
    pickle.dump(file_names_,file_)

with open(os.path.join(os.getcwd(),'multiple_labels.pkl'),'wb') as multiple_label__:
    pickle.dump(_multiple_labels, multiple_label__)

with open(os.path.join(os.getcwd(),'combined_data.pkl'),'wb') as _combine_data_:
    pickle.dump(_combined_data_, _combine_data_)


info_ = pd.DataFrame(data=list(zip(doc_id_, file_names_, _multiple_labels)), columns= ['DOC_ID', 'FILE_NAME', 'MULTIPLE_LABELS'])

info_.to_csv(os.path.join(os.getcwd(), os.path.basename(__file__)+'.csv'))