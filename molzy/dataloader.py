# Dataloading functionality

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class DataSpec:
    name: str
    activity: str
    seq: str='sequence'
    seqid: str='accession'
    smiles: str='isosmiles'
    context : str = ''


