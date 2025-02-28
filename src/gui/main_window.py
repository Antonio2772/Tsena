from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QFrame, QStackedWidget, QMessageBox,
                           QSizePolicy, QGraphicsDropShadowEffect)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor
from .views.marche_view import MarcheView
from .views.box_view import BoxView
from .views.paiement_view import PaiementView
from .views.etat_view import EtatView
from .views.finance_view import FinanceView
from services.facture_service import FactureService
from .styles import Styles

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Tsena")
        self.setMinimumSize(1200, 600)
        
        # Application des styles globaux
        self.setStyleSheet(Styles.get_main_style())
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header avec ombre
        self.header = QFrame()
        self.header.setObjectName("header")
        self.header.setFixedHeight(70)
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        # Ajouter un effet d'ombre au header
        header_shadow = QGraphicsDropShadowEffect()
        header_shadow.setBlurRadius(15)
        header_shadow.setColor(QColor(0, 0, 0, 50))
        header_shadow.setOffset(0, 2)
        self.header.setGraphicsEffect(header_shadow)
        
        # Logo et titre
        logo_title_container = QWidget()
        logo_title_layout = QHBoxLayout(logo_title_container)
        logo_title_layout.setContentsMargins(0, 0, 0, 0)
        
        # Vous pouvez remplacer ceci par un vrai logo
        logo_label = QLabel()
        # logo_label.setPixmap(QIcon("path/to/logo.png").pixmap(QSize(36, 36)))
        logo_title_layout.addWidget(logo_label)
        
        header_title = QLabel("Tsena")
        header_title.setObjectName("header-title")
        logo_title_layout.addWidget(header_title)
        
        header_layout.addWidget(logo_title_container)
        
        # Actions container
        actions_container = QWidget()
        actions_layout = QHBoxLayout(actions_container)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(15)
        
        # Ajouter le bouton Générer facture avec icône
        # self.generate_invoice_btn = QPushButton(" Générer factures")
        # self.generate_invoice_btn.setObjectName("action-button")
        # # self.generate_invoice_btn.setIcon(QIcon("path/to/invoice-icon.png"))
        # self.generate_invoice_btn.setIconSize(QSize(16, 16))
        # self.generate_invoice_btn.clicked.connect(self.generate_invoices)
        # actions_layout.addWidget(self.generate_invoice_btn)
        
        header_layout.addWidget(actions_container, alignment=Qt.AlignRight)
        main_layout.addWidget(self.header)

        # Content area (sidebar + body)
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Sidebar moderne avec effet 3D
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)
        
        # Ajouter un effet d'ombre au sidebar
        sidebar_shadow = QGraphicsDropShadowEffect()
        sidebar_shadow.setBlurRadius(10)
        sidebar_shadow.setColor(QColor(0, 0, 0, 80))
        sidebar_shadow.setOffset(3, 0)
        self.sidebar.setGraphicsEffect(sidebar_shadow)
        
        # Label de navigation
        nav_label = QLabel("NAVIGATION")
        nav_label.setObjectName("sidebar-header")
        sidebar_layout.addWidget(nav_label)
        sidebar_layout.addSpacing(10)
        
        # Menu items avec icônes
        menu_items = [
            {"name": "Marché", "icon": "market-icon.png"},
            {"name": "Box", "icon": "box-icon.png"},
            {"name": "Paiement", "icon": "payment-icon.png"},
            {"name": "Etat", "icon": "status-icon.png"},
            {"name": "Finances", "icon": "finance-icon.png"}
        ]
        
        self.menu_buttons = []
        
        for index, item in enumerate(menu_items):
            btn = QPushButton(item["name"])
            btn.setObjectName("menu-button")
            # btn.setIcon(QIcon(f"icons/{item['icon']}"))
            btn.setIconSize(QSize(20, 20))
            btn.setCheckable(True)
            if index == 0:
                btn.setChecked(True)
            
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setFixedHeight(45)
            sidebar_layout.addWidget(btn)
            self.menu_buttons.append(btn)
            
        sidebar_layout.addStretch()
        
        # User info section avec effet 3D
        user_section = QFrame()
        user_section.setObjectName("user-section")
        user_layout = QHBoxLayout(user_section)
        
        # Ajouter un effet d'ombre au profil utilisateur
        user_shadow = QGraphicsDropShadowEffect()
        user_shadow.setBlurRadius(8)
        user_shadow.setColor(QColor(0, 0, 0, 70))
        user_shadow.setOffset(0, 2)
        user_section.setGraphicsEffect(user_shadow)
        
        # user_avatar = QLabel()
        # user_avatar.setPixmap(QIcon("icons/user-avatar.png").pixmap(QSize(32, 32)))
        # user_layout.addWidget(user_avatar)
        
        user_info = QWidget()
        user_info_layout = QVBoxLayout(user_info)
        user_info_layout.setContentsMargins(0, 0, 0, 0)
        user_info_layout.setSpacing(2)
        
        username = QLabel("Admin")
        username.setObjectName("username-label")
        user_role = QLabel("Administrateur")
        user_role.setObjectName("user-role-label")
        
        user_info_layout.addWidget(username)
        user_info_layout.addWidget(user_role)
        user_layout.addWidget(user_info)
        
        sidebar_layout.addWidget(user_section)
        content_layout.addWidget(self.sidebar)

        # Body avec bordures arrondies et ombres
        self.body = QFrame()
        self.body.setObjectName("body")
        body_layout = QVBoxLayout(self.body)
        body_layout.setContentsMargins(20, 20, 20, 20)
        
        # En-tête de la page
        page_header = QWidget()
        page_header_layout = QHBoxLayout(page_header)
        page_header_layout.setContentsMargins(0, 0, 0, 15)
        
        self.page_title = QLabel("Insertion Marché")
        self.page_title.setObjectName("page-title")
        page_header_layout.addWidget(self.page_title)
        
        body_layout.addWidget(page_header)
        
        # Conteneur principal pour le contenu des vues avec effet 3D
        content_container = QFrame()
        content_container.setObjectName("content-container")
        content_container_layout = QVBoxLayout(content_container)
        
        # Ajouter un effet d'ombre au conteneur
        container_shadow = QGraphicsDropShadowEffect()
        container_shadow.setBlurRadius(20)
        container_shadow.setColor(QColor(0, 0, 0, 40))
        container_shadow.setOffset(0, 4)
        content_container.setGraphicsEffect(container_shadow)
        
        # Stacked Widget pour le contenu
        self.stacked_widget = QStackedWidget()
        content_container_layout.addWidget(self.stacked_widget)
        
        # Ajouter les pages
        self.marche_view = MarcheView()
        self.box_view = BoxView()
        self.paiement_view = PaiementView()
        self.etat_view = EtatView()
        self.finance_view = FinanceView()
        
        self.stacked_widget.addWidget(self.marche_view)
        self.stacked_widget.addWidget(self.box_view)
        self.stacked_widget.addWidget(self.paiement_view)
        self.stacked_widget.addWidget(self.etat_view)
        self.stacked_widget.addWidget(self.finance_view)
        
        body_layout.addWidget(content_container)
        content_layout.addWidget(self.body)
        main_layout.addWidget(content)

        # Footer moderne avec effet subtil
        self.footer = QFrame()
        self.footer.setObjectName("footer")
        self.footer.setFixedHeight(40)
        footer_layout = QHBoxLayout(self.footer)
        footer_layout.setContentsMargins(20, 0, 20, 0)
        
        # Ajouter une ombre au-dessus du footer
        footer_shadow = QGraphicsDropShadowEffect()
        footer_shadow.setBlurRadius(10)
        footer_shadow.setColor(QColor(0, 0, 0, 30))
        footer_shadow.setOffset(0, -2)
        self.footer.setGraphicsEffect(footer_shadow)
        
        footer_text = QLabel("© 2025 Tsena - Tous droits réservés")
        footer_text.setObjectName("footer-text")
        footer_layout.addWidget(footer_text)
        
        version_text = QLabel("v1.0")
        version_text.setObjectName("version-text")
        footer_layout.addWidget(version_text, alignment=Qt.AlignRight)
        
        main_layout.addWidget(self.footer)

        # Connect signals
        for i, btn in enumerate(self.menu_buttons):
            btn.clicked.connect(lambda checked, index=i: self.change_page(index))
    
    def change_page(self, index):
        # Mettre à jour les boutons
        for i, btn in enumerate(self.menu_buttons):
            btn.setChecked(i == index)
        
        # Mettre à jour le titre de la page
        page_titles = ["Insertion Marché", "Insertion Box", "Paiement", "Etat", "Finances"]
        self.page_title.setText(page_titles[index])
        
        # Changer la page
        self.stacked_widget.setCurrentIndex(index)

    def generate_invoices(self):
        try:
            facture_service = FactureService()
            success = facture_service.generate_monthly_invoices()
            
            if success:
                QMessageBox.information(self, "Succès", "Les factures ont été générées avec succès!")
            else:
                QMessageBox.warning(self, "Attention", "Une erreur est survenue lors de la génération des factures.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur inattendue est survenue: {str(e)}")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())