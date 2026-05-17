class NodeTypes:
    ANY = "Any"
    STRING = "String"
    FLOAT = "Float"
    INT = "Integer"
    BOOL = "Bool"
    MOL = "RDKit_Mol"
    SMILES = "SMILES"


TYPE_COLORS = {
    NodeTypes.ANY: (150, 150, 150),
    NodeTypes.STRING: (200, 150, 0),
    NodeTypes.FLOAT: (180, 180, 0),
    NodeTypes.INT: (120, 180, 180),
    NodeTypes.BOOL: (200, 100, 100),
    NodeTypes.MOL: (0, 180, 0),
    NodeTypes.SMILES: (180, 0, 180),
}

GROUP_THEME = {
            "Data I/O":       (100, 180, 255),
            "RDKit":          (80, 200, 120),
            "Properties":     (140, 160, 255),
            "Filters":        (255, 160, 60),
            "Logic":          (200, 140, 255),
            "Flow":           (255, 200, 80),
            "Input":          (80, 220, 210),
            "Output":         (255, 120, 140),
            "Math":           (170, 170, 190),
            "Similarity":     (220, 170, 110),
            "Cheminformatics":(100, 210, 160),
            "Notes":          (255, 140, 140),
            "Constants":      (180, 180, 200),
            "Text":           (170, 150, 220),
        }
