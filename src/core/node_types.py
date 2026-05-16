class NodeTypes:
    ANY = "Any"
    STRING = "String"
    FLOAT = "Float"
    INT = "Integer"
    BOOL = "Bool"
    MOL = "RDKit_Mol"
    SMILES = "SMILES"

TYPE_COLORS = {
    NodeTypes.ANY: (150,150,150),
    NodeTypes.STRING: (200,150,0),
    NodeTypes.FLOAT: (180,180,0),
    NodeTypes.INT: (120,180,180),
    NodeTypes.BOOL: (200,100,100),
    NodeTypes.MOL: (0,180,0),
    NodeTypes.SMILES: (180,0,180)
}
