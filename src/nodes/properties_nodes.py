import dearpygui.dearpygui as dpg
from rdkit.Chem import Descriptors
from core.base_node import BaseNode
from core.node_types import NodeTypes
from mol_data import MolData


# ------------------------------------------------------------
#  Молекулярная масса
# ------------------------------------------------------------
class MolWeightNode(BaseNode):
    group = "Properties"
    description = "Молекулярная масса (MW)"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_mw = self.add_output_attribute("MolWeight", NodeTypes.FLOAT)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("MW: --")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            val = Descriptors.MolWt(data.mol)
            dpg.set_value(self.text, f"MW: {val:.2f}")
            self.manager.propagate(self.out_mw)
        else:
            dpg.set_value(self.text, "MW: --")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            return Descriptors.MolWt(data.mol)
        return None

    def get_params(self):
        return {}

    def set_params(self, p):
        pass


# ------------------------------------------------------------
#  LogP (коэффициент распределения октанол/вода)
# ------------------------------------------------------------
class MolLogPNode(BaseNode):
    group = "Properties"
    description = "Коэффициент распределения LogP"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_val = self.add_output_attribute("LogP", NodeTypes.FLOAT)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("LogP: --")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            val = Descriptors.MolLogP(data.mol)
            dpg.set_value(self.text, f"LogP: {val:.2f}")
            self.manager.propagate(self.out_val)
        else:
            dpg.set_value(self.text, "LogP: --")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            return Descriptors.MolLogP(data.mol)
        return None

    def get_params(self):
        return {}

    def set_params(self, p):
        pass


# ------------------------------------------------------------
#  TPSA (полярная площадь поверхности)
# ------------------------------------------------------------
class TPSANode(BaseNode):
    group = "Properties"
    description = "Топологическая полярная площадь поверхности (TPSA)"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_val = self.add_output_attribute("TPSA", NodeTypes.FLOAT)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("TPSA: --")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            val = Descriptors.TPSA(data.mol)
            dpg.set_value(self.text, f"TPSA: {val:.2f}")
            self.manager.propagate(self.out_val)
        else:
            dpg.set_value(self.text, "TPSA: --")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            return Descriptors.TPSA(data.mol)
        return None

    def get_params(self):
        return {}

    def set_params(self, p):
        pass


# ------------------------------------------------------------
#  Количество вращающихся связей
# ------------------------------------------------------------
class RotatableBondsNode(BaseNode):
    group = "Properties"
    description = "Число вращающихся связей (Rotatable Bonds)"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_val = self.add_output_attribute("RotBonds", NodeTypes.INT)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("RotBonds: --")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            val = Descriptors.NumRotatableBonds(data.mol)
            dpg.set_value(self.text, f"RotBonds: {val}")
            self.manager.propagate(self.out_val)
        else:
            dpg.set_value(self.text, "RotBonds: --")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            return Descriptors.NumRotatableBonds(data.mol)
        return None

    def get_params(self):
        return {}

    def set_params(self, p):
        pass


# ------------------------------------------------------------
#  Количество акцепторов водорода (HBA)
# ------------------------------------------------------------
class HBANode(BaseNode):
    group = "Properties"
    description = "Число акцепторов водородной связи (HBA)"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_val = self.add_output_attribute("HBA", NodeTypes.INT)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("HBA: --")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            val = Descriptors.NumHAcceptors(data.mol)
            dpg.set_value(self.text, f"HBA: {val}")
            self.manager.propagate(self.out_val)
        else:
            dpg.set_value(self.text, "HBA: --")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            return Descriptors.NumHAcceptors(data.mol)
        return None

    def get_params(self):
        return {}

    def set_params(self, p):
        pass


# ------------------------------------------------------------
#  Количество доноров водорода (HBD)
# ------------------------------------------------------------
class HBDNode(BaseNode):
    group = "Properties"
    description = "Число доноров водородной связи (HBD)"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_val = self.add_output_attribute("HBD", NodeTypes.INT)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("HBD: --")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            val = Descriptors.NumHDonors(data.mol)
            dpg.set_value(self.text, f"HBD: {val}")
            self.manager.propagate(self.out_val)
        else:
            dpg.set_value(self.text, "HBD: --")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            return Descriptors.NumHDonors(data.mol)
        return None

    def get_params(self):
        return {}

    def set_params(self, p):
        pass


# ------------------------------------------------------------
#  Количество тяжёлых атомов
# ------------------------------------------------------------
class HeavyAtomCountNode(BaseNode):
    group = "Properties"
    description = "Число тяжёлых атомов (не водород)"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_val = self.add_output_attribute("HeavyAtoms", NodeTypes.INT)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("HeavyAtoms: --")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            val = Descriptors.HeavyAtomCount(data.mol)
            dpg.set_value(self.text, f"HeavyAtoms: {val}")
            self.manager.propagate(self.out_val)
        else:
            dpg.set_value(self.text, "HeavyAtoms: --")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            return Descriptors.HeavyAtomCount(data.mol)
        return None

    def get_params(self):
        return {}

    def set_params(self, p):
        pass


# ------------------------------------------------------------
#  Количество колец
# ------------------------------------------------------------
class RingCountNode(BaseNode):
    group = "Properties"
    description = "Общее количество колец"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_val = self.add_output_attribute("Rings", NodeTypes.INT)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("Rings: --")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            val = Descriptors.RingCount(data.mol)
            dpg.set_value(self.text, f"Rings: {val}")
            self.manager.propagate(self.out_val)
        else:
            dpg.set_value(self.text, "Rings: --")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            return Descriptors.RingCount(data.mol)
        return None

    def get_params(self):
        return {}

    def set_params(self, p):
        pass
