
import dearpygui.dearpygui as dpg
from rdkit import Chem
from core.base_node import BaseNode
from core.node_types import NodeTypes
from mol_data import MolData
from rdkit.Chem import AllChem

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

class SMILESValidatorNode(BaseNode):
    group = GROUP_NAME
    description = "Проверяет, является ли входная строка корректным SMILES"

    def build_node(self):
        self.in_smiles = self.add_input_attribute("SMILES", NodeTypes.SMILES)
        self.out_valid = self.add_output_attribute("Valid", NodeTypes.BOOL)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("Valid: --")

    def update(self):
        smi = self.manager.get_upstream_data(self.in_smiles)
        if smi:
            mol = Chem.MolFromSmiles(str(smi))
            valid = mol is not None
            dpg.set_value(self.text, f"Valid: {valid}")
            self.manager.propagate(self.out_valid)
        else:
            dpg.set_value(self.text, "Valid: --")

    def get_output_value(self, pin_id):
        smi = self.manager.get_upstream_data(self.in_smiles)
        if smi:
            return Chem.MolFromSmiles(str(smi)) is not None
        return None

    def get_params(self): return {}
    def set_params(self, p): pass

class SMILESCanonicalizerNode(BaseNode):
    group = GROUP_NAME
    description = "Преобразует произвольный SMILES в каноническую форму"

    def build_node(self):
        self.in_smiles = self.add_input_attribute("SMILES", NodeTypes.SMILES)
        self.out_canon = self.add_output_attribute("Canonical SMILES", NodeTypes.SMILES)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("Canonical: --")

    def update(self):
        smi = self.manager.get_upstream_data(self.in_smiles)
        if smi:
            mol = Chem.MolFromSmiles(str(smi))
            if mol:
                canon = Chem.MolToSmiles(mol)
                dpg.set_value(self.text, f"Canonical: {canon}")
                self.manager.propagate(self.out_canon)
            else:
                dpg.set_value(self.text, "Invalid SMILES")
        else:
            dpg.set_value(self.text, "Canonical: --")

    def get_output_value(self, pin_id):
        smi = self.manager.get_upstream_data(self.in_smiles)
        if smi:
            mol = Chem.MolFromSmiles(str(smi))
            return Chem.MolToSmiles(mol) if mol else None
        return None

    def get_params(self): return {}
    def set_params(self, p): pass

class MolTo3DNode(BaseNode):
    group = GROUP_NAME
    description = "Генерирует 3D-координаты для молекулы (ETKDG)"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_mol = self.add_output_attribute("MolData 3D", NodeTypes.MOL)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.status = dpg.add_text("Готов")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            try:
                mol = Chem.RWMol(data.mol)
                mol = mol.GetMol()
                AllChem.EmbedMolecule(mol, AllChem.ETKDG())
                AllChem.MMFFOptimizeMolecule(mol)
                self._cached_mol = MolData(mol)
                dpg.set_value(self.status, f"3D координаты сгенерированы")
                self.manager.propagate(self.out_mol)
            except Exception as e:
                dpg.set_value(self.status, f"Ошибка: {e}")
        else:
            dpg.set_value(self.status, "Нет молекулы")

    def get_output_value(self, pin_id):
        return getattr(self, '_cached_mol', None)

    def get_params(self): return {}
    def set_params(self, p): pass
