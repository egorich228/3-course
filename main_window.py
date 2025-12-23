import sqlite3
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QComboBox, QLabel, QHeaderView, QMessageBox, QFrame, QLineEdit, QDialog,
                             QFormLayout, QDialogButtonBox, QStackedWidget, QGroupBox, QCheckBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QDoubleValidator, QIntValidator
from database import Database
from datetime import datetime, timedelta

class EmployeeDialog(QDialog):
    def __init__(self, parent=None, employee_data=None):
        super().__init__(parent)
        self.employee_data = employee_data
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Добавить сотрудника" if not self.employee_data else "Редактировать сотрудника")
        self.setFixedSize(400, 300)
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.full_name_edit = QLineEdit()
        self.full_name_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        form_layout.addRow("ФИО:", self.full_name_edit)
        self.position_edit = QLineEdit()
        self.position_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        form_layout.addRow("Должность:", self.position_edit)
        self.phone_edit = QLineEdit()
        self.phone_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        form_layout.addRow("Телефон:", self.phone_edit)
        layout.addLayout(form_layout)
        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.Save).setText("Сохранить")
        button_box.button(QDialogButtonBox.Cancel).setText("Отмена")
        button_style = "QPushButton { padding: 8px 15px; border: none; border-radius: 5px; font-weight: bold; }"
        button_box.button(QDialogButtonBox.Save).setStyleSheet(button_style + "background-color: #27ae60; color: white;")
        button_box.button(QDialogButtonBox.Cancel).setStyleSheet(button_style + "background-color: #95a5a6; color: white;")
        layout.addWidget(button_box)
        if self.employee_data:
            self.full_name_edit.setText(self.employee_data.get('full_name', ''))
            self.position_edit.setText(self.employee_data.get('position', ''))
            self.phone_edit.setText(self.employee_data.get('phone', ''))

    def get_data(self):
        return {'full_name': self.full_name_edit.text().strip(), 'position': self.position_edit.text().strip(), 'phone': self.phone_edit.text().strip()}

class ServiceDialog(QDialog):
    def __init__(self, parent=None, service_data=None):
        super().__init__(parent)
        self.service_data = service_data
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Добавить услугу" if not self.service_data else "Редактировать услугу")
        self.setFixedSize(400, 200)
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        form_layout.addRow("Название услуги:", self.name_edit)
        self.price_edit = QLineEdit()
        self.price_edit.setValidator(QDoubleValidator(0, 100000, 2))
        self.price_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        form_layout.addRow("Цена (руб):", self.price_edit)
        layout.addLayout(form_layout)
        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.Save).setText("Сохранить")
        button_box.button(QDialogButtonBox.Cancel).setText("Отмена")
        button_style = "QPushButton { padding: 8px 15px; border: none; border-radius: 5px; font-weight: bold; }"
        button_box.button(QDialogButtonBox.Save).setStyleSheet(button_style + "background-color: #27ae60; color: white;")
        button_box.button(QDialogButtonBox.Cancel).setStyleSheet(button_style + "background-color: #95a5a6; color: white;")
        layout.addWidget(button_box)
        if self.service_data:
            self.name_edit.setText(self.service_data.get('name', ''))
            self.price_edit.setText(str(self.service_data.get('price', 0)))

    def get_data(self):
        return {'name': self.name_edit.text().strip(), 'price': float(self.price_edit.text() or 0)}

class MaterialDialog(QDialog):
    def __init__(self, parent=None, material_data=None):
        super().__init__(parent)
        self.material_data = material_data
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Добавить материал" if not self.material_data else "Редактировать материал")
        self.setFixedSize(400, 300)
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        form_layout.addRow("Название материала:", self.name_edit)
        self.quantity_edit = QLineEdit()
        self.quantity_edit.setValidator(QDoubleValidator(0, 100000, 2))
        self.quantity_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        form_layout.addRow("Количество:", self.quantity_edit)
        self.unit_edit = QLineEdit()
        self.unit_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        form_layout.addRow("Единица измерения:", self.unit_edit)
        self.cost_edit = QLineEdit()
        self.cost_edit.setValidator(QDoubleValidator(0, 100000, 2))
        self.cost_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        form_layout.addRow("Стоимость (руб):", self.cost_edit)
        layout.addLayout(form_layout)
        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.Save).setText("Сохранить")
        button_box.button(QDialogButtonBox.Cancel).setText("Отмена")
        button_style = "QPushButton { padding: 8px 15px; border: none; border-radius: 5px; font-weight: bold; }"
        button_box.button(QDialogButtonBox.Save).setStyleSheet(button_style + "background-color: #27ae60; color: white;")
        button_box.button(QDialogButtonBox.Cancel).setStyleSheet(button_style + "background-color: #95a5a6; color: white;")
        layout.addWidget(button_box)
        if self.material_data:
            self.name_edit.setText(self.material_data.get('name', ''))
            self.quantity_edit.setText(str(self.material_data.get('quantity', 0)))
            self.unit_edit.setText(self.material_data.get('unit', ''))
            self.cost_edit.setText(str(self.material_data.get('cost', 0)))

    def get_data(self):
        return {'name': self.name_edit.text().strip(), 'quantity': float(self.quantity_edit.text() or 0), 'unit': self.unit_edit.text().strip(), 'cost': float(self.cost_edit.text() or 0)}

class AddMaterialToServiceDialog(QDialog):
    def __init__(self, parent=None, db=None, service_id=None):
        super().__init__(parent)
        self.db = db
        self.service_id = service_id
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Добавить материал к услуге")
        self.setFixedSize(400, 200)
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.material_combo = QComboBox()
        self.load_materials()
        self.material_combo.setStyleSheet("QComboBox { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        form_layout.addRow("Материал:", self.material_combo)
        self.quantity_edit = QLineEdit()
        self.quantity_edit.setValidator(QDoubleValidator(0, 100000, 2))
        self.quantity_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        form_layout.addRow("Количество:", self.quantity_edit)
        layout.addLayout(form_layout)
        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.Save).setText("Добавить")
        button_box.button(QDialogButtonBox.Cancel).setText("Отмена")
        button_style = "QPushButton { padding: 8px 15px; border: none; border-radius: 5px; font-weight: bold; }"
        button_box.button(QDialogButtonBox.Save).setStyleSheet(button_style + "background-color: #27ae60; color: white;")
        button_box.button(QDialogButtonBox.Cancel).setStyleSheet(button_style + "background-color: #95a5a6; color: white;")
        layout.addWidget(button_box)

    def load_materials(self):
        materials = self.db.get_materials()
        self.material_combo.clear()
        for material in materials:
            self.material_combo.addItem(f"{material[1]} ({material[3]})", material[0])

    def get_data(self):
        material_id = self.material_combo.currentData()
        quantity = float(self.quantity_edit.text() or 0)
        return material_id, quantity

class ServiceMaterialsDialog(QDialog):
    def __init__(self, parent=None, db=None, service_id=None, service_name=""):
        super().__init__(parent)
        self.db = db
        self.service_id = service_id
        self.setup_ui(service_name)

    def setup_ui(self, service_name):
        self.setWindowTitle(f"Материалы для услуги: {service_name}")
        self.setFixedSize(600, 400)
        layout = QVBoxLayout(self)
        add_button_layout = QHBoxLayout()
        self.add_material_btn = QPushButton("Добавить материал")
        self.add_material_btn.setStyleSheet("QPushButton { padding: 8px 15px; border: none; border-radius: 5px; font-weight: bold; background-color: #27ae60; color: white; } QPushButton:hover { background-color: #219a52; }")
        self.add_material_btn.clicked.connect(self.add_material)
        add_button_layout.addWidget(self.add_material_btn)
        add_button_layout.addStretch()
        layout.addLayout(add_button_layout)
        self.materials_table = QTableWidget()
        self.materials_table.setColumnCount(4)
        self.materials_table.setHorizontalHeaderLabels(["Материал", "Количество", "Ед. изм.", "Удаление"])
        self.materials_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.materials_table.setStyleSheet("QTableWidget { border: 1px solid #bdc3c7; border-radius: 5px; gridline-color: #bdc3c7; background-color: white; } QTableWidget::item { padding: 10px; border-bottom: 1px solid #ecf0f1; selection-background-color: #d6eaf8; } QTableWidget::item:selected { background-color: #3498db; color: white; } QHeaderView::section { background-color: #34495e; color: white; font-weight: bold; padding: 10px; border: none; }")
        layout.addWidget(self.materials_table)
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.Close).setText("Закрыть")
        button_box.button(QDialogButtonBox.Close).setStyleSheet("QPushButton { padding: 8px 15px; border: none; border-radius: 5px; font-weight: bold; background-color: #95a5a6; color: white; } QPushButton:hover { background-color: #7f8c8d; }")
        layout.addWidget(button_box)
        self.load_service_materials()

    def load_service_materials(self):
        materials = self.db.get_service_materials(self.service_id)
        self.materials_table.setRowCount(len(materials))
        for row, material in enumerate(materials):
            material_id, name, quantity_required, current_quantity, unit = material
            self.materials_table.setItem(row, 0, QTableWidgetItem(name))
            self.materials_table.setItem(row, 1, QTableWidgetItem(str(quantity_required)))
            self.materials_table.setItem(row, 2, QTableWidgetItem(unit))
            remove_btn = QPushButton("Удалить")
            remove_btn.setStyleSheet("QPushButton { padding: 8px 12px; border: 1px solid #c0392b; border-radius: 4px; font-weight: bold; background-color: #e74c3c; color: white; min-width: 70px; } QPushButton:hover { background-color: #c0392b; } QPushButton:pressed { background-color: #a93226; }")
            remove_btn.clicked.connect(lambda checked, s_id=self.service_id, m_id=material_id: self.remove_material_from_service(s_id, m_id))
            self.materials_table.setCellWidget(row, 3, remove_btn)
            self.materials_table.setRowHeight(row, 55)

    def add_material(self):
        dialog = AddMaterialToServiceDialog(self, self.db, self.service_id)
        if dialog.exec_() == QDialog.Accepted:
            material_id, quantity = dialog.get_data()
            if quantity <= 0:
                QMessageBox.warning(self, "Ошибка", "Количество должно быть больше 0")
                return
            if self.db.add_service_material(self.service_id, material_id, quantity):
                self.load_service_materials()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить материал к услуге")

    def remove_material_from_service(self, service_id, material_id):
        if self.db.remove_service_material(service_id, material_id):
            self.load_service_materials()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось удалить материал из услуги")

class ReportsWidget(QWidget):
    def __init__(self, db, main_window):
        super().__init__()
        self.db = db
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        header_layout = QHBoxLayout()
        title_label = QLabel("Отчеты")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        period_layout = QHBoxLayout()
        period_layout.addWidget(QLabel("Период:"))
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate().addDays(-30))
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setStyleSheet("QDateEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        period_layout.addWidget(self.start_date_edit)
        period_layout.addWidget(QLabel("-"))
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setStyleSheet("QDateEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        period_layout.addWidget(self.end_date_edit)
        period_layout.addStretch()
        layout.addLayout(period_layout)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)
        finance_group = QGroupBox("Финансы")
        finance_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; color: #2c3e50; border: 2px solid #bdc3c7; border-radius: 8px; padding-top: 10px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }")
        finance_layout = QVBoxLayout(finance_group)
        self.revenue_label = QLabel("Выручка: 0 руб")
        self.material_costs_label = QLabel("Расходы на материалы: 0 руб")
        self.profit_label = QLabel("Прибыль: 0 руб")
        for label in [self.revenue_label, self.material_costs_label, self.profit_label]:
            label.setStyleSheet("QLabel { font-size: 14px; padding: 12px; background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; font-weight: bold; color: #2c3e50; margin: 2px; }")
            label.setMinimumHeight(50)
            finance_layout.addWidget(label)
        left_layout.addWidget(finance_group)
        apply_btn = QPushButton("Применить")
        apply_btn.setFixedSize(120, 40)
        apply_btn.setStyleSheet("QPushButton { background-color: #3498db; color: white; border: none; border-radius: 5px; font-weight: bold; } QPushButton:hover { background-color: #2980b9; }")
        apply_btn.clicked.connect(self.generate_report)
        left_layout.addWidget(apply_btn)
        left_layout.addStretch()
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)
        popular_group = QGroupBox("Популярные услуги")
        popular_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; color: #2c3e50; border: 2px solid #bdc3c7; border-radius: 8px; padding-top: 10px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }")
        popular_layout = QVBoxLayout(popular_group)
        self.popular_services_label = QLabel()
        self.popular_services_label.setStyleSheet("QLabel { font-size: 14px; padding: 12px; background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; min-height: 150px; }")
        popular_layout.addWidget(self.popular_services_label)
        right_layout.addWidget(popular_group)
        right_layout.addStretch()
        content_layout.addLayout(left_layout)
        content_layout.addLayout(right_layout)
        layout.addLayout(content_layout)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.back_btn = QPushButton("Главное меню")
        self.back_btn.setFixedSize(120, 40)
        self.back_btn.setStyleSheet("QPushButton { background-color: #3498db; color: white; border: none; border-radius: 5px; font-weight: bold; } QPushButton:hover { background-color: #2980b9; }")
        button_layout.addWidget(self.back_btn)
        layout.addLayout(button_layout)
        self.back_btn.clicked.connect(self.main_window.show_main_menu)
        self.generate_report()

    def generate_report(self):
        try:
            start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
            end_date = self.end_date_edit.date().toString("yyyy-MM-dd") + " 23:59:59"
            financial_data = self.db.get_financial_report(start_date, end_date)
            popular_services = self.db.get_popular_services(start_date, end_date)
            self.revenue_label.setText(f"Выручка: {financial_data['revenue']:.2f} руб")
            self.material_costs_label.setText(f"Расходы на материалы: {financial_data['material_costs']:.2f} руб")
            self.profit_label.setText(f"Прибыль: {financial_data['profit']:.2f} руб")
            if popular_services:
                popular_text = ""
                for i, (service_name, count) in enumerate(popular_services, 1):
                    popular_text += f"{i}. {service_name} - {count} \n"
                self.popular_services_label.setText(popular_text)
            else:
                self.popular_services_label.setText("Нет данных за выбранный период")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сгенерировать отчет: {str(e)}")

class ClientsWidget(QWidget):
    def __init__(self, db, main_window):
        super().__init__()
        self.db = db
        self.main_window = main_window
        self.setup_ui()
        self.load_clients()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_clients()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        header_layout = QHBoxLayout()
        title_label = QLabel("Клиенты")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        control_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск по ФИО...")
        self.search_edit.textChanged.connect(self.search_clients)
        self.search_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        control_layout.addWidget(self.search_edit)
        control_layout.addStretch()
        layout.addLayout(control_layout)
        self.clients_table = QTableWidget()
        self.clients_table.setColumnCount(5)
        self.clients_table.setHorizontalHeaderLabels(["Телефон", "ФИО", "Гос. номер авто", "Последний визит", "Кол-во заказов"])
        header = self.clients_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        self.clients_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.clients_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.clients_table.setSelectionMode(QTableWidget.SingleSelection)
        self.clients_table.setStyleSheet("QTableWidget { border: 1px solid #bdc3c7; border-radius: 5px; gridline-color: #bdc3c7; background-color: white; } QTableWidget::item { padding: 10px; border-bottom: 1px solid #ecf0f1; selection-background-color: #d6eaf8; } QTableWidget::item:selected { background-color: #3498db; color: white; } QHeaderView::section { background-color: #34495e; color: white; font-weight: bold; padding: 10px; border: none; }")
        layout.addWidget(self.clients_table)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.back_btn = QPushButton("Главное меню")
        self.back_btn.setFixedSize(120, 40)
        self.back_btn.setStyleSheet("QPushButton { background-color: #3498db; color: white; border: none; border-radius: 5px; font-weight: bold; } QPushButton:hover { background-color: #2980b9; }")
        button_layout.addWidget(self.back_btn)
        layout.addLayout(button_layout)
        self.back_btn.clicked.connect(self.main_window.show_main_menu)

    def load_clients(self, search_text=""):
        try:
            clients_data = self.db.get_clients_with_stats(search_text)
            self.clients_table.setRowCount(len(clients_data))
            for row, client in enumerate(clients_data):
                client_id, phone, full_name, license_plates, last_visit, orders_count = client
                item_phone = QTableWidgetItem(phone if phone else "")
                item_name = QTableWidgetItem(full_name if full_name else "")
                item_license = QTableWidgetItem(license_plates if license_plates else "")
                item_visit = QTableWidgetItem(last_visit if last_visit else "Нет визитов")
                item_orders = QTableWidgetItem(str(orders_count) if orders_count else "0")
                for item in [item_phone, item_name, item_license, item_visit, item_orders]:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.clients_table.setItem(row, 0, item_phone)
                self.clients_table.setItem(row, 1, item_name)
                self.clients_table.setItem(row, 2, item_license)
                self.clients_table.setItem(row, 3, item_visit)
                self.clients_table.setItem(row, 4, item_orders)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить клиентов: {str(e)}")

    def search_clients(self):
        search_text = self.search_edit.text().strip()
        self.load_clients(search_text)

class NewOrderWidget(QWidget):
    def __init__(self, db, main_window):
        super().__init__()
        self.db = db
        self.main_window = main_window
        self.selected_services = []
        self.selected_employee = None
        self.services_data = {}
        self.setup_ui()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_services()
        self.load_employees()
        self.clear_form()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        header_layout = QHBoxLayout()
        title_label = QLabel("Новый заказ")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        main_content = QVBoxLayout()
        main_content.setSpacing(15)
        car_section = self.create_car_section()
        main_content.addWidget(car_section)
        client_section = self.create_client_section()
        main_content.addWidget(client_section)
        services_section = self.create_services_section()
        main_content.addWidget(services_section, 1)
        employee_section = self.create_employee_section()
        main_content.addWidget(employee_section, 1)
        layout.addLayout(main_content, 1)
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        self.total_label = QLabel("Итого: 0 руб")
        self.total_label.setStyleSheet("QLabel { font-size: 16px; font-weight: bold; color: #2c3e50; padding: 10px; background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; }")
        total_layout.addWidget(self.total_label)
        layout.addLayout(total_layout)
        button_layout = QHBoxLayout()
        self.main_menu_btn = QPushButton("Главное меню")
        self.main_menu_btn.setFixedSize(120, 40)
        self.main_menu_btn.setStyleSheet("QPushButton { background-color: #3498db; color: white; border: none; border-radius: 5px; font-weight: bold; } QPushButton:hover { background-color: #2980b9; }")
        self.create_order_btn = QPushButton("Создать заказ")
        self.create_order_btn.setFixedSize(120, 40)
        self.create_order_btn.setStyleSheet("QPushButton { background-color: #27ae60; color: white; border: none; border-radius: 5px; font-weight: bold; } QPushButton:hover { background-color: #219a52; }")
        self.create_order_btn.setEnabled(False)
        button_layout.addWidget(self.main_menu_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.create_order_btn)
        layout.addLayout(button_layout)
        self.main_menu_btn.clicked.connect(self.go_to_main_menu)
        self.create_order_btn.clicked.connect(self.create_order)

    def create_car_section(self):
        group = QGroupBox("Данные автомобиля")
        group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; color: #2c3e50; border: 2px solid #bdc3c7; border-radius: 8px; padding-top: 10px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }")
        layout = QFormLayout(group)
        self.license_plate_edit = QLineEdit()
        self.license_plate_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        self.license_plate_edit.textChanged.connect(self.validate_form)
        layout.addRow("Гос. номер:", self.license_plate_edit)
        self.car_model_edit = QLineEdit()
        self.car_model_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        self.car_model_edit.textChanged.connect(self.validate_form)
        layout.addRow("Марка/модель:", self.car_model_edit)
        return group

    def create_client_section(self):
        group = QGroupBox("Клиент")
        group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; color: #2c3e50; border: 2px solid #bdc3c7; border-radius: 8px; padding-top: 10px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }")
        layout = QFormLayout(group)
        self.client_phone_edit = QLineEdit()
        self.client_phone_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        self.client_phone_edit.textChanged.connect(self.validate_form)
        layout.addRow("Телефон:", self.client_phone_edit)
        self.client_name_edit = QLineEdit()
        self.client_name_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        self.client_name_edit.textChanged.connect(self.validate_form)
        layout.addRow("ФИО:", self.client_name_edit)
        return group

    def create_services_section(self):
        group = QGroupBox("Выбор услуг")
        group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; color: #2c3e50; border: 2px solid #bdc3c7; border-radius: 8px; padding-top: 10px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }")
        layout = QVBoxLayout(group)
        self.services_table = QTableWidget()
        self.services_table.setColumnCount(3)
        self.services_table.setHorizontalHeaderLabels(["Выбрать", "Услуга", "Цена"])
        self.services_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.services_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.services_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.services_table.setSelectionMode(QTableWidget.SingleSelection)
        self.services_table.setStyleSheet("QTableWidget { border: 1px solid #bdc3c7; border-radius: 5px; gridline-color: #bdc3c7; background-color: white; } QTableWidget::item { padding: 10px; border-bottom: 1px solid #ecf0f1; selection-background-color: #d6eaf8; } QTableWidget::item:selected { background-color: #3498db; color: white; } QHeaderView::section { background-color: #34495e; color: white; font-weight: bold; padding: 10px; border: none; }")
        self.services_table.setMinimumHeight(200)
        layout.addWidget(self.services_table)
        return group

    def create_employee_section(self):
        group = QGroupBox("Назначить сотрудника")
        group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; color: #2c3e50; border: 2px solid #bdc3c7; border-radius: 8px; padding-top: 10px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top center; padding: 0 5px; }")
        layout = QVBoxLayout(group)
        self.employees_table = QTableWidget()
        self.employees_table.setColumnCount(2)
        self.employees_table.setHorizontalHeaderLabels(["ФИО", "Статус"])
        self.employees_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.employees_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.employees_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.employees_table.setSelectionMode(QTableWidget.SingleSelection)
        self.employees_table.setStyleSheet("QTableWidget { border: 1px solid #bdc3c7; border-radius: 5px; gridline-color: #bdc3c7; background-color: white; } QTableWidget::item { padding: 10px; border-bottom: 1px solid #ecf0f1; selection-background-color: #d6eaf8; } QTableWidget::item:selected { background-color: #3498db; color: white; } QHeaderView::section { background-color: #34495e; color: white; font-weight: bold; padding: 10px; border: none; }")
        self.employees_table.itemSelectionChanged.connect(self.select_employee)
        self.employees_table.setMinimumHeight(150)
        layout.addWidget(self.employees_table)
        return group

    def load_services(self):
        try:
            services = self.db.get_services()
            self.services_table.setRowCount(len(services))
            self.services_data = {}
            for row, service in enumerate(services):
                service_id, name, price = service
                self.services_data[service_id] = {'name': name, 'price': price}
                checkbox = QCheckBox()
                checkbox.stateChanged.connect(lambda state, s_id=service_id: self.toggle_service(s_id, state))
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setAlignment(Qt.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)
                self.services_table.setCellWidget(row, 0, checkbox_widget)
                item_name = QTableWidgetItem(name)
                item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
                self.services_table.setItem(row, 1, item_name)
                item_price = QTableWidgetItem(f"{price} руб")
                item_price.setFlags(item_price.flags() & ~Qt.ItemIsEditable)
                self.services_table.setItem(row, 2, item_price)
                item_name.setData(Qt.UserRole, service_id)
                self.services_table.setRowHeight(row, 60)
        except Exception as e:
            print(f"Ошибка загрузки услуг: {e}")

    def load_employees(self, search_text=""):
        try:
            if search_text:
                self.db.cursor.execute("SELECT id, full_name, position, phone FROM employees WHERE full_name LIKE ?", (f'%{search_text}%',))
                employees = self.db.cursor.fetchall()
            else:
                self.db.cursor.execute("SELECT id, full_name, position, phone FROM employees")
                employees = self.db.cursor.fetchall()
            self.employees_table.setRowCount(len(employees))
            for row, employee in enumerate(employees):
                employee_id, full_name, position, phone = employee
                try:
                    self.db.cursor.execute('SELECT COUNT(*) FROM orders WHERE employee_id = ? AND status = "В процессе"', (employee_id,))
                    active_orders_count = self.db.cursor.fetchone()[0]
                    status = "В работе" if active_orders_count > 0 else "Свободен"
                except Exception as e:
                    print(f"Ошибка проверки статуса сотрудника {employee_id}: {e}")
                    status = "Свободен"
                item_name = QTableWidgetItem(full_name or "")
                status_item = QTableWidgetItem(status)
                if status == "В работе":
                    status_item.setForeground(Qt.red)
                else:
                    status_item.setForeground(Qt.darkGreen)
                item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
                status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
                self.employees_table.setItem(row, 0, item_name)
                self.employees_table.setItem(row, 1, status_item)
                item_name.setData(Qt.UserRole, employee_id)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить сотрудников: {str(e)}")

    def toggle_service(self, service_id, state):
        service_data = self.services_data[service_id]
        if state == Qt.Checked:
            self.selected_services.append({'id': service_id, 'name': service_data['name'], 'price': service_data['price']})
        else:
            self.selected_services = [s for s in self.selected_services if s['id'] != service_id]
        self.update_total()
        self.validate_form()

    def select_employee(self):
        current_row = self.employees_table.currentRow()
        if current_row >= 0:
            status_item = self.employees_table.item(current_row, 1)
            if status_item.text() != "В работе":
                employee_id = self.employees_table.item(current_row, 0).data(Qt.UserRole)
                self.selected_employee = employee_id
            else:
                self.selected_employee = None
            self.validate_form()
        else:
            self.selected_employee = None
            self.validate_form()

    def update_total(self):
        total = sum(service['price'] for service in self.selected_services)
        self.total_label.setText(f"Итого: {total} руб")

    def validate_form(self):
        has_license_plate = bool(self.license_plate_edit.text().strip())
        has_client_phone = bool(self.client_phone_edit.text().strip())
        has_client_name = bool(self.client_name_edit.text().strip())
        has_services = len(self.selected_services) > 0
        has_employee = self.selected_employee is not None
        employee_not_busy = True
        if has_employee:
            current_row = self.employees_table.currentRow()
            if current_row >= 0:
                status_item = self.employees_table.item(current_row, 1)
                if status_item.text() == "В работе":
                    employee_not_busy = False
                    self.employees_table.clearSelection()
                    self.selected_employee = None
        is_valid = (has_license_plate and has_client_phone and has_client_name and has_services and has_employee and employee_not_busy)
        self.create_order_btn.setEnabled(is_valid)
        if is_valid:
            self.create_order_btn.setStyleSheet("QPushButton { background-color: #27ae60; color: white; border: none; border-radius: 5px; font-weight: bold; } QPushButton:hover { background-color: #219a52; }")
        else:
            self.create_order_btn.setStyleSheet("QPushButton { background-color: #95a5a6; color: white; border: none; border-radius: 5px; font-weight: bold; }")

    def go_to_main_menu(self):
        self.main_window.show_main_menu()

    def create_order(self):
        try:
            license_plate = self.license_plate_edit.text().strip()
            car_model = self.car_model_edit.text().strip()
            client_phone = self.client_phone_edit.text().strip()
            client_name = self.client_name_edit.text().strip()

            if not license_plate:
                QMessageBox.warning(self, "Ошибка", "Введите гос. номер автомобиля")
                return
            if not client_phone:
                QMessageBox.warning(self, "Ошибка", "Введите телефон клиента")
                return
            if not client_name:
                QMessageBox.warning(self, "Ошибка", "Введите ФИО клиента")
                return
            if not self.selected_services:
                QMessageBox.warning(self, "Ошибка", "Выберите хотя бы одну услугу")
                return
            if not self.selected_employee:
                QMessageBox.warning(self, "Ошибка", "Выберите сотрудника")
                return

            # Проверка доступности материалов
            all_materials_available = True
            missing_materials_info = []
            for service in self.selected_services:
                available, missing = self.db.check_materials_availability(service['id'])
                if not available:
                    all_materials_available = False
                    for material in missing:
                        missing_materials_info.append(
                            f"Услуга '{service['name']}': {material['name']} - требуется {material['required']} {material['unit']}, доступно {material['available']} {material['unit']}")

            if not all_materials_available:
                error_message = "Недостаточно материалов для выполнения заказа:\n\n" + "\n".join(missing_materials_info)
                QMessageBox.warning(self, "Ошибка", error_message)
                return

            # Показ окна подтверждения
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Подтверждение создания заказа")
            msg_box.setText("Вы точно хотите создать данный заказ?")
            msg_box.setIcon(QMessageBox.Question)

            # Создаем кастомные кнопки
            cancel_button = msg_box.addButton("Отмена", QMessageBox.RejectRole)
            yes_button = msg_box.addButton("Да", QMessageBox.AcceptRole)

            msg_box.setDefaultButton(cancel_button)
            msg_box.exec_()

            # Проверяем, какая кнопка была нажата
            if msg_box.clickedButton() != yes_button:
                return  # Пользователь отменил создание заказа

            # Создание заказа
            client_id = self.db.get_or_create_client(client_name, client_phone)
            client_cars = self.db.get_client_cars(client_id)
            car_exists = any(car[0] == license_plate for car in client_cars)
            if not car_exists:
                self.db.add_client_car(client_id, license_plate, car_model)

            # Списание материалов
            for service in self.selected_services:
                success = self.db.consume_materials_for_service(service['id'])
                if not success:
                    QMessageBox.warning(self, "Ошибка", f"Не удалось списать материалы для услуги '{service['name']}'")
                    return

            # Создание заказа в базе данных
            order_number = self.db.get_next_order_number()
            for service in self.selected_services:
                self.db.cursor.execute(
                    'INSERT INTO orders (order_number, license_plate, service_id, status, client_id, employee_id, created_date, materials_consumed) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (order_number, license_plate, service['id'], 'В процессе', client_id, self.selected_employee,
                     datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1))
            self.db.conn.commit()

            # Очистка формы и переход в главное меню
            self.clear_form()
            self.main_window.load_daily_info()
            self.main_window.load_current_orders()
            self.main_window.show_main_menu()

        except Exception as e:
            print(f"ОШИБКА при создании заказа: {str(e)}")
            import traceback
            print(f"Трассировка: {traceback.format_exc()}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось создать заказ: {str(e)}")
            if self.db.conn:
                self.db.conn.rollback()

    def get_or_create_client(self, name, phone):
        try:
            self.db.cursor.execute("SELECT id FROM clients WHERE full_name = ?", (name,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                self.db.cursor.execute("INSERT INTO clients (full_name) VALUES (?)", (name,))
                self.db.conn.commit()
                new_id = self.db.cursor.lastrowid
                return new_id
        except Exception as e:
            print(f"Ошибка при работе с клиентом: {e}")
            raise

    def clear_form(self):
        self.license_plate_edit.clear()
        self.car_model_edit.clear()
        self.client_phone_edit.clear()
        self.client_name_edit.clear()
        for row in range(self.services_table.rowCount()):
            checkbox_widget = self.services_table.cellWidget(row, 0)
            checkbox = checkbox_widget.findChild(QCheckBox)
            if checkbox:
                checkbox.setChecked(False)
        self.selected_services = []
        self.selected_employee = None
        self.update_total()
        self.validate_form()
        self.employees_table.clearSelection()

class EmployeesWidget(QWidget):
    def __init__(self, db, main_window):
        super().__init__()
        self.db = db
        self.main_window = main_window
        self.setup_ui()
        self.load_employees()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_employees()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        header_layout = QHBoxLayout()
        title_label = QLabel("Сотрудники")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        control_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск по ФИО...")
        self.search_edit.textChanged.connect(self.search_employees)
        self.search_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        control_layout.addWidget(self.search_edit)
        control_layout.addStretch()
        self.add_btn = QPushButton("Добавить")
        self.edit_btn = QPushButton("Редактировать")
        self.delete_btn = QPushButton("Удалить")
        button_style = "QPushButton { padding: 8px 15px; border: none; border-radius: 5px; font-weight: bold; margin-left: 5px; }"
        self.add_btn.setStyleSheet(button_style + "QPushButton { background-color: #27ae60; color: white; } QPushButton:hover { background-color: #219a52; }")
        self.edit_btn.setStyleSheet(button_style + "QPushButton { background-color: #3498db; color: white; } QPushButton:hover { background-color: #2980b9; }")
        self.delete_btn.setStyleSheet(button_style + "QPushButton { background-color: #e74c3c; color: white; } QPushButton:hover { background-color: #c0392b; }")
        control_layout.addWidget(self.add_btn)
        control_layout.addWidget(self.edit_btn)
        control_layout.addWidget(self.delete_btn)
        layout.addLayout(control_layout)
        self.employees_table = QTableWidget()
        self.employees_table.setColumnCount(4)
        self.employees_table.setHorizontalHeaderLabels(["ФИО", "Должность", "Телефон", "Статус"])
        header = self.employees_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.employees_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.employees_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.employees_table.setSelectionMode(QTableWidget.SingleSelection)
        self.employees_table.setStyleSheet("QTableWidget { border: 1px solid #bdc3c7; border-radius: 5px; gridline-color: #bdc3c7; background-color: white; } QTableWidget::item { padding: 10px; border-bottom: 1px solid #ecf0f1; selection-background-color: #d6eaf8; } QTableWidget::item:selected { background-color: #3498db; color: white; } QHeaderView::section { background-color: #34495e; color: white; font-weight: bold; padding: 10px; border: none; }")
        layout.addWidget(self.employees_table)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.back_btn = QPushButton("Главное меню")
        self.back_btn.setFixedSize(120, 40)
        self.back_btn.setStyleSheet("QPushButton { background-color: #3498db; color: white; border: none; border-radius: 5px; font-weight: bold; } QPushButton:hover { background-color: #2980b9; }")
        button_layout.addWidget(self.back_btn)
        layout.addLayout(button_layout)
        self.add_btn.clicked.connect(self.add_employee)
        self.edit_btn.clicked.connect(self.edit_employee)
        self.delete_btn.clicked.connect(self.delete_employee)
        self.back_btn.clicked.connect(self.main_window.show_main_menu)

    def load_employees(self, search_text=""):
        try:
            if search_text:
                self.db.cursor.execute("SELECT id, full_name, position, phone FROM employees WHERE full_name LIKE ?", (f'%{search_text}%',))
                employees = self.db.cursor.fetchall()
            else:
                self.db.cursor.execute("SELECT id, full_name, position, phone FROM employees")
                employees = self.db.cursor.fetchall()
            self.employees_table.setRowCount(len(employees))
            for row, employee in enumerate(employees):
                employee_id, full_name, position, phone = employee
                self.db.cursor.execute('SELECT status FROM orders WHERE employee_id = ? AND status = "В процессе" LIMIT 1', (employee_id,))
                active_order = self.db.cursor.fetchone()
                status = "В работе" if active_order else "Свободен"
                item_name = QTableWidgetItem(full_name or "")
                item_position = QTableWidgetItem(position or "")
                item_phone = QTableWidgetItem(phone or "")
                status_item = QTableWidgetItem(status)
                if status == "В работе":
                    status_item.setForeground(Qt.red)
                else:
                    status_item.setForeground(Qt.darkGreen)
                item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
                item_position.setFlags(item_position.flags() & ~Qt.ItemIsEditable)
                item_phone.setFlags(item_phone.flags() & ~Qt.ItemIsEditable)
                status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
                self.employees_table.setItem(row, 0, item_name)
                self.employees_table.setItem(row, 1, item_position)
                self.employees_table.setItem(row, 2, item_phone)
                self.employees_table.setItem(row, 3, status_item)
                item_name.setData(Qt.UserRole, employee_id)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить сотрудников: {str(e)}")

    def search_employees(self):
        search_text = self.search_edit.text().strip()
        self.load_employees(search_text)

    def add_employee(self):
        dialog = EmployeeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if not data['full_name']:
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
                return
            if not data['position']:
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
                return
            if not data['phone']:
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
                return
            try:
                self.db.cursor.execute("INSERT INTO employees (full_name, position, phone) VALUES (?, ?, ?)", (data['full_name'], data['position'], data['phone']))
                self.db.conn.commit()
                self.load_employees()
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed: employees.phone" in str(e):
                    QMessageBox.warning(self, "Ошибка", "Сотрудник уже в базе")
                else:
                    QMessageBox.warning(self, "Ошибка", f"Ошибка базы данных: {str(e)}")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось добавить сотрудника: {str(e)}")

    def edit_employee(self):
        current_row = self.employees_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для редактирования")
            return
        employee_id = self.employees_table.item(current_row, 0).data(Qt.UserRole)
        employee_data = {'full_name': self.employees_table.item(current_row, 0).text(), 'position': self.employees_table.item(current_row, 1).text(), 'phone': self.employees_table.item(current_row, 2).text()}
        dialog = EmployeeDialog(self, employee_data)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if not data['full_name']:
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
                return
            if not data['position']:
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
                return
            if not data['phone']:
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
                return
            try:
                self.db.cursor.execute("SELECT id FROM employees WHERE phone = ? AND id != ?", (data['phone'], employee_id))
                existing_employee = self.db.cursor.fetchone()
                if existing_employee:
                    QMessageBox.warning(self, "Ошибка", "Сотрудник с таким номером телефона уже существует")
                    return
                self.db.cursor.execute("UPDATE employees SET full_name = ?, position = ?, phone = ? WHERE id = ?", (data['full_name'], data['position'], data['phone'], employee_id))
                self.db.conn.commit()
                self.load_employees(self.search_edit.text().strip())
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed: employees.phone" in str(e):
                    QMessageBox.warning(self, "Ошибка", "Сотрудник с таким номером телефона уже существует")
                else:
                    QMessageBox.warning(self, "Ошибка", f"Ошибка базы данных: {str(e)}")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось обновить данные: {str(e)}")

    def delete_employee(self):
        current_row = self.employees_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для удаления")
            return
        employee_name = self.employees_table.item(current_row, 0).text()
        employee_id = self.employees_table.item(current_row, 0).data(Qt.UserRole)
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Подтверждение удаления")
        msg_box.setText(f"Вы уверены, что хотите удалить данного сотрудника?")
        msg_box.setIcon(QMessageBox.Question)
        yes_button = msg_box.addButton("Да", QMessageBox.YesRole)
        no_button = msg_box.addButton("Нет", QMessageBox.NoRole)
        msg_box.setDefaultButton(no_button)
        msg_box.exec_()
        if msg_box.clickedButton() == yes_button:
            try:
                self.db.cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
                self.db.conn.commit()
                self.load_employees(self.search_edit.text().strip())
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось удалить сотрудника: {str(e)}")

class ServicesWidget(QWidget):
    def __init__(self, db, main_window):
        super().__init__()
        self.db = db
        self.main_window = main_window
        self.setup_ui()
        self.load_services()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_services()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        header_layout = QHBoxLayout()
        title_label = QLabel("Услуги")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        control_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск по названию...")
        self.search_edit.textChanged.connect(self.search_services)
        self.search_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        control_layout.addWidget(self.search_edit)
        control_layout.addStretch()
        self.add_btn = QPushButton("Добавить")
        self.edit_btn = QPushButton("Редактировать")
        self.delete_btn = QPushButton("Удалить")
        self.materials_btn = QPushButton("Материалы")
        button_style = "QPushButton { padding: 8px 15px; border: none; border-radius: 5px; font-weight: bold; margin-left: 5px; }"
        self.add_btn.setStyleSheet(button_style + "QPushButton { background-color: #27ae60; color: white; } QPushButton:hover { background-color: #219a52; }")
        self.edit_btn.setStyleSheet(button_style + "QPushButton { background-color: #3498db; color: white; } QPushButton:hover { background-color: #2980b9; }")
        self.delete_btn.setStyleSheet(button_style + "QPushButton { background-color: #e74c3c; color: white; } QPushButton:hover { background-color: #c0392b; }")
        self.materials_btn.setStyleSheet(button_style + "QPushButton { background-color: #f39c12; color: white; } QPushButton:hover { background-color: #e67e22; }")
        control_layout.addWidget(self.add_btn)
        control_layout.addWidget(self.edit_btn)
        control_layout.addWidget(self.delete_btn)
        control_layout.addWidget(self.materials_btn)
        layout.addLayout(control_layout)
        self.services_table = QTableWidget()
        self.services_table.setColumnCount(2)
        self.services_table.setHorizontalHeaderLabels(["Название", "Цена"])
        header = self.services_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.services_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.services_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.services_table.setSelectionMode(QTableWidget.SingleSelection)
        self.services_table.setStyleSheet("QTableWidget { border: 1px solid #bdc3c7; border-radius: 5px; gridline-color: #bdc3c7; background-color: white; } QTableWidget::item { padding: 10px; border-bottom: 1px solid #ecf0f1; selection-background-color: #d6eaf8; } QTableWidget::item:selected { background-color: #3498db; color: white; } QHeaderView::section { background-color: #34495e; color: white; font-weight: bold; padding: 10px; border: none; }")
        layout.addWidget(self.services_table)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.back_btn = QPushButton("Главное меню")
        self.back_btn.setFixedSize(120, 40)
        self.back_btn.setStyleSheet("QPushButton { background-color: #3498db; color: white; border: none; border-radius: 5px; font-weight: bold; } QPushButton:hover { background-color: #2980b9; }")
        button_layout.addWidget(self.back_btn)
        layout.addLayout(button_layout)
        self.add_btn.clicked.connect(self.add_service)
        self.edit_btn.clicked.connect(self.edit_service)
        self.delete_btn.clicked.connect(self.delete_service)
        self.materials_btn.clicked.connect(self.manage_service_materials)
        self.back_btn.clicked.connect(self.main_window.show_main_menu)

    def load_services(self, search_text=""):
        try:
            services = self.db.get_services()
            if search_text:
                services = [s for s in services if search_text.lower() in s[1].lower()]
            self.services_table.setRowCount(len(services))
            for row, service in enumerate(services):
                service_id, name, price = service
                item_name = QTableWidgetItem(name)
                item_price = QTableWidgetItem(f"{price} руб")
                item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
                item_price.setFlags(item_price.flags() & ~Qt.ItemIsEditable)
                self.services_table.setItem(row, 0, item_name)
                self.services_table.setItem(row, 1, item_price)
                item_name.setData(Qt.UserRole, service_id)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить услуги: {str(e)}")

    def search_services(self):
        search_text = self.search_edit.text().strip()
        self.load_services(search_text)

    def add_service(self):
        dialog = ServiceDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if not data['name']:
                QMessageBox.warning(self, "Ошибка", "Название услуги обязательно")
                return
            try:
                price = float(data['price'])
                if price <= 0:
                    QMessageBox.warning(self, "Ошибка", "Цена услуги обязательна")
                    return
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Введите корректную цену")
                return
            if self.db.service_name_exists(data['name']):
                QMessageBox.warning(self, "Ошибка", "Услуга с таким названием уже существует")
                return
            success, message = self.db.add_service(data['name'], price)
            if success:
                self.load_services()
            else:
                QMessageBox.warning(self, "Ошибка", message)

    def edit_service(self):
        current_row = self.services_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите услугу для редактирования")
            return
        service_id = self.services_table.item(current_row, 0).data(Qt.UserRole)
        service_data = {'name': self.services_table.item(current_row, 0).text(), 'price': float(self.services_table.item(current_row, 1).text().replace(' руб', ''))}
        dialog = ServiceDialog(self, service_data)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if not data['name']:
                QMessageBox.warning(self, "Ошибка", "Название услуги обязательно")
                return
            if self.db.service_name_exists(data['name'], service_id):
                QMessageBox.warning(self, "Ошибка", "Услуга с таким названием уже существует")
                return
            if self.db.update_service(service_id, data['name'], data['price']):
                self.load_services(self.search_edit.text().strip())
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось обновить услугу")

    def delete_service(self):
        current_row = self.services_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите услугу для удаления")
            return
        service_name = self.services_table.item(current_row, 0).text()
        service_id = self.services_table.item(current_row, 0).data(Qt.UserRole)
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Подтверждение удаления")
        msg_box.setText(f"Удалить данную услугу?")
        msg_box.setIcon(QMessageBox.Question)
        yes_button = msg_box.addButton("Да", QMessageBox.YesRole)
        no_button = msg_box.addButton("Нет", QMessageBox.NoRole)
        msg_box.setDefaultButton(no_button)
        msg_box.exec_()
        if msg_box.clickedButton() == yes_button:
            if self.db.delete_service(service_id):
                self.load_services(self.search_edit.text().strip())
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить услугу")

    def manage_service_materials(self):
        current_row = self.services_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите услугу для управления материалами")
            return
        service_id = self.services_table.item(current_row, 0).data(Qt.UserRole)
        service_name = self.services_table.item(current_row, 0).text()
        dialog = ServiceMaterialsDialog(self, self.db, service_id, service_name)
        dialog.exec_()

class MaterialsWidget(QWidget):
    def __init__(self, db, main_window):
        super().__init__()
        self.db = db
        self.main_window = main_window
        self.setup_ui()
        self.load_materials()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_materials()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        header_layout = QHBoxLayout()
        title_label = QLabel("Материалы")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        control_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск по названию...")
        self.search_edit.textChanged.connect(self.search_materials)
        self.search_edit.setStyleSheet("QLineEdit { padding: 8px; border: 1px solid #bdc3c7; border-radius: 5px; font-size: 14px; }")
        control_layout.addWidget(self.search_edit)
        control_layout.addStretch()
        self.add_btn = QPushButton("Добавить")
        self.edit_btn = QPushButton("Редактировать")
        self.delete_btn = QPushButton("Удалить")
        button_style = "QPushButton { padding: 8px 15px; border: none; border-radius: 5px; font-weight: bold; margin-left: 5px; }"
        self.add_btn.setStyleSheet(button_style + "QPushButton { background-color: #27ae60; color: white; } QPushButton:hover { background-color: #219a52; }")
        self.edit_btn.setStyleSheet(button_style + "QPushButton { background-color: #3498db; color: white; } QPushButton:hover { background-color: #2980b9; }")
        self.delete_btn.setStyleSheet(button_style + "QPushButton { background-color: #e74c3c; color: white; } QPushButton:hover { background-color: #c0392b; }")
        control_layout.addWidget(self.add_btn)
        control_layout.addWidget(self.edit_btn)
        control_layout.addWidget(self.delete_btn)
        layout.addLayout(control_layout)
        self.materials_table = QTableWidget()
        self.materials_table.setColumnCount(4)
        self.materials_table.setHorizontalHeaderLabels(["Название", "Количество", "Ед.изм", "Стоимость за единицу"])
        header = self.materials_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        self.materials_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.materials_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.materials_table.setSelectionMode(QTableWidget.SingleSelection)
        self.materials_table.setStyleSheet("QTableWidget { border: 1px solid #bdc3c7; border-radius: 5px; gridline-color: #bdc3c7; background-color: white; } QTableWidget::item { padding: 10px; border-bottom: 1px solid #ecf0f1; selection-background-color: #d6eaf8; } QTableWidget::item:selected { background-color: #3498db; color: white; } QHeaderView::section { background-color: #34495e; color: white; font-weight: bold; padding: 10px; border: none; }")
        layout.addWidget(self.materials_table)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.back_btn = QPushButton("Главное меню")
        self.back_btn.setFixedSize(120, 40)
        self.back_btn.setStyleSheet("QPushButton { background-color: #3498db; color: white; border: none; border-radius: 5px; font-weight: bold; } QPushButton:hover { background-color: #2980b9; }")
        button_layout.addWidget(self.back_btn)
        layout.addLayout(button_layout)
        self.add_btn.clicked.connect(self.add_material)
        self.edit_btn.clicked.connect(self.edit_material)
        self.delete_btn.clicked.connect(self.delete_material)
        self.back_btn.clicked.connect(self.main_window.show_main_menu)

    def load_materials(self, search_text=""):
        try:
            materials = self.db.get_materials()
            if search_text:
                materials = [m for m in materials if search_text.lower() in m[1].lower()]
            self.materials_table.setRowCount(len(materials))
            for row, material in enumerate(materials):
                material_id, name, quantity, unit, cost = material
                item_name = QTableWidgetItem(name)
                item_quantity = QTableWidgetItem(str(quantity))
                item_unit = QTableWidgetItem(unit)
                item_cost = QTableWidgetItem(f"{cost} руб")
                item_name.setFlags(item_name.flags() & ~Qt.ItemIsEditable)
                item_quantity.setFlags(item_quantity.flags() & ~Qt.ItemIsEditable)
                item_unit.setFlags(item_unit.flags() & ~Qt.ItemIsEditable)
                item_cost.setFlags(item_cost.flags() & ~Qt.ItemIsEditable)
                self.materials_table.setItem(row, 0, item_name)
                self.materials_table.setItem(row, 1, item_quantity)
                self.materials_table.setItem(row, 2, item_unit)
                self.materials_table.setItem(row, 3, item_cost)
                item_name.setData(Qt.UserRole, material_id)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить материалы: {str(e)}")

    def search_materials(self):
        search_text = self.search_edit.text().strip()
        self.load_materials(search_text)

    def add_material(self):
        dialog = MaterialDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if not data['name']:
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
                return
            if not data['quantity'] or data['quantity'] <= 0:
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
                return
            if not data['unit']:
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
                return
            if not data['cost'] or data['cost'] <= 0:
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
                return
            if self.db.material_name_exists(data['name']):
                QMessageBox.warning(self, "Ошибка", "Материал с таким названием уже существует")
                return
            if self.db.add_material(data['name'], data['quantity'], data['unit'], data['cost']):
                self.load_materials()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить материал")

    def edit_material(self):
        current_row = self.materials_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите материал для редактирования")
            return
        material_id = self.materials_table.item(current_row, 0).data(Qt.UserRole)
        material_data = {'name': self.materials_table.item(current_row, 0).text(), 'quantity': float(self.materials_table.item(current_row, 1).text()), 'unit': self.materials_table.item(current_row, 2).text(), 'cost': float(self.materials_table.item(current_row, 3).text().replace(' руб', ''))}
        dialog = MaterialDialog(self, material_data)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if not data['name']:
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
                return
            if not data['quantity'] or data['quantity'] <= 0:
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
                return
            if not data['unit']:
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
                return
            if not data['cost'] or data['cost'] <= 0:
                QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
                return
            if self.db.material_name_exists(data['name'], material_id):
                QMessageBox.warning(self, "Ошибка", "Материал с таким названием уже существует")
                return
            if self.db.update_material(material_id, data['name'], data['quantity'], data['unit'], data['cost']):
                self.load_materials(self.search_edit.text().strip())
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось обновить материал")

    def delete_material(self):
        current_row = self.materials_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите материал для удаления")
            return
        material_name = self.materials_table.item(current_row, 0).text()
        material_id = self.materials_table.item(current_row, 0).data(Qt.UserRole)
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Подтверждение удаления")
        msg_box.setText(f"Удалить данный материал?")
        msg_box.setIcon(QMessageBox.Question)
        yes_button = msg_box.addButton("Да", QMessageBox.YesRole)
        no_button = msg_box.addButton("Нет", QMessageBox.NoRole)
        msg_box.setDefaultButton(no_button)
        msg_box.exec_()
        if msg_box.clickedButton() == yes_button:
            if self.db.delete_material(material_id):
                self.load_materials(self.search_edit.text().strip())
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить материал")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Автомойка - Главное меню")
        self.showFullScreen()
        self.db = Database()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.create_sidebar(main_layout)
        self.create_content_area(main_layout)
        self.load_daily_info()
        self.load_current_orders()

    def create_sidebar(self, main_layout):
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("QFrame { background-color: #2c3e50; border: none; }")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)
        self.new_order_btn = self.create_nav_button("Новый заказ")
        self.services_btn = self.create_nav_button("Услуги")
        self.reports_btn = self.create_nav_button("Отчеты")
        self.clients_btn = self.create_nav_button("Клиенты")
        self.materials_btn = self.create_nav_button("Материалы")
        self.employees_btn = self.create_nav_button("Сотрудники")
        sidebar_layout.addWidget(self.new_order_btn)
        sidebar_layout.addWidget(self.services_btn)
        sidebar_layout.addWidget(self.reports_btn)
        sidebar_layout.addWidget(self.clients_btn)
        sidebar_layout.addWidget(self.materials_btn)
        sidebar_layout.addWidget(self.employees_btn)
        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

    def create_nav_button(self, text):
        button = QPushButton(text)
        button.setFixedHeight(40)
        button.setStyleSheet("QPushButton { background-color: #34495e; color: white; border: none; border-radius: 5px; text-align: left; padding-left: 15px; font-weight: bold; } QPushButton:hover { background-color: #3498db; } QPushButton:pressed { background-color: #2980b9; }")
        if text == "Новый заказ":
            button.clicked.connect(self.open_new_order)
        elif text == "Услуги":
            button.clicked.connect(self.open_services)
        elif text == "Отчеты":
            button.clicked.connect(self.open_reports)
        elif text == "Клиенты":
            button.clicked.connect(self.open_clients)
        elif text == "Материалы":
            button.clicked.connect(self.open_materials)
        elif text == "Сотрудники":
            button.clicked.connect(self.open_employees)
        return button

    def create_content_area(self, main_layout):
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("QWidget { background-color: #ecf0f1; }")
        self.main_page = self.create_main_page()
        self.new_order_page = NewOrderWidget(self.db, self)
        self.employees_page = EmployeesWidget(self.db, self)
        self.services_page = ServicesWidget(self.db, self)
        self.materials_page = MaterialsWidget(self.db, self)
        self.clients_page = ClientsWidget(self.db, self)
        self.reports_page = ReportsWidget(self.db, self)
        self.content_stack.addWidget(self.main_page)
        self.content_stack.addWidget(self.new_order_page)
        self.content_stack.addWidget(self.employees_page)
        self.content_stack.addWidget(self.services_page)
        self.content_stack.addWidget(self.materials_page)
        self.content_stack.addWidget(self.clients_page)
        self.content_stack.addWidget(self.reports_page)
        main_layout.addWidget(self.content_stack)

    def create_main_page(self):
        main_widget = QWidget()
        content_layout = QVBoxLayout(main_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        title_label = QLabel("Сегодня:")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignLeft)
        content_layout.addWidget(title_label)
        self.create_daily_info(content_layout)
        self.create_orders_table(content_layout)
        return main_widget

    def create_daily_info(self, content_layout):
        info_frame = QFrame()
        info_frame.setStyleSheet("QFrame { background-color: white; border-radius: 8px; border: 2px solid #bdc3c7; }")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 15, 15, 15)
        info_layout.setSpacing(10)
        self.orders_count_label = QLabel("Кол-во выполненных заказов: 0")
        self.revenue_label = QLabel("Выручка: 0 руб")
        self.active_orders_label = QLabel("Кол-во активных заказов: 0")
        info_labels = [self.orders_count_label, self.revenue_label, self.active_orders_label]
        for label in info_labels:
            label.setAlignment(Qt.AlignLeft)
            label.setStyleSheet("QLabel { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 12px; font-weight: bold; font-size: 14px; color: #2c3e50; margin: 2px; }")
            label.setMinimumHeight(50)
            label.setMinimumWidth(300)
            info_layout.addWidget(label)
        content_layout.addWidget(info_frame)

    def create_orders_table(self, content_layout):
        table_frame = QFrame()
        table_frame.setStyleSheet("QFrame { background-color: white; border-radius: 8px; border: 2px solid #bdc3c7; }")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(15, 15, 15, 15)
        table_label = QLabel("Текущие заказы")
        table_label.setFont(QFont("Arial", 12, QFont.Bold))
        table_label.setStyleSheet("color: #2c3e50;")
        table_layout.addWidget(table_label)
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(5)
        self.orders_table.setHorizontalHeaderLabels(["№ заказа", "Гос.номер", "Услуги", "Статус", "Клиент"])
        header = self.orders_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        self.orders_table.setColumnWidth(0, 80)
        self.orders_table.setColumnWidth(1, 100)
        self.orders_table.setColumnWidth(3, 150)
        self.orders_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.orders_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.orders_table.setSelectionMode(QTableWidget.SingleSelection)
        self.orders_table.setStyleSheet("QTableWidget { border: 1px solid #bdc3c7; border-radius: 5px; gridline-color: #bdc3c7; background-color: white; } QTableWidget::item { padding: 15px; border-bottom: 1px solid #ecf0f1; selection-background-color: #d6eaf8; } QTableWidget::item:selected { background-color: #3498db; color: white; } QHeaderView::section { background-color: #34495e; color: white; font-weight: bold; padding: 12px; border: none; }")
        table_layout.addWidget(self.orders_table)
        content_layout.addWidget(table_frame)

    def load_daily_info(self):
        try:
            daily_info = self.db.get_daily_info()
            self.orders_count_label.setText(f"Кол-во выполненных заказов: {daily_info['orders_count']}")
            self.revenue_label.setText(f"Выручка: {daily_info['revenue']} руб")
            self.active_orders_label.setText(f"Кол-во активных заказов: {daily_info['active_orders']}")
        except Exception as e:
            print(f"Ошибка загрузки daily info: {e}")

    def load_current_orders(self):
        try:
            orders = self.db.get_current_orders()
            self.orders_table.setRowCount(len(orders))
            for row, order in enumerate(orders):
                order_number, license_plate, services, status, client_name, order_id = order
                item_order_number = QTableWidgetItem(str(order_number))
                item_order_number.setFlags(item_order_number.flags() & ~Qt.ItemIsEditable)
                item_order_number.setTextAlignment(Qt.AlignCenter)
                self.orders_table.setItem(row, 0, item_order_number)
                item_license_plate = QTableWidgetItem(license_plate if license_plate else "")
                item_license_plate.setFlags(item_license_plate.flags() & ~Qt.ItemIsEditable)
                item_license_plate.setTextAlignment(Qt.AlignCenter)
                self.orders_table.setItem(row, 1, item_license_plate)
                services_display = services if services else "Услуги не указаны"
                item_services = QTableWidgetItem(services_display)
                item_services.setFlags(item_services.flags() & ~Qt.ItemIsEditable)
                self.orders_table.setItem(row, 2, item_services)
                status_combo = QComboBox()
                status_combo.addItems(["В процессе", "Готово"])
                status_combo.setCurrentText(status if status else "В процессе")
                status_combo.currentTextChanged.connect(lambda text, order_id=order_id: self.update_order_status(order_id, text))
                status_combo.setStyleSheet("QComboBox { padding: 8px; border: 1px solid #bdc3c7; border-radius: 4px; background-color: white; min-width: 120px; } QComboBox::drop-down { border: none; } QComboBox::down-arrow { width: 12px; height: 12px; }")
                self.orders_table.setCellWidget(row, 3, status_combo)
                client_display = client_name if client_name else "Клиент не указан"
                item_client = QTableWidgetItem(client_display)
                item_client.setFlags(item_client.flags() & ~Qt.ItemIsEditable)
                self.orders_table.setItem(row, 4, item_client)
                self.orders_table.setRowHeight(row, 70)
        except Exception as e:
            print(f"Ошибка загрузки orders: {e}")

    def update_order_status(self, order_id, new_status):
        try:
            self.db.cursor.execute("SELECT order_number FROM orders WHERE id = ?", (order_id,))
            result = self.db.cursor.fetchone()
            if not result:
                return False
            order_number = result[0]
            self.db.cursor.execute("UPDATE orders SET status = ? WHERE order_number = ?", (new_status, order_number))
            self.db.conn.commit()
            self.update_employee_statuses()
            self.load_daily_info()
            self.load_current_orders()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка обновления статуса заказа: {e}")
            self.db.conn.rollback()
            return False

    def update_employee_statuses(self):
        if hasattr(self, 'employees_page'):
            self.employees_page.load_employees()
        if hasattr(self, 'new_order_page'):
            self.new_order_page.load_employees()

    def show_main_menu(self):
        self.content_stack.setCurrentWidget(self.main_page)

    def open_employees(self):
        self.content_stack.setCurrentWidget(self.employees_page)
        self.employees_page.load_employees()

    def open_services(self):
        self.content_stack.setCurrentWidget(self.services_page)
        self.services_page.load_services()

    def open_materials(self):
        self.content_stack.setCurrentWidget(self.materials_page)
        self.materials_page.load_materials()

    def open_clients(self):
        self.content_stack.setCurrentWidget(self.clients_page)
        self.clients_page.load_clients()

    def open_new_order(self):
        self.content_stack.setCurrentWidget(self.new_order_page)

    def open_reports(self):
        self.content_stack.setCurrentWidget(self.reports_page)

    def closeEvent(self, event):
        self.db.disconnect()
        event.accept()