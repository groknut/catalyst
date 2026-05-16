import dearpygui.dearpygui as dpg
from rdkit import Chem
from rdkit.Chem import Draw
from pathlib import Path
from core.base_node import BaseNode
from core.node_types import NodeTypes
from mol_data import MolData

GROUP_NAME = "Output"

class MolImageSaveNode(BaseNode):
    group = GROUP_NAME
    description = "Автоматически сохраняет изображение молекулы при изменении входных данных"

    def build_node(self):
        self.in_pin = self.add_input_attribute("MolData", NodeTypes.MOL)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):

            self.filename_input = dpg.add_input_text(
                label="Filename", default_value="molecule.png", width=200,
                tag=f"filename_{self.id}"
            )

            dpg.add_input_int(label="Width", default_value=300, width=100,
                              tag=f"width_{self.id}")
            dpg.add_input_int(label="Height", default_value=200, width=100,
                              tag=f"height_{self.id}")

            self.status_text = dpg.add_text("", color=(150, 255, 150))

        self._prev_mol = None

    def update(self):
        self._do_save()

    def _do_save(self):
        data = self.manager.get_upstream_data(self.in_pin)

        if not isinstance(data, MolData) or not data.mol:
            dpg.set_value(self.status_text, "Нет молекулы")
            return

        mol = data.mol
        filename = dpg.get_value(f"filename_{self.id}").strip()
        width = dpg.get_value(f"width_{self.id}")
        height = dpg.get_value(f"height_{self.id}")

        if not filename:
            dpg.set_value(self.status_text, "Укажите имя файла")
            return

        if self.manager.project_dir:
            path = Path(self.manager.project_dir) / "output" / filename
        else:
            path = Path(filename)

        path.parent.mkdir(parents=True, exist_ok=True)

        try:
            img = Draw.MolToImage(mol, size=(width, height))
            img.save(str(path))
            dpg.set_value(self.status_text, f"Сохранено: {path.name}")
        except Exception as e:
            dpg.set_value(self.status_text, f"Ошибка: {e}")

    def get_params(self):
        return {
            "filename": dpg.get_value(f"filename_{self.id}"),
            "width": dpg.get_value(f"width_{self.id}"),
            "height": dpg.get_value(f"height_{self.id}")
        }

    def set_params(self, params):
        dpg.set_value(f"filename_{self.id}", params.get("filename", "molecule.png"))
        dpg.set_value(f"width_{self.id}", params.get("width", 300))
        dpg.set_value(f"height_{self.id}", params.get("height", 200))
