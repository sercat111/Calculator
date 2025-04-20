import sys
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLineEdit, QPushButton, QLabel)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor, QLinearGradient, QBrush


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.memory = 0
        self.initUI()

    def initUI(self):
        # Основные настройки окна
        self.setWindowTitle('Калькулятор')
        self.setFixedSize(325, 500)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Главный вертикальный layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Установка градиентного фона
        self.set_gradient_background(central_widget)

        # Заголовок "Обычный"
        self.label = QLabel("Обычный")
        self.label.setFont(QFont('Arial', 20, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label)

        # Поле ввода
        self.entry = QLineEdit()
        self.entry.setFont(QFont('Arial', 20))
        self.entry.setAlignment(Qt.AlignRight)
        self.entry.setReadOnly(False)
        self.entry.setStyleSheet("""
            QLineEdit {
                background-color: #F2F4EF;
                border: none;
                padding: 5px;
            }
        """)
        main_layout.addWidget(self.entry)

        # Фрейм для кнопок
        self.button_frame = QWidget()
        self.button_frame.setStyleSheet("background-color: #F2F4EF;")
        main_layout.addWidget(self.button_frame)

        # Layout для кнопок
        self.grid_layout = QVBoxLayout(self.button_frame)
        self.grid_layout.setSpacing(5)

        # Кнопки памяти (MC, MR, M+, M-, MS, Mv)
        self.memory_buttons = {}
        memory_layout = QHBoxLayout()
        memory_buttons = ["MC", "MR", "M+", "M-", "MS", "Mv"]
        for btn_text in memory_buttons:
            btn = QPushButton(btn_text)
            btn.setFont(QFont('Arial', 12))
            btn.setFixedSize(50, 40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #F8F9F8;
                    border: none;
                    color: black;
                }
                QPushButton:disabled {
                    background-color: #D3D3D3;
                }
            """)
            btn.clicked.connect(lambda _, x=btn_text: self.on_button_click(x))
            memory_layout.addWidget(btn)
            self.memory_buttons[btn_text] = btn

        self.grid_layout.addLayout(memory_layout)
        self.update_memory_buttons()

        # Основные кнопки калькулятора
        buttons = [
            ["%", "CE", "C", "⌫"],
            ["√x", "x²", "⅔π", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["+/-", "0", ".", "="]
        ]

        button_colors = {
            "%": "#F8F9F8", "CE": "#F8F9F8", "C": "#F8F9F8", "⌫": "#F8F9F8",
            "√x": "#F8F9F8", "x²": "#F8F9F8", "⅔π": "#F8F9F8", "/": "#F8F9F8",
            "*": "#F8F9F8", "-": "#F8F9F8", "+": "#F8F9F8", "=": "#F8F9F8",
            "+/-": "#FFFFFF", "0": "#FFFFFF", ".": "#FFFFFF",
            "7": "#FFFFFF", "8": "#FFFFFF", "9": "#FFFFFF",
            "4": "#FFFFFF", "5": "#FFFFFF", "6": "#FFFFFF",
            "1": "#FFFFFF", "2": "#FFFFFF", "3": "#FFFFFF"
        }

        for row in buttons:
            h_layout = QHBoxLayout()
            h_layout.setSpacing(5)
            for btn_text in row:
                btn = QPushButton(btn_text)
                btn.setFont(QFont('Arial', 15))
                btn.setFixedHeight(50)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {button_colors.get(btn_text, "#FFFFFF")};
                        border: none;
                        color: black;
                    }}
                    QPushButton:pressed {{
                        background-color: #E0E0E0;
                    }}
                """)
                btn.clicked.connect(lambda _, x=btn_text: self.on_button_click(x))
                h_layout.addWidget(btn)
            self.grid_layout.addLayout(h_layout)

    def set_gradient_background(self, widget):
        palette = widget.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(240, 244, 245))  # #F0F4F5 (верх)
        gradient.setColorAt(1, QColor(242, 244, 239))  # #F2F4EF (низ)
        palette.setBrush(QPalette.Window, QBrush(gradient))
        widget.setAutoFillBackground(True)
        widget.setPalette(palette)

    def update_memory_buttons(self):
        """Обновляет состояние кнопок памяти"""
        if self.memory == 0:
            self.memory_buttons["MC"].setEnabled(False)
            self.memory_buttons["MR"].setEnabled(False)
        else:
            self.memory_buttons["MC"].setEnabled(True)
            self.memory_buttons["MR"].setEnabled(True)

    def on_button_click(self, value):
        current_text = self.entry.text()

        if current_text == "Ошибка":
            self.entry.clear()
            current_text = ""

        if value == "=":
            try:
                if any(char.isdigit() for char in current_text):
                    result = eval(current_text)
                    self.entry.setText(str(result))
                else:
                    self.entry.setText("Ошибка")
            except:
                self.entry.setText("Ошибка")
        elif value == "C":
            self.entry.clear()
        elif value == "CE":
            self.entry.clear()
        elif value == "⌫":
            if current_text != "Ошибка":
                self.entry.setText(current_text[:-1])
        elif value == "+/-":
            try:
                current_value = float(current_text)
                self.entry.setText(str(-current_value))
            except:
                self.entry.setText("Ошибка")
        elif value == "√x":
            try:
                current_value = float(current_text)
                self.entry.setText(str(math.sqrt(current_value)))
            except:
                self.entry.setText("Ошибка")
        elif value == "x²":
            try:
                current_value = float(current_text)
                self.entry.setText(str(current_value ** 2))
            except:
                self.entry.setText("Ошибка")
        elif value == "⅔π":
            self.entry.setText(str((2 / 3) * math.pi))
        elif value == "%":
            try:
                current_value = float(current_text)
                self.entry.setText(str(current_value / 100))
            except:
                self.entry.setText("Ошибка")
        elif value == "MC":
            self.memory = 0
            self.update_memory_buttons()
        elif value == "MR":
            if self.memory != 0:
                self.entry.setText(str(self.memory))
        elif value == "M+":
            try:
                self.memory += float(current_text)
                self.update_memory_buttons()
            except:
                self.entry.setText("Ошибка")
        elif value == "M-":
            try:
                self.memory -= float(current_text)
                self.update_memory_buttons()
            except:
                self.entry.setText("Ошибка")
        elif value == "MS":
            try:
                self.memory = float(current_text)
                self.update_memory_buttons()
            except:
                self.entry.setText("Ошибка")
        elif value == "Mv":
            if self.memory != 0:
                self.entry.setText(str(self.memory))
        else:
            if value in ["+", "-", "*", "/", "="]:
                if any(char.isdigit() for char in current_text):
                    self.entry.setText(current_text + value)
            else:
                self.entry.setText(current_text + value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())