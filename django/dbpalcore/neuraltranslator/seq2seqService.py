import torch
import os
from django.conf import settings
from .encoder import EncoderRNN
from .attentiondecoder import AttnDecoderRNN
from .evaluator import evaluate

ENCODER_PATH = 'encoder.dict'
DECODER_PATH = 'decoder.dict'
HIDDEN_SIZE = 256
DROPOUT = 0.2

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def model_initialization():
    encoder = EncoderRNN(789, HIDDEN_SIZE).to(device)
    attn_decoder = AttnDecoderRNN(HIDDEN_SIZE, 170, dropout_p=DROPOUT).to(device)

    encoder.load_state_dict(torch.load(os.path.join(settings.BASE_DIR, ENCODER_PATH), map_location="cpu"))
    attn_decoder.load_state_dict(torch.load(os.path.join(settings.BASE_DIR, DECODER_PATH), map_location="cpu"))
    return encoder, attn_decoder


class Seq2SeqService:

    def __init__(self):
        encoder, attn_decoder = model_initialization()
        self.encoder = encoder
        self.decoder = attn_decoder

    def evaluate_query(self, query):
        return evaluate(self.encoder, self.decoder, query)
