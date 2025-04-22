from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

from app.menu_bar import create_menu_bar

class MainWindow(QMainWindow):
    """Main window of the application."""
    
    def __init__(self):
        super().__init__()
        self._init_ui()
        
    def _init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Simple PyQt Interface")
        self.setGeometry(100, 100, 800, 600)
        
        # Create and set up central widget
        self._setup_central_widget()
        
        # Create menu bar
        self.setMenuBar(create_menu_bar(self))
        
    def _setup_central_widget(self):
        """Set up the central widget with grey background."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Set grey background
        palette = central_widget.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(200, 200, 200))
        central_widget.setAutoFillBackground(True)
        central_widget.setPalette(palette) 