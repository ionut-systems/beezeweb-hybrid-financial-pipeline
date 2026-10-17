import subprocess
import re
import csv
from datetime import datetime

print("======================================================")
print("   BEEZEWEB SYSTEM - TABLEAU DE BORD SUPERVISEUR      ")
print("======================================================")
print("[*] Demarrage du moteur COBOL en arriere-plan...\n")

# 1. Le Pont : Execution du Mainframe
resultat_cobol = subprocess.run(
    ['./batch_process.exe'], 
    capture_output=True, 
    text=True, 
    input="\n"
)
donnee_brute = resultat_cobol.stdout

# 2. Extraction Chirurgicale (Regex)
motif = r"GRAND LIVRE - CAPITAL TOTAL :\s*([\d,]+\.\d{2})"
correspondance = re.search(motif, donnee_brute)

if correspondance:
    capital_texte = correspondance.group(1)
    capital_reel = float(capital_texte.replace(',', ''))
    rendement_annuel = capital_reel * 0.05
    
    # 3. L'Interface Utilisateur (Le Terminal propre)
    print("------------------------------------------------------")
    print(" [+] SYNCHRONISATION REUSSIE AVEC LE GRAND LIVRE")
    print(f"     Capital Actuel Valide   : {capital_texte} EUR")
    print(f"     Simulation Rendement 5% : +{rendement_annuel:.2f} EUR")
    print("------------------------------------------------------\n")
    
    # 4. L'Exportation Physique (Creation du CSV)
    nom_fichier = "rapport_financier.csv"
    date_du_jour = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"[*] Generation de l'export systeme : {nom_fichier}...")
    
    # Ouverture et ecriture du fichier CSV sur le disque dur
    with open(nom_fichier, mode='w', newline='') as fichier_csv:
        # On utilise le point-virgule comme separateur pour eviter les conflits avec les virgules des nombres
        writer = csv.writer(fichier_csv, delimiter=';') 
        
        # Ecriture de l'en-tete (les colonnes)
        writer.writerow(["Date_Execution", "Capital_Total_EUR", "Taux_Simulation", "Rendement_Annuel_EUR"])
        
        # Ecriture des donnees extraites
        writer.writerow([date_du_jour, capital_reel, "5%", round(rendement_annuel, 2)])
        
    print("[+] EXPORT TERMINE : Le fichier CSV est disponible sur votre ordinateur.")

else:
    print("[-] ERREUR CRITIQUE : Impossible d'extraire la signature du Grand Livre.")

print("\n======================================================")
print("   FIN DE SESSION")
print("======================================================")

input("\nAppuyez sur ENTREE pour quitter le programme...")
