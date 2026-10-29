
import sqlite3


# Connect to the database
connection = sqlite3.connect("sales.db")

cursor = connection.cursor()


# Create the sales table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    order_id INTEGER PRIMARY KEY,
    product TEXT,
    city TEXT,
    revenue REAL
)
""")


# Insert sample data
sales_data = [
    (1, "Laptop", "Cork", 1200),
    (2, "Phone", "Dublin", 800),
    (3, "Tablet", "Cork", 300),
    (4, "Laptop", "Dublin", 1500),
    (5, "Phone", "Cork", 450),
    (6, "Tablet", "Limerick", 250),
    (7, "Laptop", "Limerick", 1300),
    (8, "Phone", "Dublin", 650),
    (9, "Tablet", "Dublin", 400),
    (10, "Laptop", "Cork", 1100),
]

cursor.executemany("""
INSERT OR IGNORE INTO sales
(order_id, product, city, revenue)
VALUES (?, ?, ?, ?)
""", sales_data)

connection.commit()


# Display all sales
print("===== ALL SALES =====")

cursor.execute("SELECT * FROM sales")
for row in cursor.fetchall():
    print(row)


# Calculate total revenue
print("\n===== TOTAL REVENUE =====")

cursor.execute("SELECT SUM(revenue) FROM sales")
print(f"Total revenue: €{cursor.fetchone()[0]:.2f}")


# Revenue by city
print("\n===== REVENUE BY CITY =====")

cursor.execute("""
SELECT city, SUM(revenue)
FROM sales
GROUP BY city
ORDER BY SUM(revenue) DESC
""")

for row in cursor.fetchall():
    print(f"{row[0]}: €{row[1]:.2f}")


# Revenue by product
print("\n===== REVENUE BY PRODUCT =====")

cursor.execute("""
SELECT product, SUM(revenue)
FROM sales
GROUP BY product
ORDER BY SUM(revenue) DESC
""")

for row in cursor.fetchall():
    print(f"{row[0]}: €{row[1]:.2f}")


# Find orders above €500
print("\n===== HIGH-VALUE ORDERS =====")

cursor.execute("""
SELECT order_id, product, city, revenue
FROM sales
WHERE revenue > 500
ORDER BY revenue DESC
""")

for row in cursor.fetchall():
    print(row)


# Find the highest-value order
print("\n===== HIGHEST-VALUE ORDER =====")

cursor.execute("""
SELECT product, city, revenue
FROM sales
ORDER BY revenue DESC
LIMIT 1
""")

print(cursor.fetchone())


# Close the database connection
connection.close()
