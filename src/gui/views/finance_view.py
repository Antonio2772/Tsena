from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QGroupBox, QFormLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QFrame, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from services.finance_service import FinanceService
import calendar
from datetime import datetime

class FinanceView(QWidget):
    def __init__(self, parent=None):
        super(FinanceView, self).__init__(parent)
        self.finance_service = FinanceService()
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
                background-color: #ecf0f1;
            }
            QTableWidget {
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Titre
        title_label = QLabel("Statistiques Financières des Boxes")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Filtres communs
        filter_frame = QFrame()
        filter_layout = QHBoxLayout(filter_frame)
        
        # Sélection du box
        box_label = QLabel("Box:")
        self.box_combo = QComboBox()
        self.load_boxes()
        
        # Sélection de l'année
        year_label = QLabel("Année:")
        self.year_combo = QComboBox()
        current_year = datetime.now().year
        for year in range(current_year - 5, current_year + 2):
            self.year_combo.addItem(str(year), year)
        self.year_combo.setCurrentText(str(current_year))
        
        # Sélection du mois
        month_label = QLabel("Mois:")
        self.month_combo = QComboBox()
        for i in range(1, 13):
            month_name = calendar.month_name[i]
            self.month_combo.addItem(month_name, i)
        self.month_combo.setCurrentIndex(datetime.now().month - 1)
        
        # Bouton pour actualiser
        self.refresh_btn = QPushButton("Actualiser")
        self.refresh_btn.clicked.connect(self.update_all)
        
        # Ajouter les widgets au layout des filtres
        filter_layout.addWidget(box_label)
        filter_layout.addWidget(self.box_combo)
        filter_layout.addWidget(year_label)
        filter_layout.addWidget(self.year_combo)
        filter_layout.addWidget(month_label)
        filter_layout.addWidget(self.month_combo)
        filter_layout.addWidget(self.refresh_btn)
        filter_layout.addStretch()
        
        main_layout.addWidget(filter_frame)
        
        # Layout pour les 3 sections
        content_layout = QHBoxLayout()
        
        # 1. Section pour le reste à payer
        remaining_group = QGroupBox("Reste à Payer")
        remaining_layout = QVBoxLayout(remaining_group)
        
        self.remaining_label = QLabel("Chargement...")
        remaining_font = QFont()
        remaining_font.setPointSize(14)
        remaining_font.setBold(True)
        self.remaining_label.setFont(remaining_font)
        self.remaining_label.setAlignment(Qt.AlignCenter)
        
        remaining_layout.addWidget(self.remaining_label)
        content_layout.addWidget(remaining_group)
        
        # 2. Section pour le montant à payer pour le mois/année
        monthly_group = QGroupBox("Montant à Payer (Mois Sélectionné)")
        monthly_layout = QVBoxLayout(monthly_group)
        
        self.monthly_label = QLabel("Chargement...")
        monthly_font = QFont()
        monthly_font.setPointSize(14)
        monthly_font.setBold(True)
        self.monthly_label.setFont(monthly_font)
        self.monthly_label.setAlignment(Qt.AlignCenter)
        
        monthly_layout.addWidget(self.monthly_label)
        content_layout.addWidget(monthly_group)
        
        # Ajouter les sections au layout principal
        main_layout.addLayout(content_layout)
        
        # 3. Section pour la table des paiements mensuels
        monthly_payments_group = QGroupBox("Paiements Mensuels (Année Sélectionnée)")
        monthly_payments_layout = QVBoxLayout(monthly_payments_group)
        
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(4)
        self.payments_table.setHorizontalHeaderLabels(["Mois", "Montant Total", "Montant Payé", "Reste à Payer"])
        header = self.payments_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        
        monthly_payments_layout.addWidget(self.payments_table)
        main_layout.addWidget(monthly_payments_group)
        
        # Connecter les signaux
        self.box_combo.currentIndexChanged.connect(self.update_all)
        self.year_combo.currentIndexChanged.connect(self.update_all)
        self.month_combo.currentIndexChanged.connect(self.update_monthly_payment)
        
        # Configuration du layout
        main_layout.setContentsMargins(20, 20, 20, 20)
        
    def load_boxes(self):
        """Charge la liste des boxes dans le combobox"""
        self.box_combo.clear()
        boxes = self.finance_service.get_all_boxes()
        
        for box in boxes:
            self.box_combo.addItem(box['libelle'], box['id'])
    
    def update_all(self):
        """Met à jour toutes les sections de la vue"""
        self.update_remaining_balance()
        self.update_monthly_payment()
        self.update_monthly_payments_table()
    
    def update_remaining_balance(self):
        """Met à jour l'affichage du reste à payer"""
        if self.box_combo.count() == 0:
            return
            
        box_id = self.box_combo.currentData()
        if not box_id:
            return
            
        remaining = self.finance_service.get_box_remaining_balance(box_id)
        self.remaining_label.setText(f"{remaining:.2f} €")
        
        # Changer la couleur selon le montant
        if remaining > 0:
            self.remaining_label.setStyleSheet("color: red;")
        else:
            self.remaining_label.setStyleSheet("color: green;")
    
    def update_monthly_payment(self):
        """Met à jour l'affichage du montant à payer pour le mois et l'année sélectionnés"""
        if self.box_combo.count() == 0:
            return
            
        box_id = self.box_combo.currentData()
        month = self.month_combo.currentData()
        year = self.year_combo.currentText()
        
        if not box_id or not month or not year:
            return
            
        monthly_payment = self.finance_service.get_monthly_payment(box_id, month, year)
        self.monthly_label.setText(f"{monthly_payment:.2f} €")
    
    def update_monthly_payments_table(self):
        """Met à jour la table des paiements mensuels"""
        if self.box_combo.count() == 0:
            return
            
        box_id = self.box_combo.currentData()
        year = self.year_combo.currentText()
        
        if not box_id or not year:
            return
            
        monthly_payments = self.finance_service.get_monthly_payments_for_year(box_id, year)
        
        self.payments_table.setRowCount(len(monthly_payments))
        
        for row, payment in enumerate(monthly_payments):
            # Mois
            self.payments_table.setItem(row, 0, QTableWidgetItem(payment['month_name']))
            
            # Montant total
            total_item = QTableWidgetItem(f"{payment['total_montant']:.2f} €")
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.payments_table.setItem(row, 1, total_item)
            
            # Montant payé
            paid_item = QTableWidgetItem(f"{payment['montant_paye']:.2f} €")
            paid_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.payments_table.setItem(row, 2, paid_item)
            
            # Reste à payer
            remaining_item = QTableWidgetItem(f"{payment['reste_a_payer']:.2f} €")
            remaining_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            # Colorer en rouge si reste à payer > 0, en vert sinon
            if payment['reste_a_payer'] > 0:
                remaining_item.setForeground(Qt.red)
            else:
                remaining_item.setForeground(Qt.darkGreen)
            self.payments_table.setItem(row, 3, remaining_item)
    
    def showEvent(self, event):
        """Appelé lorsque la vue devient visible"""
        super().showEvent(event)
        self.update_all()