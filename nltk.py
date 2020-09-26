import pandas as pd
import nltk
import re
import numpy as np
from nltk.stem.snowball import SnowballStemmer
from sklearn.decomposition import LatentDirichletAllocation

lda = LatentDirichletAllocation(n_components=10)
from sklearn.feature_extraction.text import CountVectorizer

pd.set_option('display.max_rows', None, 'display.max_columns', None)

df = pd.read_csv("com.csv")
df.dropna(subset=["text"], inplace=True)
df.reset_index(drop=True, inplace=True)
stopwords = nltk.corpus.stopwords.words("english")

stemmer = SnowballStemmer("english")
data = df["text"].to_list()


def tokenization_and_stemming(text):
    tokens = []
    for word in nltk.word_tokenize(text):
        if word.lower() not in stopwords:
            tokens.append(word.lower())

    filtered_tokens = []

    for token in tokens:
        if re.search('[a-zA-z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


tfidf_model_lda = CountVectorizer(max_df=0.99,max_features=1000, stop_words="english",
                                  tokenizer=tokenization_and_stemming, ngram_range=(2, 3))
tfidf_matrix = tfidf_model_lda.fit_transform(data)
lda_output=lda.fit_transform(tfidf_matrix)
topic_names =["Topic"+str(i) for i in range(lda.n_components)]
doc_names = ["Doc" + str(i) for i in range(len(data))]

df_document_topic = pd.DataFrame(np.round(lda_output,2),columns=topic_names,index = doc_names)

topic = np.argmax(df_document_topic.values, axis=1)
df_document_topic['topic']=topic

df_topic_words = pd.DataFrame(lda.components_)

df_topic_words.columns = tfidf_model_lda.get_feature_names()
df_topic_words.index = topic_names

def print_topic_words(tfidf_model,lda_model,n_words):
    words = np.array(tfidf_model.get_feature_names())
    topic_words = []

    for topic_words_weights in lda_model.components_:
        top_words = topic_words_weights.argsort()[::-1][:n_words]
        topic_words.append(words.take(top_words))
    return topic_words

topic_keywords = print_topic_words(tfidf_model=tfidf_model_lda,lda_model=lda,n_words=10)

df_topic_words = pd.DataFrame(topic_keywords)
df_topic_words.columns = ["Word " + str(i) for i in range(df_topic_words.shape[1])]
df_topic_words.index = ["Topic "+str(i) for i in range(df_topic_words.shape[0])]
print(df_topic_words)
