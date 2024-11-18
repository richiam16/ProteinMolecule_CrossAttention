import torch
import torch.utils.data as torch_data
import numpy as np
from torch.nn.utils.rnn import pad_sequence

class EnzymeToTensors(torch_data.Dataset):
    """Assuming the first column is protein, second is smiles."""
    def __init__(self, enzyme_index, labels,  prot_feat, mol_feat, indices):
        self.cols = enzyme_index.columns.tolist()
        self.indexer = enzyme_index.loc[indices].reset_index()
        for c in self.cols:
            self.indexer[c] = self.indexer[c].to_numpy(str)
        assert len(self.cols)==2, 'Expecting only two columns'
        self.labels = labels
        self.mol_feat = mol_feat
        self.prot_feat = prot_feat

    def __len__(self):
        return len(self.indexer)

    def __getitem__(self, i):
        row = self.indexer.loc[i]
        prot = self.prot_feat[row[self.cols[0]]][:]
        mol = self.mol_feat( np.array([row[self.cols[1]]]) )
        return prot, mol, self.labels[i]
    
def collate_fn(batch):
    """Concatenate a batch for a torch model."""
    prots = [torch.from_numpy(item[0]) for item in batch]
    mols = torch.Tensor([item[1] for item in batch])
    targets = torch.Tensor([item[2] for item in batch])
    padded_prots = pad_sequence(prots, batch_first=True)
    return padded_prots, mols, targets


def flat_mean(x):
    is_token = x.shape[0] > 1
    return np.mean(x, axis=0) if is_token else x[0,:]

def xg_collate(batch):
    """Concatenate a batch for a xgboost model (prot_vec, mol_vec)."""
    x = torch.Tensor([np.concatenate((flat_mean(item[0]), flat_mean(item[1]))) for item in batch])
    y = torch.Tensor([item[2] for item in batch])
    return x, y