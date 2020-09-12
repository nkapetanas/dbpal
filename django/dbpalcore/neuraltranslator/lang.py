import os
import re

from django.conf import settings

MAX_LENGTH = 20


class Lang:
    def __init__(self, name):
        self.name = name
        self.word2index = {"unknown": 0}
        self.word2count = {"unknown": 0}
        self.index2word = {0: "SOS", 1: "EOS", 3: "unknown"}
        self.n_words = 3  # Count SOS and EOS

    def add_sentence(self, sentence):
        for word in sentence.split(' '):  # split the sentence to the '' and then add the word
            self.add_word(word)

    def add_word(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.n_words
            self.word2count[word] = 1
            self.index2word[self.n_words] = word
            self.n_words += 1
        else:
            self.word2count[word] += 1

    # Lowercase, trim, and remove non-letter characters
    def normalize_string(self, s):
        s = s.lower().strip()
        s = re.sub(r"([.!?])", r" \1", s)
        return re.sub(r"[^a-zA-Z.!?]+", r" ", s)

    def read_languages(self, lang1, lang2, reverse=False):

        my_file = open(os.path.join(settings.BASE_DIR, 'engsql.txt'), 'r', encoding='utf-8')
        lines = my_file.read().strip().split('\n')

        # Split every line into pairs and normalize
        pairs = list()
        for l in lines:
            s = l.split('\t')
            s[0] = self.normalize_string(s[0])
            s[1] = s[1].lower()
            pairs.append(s)

        # Reverse pairs, make Lang instances
        if reverse:
            pairs = [list(reversed(p)) for p in pairs]
            input_lang = Lang(lang2)
            output_lang = Lang(lang1)
            return input_lang, output_lang, pairs

        input_lang = Lang(lang1)
        output_lang = Lang(lang2)
        return input_lang, output_lang, pairs


def filterPair(pair):
        return len(pair[0].split(' ')) < MAX_LENGTH and \
               len(pair[1].split(' ')) < MAX_LENGTH


def filter_pairs(pairs):
    return [pair for pair in pairs if filterPair(pair)]


def prepare_data(lang1, lang2, reverse=False):
    lang = Lang("seq2seqTranslator")
    input_lang, output_lang, pairs = lang.read_languages(lang1, lang2, reverse)
    print("Read %s sentence pairs" % len(pairs))

    pairs = filter_pairs(pairs)
    print("Trimmed to %s sentence pairs" % len(pairs))
    print("Counting words...")

    for pair in pairs:
        input_lang.add_sentence(pair[0])
        output_lang.add_sentence(pair[1])

    print("Counted words:")
    print(input_lang.name, input_lang.n_words)
    print(output_lang.name, output_lang.n_words)
    return input_lang, output_lang, pairs
