from collections import Counter
from typing import Tuple, List

import numpy as np
import seaborn as sns
import spacy
from matplotlib import pyplot as plt
from nltk import tokenize
from pandas import DataFrame
from tqdm import tqdm

from build_dataset import Corpus


class Statistic:
    """
    Calculates some statistics about the corpus
    """

    def __init__(self, split):
        self.essay = split
        self.nlp = spacy.load('pt_core_news_sm')

    def statistics_essays(self) -> List[Tuple]:
        """
        Computes some statistics about the corpus
        :return: average of paragraphs per essay, average of sentences per paragraph, average of sentences per essay
        standard deviation of sentences by paragraph, standard deviation of sentences by essay,
        standard deviation of paragraphs by essay, average of tokens per sentences,
        standard deviation of tokens per sentence, average of tokens per paragraphs,
        standard deviation of tokens per paragraph, average of tokens per essays, standard deviation of tokens per essay
        """
        total_essays = len(self.essay['essay'])
        total_paragraphs, total_sentences = 0, 0
        total_tok_ess, total_tok_par, total_tok_snt = 0, 0, 0
        std_para_by_essay, std_snt_per_para, std_snt_per_essay = [], [], []
        std_tok_per_essay, std_tok_per_para, std_tok_per_snt = [], [], []
        for paragraphs in self.essay['essay']:
            total_paragraphs += len(paragraphs)
            std_para_by_essay.append(len(paragraphs))
            aux_snt, aux_tok = 0, 0
            for paragraph in paragraphs:
                sentences = tokenize.sent_tokenize(paragraph, language='portuguese')
                total_sentences += len(sentences)
                std_snt_per_para.append(len(sentences))
                aux_snt += len(sentences)
                tokens_para = tokenize.word_tokenize(paragraph, language='portuguese')
                total_tok_par += len(tokens_para)
                std_tok_per_para.append(len(tokens_para))
                aux_tok += len(tokens_para)
                for snt in sentences:
                    tokens = tokenize.word_tokenize(snt, language='portuguese')
                    total_tok_snt += len(tokens)
                    std_tok_per_snt.append(len(tokens))
            std_snt_per_essay.append(aux_snt)
            std_tok_per_essay.append(aux_tok)
        return [('para_per_essay', total_paragraphs / total_essays),
                ('snt_per_para', total_sentences / total_paragraphs), ('snt_per_essay', total_sentences / total_essays),
                ('std_snt_per_para', np.std(std_snt_per_para)), ('std_snt_per_essay', np.std(std_snt_per_essay)),
                ('std_para_per_essay', np.std(std_para_by_essay)), ('tok_per_snt', total_tok_snt / total_sentences),
                ('std_tok_per_snt', np.std(std_tok_per_snt)), ('tok_per_para', total_tok_par / total_paragraphs),
                ('std_tok_per_para', np.std(std_tok_per_para)), ('tok_per_essay', total_tok_par / total_essays),
                ('std_tok_per_essay',np.std(std_tok_per_essay))]

    def forms_of_voice(self) -> Tuple[int, int]:
        """
        Computes forms of voice
        """
        active_voice, passive_voice = 0, 0
        for essay in tqdm(self.essay['essay']):
            for paragraph in essay:
                sentences = tokenize.sent_tokenize(paragraph, language='portuguese')
                for sentence in sentences:
                    doc = self.nlp(sentence)
                    for snt in doc.sents:
                        for child in snt.root.children:
                            if child.dep_ != 'nsubj':
                                passive_voice += 1
                            else:
                                active_voice += 1
                            break
        return active_voice, passive_voice

    def competence_score(self) -> List[Counter]:
        """
        Gets score for each competence
        :return: Competencies scores
        """
        competencies = self.essay['competence']
        c1, c2, c3, c4, c5 = [], [], [], [], []
        for c in competencies:
            c1.append(c[0])
            c2.append(c[1])
            c3.append(c[2])
            c4.append(c[3])
            c5.append(c[4])
        return [Counter(c1), Counter(c2), Counter(c3), Counter(c4), Counter(c5)]

    def statistics_score(self) -> DataFrame:
        """
        Gets total score of essays
        :return: total scores ordered
        """
        return self.essay['score'].value_counts(sort=False)

    def plot_score(self, top: int) -> None:
        """
        Plots the top X scores of the corpus
        :param top: number of scores to be ploted
        :return:
        """
        total_scores = self.essay['score'].value_counts()
        top_scores = total_scores[:top, ]
        plot = sns.barplot(top_scores.index, top_scores.values)
        for p in plot.patches:
            plot.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center',
                          va='center', xytext=(0, 10), textcoords='offset points')
        plt.show()


if __name__ == '__main__':
    train, dev, test = Corpus().read_splits()
    statistic = Statistic(train)
    # print(statistic.statistics_score())
    # statistic.competence_score()
    # print(statistic.statistics_essays())
    statistic.plot_score(10)
