from PyQt6.QtWidgets import QMenuBar, QMenu

def create_menu_bar(parent):
    """Create and return the application's menu bar.
    
    Args:
        parent: The parent widget for the menu bar.
        
    Returns:
        QMenuBar: The configured menu bar.
    """
    menubar = QMenuBar(parent)
    
    # File menu
    file_menu = menubar.addMenu("File")
    file_menu.addAction("New")
    file_menu.addAction("Open")
    file_menu.addAction("Save")
    file_menu.addSeparator()
    file_menu.addAction("Exit")
    
    # Edit menu
    edit_menu = menubar.addMenu("Edit")
    edit_menu.addAction("Cut")
    edit_menu.addAction("Copy")
    edit_menu.addAction("Paste")
    
    # Help menu
    help_menu = menubar.addMenu("Help")
    help_menu.addAction("About")
    
    return menubar 