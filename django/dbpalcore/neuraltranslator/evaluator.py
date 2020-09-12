from __future__ import unicode_literals, print_function, division

import torch
from .lang import prepare_data


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

SOS_TOKEN = 0  # Start of the sentence
EOS_TOKEN = 1  # End of the sentence
MAX_LENGTH = 20

def indexes_from_sentence(lang, sentence):
    return [lang.word2index.get(word) for word in sentence.split(' ')]


def tensorFromSentence(lang, sentence):
    indexes = indexes_from_sentence(lang, sentence)
    indexes.append(EOS_TOKEN)
    return torch.tensor(indexes, dtype=torch.long, device=device).view(-1, 1)

input_lang, output_lang, pairs = prepare_data('eng', 'sql')

def indexes_from_sentence(lang, sentence):

    indexes = list()
    for word in sentence.split(' '):
        index = lang.word2index.get(word.lower())
        if index is None:
            indexes.append(0)
            continue

        indexes.append(index)

    return indexes


def tensor_from_sentence(lang, sentence):
    indexes = indexes_from_sentence(lang, sentence)
    indexes.append(EOS_TOKEN)
    return torch.tensor(indexes, dtype=torch.long, device=device).view(-1, 1)


def evaluate(encoder, decoder, sentence, max_length=MAX_LENGTH):
    with torch.no_grad():
        sentence_normalized = input_lang.normalize_string(sentence)
        input_tensor = tensorFromSentence(input_lang, sentence_normalized)
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.init_hidden()

        encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

        for ei in range(input_length):
            encoder_output, encoder_hidden = encoder(input_tensor[ei],
                                                     encoder_hidden)
            encoder_outputs[ei] += encoder_output[0, 0]

        decoder_input = torch.tensor([[SOS_TOKEN]], device=device)  # SOS

        decoder_hidden = encoder_hidden

        decoded_words = []
        decoder_attentions = torch.zeros(max_length, max_length)

        for di in range(max_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            decoder_attentions[di] = decoder_attention.data
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == EOS_TOKEN:
                # decoded_words.append('<EOS>')
                break
            else:
                decoded_words.append(output_lang.index2word[topi.item()])

            decoder_input = topi.squeeze().detach()


        return ' '.join(decoded_words)
