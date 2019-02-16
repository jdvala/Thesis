#!/home/jay/miniconda3/envs/thesis/bin/python

"""
EUR-LEX parallel data scrapper, set the parallel languages and it will be good to go.
"""



# coding: utf-8
from urllib.request import urlopen as uReq
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import os
import time
import sys

LANG_1 = 'EN'
LANG_2 = 'DE'


with open(os.path.join(os.getcwd(),"links2.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]


valid_labels = ["Agriculture", "Audiovisual and media","Budget",
                "Competition","Consumers","Culture","Customs",
                "Developement","Economic and monetary affairs",
                "Education, training, youth","Education, training, youth, sport",
                "Employment and social policy","Energy","Enlargement","Enterprise",
                "Environment and climate change","Environment","External relations",
                "External trade","Humanitarian Aid and Civil Protection",
                "Fight against fraud","Food safety","Foreign and security policy",
                "Humanitarian aid","Human rights","Information society",
                "Institutional affairs","Internal market","Justice freedom security",
                "Maritime Affairs and Fisheries","Public health","Regional policy",
                "Research innovaion","Taxation","Research and innovation","Transport"]


def extractLinks(link):
    tmp_links = []
    page = uReq(link)
    soup = BeautifulSoup(page.read(), "html.parser")
    subTopic = re.sub(' - EUR-Lex', '', soup.title.string)
    subTopic = re.sub('["!<>\\\/:\?\*\|]', ' ', subTopic)
    for a in soup.find_all('a', href = re.compile(r'.*?uri=legissum:.*')):
        tmp_links.append(urljoin("https://eur-lex.europa.eu/", a['href']))
    return subTopic, tmp_links
    
def getTargetUrl(link):
    tmp_url_en = ""
    tmp_uel_de = ""
    
    page = uReq(link)
    
    soup = BeautifulSoup(page.read(), "html.parser")
    for a in soup.find_all('a', href = re.compile(r'.*/legal-content/'+LANG_1+'/TXT/HTML/.*')):
        tmp_url_en = urljoin("https://eur-lex.europa.eu/", a['href'])
    
    for a in soup.find_all('a', href = re.compile(r'.*/legal-content/'+LANG_2+'/TXT/HTML/.*')):
        tmp_url_de = urljoin("https://eur-lex.europa.eu/", a['href'])
    
    
    # for b in soup.find_all('a', href = re.compile(r'.*/legal-content/EN/ALL/.*')): 
    #     tmp_url_label = urljoin("https://eur-lex.europa.eu/",b['href'])
    
    return tmp_url_en , tmp_url_de

file_name = []
Topic = []
subtopic = []
multi_label = []

no_en = []
no_de = []

for link in content:
    
    topic = re.search(r"\/summary\/chapter\/(\w*_?\w*?_?\w*?)", link).group(1)
    subTopic, subTopicLinks =  extractLinks(link)
    for url in subTopicLinks:
        en, de = getTargetUrl(url)
        try:
            en_html = uReq(en)
            soup = BeautifulSoup(en_html.read(), "html.parser")

             # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            # get text
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            title = text.split('\n', 1)[0]
            title = re.sub('["!<>\\\/:\?\*\|]', '', title)
            title = title.strip()
            

            de_html = uReq(de)
            soup_de = BeautifulSoup(de_html.read(), "html.parser")
             # kill all script and style elements
            for script in soup_de(["script", "style"]):
                script.extract()
            # get text
            text_de = soup_de.get_text()
            lines_de = (line.strip() for line in text_de.splitlines())
            chunks_de = (phrase.strip() for line in lines_de for phrase in line.split("  "))
            text_de = '\n'.join(chunk for chunk in chunks_de if chunk)
            title_de = text_de.split('\n', 1)[0]
            title_de = re.sub('["!<>\\\/:\?\*\|]', '', title_de)
            title_de = title_de.strip()
        
        except:
            print("Something Wrong with {} or {} URL, skipping the docs...".format(LANG_1, LANG_2))
            pass
            
            file_name_en.append(title)
            file_name_de.append(title_de)
            Topic.append(topic)
            subtopic.append(subTopic)
            multi_label.append(set(tmp_label)) 

        directory = os.path.join(os.getcwd(),'scrapped_data',topic, subTopic.lower())
        if not os.path.exists(directory):
            print("creating directory "+directory)
            os.makedirs(directory)
        print("writing file: "+directory+"/"+title+".txt")
        f = open(directory+"/"+title+".txt", "w+", encoding="utf-8")
        f.write(text+'\n\n\n'+text_de)
        f.close()


# saving the lists to their respective pandas dataframe
import pandas as pd
print('Saving Pandas Dataframe')
dataframe = pd.DataFrame(data=list(zip(file_name_en, file_name_de,Topic, subtopic, multi_label)),columns=['file_name_en','file_name_de', 'topic', 'subtopic', 'multiple_label'])
other_info = pd.DataFrame(data=list(zip(no_text,no_multilabel)),columns= ['no_txt', 'no_label'])


dataframe.to_csv(os.path.join(os.getcwd(),'final.csv'))
other_info.to_csv(os.path.join(os.getcwd(),'other_info.csv'))

