import pickle
import pandas as pd
import os
from util import cut, token

news_path = os.path.join(os.path.abspath('../'), 'data', 'sqlResult_1558435.csv')
corpus_path = os.path.join(os.path.abspath('../'), 'data', 'corpus.txt')

def save_words_frequence(corpus_path):
    news_content = pd.read_csv(news_path, encoding='gb18030')
    news_content.dropna(subset=['content'], inplace=True)
    news_content.drop_duplicates(subset=['content'], inplace=True)
    news_content_cut = [token(n) for n in news_content['content']]
    news_content_cut = [''.join(n) for n in news_content_cut]
    news_content_cut = [cut(n) for n in news_content_cut]


    words = []
    for document in news_content_cut:
        words += [w for w in document.split()]


    if os.path.exists(corpus_path):
        print('文件已存在, 请勿重复写入')
    else:
        with open(corpus_path, 'w', encoding='utf-8') as f:
            for sent_cut in news_content_cut:
                f.write(sent_cut)
                f.write('\n')



if __name__ == '__main__':
    save_words_frequence(corpus_path)