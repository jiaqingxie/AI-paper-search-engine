# -*- coding: utf-8 -*-

import pandas as pd
import os
from nltk.stem import PorterStemmer
import string
from collections import Counter
import math
import collections
import re
from itertools import combinations_with_replacement

'''
base_df = pd.DataFrame()

clean_data_folder = "/Users/yuchenni/Desktop/AI-paper-search-engine-main/Papers"

for filename in os.listdir(clean_data_folder):
    full_path1 = f"{clean_data_folder}/{filename}"
    for filename2 in os.listdir(full_path1):
        full_path = f"{clean_data_folder}/{filename}/{filename2}"
        print(full_path)
        
        # load data into a DataFrame
        new_df = pd.read_csv(full_path)

        # merge into the base DataFrame
        base_df = pd.concat([base_df, new_df])
        
        
# base_df.to_csv(f"/Users/yuchenni/Desktop/AI-paper-search-engine-main/Papers/papers.csv", index=False)

base_df['abstract'][:10]

rslt_df = base_df[base_df['abstract'] != 'None']

rslt_df['abstract'][0]

fist = 'In this paper we present a state estimation method based on an inertial measurement unit (IMU) and a planar laser range finder suitable for use in real-time on a fixed-wing micro air vehicle (MAV). The algorithm is capable of maintaing accurate state estimates during aggressive flight in unstructured 3D environments without the use of an external positioning system. Our localization algorithm is based on an extension of the Gaussian Particle Filter. We partition the state according to measurement independence relationships and then calculate a pseudo-linear update which allows us to use 20x fewer particles than a naive implementation to achieve similar accuracy in the state estimate. We also propose a multi-step forward fitting method to identify the noise parameters of the IMU and compare results with and without accurate position measurements. Our process and measurement models integrate naturally with an exponential coordinates representation of the attitude uncertainty. We demonstrate our algorithms experimentally on a fixed-wing vehicle flying in a challenging indoor environment.'
'''



base_df = pd.read_csv("/Users/yuchenni/Desktop/AI-paper-search-engine-main/Papers/papers.csv")
rslt_df = base_df[base_df['abstract'] != 'None']
rslt_df = rslt_df.astype({"abstract": str}, errors='raise')
rslt_df = rslt_df.query('abstract.str.len() >= 5 ')



class Load_Data:
    def __init__(self,filepath):
        self.filepath = filepath
        
    def load_txt(self):
        return open(self.filepath, encoding='utf-8-sig').read()
    
    '''
    def load_xml(self):
        tree = ET.parse(self.filepath)
        root = tree.getroot()
        return root
    '''
    
    def load_query_txt(self):
        with open(self.filepath, encoding='utf-8-sig') as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
        return lines
    
    def read_queries(self):
        with open(self.filepath, encoding='utf-8-sig') as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
        print(lines)
        #lines_no_q = [x.split(' ', 1)[1:][0] for x in lines]
        lines_no_q = [x for x in lines]
        print(lines_no_q)
        
        #results2 = []
        
        results = []
        for t in lines_no_q:
            
            if t[0] == '#':
                t = re.sub(r'(?<=[,])(?=[^\s])', r' ', t)
                x = re.split(r"\s+(?=[^()]*(?:\(|$))", t) 
            elif t[0] == '"':
                x = re.findall(r'[^"\s]\S*|".+?"', t)
            else:
                x = t.split()
                
            results.append(x)
            
        return results
    
    

class Preprocessing:
    
    def __init__(self, string): # input as a string
        self.data = string

    def get_preprocessing_result(self):
        exclist = string.punctuation
        table_ = str.maketrans(exclist, ' '*len(exclist))
        newtext = ' '.join(self.data.translate(table_).split())
        token_lower = newtext.lower().split()

        with open("englishST.txt", 'r', encoding='utf-8-sig') as f:
            lines = [line.rstrip() for line in f]

        s = set(lines)
        result = [x for x in token_lower if x not in s]
        ps = PorterStemmer()
        stemming_words = []
        for w in result:
            stemming_words.append(ps.stem(w))
        return stemming_words
    
'''
doc_id = list(rslt_df.index)

list_preprocessing_ab = []
for i in range(len(rslt_df['abstract'])):
    p = Preprocessing(str(rslt_df.iloc[i]['abstract']))
    r = p.get_preprocessing_result()
    list_preprocessing_ab.append(r)
    

list_preprocessing_ti = []
for i in range(len(rslt_df['title'])):
    p = Preprocessing(str(rslt_df.iloc[i]['title']))
    r = p.get_preprocessing_result()
    list_preprocessing_ti.append(r)
'''

class Positional_Inverted_Index:
    
    def __init__(self, root, ab_or_ti):
        base_df = pd.read_csv(root)
        rslt_df = base_df[base_df[ab_or_ti] != 'None']
        rslt_df = rslt_df.astype({ab_or_ti: str}, errors='raise')
        self.rslt_df = rslt_df.query(ab_or_ti+'.str.len() >= 5 ')
        
        self.doc_id = list(self.rslt_df.index)

        self.list_preprocessing = [] # this is matrix
        for i in range(len(self.rslt_df[ab_or_ti])):
            p = Preprocessing(str(self.rslt_df.iloc[i][ab_or_ti]))
            r = p.get_preprocessing_result()
            self.list_preprocessing.append(r)
            

        self.result = {}

        for doc_id, doc in zip(self.doc_id, self.list_preprocessing):
            for word in set(doc):
                inside_dic = {}
                inside_dic.setdefault(doc_id, [])
                inside_dic[doc_id] = [word_position + 1 for word_position, w in enumerate(doc) if w == word]
                self.result.setdefault(word, []).append(inside_dic)

        self.ordered_result = collections.OrderedDict(sorted(self.result.items()))
        
    # 
    def get_pii(self): # use get_pii_no_df first 
        self.positional_inverted_index = {}
        for k in self.ordered_result:
            self.positional_inverted_index[(k,len(self.ordered_result[k]))] = self.ordered_result[k]
        return self.positional_inverted_index
             
    def bool_n(self, token):
        nor_token = Preprocessing(token).get_preprocessing_result()
        return [ list(x.keys())[0] for x in self.ordered_result[nor_token[0]]]
    
    def bool_not(self, word):
        return [ x  for x in self.doc_ids if x not in word ]
        
    def bool_and(self,w1, w2):
        return [ x for x in w1 if x in w2]
    
    def bool_or(self,w1, w2):
        jointed = w1 + w2
        new = list(set(jointed))
        new.sort(key=int)
        return new
    
    def tf_idf(self,tokens): 
        N = len(self.doc_id)
        doc_position = []
        for t in tokens:
            doc_position.append(self.ordered_result[t])
        list_list_w =[]    
        for t in doc_position:
            df = len(t)
            idf = math.log10(N/df)
            w_list= []
            for d in t:
                tf = len(list(d.values())[0])
                w  = (1 + math.log10(tf)) * idf
                w_list.append((int(list(d.keys())[0]),w))
            list_list_w.append(w_list)
            
        flattened = [val for sublist in list_list_w for val in sublist] 
        # Converting it to a dictionary
        tup = {i:0 for i, v in flattened}
        for key, value in flattened:
            tup[key] = tup[key]+value
        # using map
        result = list(map(tuple, tup.items()))
        result.sort(key=lambda x:x[1], reverse=True)
        return result[:150]    
   
    def phrase_search(self, phrase):
        nor_tokens = Preprocessing(phrase).get_preprocessing_result()
        def get_tokens(self,nor_token):
            return [ list(x.keys())[0] for x in self.ordered_result[nor_token]]
        tokens_list = [get_tokens(self, x)  for x in nor_tokens]
        doc_ids = self.bool_and(tokens_list[0],tokens_list[1])
        w1_positons = self.ordered_result[nor_tokens[0]]
        w2_positons = self.ordered_result[nor_tokens[1]]
       
        def get_positon(self, w_positons):
            w_positons_target=[]
            for i in doc_ids:
                for d in w_positons:
                    if i == list(d.keys())[0]:
                        w_positons_target.append(d)
                    
            return w_positons_target      
        w1_positons_target = get_positon(self, w1_positons)
        w2_positons_target = get_positon(self, w2_positons)
        result= []
        for x, y in zip (w1_positons_target, w2_positons_target):
            if len([p for p in list(x.values())[0] if p+1 in list(y.values())[0]]) != 0:
                result.append(list(x.keys())[0])
        
        return result
    
    def proximity_search(self, phrase):
        nor_tokens = Preprocessing(phrase).get_preprocessing_result()
        nor_tokens_split = [re.findall('(\d+|[A-Za-z]+)', x) for x in nor_tokens]
        flattened = [val for sublist in nor_tokens_split for val in sublist]
        words = flattened[1:]
        tokens_list = [self.bool_n(x)  for x in words]
        doc_ids = self.bool_and(tokens_list[0],tokens_list[1])
        w1_positons = self.ordered_result[words[0]]
        w2_positons = self.ordered_result[words[1]]
       
        def get_positon(self, w_positons):
            w_positons_target=[]
            for i in doc_ids:
                for d in w_positons:
                    if i == list(d.keys())[0]:
                        w_positons_target.append(d)
                    
            return w_positons_target      
        w1_positons_target = get_positon(self, w1_positons)
        w2_positons_target = get_positon(self, w2_positons)
        
        result= []
        for x, y in zip (w1_positons_target, w2_positons_target):
            for p in list(x.values())[0]:
                for pp in list(y.values())[0]:
                    if abs(pp-p) <= int(flattened[0]):
                        result.append(list(x.keys())[0])
                
        newlist = list(set(result))
        newlist.sort(key=int)
        return newlist
        
    def search_preprocessing(self, query):
        new = []
        for t in query:
            if t[0] =='"':
                t = self.phrase_search(t)
                new.append(t)
            elif t[0] == '#':
                t = self.proximity_search(t)
                new.append(t)
            elif t == "AND" or t =="OR" or t == "NOT" :
                new.append(t)        
            else:
               t  = self.bool_n(t)
               new.append(t)
        return new
    
    def search (self, query):
        q = self.search_preprocessing(query)
        for t in q :
            if t == "NOT":
                index = q.index(t)
                del q[index]        
                q[index]=self.bool_not(q[index])
                
        for t in q:
            if t == "AND":
                index = q.index(t)
                q[index] = self.bool_and(q[index-1], q[index+1])    
                del q[index+1]
                del q[index-1]
            if t == "OR":
                 index = q.index(t)
                 q[index] = self.bool_or(q[index-1], q[index+1])  
                 del q[index+1]
                 del q[index-1]   
        q = q[0]    
        return q
    
    def results_boolean(self,lines):
        self.final_results = []
        for l in lines:
            r = self.search(l)
            results = list(map(int, r))
            self.final_results.append(results)
        
        return self.final_results   
    def index_file(self):
        
        with open('index.txt', 'w') as f:
            for k in self.positional_inverted_index.keys():
                s = k[0]+":"+str(k[1])
                f.write(s)
                f.write('\n')

                for d in self.positional_inverted_index[k]:
                    docID = str(list(d.keys())[0])
                    f.write("\t"+docID+": ")
                    for p in list(d.values())[0]:
                        pos = str(p) + ", "
                        f.write(pos)
                    f.write('\n')
                     
    def boolean_file(self):
        doc_no = 1
        with open('results.boolean.txt', 'w') as f:
            for ls in self.final_results:
                for doc in ls:
                    s = str(doc_no)+','+str(doc)
                    f.write(s)
                    f.write('\n')
                    
                doc_no+=1
                
    def rank_scores(self,queries):   
        prep_data = []
        for q in queries:
            p = Preprocessing(q).get_preprocessing_result()
            prep_data.append(p)
        self.results_rank = []    
        for x in prep_data:
            self.results_rank.append(self.tf_idf(x))
        return self.results_rank    
    
    def rank_file(self):
        doc_no = 1
        with open('results.ranked.txt', 'w') as f:
            for ls in self.results_rank:
                for doc in ls:
                    s = str(doc_no)+','+str(doc[0])+","+str(('%.4f'%doc[1]))
                    f.write(s)
                    f.write('\n')
                    
                doc_no+=1
                
        
        


bool_query = Load_Data("queries.boolean.txt").read_queries()

# get phrase
pre_q = ''
for i in bool_query[0]:
    pre_q += ' ' + i
pre_q = '"'+pre_q+'"'
pre_q = [pre_q[:1]+pre_q[2:]]

# get and
pre_q_a = []
for i in bool_query[0]:
    pre_q_a.append(i)
    pre_q_a.append('AND')
pre_q_a = pre_q_a[:-1]

# get and or
comb = combinations_with_replacement(['AND','OR'], len(bool_query[0]))
a = list(comb)
pre_q_a_o = []




p_t = Positional_Inverted_Index("/Users/yuchenni/Desktop/AI-paper-search-engine-main/Papers/papers.csv", 'title')
pii_t = p_t.get_pii()
r1 = p_t.results_boolean(bool_query)
p_t.boolean_file()

r_q = ''
for i in bool_query[0]:
    r_q+=' '+i
    
r_q=r_q[1:]

p_t.rank_scores([r_q])
p_t.rank_file()


p_a = Positional_Inverted_Index("/Users/yuchenni/Desktop/AI-paper-search-engine-main/Papers/papers.csv", 'abstract')
pii_a = p_a.get_pii()
r2 = p_a.results_boolean(bool_query)
p_a.boolean_file()



'''
aaai_ls = []
acl_ls = []
cvpr_ls = []
emnlp_ls = []
iccv_ls = []
iclr_ls = []
icml_ls = []
icra_ls = []
kdd_ls = []
neurips_ls = []
sigir_ls = []
www_ls = []

   
for i in range(len(rslt_df['conference'])):
    if str(rslt_df.iloc[i]['conference']) == 'aaai':
        aaai_ls.append(list_preprocessing[i])
    elif str(rslt_df.iloc[i]['conference']) == 'acl':
        acl_ls.append(list_preprocessing[i])
    elif str(rslt_df.iloc[i]['conference']) == 'cvpr':
        cvpr_ls.append(list_preprocessing[i])
    elif str(rslt_df.iloc[i]['conference']) == 'emnlp':
        emnlp_ls.append(list_preprocessing[i])
    elif str(rslt_df.iloc[i]['conference']) == 'iccv':
        iccv_ls.append(list_preprocessing[i])
    elif str(rslt_df.iloc[i]['conference']) == 'iclr':
        iclr_ls.append(list_preprocessing[i])
    elif str(rslt_df.iloc[i]['conference']) == 'icml':
        icml_ls.append(list_preprocessing[i])
    elif str(rslt_df.iloc[i]['conference']) == 'icra':
        icra_ls.append(list_preprocessing[i])
    elif str(rslt_df.iloc[i]['conference']) == 'kdd':
        kdd_ls.append(list_preprocessing[i])
    elif str(rslt_df.iloc[i]['conference']) == 'neurips':
        neurips_ls.append(list_preprocessing[i])
    elif str(rslt_df.iloc[i]['conference']) == 'sigir':
        sigir_ls.append(list_preprocessing[i])
    elif str(rslt_df.iloc[i]['conference']) == 'www':
        www_ls.append(list_preprocessing[i])
    else:
        print('error')
    
    


import itertools

aaai_ls_f = list(itertools.chain(*aaai_ls))
acl_ls_f = list(itertools.chain(*acl_ls))
cvpr_ls_f = list(itertools.chain(*cvpr_ls))
emnlp_ls_f = list(itertools.chain(*emnlp_ls))
iccv_ls_f =list(itertools.chain(*iccv_ls))
iclr_ls_f = list(itertools.chain(*iclr_ls))
icml_ls_f = list(itertools.chain(*icml_ls))
icra_ls_f = list(itertools.chain(*icra_ls))
kdd_ls_f = list(itertools.chain(*kdd_ls))
neurips_ls_f = list(itertools.chain(*neurips_ls))
sigir_ls_f = list(itertools.chain(*sigir_ls))
www_ls_f = list(itertools.chain(*www_ls))


#uniq_ls = list(set(aaai_ls+acl_ls+cvpr_ls+emnlp_ls+iccv_ls+iclr_ls+icml_ls+icra_ls+kdd_ls+neurips_ls+sigir_ls+www_ls))


aaai_dic = Counter(aaai_ls_f)
acl_dic = Counter(acl_ls_f)
cvpr_dic = Counter(cvpr_ls_f)
emnlp_dic = Counter(emnlp_ls_f)
iccv_dic = Counter(iccv_ls_f)
iclr_dic = Counter(iclr_ls_f)
icml_dic = Counter(icml_ls_f)
icra_dic = Counter(icra_ls_f)
kdd_dic = Counter(kdd_ls_f)
neurips_dic = Counter(neurips_ls_f)
sigir_dic = Counter(sigir_ls_f)
www_dic = Counter(www_ls_f)

A,B,C,D,E,F,G,H,I,J,K,L = Counter(aaai_dic), Counter(acl_dic), Counter(cvpr_dic), Counter(emnlp_dic), Counter(iccv_dic),Counter(iclr_dic), Counter(icml_dic), Counter(icra_dic), Counter(kdd_dic), Counter(neurips_dic),Counter(sigir_dic), Counter(www_dic)
                             
total_dic = dict( A+B+C+D+E+F+G+H+I+J+K+L)                             


# Calculate Scores
def Corpus_scores(corpus_dic): # aaai_ls = corpus_NT

        MI_dic = {}
        Chi_square_dic = {}
        # divide into one corpus and the other
        
        A,B,C,D,E,F,G,H,I,J,K,L = Counter(aaai_dic), Counter(acl_dic), Counter(cvpr_dic), Counter(emnlp_dic), Counter(iccv_dic),Counter(iclr_dic), Counter(icml_dic), Counter(icra_dic), Counter(kdd_dic), Counter(neurips_dic),Counter(sigir_dic), Counter(www_dic)
        
        # len(aaai_ls)+len(acl_ls)+len(cvpr_ls)+len(emnlp_ls)+len(iccv_ls)+len(iclr_ls)+len(icml_ls)+len(icra_ls)+len(kdd_ls)+len(neurips_ls)+len(sigir_ls)+len(www_ls)
        if corpus_dic == aaai_dic:
            other_dic = dict(B+C+D+E+F+G+H+I+J+K+L)
            total_1 = len(aaai_ls)
            total_2 = len(acl_ls)+len(cvpr_ls)+len(emnlp_ls)+len(iccv_ls)+len(iclr_ls)+len(icml_ls)+len(icra_ls)+len(kdd_ls)+len(neurips_ls)+len(sigir_ls)+len(www_ls)
        elif corpus_dic == acl_dic:
            other_dic = dict(A+C+D+E+F+G+H+I+J+K+L)
            total_1 = len(acl_ls)
            total_2 = len(aaai_ls)+len(cvpr_ls)+len(emnlp_ls)+len(iccv_ls)+len(iclr_ls)+len(icml_ls)+len(icra_ls)+len(kdd_ls)+len(neurips_ls)+len(sigir_ls)+len(www_ls)
        elif corpus_dic == cvpr_dic:
            other_dic = dict(A+B+D+E+F+G+H+I+J+K+L)
            total_1 = len(cvpr_ls)
            total_2 = len(aaai_ls)+len(acl_ls)+len(emnlp_ls)+len(iccv_ls)+len(iclr_ls)+len(icml_ls)+len(icra_ls)+len(kdd_ls)+len(neurips_ls)+len(sigir_ls)+len(www_ls)
        elif corpus_dic == emnlp_dic:
            other_dic = dict(A+B+C+E+F+G+H+I+J+K+L)
            total_1 = len(emnlp_ls)
            total_2 = len(aaai_ls)+len(acl_ls)+len(cvpr_ls)+len(iccv_ls)+len(iclr_ls)+len(icml_ls)+len(icra_ls)+len(kdd_ls)+len(neurips_ls)+len(sigir_ls)+len(www_ls)
        elif corpus_dic == iccv_dic:
            other_dic = dict(A+B+C+D+F+G+H+I+J+K+L)
            total_1 = len(iccv_ls)
            total_2 = len(aaai_ls)+len(acl_ls)+len(cvpr_ls)+len(emnlp_ls)+len(iclr_ls)+len(icml_ls)+len(icra_ls)+len(kdd_ls)+len(neurips_ls)+len(sigir_ls)+len(www_ls)
        elif corpus_dic == iclr_dic:
            other_dic = dict(A+B+C+D+E+G+H+I+J+K+L)
            total_1 = len(iclr_ls)
            total_2 = len(aaai_ls)+len(acl_ls)+len(cvpr_ls)+len(emnlp_ls)+len(iccv_ls)+len(icml_ls)+len(icra_ls)+len(kdd_ls)+len(neurips_ls)+len(sigir_ls)+len(www_ls)
        elif corpus_dic == icml_dic:
            other_dic = dict(A+B+C+D+E+F+H+I+J+K+L)
            total_1 = len(icml_ls)
            total_2 = len(aaai_ls)+len(acl_ls)+len(cvpr_ls)+len(emnlp_ls)+len(iccv_ls)+len(iclr_ls)+len(icra_ls)+len(kdd_ls)+len(neurips_ls)+len(sigir_ls)+len(www_ls)
        elif corpus_dic == icra_dic:
            other_dic = dict(A+B+C+D+E+F+G+I+J+K+L)
            total_1 = len(icra_ls)
            total_2 = len(aaai_ls)+len(acl_ls)+len(cvpr_ls)+len(emnlp_ls)+len(iccv_ls)+len(iclr_ls)+len(icml_ls)+len(kdd_ls)+len(neurips_ls)+len(sigir_ls)+len(www_ls)
        elif corpus_dic == kdd_dic:
            other_dic = dict(A+B+C+D+E+F+G+H+J+K+L)
            total_1 = len(kdd_ls)
            total_2 = len(aaai_ls)+len(cvpr_ls)+len(emnlp_ls)+len(iccv_ls)+len(iclr_ls)+len(icml_ls)+len(icra_ls)+len(neurips_ls)+len(sigir_ls)+len(www_ls)
        elif corpus_dic == neurips_dic:
            other_dic = dict(A+B+C+D+E+F+G+H+I+K+L)
            total_1 = len(neurips_ls)
            total_2 = len(aaai_ls)+len(cvpr_ls)+len(emnlp_ls)+len(iccv_ls)+len(iclr_ls)+len(icml_ls)+len(icra_ls)+len(kdd_ls)+len(sigir_ls)+len(www_ls)
        elif corpus_dic == sigir_dic:
            other_dic = dict(A+B+C+D+E+F+G+H+I+J+L)
            total_1 = len(sigir_ls)
            total_2 = len(aaai_ls)+len(cvpr_ls)+len(emnlp_ls)+len(iccv_ls)+len(iclr_ls)+len(icml_ls)+len(icra_ls)+len(kdd_ls)+len(neurips_ls)+len(www_ls)
        elif corpus_dic == www_dic:
            other_dic = dict(A+B+C+D+E+F+G+H+I+J+K)
            total_1 = len(www_ls)
            total_2 = len(aaai_ls)+len(cvpr_ls)+len(emnlp_ls)+len(iccv_ls)+len(iclr_ls)+len(icml_ls)+len(icra_ls)+len(kdd_ls)+len(neurips_ls)+len(sigir_ls)
        else:
            print('error')
        

        # total number of terms
        N = total_1 + total_2
        for term in total_dic.keys():
            if term in corpus_dic.keys():
                # compute MI score
                N11 = corpus_dic[term]
                N01 = total_1 - N11
                if term in other_dic.keys():
                    N10 = other_dic[term]
                    N00 = total_2 - N10
                    print(N, N11, N01, N10, N00, total_1, total_2)
                    MI = N11 / N * math.log2(float(N * N11) / float((N10 + N11) * (N01 + N11))) \
                         + N01 / N * math.log2(float(N * N01) / float((N00 + N01) * (N01 + N11))) \
                         + N10 / N * math.log2(float(N * N10) / float((N10 + N11) * (N00 + N10))) \
                         + N00 / N * math.log2(float(N * N00) / float((N00 + N01) * (N00 + N10)))
                    
                else:
                    N10 = 0
                    N00 = total_2
                    MI = N11 / N * math.log2(float(N * N11) / float((N10 + N11) * (N01 + N11))) \
                         + N01 / N * math.log2(float(N * N01) / float((N00 + N01) * (N01 + N11))) \
                         + N00 / N * math.log2(float(N * N00) / float((N00 + N01) * (N00 + N10)))
                    
            else:
                
                N11 = 0
                N01 = total_1
                N10 = other_dic[term]
                N00 = total_2 - N10
                MI = N01/N*math.log2(float(N*N01) / float((N00+N01)*(N01+N11))) \
                     +N10/N*math.log2(float(N*N10) / float((N10+N11)*(N00+N10))) \
                     +N00/N*math.log2(float(N*N00) / float((N00+N01)*(N00+N10)))
                
            MI_dic[term] = MI
             #compute Chi_square score
            Chi_square = ((N11 + N10 + N01 + N00) * math.pow(N11 * N00 - N10 * N01, 2)) / (
                        (N11 + N01) * (N11 + N10) * (N10 + N00) * (N01 + N00))
            Chi_square_dic[term] = Chi_square
        return MI_dic, Chi_square_dic    



Corpus_scores(acl_dic)





'''
























#
    