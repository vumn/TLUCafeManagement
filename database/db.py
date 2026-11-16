import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.config = { 
            "host":"localhost",
            "user":"root",
            "password":"123456789",
            "database":"tlucafe_db",
            "port":3306,
            "charset":"utf8mb4"
        }
    def get_connection(self):
        try:
            conn = mysql.connector.connect(**self.config)
            if conn.is_connected():
                return conn
        except Error as e:
            print(f"Loi ket noi DB: {e}")
        return None
    
    def fetch_all(self, query, params=None):
        conn = self.get_connecttion()
        if not conn:
            return []
        results =  []
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            results = cursor.fetchall()
        except Error as e:
            print(f"Loi khi fetch_all: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()
        return results
    
    def fetch_one(self, query, params=None):
        conn = self.get_connecttion()
        if not conn:
            return None
        result = None
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchone()
        except Error as e:
            print(f"Loi khi fetch_one: {e}")
        finally:
            if cursor:
                cursor.close()
            conn.close()
        return result
    
    def execute_query(self, query, params=None):
        conn = self.get_connecttion()
        if not conn:
            return None
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
        except Error as e:
            conn.rollback()
            print(f"Loi khi execute_query: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            conn.close()
    
    def create_order_transaction(self, user_id, total_amount, cart_items):
        conn = self.get_connecttion()
        if not conn:
            return False, "Khong the ket noi DB"
        cursor = None
        try: 
            cursor = conn.cursor(dictionary=True)
            conn.start_transaction()

            # 1. tao ban ghi trong bang orders
            sql_insert_order = "INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)"
            cursor.execute(sql_insert_order, (user_id, total_amount))
            order_id = cursor.lastrowid

            # 2. duyet tung item trong gio hang
            for item in cart_items:
                p_id = item["product_id"]
                qty = item["quantity"]
                price = item["unit_price"]

                # check thong tin item
                sql_check = """
                    SELECT product_name, product_type, stock_quantity, status
                    FROM products WHERE product_id = %s FOR UPDATE
                """
                cursor.execute(sql_check, (p_id))
                product = cursor.fetchone()

                if not product or product["status"] == 0:
                    raise ValueError(
                        f"'{product['product_name'] if product else p_id}' het hang"
                    )
                if product["product_type"] == "packaged":
                    current_stock = product["stock_quantity"] or 0
                    if current_stock < qty:
                        raise ValueError(
                            f"'{product['product_name']} : {current_stock}'"
                        )
                    new_stock = current_stock - qty
                    new_status = 1 if new_stock > 0 else 0

                    sql_update_stock = """
                        UPDATE products
                        SET stock_quantity = %s, status = %s
                        WHERE product_id = %s
                    """
                    cursor.execute(sql_update_stock, (new_stock, new_status, p_id))
                
                # 3. luu vao order details
                sql_insert_detail = """
                    INSERT INTO order_details (order_id, product_id, quantity, unit_price)
                """
                cursor.execute(sql_insert_detail, (order_id, p_id, qty, price))
            
            conn.commit()
            return True, order_id

        except ValueError as ve:
            conn.rollback()
            return False, str(ve)
        except Error as e:
            conn.rollback()
            return False, f"Loi DB khi tao don: {e}"
        finally:
            if cursor:
                cursor.close()
            conn.close()

db = Database()

if __name__ == "__main__":
    sql = """
        SELECT p.product_id, p.product_name, c.category_name, 
               p.product_type, p.price, p.stock_quantity, p.status
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
    """
    items = db.fetch_all(sql)
    for item in items:
        loai = "Tự chế biến" if item["product_type"] == "homemade" else f"Đóng gói (Tồn: {item['stock_quantity']})"
        trang_thai = "Còn hàng" if item["status"] == 1 else "Hết hàng"
        print(f"- [{item['product_id']}] {item['product_name']} | {loai} | {item['price']:,.0f}đ | {trang_thai}")