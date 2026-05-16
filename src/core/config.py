from pathlib import Path
import yaml

DEFAULT_PATH = Path.home() / ".catalyst"
DEFAULT_CONFIG_PATH = DEFAULT_PATH / "config.yaml"
DEFAULT_CUSTOM_NODES_PATH = DEFAULT_PATH / "custom_nodes"
DEFAULT_LOGGER_MODE = "INFO"
DEFAULT_LOG_FILE = DEFAULT_PATH / "catalyst.log"

class Config:
    def __init__(self, path=None):
        self.filepath = Path(path) if path else DEFAULT_CONFIG_PATH
        self.custom_nodes_path = DEFAULT_CUSTOM_NODES_PATH
        self.custom_nodes_path.mkdir(exist_ok=True)
        self.data = self._defaults()
        self._load()

    def _defaults(self):
        return {
            "custom_nodes_dir": str(DEFAULT_CUSTOM_NODES_PATH),   # теперь self существует
            "log_level": DEFAULT_LOGGER_MODE,
            "log_file": str(DEFAULT_LOG_FILE)
        }

    def _load(self):
        if self.filepath.exists():
            try:
                self.data.update(yaml.safe_load(self.filepath.read_text(encoding="utf-8")))
            except Exception as e:
                print(f"Config load error: {e}")

    def save(self):
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self.filepath.write_text(
            yaml.dump(self.data, allow_unicode=True, default_flow_style=False),
            encoding="utf-8"
        )

    @property
    def custom_nodes_dir(self) -> str:
        return self.data.get("custom_nodes_dir", "")
