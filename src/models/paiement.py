from datetime import datetime

class Paiement:
    def __init__(self, id=None, montant=0, date_paiement=None, id_facture=None):
        self.id = id
        self.montant = montant
        self.date_paiement = date_paiement or datetime.now().date()
        self.id_facture = id_facture

    def to_dict(self):
        return {
            'id': self.id,
            'montant': self.montant,
            'date_paiement': self.date_paiement,
            'id_facture': self.id_facture
        }
