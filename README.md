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

>>> train.loc[1:5 ['essay', 'score', 'competence']] 
>>>                                                 essay  score    competence
>>> 1  [Pode -se afirmar que a presença dos Jesuítas,...    480     [120, 120, 80, 80, 80]
>>> 2  [Em 13 de maio de 1888 veio ao Brasil a lei da...    440     [120, 80, 80, 80, 80]
>>> 3  [“Uma sociedade só progride quando um se mobil...    640     [120, 160, 120, 120, 120]
>>> 4  [Nas últimas décadas, o Brasil vem enfrentando...    560     [120, 120, 80, 120, 120]
>>> 5  [A previdência social trata-se de um seguro pú...    560     [120, 160, 80, 120, 80]

>>> valid.shape
>>> (686, 5)

>>> valid.loc[1:5 ['essay', 'score', 'competence']]
>>>                                                 essay  score    competence
>>> 1  [No Brasil atual algo que infelizmente acabou...     400     [120, 80, 80, 80, 40]
>>> 2  [Na Grécia antiga, houve um momento de forte s...    760     [160, 160, 120, 160, 160]
>>> 3  [Muito tem se falado nos noticiários à respeit...    440     [120, 80, 80, 120, 40]
>>> 4  [Segundo Aristóteles, toda organização social ...    720     [160, 120, 160, 160, 120]
>>> 5  [Quem educa a criança jamais punirá o adulto. ...    720     [160, 120, 120, 160, 160]

>>> test.shape
>>> (686, 5)

>>> test.loc[1:5 ['essay', 'score', 'competence']]
>>>                                                  essay  score   competence
>>> 1  [Todos nós sabemos que é impossível melhorar a...    600     [120, 120, 120, 120, 120]
>>> 2  [Recentemente, a pauta do foro especial por pr...    800     [200, 200, 200, 200, 0]
>>> 3  [O movimento antivacina vem acontecendo no mun...    480     [80, 120, 80, 120, 80]
>>> 4  [Vários momentos da História destacam situaçõe...    640     [120, 160, 120, 120, 120]
>>> 5  [No contexto atual, com o avanço tecnológico ...     600     [120, 120, 120, 120, 120]