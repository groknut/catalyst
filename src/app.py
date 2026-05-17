import argparse
from pathlib import Path
import dearpygui.dearpygui as dpg
from core.config import Config
from core.project_manager import ProjectManager
from ui.start_window import StartWindow
from ui.main_window import MainWindow
from node_register import load_all_nodes
from core.logger import setup_logging
import sys


class Application:
    def __init__(self, config_path=None, open_file=None, init_dir=None):
        self.config = Config(config_path)
        self.logger = setup_logging(self.config)
        self.logger.info("Catalyst starting...")
        dpg.create_context()
        self._setup_font()
        self.pm = ProjectManager(self.logger)

        if getattr(sys, "frozen", False):
            base_path = Path(__file__).parent
        else:
            base_path = Path(__file__).parent

        self.node_factory, self.groups = load_all_nodes(
            self.config, nodes_folder=base_path / "nodes"
        )
        self.open_file = Path(open_file) if open_file else None
        self.init_dir = Path(init_dir) if init_dir else None
        self.main_window = None
        self.start_window = None



    def _setup_icon(self):
        if getattr(sys, 'frozen', False):
            base = Path(sys.executable).parent
        else:
            base = Path(__file__).resolve().parent

        icon_path = base / "assets" / "icon.ico"

        if icon_path.exists():
            try:
                dpg.set_viewport_small_icon(str(icon_path))
                dpg.set_viewport_large_icon(str(icon_path))
                print(f"Иконка окна загружена: {icon_path}")
            except Exception as e:
                print(f"Не удалось загрузить иконку окна: {e}")
        else:
            print("Иконка окна не найдена (assets/icon.ico)")

    def _setup_font(self):

        if getattr(sys, "frozen", False):
            base_path = Path(sys.executable).parent
        else:
            base_path = Path(__file__).parent

        font_path = base_path / "assets" / "font.ttf"
        self.logger.debug(font_path)
        if font_path.exists():
            with dpg.font_registry():
                with dpg.font(str(font_path), size=18) as font:
                    dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
                dpg.bind_font(font)
            self.logger.debug(f"Загружен встроенный шрифт: {font_path}")
        else:
            self.logger.debug(
                "Встроенный шрифт не найден (assets/font.ttf). Кириллица может не отображаться."
            )

    def run(self):
        dpg.create_viewport(title="Catalyst", width=800, height=600, resizable=False)
        dpg.setup_dearpygui()
        self._setup_icon()

        if self.open_file or self.init_dir:
            self.main_window = MainWindow(
                self.pm, self.node_factory, self.groups, self.config
            )
            if self.open_file:
                if self.open_file.exists():
                    success = self.pm.open_project(self.open_file, self.node_factory)
                    if not success:
                        print(f"❌ Не удалось открыть проект: {self.open_file}")
                else:
                    print(f"❌ Файл проекта не найден: {self.open_file}")
            elif self.init_dir:
                self.pm.new_project(self.init_dir)
            dpg.maximize_viewport()
        else:
            # Обычный запуск: показываем лаунчер
            self.start_window = StartWindow(app_callback=self.on_start_action)
            self.start_window.show()

        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def on_start_action(self, action, path):
        path = Path(path)
        # Сначала убираем лаунчер и создаём редактор
        if dpg.does_item_exist("start_window"):
            dpg.delete_item("start_window")
        self.main_window = MainWindow(
            self.pm, self.node_factory, self.groups, self.config
        )

        if action == "new":
            self.pm.new_project(path)
        elif action == "open":
            if not self.pm.open_project(path, self.node_factory):
                print("⚠️ Could not open project")

        dpg.maximize_viewport()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Catalyst Node Editor")
    parser.add_argument("-c", "--config", help="Path to YAML config file")
    parser.add_argument("-o", "--open", help="Open project from .catalyst file")
    parser.add_argument("--init", help="Create new project in the specified folder")
    parser.add_argument(
        "-l",
        "--list-nodes",
        action="store_true",
        help="Print available node types and exit",
    )
    args = parser.parse_args()

    if args.list_nodes:
        config = Config(args.config)
        if getattr(sys, "frozen", False):
            base_path = Path(__file__).parent
        else:
            base_path = Path(__file__).parent
        factory, groups = load_all_nodes(config, nodes_folder=base_path / "nodes")
        print("=== Available Nodes ===\n")
        for grp, names in groups.items():
            print(f"--- {grp} ---")
            for name in sorted(names):
                print(f"  • {name}")
            print()
        sys.exit(0)

    if args.open and args.init:
        print(
            "Warning: both --open and --init specified, opening file, ignoring --init."
        )
        init_dir = None
    else:
        init_dir = args.init

    app = Application(config_path=args.config, open_file=args.open, init_dir=init_dir)
    app.run()
