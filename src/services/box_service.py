from models.box import Box
from database.connection import create_connection, close_connection
from database.queries import insert_data
import configparser

class BoxService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.db_path = config['config']['database_path'].strip('"')

    def create_box(self, box: Box):
        conn = create_connection(self.db_path)
        if conn:
            try:
                query = """
                INSERT INTO Box (libelle, posX, posY, longueur, largeur, id_marche)
                VALUES (?, ?, ?, ?, ?, ?)
                """
                data = (box.libelle, box.pos_x, box.pos_y, 
                       box.longueur, box.largeur, box.id_marche)
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
        boxs = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, libelle, posX, posY, longueur, largeur, id_marche FROM Box")
                rows = cursor.fetchall()
                for row in rows:
                    box = Box(
                        id=row[0],
                        libelle=row[1],
                        pos_x=row[2],
                        pos_y=row[3],
                        longueur=row[4],
                        largeur=row[5],
                        id_marche=row[6]
                    )
                    boxs.append(box)
                return boxs
            except Exception as e:
                print(f"Erreur lors de la récupération des boxs: {e}")
                return []
            finally:
                close_connection(conn)
        return []
    
    def getById(self, box_id: int):
        conn = create_connection(self.db_path)
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, libelle, posX, posY, longueur, largeur, id_marche FROM Box WHERE id = ?", (box_id,))
                row = cursor.fetchone()
                if row:
                    return Box(
                        id=row[0],
                        libelle=row[1],
                        pos_x=row[2],
                        pos_y=row[3],
                        longueur=row[4],
                        largeur=row[5],
                        id_marche=row[6]
                    )
                return None
            except Exception as e:
                print(f"Erreur lors de la récupération du box: {e}")
                return None
            finally:
                close_connection(conn)
        return None

    def getAllWithMarche(self):
        conn = create_connection(self.db_path)
        boxs = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT b.id, b.libelle, b.posX, b.posY, b.longueur, b.largeur, 
                           b.id_marche, m.libelle as marche_libelle 
                    FROM Box b 
                    LEFT JOIN Marche m ON b.id_marche = m.id
                """)
                rows = cursor.fetchall()
                for row in rows:
                    box = Box(
                        id=row[0],
                        libelle=row[1],
                        pos_x=row[2],
                        pos_y=row[3],
                        longueur=row[4],
                        largeur=row[5],
                        id_marche=row[6]
                    )
                    box.marche_libelle = row[7]  # Ajout du libellé du marché
                    boxs.append(box)
                return boxs
            except Exception as e:
                print(f"Erreur lors de la récupération des boxs: {e}")
                return []
            finally:
                close_connection(conn)
        return []