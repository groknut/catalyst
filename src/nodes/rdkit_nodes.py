# nodes/inchi_node.py
import dearpygui.dearpygui as dpg
from rdkit import Chem
from core.base_node import BaseNode
from core.node_types import NodeTypes
from mol_data import MolData

GROUP_NAME = "RDkit"

class MolToInChINode(BaseNode):
    group = GROUP_NAME
    description = "Преобразует молекулу в InChI строку"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_inchi = self.add_output_attribute("InChI", NodeTypes.STRING)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("InChI: --")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            try:
                inchi = Chem.MolToInchi(data.mol)
                dpg.set_value(self.text, f"InChI: {inchi}")
                self.manager.propagate(self.out_inchi)
            except Exception as e:
                dpg.set_value(self.text, f"Error: {e}")
        else:
            dpg.set_value(self.text, "InChI: --")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            try:
                return Chem.MolToInchi(data.mol)
            except:
                return None
        return None

    def get_params(self):
        return {}

    def set_params(self, p):
        pass


class SaltRemoverNode(BaseNode):
    group = GROUP_NAME
    description = "Удаляет соли, оставляя самый большой органический фрагмент"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_mol = self.add_output_attribute("MolData", NodeTypes.MOL)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.status = dpg.add_text("Готов")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            try:
                remover = Chem.SaltRemover()
                clean_mol = remover.StripMol(data.mol)
                if clean_mol is not None:
                    self._cached_mol = MolData(clean_mol)
                    dpg.set_value(
                        self.status, f"Очищено, атомов: {clean_mol.GetNumAtoms()}"
                    )
                else:
                    self._cached_mol = None
                    dpg.set_value(self.status, "Ошибка удаления солей")
                self.manager.propagate(self.out_mol)
            except Exception as e:
                dpg.set_value(self.status, f"Ошибка: {e}")
                self._cached_mol = None
        else:
            dpg.set_value(self.status, "Нет молекулы")

    def get_output_value(self, pin_id):
        return getattr(self, "_cached_mol", None)

    def get_params(self):
        return {}

    def set_params(self, p):
        pass

from rdkit.Chem import AllChem, DataStructs

class TanimotoSimilarityNode(BaseNode):
    group = "Similarity"
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
