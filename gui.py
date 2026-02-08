import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager
from PIL import Image, ImageTk
import os

class ApplicationVentes:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Ventes")
        self.root.geometry("950x600")
        self.root.resizable(False, False)
        
        self.charger_logo()
        
        self.db = DatabaseManager()
        
        self.creer_interface()
        self.actualiser_liste()
        self.actualiser_statistiques()
    
    def charger_logo(self):
        try:
            logo_path = os.path.join('assets', 'logo.png')
            if os.path.exists(logo_path):
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((32, 32), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_image)
                self.root.iconphoto(True, self.logo_photo)
            else:
                self.logo_photo = None
        except Exception as e:
            print(f"Erreur lors du chargement du logo: {e}")
            self.logo_photo = None
    
    def creer_interface(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.frame_ventes = tk.Frame(notebook, bg='#f0f0f0')
        self.frame_a_propos = tk.Frame(notebook, bg='#e8f4f8')
        
        notebook.add(self.frame_ventes, text='Enregistrer une vente')
        notebook.add(self.frame_a_propos, text='À propos')
        
        self.creer_interface_ventes()
        self.creer_interface_a_propos()
    
    def creer_interface_ventes(self):
        frame_formulaire = tk.LabelFrame(
            self.frame_ventes, 
            text="Nouvelle vente", 
            bg='#f0f0f0',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=20
        )
        frame_formulaire.pack(padx=20, pady=20, fill='x')
        
        tk.Label(frame_formulaire, text="Nom du produit:", bg='#f0f0f0', font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.entry_nom = tk.Entry(frame_formulaire, width=30, font=('Arial', 10))
        self.entry_nom.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(frame_formulaire, text="Quantité:", bg='#f0f0f0', font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.entry_quantite = tk.Entry(frame_formulaire, width=30, font=('Arial', 10))
        self.entry_quantite.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(frame_formulaire, text="Prix unitaire (F CFA):", bg='#f0f0f0', font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        self.entry_prix_unitaire = tk.Entry(frame_formulaire, width=30, font=('Arial', 10))
        self.entry_prix_unitaire.grid(row=2, column=1, pady=5, padx=10)
        
        btn_ajouter = tk.Button(
            frame_formulaire,
            text="Enregistrer la vente",
            command=self.ajouter_vente,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            padx=20,
            pady=5
        )
        btn_ajouter.grid(row=3, column=0, columnspan=2, pady=15)
        
        frame_statistiques = tk.LabelFrame(
            self.frame_ventes,
            text="Statistiques",
            bg='#f0f0f0',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10
        )
        frame_statistiques.pack(padx=20, pady=10, fill='x')
        
        self.label_total = tk.Label(frame_statistiques, text="Total des ventes: 0.00 F CFA", bg='#f0f0f0', font=('Arial', 11))
        self.label_total.pack(anchor='w')
        
        self.label_nombre = tk.Label(frame_statistiques, text="Nombre de ventes: 0", bg='#f0f0f0', font=('Arial', 11))
        self.label_nombre.pack(anchor='w')
        
        frame_liste = tk.LabelFrame(
            self.frame_ventes,
            text="Historique des ventes",
            bg='#f0f0f0',
            font=('Arial', 12, 'bold'),
            padx=10,
            pady=10
        )
        frame_liste.pack(padx=20, pady=10, fill='both', expand=True)
        
        style = ttk.Style()
        style.configure("Treeview", 
                       rowheight=25, 
                       font=('Arial', 9),
                       foreground='black')
        style.configure("Treeview.Heading", 
                       font=('Arial', 10, 'bold'), 
                       foreground='black')
        
        style.map('Treeview',
                 foreground=[('selected', 'white')],
                 background=[('selected', '#0078d7')])
        
        colonnes = ('N°', 'Produit', 'Quantité', 'Prix unitaire', 'Prix total', 'Date', 'Supprimer')
        self.tree = ttk.Treeview(frame_liste, columns=colonnes, show='headings', height=8)
        
        largeurs = {
            'N°': 50, 
            'Produit': 150, 
            'Quantité': 90, 
            'Prix unitaire': 120, 
            'Prix total': 120, 
            'Date': 150, 
            'Supprimer': 80
        }
        
        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=largeurs.get(col, 130), anchor='center' if col != 'Produit' else 'w')
        
        self.tree.tag_configure('normal', foreground='black', font=('Arial', 9))
        self.tree.tag_configure('delete_icon', foreground='red', font=('Arial', 12, 'bold'))
        
        scrollbar = ttk.Scrollbar(frame_liste, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.tree.bind('<Button-1>', self.on_click)
    
    def creer_interface_a_propos(self):
        titre = tk.Label(
            self.frame_a_propos,
            text="Application de Gestion de Ventes",
            font=('Arial', 18, 'bold'),
            bg='#e8f4f8',
            fg='#2196F3'
        )
        titre.pack(pady=30)
        
        info_frame = tk.Frame(self.frame_a_propos, bg='#e8f4f8')
        info_frame.pack(pady=20)
        
        infos = [
            ("Développeur:", "Wingnemila Edwige BAMBA"),
            ("Version:", "1.0.0"),
            ("Langage:", "Python 3.14.3"),
            ("Framework:", "Tkinter"),
            ("Date:", "2025"),
            ("Description:", "Application desktop pour la gestion des ventes d'un commerce")
        ]
        
        for label, valeur in infos:
            frame_ligne = tk.Frame(info_frame, bg='#e8f4f8')
            frame_ligne.pack(pady=5, anchor='w')
            
            tk.Label(
                frame_ligne,
                text=label,
                font=('Arial', 11, 'bold'),
                bg='#e8f4f8',
                width=15,
                anchor='w'
            ).pack(side='left')
            
            tk.Label(
                frame_ligne,
                text=valeur,
                font=('Arial', 11),
                bg='#e8f4f8',
                anchor='w'
            ).pack(side='left')
        
        contact_frame = tk.LabelFrame(
            self.frame_a_propos,
            text="Contact",
            bg='#e8f4f8',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=15
        )
        contact_frame.pack(pady=30)
        
        tk.Label(
            contact_frame,
            text="Email: bambawingnemilaedwige@gmail.com",
            font=('Arial', 10),
            bg='#e8f4f8'
        ).pack()
        
        tk.Label(
            contact_frame,
            text="GitHub: https://github.com/wingnemila",
            font=('Arial', 10),
            bg='#e8f4f8'
        ).pack()
    
    def ajouter_vente(self):
        nom = self.entry_nom.get().strip()
        quantite_str = self.entry_quantite.get().strip()
        prix_unitaire_str = self.entry_prix_unitaire.get().strip()
        
        if not nom or not quantite_str or not prix_unitaire_str:
            messagebox.showwarning("Attention", "Tous les champs sont obligatoires!")
            return
        
        try:
            quantite = int(quantite_str)
            prix_unitaire = float(prix_unitaire_str)
            
            if quantite <= 0 or prix_unitaire <= 0:
                messagebox.showerror("Erreur", "La quantité et le prix doivent être positifs!")
                return
            
            prix_total = self.db.ajouter_vente(nom, quantite, prix_unitaire)
            
            self.entry_nom.delete(0, tk.END)
            self.entry_quantite.delete(0, tk.END)
            self.entry_prix_unitaire.delete(0, tk.END)
            
            self.actualiser_liste()
            self.actualiser_statistiques()
            
            messagebox.showinfo("Succès", f"Vente enregistrée!\nPrix total: {prix_total:.2f} F CFA")
            
        except ValueError:
            messagebox.showerror("Erreur", "Quantité et prix doivent être des nombres valides!")
    
    def on_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        
        column = self.tree.identify_column(event.x)
        item = self.tree.identify_row(event.y)
        
        if not item:
            return
        
        if column == '#7':
            self.supprimer_vente(item)
    
    def supprimer_vente(self, item):
        valeurs_brutes = self.tree.item(item)['values']
        vente_id = self.tree.item(item)['tags'][0]
        
        numero = valeurs_brutes[0]
        produit = valeurs_brutes[1]
        quantite = valeurs_brutes[2]
        prix_total = valeurs_brutes[4]
        
        reponse = messagebox.askyesno(
            "Confirmation de suppression", 
            f"Voulez-vous vraiment supprimer cette vente ?\n\n"
            f"N°: {numero}\n"
            f"Produit: {produit}\n"
            f"Quantité: {quantite}\n"
            f"Prix total: {prix_total}"
        )
        
        if reponse:
            self.db.supprimer_vente(vente_id)
            self.actualiser_liste()
            self.actualiser_statistiques()
            messagebox.showinfo("Succès", "Vente supprimée avec succès!")
    
    def actualiser_liste(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        ventes = self.db.obtenir_ventes()
        for index, vente in enumerate(ventes, start=1):
            item_id = self.tree.insert('', 'end', values=(
                index,
                vente[1],
                vente[2],
                f"{vente[3]:.2f} F CFA",
                f"{vente[4]:.2f} F CFA",
                vente[5],
                ""
            ), tags=(vente[0], 'normal'))
            
            self.tree.set(item_id, 'Supprimer', '❌')
            self.tree.item(item_id, tags=(vente[0], 'normal', 'delete_icon'))
    
    def actualiser_statistiques(self):
        total, nombre = self.db.obtenir_statistiques()
        self.label_total.config(text=f"Total des ventes: {total:.2f} F CFA")
        self.label_nombre.config(text=f"Nombre de ventes: {nombre}")
    
    def fermer_application(self):
        self.db.fermer()
        self.root.destroy()