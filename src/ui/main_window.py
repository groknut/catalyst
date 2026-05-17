import dearpygui.dearpygui as dpg
from core.node_types import TYPE_COLORS, NodeTypes
from pathlib import Path

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
                with dpg.menu(label="Edit"):
                    dpg.add_menu_item(label="Export Graph Image", callback=self._export_graph_image)

            dpg.add_spacer(height=15)


            with dpg.group(horizontal=True):
                with dpg.child_window(tag="library_panel", width=220, border=True):
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
            dpg.add_key_press_handler(dpg.mvKey_S, callback=self._handle_key_s)
            dpg.add_key_press_handler(dpg.mvKey_Left, callback=self._handle_move_node)
            dpg.add_key_press_handler(dpg.mvKey_Right, callback=self._handle_move_node)
            dpg.add_key_press_handler(dpg.mvKey_Up, callback=self._handle_move_node)
            dpg.add_key_press_handler(dpg.mvKey_Down, callback=self._handle_move_node)
            dpg.add_key_press_handler(dpg.mvKey_Tab, callback=self._handle_tab)
            dpg.add_key_press_handler(dpg.mvKey_B, callback=self._handle_key_b)

    def _handle_key_b(self):
        if dpg.is_key_down(dpg.mvKey_LControl) or dpg.is_key_down(dpg.mvKey_RControl):
            self._toggle_library()

    def _toggle_library(self):
        if dpg.is_item_shown("library_panel"):
            dpg.hide_item("library_panel")
        else:
            dpg.show_item("library_panel")

    # def _style_node(self, node_id, group):
    #     color = GROUP_COLORS.get(group, (80, 80, 100))
    #     with dpg.theme() as node_theme:
    #         with dpg.theme_component(dpg.mvNode):
    #             dpg.add_theme_color(dpg.mvNodeCol_TitleBar, color, category=dpg.mvThemeCat_Nodes)
    #             dpg.add_theme_color(dpg.mvNodeCol_TitleBarHovered,
    #                                 tuple(min(c+30,255) for c in color),
    #                                 category=dpg.mvThemeCat_Nodes)
    #             dpg.add_theme_color(dpg.mvNodeCol_TitleBarSelected,
    #                                 tuple(min(c+50,255) for c in color),
    #                                 category=dpg.mvThemeCat_Nodes)
    #     dpg.bind_item_theme(node_id, node_theme)

    def _handle_tab(self, sender, app_data):
        if dpg.is_key_down(dpg.mvKey_LControl) or dpg.is_key_down(dpg.mvKey_RControl):
            return
        cls = self.node_factory.get("StickyNoteNode")
        if cls is None:
            return
        self._add_node(cls)

    def _handle_move_node(self, sender, app_data):
        ctrl = dpg.is_key_down(dpg.mvKey_LControl) or dpg.is_key_down(dpg.mvKey_RControl)
        shift = dpg.is_key_down(dpg.mvKey_LShift) or dpg.is_key_down(dpg.mvKey_RShift)

        if not (ctrl and shift):
            return

        dx, dy = 0, 0
        if app_data == dpg.mvKey_Left:
            dx = -20
        elif app_data == dpg.mvKey_Right:
            dx = 20
        elif app_data == dpg.mvKey_Up:
            dy = -20
        elif app_data == dpg.mvKey_Down:
            dy = 20
        else:
            return

        for node_id in dpg.get_selected_nodes("main_editor"):
            x, y = dpg.get_item_pos(node_id)
            dpg.set_item_pos(node_id, (x + dx, y + dy))

    def _export_graph_image(self):
        if self.pm.current_file:
            output_dir = Path(self.pm.current_file).parent / "output"
        else:
            output_dir = Path(".")
        output_dir.mkdir(exist_ok=True)
        path = output_dir / "graph.png"
        dpg.output_frame_buffer(str(path))
        print(f"Graph image saved to {path}")


    def _handle_escape(self):
        self._save()
        dpg.stop_dearpygui()

    def _handle_key_q(self):
        """Ctrl+Q → выйти из редактора"""
        if dpg.is_key_down(dpg.mvKey_LControl) or dpg.is_key_down(dpg.mvKey_RControl):
            dpg.stop_dearpygui()

    def _handle_key_s(self, sender, app_data):
        """Ctrl+S → сохранить проект."""
        shift = dpg.is_key_down(dpg.mvKey_LShift) or dpg.is_key_down(dpg.mvKey_RShift)
        ctrl = dpg.is_key_down(dpg.mvKey_LControl) or dpg.is_key_down(dpg.mvKey_RControl)
        if shift and ctrl:
            self._export_graph_image()
        else:
            self._save()

    def _make_add_node_callback(self, node_class):
        """Возвращает коллбэк, который точно добавляет конкретный узел."""
        def callback(sender, app_data, user_data=None):
            self._add_node(node_class)

        return callback

    def _add_node(self, node_class):
        if node_class is None:
            print("ERROR: Tried to add None node class!")
            return
        node = node_class(self.pm.node_manager, node_class.__name__, parent="main_editor")
        # self._style_node(node.id, node_class.group)   # ← красим заголовок


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
        if not path:
            return

        for link_id in list(self.pm.node_manager.link_id_to_in.keys()):
                self.pm.node_manager.remove_link_by_id(link_id)
        for node_id in list(self.pm.node_manager.nodes.keys()):
            self.pm.node_manager.unregister_node(node_id)
            if dpg.does_item_exist(node_id):
                dpg.delete_item(node_id)
        # Сбрасываем состояние менеджера
        self.pm.node_manager.links.clear()
        self.pm.node_manager.nodes.clear()
        self.pm.node_manager.pin_to_node.clear()
        self.pm.node_manager.out_to_ins.clear()
        self.pm.node_manager.link_id_to_in.clear()

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
            # self._style_node(new_node.id, cls.group)
