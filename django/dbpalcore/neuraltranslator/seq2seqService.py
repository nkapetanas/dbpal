import torch
import os
from django.conf import settings
from .encoder import EncoderRNN
from .attentiondecoder import AttnDecoderRNN
from .evaluator import evaluate

ENCODER_PATH = 'encoder.dict'
DECODER_PATH = 'decoder.dict'
HIDDEN_SIZE = 256
DROPOUT = 0.1

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def model_initialization():
    # input_lang.n_words
    # output_lang.n_words
    encoder = EncoderRNN(4258, HIDDEN_SIZE).to(device)
    attn_decoder = AttnDecoderRNN(HIDDEN_SIZE, 23, dropout_p=DROPOUT).to(device)

    encoder.load_state_dict(torch.load(os.path.join(settings.BASE_DIR, ENCODER_PATH)))
    attn_decoder.load_state_dict(torch.load(os.path.join(settings.BASE_DIR, DECODER_PATH)))
    return encoder, attn_decoder


class Seq2SeqService:

    def __init__(self):
        encoder, attn_decoder = model_initialization()
        self.encoder = encoder
        self.decoder = attn_decoder

    def evaluate_query(self, query):
        return evaluate(self.encoder, self.decoder, query)
