from gensim.corpora import Dictionary
from gensim.models import LdaModel
from setting import corpus_path

news_content_cut = []
for line in open(corpus_path, 'r', encoding='utf-8'):
    news_content_cut.append(line)


print(news_content_cut)

