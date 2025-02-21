import mysql.connector as con

connection = con.connect(host='192.168.56.103',
                         user='root',
                         password='changeme',
                         database='new_schema')

cursor = connection.cursor()

products_tb = ''' CREATE TABLE IF NOT EXISTS products(
                product_id SERIAL PRIMARY KEY,
                product_nm VARCHAR(255) NOT NULL,
                price DECIMAL(10,2),
                stock_quantity INT);
            '''

cursor.execute(products_tb)
connection.commit()

cursor.close()
connection.close()