import dearpygui.dearpygui as dpg
from rdkit.Chem import Descriptors
from core.base_node import BaseNode
from core.node_types import NodeTypes
from mol_data import MolData
from rdkit.Chem import QED, rdMolDescriptors

GROUP_NAME = "Properties"

#  Молекулярная масса
class MolWeightNode(BaseNode):
    group = GROUP_NAME
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



#  LogP (коэффициент распределения октанол/вода)
class MolLogPNode(BaseNode):
    group = GROUP_NAME
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



#  TPSA (полярная площадь поверхности)
class TPSANode(BaseNode):
    group = GROUP_NAME
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



#  Количество вращающихся связей
class RotatableBondsNode(BaseNode):
    group = GROUP_NAME
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



#  Количество акцепторов водорода (HBA)
class HBANode(BaseNode):
    group = GROUP_NAME
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



#  Количество доноров водорода (HBD)
class HBDNode(BaseNode):
    group = GROUP_NAME
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


#  Количество тяжёлых атомов
class HeavyAtomCountNode(BaseNode):
    group = GROUP_NAME
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



#  Количество колец
class RingCountNode(BaseNode):
    group = GROUP_NAME
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



#  Количественная оценка сходства с лекарственным средством
class QEDNode(BaseNode):
    group = GROUP_NAME
    description = (
        "Количественная оценка сходства с лекарственным средством (индекс QED)"
    )

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_qed = self.add_output_attribute("QED", NodeTypes.FLOAT)

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("QED: --")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            qed = QED.qed(data.mol)
            dpg.set_value(self.text, f"QED: {qed:.3f}")
            self.manager.propagate(self.out_qed)
        else:
            dpg.set_value(self.text, "QED: --")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            return QED.qed(data.mol)
        return None

    def get_params(self):
        return {}

    def set_params(self, p):
        pass


#  Молекулярная формула в виде строки
class MolecularFormulaNode(BaseNode):
    group = GROUP_NAME
    description = "Выдаёт молекулярную формулу в виде строки"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_formula = self.add_output_attribute("Formula", NodeTypes.STRING)

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("Formula: --")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)

        if isinstance(data, MolData) and data.mol:
            formula = rdMolDescriptors.CalcMolFormula(data.mol)
            dpg.set_value(self.text, f"Formula: {formula}")
            self.manager.propagate(self.out_formula)
        else:
            dpg.set_value(self.text, "Formula: --")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            return rdMolDescriptors.CalcMolFormula(data.mol)
        return None

    def get_params(self):
        return {}

    def set_params(self, p):
        pass

# подсчет ароматических колец
class AromaticRingCountNode(BaseNode):
    group = GROUP_NAME
    description = "Количество ароматических колец"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_count = self.add_output_attribute("AromRings", NodeTypes.INT)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("AromRings: --")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            count = rdMolDescriptors.CalcNumAromaticRings(data.mol)
            dpg.set_value(self.text, f"AromRings: {count}")
            self.manager.propagate(self.out_count)
        else:
            dpg.set_value(self.text, "AromRings: --")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            return rdMolDescriptors.CalcNumAromaticRings(data.mol)
        return None

    def get_params(self):
        return {}

    def set_params(self, p):
        pass

class MolInspectorNode(BaseNode):
    group = GROUP_NAME
    description = "Показывает сводку основных свойств молекулы"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.info_text = dpg.add_text("Нет молекулы")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            mol = data.mol
            mw = Descriptors.MolWt(mol)
            logp = Descriptors.MolLogP(mol)
            tpsa = Descriptors.TPSA(mol)
            hba = rdMolDescriptors.CalcNumHBA(mol)
            hbd = rdMolDescriptors.CalcNumHBD(mol)
            qed_val = QED.qed(mol)
            arom = rdMolDescriptors.CalcNumAromaticRings(mol)
            rotb = Descriptors.NumRotatableBonds(mol)
            formula = rdMolDescriptors.CalcMolFormula(mol)
            info = (
                f"Formula: {formula}\n"
                f"MW: {mw:.2f}  LogP: {logp:.2f}  TPSA: {tpsa:.2f}\n"
                f"HBA: {hba}  HBD: {hbd}  QED: {qed_val:.3f}\n"
                f"AromRings: {arom}  RotBonds: {rotb}"
            )
            dpg.set_value(self.info_text, info)
        else:
            dpg.set_value(self.info_text, "Нет молекулы")

    def get_params(self): return {}
    def set_params(self, p): pass


class NumAtomsNode(BaseNode):
    group = GROUP_NAME
    description = "Общее количество атомов (включая водород)"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_num = self.add_output_attribute("NumAtoms", NodeTypes.INT)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("NumAtoms: --")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            count = data.mol.GetNumAtoms()
            dpg.set_value(self.text, f"NumAtoms: {count}")
            self.manager.propagate(self.out_num)
        else:
            dpg.set_value(self.text, "NumAtoms: --")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            return data.mol.GetNumAtoms()
        return None

    def get_params(self): return {}
    def set_params(self, p): pass
