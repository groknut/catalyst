from rdkit.Chem import AllChem, DataStructs
from core.base_node import BaseNode
from core.node_types import NodeTypes
import dearpygui.dearpygui as dpg
from mol_data import MolData

GROUP_NAME = "Similarity"
class TanimotoSimilarityNode(BaseNode):
    group = GROUP_NAME
    description = "Вычисляет сходство Танимото двух молекул (Morgan2)"

    def build_node(self):
        self.in_mol1 = self.add_input_attribute("MolData A", NodeTypes.MOL)
        self.in_mol2 = self.add_input_attribute("MolData B", NodeTypes.MOL)
        self.out_sim = self.add_output_attribute("Tanimoto", NodeTypes.FLOAT)

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("Tanimoto: --")

    def update(self):
        mol1_data = self.manager.get_upstream_data(self.in_mol1)
        mol2_data = self.manager.get_upstream_data(self.in_mol2)

        if (
            isinstance(mol1_data, MolData)
            and mol1_data.mol
            and isinstance(mol2_data, MolData)
            and mol2_data.mol
        ):
            try:
                fp1 = AllChem.GetMorganFingerprintAsBitVect(
                    mol1_data.mol, 2, nBits=2048
                )
                fp2 = AllChem.GetMorganFingerprintAsBitVect(
                    mol2_data.mol, 2, nBits=2048
                )
                sim = DataStructs.TanimotoSimilarity(fp1, fp2)
                dpg.set_value(self.text, f"Tanimoto: {sim:.4f}")
                self.manager.propagate(self.out_sim)
            except Exception:
                dpg.set_value(self.text, "Ошибка")
        else:
            dpg.set_value(self.text, "Tanimoto: --")

    def get_output_value(self, pin_id):
        mol1_data = self.manager.get_upstream_data(self.in_mol1)
        mol2_data = self.manager.get_upstream_data(self.in_mol2)
        if (
            isinstance(mol1_data, MolData)
            and mol1_data.mol
            and isinstance(mol2_data, MolData)
            and mol2_data.mol
        ):
            try:
                fp1 = AllChem.GetMorganFingerprintAsBitVect(
                    mol1_data.mol, 2, nBits=2048
                )
                fp2 = AllChem.GetMorganFingerprintAsBitVect(
                    mol2_data.mol, 2, nBits=2048
                )
                return DataStructs.TanimotoSimilarity(fp1, fp2)
            except:
                return None
        return None

    def get_params(self):
        return {}

    def set_params(self, p):
        pass
