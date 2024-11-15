
import sys
sys.path.append('../..')

import molzy
import molzy.utils as utils
import pandas as pd
import itertools


_P = molzy.Paths()



if __name__ == "__main__":

    spec = molzy.data.DataSpec(name='SAM',
                                     label='activity',
                                     protid='Entry Name', 
                                     context="""
                                     * Reaction information could be levearaged in the future
                                     """.strip()
                                     )
    work_dir = _P.raw_data_dir / 'SAM'
    out_dir = _P.data_dir / spec.name
    out_dir.mkdir(exist_ok=True)
    
    with (out_dir / 'dataspec.json').open('w') as afile:
        afile.write(spec.to_json())

    rename_map = {'Entry Name': spec.protid,
                  'Sequence': spec.protein,
                  'smiles': spec.smiles}
    

    prot_df = pd.read_csv(work_dir / 'SAM_raw_cleaned.csv')

    utils.peek_df(prot_df, 'Sequence')
    prot_df = prot_df.rename(columns=rename_map)
    prot_df = prot_df[[c for c in prot_df.columns if c in list(rename_map.values())]]
    utils.peek_df(prot_df, 'Sequence')

    unique_prot, unique_mol = prot_df[[spec.protid, spec.protein]].drop_duplicates(), prot_df[spec.smiles].unique()
 
    comb = list(itertools.product(unique_prot.values, unique_mol))

    flattened_combinations = [(entry_seq[0], entry_seq[1], smile) for entry_seq, smile in comb]

    df_comb = pd.DataFrame(flattened_combinations, columns=[c for c in prot_df.columns if c in list(rename_map.values())])

    merged_df = df_comb.merge(prot_df, on=[c for c in prot_df.columns if c in list(rename_map.values())], how='left', indicator=True)
    df_comb['Activity'] = merged_df['_merge'].apply(lambda x: 1 if x == 'both' else 0)


    df_comb.to_csv(out_dir / f'{spec.name}_data.csv', index=False)