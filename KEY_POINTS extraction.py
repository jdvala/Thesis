
# coding: utf-8

# # Extracting Key Points
# 

# There is a pattern in the document which enables us to extract 'KEY POINTS' from the document without the HTML tags, as we have already removed these tags when we scraped the data from website. It would not be wise to do the whole process again.
# 
# The idea is very simple, there is pattern in the documents which we will exploit here
# * We will iterate through the list of sentences, and note the starting index of the string 'KEY POINTS\n'
# * We will again iterate throught the same list of sentences and find the starting index of srting 'SINCE WHEN DOES THE DIRECTIVE APPLY?\n' or 'FROM WHEN DOES THE REGULATION APPLY?\n' 
# * And we will extract all the text in between these indices, that will be our Key Points
# 
# 
# **NOTE:** *There are files which would not comply to this method, So I will collect statistics along to see how many files falls outside the scope of this algorithm.*
# 
# 

# In[34]:


import re
import os
import sys
import pandas as pd


# In[35]:


# Starting index
def start_index(text_list):
    """Returns strating index of Key Points
    Args: List of Text
    
    Returns: Integer - Index 
    """
    indice = 0 
    
    for index, sentence in enumerate(file_content):
        if re.match(r"KEY POINTS\n", sentence) is not None:
            indice = index
        else:
            # If we are unable to retrive the index of 'KEY POINTS' in the document,
            # we will return '0' as starting index so it will be easy for us to determine,
            # how many documents we are unable to extract 'KEY POINTS' from. 
            indice = indice 
            
    return indice


# In[36]:


# Ending index
def end_index(text_list):
    """Retruns the index where we find 'SINCE WHEN DOES THE DIRECTIVE APPLY?' or 
    'FROM WHEN DOES THE REGULATION APPLY\?'
    Args: List of Text
    
    Returns: Integer - Index
    """
    indice = 0
    
    for index, sentence in enumerate(file_content):
        if re.match(r"SINCE WHEN DOES THE DIRECTIVE APPLY\?\n", sentence) is not None:
            indice = index
        elif re.match(r"FROM WHEN DOES THE REGULATION APPLY\?\n", sentence) is not None:
            indice = index
        else:
            # If we are unable to retrive the index of 'KEY POINTS' in the document,
            # we will return '0' as starting index so it will be easy for us to determine,
            # how many documents we are unable to extract 'KEY POINTS' from. 
            indice = index
            
    return indice


# In[37]:


# Statistics 

Success_KEY_POINT = pd.DataFrame(columns=['Topic','Subtopic','Path'])
Failure_KEY_POINT = pd.DataFrame(columns=['Topic','Subtopic','Path'])


# In[57]:


# Go through every directory, extract content, find indices, extract content between indices, save the file in
# another directory 
_index_success = 0  # indexer for saving values to Success_KEY_POINT
_index_fail = 0     # indexer for saving values to Failure_KEY_POINT
path = "/home/jay/Thesis/Data/Data_EN/"   # 'Data_EN' will be my root folder
counter = 0
for root, dirs, files in os.walk(path):
    for file in files:
        topic = root.split(os.path.sep)[-2]
        subtopic = root.split(os.path.sep)[-1]
        title = file
        dir_path = path+topic+'/'+subtopic+'/'+file
        if file.endswith(".txt"):
            if (file != 'log.txt') and (file != 'success.txt') and (file != 'failure.txt'):
                with open(dir_path, "r") as fileContent:
                    fileContent = fileContent.readlines()
                    
                    # Start index
                    s_index = start_index(fileContent)
                    # Casting s_index to int explicitly just for safty
                    s_index = int(s_index)
                    
                    # End Index 
                    e_index = end_index(fileContent)
                    e_index = int(e_index)
                    
                    # 2 conditions: 1 - if I get the start and end index 
                    #               2 - if one or both of them are 0 
                    # In first case I proceed normally extracting whatever needs to be extracted
                    # In second case I will write all the statistics to an excel sheet (its easy to perform oprations on csv than on txt)
                    # Better I write statistics no matter what
                    
                    
                    ### Conditon 1 ###
                    # if both have values other than '0'
                    
                    if s_index != 0 and e_index != 0:
                        keypoints = []
                    
                        for index, sentence in enumerate(fileContent[s_index+1:e_index-1]):
                            keypoints.append(sentence)
                            
                            
                        # Writing Key Points to Files at '/home/jay/Thesis/Data_key_points/' 
                        
                        path_to_write = '/home/jay/Thesis/Data_key_points/'+topic+'/'+subtopic
                        
                        try:
                            os.stat(path_to_write)
                        except:
                            os.makedirs(path_to_write)
                            
                        print("Saving file at: {}".format(path_to_write))
                        
                        with open(path_to_write+'/'+file, "w") as file_to_write:
                            file_to_write.writelines(keypoints)
                            
                        
                        # Writing file name, path, topic and subtopic to file 'Success_KEY_POINT dataframe'
                        
                        _index_success += 1
    
                        Success_KEY_POINT.set_value(_index_success, 'Topic', topic)
                        Success_KEY_POINT.set_value(_index_success, 'Subtopic', subtopic)
                        Success_KEY_POINT.set_value(_index_success, 'Path', path)
                        
                       
                    ### Condition 2 ####
                    else:
                        
                        # Writing file name, path, topic and subtopic to file 'Failure_KEY_POINT dataframe'
                        
                        _index_fail += 1
    
                        Failure_KEY_POINT.set_value(_index_success, 'Topic', topic)
                        Failure_KEY_POINT.set_value(_index_success, 'Subtopic', subtopic)
                        Failure_KEY_POINT.set_value(_index_success, 'Path', path)
                
                
# Saving statistics to csv file at 'path'

success.to_csv(path)  # success dataframe to csv
failure.to_csv(path)  # failure dataframe to csv                
          
    

