"""Utility functions."""

import pandas as pd




def peek_df(df:pd.DataFrame, title:str=None, n=5)-> None:
    if title:
        print(f'{title:-^30}')
    print(df.columns)
    print(df.shape)
    if n > 0:
        df.head(n=n)