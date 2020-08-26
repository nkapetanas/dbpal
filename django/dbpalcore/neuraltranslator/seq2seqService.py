import torch
# read the files from the producedmodel file
from seq2seqModel.attentiondecoder import AttnDecoderRNN
from seq2seqModel.encoder import EncoderRNN
from seq2seqModel.seq2seqTranslator import evaluate

ENCODER_PATH = '../../../seq2seqModel/producedmodel/encoder.dict'
DECODER_PATH = '../../../seq2seqModel/producedmodel/decoder.dict'
HIDDEN_SIZE = 256
DROPOUT = 0.1

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Seq2SeqService:
    def model_initialization(self):
        # input_lang.n_words
        # output_lang.n_words
        encoder = EncoderRNN(4345, HIDDEN_SIZE).to(device)
        attn_decoder = AttnDecoderRNN(HIDDEN_SIZE, 2803, dropout_p=DROPOUT).to(device)

        encoder.load_state_dict(torch.load(ENCODER_PATH))
        attn_decoder.load_state_dict(torch.load(DECODER_PATH))
        return encoder, attn_decoder

    def evaluate_query(self, query):
        encoder, attn_decoder = self.model_initialization()
        return evaluate(encoder, attn_decoder, query)
