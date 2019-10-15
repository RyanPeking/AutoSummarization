import os
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence



corpus_path = os.path.join(os.path.abspath('../'), 'data', 'corpus.txt')
word2vec_path = os.path.join(os.path.abspath('../'), 'data', 'word2vec.model')

def save_word2vec(word2vec_path):
    if os.path.exists(word2vec_path):
        print('文件已存在, 请勿重复写入')
    else:
        w2v_model = Word2Vec(LineSentence(corpus_path), workers=4, min_count=5)
        w2v_model.save(word2vec_path)


if __name__ == '__main__':
    save_word2vec(word2vec_path)