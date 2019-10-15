import pickle
import pandas as pd
from collections import Counter
import os
from util import cut, token

news_path = os.path.join(os.path.abspath('../'), 'data', 'sqlResult_1558435.csv')
words_frequence_path = os.path.join(os.path.abspath('../'), 'data', 'words_frequence.pk')

def save_words_frequence(words_frequence_path):
    news_content = pd.read_csv(news_path, encoding='gb18030')
    news_content.dropna(subset=['content'], inplace=True)
    news_content.drop_duplicates(subset=['content'], inplace=True)
    news_content_cut = [token(n) for n in news_content['content']]
    news_content_cut = [''.join(n) for n in news_content_cut]
    news_content_cut = [cut(n) for n in news_content_cut]


    words = []
    for document in news_content_cut:
        words += [w for w in document.split()]

    words_counter = Counter(words)
    frequence = {w:count/len(words) for w, count in words_counter.items()}

    if os.path.exists(words_frequence_path):
        print('文件已存在, 请勿重复写入')
    else:
        with open(words_frequence_path, 'wb') as f:
            pickle.dump(frequence, f)



if __name__ == '__main__':
    save_words_frequence(words_frequence_path)

