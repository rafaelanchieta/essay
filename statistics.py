from collections import Counter

import numpy as np
import pandas as pd
from nltk import tokenize

from buil_dataset import Corpus
from essay import Essay


class Statistic:
    """
    Calculate some statistics about the corpus
    """

    def __init__(self, split):
        self.essay = split

    def statistics_essays(self) -> (float, float, float, float, float, float, float, float, float, float, float, float):
        """
        Compute some statistics about the corpus
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
        return (total_paragraphs / total_essays, total_sentences / total_paragraphs, total_sentences / total_essays,
                np.std(std_snt_per_para), np.std(std_snt_per_essay), np.std(std_para_by_essay),
                total_tok_snt / total_sentences, np.std(std_tok_per_snt), total_tok_par / total_paragraphs,
                np.std(std_tok_per_para), total_tok_par / total_essays, np.std(std_tok_per_essay))

    def competence_score(self) -> (Counter, Counter, Counter, Counter, Counter):
        """
        Get score for each competence
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
        return Counter(c1), Counter(c2), Counter(c3), Counter(c4), Counter(c5)

    def statistics_score(self) -> pd:
        """
        Get total score of essays
        :return: total scores ordered
        """
        return self.essay['score'].value_counts(sort=False)


if __name__ == '__main__':
    essay = Essay().get_essay()
    train, dev, test = Corpus().read_corpus()
    statistic = Statistic(train)
    # print(statistic.statistics_score())
    # statistic.competence_score()
    # statistic.statistics_essays()
