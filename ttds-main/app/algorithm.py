import re
import pickle
from stemming.porter2 import stem
from collections import defaultdict
from math import log10


# tokenization
def preprocessing(text):
    words = []
    words.extend(re.findall(r'[\w]+', text))
    words = [word.lower() for word in words]
    words = [stem(word) for word in words]
    return words


# Boolean operator
def op_not(docs_list, inverted_idx):
    docs = set()
    for word in inverted_idx:
        for artist, index in inverted_idx[word]:
            docs.add((artist, index))
    docs_diff = docs.difference(docs_list)
    return sorted(list(docs_diff), key=lambda x: x[0])


def op_and(a, b):
    res = set(a).intersection(set(b))
    return sorted(list(res), key=lambda x: x[0])


def op_or(a, b):
    res = set(a).union(set(b))
    return sorted(list(res), key=lambda x: x[0])


# search method
def word_search(inverted_idx, word):
    docs_list = []
    word = stem(word.lower())
    if word in inverted_idx:
        for artist, index in inverted_idx[word]:
            docs_list.append((artist, index))

    return docs_list


def proximity_search(inverted_idx, word_1, word_2, proximity=1):
    res = []
    word_1 = stem(word_1.lower())
    word_2 = stem(word_2.lower())
    if word_1 in inverted_idx and word_2 in inverted_idx:
        for (artist, index) in inverted_idx[word_1]:
            if (artist, index) not in inverted_idx[word_2]:
                continue
            else:
                pos_1 = inverted_idx[word_1][artist, index]
                pos_2 = inverted_idx[word_2][artist, index]
                i = 0
                j = 0

                while i < len(pos_1) and j < len(pos_2):
                    if pos_1[i] > pos_2[j] + proximity:
                        j += 1
                    elif pos_1[i] < pos_2[j] - proximity:
                        i += 1
                    else:
                        res.append((artist, index))
                        break
    return res


def phrase_search(inverted_idx, query):
    is_not = False
    if query.find('#') != -1:
        start = query.index('(')
        end = query.index(')')
        proximity = int(query[query.index('#') + 1: start])
        p = query[start + 1: end].replace(',', ' ').split()
        return proximity_search(inverted_idx, p[0], p[1], proximity)
    elif query.find('NOT') != -1:
        query = query.replace('NOT', '')
        is_not = True

    words = query.replace('"', ' ').split()

    if len(words) == 1:
        res = word_search(inverted_idx, words[0])
    else:
        res = word_search(inverted_idx, words[0])
        words = [stem(word.lower()) for word in words]
        for k in range(0, len(words) - 1):
            res_k = []
            if words[k] in inverted_idx and words[k + 1] in inverted_idx:
                for (artist, index) in inverted_idx[words[k]]:
                    if (artist, index) not in inverted_idx[words[k + 1]]:
                        continue
                    else:
                        pos_1 = inverted_idx[words[k]][artist, index]
                        pos_2 = inverted_idx[words[k + 1]][artist, index]
                        i = 0
                        j = 0

                        while i < len(pos_1) and j < len(pos_2):
                            if pos_1[i] < pos_2[j]:
                                if pos_1[i] + 1 == pos_2[j]:
                                    res_k.append((artist, index))
                                    break
                                else:
                                    i += 1
                            elif pos_1[i] > pos_2[j]:
                                j += 1

            res = op_and(res, res_k)

    if is_not:
        res = op_not(res, inverted_idx)
    return res


def evaluate(query):
    q = re.split(" (AND|OR) ", query)
    res = []
    for elem in q:
        if elem[0] == '(' and elem[-1] == ')':
            res.append(elem[0])
            res.append(elem[1:-1])
            res.append(elem[-1])
        elif elem[0] == '(':
            res.append(elem[0])
            res.append(elem[1:])
        elif elem[-1] == ')':
            res.append(elem[:-1])
            res.append(elem[-1])
        else:
            res.append(elem)
    return res


def boolean_search(inverted_idx, query):
    def is_op(t):
        if t in ['AND', 'OR', '(', ')']:
            return True
        else:
            return False

    res = list()
    docs_stack = []
    ops_stack = []
    for i in range(len(query)):
        if query[i] == '(':
            ops_stack.append(query[i])
        elif not is_op(query[i]):
            docs_list = phrase_search(inverted_idx, query[i])
            docs_stack.append(docs_list)
        elif query[i] == ')':
            while len(ops_stack) != 0 and ops_stack[-1] != '(':
                docs_list1 = docs_stack.pop()
                docs_list2 = docs_stack.pop()
                op = ops_stack.pop()
                new_docs = []
                if op == 'OR':
                    new_docs = op_or(docs_list1, docs_list2)
                elif op == 'AND':
                    new_docs = op_and(docs_list1, docs_list2)
                docs_stack.append(new_docs)
            ops_stack.pop()
        else:
            ops_stack.append(query[i])

    while len(ops_stack) != 0:
        docs_list1 = docs_stack.pop()
        docs_list2 = docs_stack.pop()
        op = ops_stack.pop()
        new_docs = []
        if op == 'OR':
            new_docs = op_or(docs_list1, docs_list2)
        elif op == 'AND':
            new_docs = op_and(docs_list1, docs_list2)
        docs_stack.append(new_docs)
    res = docs_stack[-1]
    return res


def rank(query, inverted_index):
    tfidf = defaultdict(int)
    words = preprocessing(query)
    songs = set()
    for word in inverted_index:
        for (artist, index) in inverted_index[word]:
            songs.add((artist, index))
    songs_num = len(songs)
    for word in words:
        tf_dict = {}
        if word not in inverted_index:
            continue
        else:
            for (artist, index) in inverted_index[word]:
                tf_dict[artist, index] = len(inverted_index[word][artist, index])

            df = len(inverted_index[word])
            for (artist, index) in tf_dict:
                tfidf[artist, index] += (1 + log10(tf_dict[artist, index])) * log10(songs_num / df)

    sorted_tfidf = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)
    return sorted_tfidf


def rank_BM25(query, docs, inv_idx_docs, idx_docs):
    tf = defaultdict(float)
    idf = defaultdict(float)
    tfidf = defaultdict(float)
    words = preprocessing(query)
    k1 = 1.5
    b = 0.75

    songs_num = len(docs)
    docs_len = {}
    avg_len = 0.0
    for (artist, index) in idx_docs:
        docs_len[artist, index] = 0
        for word in idx_docs[artist, index]:
            docs_len[artist, index] += idx_docs[artist, index][word]

        avg_len += docs_len[artist, index]
    avg_len /= float(len(docs))

    for word in words:
        if word not in inv_idx_docs:
            continue
        else:
            df = len(inv_idx_docs[word])
            idf[word] = log10((songs_num - df + 0.5) / (df + 0.5))

    for (artist, index) in idx_docs:
        for word in words:
            if word not in idx_docs[artist, index]:
                continue
            else:
                tf[word] = idx_docs[artist, index][word] / docs_len[artist, index]
                K = k1 * (1 - b + b * docs_len[artist, index] / avg_len)
                tfidf[artist, index] += tf[word] * (k1 + 1) / (tf[word] + K) * idf[word]
    sorted_tfidf = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)
    return sorted_tfidf


def algorithm(choice, query):
    with open('./app/ml_data/pickle/title.pickle', 'rb') as f:
        title = pickle.load(f)
    with open('./app/ml_data/pickle/title_reverse_indexer.pickle', 'rb') as f:
        title_reverse_indexer = pickle.load(f)
    with open('./app/ml_data/pickle/title_words_count.pickle', 'rb') as f:
        title_words_count = pickle.load(f)

    with open('./app/ml_data/pickle/conference.pickle', 'rb') as f:
        conference = pickle.load(f)
    with open('./app/ml_data/pickle/conference_reverse_indexer.pickle', 'rb') as f:
        conference_reverse_indexer = pickle.load(f)
    with open('./app/ml_data/pickle/conference_words_count.pickle', 'rb') as f:
        conference_word_counts = pickle.load(f)

    with open('./app/ml_data/pickle/abstract.pickle', 'rb') as f:
        abstract = pickle.load(f)
    with open('./app/ml_data/pickle/abstract_reverse_indexer.pickle', 'rb') as f:
        abstract_reverse_indexer = pickle.load(f)
    with open('./app/ml_data/pickle/abstract_words_count.pickle', 'rb') as f:
        abstract_word_counts = pickle.load(f)

    with open('./app/ml_data/pickle/topic_related_words.pickle', 'rb') as f:
        topic_related_words = pickle.load(f)
    with open('./app/ml_data/pickle/citations.pickle', 'rb') as f:
        citations = pickle.load(f)

    res = dict()
    i = 1
    if choice == 'song':
        p = re.split(r' (AND|OR) ', query)
        q = query
        q = q.replace('AND', ' ')
        q = q.replace('OR', ' ')
        q = q.replace('NOT', ' ')

        tfidf = rank_BM25(q, title, title_reverse_indexer, title_words_count)

        if len(p) == 1:
            search_result = phrase_search(title_reverse_indexer, query)
            for (artist, index), tfidf_value in tfidf:
                if (artist, index) in search_result:
                    line = [title[artist, index], artist, conference[artist, index], 
                            " ".join(topic_related_words[artist, index])]
                    res[i] = line
                    i += 1
            for (artist, index), tfidf_value in tfidf:
                if (artist, index) not in search_result:
                    line = [title[artist, index], artist, conference[artist, index], 
                            " ".join(topic_related_words[artist, index])]
                    res[i] = line
                    i += 1
        else:
            query = evaluate(query)
            search_result = boolean_search(title_reverse_indexer, query)
            for (artist, index), tfidf_value in tfidf:
                if (artist, index) in search_result:
                    line = [title[artist, index], artist, conference[artist, index], 
                            " ".join(topic_related_words[artist, index])]
                    res[i] = line
                    i += 1
            for (artist, index), tfidf_value in tfidf:
                if (artist, index) not in search_result:
                    line = [title[artist, index], artist, conference[artist, index], 
                            " ".join(topic_related_words[artist, index])]
                    res[i] = line
                    i += 1

    elif choice == 'keyword':
        p = re.split(r' (AND|OR) ', query)
        q = query
        q = q.replace('AND', ' ')
        q = q.replace('OR', ' ')
        q = q.replace('NOT', ' ')
        tfidf = rank_BM25(q, abstract, abstract_reverse_indexer, abstract_word_counts)
        if len(p) == 1:
            search_result = phrase_search(abstract_reverse_indexer, query)
            for (artist, index), tfidf_value in tfidf:
                print(artist)
                if (artist, index) in search_result:
                    line = [title[artist, index], artist, conference[artist, index], 
                            " ".join(topic_related_words[artist, index]),citations[artist, index]]
                    res[i] = line
                    i += 1
            for (artist, index), tfidf_value in tfidf:
                if (artist, index) not in search_result:
                    line = [title[artist, index], artist, conference[artist, index], 
                            " ".join(topic_related_words[artist, index]),citations[artist, index]]
                    res[i] = line
                    i += 1
        else:
            query = evaluate(query)
            search_result = boolean_search(abstract_reverse_indexer, query)
            for (artist, index), tfidf_value in tfidf:
                if (artist, index) in search_result:
                    line = [title[artist, index], artist, conference[artist, index], 
                            " ".join(topic_related_words[artist, index]),citations[artist, index]]
                    res[i] = line
                    i += 1
            for (artist, index), tfidf_value in tfidf:
                if (artist, index) not in search_result:
                    line = [title[artist, index], artist, conference[artist, index], 
                            " ".join(topic_related_words[artist, index]),citations[artist, index]]
                    res[i] = line
                    i += 1

    return res