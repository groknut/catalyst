import dearpygui.dearpygui as dpg
from rdkit.Chem import Draw

from core.base_node import BaseNode
from core.node_types import NodeTypes
from mol_data import MolData
from pathlib import Path

GROUP_NAME = "Output"


class MolImageSaverNode(BaseNode):
    group = GROUP_NAME

    def build_node(self):
        self.in_pin = self.add_input_attribute("MolData", NodeTypes.MOL)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_input_text(
                label="Filename",
                default_value="molecule.png",
                width=200,
                tag=f"filename_{self.id}",
            )
            dpg.add_input_int(
                label="Width", default_value=300, width=100, tag=f"width_{self.id}"
            )
            dpg.add_input_int(
                label="Height", default_value=200, width=100, tag=f"height_{self.id}"
            )
            dpg.add_button(label="Save Image", callback=lambda: self.save_image())
            self.status_text = dpg.add_text("", color=(150, 255, 150))

    def _resolve_path(self):
        """Полный путь для сохранения: <project>/output/<filename>"""
        filename = dpg.get_value(f"filename_{self.id}").strip()
        if not filename:
            return None
        if self.manager.project_dir:
            return self.manager.project_dir / "output" / filename
        return Path(filename)

    def save_image(self):
        data = self.manager.get_upstream_data(self.in_pin)
        if not isinstance(data, MolData) or not data.mol:
            dpg.set_value(self.status_text, "No molecule")
            return
        path = self._resolve_path()
        if path is None:
            dpg.set_value(self.status_text, "No filename")
            return
        mol = data.mol
        width = dpg.get_value(f"width_{self.id}")
        height = dpg.get_value(f"height_{self.id}")
        try:
            img = Draw.MolToImage(mol, size=(width, height))
            path.parent.mkdir(parents=True, exist_ok=True)
            img.save(str(path))
            dpg.set_value(self.status_text, f"Saved: {path.name}")
        except Exception as e:
            dpg.set_value(self.status_text, f"Error: {e}")

    def get_params(self):
        return {
            "filename": dpg.get_value(f"filename_{self.id}"),
            "width": dpg.get_value(f"width_{self.id}"),
            "height": dpg.get_value(f"height_{self.id}"),
        }

    def set_params(self, params):
        dpg.set_value(f"filename_{self.id}", params.get("filename", "molecule.png"))
        dpg.set_value(f"width_{self.id}", params.get("width", 300))
        dpg.set_value(f"height_{self.id}", params.get("height", 200))
