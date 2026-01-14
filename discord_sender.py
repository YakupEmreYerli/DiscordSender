import sys
import os
import threading
import json
import requests
import keyboard
from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout
from PySide6.QtCore import Qt, Signal, QObject, Slot
from PySide6.QtGui import QFont, QColor, QPalette, QIcon

# --- Helper Function for PyInstaller ---
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Configuration Loading ---
def load_config():
    """Load configuration from config.json"""
    config_path = resource_path("config.json")
    
    # Default configuration
    default_config = {
        "webhook_url": "YOUR_DISCORD_WEBHOOK_URL_HERE",
        "hotkey": "ctrl+k",
        "hotkey_clipboard": "ctrl+alt+k"
    }
    
    # If config doesn't exist, create it with defaults
    if not os.path.exists(config_path):
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2)
        except Exception:
            pass
        return default_config
    
    # Load existing config
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default_config

# Load configuration
config = load_config()
WEBHOOK_URL = config.get("webhook_url", "YOUR_DISCORD_WEBHOOK_URL_HERE")
HOTKEY = config.get("hotkey", "ctrl+k")
HOTKEY_CLIPBOARD = config.get("hotkey_clipboard", "ctrl+alt+k")

# --- Hotkey Signal Communicator ---
class HotkeyCommunicator(QObject):
    show_signal = Signal()
    clipboard_signal = Signal()

# --- Overlay Window ---
class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Window flags: Frameless, Always on Top, Tool (no taskbar icon)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)

        # Input Field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Discord'a mesaj gönder...")
        self.input_field.setFont(QFont("Segoe UI", 12))
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #2C2F33;
                color: #FFFFFF;
                border: 2px solid #7289DA;
                border-radius: 5px;
                padding: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #5865F2;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        layout.addWidget(self.input_field)

        # Center on screen (approximate size)
        self.resize(400, 60)
        self.center_on_screen()

    def center_on_screen(self):
        screen = QApplication.primaryScreen()
        if screen:
            rect = screen.availableGeometry()
            self.move(
                rect.x() + (rect.width() - self.width()) // 2,
                rect.y() + (rect.height() - self.height()) // 2
            )

    def showEvent(self, event):
        """Called when window is shown."""
        self.center_on_screen()
        self.input_field.clear()
        self.input_field.setFocus()
        self.activateWindow()
        super().showEvent(event)

    def keyPressEvent(self, event):
        """Handle ESC key to close."""
        if event.key() == Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)

    def send_message(self):
        text = self.input_field.text().strip()
        if not text:
            self.hide()
            return

        # Send in a separate thread to prevent UI freeze (though requests are fast)
        threading.Thread(target=self._post_to_discord, args=(text,), daemon=True).start()
        
        self.input_field.clear()
        self.hide()

    def _post_to_discord(self, content):
        payload = {"content": content}
        try:
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
        except Exception:
            pass  # Fail silently as requested

    @Slot()
    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.activateWindow()

    @Slot()
    def send_clipboard_content(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        
        if text:
            # Send in background
            threading.Thread(target=self._post_to_discord, args=(text,), daemon=True).start()
            
            # Show a brief tray notification if possible (optional but good for feedback)
            # For now, just silent send is fine as per original minimal spec, 
            # but user might want confirmation. Let's keep it silent/minimal for now.

# --- Main Application ---
def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) # Keep app running when window hides

    # Load Icon
    icon_path = resource_path("app_icon.ico")
    app_icon = QIcon(icon_path)
    app.setWindowIcon(app_icon)

    window = OverlayWindow()
    window.setWindowIcon(app_icon)
    
    # Setup Hotkey Communicator
    communicator = HotkeyCommunicator()
    communicator.show_signal.connect(window.toggle_visibility)
    communicator.clipboard_signal.connect(window.send_clipboard_content)

    # Hotkey Handler (runs in background thread by keyboard lib)
    def on_hotkey():
        try:
            communicator.show_signal.emit()
        except Exception:
            pass

    def on_hotkey_clipboard():
        try:
            communicator.clipboard_signal.emit()
        except Exception:
            pass

    try:
        # suppressed=True consumes the event so it doesn't propagate to other apps
        keyboard.add_hotkey(HOTKEY, on_hotkey, suppress=True)
        keyboard.add_hotkey(HOTKEY_CLIPBOARD, on_hotkey_clipboard, suppress=True)
    except ImportError:
        print("Error: 'keyboard' module not found or permission denied.")
        # Continue running anyway for tray icon access

    # --- System Tray ---
    from PySide6.QtWidgets import QSystemTrayIcon, QMenu

    tray_icon = QSystemTrayIcon(app_icon, app)
    tray_icon.setToolTip("Discord Webhook Sender")
    
    tray_menu = QMenu()
    
    show_action = tray_menu.addAction("Göster")
    show_action.triggered.connect(window.toggle_visibility)
    
    quit_action = tray_menu.addAction("Çıkış")
    quit_action.triggered.connect(app.quit)
    
    tray_icon.setContextMenu(tray_menu)
    tray_icon.show()
    
    # Show a notification on startup
    tray_icon.showMessage(
        "Hazır", 
        f"Açmak için: {HOTKEY.upper()}\nPanoyu Yollamak için: {HOTKEY_CLIPBOARD.upper()}",
        QSystemTrayIcon.Information,
        3000
    )

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
