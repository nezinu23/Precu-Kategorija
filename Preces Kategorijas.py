
import sqlite3


conn = sqlite3.connect("veikals.db")
cursor = conn.cursor()


cursor.execute("PRAGMA foreign_keys = ON")


cursor.execute("""
CREATE TABLE IF NOT EXISTS kategorijas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nosaukums TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS preces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nosaukums TEXT,
    cena REAL,
    kategorija_id INTEGER,
    FOREIGN KEY (kategorija_id) REFERENCES kategorijas(id)
)
""")


cursor.execute("DELETE FROM preces")
cursor.execute("DELETE FROM kategorijas")


cursor.execute("INSERT INTO kategorijas (nosaukums) VALUES ('Partika')")
cursor.execute("INSERT INTO kategorijas (nosaukums) VALUES ('Elektronika')")
cursor.execute("INSERT INTO kategorijas (nosaukums) VALUES ('Apgerbi')")


cursor.execute("SELECT id FROM kategorijas WHERE nosaukums = 'Partika'")
partika = cursor.fetchone()[0]

cursor.execute("SELECT id FROM kategorijas WHERE nosaukums = 'Elektronika'")
elektronika = cursor.fetchone()[0]

cursor.execute("SELECT id FROM kategorijas WHERE nosaukums = 'Apgerbi'")
apgerbi = cursor.fetchone()[0]


cursor.execute(
    "INSERT INTO preces (nosaukums, cena, kategorija_id) VALUES (?, ?, ?)",
    ("Piens", 1.29, partika)
)

cursor.execute(
    "INSERT INTO preces (nosaukums, cena, kategorija_id) VALUES (?, ?, ?)",
    ("Maize", 1.50, partika)
)

cursor.execute(
    "INSERT INTO preces (nosaukums, cena, kategorija_id) VALUES (?, ?, ?)",
    ("Siers", 3.20, partika)
)

cursor.execute(
    "INSERT INTO preces (nosaukums, cena, kategorija_id) VALUES (?, ?, ?)",
    ("Telefons", 399.00, elektronika)
)

cursor.execute(
    "INSERT INTO preces (nosaukums, cena, kategorija_id) VALUES (?, ?, ?)",
    ("Krekls", 15.99, apgerbi)
)

conn.commit()


cursor.execute("""
UPDATE preces
SET cena = 349.00
WHERE nosaukums = 'Telefons'
""")

conn.commit()


cursor.execute("""
DELETE FROM preces
WHERE nosaukums = 'Siers'
""")

conn.commit()


print("VEIKALA PRECES")
print("-----------------------------")

cursor.execute("""
SELECT preces.nosaukums, kategorijas.nosaukums, preces.cena
FROM preces
JOIN kategorijas
ON preces.kategorija_id = kategorijas.id
""")

preces = cursor.fetchall()

for prece in preces:
    print(prece[0], "|", prece[1], "|", format(prece[2], ".2f"), "EUR")


print("-----------------------------")
print("KATEGORIJAS")

cursor.execute("SELECT * FROM kategorijas")
kategorijas = cursor.fetchall()

for kategorija in kategorijas:
    print(kategorija[0], "-", kategorija[1])

print("PARBAUDE")

cursor.execute("SELECT COUNT(*) FROM kategorijas")
print("Kategoriju skaits:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM preces")
print("Precu skaits:", cursor.fetchone()[0])

cursor.execute("PRAGMA foreign_key_check")
print("Arējo atslegu kludas:", cursor.fetchall())

conn.close()

print("-----------------------------")
print("Preces Kategorija pabeigta!")
