#!/home/jay/miniconda3/envs/thesis/bin/python

# coding: utf-8

# In[1]:


from urllib.request import urlopen as uReq
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import os
import sys


# In[2]:


with open("/home/jay/backup/Old_1/Thesis/links2.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]


# In[3]:


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
                "Research innovaion","Taxation","Research and innovation""Transport"]


# In[4]:


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
    tmp_url = ""
    tmp_url_label = ""
    page = uReq(link)
    soup = BeautifulSoup(page.read(), "html.parser")
    for a in soup.find_all('a', href = re.compile(r'.*/legal-content/EN/TXT/HTML/.*')):
        tmp_url = urljoin("https://eur-lex.europa.eu/", a['href'])
    
    for b in soup.find_all('a', href = re.compile(r'.*/legal-content/EN/ALL/.*')): 
        tmp_url_label = urljoin("https://eur-lex.europa.eu/",b['href'])
    
    return tmp_url , tmp_url_label


# In[18]:


import pandas as pd
dataframe = pd.DataFrame(columns=['file_name', 'topic', 'topic', 'multiple_label'])


# In[17]:


file_name = []
Topic = []
subtopic = []
multi_label = []

no_text = []
no_multilabel = []

for link in content:
    topic = re.search(r"\/summary\/chapter\/(\w*_?\w*?_?\w*?)", link).group(1)
    subTopic, subTopicLinks =  extractLinks(link)
    for url in subTopicLinks:
        
        target, target_for_label = getTargetUrl(url)
#         print(target_for_label)
#         sys.exit(0)
        try:
            target_html = uReq(target)
            soup = BeautifulSoup(target_html.read(), "html.parser")
        except:
            print('Something wrong with text url')
            no_text.append(target)
            
        
        try:
            target_label_html = uReq(target_for_label)
            soup_label = BeautifulSoup(target_label_html.read(), "html.parser")
        except:
            print("Something Wrong with label url-->> {}".format(target_label_html))
            no_multilabel.append(target_label_html)
            
        
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
        
        
        try:
            # extract the labels from the soup label
            tmp_label = []
            # get all the labels
            for span in soup_label.findAll('span', lang='en'):
                if span.text in valid_labels:
                    tmp_label.append(span.text)
            print("Labels for file:{} -->> {}".format(title, tmp_label))
            
#             dataframe.set_value(counter, 'file_name', title)
#             # Savinf topic, subtopic and labels
#             dataframe.set_value(counter, 'topic', topic)
#             dataframe.set_value(counter, 'subtopic', subTopic)
#             dataframe.set_value(counter, 'multiple_label', tmp_label)

            file_name.append(title)
            Topic.append(topic)
            subtopic.append(subTopic)
            multi_label.append(tmp_label) 


                
        except:
            print("Something wrong with label extraction")
            no_multilabel.append(target_label_html)
            
            
        directory = "/home/jay/output/"+topic+"/"+subTopic.lower()
        if not os.path.exists(directory):
            print("creating directory "+directory)
            os.makedirs(directory)
        print("writing file: "+directory+"/"+title+".txt")
        f = open(directory+"/"+title+".txt", "w+", encoding="utf-8")
        f.write(text)
        f.close()


# In[19]:


# saving the lists to their respective pandas dataframe
import pandas as pd
print('Saving Pandas Dataframe')
dataframe = pd.DataFrame(data,list(zip(file_name, Topic, subtopic, multi_label)),columns=['file_name', 'topic', 'topic', 'multiple_label'])
other_info = pd.DataFrame(data=list(zip(no_text,no_multilabel)),columns= ['no_txt', 'no_label'])


# In[21]:


dataframe.to_csv('/home/jay/final.csv')
other_info.to_csv('/home/jay/other_info.csv')

