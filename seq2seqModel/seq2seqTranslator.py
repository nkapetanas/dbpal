from __future__ import unicode_literals, print_function, division
import random
import time

import torch
import torch.nn as nn
from torch import optim

from . import Utils
from .encoder import EncoderRNN
from .attentiondecoder import AttnDecoderRNN
from .lang import prepare_data
from .training import train

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

SOS_TOKEN = 0  # Start of the sentence
EOS_TOKEN = 1  # End of the sentence
MAX_LENGTH = 10
LEARNING_RATE = 0.01
HIDDEN_SIZE = 256
NUMBER_OF_ITERATIONS = 75000
DROPOUT = 0.1

TRAINED_ENCODER_PATH = 'producedmodel/encoder.dict'
TRAINED_DECODER_PATH = 'producedmodel/decoder.dict'

input_lang, output_lang, pairs = prepare_data('eng', 'sql', True)


def save_model(encoder, decoder):
    torch.save(encoder.state_dict(), TRAINED_ENCODER_PATH)
    torch.save(decoder.state_dict(), TRAINED_DECODER_PATH)


def indexes_from_sentence(lang, sentence):
    return [lang.word2index[word] for word in sentence.split(' ')]


def tensor_from_sentence(lang, sentence):
    indexes = indexes_from_sentence(lang, sentence)
    indexes.append(EOS_TOKEN)
    return torch.tensor(indexes, dtype=torch.long, device=device).view(-1, 1)


def tensors_from_pair(pair):
    input_tensor = tensor_from_sentence(input_lang, pair[0])
    target_tensor = tensor_from_sentence(output_lang, pair[1])
    return input_tensor, target_tensor


def training_iterations(encoder, decoder, iteration_number, print_every=1000, plot_every=100,
                        learning_rate=LEARNING_RATE):
    start = time.time()
    plot_losses = []
    print_loss_total = 0  # Reset every print_every
    plot_loss_total = 0  # Reset every plot_every

    encoder_optimizer = optim.SGD(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = optim.SGD(decoder.parameters(), lr=learning_rate)
    training_pairs = [tensors_from_pair(random.choice(pairs))
                      for _ in range(iteration_number)]
    criterion = nn.NLLLoss()

    for iteration in range(1, iteration_number + 1):
        training_pair = training_pairs[iteration - 1]
        input_tensor = training_pair[0]
        target_tensor = training_pair[1]

        loss = train(input_tensor, target_tensor, encoder,
                     decoder, encoder_optimizer, decoder_optimizer, criterion)
        print_loss_total += loss
        plot_loss_total += loss

        if iteration % print_every == 0:
            print_loss_avg = print_loss_total / print_every
            print_loss_total = 0
            print('%s (%d %d%%) %.4f' % (Utils.time_since(start, iteration / iteration_number),
                                         iteration, iteration / iteration_number * 100, print_loss_avg))

        if iteration % plot_every == 0:
            plot_loss_avg = plot_loss_total / plot_every
            plot_losses.append(plot_loss_avg)
            plot_loss_total = 0

    Utils.show_plot(plot_losses)


def evaluate(encoder, decoder, sentence, max_length=MAX_LENGTH):
    with torch.no_grad():
        input_tensor = tensor_from_sentence(input_lang, sentence)
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.initHidden()

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
                decoded_words.append('<EOS>')
                break
            else:
                decoded_words.append(output_lang.index2word[topi.item()])

            decoder_input = topi.squeeze().detach()

        # return decoded_words, decoder_attentions[:di + 1]
        return decoded_words


encoder = EncoderRNN(input_lang.n_words, HIDDEN_SIZE).to(device)
attn_decoder = AttnDecoderRNN(HIDDEN_SIZE, output_lang.n_words, dropout_p=DROPOUT).to(device)

training_iterations(encoder, attn_decoder, NUMBER_OF_ITERATIONS, print_every=5000)

save_model(encoder, attn_decoder)