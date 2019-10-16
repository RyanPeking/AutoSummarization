from gensim.models import LdaModel
from gensim.corpora import Dictionary
from setting import news_lda_path, summary_ratio, stopwords_path, corpus_path
from LDA_model.build_lda_model import get_train_set
from util import get_stop_words, cut, token, split_sentence
from scipy.spatial.distance import cosine

def get_model():
    stop_words = get_stop_words(stopwords_path)
    train_set = []

    for line in open(corpus_path, 'r', encoding='utf-8'):
        line = line.split()
        train_set.append([w for w in line if w not in stop_words])

    lda = LdaModel.load(news_lda_path)
    dictionary = Dictionary(train_set)

    return stop_words, dictionary, lda


def get_ndarray(text_cut, stop_words, dictionary, lda):
    bow = dictionary.doc2bow([w for w in text_cut.split() if w not in stop_words ])
    ndarray = lda.inference([bow])[0]
#     print(ndarray[0])
    return ndarray[0]


def get_cos_with_content(sentence, content_ndarray, stop_words, dictionary, lda ):
    sentence_ndarray = get_ndarray(cut(''.join(token(sentence))), stop_words, dictionary, lda )

    return cosine(sentence_ndarray, content_ndarray)


def get_sentence_cos(original_text, title):
    stop_words, dictionary, lda = get_model()
    sentences = split_sentence(original_text)
    sentences_cos = {}

    if title:
        original_text += title
    content_ndarray = get_ndarray(cut(''.join(token(original_text))), stop_words, dictionary, lda)

    for i, sentence in enumerate(sentences):
        sentences_cos[i] = get_cos_with_content(sentence, content_ndarray, stop_words, dictionary, lda )

    return sentences, sentences_cos


def sentences_ranking(original_text, title):
    sentences, sentences_cos = get_sentence_cos(original_text, title)
    sentences_cos[0] /= 2
    ranking_sentences_id = sorted(sentences_cos.items(), key=lambda x: x[1])

    return ranking_sentences_id, sentences


def get_summarization_by_lda(original_text, title, summary_ratio=summary_ratio):
    #  summary_ratio为原文与摘要的比例

    # 正文不能为空
    if original_text == None:
        print('please input text')
        return None

    ranking_sentences_id, sentences = sentences_ranking(original_text, title)
    # if len(sentences) <= summary_ratio:
    #     return ''.join(sentences)
    candidate_sentences = [s[0] for s in ranking_sentences_id[:len(sentences)//summary_ratio + 1]]
    candidate_sentences = sorted(candidate_sentences)
    return ''.join([sentences[id] for id in candidate_sentences])


if __name__ == '__main__':
    text = '网易娱乐7月21日报道林肯公园主唱查斯特·贝宁顿 Chester Bennington于今天早上,在洛杉矶帕洛斯弗迪斯的一个私人庄园自缢身亡,年仅41岁。此消息已得到洛杉矶警方证实。洛杉矶警方透露, Chester的家人正在外地度假, Chester独自在家,上吊地点是家里的二楼。一说是一名音乐公司工作人员来家里找他时发现了尸体,也有人称是佣人最早发现其死亡。林肯公园另一位主唱麦克信田确认了 Chester Bennington自杀属实,并对此感到震惊和心痛,称稍后官方会发布声明。Chester昨天还在推特上转发了一条关于曼哈顿垃圾山的新闻。粉丝们纷纷在该推文下留言,不相信 Chester已经走了。外媒猜测,Chester选择在7月20日自杀的原因跟他极其要好的朋友Soundgarden(声音花园)乐队以及AudioslaveChris乐队主唱 Cornell有关,因为7月20日是 Chris CornellChris的诞辰。而 Cornell于今年5月17日上吊自杀,享年52岁。 Chris去世后, Chester还为他写下悼文。对于 Chester的自杀,亲友表示震惊但不意外,因为 Chester曾经透露过想自杀的念头,他曾表示自己童年时被虐待,导致他医生无法走出阴影,也导致他长期酗酒和嗑药来疗伤。目前,洛杉矶警方仍在调查Chester的死因。据悉, Chester与毒品和酒精斗争多年,年幼时期曾被成年男子性侵,导致常有轻生念头。 Chester生前有过2段婚姻,育有6个孩子。林肯公园在今年五月发行了新专辑《多一丝曙光OneMoreLight》,成为他们第五张登顶ilboard排行榜的专辑。而昨晚刚刚发布新单《 Talking To Myself》MV'
    title = None
    summarization = get_summarization_by_lda(text, title)
    print(summarization)

    title = '林肯公园主唱查斯特·贝宁顿 Chester Bennington自杀'
    summarization = get_summarization_by_lda(text, title)
    print(summarization)
