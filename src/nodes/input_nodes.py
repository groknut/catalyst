import dearpygui.dearpygui as dpg
from rdkit import Chem

from core.base_node import BaseNode
from core.node_types import NodeTypes
from mol_data import MolData
from pathlib import Path

GROUP_NAME = "Input"

class SMILESInputNode(BaseNode):
    group = GROUP_NAME
    description = "Ввести SMILES строку молекулы"

    def build_node(self):
        self.out_mol = self.add_output_attribute("MolData", NodeTypes.MOL)
        self.out_smiles = self.add_output_attribute("SMILES", NodeTypes.SMILES)

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.smiles_input = dpg.add_input_text(
                label="SMILES", width=200, callback=lambda: self.on_smiles_changed()
            )

    def on_smiles_changed(self):
        self.manager.propagate(self.out_mol)
        self.manager.propagate(self.out_smiles)

    def get_output_value(self, pin_id):
        smi = dpg.get_value(self.smiles_input).strip()
        mol = Chem.MolFromSmiles(smi) if smi else None
        if pin_id == self.out_mol:
            return MolData(mol)
        elif pin_id == self.out_smiles:
            return smi if mol else "Invalid SMILES"
        return None

    def get_params(self):
        return {"smiles": dpg.get_value(self.smiles_input)}

    def set_params(self, params):
        dpg.set_value(self.smiles_input, params.get("smiles", ""))

# чтение из SDF файла
class SDFIndexInputNode(BaseNode):
    group = GROUP_NAME
    description = "Загружает молекулу по индексу из SDF-файла в input/"

    def build_node(self):
        self.out_mol = self.add_output_attribute("MolData", NodeTypes.MOL)
        self.out_count = self.add_output_attribute("Count", NodeTypes.INT)

        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            self.filename_input = dpg.add_input_text(
                label="Filename (.sdf)", default_value="molecules.sdf",
                width=200, tag=f"sdfidx_fn_{self.id}",
                callback=lambda: self._on_param_changed()
            )
            self.index_input = dpg.add_input_int(
                label="Index", default_value=0, min_value=0, max_value=9999,
                width=100, tag=f"sdfidx_idx_{self.id}",
                callback=lambda: self._on_param_changed()
            )
            with dpg.group(horizontal=True):
                dpg.add_button(label="◀ Prev", callback=lambda: self._move(-1))
                dpg.add_button(label="Next ▶", callback=lambda: self._move(1))
            self.status_text = dpg.add_text("Not loaded")

    def _on_param_changed(self):
        self._load()
        self.manager.propagate(self.out_mol)
        self.manager.propagate(self.out_count)

    def _move(self, delta):
        idx = dpg.get_value(f"sdfidx_idx_{self.id}") + delta
        if idx < 0:
            idx = 0
        dpg.set_value(f"sdfidx_idx_{self.id}", idx)
        self._on_param_changed()

    def _resolve_path(self):
        filename = dpg.get_value(f"sdfidx_fn_{self.id}").strip()
        if not filename:
            return None
        if self.manager.project_dir:
            return Path(self.manager.project_dir) / "input" / filename
        return Path(filename)

    def _load(self):
        path = self._resolve_path()
        if not path or not path.exists():
            self._cached_mols = []
            dpg.set_value(self.status_text, "File not found")
            return
        try:
            suppl = Chem.SDMolSupplier(str(path))
            mols = [MolData(m) for m in suppl if m is not None]
            self._cached_mols = mols
            total = len(mols)
            idx = dpg.get_value(f"sdfidx_idx_{self.id}")
            if total == 0:
                dpg.set_value(self.status_text, "No valid molecules")
            elif 0 <= idx < total:
                dpg.set_value(self.status_text, f"Loaded {total} mols, showing #{idx+1}")
            else:
                dpg.set_value(self.status_text, f"Index out of range (0–{total-1})")
        except Exception as e:
            self._cached_mols = []
            dpg.set_value(self.status_text, f"Error: {e}")

    def get_output_value(self, pin_id):
        mols = getattr(self, '_cached_mols', [])
        if pin_id == self.out_count:
            return len(mols)
        idx = dpg.get_value(f"sdfidx_idx_{self.id}")
        if 0 <= idx < len(mols):
            return mols[idx]
        return None

    def get_params(self):
        return {
            "filename": dpg.get_value(f"sdfidx_fn_{self.id}"),
            "index": dpg.get_value(f"sdfidx_idx_{self.id}")
        }
    def set_params(self, params):
        dpg.set_value(f"sdfidx_fn_{self.id}", params.get("filename", "molecules.sdf"))
        dpg.set_value(f"sdfidx_idx_{self.id}", params.get("index", 0))
        self._load()
