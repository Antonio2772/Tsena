class Marche:
    def __init__(self, id=None, libelle="", pos_x=0, pos_y=0, longueur=0, largeur=0, prix_m2=0):
        self.id = id
        self.libelle = libelle
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.longueur = longueur
        self.largeur = largeur
        self.prix_m2 = prix_m2

    def to_dict(self):
        return {
            'id': self.id,
            'libelle': self.libelle,
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'longueur': self.longueur,
            'largeur': self.largeur,
            'prix_m2': self.prix_m2
        }

    @staticmethod
    def from_dict(data):
        return Marche(
            id=data.get('id'),
            libelle=data.get('libelle', ''),
            pos_x=data.get('pos_x', 0),
            pos_y=data.get('pos_y', 0),
            longueur=data.get('longueur', 0),
            largeur=data.get('largeur', 0),
            prix_m2=data.get('prix_m2', 0)
        )
