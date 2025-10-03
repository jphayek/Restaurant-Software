# type: ignore
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
print(A4)
import db

# Impression PDF
def print_bill_pdf(order_id):
    conn = db.get_connection()
    cursor = conn.cursor()

    # Récupérer infos commande
    cursor.execute("SELECT table_id FROM orders WHERE id=?", (order_id,))
    table_id = cursor.fetchone()[0]

    cursor.execute("""
        SELECT item, quantity, notes 
        FROM order_items 
        WHERE order_id=?
    """, (order_id,))
    items = cursor.fetchall()

    # Exemple de prix fictifs (à remplacer par mon menu en DB plus tard)
    total = 0
    prix_plat = 10
    prix_boisson = 3
    for item, qty, notes in items:
        if "coca" in item.lower() or "boisson" in item.lower():
            total += int(qty) * prix_boisson
        else:
            total += int(qty) * prix_plat

    # Génération PDF
    filename = f"facture_{order_id}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, 800, "Restaurant Software by Jp")
    c.setFont("Helvetica", 10)
    c.drawString(50, 770, f"Table : {table_id}")
    c.drawString(50, 755, f"Commande n° {order_id}")
    c.drawString(50, 740, "-"*50)

    y = 720
    for item, qty, notes in items:
        line = f"{item} x{qty} ({notes if notes else ''})"
        c.drawString(50, y, line)
        y -= 20

    c.drawString(50, y-10, "-"*50)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y-40, f"TOTAL : {total} €")

    c.save()
    conn.close()
    return filename


# Impression directe sur imprimante thermique (ESC/POS)
def print_bill_thermal(order_id, usb_ids=(0x04b8, 0x0e15)):
    """
    usb_ids = (vendor_id, product_id) de ton imprimante USB
    Exemple : (0x04b8, 0x0e15) pour Epson TM-T20II
    """
    try:
        from escpos.printer import Usb
    except ImportError:
        raise ImportError("⚠️ Installe python-escpos : pip install python-escpos")

    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT table_id FROM orders WHERE id=?", (order_id,))
    table_id = cursor.fetchone()[0]

    cursor.execute("""
        SELECT item, quantity, notes 
        FROM order_items 
        WHERE order_id=?
    """, (order_id,))
    items = cursor.fetchall()
    conn.close()

    # Connexion à l’imprimante
    p = Usb(usb_ids[0], usb_ids[1])

    p.set(align="center", bold=True)
    p.text("Restaurant Chez Toi\n")
    p.text("--------------------------\n")
    p.set(align="left", bold=False)

    p.text(f"Table : {table_id}\n")
    p.text(f"Commande n°{order_id}\n")
    p.text("--------------------------\n")

    for item, qty, notes in items:
        line = f"{item} x{qty}"
        if notes:
            line += f" ({notes})"
        p.text(line + "\n")

    p.text("--------------------------\n")
    p.set(align="center", bold=True)
