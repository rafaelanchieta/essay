#!/usr/bin/env python3
# Based on Mabodo's ipython notebook (https://github.com/mabodo/sibilizador)
# (c) Mabodo
from nltk import tokenize


class CharLine:
    def __init__(self, word):
        self.word = word
        self.char_line = [(char, self.char_type(char)) for char in word]
        self.type_line = ''.join(chartype for char, chartype in self.char_line)

    @staticmethod
    def char_type(char):
        if char in {'a', 'á', 'e', 'é', 'o', 'ó', 'í', 'ú'}:
            return 'V'  # strong vowel
        if char in {'i', 'u', 'ü'}:
            return 'v'  # week vowel
        if char == 'x':
            return 'x'
        if char == 's':
            return 's'
        else:
            return 'c'

    def find(self, finder):
        return self.type_line.find(finder)

    def split(self, pos, where):
        return CharLine(self.word[0:pos + where]), CharLine(self.word[pos + where:])

    def split_by(self, finder, where):
        split_point = self.find(finder)
        if split_point != -1:
            chl1, chl2 = self.split(split_point, where)
            return chl1, chl2
        return self, False

    def __str__(self):
        return self.word

    def __repr__(self):
        return repr(self.word)


class Silabizer:
    def __init__(self):
        self.grammar = []

    def split(self, chars):
        rules = [('VV', 1), ('cccc', 2), ('xcc', 1), ('ccx', 2), ('csc', 2), ('xc', 1), ('cc', 1), ('vcc', 2),
                 ('Vcc', 2), ('sc', 1), ('cs', 1), ('Vc', 1), ('vc', 1), ('Vs', 1), ('vs', 1)]
        for split_rule, where in rules:
            first, second = chars.split_by(split_rule, where)
            if second:
                if first.type_line in {'c', 's', 'x', 'cs'} or second.type_line in {'c', 's', 'x', 'cs'}:
                    # print 'skip1', first.word, second.word, split_rule, chars.type_line
                    continue
                if first.type_line[-1] == 'c' and second.word[0] in {'l', 'r'}:
                    continue
                if first.word[-1] == 'l' and second.word[-1] == 'l':
                    continue
                if first.word[-1] == 'r' and second.word[-1] == 'r':
                    continue
                if first.word[-1] == 'c' and second.word[-1] == 'h':
                    continue
                return self.split(first) + self.split(second)
        return [chars]

    def __call__(self, word):
        return self.split(CharLine(word))


if __name__ == '__main__':
    s = '''Foi o senador Flávio Arns (PT-PR) quem sugeriu a inclusão da peça entre os itens do uniforme de alunos dos 
    ensinos Fundamental e Médio nas escolas municipais, estaduais e federais. Ele defende a medida como forma de 
    proteger crianças e adolescentes dos males provocados pelo excesso de exposição aos raios solares. Se a ideia for 
    aprovada, os estudantes receberão dois conjuntos anuais, completados por calçado, meias, calça e camiseta.'''
    sil = Silabizer()
    si = len(sil(s))
    snts = len(tokenize.sent_tokenize(s, language='portuguese'))
    toks = tokenize.word_tokenize(s, language='portuguese')
    cont = 0
    for tk in toks:
        # print(tk)
        # cont += len(sil(tk))
        print(sil(tk))
    # print(si, snts, toks)
    print(cont)