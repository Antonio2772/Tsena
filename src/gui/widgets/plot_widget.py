from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
import pyqtgraph as pg
from styles import Styles

class PlotWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, title="Graphique"):
        super(PlotWidget, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Appliquer les styles globaux
        self.setStyleSheet(Styles.get_plot_widget_style())
        
        # Titre du graphique
        self.title_label = QtWidgets.QLabel(title)
        self.title_label.setObjectName("plot-title")
        self.layout.addWidget(self.title_label)
        
        # Container pour le graphique avec un style moderne
        self.plot_container = QtWidgets.QFrame()
        self.plot_container.setObjectName("plot-container")
        container_layout = QtWidgets.QVBoxLayout(self.plot_container)
        container_layout.setContentsMargins(15, 15, 15, 15)
        
        # Ajouter un effet d'ombre au conteneur
        container_shadow = QGraphicsDropShadowEffect()
        container_shadow.setBlurRadius(10)
        container_shadow.setColor(QColor(0, 0, 0, 40))
        container_shadow.setOffset(0, 2)
        self.plot_container.setGraphicsEffect(container_shadow)
        
        # Configuration du graphique avec des styles améliorés
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')  # Fond blanc
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)
        
        # Améliorer l'apparence des axes
        axis_pen = pg.mkPen(color="#5f6368", width=1)  # Couleur texte secondaire pour les axes
        self.plot_widget.getAxis('bottom').setPen(axis_pen)
        self.plot_widget.getAxis('left').setPen(axis_pen)
        
        # Style des labels d'axes
        label_style = {'color': '#202124', 'font-size': '11pt'}  # Couleur texte primaire
        self.plot_widget.getAxis('bottom').setTextPen(label_style)
        self.plot_widget.getAxis('left').setTextPen(label_style)
        
        # Personnalisation des couleurs et styles
        pen = pg.mkPen(color=(26, 115, 232), width=2)  # Couleur primaire professionnelle
        self.plot_line = None
        
        container_layout.addWidget(self.plot_widget)
        self.layout.addWidget(self.plot_container)

    def plot_data(self, x, y, title=None, color=(26, 115, 232), width=2):
        """
        Affiche des données sur le graphique avec des options de personnalisation
        
        Args:
            x: Données pour l'axe X
            y: Données pour l'axe Y
            title: Titre du graphique (optionnel)
            color: Couleur de la ligne (RGB)
            width: Épaisseur de la ligne
        """
        self.plot_widget.clear()
        
        if title:
            self.title_label.setText(title)
            
        pen = pg.mkPen(color=color, width=width)
        
        # Ajouter un effet de dégradé au graphique pour un effet 3D
        brush = pg.mkBrush(color=(*color[:3], 30))  # Version transparente de la couleur
        
        # Créer le graphique avec plus d'options visuelles
        self.plot_line = self.plot_widget.plot(x, y, pen=pen, symbol='o', symbolSize=6, 
                                             symbolBrush=color, symbolPen='w')
        
        # Optionnel : ajouter une aire sous la courbe pour un effet 3D
        fill = pg.FillBetweenItem(
            pg.PlotCurveItem(x, y, pen=pen),
            pg.PlotCurveItem(x, [min(y)] * len(x), pen=None),
            brush=brush
        )
        self.plot_widget.addItem(fill)
                                              
    def add_legend(self, name="Données"):
        """Ajoute une légende au graphique"""
        legend = self.plot_widget.addLegend()
        if self.plot_line:
            legend.addItem(self.plot_line, name)
            
    def set_labels(self, x_label="Axe X", y_label="Axe Y"):
        """Définit les étiquettes des axes"""
        self.plot_widget.setLabel('bottom', x_label)
        self.plot_widget.setLabel('left', y_label)
        
    def set_title(self, title):
        """Définit le titre du graphique"""
        self.title_label.setText(title)
        
    def enable_3d_effect(self, enable=True):
        """
        Active ou désactive l'effet 3D sur le graphique
        
        Args:
            enable: True pour activer, False pour désactiver
        """
        if hasattr(self, 'plot_line') and self.plot_line:
            if enable:
                # Récupérer les données actuelles
                x, y = self.plot_line.getData()
                color = self.plot_line.opts['symbolBrush']
                if isinstance(color, pg.mkBrush):
                    color = color.color().getRgb()[:3]
                elif isinstance(color, tuple):
                    color = color[:3]
                
                # Créer l'effet 3D (ombre sous la courbe)
                brush = pg.mkBrush(color=(*color, 40))
                
                # Ajouter l'effet de remplissage sous la courbe
                self.fill_effect = pg.FillBetweenItem(
                    pg.PlotCurveItem(x, y, pen=self.plot_line.opts['pen']),
                    pg.PlotCurveItem(x, [min(y)] * len(x), pen=None),
                    brush=brush
                )
                self.plot_widget.addItem(self.fill_effect)
                
                # Ajouter un effet d'ombre à la courbe pour renforcer l'effet 3D
                glow = QGraphicsDropShadowEffect()
                glow.setBlurRadius(8)
                glow.setColor(QColor(*color, 80))
                glow.setOffset(1, 1)
                self.plot_line.setGraphicsEffect(glow)
            else:
                # Supprimer l'effet de remplissage
                if hasattr(self, 'fill_effect'):
                    self.plot_widget.removeItem(self.fill_effect)
                    delattr(self, 'fill_effect')
                
                # Supprimer l'effet d'ombre
                self.plot_line.setGraphicsEffect(None)