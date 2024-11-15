
import sys
sys.path.append('../..')

import molzy
import molzy.utils as utils
import pandas as pd


_P = molzy.Paths()



if __name__ == "__main__":

    spec = molzy.data.DataSpec(name='SDR',
                                     label='cat_nadph',
                                     protid='Entry Name', 
                                     context="""
                                     * Reaction information could be levearaged in the future
                                     """.strip()
                                     )
    work_dir = _P.raw_data_dir / spec.name
    out_dir = _P.data_dir / spec.name
    out_dir.mkdir(exist_ok=True)
    
    with (out_dir / 'dataspec.json').open('w') as afile:
        afile.write(spec.to_json())

    rename_map = {'Entry Name': spec.protid,
                  'Sequence': spec.protein, 
                  "smile": spec.smiles, 
                  "cat_nadph": spec.label}
    

    prot_df = pd.read_excel(work_dir / 'output.xlsx')

    utils.peek_df(prot_df, 'Sequence')
    smiles_subtrate =["C1C=CN(C=C1C(=O)N)[C@H]2[C@@H]([C@@H]([C@H](O2)COP(=O)(O)OP(=O)(O)OC[C@@H]3[C@H]([C@H]([C@@H](O3)N4C=NC5=C(N=CN=C54)N)OP(=O)(O)O)O)O)O", 
    "C1C=CN(C=C1C(=O)N)[C@H]2[C@@H]([C@@H]([C@H](O2)COP(=O)(O)OP(=O)(O)OC[C@@H]3[C@H]([C@H]([C@@H](O3)N4C=NC5=C(N=CN=C54)N)O)O)O)O"]
    prot_df.columns
    prot_df[spec.smiles] = prot_df.apply(lambda row: smiles_subtrate[0] if row["NADPH_present"] == 1 else
                                            smiles_subtrate[1] if row["NADH_present"] == 1 else
                                            None, axis=1)
    prot_df = prot_df.rename(columns=rename_map)
    prot_df = prot_df[[c for c in prot_df.columns if c in list(rename_map.values())]]
    utils.peek_df(prot_df, 'Sequence')

    prot_df.to_csv(out_dir / f'{spec.name}_data.csv', index=False)