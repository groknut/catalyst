import dearpygui.dearpygui as dpg
from .node_types import NodeTypes, TYPE_COLORS


class BaseNode:
    group = "Ungrouped"
    description = ""

    def __init__(self, manager, label, pos=(10, 10), parent=""):
        self.manager = manager
        self.inputs = []
        self.outputs = []
        self.pin_types = {}  # {pin_id: str}

        with dpg.node(label=label, pos=pos, parent=parent) as self.id:
            self.build_node()
        self.manager.register_node(self)

    def build_node(self):
        pass

    def update(self):
        pass

    def get_output_value(self, pin_id):
        return None

    def add_input_attribute(self, label, pin_type=NodeTypes.ANY):
        color = TYPE_COLORS.get(pin_type, (150, 150, 150))
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input) as pin_id:
            dpg.add_text(f"● {label}", color=color)
        self.inputs.append(pin_id)
        self.pin_types[pin_id] = pin_type
        return pin_id

    def add_output_attribute(self, label, pin_type=NodeTypes.ANY):
        color = TYPE_COLORS.get(pin_type, (150, 150, 150))
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output) as pin_id:
            dpg.add_text(f"● {label}", color=color)
        self.outputs.append(pin_id)
        self.pin_types[pin_id] = pin_type
        return pin_id

    # --- Сериализация ---
    def get_params(self):
        return {}

    def set_params(self, params):
        pass

    def serialize(self):
        return {
            "id": self.id,
            "type": self.__class__.__name__,
            "label": dpg.get_item_label(self.id),
            "pos": dpg.get_item_pos(self.id),
            "inputs": self.inputs,
            "outputs": self.outputs,
            "params": self.get_params(),
        }
