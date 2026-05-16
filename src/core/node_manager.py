import dearpygui.dearpygui as dpg
from .node_types import NodeTypes

class NodeManager:
    def __init__(self, logger=None):
        self.nodes = {}
        self.links = {}
        self.pin_to_node = {}
        self.out_to_ins = {}
        self.link_id_to_in = {}
        self.project_dir = None
        self.logger = logger

    def register_node(self, node):
        self.nodes[node.id] = node
        for pin in node.inputs + node.outputs:
            self.pin_to_node[pin] = node

    def unregister_node(self, node_id):
        node = self.nodes.pop(node_id, None)
        if not node:
            return
        for in_pin in node.inputs:
            self.remove_link_by_pin(in_pin, update_gui=False)
            self.pin_to_node.pop(in_pin, None)
        for out_pin in node.outputs:
            if out_pin in self.out_to_ins:
                for in_pin in list(self.out_to_ins[out_pin]):
                    self.remove_link_by_pin(in_pin, update_gui=False)
                del self.out_to_ins[out_pin]
            self.pin_to_node.pop(out_pin, None)

    def add_link(self, out_pin, in_pin, link_id=None):
        out_node = self.pin_to_node.get(out_pin)
        in_node = self.pin_to_node.get(in_pin)

        if not out_node or not in_node:
            return

        out_type = out_node.pin_types.get(out_pin, NodeTypes.ANY)
        in_type = in_node.pin_types.get(in_pin, NodeTypes.ANY)
        if out_type != NodeTypes.ANY and in_type != NodeTypes.ANY and out_type != in_type:
            return
        if in_pin in self.links:
            self.remove_link_by_pin(in_pin)
        self.links[in_pin] = out_pin
        self.out_to_ins.setdefault(out_pin, set()).add(in_pin)
        if link_id is not None:
            self.link_id_to_in[link_id] = in_pin
        target = self.pin_to_node.get(in_pin)
        if target:
            target.update()
            for out_p in target.outputs:
                self.propagate(out_p)

    def remove_link_by_pin(self, in_pin, update_gui=True):
        out_pin = self.links.pop(in_pin, None)
        if out_pin and out_pin in self.out_to_ins:
            self.out_to_ins[out_pin].discard(in_pin)
            if not self.out_to_ins[out_pin]:
                del self.out_to_ins[out_pin]
        for lid, pin in list(self.link_id_to_in.items()):
            if pin == in_pin:
                del self.link_id_to_in[lid]
                if update_gui and dpg.does_item_exist(lid):
                    dpg.delete_item(lid)
                break

    def remove_link_by_id(self, link_id):
        in_pin = self.link_id_to_in.pop(link_id, None)
        if in_pin:
            self.remove_link_by_pin(in_pin, update_gui=False)
        if dpg.does_item_exist(link_id):
            dpg.delete_item(link_id)

    def propagate(self, out_pin, visited_nodes=None):
        if visited_nodes is None:
            visited_nodes = set()
        source_node = self.pin_to_node.get(out_pin)
        if not source_node or source_node.id in visited_nodes:
            return
        visited_nodes.add(source_node.id)
        for in_pin in self.out_to_ins.get(out_pin, []):
            target = self.pin_to_node.get(in_pin)
            if target and target.id not in visited_nodes:
                target.update()
                for next_out in target.outputs:
                    self.propagate(next_out, visited_nodes)

    def get_upstream_data(self, in_pin):
        out_pin = self.links.get(in_pin)
        if out_pin:
            source_node = self.pin_to_node.get(out_pin)
            if source_node:
                return source_node.get_output_value(out_pin)
        return None

    def load_from_data(self, data, node_factory):

        for node_id in list(self.nodes.keys()):
            self.unregister_node(node_id)
            if dpg.does_item_exist(node_id):
                dpg.delete_item(node_id)

        self.links.clear()
        self.pin_to_node.clear()
        self.out_to_ins.clear()
        self.link_id_to_in.clear()

        old_to_new_pins = {}
        missed_types = []

        for ndata in data.get("nodes", []):
            cls_name = ndata["type"]
            if cls_name not in node_factory:
                self.logger.warning(f"Unknown node type {cls_name} – skipping")
                missed_types.append(cls_name)
                continue
            node_cls = node_factory[cls_name]
            pos = tuple(ndata.get("pos", (10, 10)))
            node = node_cls(self, ndata["label"], parent="main_editor", pos=pos)
            if "params" in ndata:
                node.set_params(ndata["params"])

            for i, old_pin in enumerate(ndata.get("inputs", [])):
                if i < len(node.inputs):
                    old_to_new_pins[old_pin] = node.inputs[i]
            for i, old_pin in enumerate(ndata.get("outputs", [])):
                if i < len(node.outputs):
                    old_to_new_pins[old_pin] = node.outputs[i]

        for in_old, out_old in data.get("links", []):
            in_new = old_to_new_pins.get(in_old)
            out_new = old_to_new_pins.get(out_old)
            if in_new and out_new:
                link_id = dpg.add_node_link(out_new, in_new, parent="main_editor")
                self.add_link(out_new, in_new, link_id=link_id)
            else:
                self.logger.warning(f"Skipping link {out_old}->{in_old}: pin mapping failed")

        self._missed_types_in_last_load = missed_types
        self.logger.info(f"Loaded {len(self.nodes)} nodes, {len(self.links)} links.")
