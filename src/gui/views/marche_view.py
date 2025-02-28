from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QFormLayout, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from models.marche import Marche
from services.marche_service import MarcheService

class MarcheView(QWidget):
    def __init__(self, parent=None):
        super(MarcheView, self).__init__(parent)
        self.marche_service = MarcheService()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("Insertion Marché")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px 0;")
        main_layout.addWidget(title)

        # Formulaire
        form_layout = QFormLayout()
        
        self.libelle_input = QLineEdit()
        self.pos_x_input = QLineEdit()
        self.pos_y_input = QLineEdit()
        self.longueur_input = QLineEdit()
        self.largeur_input = QLineEdit()

        # Validation pour les champs numériques
        for input_field in [self.pos_x_input, self.pos_y_input, 
                          self.longueur_input, self.largeur_input]:
            input_field.setPlaceholderText("Entrer un nombre")
            input_field.setValidator(QtGui.QDoubleValidator())

        form_layout.addRow("Libellé:", self.libelle_input)
        form_layout.addRow("Position X:", self.pos_x_input)
        form_layout.addRow("Position Y:", self.pos_y_input)
        form_layout.addRow("Longueur:", self.longueur_input)
        form_layout.addRow("Largeur:", self.largeur_input)

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

    def submit_form(self):
        try:
            marche = Marche(
                libelle=self.libelle_input.text(),
                pos_x=float(self.pos_x_input.text() or 0),
                pos_y=float(self.pos_y_input.text() or 0),
                longueur=float(self.longueur_input.text() or 0),
                largeur=float(self.largeur_input.text() or 0)
            )

            if self.marche_service.create_marche(marche):
                QMessageBox.information(self, "Succès", "Marché enregistré avec succès!")
                self.clear_form()
            else:
                QMessageBox.critical(self, "Erreur", "Erreur lors de l'enregistrement du marché")
        except ValueError as e:
            QMessageBox.warning(self, "Erreur de validation", "Veuillez vérifier les valeurs numériques")

    def clear_form(self):
        for field in [self.libelle_input, self.pos_x_input, 
                     self.pos_y_input, self.longueur_input, 
                     self.largeur_input]:
            field.clear()
