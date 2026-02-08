import sqlite3
from datetime import datetime
import locale

class DatabaseManager:
    def __init__(self):
        self.connection = sqlite3.connect('ventes.db')
        self.cursor = self.connection.cursor()
        self.creer_table()
        
        try:
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_TIME, 'French_France.1252')
            except:
                pass
    
    def creer_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_produit TEXT NOT NULL,
                quantite INTEGER NOT NULL,
                prix_unitaire REAL NOT NULL,
                prix_total REAL NOT NULL,
                date_vente TEXT NOT NULL
            )
        ''')
        self.connection.commit()
    
    def ajouter_vente(self, nom_produit, quantite, prix_unitaire):
        prix_total = quantite * prix_unitaire
        date_vente = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        self.cursor.execute('''
            INSERT INTO ventes (nom_produit, quantite, prix_unitaire, prix_total, date_vente)
            VALUES (?, ?, ?, ?, ?)
        ''', (nom_produit, quantite, prix_unitaire, prix_total, date_vente))
        
        self.connection.commit()
        return prix_total
    
    def obtenir_ventes(self):
        self.cursor.execute('SELECT * FROM ventes ORDER BY id DESC')
        return self.cursor.fetchall()
    
    def supprimer_vente(self, vente_id):
        self.cursor.execute('DELETE FROM ventes WHERE id = ?', (vente_id,))
        self.connection.commit()
    
    def obtenir_statistiques(self):
        self.cursor.execute('SELECT SUM(prix_total), COUNT(*) FROM ventes')
        total, nombre = self.cursor.fetchone()
        return total or 0, nombre or 0
    
    def fermer(self):
        self.connection.close()