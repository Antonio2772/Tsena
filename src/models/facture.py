from datetime import datetime

class Facture:
    def __init__(self, id=None, montant_paye=0, reste_a_payer=0, date_facturation=None, id_box=None):
        self.id = id
        self.montant_paye = montant_paye
        self.reste_a_payer = reste_a_payer
        self.date_facturation = date_facturation or datetime.now().date()
        self.id_box = id_box

    def to_dict(self):
        return {
            'id': self.id,
            'montant_paye': self.montant_paye,
            'reste_a_payer': self.reste_a_payer,
            'date_facturation': self.date_facturation,
            'id_box': self.id_box
        }
