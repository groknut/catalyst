import dearpygui.dearpygui as dpg
from core.node_types import TYPE_COLORS, NodeTypes


class MainWindow:
    def __init__(
        self,
        project_manager,
        node_factory,
        groups,
        config=None,
    ):
        self.pm = project_manager
        self.node_factory = node_factory
        self.groups = groups
        self._setup_ui()

    def _setup_ui(self):

        with dpg.file_dialog(
            tag="open_editor_dialog",
            show=False,
            width=700,
            height=400,
            callback=self._open_in_editor_callback,
        ):
            dpg.add_file_extension(".catalyst")


        with dpg.window(
            tag="main_window",
            no_title_bar=True,
            no_resize=True,
            no_move=True,
            no_close=True,
            width=-1,
            height=-1,
        ):
            with dpg.viewport_menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="Save", callback=self._save)
                    dpg.add_menu_item(
                        label="Open...",
                        callback=lambda: dpg.show_item("open_editor_dialog"),
                    )

            dpg.add_spacer(height=15)


            with dpg.group(horizontal=True):
                with dpg.child_window(width=220, border=True):
                    dpg.add_spacer(height=15)
                    dpg.add_text("Node Library", color=(100, 200, 255))
                    dpg.add_separator()

                    for grp, names in self.groups.items():
                        with dpg.collapsing_header(label=grp, default_open=False):
                            for name in names:
                                cls = self.node_factory.get(name)
                                if cls is None:
                                    continue

                                btn_callback = self._make_add_node_callback(cls)
                                btn = dpg.add_button(
                                    label=f"Add {name}", width=-1, callback=btn_callback
                                )
                                desc = getattr(cls, "description", "")

                                if desc:
                                    with dpg.tooltip(btn):
                                        dpg.add_text(desc)

                    dpg.add_spacer(height=15)
                    dpg.add_text("Pin Types", color=(150, 150, 150))

                    for t, color in TYPE_COLORS.items():
                        dpg.add_text(f"● {t}", color=color)

                with dpg.node_editor(
                    tag="main_editor", callback=self._link_callback, width=-1, height=-1, minimap=True, minimap_location=dpg.mvNodeMiniMap_Location_TopRight
                ):
                    pass

        dpg.set_primary_window("main_window", True)

        with dpg.handler_registry():
            dpg.add_key_press_handler(dpg.mvKey_Delete, callback=self._delete_selected)
            dpg.add_key_press_handler(dpg.mvKey_S, callback=self._handle_key_s)
            dpg.add_key_press_handler(dpg.mvKey_Q, callback=self._handle_key_q)
            dpg.add_key_press_handler(dpg.mvKey_Escape, callback=self._handle_escape)
            dpg.add_key_press_handler(dpg.mvKey_D, callback=self._handle_key_d)

    def _handle_escape(self):
        self._save()
        dpg.stop_dearpygui()

    def _handle_key_q(self):
        """Ctrl+Q → выйти из редактора"""
        if dpg.is_key_down(dpg.mvKey_LControl) or dpg.is_key_down(dpg.mvKey_RControl):
            dpg.stop_dearpygui()

    def _handle_key_s(self, sender, app_data):
        """Ctrl+S → сохранить проект."""
        if dpg.is_key_down(dpg.mvKey_LControl) or dpg.is_key_down(dpg.mvKey_RControl):
            self._save()

    def _autosave_callback(self, sender, app_data):
        """Вызывается таймером каждые 60 секунд (если autosave включён)."""
        if self.pm.current_file is not None:
            self.pm.save_project()

    def _make_add_node_callback(self, node_class):
        """Возвращает коллбэк, который точно добавляет конкретный узел."""

        def callback(sender, app_data, user_data=None):
            self._add_node(node_class)

        return callback

    def _add_node(self, node_class):
        if node_class is None:
            print("ERROR: Tried to add None node class!")
            return
        node_class(self.pm.node_manager, node_class.__name__, parent="main_editor")

    def _link_callback(self, sender, app_data):
        out_pin, in_pin = app_data
        out_node = self.pm.node_manager.pin_to_node.get(out_pin)
        in_node = self.pm.node_manager.pin_to_node.get(in_pin)
        if out_node and in_node:
            out_type = out_node.pin_types.get(out_pin, NodeTypes.ANY)
            in_type = in_node.pin_types.get(in_pin, NodeTypes.ANY)
            if (
                out_type != NodeTypes.ANY
                and in_type != NodeTypes.ANY
                and out_type != in_type
            ):
                return
        link_id = dpg.add_node_link(out_pin, in_pin, parent=sender)
        self.pm.node_manager.add_link(out_pin, in_pin, link_id=link_id)

    def _delete_selected(self):
        for link_id in dpg.get_selected_links("main_editor"):
            self.pm.node_manager.remove_link_by_id(link_id)
        for node_id in dpg.get_selected_nodes("main_editor"):
            self.pm.node_manager.unregister_node(node_id)
            if dpg.does_item_exist(node_id):
                dpg.delete_item(node_id)

    def _save(self):
        self.pm.save_project()

    def _save_as_callback(self, sender, app_data):
        path = app_data.get("file_path_name", "")
        if path:
            self.pm.save_project_as(path)

    def _open_in_editor_callback(self, sender, app_data):
        path = app_data.get("file_path_name", "")
        if path:
            self.pm.open_project(path, self.node_factory)

    def _handle_key_d(self, sender, app_data):
        if dpg.is_key_down(dpg.mvKey_LControl) or dpg.is_key_down(dpg.mvKey_RControl):
            self._duplicate_selected()

    def _duplicate_selected(self):
        selected = dpg.get_selected_nodes("main_editor")

        for node_id in selected:
            node = self.pm.node_manager.nodes.get(node_id)
            if not node:
                continue

            params = node.get_params()
            pos = dpg.get_item_pos(node_id)
            cls = type(node)

            new_node = cls(
                self.pm.node_manager,
                dpg.get_item_label(node_id),
                parent="main_editor",
                pos=(pos[0] + 200, pos[1])
            )

            new_node.set_params(params)
