import os

stopwords_path = os.path.join(os.path.abspath('./'), 'data', 'stop_words.txt')
word2vec_path = os.path.join(os.path.abspath('./'), 'data', 'word2vec.model')
news_path = os.path.join(os.path.abspath('./'), 'data', 'sqlResult_1558435.csv')
words_frequence_path = os.path.join(os.path.abspath('./'), 'data', 'words_frequence.pk')

summary_ratio = 6