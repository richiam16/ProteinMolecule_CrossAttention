


import sys
sys.path.append('..')

import molzy
import molzy.dataloader
import descriptastorus.descriptors.rdNormalizedDescriptors as rdNormalizedDescriptors
import argparse
import numpy as np
import tqdm.auto as tqdm

_P = molzy.Paths()
parser = argparse.ArgumentParser(
        description='Precompute molecule features for a dataset.',
        formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument(
        '--dataset',
        '-d',
        type=str,
        help='Dataset name, assumes its in processed',
        required=True
    )
    
if __name__ == "__main__":
    args = parser.parse_args()
    _D, df = molzy.dataloader.load_dataset(args.dataset)
    out_dir = _P.data_dir / _D.name 
    generator = rdNormalizedDescriptors.RDKit2DHistogramNormalized()
    smiles = np.unique(df[_D.smiles].dropna().to_numpy(str))
    print(smiles)
    values = np.stack([np.array(generator.process(s))[1:].astype(np.float32) for s in tqdm.tqdm(smiles)])
    feats = molzy.dataloader.ArrayMap(smiles, values)
    feats.save(out_dir / 'rdkit2dnorm.npz')
    print(f'Done for {_D.name}')