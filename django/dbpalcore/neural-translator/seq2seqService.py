
import torch
# read the files from the producedmodel file
from seq2seqModel.attentiondecoder import AttnDecoderRNN
from seq2seqModel.encoder import EncoderRNN

PATH = ''

encoder = EncoderRNN(input_lang.n_words, HIDDEN_SIZE).to(device)
attn_decoder = AttnDecoderRNN(HIDDEN_SIZE, output_lang.n_words, dropout_p=DROPOUT).to(device)


encoder.load_state_dict(torch.load('encoder.dict'))
attn_decoder.load_state_dict(torch.load('decoder.dict'))