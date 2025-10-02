import sqlite3

def get_connection():
    return sqlite3.connect("restaurant.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Utilisateurs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # Tables du resto
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number INTEGER
    )
    """)

    # Commandes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_id INTEGER,
        status TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(table_id) REFERENCES tables(id)
    )
    """)

    # Détails commande
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        item TEXT,
        quantity INTEGER,
        notes TEXT,
        FOREIGN KEY(order_id) REFERENCES orders(id)
    )
    """)

    # Paiements
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        total REAL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(order_id) REFERENCES orders(id)
    )
    """)

    conn.commit()
    conn.close()

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    ########## Comptes fictifs ##########
    users = [
        ("admin", "admin123", "admin"),
        ("serveur1", "pass123", "serveur"),
        ("cuisinier1", "cook123", "cuisinier"),
        ("barman1", "bar123", "barman"),
    ]
    for username, password, role in users:
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                           (username, password, role))
        except sqlite3.IntegrityError:
            pass  # déjà existant

    ########## Tables du restaurant (1 à 5) ##########
    for i in range(1, 6):
        try:
            cursor.execute("INSERT INTO tables (number) VALUES (?)", (i,))
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()
    print("✅ Données fictives ajoutées avec succès")

if __name__ == "__main__":
    init_db()
    seed_data()
