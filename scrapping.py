
# coding: utf-8

# **Done with english corpus**
# 
# *TODO:* 
# * German, French and Spanish Corpus

# In[1]:


# Too many warnings, Beautiful Soup is not beautiful at all 

import warnings
import os
import sys
import re

from bs4 import BeautifulSoup
import urllib.request

if not sys.warnoptions:
    warnings.simplefilter("ignore")


# In[2]:


# Text File with all the links
with open("/home/jay/Thesis/links.txt") as file:
    lines = file.readlines()


################################################################################################################

download = int(input("Enter 1 for English, 2 for German, 3 for French, 4 for Spanish: \n"))
if download == 1:
    lang = "EN"
elif download == 2:
    lang = "DE"
elif download == 3:
    lang = "FR"
elif download == 4:
    lang = "ES"


###############################################################################################################
def topic_and_subtopic(list_links):
    """Returns the Topic and Subtopic by HTML Parsing"""
    topic = []
    subtopic = []
    topic_str = ""
    subtopic_str = ""
    # Topic extraction
    for index,link in enumerate(list_links):
        try:
            top = re.search(r"(\/summary\/chapter\/)(\w*_?\w*?_?\w*?)(.html)", link)
            #print("Found Topic: {}".format(m.group(1)))                 # For debugging
            topic.append(top.group(2))
            topic_str = "".join(topic)
        except:
            pass
        
    # Subtopic extraction
    for index,link in enumerate(list_links):
       
        try:
            sub = re.search(r"(.\/..\/..\/..\/print-pdf.html\?pageTitle=)(\w*)\+?(\w*)?\+?(\w*)?\+?(\w*)?\+?(\w*)?\+?(\w*)?\+?(\w*)?\+?(\w*)?\+?(\w*)?\+?(\w*)?", link)
            #print("Found Topic: {}".format(m.group(1)))                 # For debugging
            
            # There can be many groups, so we will take all groups except for group at index 0
            
            # Find lenght of sub list, count the number of subgroups
            subtopic.append(sub.groups())
            subtopic_str = " ".join(subtopic[0][1:])
            subtopic_str = subtopic_str.strip()
        
        except:
            pass
    
    return topic_str,subtopic_str


# In[4]:


# Creates links

# TODO:
    # Add support for language selection
    # Currently set to manual
    
def link_creation(list_links, language):
    """Returns list of links to extract text from"""
    link_extract = []    # List to store all the links created
    temp_list = []       # Temporary list to store all the numbers we get from regular expressions
    
    # Regular expressions to extract numbers
    for index, link in enumerate(list_links):
        try:
            number = re.match(r"(.\/..\/..\/..\/legal-content\/EN\/AUTO\/\?uri=legissum)\:(\w+?\d+_?\d+?)",link)
            temp_list.append(number.group(2))
            
        except:
            pass
    
    # Creating list of links to extract text from 
    for index, number in enumerate(temp_list):
        link_extract.append("https://eur-lex.europa.eu/legal-content/"+language+"/TXT/HTML/?uri=LEGISSUM:"+number+"&from="+language)

    return link_extract


# In[5]:


# Extraction function
store_list_success = []     # List to store all the links that were successfully extracted\
store_list_failure = []     # List to store all the links that were not successfully extracted\

def extraction(hyper_links, language):
    
    """Saves text in its native form from webpages
       Returns information regarding files """
    
    
    # Get topic and subtopic
    topic, subtopic = topic_and_subtopic(links)
        
    # stripping white spaces in topic and subtopic if any;
        
    topic = topic.replace(" ","")
    subtopic = subtopic.replace(" ","")
        
    # Saving the text in appropiate folder
    homedir = os.environ['HOME']

    dir_to_save = homedir+"/"+"Data_"+language+"/"+topic+"/"+subtopic
        
        
    try:
        os.stat(dir_to_save)
    except:
        os.makedirs(dir_to_save)
        
    log_file = open(dir_to_save+"/"+'log'+'.txt',"w")  #logging all the outputs to log file
    
    sys.stdout = log_file # Telling system to write all the print statements to log file
    
    for i, link in enumerate(hyper_links):
        print("URL for Extraction is: {}".format(link))
        try:
            htp = urllib.request.urlopen(link)
            print("Waiting for response from webpage:{}".format(link))
            
            soup = BeautifulSoup(htp, from_encoding=resp.info().get_param('charset'))
            
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    

            # get text
            text = soup.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Get the first line of text, that is the title of the summary
            title = text.split('\n', 1)[0]
    
                    
            print("Saving Text to the file: {}.txt".format(dir_to_save+"/"+title))
        
            with open(dir_to_save+"/"+title+'.txt', "w") as text_file:
                text_file.write(text)
                
            # As the file is written successfully, we will store this like to successfull list
            
            # Updating the 'store_list_success'
            store_list_success.append(link)
            
            
        except:
            print("Unable to open link: {}".format(link))
            
            # As we got no response from the webiste we are going to store the link in 'store_list_failure'
            
            # Updating the 'store_list_failure'
            store_list_failure.append(link)
            
            pass


for index, links in enumerate(lines):
    resp = urllib.request.urlopen(links)
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    
    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])
    
    # Topic and subtopic 
    topic, subtopic = topic_and_subtopic(links)
    
    print("Topic is:{} and Subtopic is:{}".format(topic, subtopic))
    
    # Creating links:
    print("Creating links for extraction...")
    
    extraction_links = link_creation(links,lang)      # Gets the list of links to extract contents from
        
    print("Link creation completet for topic:{} and subtopic:{}".format(topic, subtopic))
    
    # Extraction Process:
    print("Strating the extraction process...")
    
    #for index, links_2_extract in enumerate(extraction_links):
    extraction(extraction_links,lang)
    
    print("Extraction Process completed.")
    

    


# In[ ]:


# Storing the 'store_list_success' and 'store_list_failure' into text file
homedir = os.environ['HOME']
with open(homedir+"/"+"Data/"+"success.txt","a") as fileStore:
    fileStore.write("\n".join(store_list_success))

with open(homedir+"/"+"Data/"+"failure.txt","a") as file_Store:
    file_Store.write("\n".join(store_list_failure))
    

