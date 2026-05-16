
from rdkit import Chem

class MolData:
    """Обёртка для передачи молекулы между узлами."""
    def __init__(self, mol):
        self.mol = mol
        self.smiles = Chem.MolToSmiles(mol) if mol else ""
