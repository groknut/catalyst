import dearpygui.dearpygui as dpg
from core.base_node import BaseNode
from core.node_types import NodeTypes
from mol_data import MolData

GROUP_NAME = "Logic"
# узел проверки верности условия
class IfNode(BaseNode):
    group = GROUP_NAME
    description = (
        "Направляет молекулу на True-выход, если флаг Pass=True, иначе на False-выход"
    )

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)
        self.in_flag = self.add_input_attribute("Pass", NodeTypes.BOOL)

        self.out_true = self.add_output_attribute("True", NodeTypes.MOL)
        self.out_false = self.add_output_attribute("False", NodeTypes.MOL)

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.status_text = dpg.add_text("Ожидание данных...")

    def update(self):
        mol_data = self.manager.get_upstream_data(self.in_mol)
        flag = self.manager.get_upstream_data(self.in_flag)

        if isinstance(mol_data, MolData) and mol_data.mol is not None and flag is True:
            dpg.set_value(self.status_text, "Открыт → True")
            self.manager.propagate(self.out_true)
        elif (
            isinstance(mol_data, MolData) and mol_data.mol is not None and flag is False
        ):
            dpg.set_value(self.status_text, "Закрыт → False")
            self.manager.propagate(self.out_false)
        else:
            reason = "нет флага" if flag is None else "флаг False"
            if not (isinstance(mol_data, MolData) and mol_data.mol):
                reason = "нет молекулы"
            dpg.set_value(self.status_text, f"Ожидание ({reason})")

    def get_output_value(self, pin_id):
        mol_data = self.manager.get_upstream_data(self.in_mol)
        flag = self.manager.get_upstream_data(self.in_flag)

        if isinstance(mol_data, MolData) and mol_data.mol is not None:
            if pin_id == self.out_true and flag is True:
                return mol_data
            if pin_id == self.out_false and flag is False:
                return mol_data
        return MolData(None)

    def get_params(self):
        return {}

    def set_params(self, p):
        pass


class BoolAndNode(BaseNode):
    group = "Logic"
    description = "Логическое И (AND) для двух флагов"

    def build_node(self):
        self.in_a = self.add_input_attribute("A", NodeTypes.BOOL)
        self.in_b = self.add_input_attribute("B", NodeTypes.BOOL)
        self.out_result = self.add_output_attribute("A AND B", NodeTypes.BOOL)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("AND: --")

    def update(self):
        a = self.manager.get_upstream_data(self.in_a)
        b = self.manager.get_upstream_data(self.in_b)
        if a is not None and b is not None:
            res = bool(a) and bool(b)
            dpg.set_value(self.text, f"AND: {res}")
            self.manager.propagate(self.out_result)
        else:
            dpg.set_value(self.text, "AND: --")

    def get_output_value(self, pin_id):
        a = self.manager.get_upstream_data(self.in_a)
        b = self.manager.get_upstream_data(self.in_b)
        if a is not None and b is not None:
            return bool(a) and bool(b)
        return None

    def get_params(self): return {}
    def set_params(self, p): pass


class BoolOrNode(BaseNode):
    group = "Logic"
    description = "Логическое ИЛИ (OR) для двух флагов"

    def build_node(self):
        self.in_a = self.add_input_attribute("A", NodeTypes.BOOL)
        self.in_b = self.add_input_attribute("B", NodeTypes.BOOL)
        self.out_result = self.add_output_attribute("A OR B", NodeTypes.BOOL)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.text = dpg.add_text("OR: --")

    def update(self):
        a = self.manager.get_upstream_data(self.in_a)
        b = self.manager.get_upstream_data(self.in_b)
        if a is not None and b is not None:
            res = bool(a) or bool(b)
            dpg.set_value(self.text, f"OR: {res}")
            self.manager.propagate(self.out_result)
        else:
            dpg.set_value(self.text, "OR: --")

    def get_output_value(self, pin_id):
        a = self.manager.get_upstream_data(self.in_a)
        b = self.manager.get_upstream_data(self.in_b)
        if a is not None and b is not None:
            return bool(a) or bool(b)
        return None

    def get_params(self): return {}
    def set_params(self, p): pass
