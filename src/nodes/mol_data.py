
from rdkit import Chem
class MolData:
    """Обёртка для передачи молекулы между узлами."""
    def __init__(self, mol):
        self.mol = mol
        self.smiles = Chem.MolToSmiles(mol) if mol else ""

class MolList:
    """Обёртка для передачи списка молекул между узлами."""
    def __init__(self, mols):
        if mols is None:
            self.items = []
        else:
            self.items = []
            for m in mols:
                if isinstance(m, MolData):
                    self.items.append(m)
                else:
                    # оборачиваем RDKit Mol
                    self.items.append(MolData(m))
