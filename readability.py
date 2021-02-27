from collections import Counter

from typing import Tuple

import nlpnet
from nltk import RegexpTokenizer, tokenize
from tqdm import tqdm

from build_dataset import Corpus
from syllables import Silabizer


class Readability:
    """
    Calculates some readability statistics about the corpus
    """

    def __init__(self, essay):
        self.essay = essay
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.syllable = Silabizer()
        self.tagger = nlpnet.POSTagger('model/pos-pt/', language='pt')

    def compute_metrics(self) -> Tuple[float, float, float, float]:
        """
        Computes readability metrics
        """
        ttr, flesch, hapax, l_dens = 0, 0, 0, 0
        total = len(self.essay['essay'])
        for paragraphs in tqdm(self.essay['essay']):
            words, tokens, sentences = [], [], []
            for paragraph in paragraphs:
                sentences.extend(tokenize.sent_tokenize(paragraph, language='portuguese'))
                for sentence in sentences:
                    tokens.extend(tokenize.word_tokenize(sentence, language='portuguese'))
                    words.extend(self.tokenizer.tokenize(sentence))
            ttr += self.lexical_diversity(words)
            flesch += self.flesh_score(words, sentences)
            hapax += self.hapax_legomenon(tokens)
            l_dens += self.lexical_density(sentences, words)
        return ttr / total, flesch / total, hapax / total,  l_dens / total

    @staticmethod
    def lexical_diversity(words: list) -> float:
        """
        Computes lexical diversity
        """
        return len(set(words)) / len(words)

    def lexical_density(self, sentences: list, words: list) -> float:
        """
        Computes lexical density
        """
        open_class = []
        for sentence in sentences:
            for text, tag in self.tagger.tag(sentence)[0]:
                if tag == 'N' or tag == 'ADJ' or tag == 'ADV' or tag == 'IN' or tag == 'V' or tag == 'NPROP':
                    open_class.append(text)
        return len(open_class) / len(words)

    def flesh_score(self, words: list, sentences: list) -> float:
        """
        Computes flesch score
        """
        syllables = cont_syllables(words, self.syllable)
        return 206.835 - 1.015 * (len(words) / len(sentences)) - 84.6 * (syllables / len(words))

    @staticmethod
    def hapax_legomenon(tokens: list) -> float:
        """
        Computes hapax legomenon
        """
        count = Counter(tokens)
        hapax = sum(value == 1 for value in count.values())
        return hapax
        # return 100 * log(len(tokens)) / (1 - (hapax / len(list(set(tokens)))))


def cont_syllables(words: list, syllable: Silabizer) -> int:
    """
    Counts syllables
    """
    return len([syllable(word) for word in words])


if __name__ == '__main__':
    essay = Corpus().read_corpus()
    r = Readability(essay).compute_metrics()
    print(r)
