from unittest.mock import patch, MagicMock
import pytest
from core.base_node import BaseNode
from core.node_types import NodeTypes


@pytest.fixture
def mock_dpg():
    """Создаёт изолированный мок для DearPyGui."""
    with patch("core.base_node.dpg") as mock:
        # Возвращаем уникальные pin_id через side_effect
        pin_counter = 0

        def node_attribute(*args, **kwargs):
            # Создаём контекстный менеджер с уникальным pin_id
            nonlocal pin_counter
            pin_counter += 1
            cm = MagicMock()
            cm.__enter__.return_value = pin_counter
            cm.__exit__.return_value = None
            return cm

        mock.node_attribute = node_attribute
        mock.add_text = MagicMock()
        mock.node = MagicMock(
            return_value=MagicMock(
                __enter__=MagicMock(return_value=1), __exit__=MagicMock()
            )
        )
        mock.get_item_label = MagicMock(return_value="TestNode")
        mock.get_item_pos = MagicMock(return_value=(10, 20))
        mock.mvNode_Attr_Input = "input"
        mock.mvNode_Attr_Output = "output"
        yield mock


@pytest.fixture
def mock_manager():
    return MagicMock()


@pytest.fixture
def test_node(mock_dpg, mock_manager):
    """Создаёт конкретный тестовый узел с одним входом и одним выходом."""

    class TestNode(BaseNode):
        def build_node(self):
            self.in_a = self.add_input_attribute("A", NodeTypes.FLOAT)
            self.out_b = self.add_output_attribute("B", NodeTypes.INT)

    node = TestNode(mock_manager, "TestNode", pos=(0, 0), parent="editor")
    return node


# ----------------------------------------------------------------
#  Tests
# ----------------------------------------------------------------
def test_node_creation_and_registration(mock_dpg, mock_manager):
    """Узел создаётся и регистрируется в менеджере."""

    class SimpleNode(BaseNode):
        pass

    node = SimpleNode(mock_manager, "Simple")
    assert node.id is not None
    mock_manager.register_node.assert_called_once_with(node)


def test_add_input_attribute(test_node):
    """Входной атрибут добавляется в inputs и pin_types с правильным типом."""
    assert len(test_node.inputs) == 1
    pin_id = test_node.inputs[0]
    assert pin_id is not None
    assert test_node.pin_types[pin_id] == NodeTypes.FLOAT


def test_add_output_attribute(test_node):
    """Выходной атрибут добавляется в outputs и pin_types с правильным типом."""
    assert len(test_node.outputs) == 1
    pin_id = test_node.outputs[0]
    assert pin_id is not None
    assert test_node.pin_types[pin_id] == NodeTypes.INT


def test_serialization_structure(test_node):
    """Сериализация содержит все обязательные ключи."""
    data = test_node.serialize()
    assert data["type"] == "TestNode"
    assert data["label"] == "TestNode"
    assert data["pos"] == (10, 20)  # mock get_item_pos
    assert "inputs" in data
    assert "outputs" in data
    assert "params" in data
    assert data["inputs"] == test_node.inputs
    assert data["outputs"] == test_node.outputs


def test_serialization_preserves_pin_ids(test_node):
    """ID пинов в сериализации совпадают с реальными списками."""
    data = test_node.serialize()
    assert data["inputs"] == test_node.inputs
    assert data["outputs"] == test_node.outputs


def test_get_params_default(test_node):
    assert test_node.get_params() == {}


def test_set_params_no_error(test_node):
    test_node.set_params({"any": "value"})


def test_update_no_error(test_node):
    test_node.update()


def test_get_output_value_default(test_node):
    assert test_node.get_output_value(None) is None
