#!/usr/bin/env python
# coding: utf-8

# In[3]:
import os

os.getcwd()


# In[17]:


os.chdir("c:\\Users\\ROG\\Desktop\\test_ttds\\ttds-main\\app\\ml")


# In[25]:


import pandas as pd


base_df = pd.DataFrame()

clean_data_folder = "./Papers"

for filename in os.listdir(clean_data_folder):
    full_path1 = f"{clean_data_folder}/{filename}"
    for filename2 in os.listdir(full_path1):
        full_path = f"{clean_data_folder}/{filename}/{filename2}"
        print(full_path)
        
        # load data into a DataFrame
        new_df = pd.read_csv(full_path)

        # merge into the base DataFrame
        base_df = pd.concat([base_df, new_df])




# In[27]:


len(base_df)


# In[28]:


base_df.head()


# In[ ]:


base_df.columns


# In[ ]:


base_df['abstract'].shape


# In[ ]:


len(base_df['abstract'].values)


# In[ ]:


base_df['abstract'].values[0]


# In[ ]:


base_df['title'].values[0]


# In[ ]:


get_ipython().system('pip install keybert')
from keybert import KeyBERT


# In[ ]:


kw_model = KeyBERT()


# In[ ]:


keywords = kw_model.extract_keywords(base_df['abstract'].values[0])
keywords


# In[ ]:


keywords2 = kw_model.extract_keywords(base_df['title'].values[0])
keywords2


# In[ ]:


a = "Knowledge Graph Completion (KGC) has been proposed to improve Knowledge Graphs by filling in missing connections via link prediction or relation extraction. One of the main difficulties for KGC is a low resource problem. Previous approaches assume sufficient training triples to learn versatile vectors for entities and relations, or a satisfactory number of labeled sentences to train a competent relation extraction model. However, low resource relations are very common in KGs, and those newly added relations often do not have many known samples for training. In this work, we aim at predicting new facts under a challenging setting where only limited training instances are available. We propose a general framework called Weighted Relation Adversarial Network, which utilizes an adversarial procedure to help adapt knowledge/features learned from high resource relations to different but related low resource relations. Specifically, the framework takes advantage of a relation discriminator to distinguish between samples from different relations, and help learn relation-invariant features more transferable from source relations to target relations. Experimental results show that the proposed approach outperforms previous methods regarding low resource settings for both link prediction and relation extraction."


# In[ ]:


keyword = kw_model.extract_keywords(a)
keyword


# In[ ]:


a


# In[ ]:


t = "Relation Adversarial Network for Low Resource Knowledge Graph Completion"


# In[ ]:


keyword = kw_model.extract_keywords(t)
keyword


# In[ ]:




