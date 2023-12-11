import torch

# specify path to pytorch model .pt file
pt_file_path = 'your_model.pt'

# load pytorch model and set to eval mode
model = torch.load(pt_file_path)
model.eval()