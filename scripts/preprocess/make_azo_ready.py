
import sys
sys.path.append('../..')

import molzy
import molzy.utils as utils
import pandas as pd

_P = molzy.Paths()



if __name__ == "__main__":

    spec = molzy.dataloader.DataSpec(name='azoreductases',
                                     activity='activity',
                                     context="""
                                     Reaction information could be levearaged in the future.
                                     """
                                     )
    work_dir = _P.raw_data_dir / 'Azoreductases'
    out_dir = _P.data_dir / spec.name
    out_dir.mkdir(exist_ok=True)
    print(spec)
    with (out_dir / 'dataspec.json').open('w') as afile:
        afile.write(spec.to_json())

    rename_map = {'Entry Name': spec.seqid,
                  'Protein Sequence': spec.seq,
                  'S2_smile': spec.smiles}
    
    df = pd.DataFrame()
    prot_df = pd.read_csv(work_dir / 'azo.csv')
    utils.peek_df(prot_df, 'Proteins')
    prot_df = prot_df.rename(columns=rename_map)
    prot_df = prot_df[[c for c in prot_df.columns if c in list(rename_map.values())]]

    useful_cols = ['S2_smile', 'Entry Name', spec.activity]
    neg_df = pd.read_csv(work_dir / 'Copia de Data_With_Reactions_Negatives.csv')
    neg_df[spec.activity] = 0
    utils.peek_df(neg_df, 'Negatives')
    pos_df = pd.read_csv(work_dir / 'Copia de Data_With_Reactions_Positives.csv')
    pos_df[spec.activity] = 1
    utils.peek_df(pos_df, 'Positives')
    joint_df = pd.concat([neg_df[useful_cols], pos_df[useful_cols]])
    joint_df = joint_df.rename(columns=rename_map)
    utils.peek_df(joint_df, 'Joint')
    df = prot_df.merge(joint_df, on=spec.seqid)
    utils.peek_df(df, 'Final')
    df.to_csv(out_dir / f'{spec.name}_data.csv', index=False)






