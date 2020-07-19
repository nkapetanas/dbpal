from __future__ import unicode_literals, print_function, division
from io import open
import unicodedata
import string
import re
import random

import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

SOS_token = 0  # Start of the sentence
EOS_token = 1  # End of the sentence
MAX_LENGTH = 10


class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = dict()  # Mapping word to index
        self.word2count = dict()  # Mapping word to count
        self.index2word = {0: "SOS", 1: "EOS"}
        self.n_words = 2  # Count SOS and EOS

    def addSentence(self, sentence):
        for word in sentence.split(' '):  # split the sentence to the '' and then add the word
            self.addWord(word)

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1


    # Lowercase, trim, and remove non-letter characters
    def normalizeString(self, s):
        s = s.lower().strip()
        s = re.sub(r"([.!?])", r" \1", s)
        return re.sub(r"[^a-zA-Z.!?]+", r" ", s)

    def readLangs(self, lang1, lang2, reverse=False):

        print("Reading lines...")

        # Read the file and split into lines
        lines = open('data/%s-%s.txt' % (lang1, lang2), encoding='utf-8'). \
            read().strip().split('\n')

        # Split every line into pairs and normalize
        pairs = [[self.normalizeString(s) for s in l.split('\t')] for l in lines]

        # Reverse pairs, make Lang instances
        if reverse:
            pairs = [list(reversed(p)) for p in pairs]
            input_lang = Lang(lang2)
            output_lang = Lang(lang1)
        else:
            input_lang = Lang(lang1)
            output_lang = Lang(lang2)

        return input_lang, output_lang, pairs


def filterPair(pairs):
    return [p for p in pairs
            if
            len(p[0].split(' ')) < MAX_LENGTH and \
            len(p[1].split(' ')) < MAX_LENGTH]


def filterPairs(pairs):
    return [pair for pair in pairs if filterPair(pair)]

def prepareData(lang1, lang2, reverse=False):
    input_lang, output_lang, pairs = readLangs(lang1, lang2, reverse)
    print("Read %s sentence pairs" % len(pairs))
    pairs = filterPairs(pairs)
    print("Trimmed to %s sentence pairs" % len(pairs))
    print("Counting words...")
    for pair in pairs:
        input_lang.addSentence(pair[0])
        output_lang.addSentence(pair[1])
    print("Counted words:")
    print(input_lang.name, input_lang.n_words)
    print(output_lang.name, output_lang.n_words)
    return input_lang, output_lang, pairs


input_lang, output_lang, pairs = prepareData('eng', 'sql', True)
print(random.choice(pairs))





def indexesFromSentence(lang, sentence):
    return [lang.word2index[word] for word in sentence.split(' ')]


def tensorFromSentence(lang, sentence):
    indexes = indexesFromSentence(lang, sentence)
    indexes.append(EOS_token)
    return torch.tensor(indexes, dtype=torch.long, device=device).view(-1, 1)


def tensorsFromPair(pair):
    input_tensor = tensorFromSentence(input_lang, pair[0])
    target_tensor = tensorFromSentence(output_lang, pair[1])
    return (input_tensor, target_tensor)