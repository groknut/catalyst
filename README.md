# Catalyst IDE

Визуальный редактор графов для хемоинформатики.  
Создавайте вычислительные пайплайны без программирования — просто перетаскивайте узлы и соединяйте их.

[![GitHub release](https://img.shields.io/github/v/release/groknut/catalyst?style=flat-square)](https://github.com/groknut/catalyst/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)

---

## Возможности

- **Загрузка молекул** из SMILES, SDF-файлов.
- **11 встроенных дескрипторов**: MW, LogP, TPSA, QED, HBA/HBD, формула и другие.
- **Фильтры** по массе, LogP, числу атомов и правилу Липински.
- **Сравнение молекул** — коэффициент Танимото, MCS.
- **Структурные преобразования** — удаление солей, канонизация SMILES, 3D‑координаты, InChI.
- **Экспорт** результатов в CSV, SDF, PNG.
- **Горячие клавиши** для быстрой работы.
- **Кастомные узлы** — загружаются из папки без переустановки.
- **Офлайн‑режим** — не требует интернета.

---

## Готовые сборки

Скачайте последнюю версию для Windows (`.exe`, ~50 МБ) на странице [Releases](https://github.com/groknut/catalyst/releases).

---

## Быстрый старт (из исходников)

```bash
git clone https://github.com/groknut/catalyst
cd catalyst
uv sync
uv run src/app.py
```

---

## Запуск с аргументами
```bash
# Открыть существующий проект
uv run src/app.py -o my_project/project.catalyst

# Создать новый проект
uv run src/app.py --init new_project

# Посмотреть список доступных узлов
uv run src/app.py --list-nodes
```

---

## Лицензия
MIT © 2026 Groknut
