import dearpygui.dearpygui as dpg
from core.base_node import BaseNode

class StickyNoteNode(BaseNode):
    group = "Notes"
    description = "Текстовая заметка с автоматическим изменением размера"

    def build_node(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
            dpg.add_text("Note text:")
            self.text_input = dpg.add_input_text(
                label="", default_value="Введите заметку...",
                multiline=True, width=150, height=80,
                no_horizontal_scroll=True,
                tag=f"note_text_{self.id}",
                callback=lambda s,a,u: self._on_text_changed()
            )

    def _on_text_changed(self):
        text = dpg.get_value(self.text_input)
        lines = text.split('\n') if text else [""]
        max_line_len = max((len(line) for line in lines), default=0)
        new_width = max(150, min(800, max_line_len * 8))
        new_height = max(80, min(600, len(lines) * 20))
        dpg.configure_item(self.text_input, width=new_width, height=new_height)

    def get_params(self):
        return {"text": dpg.get_value(f"note_text_{self.id}")}

    def set_params(self, params):
        dpg.set_value(f"note_text_{self.id}", params.get("text", ""))
        self._on_text_changed()

    def get_output_value(self, pin_id):
        return None
    def update(self):
        pass
