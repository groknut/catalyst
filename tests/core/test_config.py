# tests/test_config.py
import pytest
from pathlib import Path
import yaml
from core.config import Config


# ----------------------------------------------------------------
#  Fixtures
# ----------------------------------------------------------------
@pytest.fixture
def temp_config_file(tmp_path):
    """Создаёт временный путь к config.yaml и возвращает его."""
    cfg_file = tmp_path / "config.yaml"
    return cfg_file


# ----------------------------------------------------------------
#  Tests
# ----------------------------------------------------------------


def test_default_config_with_explicit_path(temp_config_file):
    """Без файла – значения по умолчанию."""
    cfg = Config(path=temp_config_file)  # используем временный путь
    assert cfg.data["log_level"] == "INFO"
    assert cfg.data["log_file"] == str(Path.home() / ".catalyst" / "catalyst.log")
    # custom_nodes_dir по умолчанию – системный путь, но проверяем, что он заканчивается нужным фрагментом
    assert cfg.data["custom_nodes_dir"].endswith(
        str(Path(".catalyst") / "custom_nodes")
    )


def test_load_existing_config(temp_config_file):
    """Загружаем корректный YAML – значения обновляются."""
    temp_config_file.parent.mkdir(parents=True, exist_ok=True)
    temp_config_file.write_text(
        "custom_nodes_dir: /my/custom/nodes\n"
        "log_level: DEBUG\n"
        "log_file: /var/log/catalyst.log\n",
        encoding="utf-8",
    )
    cfg = Config(path=temp_config_file)
    assert cfg.data["custom_nodes_dir"] == "/my/custom/nodes"
    assert cfg.data["log_level"] == "DEBUG"
    assert cfg.data["log_file"] == "/var/log/catalyst.log"


def test_save_and_reload(temp_config_file):
    """Сохраняем изменения и загружаем заново."""
    cfg = Config(path=temp_config_file)
    cfg.data["log_level"] = "WARNING"
    cfg.save()
    assert temp_config_file.exists()
    # загружаем свежий экземпляр
    cfg2 = Config(path=temp_config_file)
    assert cfg2.data["log_level"] == "WARNING"


def test_missing_file_uses_defaults(temp_config_file):
    """Если файл не существует, ошибок нет, данные дефолтные."""
    assert not temp_config_file.exists()
    cfg = Config(path=temp_config_file)
    assert cfg.data["log_level"] == "INFO"


def test_corrupted_file_does_not_crash(temp_config_file, capsys):
    """Повреждённый YAML не ломает загрузку, пишет ошибку."""
    temp_config_file.parent.mkdir(parents=True, exist_ok=True)
    temp_config_file.write_text("{{{ bad yaml", encoding="utf-8")
    cfg = Config(path=temp_config_file)
    captured = capsys.readouterr()
    assert "Config load error" in captured.out or "Config load error" in captured.err
    assert cfg.data["log_level"] == "INFO"


def test_save_creates_parent_directories(temp_config_file):
    """Проверяем, что при сохранении создаются недостающие папки."""
    # Убедимся, что родительской папки нет
    if temp_config_file.parent.exists():
        import shutil

        shutil.rmtree(temp_config_file.parent)
    assert not temp_config_file.parent.exists()
    cfg = Config(path=temp_config_file)
    cfg.save()
    assert temp_config_file.parent.exists()
    assert temp_config_file.exists()


def test_explicit_path(tmp_path):
    """Можно передать свой путь к конфигу."""
    custom_path = tmp_path / "my_config.yaml"
    cfg = Config(path=custom_path)
    assert cfg.filepath == custom_path
    cfg.data["log_level"] = "ERROR"
    cfg.save()
    assert custom_path.exists()
    loaded = yaml.safe_load(custom_path.read_text(encoding="utf-8"))
    assert loaded["log_level"] == "ERROR"
