import dearpygui.dearpygui as dpg
from rdkit.Chem import Descriptors, rdMolDescriptors
from core.base_node import BaseNode
from core.node_types import NodeTypes
from mol_data import MolData

GROUP_NAME = "Filters"

#  Правило Липински
class RuleOfFiveFilterNode(BaseNode):
    group = GROUP_NAME
    description = "Правило Липински (Rule of 5): MW ≤ 500, LogP ≤ 5, HBD ≤ 5, HBA ≤ 10"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_pass = self.add_output_attribute("Pass", NodeTypes.BOOL)
        self.out_mol = self.add_output_attribute("MolOut", NodeTypes.MOL)

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_text("Rule of 5 check")
            self.status_text = dpg.add_text("")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            mol = data.mol
            mw = Descriptors.MolWt(mol)
            logp = Descriptors.MolLogP(mol)
            hbd = rdMolDescriptors.CalcNumHBD(mol)
            hba = rdMolDescriptors.CalcNumHBA(mol)

            passed = (mw <= 500) and (logp <= 5) and (hbd <= 5) and (hba <= 10)
            dpg.set_value(
                self.status_text,
                f"MW={mw:.1f} LogP={logp:.2f} HBD={hbd} HBA={hba} -> {'PASS' if passed else 'FAIL'}",
            )
            self.manager.propagate(self.out_pass)
            self.manager.propagate(self.out_mol)
        else:
            dpg.set_value(self.status_text, "Нет молекулы")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            mol = data.mol
            mw = Descriptors.MolWt(mol)
            logp = Descriptors.MolLogP(mol)
            hbd = rdMolDescriptors.CalcNumHBD(mol)
            hba = rdMolDescriptors.CalcNumHBA(mol)
            passed = (mw <= 500) and (logp <= 5) and (hbd <= 5) and (hba <= 10)
            if pin_id == self.out_pass:
                return passed
            elif pin_id == self.out_mol:
                return data if passed else MolData(None)
        return None

    def get_params(self):
        return {}

    def set_params(self, p):
        pass



#  Фильтр по молекулярной массе
class MolWeightFilterNode(BaseNode):
    group = GROUP_NAME
    description = "Пропускает молекулу, если MW находится в заданном диапазоне"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)

        self.out_pass = self.add_output_attribute("Pass", NodeTypes.BOOL)
        self.out_mol = self.add_output_attribute("MolOut", NodeTypes.MOL)

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_text("Диапазон MW:")
            self.min_input = dpg.add_input_float(
                label="Min", default_value=0.0, width=120, tag=f"mw_min_{self.id}"
            )
            self.max_input = dpg.add_input_float(
                label="Max", default_value=500.0, width=120, tag=f"mw_max_{self.id}"
            )
            self.status_text = dpg.add_text("")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            mw = Descriptors.MolWt(data.mol)
            mn = dpg.get_value(f"mw_min_{self.id}")
            mx = dpg.get_value(f"mw_max_{self.id}")
            passed = mn <= mw <= mx
            dpg.set_value(
                self.status_text, f"MW={mw:.1f}: {'PASS' if passed else 'FAIL'}"
            )
            self.manager.propagate(self.out_pass)
            self.manager.propagate(self.out_mol)
        else:
            dpg.set_value(self.status_text, "Нет молекулы")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            mw = Descriptors.MolWt(data.mol)
            mn = dpg.get_value(f"mw_min_{self.id}")
            mx = dpg.get_value(f"mw_max_{self.id}")
            if pin_id == self.out_pass:
                return mn <= mw <= mx
            elif pin_id == self.out_mol:
                return data if mn <= mw <= mx else MolData(None)
        return None

    def get_params(self):
        return {
            "min": dpg.get_value(f"mw_min_{self.id}"),
            "max": dpg.get_value(f"mw_max_{self.id}"),
        }

    def set_params(self, params):
        dpg.set_value(f"mw_min_{self.id}", params.get("min", 0.0))
        dpg.set_value(f"mw_max_{self.id}", params.get("max", 500.0))



#  Фильтр по LogP

class LogPFilterNode(BaseNode):
    group = GROUP_NAME
    description = "Пропускает молекулу, если LogP в заданном диапазоне"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_pass = self.add_output_attribute("Pass", NodeTypes.BOOL)
        self.out_mol = self.add_output_attribute("MolOut", NodeTypes.MOL)

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_text("Диапазон LogP:")
            self.min_input = dpg.add_input_float(
                label="Min", default_value=-5.0, width=120, tag=f"logp_min_{self.id}"
            )
            self.max_input = dpg.add_input_float(
                label="Max", default_value=5.0, width=120, tag=f"logp_max_{self.id}"
            )
            self.status_text = dpg.add_text("")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            logp = Descriptors.MolLogP(data.mol)
            mn = dpg.get_value(f"logp_min_{self.id}")
            mx = dpg.get_value(f"logp_max_{self.id}")
            passed = mn <= logp <= mx
            dpg.set_value(
                self.status_text, f"LogP={logp:.2f}: {'PASS' if passed else 'FAIL'}"
            )
            self.manager.propagate(self.out_pass)
            self.manager.propagate(self.out_mol)
        else:
            dpg.set_value(self.status_text, "Нет молекулы")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            logp = Descriptors.MolLogP(data.mol)
            mn = dpg.get_value(f"logp_min_{self.id}")
            mx = dpg.get_value(f"logp_max_{self.id}")
            if pin_id == self.out_pass:
                return mn <= logp <= mx
            elif pin_id == self.out_mol:
                return data if mn <= logp <= mx else MolData(None)
        return None

    def get_params(self):
        return {
            "min": dpg.get_value(f"logp_min_{self.id}"),
            "max": dpg.get_value(f"logp_max_{self.id}"),
        }

    def set_params(self, params):
        dpg.set_value(f"logp_min_{self.id}", params.get("min", -5.0))
        dpg.set_value(f"logp_max_{self.id}", params.get("max", 5.0))



#  Фильтр по количеству тяжёлых атомов

class HeavyAtomFilterNode(BaseNode):
    group = GROUP_NAME
    description = "Пропускает молекулу по числу тяжёлых атомов"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_pass = self.add_output_attribute("Pass", NodeTypes.BOOL)
        self.out_mol = self.add_output_attribute("MolOut", NodeTypes.MOL)

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_text("Диапазон тяжёлых атомов:")
            self.min_input = dpg.add_input_int(
                label="Min", default_value=0, width=120, tag=f"heavy_min_{self.id}"
            )
            self.max_input = dpg.add_input_int(
                label="Max", default_value=100, width=120, tag=f"heavy_max_{self.id}"
            )
            self.status_text = dpg.add_text("")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            ha = Descriptors.HeavyAtomCount(data.mol)
            mn = dpg.get_value(f"heavy_min_{self.id}")
            mx = dpg.get_value(f"heavy_max_{self.id}")
            passed = mn <= ha <= mx
            dpg.set_value(
                self.status_text, f"HeavyAtoms={ha}: {'PASS' if passed else 'FAIL'}"
            )
            self.manager.propagate(self.out_pass)
            self.manager.propagate(self.out_mol)
        else:
            dpg.set_value(self.status_text, "Нет молекулы")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            ha = Descriptors.HeavyAtomCount(data.mol)
            mn = dpg.get_value(f"heavy_min_{self.id}")
            mx = dpg.get_value(f"heavy_max_{self.id}")
            if pin_id == self.out_pass:
                return mn <= ha <= mx
            elif pin_id == self.out_mol:
                return data if mn <= ha <= mx else MolData(None)
        return None

    def get_params(self):
        return {
            "min": dpg.get_value(f"heavy_min_{self.id}"),
            "max": dpg.get_value(f"heavy_max_{self.id}"),
        }

    def set_params(self, params):
        dpg.set_value(f"heavy_min_{self.id}", params.get("min", 0))
        dpg.set_value(f"heavy_max_{self.id}", params.get("max", 100))



#  Фильтр по числу вращающихся связей

class RotBondsFilterNode(BaseNode):
    group = GROUP_NAME
    description = "Пропускает молекулу по числу вращающихся связей"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.out_pass = self.add_output_attribute("Pass", NodeTypes.BOOL)
        self.out_mol = self.add_output_attribute("MolOut", NodeTypes.MOL)

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_text("Диапазон RotBonds:")
            self.min_input = dpg.add_input_int(
                label="Min", default_value=0, width=120, tag=f"rotb_min_{self.id}"
            )
            self.max_input = dpg.add_input_int(
                label="Max", default_value=10, width=120, tag=f"rotb_max_{self.id}"
            )
            self.status_text = dpg.add_text("")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            rb = Descriptors.NumRotatableBonds(data.mol)
            mn = dpg.get_value(f"rotb_min_{self.id}")
            mx = dpg.get_value(f"rotb_max_{self.id}")
            passed = mn <= rb <= mx
            dpg.set_value(
                self.status_text, f"RotBonds={rb}: {'PASS' if passed else 'FAIL'}"
            )
            self.manager.propagate(self.out_pass)
            self.manager.propagate(self.out_mol)
        else:
            dpg.set_value(self.status_text, "Нет молекулы")

    def get_output_value(self, pin_id):
        data = self.manager.get_upstream_data(self.in_mol)
        if isinstance(data, MolData) and data.mol:
            rb = Descriptors.NumRotatableBonds(data.mol)
            mn = dpg.get_value(f"rotb_min_{self.id}")
            mx = dpg.get_value(f"rotb_max_{self.id}")
            if pin_id == self.out_pass:
                return mn <= rb <= mx
            elif pin_id == self.out_mol:
                return data if mn <= rb <= mx else MolData(None)
        return None

    def get_params(self):
        return {
            "min": dpg.get_value(f"rotb_min_{self.id}"),
            "max": dpg.get_value(f"rotb_max_{self.id}"),
        }

    def set_params(self, params):
        dpg.set_value(f"rotb_min_{self.id}", params.get("min", 0))
        dpg.set_value(f"rotb_max_{self.id}", params.get("max", 10))
