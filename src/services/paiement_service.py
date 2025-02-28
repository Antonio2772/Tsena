from models.paiement import Paiement
from database.connection import create_connection, close_connection
import configparser
from datetime import datetime

class PaiementService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.db_path = config['config']['database_path'].strip('"')
        
    def process_payment(self, box_id, payment_date, amount):
        conn = create_connection(self.db_path)
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            
            # Récupérer toutes les factures impayées pour ce box, triées par date
            cursor.execute("""
                SELECT id, reste_a_payer 
                FROM Facture 
                WHERE id_box = ? AND reste_a_payer > 0 
                ORDER BY date_facturation ASC
            """, (box_id,))
            
            unpaid_invoices = cursor.fetchall()
            remaining_amount = amount
            
            for invoice_id, remaining_to_pay in unpaid_invoices:
                if remaining_amount <= 0:
                    break
                    
                # Calculer le montant à appliquer sur cette facture
                payment_for_invoice = min(remaining_amount, remaining_to_pay)
                
                # Mettre à jour la facture
                cursor.execute("""
                    UPDATE Facture 
                    SET montant_paye = montant_paye + ?,
                        reste_a_payer = reste_a_payer - ?
                    WHERE id = ?
                """, (payment_for_invoice, payment_for_invoice, invoice_id))
                
                # Créer l'enregistrement de paiement
                cursor.execute("""
                    INSERT INTO Paiement (montant, date_paiement, id_facture)
                    VALUES (?, ?, ?)
                """, (payment_for_invoice, payment_date, invoice_id))
                
                remaining_amount -= payment_for_invoice
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Erreur lors du traitement du paiement: {e}")
            conn.rollback()
            return False
        finally:
            close_connection(conn)
