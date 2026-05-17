# Сравнение двух молекул по Танимото

**Задача:** оценить структурное сходство аспирина и ибупрофена.

**Узлы:** два `SMILESInputNode` → `TanimotoSimilarityNode` → `PrintNode`

**Пошагово:**
1. Добавьте два `SMILESInputNode`. В первый введите `CC(=O)OC1=CC=CC=C1C(=O)O` (аспирин), во второй — `CC(C)CC1=CC=C(C=C1)C(C)C(=O)O` (ибупрофен).
2. Добавьте `TanimotoSimilarityNode`. Подключите выходы `MolData` обоих источников к входам `MolData A` и `MolData B`.
3. К выходу `Tanimoto` подключите `PrintNode`.

**Результат:** `PrintNode` покажет `Tanimoto: 0.19`. Молекулы умеренно схожи.

![Итоговый результат](./output/graph.png)
