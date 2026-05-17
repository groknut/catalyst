import dearpygui.dearpygui as dpg
from rdkit.Chem import Draw, Descriptors, QED, rdMolDescriptors
from pathlib import Path
from core.base_node import BaseNode
from core.node_types import NodeTypes
from mol_data import MolData
import csv

GROUP_NAME = "Output"

# узел для сохранения изображения молекулы
class MolImageSaveNode(BaseNode):
    group = GROUP_NAME
    description = (
        "Автоматически сохраняет изображение молекулы при изменении входных данных"
    )

    def build_node(self):
        self.in_pin = self.add_input_attribute("MolData", NodeTypes.MOL)
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.filename_input = dpg.add_input_text(
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
            "height": dpg.get_value(f"height_{self.id}"),
        }

    def set_params(self, params):
        dpg.set_value(f"filename_{self.id}", params.get("filename", "molecule.png"))
        dpg.set_value(f"width_{self.id}", params.get("width", 300))
        dpg.set_value(f"height_{self.id}", params.get("height", 200))

# узел для логгирования молекул в csv
class CSVLoggerNode(BaseNode):
    group = GROUP_NAME
    description = "Дописывает свойства молекулы в CSV-файл при каждом обновлении"

    def build_node(self):
        self.in_mol = self.add_input_attribute("MolData", NodeTypes.MOL)

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.filename_input = dpg.add_input_text(
                label="Filename",
                default_value="molecules.csv",
                width=200,
                tag=f"csvlog_fn_{self.id}",
            )
            self.status_text = dpg.add_text("Файл: --")

    def update(self):
        data = self.manager.get_upstream_data(self.in_mol)
        if not isinstance(data, MolData) or not data.mol:
            return

        filename = dpg.get_value(f"csvlog_fn_{self.id}").strip()
        if not filename:
            dpg.set_value(self.status_text, "Укажите имя файла")
            return

        if self.manager.project_dir:
            path = Path(self.manager.project_dir) / "output" / filename
        else:
            path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        mol = data.mol
        smiles = data.smiles
        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        tpsa = Descriptors.TPSA(mol)
        qed_val = QED.qed(mol)
        hba = rdMolDescriptors.CalcNumHBA(mol)
        hbd = rdMolDescriptors.CalcNumHBD(mol)
        formula = rdMolDescriptors.CalcMolFormula(mol)

        file_exists = path.exists()
        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(
                    ["SMILES", "MW", "LogP", "TPSA", "QED", "HBA", "HBD", "Formula"]
                )
            writer.writerow(
                [
                    smiles,
                    f"{mw:.2f}",
                    f"{logp:.2f}",
                    f"{tpsa:.2f}",
                    f"{qed_val:.3f}",
                    hba,
                    hbd,
                    formula,
                ]
            )

        dpg.set_value(self.status_text, f"Добавлено в {filename}")

    # Параметры: только имя файла
    def get_params(self):
        return {"filename": dpg.get_value(f"csvlog_fn_{self.id}")}

    def set_params(self, params):
        dpg.set_value(f"csvlog_fn_{self.id}", params.get("filename", "molecules.csv"))
