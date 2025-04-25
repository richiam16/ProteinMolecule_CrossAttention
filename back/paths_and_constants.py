
from pathlib import Path

_main_dir = Path(__file__).parent.parent

class Paths:

    raw_data_dir = _main_dir / 'data/raw'
    data_dir = _main_dir / 'data/processed'
    
