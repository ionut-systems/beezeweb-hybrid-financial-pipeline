import tkinter as tk
from tkinter import messagebox
import subprocess
import re
import csv
from datetime import datetime

def lancer_audit():
    """Fonction déclenchée au clic sur le bouton de l'interface."""
    lbl_statut.config(text="Statut : Exécution du moteur COBOL en cours...", fg="#f39c12")
    fenetre.update()

    try:
        # 1. Appel furtif du binaire COBOL
        resultat_cobol = subprocess.run(
            ['./batch_process.exe'],
            capture_output=True,
            text=True,
            input="\n",
            creationflags=subprocess.CREATE_NO_WINDOW  # Pour éviter l'ouverture d'une console supplémentaire
        ) # type: ignore
        donnee_brute = resultat_cobol.stdout

        # 2. Extraction chirurgicale via Regex
        motif = r"GRAND LIVRE - CAPITAL TOTAL :\s*([\d,]+\.\d{2})"
        correspondance = re.search(motif, donnee_brute)

        if correspondance:
            capital_texte = correspondance.group(1)
            capital_reel = float(capital_texte.replace(',', ''))
            rendement_annuel = capital_reel * 0.05
            date_du_jour = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 3. Mise à jour visuelle des compteurs dans la fenêtre
            lbl_capital_val.config(text=f"{capital_texte} EUR")
            lbl_rendement_val.config(text=f"+{rendement_annuel:.2f} EUR")

            # 4. Persistance des données (Export CSV)
            nom_fichier = "rapport_financier.csv"
            with open(nom_fichier, mode='w', newline='') as fichier_csv:
                writer = csv.writer(fichier_csv, delimiter=';')
                writer.writerow(["Date_Execution", "Capital_Total_EUR", "Taux_Simulation", "Rendement_Annuel_EUR"])
                writer.writerow([date_du_jour, capital_reel, "5%", round(rendement_annuel, 2)])

            lbl_statut.config(text=f"Statut : Synchronisé & Exporté ({date_du_jour})", fg="#2ecc71")
            messagebox.showinfo("Succès Beezeweb", "Le Grand Livre COBOL a été audité et le fichier CSV est généré.")
        else:
            lbl_statut.config(text="Statut : Erreur de lecture du Grand Livre", fg="#e74c3c")
            messagebox.showerror("Erreur d'extraction", "Impossible d'isoler la signature financière dans le flux COBOL.")

    except FileNotFoundError:
        lbl_statut.config(text="Statut : Moteur COBOL introuvable", fg="#e74c3c")
        messagebox.showerror("Erreur Système", "Le fichier batch_process.exe est introuvable dans ce répertoire.")

# --- CONFIGURATION DE LA FENÊTRE PRINCIPALE ---
fenetre = tk.Tk()
fenetre.title("Beezeweb - Superviseur Financier Hybride")
fenetre.geometry("480x340")
fenetre.configure(bg="#1e272e")
fenetre.resizable(False, False)

# --- EN-TÊTE ---
lbl_titre = tk.Label(
    fenetre, text="BEEZEWEB FINANCIAL ENGINE", 
    font=("Consolas", 15, "bold"), bg="#1e272e", fg="#ffffff", pady=15
)
lbl_titre.pack()

# --- CADRE DES MÉTRIQUES ---
cadre_donnees = tk.Frame(fenetre, bg="#2f3640", bd=2, relief="groove", padx=20, pady=15)
cadre_donnees.pack(pady=5, fill="x", padx=30)

tk.Label(cadre_donnees, text="Capital Grand Livre (COBOL) :", font=("Arial", 10), bg="#2f3640", fg="#dcdde1").grid(row=0, column=0, sticky="w", pady=5)
lbl_capital_val = tk.Label(cadre_donnees, text="---.-- EUR", font=("Consolas", 12, "bold"), bg="#2f3640", fg="#00a8ff")
lbl_capital_val.grid(row=0, column=1, sticky="e", padx=15, pady=5)

tk.Label(cadre_donnees, text="Projection Rendement (5%) :", font=("Arial", 10), bg="#2f3640", fg="#dcdde1").grid(row=1, column=0, sticky="w", pady=5)
lbl_rendement_val = tk.Label(cadre_donnees, text="---.-- EUR", font=("Consolas", 12, "bold"), bg="#2f3640", fg="#4cd137")
lbl_rendement_val.grid(row=1, column=1, sticky="e", padx=15, pady=5)

# --- BOUTON D'ACTION ---
btn_lancer = tk.Button(
    fenetre, text="LANCER L'AUDIT & EXPORTER CSV", command=lancer_audit,
    font=("Arial", 10, "bold"), bg="#0097e6", fg="white", 
    activebackground="#00a8ff", activeforeground="white",
    padx=15, pady=8, cursor="hand2", relief="flat"
)
btn_lancer.pack(pady=20)

# --- BARRE DE STATUT ---
lbl_statut = tk.Label(
    fenetre, text="Statut : En attente d'exécution...", 
    font=("Arial", 9, "italic"), bg="#1e272e", fg="#7f8fa6"
)
lbl_statut.pack(side="bottom", pady=10)

# Boucle d'affichage continu
fenetre.mainloop()