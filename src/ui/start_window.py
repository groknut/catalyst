import dearpygui.dearpygui as dpg
import webbrowser


class StartWindow:
    def __init__(self, app_callback):
        self.tag = "start_window"
        self.on_launch = app_callback
        self.width = 300
        self._create_file_dialogs()

    def _create_file_dialogs(self):
        with dpg.file_dialog(
            tag="new_project_dialog",
            directory_selector=True,
            show=False,
            width=700,
            height=400,
            callback=self._on_new_project_selected,
            label="Выберите папку для нового проекта",
        ):
            dpg.add_file_extension(".*", color=(150, 150, 150))

        with dpg.file_dialog(
            tag="open_project_dialog",
            directory_selector=True,
            show=False,
            width=700,
            height=400,
            callback=self._on_open_project_selected,
            label="Выберите папку проекта",
        ):
            dpg.add_file_extension(".catalyst", color=(150, 150, 150))

    def _on_new_project_selected(self, sender, app_data, user_data, *args, **kwargs):
        if app_data and app_data.get("file_path_name"):
            self.on_launch("new", app_data["file_path_name"])

    def _on_open_project_selected(self, sender, app_data, user_data, *args, **kwargs):
        if app_data and app_data.get("file_path_name"):
            self.on_launch("open", app_data["file_path_name"])

    def show(self):
        with dpg.window(
            tag=self.tag,
            no_title_bar=True,
            no_resize=True,
            no_move=True,
            width=800,
            height=800,
        ):
            with dpg.group(tag="launcher_layout"):
                dpg.add_text("CATALYST")
                dpg.add_text("Get started:")
                dpg.add_button(
                    label="New project",
                    width=self.width,
                    callback=lambda: dpg.show_item("new_project_dialog"),
                )
                dpg.add_button(
                    label="Open project",
                    width=self.width,
                    callback=lambda: dpg.show_item("open_project_dialog"),
                )
                dpg.add_spacer(height=10)
                dpg.add_text("Resources:")
                dpg.add_button(
                    label="Github Repository",
                    width=self.width,
                    callback=lambda: webbrowser.open(
                        "https://github.com/groknut/catalyst"
                    ),
                )
                dpg.add_button(
                    label="Custom Node Repository",
                    width=self.width,
                    callback=lambda: webbrowser.open(
                        "https://github.com/groknut/catalyst"
                    ),
                )

        dpg.set_primary_window(self.tag, True)
        self.center_ui()

    def center_ui(self):
        vw, vh = dpg.get_viewport_width(), dpg.get_viewport_height()
        pos_x = (vw // 2) - (self.width // 2)
        pos_y = (vh // 2) - 100
        dpg.set_item_pos("launcher_layout", [pos_x, pos_y])
