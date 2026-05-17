import dearpygui.dearpygui as dpg
from core.base_node import BaseNode
from core.node_types import NodeTypes

# узел математической операции между двумя числами
class MathNode(BaseNode):
    group = "Math"
    description = "Арифметическая операция над двумя числами"

    def build_node(self):
        self.in_a = self.add_input_attribute("A", NodeTypes.FLOAT)
        self.in_b = self.add_input_attribute("B", NodeTypes.FLOAT)
        self.out_result = self.add_output_attribute("Result", NodeTypes.FLOAT)

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.op_combo = dpg.add_combo(
                items=["+", "-", "*", "/"],
                default_value="+",
                width=80,
                callback=lambda: self._on_param_changed(),
            )
            self.result_text = dpg.add_text("Result: --")

    def _on_param_changed(self):
        self.update()
        self.manager.propagate(self.out_result)

    def update(self):
        a = self.manager.get_upstream_data(self.in_a)
        b = self.manager.get_upstream_data(self.in_b)
        op = dpg.get_value(self.op_combo)

        if a is None or b is None:
            dpg.set_value(self.result_text, "Result: --")
            return

        try:
            a = float(a)
            b = float(b)
            if op == "+":
                res = a + b
            elif op == "-":
                res = a - b
            elif op == "*":
                res = a * b
            elif op == "/":
                res = a / b if b != 0 else float("inf")
            dpg.set_value(self.result_text, f"Result: {res:.4f}")
        except (ValueError, TypeError):
            dpg.set_value(self.result_text, "Error")

    def get_output_value(self, pin_id):
        a = self.manager.get_upstream_data(self.in_a)
        b = self.manager.get_upstream_data(self.in_b)
        op = dpg.get_value(self.op_combo)
        if a is None or b is None:
            return None
        try:
            a = float(a)
            b = float(b)
            if op == "+":
                return a + b
            elif op == "-":
                return a - b
            elif op == "*":
                return a * b
            elif op == "/":
                return a / b if b != 0 else float("inf")
        except:
            return None

    def get_params(self):
        return {"operation": dpg.get_value(self.op_combo)}

    def set_params(self, params):
        dpg.set_value(self.op_combo, params.get("operation", "+"))
