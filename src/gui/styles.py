# styles.py

class Styles:
    # Couleurs professionnelles
    PRIMARY_COLOR = "#1a73e8"     # Bleu Google/entreprise - plus professionnel que le bleu vif initial
    PRIMARY_DARK = "#0d47a1"      # Bleu foncé pour les effets
    SECONDARY_COLOR = "#34A853"   # Vert business/croissance
    SECONDARY_DARK = "#2E7D32"    # Vert foncé pour les effets
    BACKGROUND_COLOR = "#f8f9fa"  # Gris très clair, plus doux que le blanc pur
    SIDEBAR_COLOR = "#263238"     # Bleu-gris foncé pour le sidebar (Material design)
    SIDEBAR_DARK = "#1c2529"      # Version plus foncée pour les effets
    TEXT_COLOR = "#202124"        # Gris très foncé, meilleur pour la lisibilité que le noir
    TEXT_LIGHT = "#f1f3f4"        # Blanc cassé pour texte sur fond foncé
    TEXT_SECONDARY = "#5f6368"    # Gris moyen pour texte secondaire
    BORDER_COLOR = "#dadce0"      # Gris clair pour les bordures
    ACCENT_COLOR = "#fbbc04"      # Jaune/Ambre pour accentuation (alertes, notifications)
    DANGER_COLOR = "#ea4335"      # Rouge pour les actions critiques/dangereuses
    
    @classmethod
    def get_main_style(cls):
        return f"""
            /* Global styles */
            QMainWindow, QDialog {{
                background-color: {cls.BACKGROUND_COLOR};
                color: {cls.TEXT_COLOR};
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }}
            
            QWidget {{
                font-size: 14px;
            }}
            
            /* Header */
            QFrame#header {{
                background-color: white;
                border-bottom: 1px solid {cls.BORDER_COLOR};
                /* Shadow effect */
                border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            }}
            
            QFrame#header::after {{
                content: "";
                position: absolute;
                left: 0;
                right: 0;
                bottom: -10px;
                height: 10px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 0.1), stop:1 rgba(0, 0, 0, 0));
            }}
            
            QLabel#header-title {{
                font-size: 20px;
                font-weight: bold;
                color: {cls.PRIMARY_COLOR};
            }}
            
            /* Sidebar */
            QFrame#sidebar {{
                background-color: {cls.SIDEBAR_COLOR};
                color: {cls.TEXT_LIGHT};
                border-right: none;
                /* Right shadow effect */
                border-right: 5px solid rgba(0, 0, 0, 0.1);
            }}
            
            QLabel#sidebar-header {{
                color: {cls.TEXT_LIGHT};
                font-size: 12px;
                font-weight: bold;
                padding: 5px 0;
                opacity: 0.7;
            }}
            
            QPushButton#menu-button {{
                text-align: left;
                padding: 12px 15px;
                border: none;
                border-radius: 6px;
                color: {cls.TEXT_LIGHT};
                background-color: transparent;
                font-size: 14px;
                /* 3D effect for buttons */
                margin: 2px 0;
            }}
            
            QPushButton#menu-button:hover {{
                background-color: rgba(255, 255, 255, 0.1);
                /* Subtle 3D effect on hover */
                border-bottom: 2px solid rgba(0, 0, 0, 0.2);
            }}
            
            QPushButton#menu-button:checked {{
                background-color: {cls.PRIMARY_COLOR};
                color: white;
                font-weight: bold;
                /* 3D pressed effect */
                border-bottom: 2px solid rgba(0, 0, 0, 0.3);
                transform: translateY(1px);
            }}
            
            /* Body */
            QFrame#body {{
                background-color: {cls.BACKGROUND_COLOR};
                border-radius: 0px;
                /* Add a subtle shadow to the entire body */
                border: none;
            }}
            
            QLabel#page-title {{
                font-size: 22px;
                font-weight: bold;
                color: {cls.TEXT_COLOR};
                margin-bottom: 10px;
            }}
            
            QFrame#content-container {{
                background-color: white;
                border-radius: 8px;
                border: 1px solid {cls.BORDER_COLOR};
                /* 3D shadow effect */
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin: 10px;
                padding: 15px;
            }}
            
            /* Action buttons */
            QPushButton#action-button {{
                background-color: {cls.PRIMARY_COLOR};
                color: white;
                padding: 10px 18px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                /* 3D effect */
                border-bottom: 2px solid {cls.PRIMARY_DARK};
            }}
            
            QPushButton#action-button:hover {{
                background-color: {cls.PRIMARY_DARK};
                /* Slight lift effect on hover */
                margin-top: -1px;
                margin-bottom: 1px;
            }}
            
            QPushButton#action-button:pressed {{
                background-color: {cls.PRIMARY_DARK};
                border-bottom: 1px solid {cls.PRIMARY_DARK};
                margin-top: 2px;
                margin-bottom: -2px;
            }}
            
            /* User section */
            QFrame#user-section {{
                background-color: {cls.SIDEBAR_DARK};
                border-radius: 6px;
                padding: 10px;
                /* 3D effect */
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-bottom: 2px solid rgba(0, 0, 0, 0.2);
            }}
            
            QLabel#username-label {{
                color: white;
                font-weight: bold;
                font-size: 14px;
            }}
            
            QLabel#user-role-label {{
                color: {cls.TEXT_LIGHT};
                font-size: 12px;
                opacity: 0.8;
            }}
            
            /* Footer */
            QFrame#footer {{
                background-color: white;
                border-top: 1px solid {cls.BORDER_COLOR};
                color: {cls.TEXT_SECONDARY};
            }}
            
            QLabel#footer-text, QLabel#version-text {{
                color: {cls.TEXT_SECONDARY};
                font-size: 12px;
            }}
            
            /* Form elements */
            QLineEdit, QComboBox, QDateEdit, QSpinBox, QTextEdit {{
                border: 1px solid {cls.BORDER_COLOR};
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                selection-background-color: {cls.PRIMARY_COLOR};
            }}
            
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QSpinBox:focus, QTextEdit:focus {{
                border: 1px solid {cls.PRIMARY_COLOR};
                /* 3D focus effect */
                box-shadow: 0 0 3px rgba(26, 115, 232, 0.4);
            }}
            
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            
            QDateEdit::drop-down {{
                border: none;
                width: 20px;
            }}
            
            /* Messages boxes */
            QMessageBox {{
                background-color: white;
                border-radius: 8px;
            }}
            
            QMessageBox QPushButton {{
                background-color: {cls.PRIMARY_COLOR};
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                /* 3D effect */
                border-bottom: 2px solid {cls.PRIMARY_DARK};
                min-width: 80px;
            }}
            
            QMessageBox QPushButton:hover {{
                background-color: {cls.PRIMARY_DARK};
            }}
            
            /* Tables */
            QTableWidget {{
                border: 1px solid {cls.BORDER_COLOR};
                border-radius: 4px;
                background-color: white;
                /* 3D effect */
                box-shadow: inset 1px 1px 3px rgba(0, 0, 0, 0.05);
            }}
            
            QTableWidget::item {{
                padding: 5px;
                border-bottom: 1px solid rgba(0, 0, 0, 0.05);
            }}
            
            QTableWidget::item:selected {{
                background-color: {cls.PRIMARY_COLOR};
                color: white;
            }}
            
            QHeaderView::section {{
                background-color: {cls.BACKGROUND_COLOR};
                padding: 6px;
                border: none;
                border-right: 1px solid {cls.BORDER_COLOR};
                border-bottom: 1px solid {cls.BORDER_COLOR};
                font-weight: bold;
            }}
            
            /* ScrollBar modern style */
            QScrollBar:vertical {{
                border: none;
                background: {cls.BACKGROUND_COLOR};
                width: 8px;
                border-radius: 4px;
            }}
            
            QScrollBar::handle:vertical {{
                background: #c2c7cb;
                border-radius: 4px;
                min-height: 20px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background: #a8adb1;
            }}
            
            QScrollBar:horizontal {{
                border: none;
                background: {cls.BACKGROUND_COLOR};
                height: 8px;
                border-radius: 4px;
            }}
            
            QScrollBar::handle:horizontal {{
                background: #c2c7cb;
                border-radius: 4px;
                min-width: 20px;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background: #a8adb1;
            }}
            
            /* Group boxes */
            QGroupBox {{
                font-weight: bold;
                border: 1px solid {cls.BORDER_COLOR};
                border-radius: 6px;
                margin-top: 15px;
                padding-top: 20px;
                /* 3D effect */
                background-color: white;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                background-color: white;
                color: {cls.PRIMARY_COLOR};
                border-radius: 3px;
            }}
        """
    
    @classmethod
    def get_form_button_style(cls):
        return f"""
            QPushButton {{
                background-color: {cls.SECONDARY_COLOR};
                color: white;
                padding: 10px 18px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                /* 3D effect */
                border-bottom: 2px solid {cls.SECONDARY_DARK};
            }}
            
            QPushButton:hover {{
                background-color: {cls.SECONDARY_DARK};
                /* Slight lift effect on hover */
                margin-top: -1px;
                margin-bottom: 1px;
            }}
            
            QPushButton:pressed {{
                background-color: {cls.SECONDARY_DARK};
                border-bottom: 1px solid {cls.SECONDARY_DARK};
                margin-top: 2px;
                margin-bottom: -2px;
            }}
        """
    
    @classmethod
    def get_plot_widget_style(cls):
        return f"""
            QLabel#plot-title {{
                font-size: 16px;
                font-weight: bold;
                color: {cls.TEXT_COLOR};
                margin-bottom: 6px;
            }}
            
            QFrame#plot-container {{
                background-color: white;
                border-radius: 6px;
                border: 1px solid {cls.BORDER_COLOR};
                /* 3D shadow effect */
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
                padding: 12px;
            }}
        """