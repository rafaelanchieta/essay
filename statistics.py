
import numpy as np
import pandas as pd
from nltk import tokenize

from essay import Essay


class Statistic:

    def __init__(self, essay):
        self.essay = essay

    def statistics_essay(self) -> (float, float, float, float, float, float):
        """
        Compute some statistics about the corpus
        :return: average of sentences per essay, average of tokens per sentence, standard deviation of sentences by
        essay, standard deviation of tokens per sentence, median of sentences per essay, and media of tokens per
        sentences
        """
        cont_sentences, cont_tokens = 0, 0
        lst_sentences, lst_tokens = [], []
        total = len(self.essay['essay'])
        for essay in self.essay['essay']:
            sentences = tokenize.sent_tokenize(essay, language='portuguese')
            lst_sentences.append(len(sentences))
            lst_tokens.append(self.number_of_tokens_per_sentence(sentences))
            cont_tokens += lst_tokens[-1]
            cont_sentences += lst_sentences[-1]
        return cont_sentences / total, cont_tokens / cont_sentences, np.std(lst_tokens), np.std(lst_sentences), \
               np.median(lst_tokens), np.median(lst_sentences)

    @staticmethod
    def number_of_tokens_per_sentence(sentences: list) -> int:
        tokens = 0
        for snt in sentences:
            tokens += len(tokenize.word_tokenize(snt, language='portuguese'))
        return tokens

    def statistics_score(self) -> pd:
        return self.essay['score'].value_counts(sort=False)


if __name__ == '__main__':
    essay = Essay().get_essay()
    statistic = Statistic(essay)
    snt, tok, std_tok, std_snt, med_tok, med_snt = statistic.statistics_essay()
    print(snt, std_snt, med_snt, tok, std_tok, med_tok)
    print(statistic.statistics_score())
