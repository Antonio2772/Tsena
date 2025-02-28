from database.connection import create_connection, close_connection
import configparser
from datetime import datetime, date

class FinanceService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.db_path = config['config']['database_path'].strip('"')
    
    def get_box_remaining_balance(self, box_id):
        """Récupère le montant total restant à payer pour un box spécifique"""
        conn = create_connection(self.db_path)
        if not conn:
            return 0
            
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(reste_a_payer) 
                FROM Facture 
                WHERE id_box = ?
            """, (box_id,))
            
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0
            
        except Exception as e:
            print(f"Erreur lors de la récupération du solde restant: {e}")
            return 0
        finally:
            close_connection(conn)
    
    def get_monthly_payment(self, box_id, month, year):
        """Récupère le montant à payer pour un mois et une année donnés pour un box"""
        conn = create_connection(self.db_path)
        if not conn:
            return 0
            
        try:
            cursor = conn.cursor()
            # Convertir le mois en string si c'est un int
            if isinstance(month, int):
                month = str(month)
                
            # Construire les dates de début et de fin du mois
            start_date = f"{year}-{month.zfill(2)}-01"
            
            # Déterminer le dernier jour du mois
            if month == '2':  # Février
                last_day = 29 if (int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0)) else 28
            elif month in ['4', '6', '9', '11']:  # Avril, Juin, Septembre, Novembre
                last_day = 30
            else:
                last_day = 31
                
            end_date = f"{year}-{month.zfill(2)}-{last_day}"
            
            cursor.execute("""
                SELECT SUM(montant_paye + reste_a_payer) 
                FROM Facture 
                WHERE id_box = ? AND date_facturation BETWEEN ? AND ?
            """, (box_id, start_date, end_date))
            
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0
            
        except Exception as e:
            print(f"Erreur lors de la récupération du paiement mensuel: {e}")
            return 0
        finally:
            close_connection(conn)
    
    def get_monthly_payments_for_year(self, box_id, year):
        """Récupère les montants à payer par mois pour un box pour une année spécifique"""
        conn = create_connection(self.db_path)
        if not conn:
            return []
            
        try:
            cursor = conn.cursor()
            monthly_payments = []
            
            for month in range(1, 13):
                # Construire les dates de début et de fin du mois
                start_date = f"{year}-{str(month).zfill(2)}-01"
                
                # Déterminer le dernier jour du mois
                if month == 2:  # Février
                    last_day = 29 if (int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0)) else 28
                elif month in [4, 6, 9, 11]:  # Avril, Juin, Septembre, Novembre
                    last_day = 30
                else:
                    last_day = 31
                    
                end_date = f"{year}-{str(month).zfill(2)}-{last_day}"
                
                cursor.execute("""
                    SELECT SUM(montant_paye + reste_a_payer) as total_montant,
                        SUM(Facture.montant_paye) as montant_paye_sum,
                        SUM(Facture.reste_a_payer) as reste_a_payer_sum 
                    FROM Facture 
                    WHERE id_box = ? AND date_facturation BETWEEN ? AND ?
                """, (box_id, start_date, end_date))

                result = cursor.fetchone()
                total_montant = result[0] if result[0] is not None else 0
                montant_paye = result[1] if result[1] is not None else 0
                reste_a_payer = result[2] if result[2] is not None else 0
                
                monthly_payments.append({
                    'month': month,
                    'month_name': self._get_month_name(month),
                    'total_montant': total_montant,
                    'montant_paye': montant_paye,
                    'reste_a_payer': reste_a_payer
                })
            
            return monthly_payments
            
        except Exception as e:
            print(f"Erreur lors de la récupération des paiements mensuels: {e}")
            return []
        finally:
            close_connection(conn)
    
    def get_all_boxes(self):
        """Récupère tous les boxes pour les selects"""
        conn = create_connection(self.db_path)
        if not conn:
            return []
            
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, libelle 
                FROM Box 
                ORDER BY libelle
            """)
            
            boxes = []
            for row in cursor.fetchall():
                boxes.append({
                    'id': row[0],
                    'libelle': row[1]
                })
            
            return boxes
            
        except Exception as e:
            print(f"Erreur lors de la récupération des boxes: {e}")
            return []
        finally:
            close_connection(conn)
    
    def _get_month_name(self, month_number):
        """Convertit un numéro de mois en nom de mois"""
        month_names = [
            "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
        ]
        return month_names[month_number - 1]
