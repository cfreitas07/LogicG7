from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt, QSize

class LEDIndicator(QWidget):
    """A widget that displays a colored LED indicator."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(12, 12)  # Small circular LED
        self._is_on = False
        self._color = QColor(255, 0, 0)  # Default red
        
    def set_state(self, is_on: bool):
        """Set the LED state.
        
        Args:
            is_on: True for green (on), False for red (off)
        """
        self._is_on = is_on
        self._color = QColor(0, 255, 0) if is_on else QColor(255, 0, 0)
        self.update()
        
    def paintEvent(self, event):
        """Paint the LED indicator."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw LED circle
        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        painter.setBrush(self._color)
        painter.drawEllipse(0, 0, self.width() - 1, self.height() - 1)
        
        # Add highlight effect
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(255, 255, 255, 100))
        painter.drawEllipse(2, 2, 4, 4) 