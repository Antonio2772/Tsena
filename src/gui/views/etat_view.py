from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt, QRectF
from services.marche_service import MarcheService
from services.box_service import BoxService
from services.facture_service import FactureService
import calendar
from datetime import datetime

class EtatView(QWidget):
    def __init__(self, parent=None):
        super(EtatView, self).__init__(parent)
        self.marche_service = MarcheService()
        self.box_service = BoxService()
        self.facture_service = FactureService()
        self.marches = []
        self.boxs = []
        self.scale_factor = 50
        self.offset_x = 50
        self.offset_y = 50
        self.zoom_level = 1.0
        self.payment_status = {}
        
        # Création des layouts
        self.main_layout = QVBoxLayout(self)
        self.button_layout = QHBoxLayout()
        
        # Création des boutons
        self.zoom_in_btn = QPushButton("+", self)
        self.zoom_out_btn = QPushButton("-", self)
        self.reset_btn = QPushButton("Reset", self)
        
        # Ajout des boutons au layout
        self.button_layout.addWidget(self.zoom_in_btn)
        self.button_layout.addWidget(self.zoom_out_btn)
        self.button_layout.addWidget(self.reset_btn)
        self.button_layout.addStretch()
        
        # Configuration du layout principal
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addStretch()
        
        # Connexion des signaux
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        self.reset_btn.clicked.connect(self.reset_zoom)
        
        self.setup_filters()

    def setup_filters(self):
        filter_layout = QHBoxLayout()
        
        # Mois
        self.month_combo = QComboBox()
        months = [(str(i), calendar.month_name[i]) for i in range(1, 13)]
        for value, name in months:
            self.month_combo.addItem(name, value)
        self.month_combo.setCurrentIndex(datetime.now().month - 1)
        
        # Année
        self.year_combo = QComboBox()
        current_year = datetime.now().year
        years = range(current_year - 5, current_year + 1)
        for year in years:
            self.year_combo.addItem(str(year), year)
        self.year_combo.setCurrentText(str(current_year))
        
        filter_layout.addWidget(QLabel("Mois:"))
        filter_layout.addWidget(self.month_combo)
        filter_layout.addWidget(QLabel("Année:"))
        filter_layout.addWidget(self.year_combo)
        filter_layout.addStretch()
        
        # Connecter les signaux
        self.month_combo.currentIndexChanged.connect(self.update_payment_status)
        self.year_combo.currentIndexChanged.connect(self.update_payment_status)
        
        # Ajouter le layout des filtres avant le layout des boutons
        self.main_layout.insertLayout(0, filter_layout)

    def update_payment_status(self):
        month = self.month_combo.currentData()
        year = self.year_combo.currentText()
        self.payment_status = self.facture_service.get_payment_status(month, year)
        self.update()
    
    def zoom_in(self):
        self.zoom_level *= 1.2
        self.update()
    
    def zoom_out(self):
        self.zoom_level /= 1.2
        self.update()
    
    def reset_zoom(self):
        self.zoom_level = 1.0
        self.calculate_optimal_scale()
        self.update()
    
    def calculate_optimal_scale(self):
        if not self.marches and not self.boxs:
            return
        
        # Calculer les limites des marchés et des boxs
        all_items = self.marches + self.boxs
        min_x = min(item.pos_x for item in all_items)
        max_x = max(item.pos_x + item.longueur for item in all_items)
        min_y = min(item.pos_y for item in all_items)
        max_y = max(item.pos_y + item.largeur for item in all_items)
        
        # Calculer l'échelle optimale
        width_scale = (self.width() - 2 * self.offset_x) / (max_x - min_x) if max_x != min_x else 1
        height_scale = (self.height() - 2 * self.offset_y) / (max_y - min_y) if max_y != min_y else 1
        
        self.scale_factor = min(width_scale, height_scale) * 0.8  # 80% de l'échelle maximale

    def paintEvent(self, event):
        self.marches = self.marche_service.getAll()
        self.boxs = self.box_service.getAll()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Appliquer le zoom
        effective_scale = self.scale_factor * self.zoom_level
        
        # Dessiner les axes
        painter.setPen(QPen(Qt.black, 1))
        painter.drawLine(0, self.height() - self.offset_y, 
                        self.width(), self.height() - self.offset_y)
        painter.drawLine(self.offset_x, 0, 
                        self.offset_x, self.height())
        
        # Dessiner les marchés
        for marche in self.marches:
            x = self.offset_x + (marche.pos_x * effective_scale)
            y = self.height() - self.offset_y - (marche.pos_y * effective_scale)
            width = marche.longueur * effective_scale
            height = marche.largeur * effective_scale
            
            painter.setPen(QPen(Qt.blue, 2))
            painter.setBrush(QBrush(QColor(173, 216, 230, 100)))
            painter.drawRect(int(x), int(y - height), int(width), int(height))
            
            painter.setPen(Qt.black)
            painter.drawText(QRectF(x, y - height, width, height), 
                           Qt.AlignCenter, marche.libelle)

        # Dessiner les boxs
        for box in self.boxs:
            x = self.offset_x + (box.pos_x * effective_scale)
            y = self.height() - self.offset_y - (box.pos_y * effective_scale)
            width = box.longueur * effective_scale
            height = box.largeur * effective_scale
            
            # Définir la couleur en fonction du statut de paiement
            status = self.payment_status.get(box.id, 'unknown')
            if status == 'paid':
                color = QColor(144, 238, 144, 100)  # Vert clair
                border_color = Qt.green
            elif status == 'unpaid':
                color = QColor(255, 182, 193, 100)  # Rouge clair
                border_color = Qt.red
            else:
                color = QColor(200, 200, 200, 100)  # Gris
                border_color = Qt.gray
            
            painter.setPen(QPen(border_color, 2))
            painter.setBrush(QBrush(color))
            painter.drawRect(int(x), int(y - height), int(width), int(height))
            
            painter.setPen(Qt.black)
            painter.drawText(QRectF(x, y - height, width, height), 
                           Qt.AlignCenter, box.libelle)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.calculate_optimal_scale()
        self.update()

    def showEvent(self, event):
        super().showEvent(event)
        self.update_payment_status()
