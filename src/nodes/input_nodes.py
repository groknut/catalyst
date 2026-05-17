import dearpygui.dearpygui as dpg
from rdkit import Chem

from core.base_node import BaseNode
from core.node_types import NodeTypes
from mol_data import MolData

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
