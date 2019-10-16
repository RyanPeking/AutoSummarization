import os
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from util import get_stop_words

corpus_path = os.path.join(os.path.abspath('../'), 'data', 'corpus.txt')
stopwords_path = os.path.join(os.path.abspath('../'), 'data', 'stop_words.txt')

def get_train_set():
    stop_words = get_stop_words(stopwords_path)
    train_set = []
    for line in open(corpus_path, 'r', encoding='utf-8'):
        line = line.split()
        train_set.append([w for w in line if w not in stop_words])

    return train_set


def save_model(model_path):
    train_set = get_train_set()
    # 构建训练语料
    dictionary = Dictionary(train_set)
    corpus = [ dictionary.doc2bow(text) for text in train_set]

    # lda模型训练
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=100)
    lda.print_topics(100)

    lda.save(model_path)


if __name__ == '__main__':
    model_path = os.path.join(os.path.abspath('../'), 'data', 'news_lda.model')
    save_model(model_path)