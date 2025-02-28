class Box:
    def __init__(self, id=None, libelle="", pos_x=0, pos_y=0, longueur=0, largeur=0, id_marche=None):
        self.id = id
        self.libelle = libelle
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.longueur = longueur
        self.largeur = largeur
        self.id_marche = id_marche

    def to_dict(self):
        return {
            'id': self.id,
            'libelle': self.libelle,
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'longueur': self.longueur,
            'largeur': self.largeur,
            'id_marche': self.id_marche
        }

    @staticmethod
    def from_dict(data):
        return Box(
            id=data.get('id'),
            libelle=data.get('libelle', ''),
            pos_x=data.get('pos_x', 0),
            pos_y=data.get('pos_y', 0),
            longueur=data.get('longueur', 0),
            largeur=data.get('largeur', 0),
            id_marche=data.get('id_marche')
        )
