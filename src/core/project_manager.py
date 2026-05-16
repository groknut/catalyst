import json
from pathlib import Path
from core.node_manager import NodeManager

class ProjectManager:
    def __init__(self, logger=None):
        self.node_manager = NodeManager(logger)
        self.current_file: Path | None = None
        self.logger = logger

    def new_project(self, folder_path: Path | str):
        folder = Path(folder_path)
        folder.mkdir(parents=True, exist_ok=True)
        self.current_file = folder / "project.catalyst"
        file = folder / "README.md"
        file.write_text('\n# By Catalyst')

        (folder / "input").mkdir(exist_ok=True)
        (folder / "output").mkdir(exist_ok=True)

        self.node_manager = NodeManager()
        self.node_manager.project_dir = folder
        self.save_project()

        return True

    def open_project(self, file_path: Path | str, node_factory):

        path = Path(file_path)
        if not path.exists():
            return False

        data = json.loads(path.read_text(encoding="utf-8"))
        self.node_manager = NodeManager(self.logger)
        self.node_manager.load_from_data(data, node_factory)
        self.current_file = path
        project_dir = path.parent
        self.node_manager.project_dir = project_dir

        (project_dir / "input").mkdir(exist_ok=True)
        (project_dir / "output").mkdir(exist_ok=True)

        self.missed_types = getattr(self.node_manager, '_missed_types_in_last_load', [])

        if self.missed_types:
            self.logger.warning(f"Missing node types in project: {self.missed_types}")

        return True

    def save_project(self):
        if not self.current_file:
            self.logger.warning("❌ Cannot save: current_file is None")
            return
        self.current_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "nodes": [node.serialize() for node in self.node_manager.nodes.values()],
            "links": list(self.node_manager.links.items())
        }
        self.logger.info(f"💾 Saving {len(self.node_manager.nodes)} nodes to {self.current_file}")
        self.current_file.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
