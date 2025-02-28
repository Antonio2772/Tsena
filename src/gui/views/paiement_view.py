from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QFormLayout, QComboBox,
                           QDateEdit, QMessageBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5 import QtGui
from services.box_service import BoxService
from services.paiement_service import PaiementService

class PaiementView(QWidget):
    def __init__(self, parent=None):
        super(PaiementView, self).__init__(parent)
        self.box_service = BoxService()
        self.paiement_service = PaiementService()
        self.boxes = []  # Pour stocker les références aux boxes
        self.setup_ui()
        self.load_boxes()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("Paiement de Loyer")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px 0;")
        main_layout.addWidget(title)

        # Formulaire
        form_layout = QFormLayout()
        
        # Box (liste déroulante)
        self.box_combo = QComboBox()
        self.box_combo.setPlaceholderText("Sélectionner un box")
        
        # Date
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        
        # Montant
        self.montant_input = QLineEdit()
        self.montant_input.setPlaceholderText("Entrer le montant")
        self.montant_input.setValidator(QtGui.QDoubleValidator())

        form_layout.addRow("Box:", self.box_combo)
        form_layout.addRow("Date:", self.date_edit)
        form_layout.addRow("Montant:", self.montant_input)

        main_layout.addLayout(form_layout)

        # Bouton de soumission
        button_layout = QHBoxLayout()
        submit_btn = QPushButton("Enregistrer")
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        submit_btn.clicked.connect(self.submit_form)
        
        button_layout.addStretch()
        button_layout.addWidget(submit_btn)
        main_layout.addLayout(button_layout)
        
        main_layout.addStretch()

    def load_boxes(self):
        self.boxes = self.box_service.getAllWithMarche()
        self.box_combo.clear()
        for box in self.boxes:
            # Afficher le box avec son marché
            display_text = f"{box.libelle} - Marché: {box.marche_libelle}"
            self.box_combo.addItem(display_text, box.id)  # Stocke l'ID du box comme données

    def submit_form(self):
        try:
            box_id = self.box_combo.currentData()
            if not box_id:
                QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un box.")
                return

            montant_text = self.montant_input.text()
            if not montant_text:
                QMessageBox.warning(self, "Erreur", "Veuillez entrer un montant.")
                return

            montant = float(montant_text)
            if montant <= 0:
                QMessageBox.warning(self, "Erreur", "Le montant doit être supérieur à 0.")
                return

            date_paiement = self.date_edit.date().toString('yyyy-MM-dd')
            
            success = self.paiement_service.process_payment(box_id, date_paiement, montant)
            
            if success:
                QMessageBox.information(self, "Succès", "Le paiement a été enregistré avec succès.")
                # Réinitialiser le formulaire
                self.montant_input.clear()
                self.date_edit.setDate(QDate.currentDate())
            else:
                QMessageBox.warning(self, "Erreur", "Une erreur est survenue lors de l'enregistrement du paiement.")
                
        except ValueError as e:
            QMessageBox.warning(self, "Erreur", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur inattendue est survenue: {str(e)}")
