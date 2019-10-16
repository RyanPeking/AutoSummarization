import re
import jieba
from gensim.models.word2vec import Word2Vec


# 获取词向量：
def get_word2vec(word2vec_path):
    word2vec = Word2Vec.load(word2vec_path)
    return word2vec


# 加载停用词
def get_stop_words(stopwords_path):
    stop_words = []
    for line in open(stopwords_path, 'r', encoding='utf-8'):
        stop_words.append(line.replace('\n', ''))
    return stop_words


def cut(string): return ' '.join(jieba.cut(string))


def token(string): return re.findall(r'[\d|\w]+', string)


# 切句子
def split_sentence(original_text):
    original_text = original_text.replace('\r\n', '')
    sentences = re.split('([。?!！？.])', original_text) # split sentence
    new_sents = []
    for i in range(len(sentences) // 2):
        sent = sentences[2*i] + sentences[2*i+1]
        new_sents.append(sent)
    return new_sents


if __name__ == '__main__':
    pass

