
import os
import re
import pandas as pd


class Essay:
    """
    Read and normalize the Essay-BR corpus
    """

    def __init__(self):
        self.root = 'essay-br'
        self.essay = self._get_essay()

    def get_scores(self) -> pd:
        return self.essay['score']

    def get_essay(self) -> pd:
        return self.essay

    def _get_essay(self) -> pd:
        """
        Read files of the corpus and return a DataFrame
        :return: DataFrame with score, title, and essay itself

        Example:
            >>> self.get_essay()
                score   title               essay
            0   500     title of the essay  content of the essay
            .   .       .                   .
        """
        essays = []
        for file in os.listdir(self.root):
            with open(os.path.join(self.root, file)) as f:
                content = {}
                aux = []
                for i, line in enumerate(f):
                    if line.startswith('# score'):
                        score = line.split(':')[1].strip()
                        content['score'] = normalize_score(format_score(score))
                    elif i == 1:
                        content['title'] = re.sub(r'\[(.+)\]', '', line.strip())
                    else:
                        aux.append(line.strip())
                content['essay'] = ''.join(aux)
                essays.append(content)
        return pd.DataFrame(essays)


def normalize_score(score: int) -> int:
    """
    Normalize score ranging from 50
    :param score: the score of an essay
    :return: normalized score

    Example
        >>> normalize_score(10)
        0
        >>> normalize_score(30)
        50
        >>> normalize_score(60)
        50
        >>> normalize_score(70)
        100
    """
    value = score % 100
    if value != 50 and value != 0:
        if 40 <= value <= 60 or 20 <= value < 40:
            score = score + 50 - value
        elif value > 60:
            score = score + (100 - value)
        elif value < 20:
            score = score - value
    return score


def format_score(score: str) -> int:
    """
    Get a score and return a normalized integer score
    :param score: essay's score
    :return: normalized integer score

    Example:
        >>> format_score('9,5')
        950
    """
    if ',' in score:
        score = int(score.replace(',', '')) * 10
    elif '.' in score:
        score = int(score.replace('.', '')) * 10
    else:
        score = int(score)
    return score


if __name__ == '__main__':
    print(Essay().get_essay())
