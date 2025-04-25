"""Utility functions."""
from typing import Any
import pandas as pd
from IPython import get_ipython
import IPython.display as ipy_display
import pprint as _pprint

def is_notebook() -> bool:
    """Detect whether code is running in a Jupyter Notebook or Google Colab environment."""
    try:
        # Get the shell type from IPython
        shell = get_ipython().__class__.__name__
        if shell in ['ZMQInteractiveShell',  # Jupyter Notebook
                    'Shell',                  # Google Colab
                    'TerminalInteractiveShell']:  # IPython terminal
            return True
        else:
            return False
    except NameError:
        # If get_ipython() is not defined, we're in a regular Python script
        return False
    
def html_header(text:str, n:int = 3)-> None:
    ipy_display.display(ipy_display.HTML('<h{n}>{text}</h{n}>'))

def print_modules(mod_list)-> None:
    for mod in mod_list:
        print(f'{mod.__name__:<20s} = {mod.__version__}')

def pprint(a:Any):
    _pprint.pprint(a)
    
def peek_df(df:pd.DataFrame, title:str=None, n=5)-> None:
    if title:
        if is_notebook():
            html_header(f'{title:-^30}')
        else:
            print(f'{title:-^30}')
        
    print(f'Columns: {df.columns}')
    print(f'Shape: {df.shape}')
    if n > 0 and is_notebook():
        ipy_display.display(df.head(n=n))