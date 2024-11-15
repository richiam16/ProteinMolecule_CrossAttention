"""Convert a series of torch tensors to h5.

Running ESM2 generates a torch tensor pickle file for each sequence,
to standarize data we package all tensors into a single h5 file.
The cmd to run esm is:
```
esm-extract esm2_t33_650M_UR50D proteins.fasta \
  esm2_embs --repr_layers 33 --include per_tok
```
"""
import glob
from pathlib import Path
import torch
import h5py
import argparse

import tqdm.auto as tqdm

parser = argparse.ArgumentParser(
        description='Precompute molecule features for a dataset.',
        formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument(
        '--directory',
        '-d',
        type=str,
        help='Directory of esm embeddings',
        required=True
    )
    
if __name__ == "__main__":
    args = parser.parse_args()
    work_dir = Path(args.directory)
    files = list(glob.glob(str(work_dir / '*.pt')))
    print(f'Found {len(files)} pt files in {work_dir}')
    emb_path = work_dir.parent / 'esm2_token_embs.h5'
    with h5py.File(emb_path, "w") as hf:
        for path in tqdm.tqdm(files):
            with open(path, 'r') as afile:
                adict = torch.load(path)
                key = adict['label']
                t = adict['representations'][33].detach().cpu().numpy()
            hf.create_dataset(key, data=t)
        print('Done!')