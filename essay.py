
import os
import re
import pandas as pd

import numpy as np


class Essay:
    """
    Read and normalize all the essays from the Essay-BR corpus
    """

    def __init__(self):
        self.root = 'essay-br/all_essays/'

    def get_essay(self) -> pd:
        return self._get_essay()

    def _get_essay(self) -> pd:
        """
        Read files of the corpus and return a DataFrame
        :return: DataFrame with prompt, score, title, essay itself, and competencies

        Example:
            >>> self.get_essay()
                prompt      score   title   essay           competence
            0   violency    440     title   [paragraphs]    [80, 200, 120, 40]
            .   .       .                   .
        """
        essays = []

        for file in os.listdir(self.root):
            with open(os.path.join(self.root, file)) as f:
                content = {}
                paragraph, competencies = [], []
                for line in f.readlines():
                    if line.startswith('# prompt'):
                        content['prompt'] = line.split(':')[1].strip()
                    elif line.startswith('# title'):
                        content['title'] = re.sub(r'\[(.+)\]', '', line.split(':')[1].strip())
                    elif line.startswith('# C'):
                        competencies.append(normalize_score(format_score(line.split(':')[1].strip())))
                    elif not line.startswith('#'):
                        paragraph.append(line.strip())
                content['essay'] = paragraph
                content['competence'] = competencies
                content['score'] = int(np.sum(competencies))
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
    scores = [0, 40, 80, 120, 160, 200]
    value = score % 100
    if score not in scores:
        if score < 20:
            score = score - value
        elif 20 <= score < 50:
            score = score + 40 - value
        elif 50 <= score < 100:
            score = score + 80 - value
        elif 100 <= score < 150:
            score = score + 20 - value
        elif 150 <= score < 200:
            score = score + 60 - value
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
    e = Essay()
    print(e.get_essay())
