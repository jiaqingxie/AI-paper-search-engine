from time import perf_counter
import RAKE
import operator
import tqdm
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk import pos_tag, word_tokenize
from nltk.tag.stanford import StanfordPOSTagger
from nltk import StanfordTagger

nltk.download('averaged_perceptron_tagger')
jar = "ml/stanford-postagger.jar"
model = "ml/english-bidirectional-distsim.tagger"
stop_dir = "ml/SmartStoplist.txt" # load stopwords
stemmer = SnowballStemmer(language='english')

def Sort_Tuple(tup):
    tup.sort(key = lambda x: x[1])
    return tup

def stemsentence(arr):
    global stemmer
    return  " ".join([stemmer.stem(aa) for aa in arr.split(" ")])

def keyword_extractor(content):
    global jar, model, stop_dir

    rake_object = RAKE.Rake(stop_dir)
    keywords = Sort_Tuple(rake_object.run(content))[-10:][::-1] # Top 10 keywords (highest score --> more important, descending order)
    pos_tagger = StanfordPOSTagger(model, jar, encoding = "utf-8")
    
    result = []
    print("Preprocessing words for extraction...")
    t1 = perf_counter()
    for keyword in keywords:
        postag = pos_tagger.tag(word_tokenize(keyword[0]))
        k = []
        for (a, b) in postag:
            if not 'V' in b[0]: # and not 'J' in b[0]:
                k.append(a)
        if len(k)>1:
            result.append(" ".join(k))
            
    t2 = perf_counter()
    print(f"Finished preprocessing...time took {t2-t1} secs.\nStart to extract keywords...")
    
    result = list(set(result))
    
    res2 = result .copy()
    for i in range(len(result)):
        r = result[i]
        others = result[:i] + result[i+1:]
        r2 = "".join(stemsentence(r))
        others = "".join([stemsentence(other) for other in others])
        if r2 in others:
            res2.remove(r)
            
    return res2

if __name__ == "__main__":
    example = "Knowledge Graph Completion (KGC) has been proposed to improve Knowledge Graphs by filling in missing connections via link prediction or relation extraction. One of the main difficulties for KGC is a low resource problem. Previous approaches assume sufficient training triples to learn versatile vectors for entities and relations, or a satisfactory number of labeled sentences to train a competent relation extraction model. However, low resource relations are very common in KGs, and those newly added relations often do not have many known samples for training. In this work, we aim at predicting new facts under a challenging setting where only limited training instances are available. We propose a general framework called Weighted Relation Adversarial Network, which utilizes an adversarial procedure to help adapt knowledge/features learned from high resource relations to different but related low resource relations. Specifically, the framework takes advantage of a relation discriminator to distinguish between samples from different relations, and help learn relation-invariant features more transferable from source relations to target relations. Experimental results show that the proposed approach outperforms previous methods regarding low resource settings for both link prediction and relation extraction."
    print(keyword_extractor(example))