# Essay-BR
This repository contains essays written by high school Brazilian students.
These essays were graded by humans professionals following the criteria of the ENEM exam.

## Requirements

- Python (version 3.6 or later)
- `pip install -r requirements.txt`

## Usage
To read the corpus, simply following these steps:

````python
>>> from build_dataset import Corpus

>>> c = Corpus()
>>> c.read_corpus().shape
>>> (4570, 5)

>>> train, valid, test = c.read_splits()
>>> train.shape
>>> (3198, 5)

>>> valid.shape
>>> (686, 5)

>>> test.shape
>>> (686, 5)