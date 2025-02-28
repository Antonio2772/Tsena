from models.facture import Facture
from services.box_service import BoxService
from services.marche_service import MarcheService
from database.connection import create_connection, close_connection
from datetime import datetime, date
import calendar
import configparser

class FactureService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.db_path = config['config']['database_path'].strip('"')
        self.box_service = BoxService()
        self.marche_service = MarcheService()
        
    def calculate_monthly_amount(self, box_id):
        box = self.box_service.getById(box_id)
        if not box:
            return 0
            
        marche = self.marche_service.getById(box.id_marche)
        if not marche:
            return 0
            
        surface = box.longueur * box.largeur
        return surface * marche.prix_m2

    def generate_monthly_invoices(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        # Correction du parsing des dates
        debut_str = config['config']['debut_exercice'].strip('"')
        fin_str = config['config']['fin_exercice'].strip('"')
        
        try:
            debut_exercice = datetime.strptime(debut_str, '%Y-%m-%d').date()
            fin_exercice = datetime.strptime(fin_str, '%Y-%m-%d').date()
        except ValueError as e:
            print(f"Erreur de format de date: {e}")
            return False
            
        conn = create_connection(self.db_path)
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            boxes = self.box_service.getAll()
            
            current_date = debut_exercice
            while current_date <= fin_exercice:
                for box in boxes:
                    # Vérifier si une facture existe déjà pour ce mois et ce box
                    cursor.execute("""
                        SELECT COUNT(*) FROM Facture 
                        WHERE id_box = ? AND MONTH(date_facturation) = ? AND YEAR(date_facturation) = ?
                    """, (box.id, current_date.month, current_date.year))
                    
                    if cursor.fetchone()[0] == 0:
                        montant = self.calculate_monthly_amount(box.id)
                        query = """
                            INSERT INTO Facture (montant_paye, reste_a_payer, date_facturation, id_box)
                            VALUES (?, ?, ?, ?)
                        """
                        cursor.execute(query, (0, montant, current_date, box.id))
                
                # Passer au mois suivant
                if current_date.month == 12:
                    current_date = date(current_date.year + 1, 1, 1)
                else:
                    current_date = date(current_date.year, current_date.month + 1, 1)
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Erreur lors de la génération des factures: {e}")
            conn.rollback()
            return False
        finally:
            close_connection(conn)

    def get_payment_status(self, month, year):
        """Récupère l'état des paiements de tous les boxes pour un mois donné"""
        conn = create_connection(self.db_path)
        if not conn:
            return {}
            
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT f.id_box, 
                       IIF(f.reste_a_payer = 0, 'paid', 'unpaid') as status
                FROM Facture f
                WHERE FORMAT(f.date_facturation, 'mm') = ? 
                AND FORMAT(f.date_facturation, 'yyyy') = ?
            """, (str(month).zfill(2), str(year)))
            
            results = cursor.fetchall()
            return {row[0]: row[1] for row in results}
            
        except Exception as e:
            print(f"Erreur lors de la récupération des états de paiement: {e}")
            return {}
        finally:
            close_connection(conn)

    def get_payment_status_for_box(self, box_id, month=None, year=None):
        """
        Récupère le statut de paiement détaillé pour un box spécifique.
        Peut être filtré par mois et année si fournis.
        """
        conn = create_connection(self.db_path)
        if not conn:
            return {}
            
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    f.id, 
                    f.date_facturation, 
                    f.montant_paye, 
                    f.reste_a_payer,
                    (f.montant_paye + f.reste_a_payer) as montant_total
                FROM Facture f
                WHERE f.id_box = ?
            """
            
            params = [box_id]
            
            # Ajouter des filtres si demandés
            if month and year:
                # Construire les dates de début et de fin du mois
                if isinstance(month, int):
                    month = str(month)
                    
                start_date = f"{year}-{month.zfill(2)}-01"
                
                # Déterminer le dernier jour du mois
                if month == '2':  # Février
                    last_day = 29 if (int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0)) else 28
                elif month in ['4', '6', '9', '11']:  # Avril, Juin, Septembre, Novembre
                    last_day = 30
                else:
                    last_day = 31
                    
                end_date = f"{year}-{month.zfill(2)}-{last_day}"
                
                query += " AND f.date_facturation BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            elif year:
                # Filtrer juste par année
                start_date = f"{year}-01-01"
                end_date = f"{year}-12-31"
                query += " AND f.date_facturation BETWEEN ? AND ?"
                params.extend([start_date, end_date])
                
            query += " ORDER BY f.date_facturation DESC"
            
            cursor.execute(query, params)
            
            result = {}
            for row in cursor.fetchall():
                facture_id = row[0]
                date_facturation = row[1]
                montant_paye = row[2]
                reste_a_payer = row[3]
                montant_total = row[4]
                
                # Convertir la date en objet date si c'est une chaîne
                if isinstance(date_facturation, str):
                    date_facturation = datetime.strptime(date_facturation, "%Y-%m-%d").date()
                
                # Formater la date pour l'affichage
                date_str = date_facturation.strftime("%Y-%m-%d")
                
                result[facture_id] = {
                    'date': date_str,
                    'montant_total': montant_total,
                    'montant_paye': montant_paye,
                    'reste_a_payer': reste_a_payer,
                    'status': 'paid' if reste_a_payer == 0 else 'unpaid'
                }
                
            return result
                
        except Exception as e:
            print(f"Erreur lors de la récupération du statut de paiement: {e}")
            return {}
        finally:
            close_connection(conn)

# Ampiasana ao amin'ny main_window.py (header)
# facture_service = FactureService()
# facture_service.generate_monthly_invoices()