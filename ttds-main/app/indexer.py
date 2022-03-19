import os
import re
import pandas as pd
import pickle
from stemming.porter2 import stem
from gensim import corpora, models


# tokenization
def preprocessing(text):
    words = []
    words.extend(re.findall(r'[\w]+', text))
    words = [word.lower() for word in words]
    words = [stem(word) for word in words]
    return words


class Indexer:

    def __init__(self):
        self.title, self.conference, self.abstract, self.title_reverse_indexer, self.conference_reverse_indexer, self.abstract_reverse_indexer, self.title_word_counts, self.conference_word_counts, self.abstract_word_counts,self.citations = self.build_index()

        self.topic_related_words = self.build_topic_list()

    @staticmethod
    def build_index():
        title, conference, abstract= dict(), dict(), dict()
        title_reverse_indexer, conference_reverse_indexer, abstract_reverse_indexer = dict(), dict(), dict()
        title_word_counts, conference_word_counts, abstract_word_counts = dict(), dict(), dict()
        citations = dict()
        
        for root, dirs, files in os.walk('./Papers/paper_collection'):
            
            subject = 'extended'
            for filename in files:
                if subject in filename:
                    papers = './Papers/paper_collection/' + filename
                    df = pd.read_csv(papers) 
                    authors = df['authors'].tolist()
                    
                    print(f"finished read {filename}...")
                else:
                    continue
                

                
                # process title
                for index, text in enumerate(df['title'].tolist()):
                    title[authors[index], index] = str(text)
                    words = preprocessing(title[authors[index], index])
                    for i in range(len(words)):
                        word = words[i]
                        pos = i
                        if word in title_reverse_indexer:
                            if (authors[index], index) in title_reverse_indexer[word]:
                                title_reverse_indexer[word][authors[index], index].append(pos)
                            else:
                                title_reverse_indexer[word][authors[index], index] = [pos]
                        else:
                            title_reverse_indexer[word] = {(authors[index], index): [pos]}

                        if (authors[index], index) in title_word_counts:
                            if word in title_word_counts[authors[index], index]:
                                title_word_counts[authors[index], index][word] += 1
                            else:
                                title_word_counts[authors[index], index][word] = 1
                        else:
                            title_word_counts[authors[index], index] = {word: 1}

                # process conference
                for index, text in enumerate(df['conference'].tolist()):
                    conference[authors[index], index] = str(text)
                    if conference[authors[index], index] == 'NaN' or conference[authors[index], index] == 'nan':
                        conference[authors[index], index] = ''
                    else:
                        words = preprocessing(conference[authors[index], index])
                        for i in range(len(words)):
                            word = words[i]
                            pos = i
                            if word in conference_reverse_indexer:
                                if (authors[index], index) in conference_reverse_indexer[word]:
                                    conference_reverse_indexer[word][authors[index], index].append(pos)
                                else:
                                    conference_reverse_indexer[word][authors[index], index] = [pos]
                            else:
                                conference_reverse_indexer[word] = {(authors[index], index): [pos]}

                            if (authors[index], index) in conference_word_counts:
                                if word in conference_word_counts[authors[index], index]:
                                    conference_word_counts[authors[index], index][word] += 1
                                else:
                                    conference_word_counts[authors[index], index][word] = 1
                            else:
                                conference_word_counts[authors[index], index] = {word: 1}

                # process abstract
                for index, text in enumerate(df['abstract'].tolist()):
                    abstract[authors[index], index] = str(text).replace(str(authors[index]), '')
                    words = preprocessing(abstract[authors[index], index])
                    for i in range(len(words)):
                        word = words[i]
                        pos = i
                        if word in abstract_reverse_indexer:
                            if (authors[index], index) in abstract_reverse_indexer[word]:
                                abstract_reverse_indexer[word][authors[index], index].append(pos)
                            else:
                                abstract_reverse_indexer[word][authors[index], index] = [pos]
                        else:
                            abstract_reverse_indexer[word] = {(authors[index], index): [pos]}

                        if (authors[index], index) in abstract_word_counts:
                            if word in abstract_word_counts[authors[index], index]:
                                abstract_word_counts[authors[index], index][word] += 1
                            else:
                                abstract_word_counts[authors[index], index][word] = 1
                        else:
                            abstract_word_counts[authors[index], index] = {word: 1}


                # process citations
                for index, text in enumerate(df['citations'].tolist()):
                    citations[authors[index], index] = str(text)
                    if citations[authors[index], index] == 'NaN' or citations[authors[index], index] == 'nan' or citations[authors[index], index] == 'None':
                        citations[authors[index], index] = ''

               

        title_reverse_indexer = dict(sorted(title_reverse_indexer.items(), key=lambda x: x[0]))
        conference_reverse_indexer = dict(sorted(conference_reverse_indexer.items(), key=lambda x: x[0]))
        abstract_reverse_indexer = dict(sorted(abstract_reverse_indexer.items(), key=lambda x: x[0]))
        return title, conference, abstract, title_reverse_indexer, conference_reverse_indexer, abstract_reverse_indexer, title_word_counts, conference_word_counts, abstract_word_counts,citations

    def build_topic_list(self):
        common_texts = []
        topic_related_words = {}

        with open('./englishST.txt', encoding='utf-8') as f:
            stop_words = f.read().split()
        for (authors, index) in self.abstract.keys():
            words = []
            words.extend(re.findall(r'[\w]+', self.abstract[authors, index]))
            words = [word.lower() for word in words]
            words = [word for word in words if word not in stop_words]
            common_texts.append(words)

        common_dictionary = corpora.Dictionary(common_texts)
        common_dictionary.filter_extremes(no_below=10, no_above=0.5, keep_n=10000, keep_tokens=None)
        bow = [common_dictionary.doc2bow(words) for words in common_texts]
        lda = models.LdaModel(bow, num_topics=100, id2word=common_dictionary, random_state=1)
        topics = lda.show_topics(num_topics=100, num_words=5, formatted=False)
        topics_words = [[word[0] for word in topic[1]] for topic in topics]
        for words, (authors, index) in zip(common_texts, self.abstract.keys()):
            doc_bow = common_dictionary.doc2bow(words)
           
            if lda[doc_bow] ==[]:
                pass
            else:
                topic_related_words[authors, index] = topics_words[lda[doc_bow][0][0]]
        return topic_related_words

    def store_data(self):
        print("Start loading")
        with open('./ml_data/pickle/title.pickle', 'wb') as f:
            pickle.dump(self.title, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open('./ml_data/pickle/title_reverse_indexer.pickle', 'wb') as f:
            pickle.dump(self.title_reverse_indexer, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open('./ml_data/pickle/title_words_count.pickle', 'wb') as f:
            pickle.dump(self.title_word_counts, f, protocol=pickle.HIGHEST_PROTOCOL)

        with open('./ml_data/pickle/conference.pickle', 'wb') as f:
            pickle.dump(self.conference, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open('./ml_data/pickle/conference_reverse_indexer.pickle', 'wb') as f:
            pickle.dump(self.conference_reverse_indexer, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open('./ml_data/pickle/conference_words_count.pickle', 'wb') as f:
            pickle.dump(self.conference_word_counts, f, protocol=pickle.HIGHEST_PROTOCOL)

        with open('./ml_data/pickle/abstract.pickle', 'wb') as f:
            pickle.dump(self.abstract, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open('./ml_data/pickle/abstract_reverse_indexer.pickle', 'wb') as f:
            pickle.dump(self.abstract_reverse_indexer, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open('./ml_data/pickle/abstract_words_count.pickle', 'wb') as f:
            pickle.dump(self.abstract_word_counts, f, protocol=pickle.HIGHEST_PROTOCOL)

        with open('./ml_data/pickle/topic_related_words.pickle', 'wb') as f:
            pickle.dump(self.topic_related_words, f, protocol=pickle.HIGHEST_PROTOCOL)

        with open('./ml_data/pickle/citations.pickle', 'wb') as f:
            pickle.dump(self.citations, f, protocol=pickle.HIGHEST_PROTOCOL)




indexer = Indexer()
indexer.store_data()