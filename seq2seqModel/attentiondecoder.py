import torch
import torch.nn as nn
import torch.nn.functional as f

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MAX_LENGTH = 20

class AttnDecoderRNN(nn.Module):
    def __init__(self, hidden_size, output_size, dropout_p=0.1, max_length=MAX_LENGTH):
        super(AttnDecoderRNN, self).__init__()
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.dropout_p = dropout_p
        self.max_length = max_length

        self.embedding = nn.Embedding(self.output_size, self.hidden_size)
        self.attn = nn.Linear(self.hidden_size * 2, self.max_length)
        self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.dropout = nn.Dropout(self.dropout_p)
        self.gru = nn.GRU(self.hidden_size, self.hidden_size)
        self.out = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, input, hidden, encoder_outputs):
        embedded = self.embedding(input).view(1, 1, -1) # change the shape to map the shape that the GRU expects
        embedded = self.dropout(embedded)

        attention_weights = f.softmax(
            self.attn(torch.cat((embedded[0], hidden[0]), 1)), dim=1)
        attention_applied = torch.bmm(attention_weights.unsqueeze(0),
                                 encoder_outputs.unsqueeze(0))

        output = torch.cat((embedded[0], attention_applied[0]), 1)
        output = self.attn_combine(output).unsqueeze(0)

        output = f.relu(output)
        output, hidden = self.gru(output, hidden)

        output = f.log_softmax(self.out(output[0]), dim=1)
        return output, hidden, attention_weights

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=device)