import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QPushButton, QFileDialog,
                             QLabel, QSlider, QListWidget, QListWidgetItem,
                             QMessageBox, QInputDialog, QLineEdit, QDialog,
                             QDialogButtonBox, QTabWidget, QGroupBox, QComboBox)
from PyQt5.QtCore import Qt, QUrl, QTimer, pyqtSignal, QObject
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QBrush, QPen, QColor, QKeySequence

try:
    import keyboard
    GLOBAL_HOTKEY_AVAILABLE = True
except ImportError:
    GLOBAL_HOTKEY_AVAILABLE = False

class LanguageManager:
    def __init__(self):
        self.current_lang = "ru"
        self.strings = {
            "ru": {
                "add_sound": "Добавить звук",
                "remove_sound": "Удалить звук",
                "stop_all": "Остановить всё",
                "clear_all": "Очистить всё",
                "show_hotkeys": "Горячие клавиши",
                "volume": "Громкость",
                "rename": "Переименовать",
                "replace_sound": "Заменить звук",
                "assign_hotkey": "Назначить глобальную горячую клавишу",
                "remove_hotkey": "Удалить глобальную клавишу",
                "close": "Закрыть",
                "ready": "Готов к работе",
                "playing": "Воспроизводится",
                "stopped": "Все звуки остановлены",
                "added": "Добавлен звук",
                "removed": "Удален звук",
                "renamed": "Переименован",
                "replaced": "Звук заменен",
                "hotkey_assigned": "Горячая клавиша назначена",
                "hotkey_removed": "Горячая клавиша удалена",
                "no_sounds": "Нет звуков для удаления",
                "clear_confirm": "Вы уверены, что хотите удалить все звуки?",
                "select_sound": "Выберите звук для удаления:",
                "enter_name": "Введите название для кнопки:",
                "enter_new_name": "Введите новое название:",
                "want_hotkey": "Хотите назначить глобальную горячую клавишу?",
                "hotkey_conflict": "Горячая клавиша уже используется. Заменить?",
                "error_file_not_found": "Файл не найден",
                "hotkey_error": "Ошибка: клавиша не может быть использована",
                "global_hotkeys": "Глобальные горячие клавиши",
                "hotkey_works": "Горячие клавиши работают даже когда приложение не активно",
                "no_hotkeys": "Нет назначенных глобальных горячих клавиш",
                "language": "Язык",
                "settings": "Настройки",
                "theme": "Тема",
                "black": "Черная",
                "white": "Белая",
                "green": "Зеленая",
                "blue": "Синяя",
                "pink": "Розовая",
                "save_settings": "Сохранить настройки",
                "cancel": "Отмена"
            },
            "en": {
                "add_sound": "Add Sound",
                "remove_sound": "Remove Sound",
                "stop_all": "Stop All",
                "clear_all": "Clear All",
                "show_hotkeys": "Hotkeys",
                "volume": "Volume",
                "rename": "Rename",
                "replace_sound": "Replace Sound",
                "assign_hotkey": "Assign global hotkey",
                "remove_hotkey": "Remove global hotkey",
                "close": "Close",
                "ready": "Ready to work",
                "playing": "Playing",
                "stopped": "All sounds stopped",
                "added": "Sound added",
                "removed": "Sound removed",
                "renamed": "Renamed",
                "replaced": "Sound replaced",
                "hotkey_assigned": "Hotkey assigned",
                "hotkey_removed": "Hotkey removed",
                "no_sounds": "No sounds to remove",
                "clear_confirm": "Are you sure you want to delete all sounds?",
                "select_sound": "Select sound to remove:",
                "enter_name": "Enter button name:",
                "enter_new_name": "Enter new name:",
                "want_hotkey": "Do you want to assign a global hotkey?",
                "hotkey_conflict": "Hotkey already in use. Replace?",
                "error_file_not_found": "File not found",
                "hotkey_error": "Error: hotkey cannot be used",
                "global_hotkeys": "Global Hotkeys",
                "hotkey_works": "Hotkeys work even when the app is not active",
                "no_hotkeys": "No global hotkeys assigned",
                "language": "Language",
                "settings": "Settings",
                "theme": "Theme",
                "black": "Black",
                "white": "White",
                "green": "Green",
                "blue": "Blue",
                "pink": "Pink",
                "save_settings": "Save Settings",
                "cancel": "Cancel"
            }
        }
    
    def tr(self, key):
        return self.strings[self.current_lang].get(key, key)
    
    def set_language(self, lang):
        if lang in self.strings:
            self.current_lang = lang
            return True
        return False

lang = LanguageManager()

class ThemeManager:
    themes = {
        "black": {
            "bg": "#1e1e1e",
            "fg": "#ffffff",
            "button_bg": "#2d2d2d",
            "button_hover": "#3d3d3d",
            "border": "#3d3d3d",
            "accent": "#007acc",
            "status_bg": "#252526",
            "scroll_bg": "#2d2d2d",
            "info_bg": "#2d2d2d"
        },
        "white": {
            "bg": "#f5f5f5",
            "fg": "#000000",
            "button_bg": "#e0e0e0",
            "button_hover": "#d0d0d0",
            "border": "#cccccc",
            "accent": "#2196f3",
            "status_bg": "#e8e8e8",
            "scroll_bg": "#f0f0f0",
            "info_bg": "#e8e8e8"
        },
        "green": {
            "bg": "#1b5e20",
            "fg": "#ffffff",
            "button_bg": "#2e7d32",
            "button_hover": "#388e3c",
            "border": "#4caf50",
            "accent": "#81c784",
            "status_bg": "#1b5e20",
            "scroll_bg": "#2e7d32",
            "info_bg": "#2e7d32"
        },
        "blue": {
            "bg": "#0d47a1",
            "fg": "#ffffff",
            "button_bg": "#1565c0",
            "button_hover": "#1976d2",
            "border": "#42a5f5",
            "accent": "#90caf9",
            "status_bg": "#0d47a1",
            "scroll_bg": "#1565c0",
            "info_bg": "#1565c0"
        },
        "pink": {
            "bg": "#880e4f",
            "fg": "#ffffff",
            "button_bg": "#ad1457",
            "button_hover": "#c2185b",
            "border": "#e91e63",
            "accent": "#f48fb1",
            "status_bg": "#880e4f",
            "scroll_bg": "#ad1457",
            "info_bg": "#ad1457"
        }
    }
    
    current_theme = "white"
    
    @classmethod
    def get_style(cls):
        theme = cls.themes[cls.current_theme]
        return f"""
            QMainWindow {{ background-color: {theme["bg"]}; }}
            QWidget {{ background-color: {theme["bg"]}; color: {theme["fg"]}; }}
            QPushButton {{
                background-color: {theme["button_bg"]};
                color: {theme["fg"]};
                border: 1px solid {theme["border"]};
                border-radius: 8px;
                padding: 8px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {theme["button_hover"]}; }}
            QLabel {{ color: {theme["fg"]}; }}
            QSlider::groove:horizontal {{
                height: 6px;
                background: {theme["border"]};
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                width: 15px;
                background: {theme["accent"]};
                border-radius: 7px;
            }}
            QSlider::handle:horizontal:hover {{ background: {theme["button_hover"]}; }}
            QScrollArea {{ border: none; background-color: {theme["bg"]}; }}
            QScrollBar:vertical {{
                border: none;
                background: {theme["scroll_bg"]};
                width: 10px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: {theme["accent"]};
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{ background: {theme["button_hover"]}; }}
            QListWidget {{
                background-color: {theme["button_bg"]};
                color: {theme["fg"]};
                border: 1px solid {theme["border"]};
                border-radius: 5px;
            }}
            QListWidget::item:hover {{ background-color: {theme["button_hover"]}; }}
            QListWidget::item:selected {{ background-color: {theme["accent"]}; }}
            QLineEdit, QComboBox {{
                background-color: {theme["button_bg"]};
                color: {theme["fg"]};
                border: 1px solid {theme["border"]};
                border-radius: 5px;
                padding: 5px;
            }}
            QDialog {{
                background-color: {theme["bg"]};
                color: {theme["fg"]};
            }}
            QGroupBox {{
                border: 1px solid {theme["border"]};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
        """
    
    @classmethod
    def get_info_style(cls):
        theme = cls.themes[cls.current_theme]
        return f"""
            background-color: {theme["info_bg"]};
            color: {theme["fg"]};
            border: 1px solid {theme["border"]};
            border-radius: 5px;
            padding: 10px;
        """
    
    @classmethod
    def set_theme(cls, theme_name):
        if theme_name in cls.themes:
            cls.current_theme = theme_name
            return True
        return False

class IconManager:
    @staticmethod
    def create_icon(color, size=32):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(color)))
        painter.setPen(QPen(Qt.white, 2))
        painter.drawEllipse(2, 2, size-4, size-4)
        painter.end()
        return QIcon(pixmap)

class SoundPadButton(QPushButton):
    def __init__(self, text, sound_path=None, hotkey=None, parent=None):
        super().__init__(text, parent)
        self.sound_path = sound_path
        self.hotkey = hotkey
        self.is_playing = False
        self.animation_timer = None
        self.animation_frame = 0
        self.setMinimumSize(140, 120)
        self.setFont(QFont("Arial", 11, QFont.Bold))
        self.update_icon()
        self.setIconSize(self.size() * 0.4)
        self.update_style()
    
    def update_icon(self):
        if self.is_playing:
            icon = IconManager.create_icon("#e74c3c", 48)
        elif self.hotkey:
            icon = IconManager.create_icon("#8e44ad", 48)
        else:
            icon = IconManager.create_icon(ThemeManager.themes[ThemeManager.current_theme]["accent"], 48)
        self.setIcon(icon)
    
    def start_playing_animation(self):
        self.is_playing = True
        self.animation_frame = 0
        if self.animation_timer is None:
            self.animation_timer = QTimer()
            self.animation_timer.timeout.connect(self.animate)
            self.animation_timer.start(300)
        self.update_icon()
        self.update_style()
    
    def stop_playing_animation(self):
        self.is_playing = False
        if self.animation_timer:
            self.animation_timer.stop()
            self.animation_timer = None
        self.update_icon()
        self.update_style()
    
    def animate(self):
        if self.is_playing:
            self.animation_frame += 1
            self.update_icon()
    
    def update_style(self):
        theme = ThemeManager.themes[ThemeManager.current_theme]
        if self.is_playing:
            self.setToolTip(f"{lang.tr('playing')}... {self.hotkey if self.hotkey else ''}")
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: #ffebee;
                    color: #c62828;
                    border: 2px solid #e74c3c;
                    border-radius: 12px;
                    padding: 15px;
                    font-weight: bold;
                }}
                QPushButton:hover {{ background-color: #ffcdd2; }}
            """)
        elif self.hotkey:
            self.setToolTip(f"{lang.tr('assign_hotkey')}: {self.hotkey}")
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme["button_bg"]};
                    color: {theme["fg"]};
                    border: 2px solid #9b59b6;
                    border-radius: 12px;
                    padding: 15px;
                    font-weight: bold;
                }}
                QPushButton:hover {{ background-color: {theme["button_hover"]}; }}
            """)
        else:
            self.setToolTip(lang.tr("assign_hotkey"))
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme["button_bg"]};
                    color: {theme["fg"]};
                    border: 2px solid {theme["accent"]};
                    border-radius: 12px;
                    padding: 15px;
                    font-weight: bold;
                }}
                QPushButton:hover {{ background-color: {theme["button_hover"]}; }}
            """)
    
    def set_hotkey(self, hotkey):
        self.hotkey = hotkey
        self.update_icon()
        self.update_style()

class HotkeyDialog(QDialog):
    def __init__(self, current_key=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(lang.tr("assign_hotkey"))
        self.setModal(True)
        self.setMinimumSize(450, 250)
        self.setupUI()
        self.current_key = current_key
        if current_key:
            self.key_display.setText(current_key)
    
    def setupUI(self):
        layout = QVBoxLayout()
        
        icon_label = QLabel()
        icon_label.setPixmap(IconManager.create_icon(ThemeManager.themes[ThemeManager.current_theme]["accent"], 64).pixmap(64, 64))
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        instruction = QLabel(
            f"{lang.tr('hotkey_works')}\n\n"
            "Examples: Ctrl+Shift+F, Alt+Z, F1-F12, Ctrl+1, Shift+Space"
        )
        instruction.setAlignment(Qt.AlignCenter)
        instruction.setWordWrap(True)
        instruction.setStyleSheet(ThemeManager.get_info_style())
        layout.addWidget(instruction)
        
        self.key_display = QLineEdit()
        self.key_display.setReadOnly(True)
        self.key_display.setAlignment(Qt.AlignCenter)
        self.key_display.setPlaceholderText("Press any key...")
        self.key_display.setMinimumHeight(40)
        self.key_display.setStyleSheet(f"""
            QLineEdit {{
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border: 2px solid {ThemeManager.themes[ThemeManager.current_theme]["accent"]};
                border-radius: 5px;
                background-color: {ThemeManager.themes[ThemeManager.current_theme]["button_bg"]};
                color: {ThemeManager.themes[ThemeManager.current_theme]["fg"]};
            }}
        """)
        layout.addWidget(self.key_display)
        
        button_box = QDialogButtonBox()
        clear_btn = QPushButton("Clear")
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ThemeManager.themes[ThemeManager.current_theme]["button_bg"]};
                color: {ThemeManager.themes[ThemeManager.current_theme]["fg"]};
                border: 1px solid {ThemeManager.themes[ThemeManager.current_theme]["border"]};
                border-radius: 5px;
                padding: 5px 15px;
            }}
            QPushButton:hover {{ background-color: {ThemeManager.themes[ThemeManager.current_theme]["button_hover"]}; }}
        """)
        clear_btn.clicked.connect(self.clear_key)
        
        cancel_btn = button_box.addButton(QDialogButtonBox.Cancel)
        ok_btn = button_box.addButton(QDialogButtonBox.Ok)
        
        clear_btn.clicked.connect(self.clear_key)
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(button_box)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.key_display.setFocus()
    
    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()
        if key in (Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt, Qt.Key_Meta):
            return
        key_text = []
        if modifiers & Qt.ControlModifier:
            key_text.append("ctrl")
        if modifiers & Qt.AltModifier:
            key_text.append("alt")
        if modifiers & Qt.ShiftModifier:
            key_text.append("shift")
        key_name = QKeySequence(key).toString().lower()
        if key_name:
            special_keys = {
                "space": "space", "return": "enter", "escape": "esc",
                "delete": "del", "insert": "ins", "home": "home",
                "end": "end", "page up": "page up", "page down": "page down",
                "up": "up", "down": "down", "left": "left", "right": "right"
            }
            key_name = special_keys.get(key_name, key_name)
            key_text.append(key_name)
        if key_text:
            hotkey = "+".join(key_text)
            self.key_display.setText(hotkey)
    
    def get_hotkey(self):
        return self.key_display.text() if self.key_display.text() else None
    
    def clear_key(self):
        self.key_display.setText("")
        self.accept()

class HotkeyManager(QObject):
    hotkey_pressed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.hotkeys = {}
        self.hotkey_ids = {}
    
    def register_hotkey(self, hotkey, sound_name):
        if not GLOBAL_HOTKEY_AVAILABLE:
            return False
        try:
            if hotkey in self.hotkey_ids:
                try:
                    keyboard.remove_hotkey(self.hotkey_ids[hotkey])
                except:
                    pass
                del self.hotkey_ids[hotkey]
            
            if hotkey in self.hotkeys:
                del self.hotkeys[hotkey]
            
            hotkey_id = keyboard.add_hotkey(hotkey, self._on_hotkey, args=(sound_name,))
            self.hotkey_ids[hotkey] = hotkey_id
            self.hotkeys[hotkey] = sound_name
            return True
        except Exception as e:
            print(f"Error registering hotkey {hotkey}: {e}")
            return False
    
    def unregister_hotkey(self, hotkey):
        if GLOBAL_HOTKEY_AVAILABLE and hotkey in self.hotkey_ids:
            try:
                keyboard.remove_hotkey(self.hotkey_ids[hotkey])
                del self.hotkey_ids[hotkey]
                if hotkey in self.hotkeys:
                    del self.hotkeys[hotkey]
                return True
            except Exception as e:
                print(f"Error unregistering hotkey {hotkey}: {e}")
        return False
    
    def unregister_all(self):
        if GLOBAL_HOTKEY_AVAILABLE:
            for hotkey in list(self.hotkey_ids.keys()):
                try:
                    keyboard.remove_hotkey(self.hotkey_ids[hotkey])
                except:
                    pass
            self.hotkey_ids.clear()
            self.hotkeys.clear()
    
    def _on_hotkey(self, sound_name):
        try:
            self.hotkey_pressed.emit(sound_name)
        except Exception as e:
            print(f"Error in hotkey callback: {e}")

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle(lang.tr("settings"))
        self.setModal(True)
        self.setMinimumSize(400, 300)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        tabs = QTabWidget()
        
        theme_tab = QWidget()
        theme_layout = QVBoxLayout()
        
        theme_group = QGroupBox(lang.tr("theme"))
        theme_group_layout = QVBoxLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItem(lang.tr("black"), "black")
        self.theme_combo.addItem(lang.tr("white"), "white")
        self.theme_combo.addItem(lang.tr("green"), "green")
        self.theme_combo.addItem(lang.tr("blue"), "blue")
        self.theme_combo.addItem(lang.tr("pink"), "pink")
        self.theme_combo.setCurrentText(self.get_theme_name(ThemeManager.current_theme))
        
        theme_group_layout.addWidget(self.theme_combo)
        theme_group.setLayout(theme_group_layout)
        theme_layout.addWidget(theme_group)
        
        language_group = QGroupBox(lang.tr("language"))
        language_layout = QVBoxLayout()
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("Русский", "ru")
        self.lang_combo.addItem("English", "en")
        self.lang_combo.setCurrentIndex(0 if lang.current_lang == "ru" else 1)
        
        language_layout.addWidget(self.lang_combo)
        language_group.setLayout(language_layout)
        theme_layout.addWidget(language_group)
        
        theme_layout.addStretch()
        theme_tab.setLayout(theme_layout)
        tabs.addTab(theme_tab, lang.tr("settings"))
        
        layout.addWidget(tabs)
        
        button_box = QDialogButtonBox()
        save_btn = button_box.addButton(lang.tr("save_settings"), QDialogButtonBox.AcceptRole)
        cancel_btn = button_box.addButton(lang.tr("cancel"), QDialogButtonBox.RejectRole)
        save_btn.clicked.connect(self.save_settings)
        cancel_btn.clicked.connect(self.reject)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def get_theme_name(self, theme_key):
        theme_names = {
            "black": lang.tr("black"),
            "white": lang.tr("white"),
            "green": lang.tr("green"),
            "blue": lang.tr("blue"),
            "pink": lang.tr("pink")
        }
        return theme_names.get(theme_key, theme_key)
    
    def save_settings(self):
        new_theme = self.theme_combo.currentData()
        new_lang = self.lang_combo.currentData()
        
        if new_theme != ThemeManager.current_theme:
            ThemeManager.set_theme(new_theme)
            self.parent.apply_theme()
        
        if new_lang != lang.current_lang:
            lang.set_language(new_lang)
            self.parent.update_ui_language()
        
        self.parent.save_config()
        self.accept()

class SoundPadApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sounds = {}
        self.hotkeys = {}
        self.player = QMediaPlayer()
        self.current_playing_button = None
        self.volume = 70
        self.play_queue = []
        self.info_label = None
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.player.stateChanged.connect(self.on_player_state_changed)
        self.hotkey_manager = HotkeyManager()
        self.hotkey_manager.hotkey_pressed.connect(self.play_sound_by_name)
        self.initUI()
        self.load_config()
        self.apply_theme()
        self.play_timer = QTimer()
        self.play_timer.timeout.connect(self.process_play_queue)
        self.play_timer.start(50)
        if not GLOBAL_HOTKEY_AVAILABLE:
            QMessageBox.warning(self, "Warning", "Install keyboard: pip install keyboard")
    
    def on_media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia and self.current_playing_button:
            self.current_playing_button.stop_playing_animation()
            self.current_playing_button = None
    
    def on_player_state_changed(self, state):
        if state == QMediaPlayer.StoppedState and self.current_playing_button:
            self.current_playing_button.stop_playing_animation()
            self.current_playing_button = None
    
    def initUI(self):
        self.setWindowTitle("KeySound - Global Hotkeys")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(IconManager.create_icon("#3498db", 64))
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        control_panel = QHBoxLayout()
        
        self.add_sound_btn = QPushButton(lang.tr("add_sound"))
        self.add_sound_btn.setIcon(IconManager.create_icon("#2ecc71", 24))
        self.add_sound_btn.clicked.connect(self.add_sound)
        
        self.remove_sound_btn = QPushButton(lang.tr("remove_sound"))
        self.remove_sound_btn.setIcon(IconManager.create_icon("#e74c3c", 24))
        self.remove_sound_btn.clicked.connect(self.remove_sound)
        
        self.stop_all_btn = QPushButton(lang.tr("stop_all"))
        self.stop_all_btn.setIcon(IconManager.create_icon("#f39c12", 24))
        self.stop_all_btn.clicked.connect(self.stop_all_sounds)
        
        self.clear_all_btn = QPushButton(lang.tr("clear_all"))
        self.clear_all_btn.setIcon(IconManager.create_icon("#95a5a6", 24))
        self.clear_all_btn.clicked.connect(self.clear_all_sounds)
        
        self.show_hotkeys_btn = QPushButton(lang.tr("show_hotkeys"))
        self.show_hotkeys_btn.setIcon(IconManager.create_icon("#1abc9c", 24))
        self.show_hotkeys_btn.clicked.connect(self.show_hotkeys_list)
        
        self.settings_btn = QPushButton(lang.tr("settings"))
        self.settings_btn.setIcon(IconManager.create_icon("#9b59b6", 24))
        self.settings_btn.clicked.connect(self.open_settings)
        
        control_panel.addWidget(self.add_sound_btn)
        control_panel.addWidget(self.remove_sound_btn)
        control_panel.addWidget(self.stop_all_btn)
        control_panel.addWidget(self.clear_all_btn)
        control_panel.addWidget(self.show_hotkeys_btn)
        control_panel.addWidget(self.settings_btn)
        
        volume_layout = QHBoxLayout()
        volume_icon = QLabel()
        volume_icon.setPixmap(IconManager.create_icon("#3498db", 24).pixmap(24, 24))
        volume_layout.addWidget(volume_icon)
        volume_label = QLabel(f"{lang.tr('volume')}:")
        volume_label.setFont(QFont("Arial", 10))
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.volume)
        self.volume_slider.valueChanged.connect(self.change_volume)
        self.volume_value_label = QLabel(f"{self.volume}%")
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addWidget(self.volume_value_label)
        control_panel.addLayout(volume_layout)
        control_panel.addStretch()
        main_layout.addLayout(control_panel)
        
        info_panel = QHBoxLayout()
        self.info_label = QLabel(lang.tr("hotkey_works"))
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet(ThemeManager.get_info_style())
        info_panel.addWidget(self.info_label)
        info_panel.addStretch()
        main_layout.addLayout(info_panel)
        
        self.sounds_grid = QGridLayout()
        self.sounds_grid.setSpacing(20)
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.sounds_grid)
        from PyQt5.QtWidgets import QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)
        
        self.status_label = QLabel(f"{lang.tr('ready')} | {lang.tr('hotkey_works')}")
        self.status_label.setStyleSheet(f"QLabel {{ padding: 10px; background-color: {ThemeManager.themes[ThemeManager.current_theme]['status_bg']}; color: {ThemeManager.themes[ThemeManager.current_theme]['fg']}; font-weight: bold; border-radius: 5px; }}")
        main_layout.addWidget(self.status_label)
    
    def apply_theme(self):
        self.setStyleSheet(ThemeManager.get_style())
        theme = ThemeManager.themes[ThemeManager.current_theme]
        self.status_label.setStyleSheet(f"QLabel {{ padding: 10px; background-color: {theme['status_bg']}; color: {theme['fg']}; font-weight: bold; border-radius: 5px; }}")
        
        if self.info_label:
            self.info_label.setStyleSheet(ThemeManager.get_info_style())
        
        for button in self.sounds.keys():
            button.update_style()
    
    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()
    
    def update_ui_language(self):
        self.add_sound_btn.setText(lang.tr("add_sound"))
        self.remove_sound_btn.setText(lang.tr("remove_sound"))
        self.stop_all_btn.setText(lang.tr("stop_all"))
        self.clear_all_btn.setText(lang.tr("clear_all"))
        self.show_hotkeys_btn.setText(lang.tr("show_hotkeys"))
        self.settings_btn.setText(lang.tr("settings"))
        self.status_label.setText(f"{lang.tr('ready')} | {lang.tr('hotkey_works')}")
        
        if self.info_label:
            self.info_label.setText(lang.tr("hotkey_works"))
        
        for button in self.sounds.keys():
            button.update_style()
    
    def register_global_hotkey(self, button):
        if not GLOBAL_HOTKEY_AVAILABLE or not button.hotkey:
            return False
        
        try:
            if button.hotkey in self.hotkeys:
                self.hotkey_manager.unregister_hotkey(button.hotkey)
                del self.hotkeys[button.hotkey]
            
            if self.hotkey_manager.register_hotkey(button.hotkey, button.text()):
                self.hotkeys[button.hotkey] = button
                self.status_label.setText(f"{lang.tr('hotkey_assigned')}: '{button.hotkey}' -> '{button.text()}'")
                return True
            else:
                self.status_label.setText(f"{lang.tr('hotkey_error')}: {button.hotkey}")
                return False
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            return False
    
    def unregister_global_hotkey(self, button):
        if GLOBAL_HOTKEY_AVAILABLE and button.hotkey and button.hotkey in self.hotkeys:
            try:
                self.hotkey_manager.unregister_hotkey(button.hotkey)
                del self.hotkeys[button.hotkey]
                return True
            except Exception as e:
                print(f"Error unregistering: {e}")
        return False
    
    def play_sound_by_name(self, sound_name):
        try:
            for button in self.sounds.keys():
                if button.text() == sound_name:
                    self.play_queue.append(button)
                    break
        except Exception as e:
            print(f"Error in play_sound_by_name: {e}")
    
    def process_play_queue(self):
        try:
            if self.play_queue:
                button = self.play_queue.pop(0)
                self.play_sound(button)
        except Exception as e:
            print(f"Error in process_play_queue: {e}")
    
    def add_sound(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", 
                "Audio Files (*.mp3 *.wav *.ogg *.m4a);;All Files (*.*)")
            if file_path:
                name, ok = QInputDialog.getText(self, "Sound Name", lang.tr("enter_name"))
                if not ok or not name.strip():
                    name = os.path.basename(file_path).split('.')[0]
                reply = QMessageBox.question(self, "Global Hotkey", lang.tr("want_hotkey"),
                                            QMessageBox.Yes | QMessageBox.No)
                hotkey = None
                if reply == QMessageBox.Yes:
                    dialog = HotkeyDialog(parent=self)
                    if dialog.exec_() == QDialog.Accepted:
                        hotkey = dialog.get_hotkey()
                        if hotkey and hotkey in self.hotkeys:
                            reply = QMessageBox.question(self, "Conflict", lang.tr("hotkey_conflict"),
                                                        QMessageBox.Yes | QMessageBox.No)
                            if reply == QMessageBox.No:
                                hotkey = None
                button = SoundPadButton(name, file_path, hotkey)
                button.clicked.connect(lambda checked, b=button: self.play_sound(b))
                button.setContextMenuPolicy(Qt.CustomContextMenu)
                button.customContextMenuRequested.connect(lambda pos, b=button: self.show_context_menu(pos, b))
                row = self.sounds_grid.count() // 4
                col = self.sounds_grid.count() % 4
                self.sounds_grid.addWidget(button, row, col)
                self.sounds[button] = file_path
                if hotkey:
                    self.register_global_hotkey(button)
                self.status_label.setText(f"{lang.tr('added')}: {name}")
                self.save_config()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error adding sound: {str(e)}")
    
    def remove_sound(self):
        try:
            buttons = [self.sounds_grid.itemAt(i).widget() for i in range(self.sounds_grid.count())]
            if not buttons:
                QMessageBox.information(self, "Info", lang.tr("no_sounds"))
                return
            items = [f"{i+1}. {btn.text()} {f'[{btn.hotkey}]' if btn.hotkey else ''}" 
                    for i, btn in enumerate(buttons)]
            item, ok = QInputDialog.getItem(self, "Remove Sound", lang.tr("select_sound"), items, 0, False)
            if ok and item:
                index = int(item.split('.')[0]) - 1
                button_to_remove = buttons[index]
                if self.current_playing_button == button_to_remove:
                    self.player.stop()
                    self.current_playing_button.stop_playing_animation()
                    self.current_playing_button = None
                self.unregister_global_hotkey(button_to_remove)
                if button_to_remove in self.sounds:
                    del self.sounds[button_to_remove]
                self.sounds_grid.removeWidget(button_to_remove)
                button_to_remove.deleteLater()
                self.rebuild_grid()
                self.status_label.setText(f"{lang.tr('removed')}: {item.split('.')[1].strip()}")
                self.save_config()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error removing sound: {str(e)}")
    
    def clear_all_sounds(self):
        try:
            reply = QMessageBox.question(self, "Confirm", lang.tr("clear_confirm"), QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.player.stop()
                if self.current_playing_button:
                    self.current_playing_button.stop_playing_animation()
                    self.current_playing_button = None
                for button in list(self.sounds.keys()):
                    self.unregister_global_hotkey(button)
                for i in reversed(range(self.sounds_grid.count())):
                    widget = self.sounds_grid.itemAt(i).widget()
                    if widget:
                        self.sounds_grid.removeWidget(widget)
                        widget.deleteLater()
                self.sounds.clear()
                self.status_label.setText(lang.tr("clear_all"))
                self.save_config()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error clearing sounds: {str(e)}")
    
    def rebuild_grid(self):
        buttons = list(self.sounds.keys())
        self.clear_grid()
        for i, button in enumerate(buttons):
            row = i // 4
            col = i % 4
            self.sounds_grid.addWidget(button, row, col)
    
    def clear_grid(self):
        while self.sounds_grid.count():
            self.sounds_grid.takeAt(0)
    
    def play_sound(self, button):
        try:
            if button.sound_path and os.path.exists(button.sound_path):
                if self.current_playing_button and self.current_playing_button != button:
                    self.current_playing_button.stop_playing_animation()
                    self.player.stop()
                url = QUrl.fromLocalFile(button.sound_path)
                content = QMediaContent(url)
                self.player.setMedia(content)
                self.player.play()
                self.current_playing_button = button
                button.start_playing_animation()
                hotkey_info = f" [{button.hotkey}]" if button.hotkey else ""
                self.status_label.setText(f"{lang.tr('playing')}: {button.text()}{hotkey_info}")
            else:
                QMessageBox.warning(self, "Error", f"{lang.tr('error_file_not_found')}: {button.text()}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error playing sound: {str(e)}")
    
    def stop_all_sounds(self):
        try:
            self.player.stop()
            if self.current_playing_button:
                self.current_playing_button.stop_playing_animation()
                self.current_playing_button = None
            self.status_label.setText(lang.tr("stopped"))
        except Exception as e:
            print(f"Error stopping sounds: {e}")
    
    def change_volume(self, value):
        self.volume = value
        self.player.setVolume(value)
        self.volume_value_label.setText(f"{value}%")
    
    def show_context_menu(self, pos, button):
        try:
            from PyQt5.QtWidgets import QMenu, QAction
            menu = QMenu()
            rename_action = QAction(lang.tr("rename"), self)
            rename_action.triggered.connect(lambda: self.rename_sound(button))
            replace_action = QAction(lang.tr("replace_sound"), self)
            replace_action.triggered.connect(lambda: self.replace_sound(button))
            hotkey_action = QAction(lang.tr("assign_hotkey"), self)
            hotkey_action.triggered.connect(lambda: self.assign_hotkey(button))
            if button.hotkey:
                remove_hotkey_action = QAction(f"{lang.tr('remove_hotkey')} ({button.hotkey})", self)
                remove_hotkey_action.triggered.connect(lambda: self.remove_hotkey(button))
                menu.addAction(remove_hotkey_action)
            menu.addAction(hotkey_action)
            menu.addSeparator()
            menu.addAction(rename_action)
            menu.addAction(replace_action)
            menu.exec_(button.mapToGlobal(pos))
        except Exception as e:
            print(f"Error showing context menu: {e}")
    
    def assign_hotkey(self, button):
        try:
            dialog = HotkeyDialog(button.hotkey, self)
            if dialog.exec_() == QDialog.Accepted:
                new_hotkey = dialog.get_hotkey()
                if new_hotkey and new_hotkey in self.hotkeys and self.hotkeys[new_hotkey] != button:
                    reply = QMessageBox.question(self, "Conflict", lang.tr("hotkey_conflict"),
                                                QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        old_button = self.hotkeys[new_hotkey]
                        old_button.set_hotkey(None)
                        self.unregister_global_hotkey(old_button)
                    else:
                        return
                if button.hotkey:
                    self.unregister_global_hotkey(button)
                button.set_hotkey(new_hotkey)
                if new_hotkey:
                    self.register_global_hotkey(button)
                self.status_label.setText(f"{lang.tr('hotkey_assigned')}: '{button.text()}'")
                self.save_config()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error assigning hotkey: {str(e)}")
    
    def remove_hotkey(self, button):
        try:
            if button.hotkey:
                self.unregister_global_hotkey(button)
                button.set_hotkey(None)
                self.status_label.setText(f"{lang.tr('hotkey_removed')}: '{button.text()}'")
                self.save_config()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error removing hotkey: {str(e)}")
    
    def rename_sound(self, button):
        try:
            new_name, ok = QInputDialog.getText(self, "Rename", lang.tr("enter_new_name"), text=button.text())
            if ok and new_name.strip():
                if button.hotkey and button.hotkey in self.hotkeys:
                    self.hotkey_manager.unregister_hotkey(button.hotkey)
                    self.hotkey_manager.register_hotkey(button.hotkey, new_name)
                button.setText(new_name)
                self.status_label.setText(f"{lang.tr('renamed')}: {new_name}")
                self.save_config()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error renaming: {str(e)}")
    
    def replace_sound(self, button):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select New Audio File", "", 
                "Audio Files (*.mp3 *.wav *.ogg *.m4a);;All Files (*.*)")
            if file_path:
                button.sound_path = file_path
                self.sounds[button] = file_path
                self.status_label.setText(f"{lang.tr('replaced')}: {button.text()}")
                self.save_config()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error replacing sound: {str(e)}")
    
    def show_hotkeys_list(self):
        try:
            if not self.hotkeys:
                QMessageBox.information(self, lang.tr("global_hotkeys"), lang.tr("no_hotkeys"))
                return
            dialog = QDialog(self)
            dialog.setWindowTitle(lang.tr("global_hotkeys"))
            dialog.setMinimumSize(500, 400)
            dialog.setWindowIcon(IconManager.create_icon("#1abc9c", 32))
            layout = QVBoxLayout()
            info_label = QLabel(lang.tr("hotkey_works"))
            info_label.setWordWrap(True)
            info_label.setStyleSheet(ThemeManager.get_info_style())
            layout.addWidget(info_label)
            list_widget = QListWidget()
            for hotkey, button in sorted(self.hotkeys.items()):
                item = QListWidgetItem(f"{hotkey} -> {button.text()}")
                item.setFont(QFont("Arial", 11))
                list_widget.addItem(item)
            layout.addWidget(list_widget)
            close_btn = QPushButton(lang.tr("close"))
            close_btn.setIcon(IconManager.create_icon("#3498db", 16))
            close_btn.clicked.connect(dialog.accept)
            close_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ThemeManager.themes[ThemeManager.current_theme]["button_bg"]};
                    color: {ThemeManager.themes[ThemeManager.current_theme]["fg"]};
                    border: 1px solid {ThemeManager.themes[ThemeManager.current_theme]["border"]};
                    border-radius: 5px;
                    padding: 8px;
                }}
                QPushButton:hover {{ background-color: {ThemeManager.themes[ThemeManager.current_theme]["button_hover"]}; }}
            """)
            layout.addWidget(close_btn)
            dialog.setLayout(layout)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error showing hotkeys: {str(e)}")
    
    def save_config(self):
        try:
            config = {
                "sounds": {},
                "hotkeys": {},
                "volume": self.volume,
                "theme": ThemeManager.current_theme,
                "language": lang.current_lang
            }
            for button, path in self.sounds.items():
                config["sounds"][button.text()] = path
                if button.hotkey:
                    config["hotkeys"][button.text()] = button.hotkey
            with open("soundpad_config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Save error: {e}")
    
    def load_config(self):
        try:
            if os.path.exists("soundpad_config.json"):
                with open("soundpad_config.json", "r", encoding="utf-8") as f:
                    config = json.load(f)
                sounds_data = config.get("sounds", {})
                hotkeys_data = config.get("hotkeys", {})
                volume = config.get("volume", 70)
                theme = config.get("theme", "white")
                language = config.get("language", "ru")
                
                ThemeManager.set_theme(theme)
                lang.set_language(language)
                
                self.volume = volume
                self.volume_slider.setValue(volume)
                self.player.setVolume(volume)
                
                for name, path in sounds_data.items():
                    if os.path.exists(path):
                        hotkey = hotkeys_data.get(name)
                        button = SoundPadButton(name, path, hotkey)
                        button.clicked.connect(lambda checked, b=button: self.play_sound(b))
                        button.setContextMenuPolicy(Qt.CustomContextMenu)
                        button.customContextMenuRequested.connect(lambda pos, b=button: self.show_context_menu(pos, b))
                        row = self.sounds_grid.count() // 4
                        col = self.sounds_grid.count() % 4
                        self.sounds_grid.addWidget(button, row, col)
                        self.sounds[button] = path
                        if hotkey:
                            self.register_global_hotkey(button)
                self.status_label.setText(f"Loaded {len(sounds_data)} sounds with {len(hotkeys_data)} hotkeys")
                self.update_ui_language()
                self.apply_theme()
        except Exception as e:
            print(f"Load error: {e}")
    
    def closeEvent(self, event):
        try:
            self.player.stop()
            if self.current_playing_button:
                self.current_playing_button.stop_playing_animation()
            if GLOBAL_HOTKEY_AVAILABLE:
                self.hotkey_manager.unregister_all()
            event.accept()
        except Exception as e:
            print(f"Error in closeEvent: {e}")
            event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = SoundPadApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()