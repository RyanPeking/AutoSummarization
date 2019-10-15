import re
from util import get_stop_words, split_sentence, cut, token
import jieba
import networkx as nx
import math
from setting import summary_ratio, stopwords_path


def get_connect_graph_by_weight_text_rank(original_text, title):
    sentences_graph = nx.Graph()
    sentences = split_sentence(original_text)
    sentences_cut = [cut(''.join(token(n))) for n in sentences]
    sentences_cut_del_stopwords = []
    stop_words = get_stop_words(stopwords_path)

    for s in sentences_cut:
        words = s.split()
        sentence_cut_del_stopwords = list(set(words) - set(stop_words))
        if sentence_cut_del_stopwords != []:
            sentences_cut_del_stopwords.append(sentence_cut_del_stopwords)

    is_title = False
    # 处理标题
    if title:
        title_cut = [cut(''.join(token(title)))]
        words = title_cut[0].split()
        title_cut_del_stopwords = list(set(words) - set(stop_words))
        if title_cut_del_stopwords != []:
            is_title = True
            sentences_cut_del_stopwords.insert(0, title_cut_del_stopwords)
            sentences.insert(0, title)

    for i, sentence in enumerate(sentences_cut_del_stopwords):
        for connect_id in range(i + 1, len(sentences_cut_del_stopwords)):
            # 求两个句子的相同词
            length_same_words = len(set(sentence).intersection(set(sentences_cut_del_stopwords[connect_id])))

            if is_title and (i == 0 or i == 1):
                # 如果是第一句double权重
                similiar = 2 * length_same_words / (
                        math.log(len(sentence)) + math.log(len(sentences_cut_del_stopwords[connect_id])))

            elif (not is_title) and i == 0:
                similiar = 2 * length_same_words / (
                        math.log(len(sentence)) + math.log(len(sentences_cut_del_stopwords[connect_id])))

            else:
                similiar = length_same_words / (
                            math.log(len(sentence)) + math.log(len(sentences_cut_del_stopwords[connect_id])))
            sentences_graph.add_edges_from([(i, connect_id)], weight=similiar)

    return sentences, sentences_graph, is_title


def sentences_ranking(original_text, title):
    sentences, sentences_graph, is_title = get_connect_graph_by_weight_text_rank(original_text, title)
    ranking_sentences_id = nx.pagerank(sentences_graph)
    if is_title:
        ranking_sentences_id.pop(0)
    ranking_sentences_id = sorted(ranking_sentences_id.items(), key=lambda x: x[1], reverse=True)
    return ranking_sentences_id, sentences


def get_summarization(original_text=None, title=None, summary_ratio=summary_ratio):
    '''
    :param original_text: 正文
    :param title: 标题
    :param summary_ratio: 压缩比，原文与摘要句子数量的比例
    :return:
    '''
    # 正文不能为空
    if original_text == None:
        print('please input text')
        return None

    ranking_sentences_id, sentences = sentences_ranking(original_text, title)
    # if len(sentences) <= summary_ratio:
    #     return ''.join(sentences)
    candidate_sentences = [s[0] for s in ranking_sentences_id[:len(sentences) // summary_ratio + 1]]
    candidate_sentences = sorted(candidate_sentences)

    return ''.join([sentences[id] for id in candidate_sentences])


if __name__ == '__main__':
    text = '网易娱乐7月21日报道林肯公园主唱查斯特·贝宁顿 Chester Bennington于今天早上,在洛杉矶帕洛斯弗迪斯的一个私人庄园自缢身亡,年仅41岁。此消息已得到洛杉矶警方证实。洛杉矶警方透露, Chester的家人正在外地度假, Chester独自在家,上吊地点是家里的二楼。一说是一名音乐公司工作人员来家里找他时发现了尸体,也有人称是佣人最早发现其死亡。林肯公园另一位主唱麦克信田确认了 Chester Bennington自杀属实,并对此感到震惊和心痛,称稍后官方会发布声明。Chester昨天还在推特上转发了一条关于曼哈顿垃圾山的新闻。粉丝们纷纷在该推文下留言,不相信 Chester已经走了。外媒猜测,Chester选择在7月20日自杀的原因跟他极其要好的朋友Soundgarden(声音花园)乐队以及AudioslaveChris乐队主唱 Cornell有关,因为7月20日是 Chris CornellChris的诞辰。而 Cornell于今年5月17日上吊自杀,享年52岁。 Chris去世后, Chester还为他写下悼文。对于 Chester的自杀,亲友表示震惊但不意外,因为 Chester曾经透露过想自杀的念头,他曾表示自己童年时被虐待,导致他医生无法走出阴影,也导致他长期酗酒和嗑药来疗伤。目前,洛杉矶警方仍在调查Chester的死因。据悉, Chester与毒品和酒精斗争多年,年幼时期曾被成年男子性侵,导致常有轻生念头。 Chester生前有过2段婚姻,育有6个孩子。林肯公园在今年五月发行了新专辑《多一丝曙光OneMoreLight》,成为他们第五张登顶ilboard排行榜的专辑。而昨晚刚刚发布新单《 Talking To Myself》MV'
    title = None
    summarization = get_summarization(text, title)
    print(summarization)

    title = '林肯公园主唱查斯特·贝宁顿 Chester Bennington自杀'
    summarization = get_summarization(text, title)
    print(summarization)