from models.marche import Marche
from database.connection import create_connection, close_connection
from database.queries import insert_data
import configparser

class MarcheService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.db_path = config['config']['database_path'].strip('"')

    def create_marche(self, marche: Marche):
        conn = create_connection(self.db_path)
        if conn:
            try:
                query = """
                INSERT INTO Marche (libelle, posX, posY, longueur, largeur, prix_m2)
                VALUES (?, ?, ?, ?, ?)
                """
                data = (marche.libelle, marche.pos_x, marche.pos_y, 
                       marche.longueur, marche.largeur, marche.prix_m2)
                insert_data(conn, query, data)
                return True
            except Exception as e:
                print(f"Erreur lors de l'insertion: {e}")
                return False
            finally:
                close_connection(conn)
        return False

    def getAll(self):
        conn = create_connection(self.db_path)
        marches = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, libelle, posX, posY, longueur, largeur, prix_m2 FROM Marche")
                rows = cursor.fetchall()
                for row in rows:
                    marche = Marche(
                        id=row[0],
                        libelle=row[1],
                        pos_x=row[2],
                        pos_y=row[3],
                        longueur=row[4],
                        largeur=row[5],
                        prix_m2=row[6]
                    )
                    marches.append(marche)
                return marches
            except Exception as e:
                print(f"Erreur lors de la récupération des marchés: {e}")
                return []
            finally:
                close_connection(conn)
        return []

    def getById(self, marche_id: int):
        conn = create_connection(self.db_path)
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, libelle, posX, posY, longueur, largeur, prix_m2 FROM Marche WHERE id = ?", (marche_id,))
                row = cursor.fetchone()
                if row:
                    return Marche(
                        id=row[0],
                        libelle=row[1],
                        pos_x=row[2],
                        pos_y=row[3],
                        longueur=row[4],
                        largeur=row[5],
                        prix_m2=row[6]
                    )  
                return None
            except Exception as e:
                print(f"Erreur lors de la récupération du marché: {e}")
                return None
            finally:
                close_connection(conn)
        return None
