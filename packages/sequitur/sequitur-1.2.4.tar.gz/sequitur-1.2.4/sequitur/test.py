import torch
from models import LINEAR_AE
from quick_train import quick_train

train_seqs = [torch.randn(4) for _ in range(100)] # Sequences of length 4
encoder, decoder, _, _ = quick_train(LINEAR_AE, train_seqs, encoding_dim=2, denoise=True)

print(encoder(torch.randn(4))) # => torch.tensor([0.19, 0.84])
