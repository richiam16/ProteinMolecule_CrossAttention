
import sys

sys.path.append('../..')

import molzy
import molzy.utils as utils
import molzy.files as files
import molzy.types as types
import pandas as pd

_P = molzy.Paths()

if __name__ == "__main__":

    dataset = molzy.data.DatasetSpec(name='azoreductases',
                                  shortname='azo',
                                  data_file='azo_dataset.csv',
                                  protein = 'Protein Sequence',
                                  protid = 'Entry Name',
                                  smiles = 'S2_smile',
                                  labels=['activity'],
                                  columns={'DyeallE': 'Dye used for enzymatic assay',
                                           'Ename': 'Internal code for enzyme',
                                           'SMILE_Substrate1': 'Eletron donor NADPH or NADH',
                                           'SMILE_Product1': 'Dye molecule product',
                                           'Reaction': 'SMILES equation representing rxn'},
                                    comments="""
                                     * Reaction information could be levearaged in the future.
                                     * Original data has 23 null smiles (why?).
                                     """.strip(),
                                     )
    task = molzy.data.TaskSpec(dataset=dataset,
                               label=dataset.labels[0],
                               task_type=types.TaskType.binary,
                               units='',
                               standard_split='random',
                               available_splits=['random']
                               )
    work_dir = _P.raw_data_dir / 'Azoreductases'
    out_dir = files.dataset_dir(dataset.shortname)
    out_dir.mkdir(exist_ok=True)
    with files.datasetspec_path(out_dir).open('w') as afile:
        afile.write(dataset.to_json())

    with files.taskspec_path(out_dir, task.label).open('w') as afile:
        afile.write(task.to_json())

    prot_df = pd.read_csv(work_dir / 'azo.csv')
    utils.peek_df(prot_df, 'Proteins')

    assert len(dataset.labels) == 1, "Expecting a single label column"
    useful_cols = list(dataset.columns.keys()) + [dataset.smiles, dataset.protid] + dataset.labels
    neg_df = pd.read_csv(work_dir / 'Copia de Data_With_Reactions_Negatives.csv')
    neg_df[dataset.labels[0]] = 0
    utils.peek_df(neg_df, 'Negatives')
    pos_df = pd.read_csv(work_dir / 'Copia de Data_With_Reactions_Positives.csv')
    pos_df[dataset.labels[0]] = 1
    utils.peek_df(pos_df, 'Positives')
    joint_df = pd.concat([neg_df[useful_cols], pos_df[useful_cols]])
    utils.peek_df(joint_df, 'Joint')
    print(prot_df.shape, joint_df.shape)
    df = prot_df.merge(joint_df, on=dataset.protid)
    
    mask = df[dataset.smiles].isnull()
    print(f'{mask.sum()} null smiles, dropping these rows')
    df = df[~mask]
    utils.peek_df(df, 'Final')
    df.to_csv(out_dir / dataset.data_file, index=False)

    uniq_df = df[[dataset.protid, dataset.protein]].drop_duplicates(subset=dataset.protein)
    utils.peek_df(uniq_df)
    files.write_fasta(uniq_df[dataset.protid], uniq_df[dataset.protein], out_dir)


    y = df[task.label].to_numpy().reshape(-1, 1)

    split = molzy.splits.create_stratified_split(y,
                            train_size=0.6, val_size=0.2, test_size=0.2, random_state=42)
    split.save(files.split_path(out_dir, f'{task.label}_stratified'))

