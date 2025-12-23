import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='car_wash.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.init_db()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def init_db(self):
        try:
            tables = {
                'services': 'CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, price REAL NOT NULL)',
                'materials': 'CREATE TABLE IF NOT EXISTS materials (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, quantity REAL NOT NULL, unit TEXT NOT NULL, cost REAL NOT NULL)',
                'service_materials': 'CREATE TABLE IF NOT EXISTS service_materials (service_id INTEGER, material_id INTEGER, quantity_required REAL NOT NULL, PRIMARY KEY (service_id, material_id), FOREIGN KEY (service_id) REFERENCES services (id) ON DELETE CASCADE, FOREIGN KEY (material_id) REFERENCES materials (id) ON DELETE CASCADE)',
                'clients': 'CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT NOT NULL, phone TEXT)',
                'client_cars': 'CREATE TABLE IF NOT EXISTS client_cars (id INTEGER PRIMARY KEY AUTOINCREMENT, client_id INTEGER, license_plate TEXT NOT NULL, car_model TEXT, FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE)',
                'employees': 'CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT NOT NULL, position TEXT NOT NULL, phone TEXT NOT NULL UNIQUE)',
                'orders': 'CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, order_number INTEGER, license_plate TEXT, service_id INTEGER, status TEXT, client_id INTEGER, employee_id INTEGER, created_date TEXT, materials_consumed BOOLEAN DEFAULT 0, FOREIGN KEY (service_id) REFERENCES services (id), FOREIGN KEY (client_id) REFERENCES clients (id), FOREIGN KEY (employee_id) REFERENCES employees (id))'
            }
            for table_name, create_sql in tables.items():
                self.cursor.execute(create_sql)

            self.cursor.execute("PRAGMA table_info(orders)")
            columns = [column[1] for column in self.cursor.fetchall()]
            if 'employee_id' not in columns:
                self.cursor.execute("ALTER TABLE orders ADD COLUMN employee_id INTEGER")
            if 'materials_consumed' not in columns:
                self.cursor.execute("ALTER TABLE orders ADD COLUMN materials_consumed BOOLEAN DEFAULT 0")

            self.cursor.execute("PRAGMA table_info(clients)")
            client_columns = [column[1] for column in self.cursor.fetchall()]
            if 'phone' not in client_columns:
                self.cursor.execute("ALTER TABLE clients ADD COLUMN phone TEXT")

            if 'order_number' in columns:
                self.cursor.execute("PRAGMA table_info(orders)")
                column_info = self.cursor.fetchall()
                for col in column_info:
                    if col[1] == 'order_number' and col[2] == 'TEXT':
                        self.cursor.execute('CREATE TABLE orders_temp (id INTEGER PRIMARY KEY AUTOINCREMENT, order_number INTEGER, license_plate TEXT, service_id INTEGER, status TEXT, client_id INTEGER, employee_id INTEGER, created_date TEXT, materials_consumed BOOLEAN DEFAULT 0)')
                        self.cursor.execute('INSERT INTO orders_temp SELECT id, CAST(order_number AS INTEGER), license_plate, service_id, status, client_id, employee_id, created_date, materials_consumed FROM orders')
                        self.cursor.execute("DROP TABLE orders")
                        self.cursor.execute("ALTER TABLE orders_temp RENAME TO orders")

            self.conn.commit()
        except Exception as e:
            print(f"Ошибка инициализации БД: {e}")
            self.conn.rollback()

    def get_next_order_number(self):
        try:
            self.cursor.execute("SELECT MAX(order_number) FROM orders")
            result = self.cursor.fetchone()[0]
            return int(result) + 1 if result else 1
        except Exception as e:
            print(f"Ошибка получения номера заказа: {e}")
            return 1

    def service_name_exists(self, name, exclude_id=None):
        try:
            if exclude_id:
                self.cursor.execute("SELECT id FROM services WHERE name = ? AND id != ?", (name, exclude_id))
            else:
                self.cursor.execute("SELECT id FROM services WHERE name = ?", (name,))
            return self.cursor.fetchone() is not None
        except Exception as e:
            print(f"Ошибка проверки названия услуги: {e}")
            return False

    def material_name_exists(self, name, exclude_id=None):
        try:
            if exclude_id:
                self.cursor.execute("SELECT id FROM materials WHERE name = ? AND id != ?", (name, exclude_id))
            else:
                self.cursor.execute("SELECT id FROM materials WHERE name = ?", (name,))
            return self.cursor.fetchone() is not None
        except Exception as e:
            print(f"Ошибка проверки названия материала: {e}")
            return False

    def get_clients_with_stats(self, search_text=""):
        try:
            query = '''
                SELECT 
                    c.id,
                    c.phone,
                    c.full_name,
                    (SELECT GROUP_CONCAT(DISTINCT cc.license_plate) 
                     FROM client_cars cc 
                     WHERE cc.client_id = c.id) as license_plates,
                    (SELECT MAX(o.created_date) FROM orders o 
                     WHERE o.client_id = c.id) as last_visit,
                    (SELECT COUNT(DISTINCT o.order_number) FROM orders o 
                     WHERE o.client_id = c.id) as orders_count
                FROM clients c
            '''
            if search_text:
                query += " WHERE c.full_name LIKE ? OR c.phone LIKE ?"
                self.cursor.execute(query, (f'%{search_text}%', f'%{search_text}%'))
            else:
                self.cursor.execute(query)

            clients_data = self.cursor.fetchall()
            formatted_clients = []
            for client in clients_data:
                client_id, phone, full_name, license_plates, last_visit, orders_count = client
                if last_visit:
                    try:
                        last_visit_dt = datetime.strptime(last_visit, '%Y-%m-%d %H:%M:%S')
                        formatted_last_visit = last_visit_dt.strftime('%d.%m.%Y %H:%M')
                    except:
                        formatted_last_visit = last_visit
                else:
                    formatted_last_visit = "Нет визитов"
                orders_display = str(orders_count) if orders_count else "0"
                phones_display = phone if phone else ""
                license_plates_display = license_plates if license_plates else ""
                formatted_clients.append((
                    client_id, phones_display, full_name, license_plates_display,
                    formatted_last_visit, orders_display
                ))
            return formatted_clients
        except Exception as e:
            print(f"Ошибка получения клиентов: {e}")
            return []

    def get_client_cars(self, client_id):
        try:
            self.cursor.execute("SELECT license_plate, car_model FROM client_cars WHERE client_id = ?", (client_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Ошибка получения автомобилей клиента: {e}")
            return []

    def add_client_car(self, client_id, license_plate, car_model=""):
        try:
            self.cursor.execute("SELECT id FROM client_cars WHERE client_id = ? AND license_plate = ?", (client_id, license_plate))
            if self.cursor.fetchone():
                return True
            self.cursor.execute("INSERT INTO client_cars (client_id, license_plate, car_model) VALUES (?, ?, ?)", (client_id, license_plate, car_model))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка добавления автомобиля клиенту: {e}")
            self.conn.rollback()
            return False

    def get_or_create_client(self, full_name, phone=""):
        try:
            if phone:
                self.cursor.execute("SELECT id FROM clients WHERE full_name = ? AND phone = ?", (full_name, phone))
                result = self.cursor.fetchone()
            else:
                self.cursor.execute("SELECT id FROM clients WHERE full_name = ?", (full_name,))
                result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                self.cursor.execute("INSERT INTO clients (full_name, phone) VALUES (?, ?)", (full_name, phone))
                self.conn.commit()
                return self.cursor.lastrowid
        except Exception as e:
            print(f"Ошибка при работе с клиентом: {e}")
            raise

    def update_client_phone(self, client_id, phone):
        try:
            self.cursor.execute("UPDATE clients SET phone = ? WHERE id = ?", (phone, client_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка обновления телефона клиента: {e}")
            return False

    def get_daily_info(self):
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute('SELECT COUNT(DISTINCT order_number) FROM orders WHERE status = "Готово" AND created_date LIKE ?', (f'{today}%',))
            completed_orders = self.cursor.fetchone()[0]
            self.cursor.execute('SELECT SUM(s.price) FROM orders o JOIN services s ON o.service_id = s.id WHERE o.status = "Готово" AND o.created_date LIKE ?', (f'{today}%',))
            revenue_result = self.cursor.fetchone()[0]
            revenue = revenue_result if revenue_result else 0
            self.cursor.execute('SELECT COUNT(DISTINCT order_number) FROM orders WHERE status != "Готово" AND created_date LIKE ?', (f'{today}%',))
            active_orders = self.cursor.fetchone()[0]
            return {'orders_count': completed_orders, 'revenue': revenue, 'active_orders': active_orders}
        except Exception as e:
            print(f"Ошибка получения daily info: {e}")
            return {'orders_count': 0, 'revenue': 0, 'active_orders': 0}

    def get_current_orders(self):
        try:
            self.cursor.execute('SELECT o.order_number, o.license_plate, GROUP_CONCAT(s.name, ", ") as services, o.status, c.full_name, o.id FROM orders o LEFT JOIN services s ON o.service_id = s.id LEFT JOIN clients c ON o.client_id = c.id WHERE o.status != "Готово" GROUP BY o.order_number, o.license_plate, o.status, c.full_name ORDER BY o.order_number DESC')
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Ошибка получения заказов: {e}")
            return []

    def update_order_status(self, order_id, new_status):
        try:
            self.cursor.execute("SELECT order_number FROM orders WHERE id = ?", (order_id,))
            result = self.cursor.fetchone()
            if not result:
                return False
            order_number = result[0]
            self.cursor.execute("UPDATE orders SET status = ? WHERE order_number = ?", (new_status, order_number))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка обновления статуса заказа: {e}")
            self.conn.rollback()
            return False

    def get_services(self):
        try:
            self.cursor.execute("SELECT id, name, price FROM services")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Ошибка получения услуг: {e}")
            return []

    def add_service(self, name, price):
        try:
            if not name or not name.strip():
                return False, "Название услуги не может быть пустым"
            try:
                price_float = float(price)
                if price_float <= 0:
                    return False, "Цена должна быть больше 0"
            except (ValueError, TypeError):
                return False, "Некорректное значение цены"
            self.cursor.execute("INSERT INTO services (name, price) VALUES (?, ?)", (name.strip(), price_float))
            self.conn.commit()
            return True, "Услуга успешно добавлена"
        except sqlite3.IntegrityError:
            return False, "Услуга с таким названием уже существует"
        except sqlite3.Error as e:
            print(f"Ошибка добавления услуги: {e}")
            self.conn.rollback()
            return False, f"Ошибка базы данных: {e}"
        except Exception as e:
            print(f"Ошибка добавления услуги: {e}")
            return False, f"Ошибка: {e}"

    def update_service(self, service_id, name, price):
        try:
            self.cursor.execute("UPDATE services SET name=?, price=? WHERE id=?", (name, price, service_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except sqlite3.Error as e:
            print(f"Ошибка обновления услуги: {e}")
            return False

    def delete_service(self, service_id):
        try:
            self.cursor.execute("DELETE FROM services WHERE id=?", (service_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка удаления услуги: {e}")
            return False

    def get_materials(self):
        try:
            self.cursor.execute("SELECT id, name, quantity, unit, cost FROM materials")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Ошибка получения материалов: {e}")
            return []

    def add_material(self, name, quantity, unit, cost):
        try:
            self.cursor.execute("INSERT INTO materials (name, quantity, unit, cost) VALUES (?, ?, ?, ?)", (name, quantity, unit, cost))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except sqlite3.Error as e:
            print(f"Ошибка добавления материала: {e}")
            return False

    def update_material(self, material_id, name, quantity, unit, cost):
        try:
            self.cursor.execute("UPDATE materials SET name=?, quantity=?, unit=?, cost=? WHERE id=?", (name, quantity, unit, cost, material_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except sqlite3.Error as e:
            print(f"Ошибка обновления материала: {e}")
            return False

    def delete_material(self, material_id):
        try:
            self.cursor.execute("DELETE FROM materials WHERE id=?", (material_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка удаления материала: {e}")
            return False

    def get_service_materials(self, service_id):
        try:
            self.cursor.execute('SELECT m.id, m.name, sm.quantity_required, m.quantity, m.unit FROM service_materials sm JOIN materials m ON sm.material_id = m.id WHERE sm.service_id = ?', (service_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Ошибка получения материалов услуги: {e}")
            return []

    def add_service_material(self, service_id, material_id, quantity_required):
        try:
            self.cursor.execute('INSERT INTO service_materials (service_id, material_id, quantity_required) VALUES (?, ?, ?)', (service_id, material_id, quantity_required))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка добавления материала к услуге: {e}")
            return False

    def remove_service_material(self, service_id, material_id):
        try:
            self.cursor.execute('DELETE FROM service_materials WHERE service_id = ? AND material_id = ?', (service_id, material_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка удаления материала из услуги: {e}")
            return False

    def consume_materials_for_service(self, service_id):
        try:
            service_materials = self.get_service_materials(service_id)
            if not service_materials:
                return True
            for material in service_materials:
                material_id, material_name, quantity_required, current_quantity, unit = material
                if current_quantity < quantity_required:
                    return False
            for material in service_materials:
                material_id, material_name, quantity_required, current_quantity, unit = material
                new_quantity = current_quantity - quantity_required
                self.cursor.execute("UPDATE materials SET quantity = ? WHERE id = ?", (new_quantity, material_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при списании материалов: {e}")
            self.conn.rollback()
            return False

    def check_materials_availability(self, service_id):
        try:
            service_materials = self.get_service_materials(service_id)
            if not service_materials:
                return True, []
            missing_materials = []
            for material in service_materials:
                material_id, material_name, quantity_required, current_quantity, unit = material
                if current_quantity < quantity_required:
                    missing_materials.append({'name': material_name, 'required': quantity_required, 'available': current_quantity, 'unit': unit})
            return len(missing_materials) == 0, missing_materials
        except Exception as e:
            print(f"Ошибка проверки доступности материалов: {e}")
            return False, []

    def get_financial_report(self, start_date, end_date):
        try:
            revenue_query = '''
                SELECT SUM(s.price) as revenue
                FROM orders o
                JOIN services s ON o.service_id = s.id
                WHERE o.status = "Готово" 
                AND o.created_date BETWEEN ? AND ?
            '''
            self.cursor.execute(revenue_query, (start_date, end_date))
            revenue_result = self.cursor.fetchone()
            revenue = revenue_result[0] if revenue_result[0] else 0

            material_costs_query = '''
                SELECT SUM(m.cost * sm.quantity_required) as material_costs
                FROM orders o
                JOIN services s ON o.service_id = s.id
                JOIN service_materials sm ON s.id = sm.service_id
                JOIN materials m ON sm.material_id = m.id
                WHERE o.status = "Готово" 
                AND o.created_date BETWEEN ? AND ?
            '''
            self.cursor.execute(material_costs_query, (start_date, end_date))
            material_costs_result = self.cursor.fetchone()
            material_costs = material_costs_result[0] if material_costs_result[0] else 0

            profit = revenue - material_costs

            return {
                'revenue': revenue,
                'material_costs': material_costs,
                'profit': profit
            }
        except Exception as e:
            print(f"Ошибка получения финансового отчета: {e}")
            return {'revenue': 0, 'material_costs': 0, 'profit': 0}

    def get_popular_services(self, start_date, end_date):
        try:
            query = '''
                SELECT s.name, COUNT(o.id) as order_count
                FROM orders o
                JOIN services s ON o.service_id = s.id
                WHERE o.status = "Готово" 
                AND o.created_date BETWEEN ? AND ?
                GROUP BY s.name
                ORDER BY order_count DESC
                LIMIT 3
            '''
            self.cursor.execute(query, (start_date, end_date))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Ошибка получения популярных услуг: {e}")
            return []