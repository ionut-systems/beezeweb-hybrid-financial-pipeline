# Beezeweb - Hybrid Financial Pipeline (COBOL / Python)

## 🏛️ Vue d'ensemble de l'Architecture
Ce projet met en œuvre un pipeline de données hybride et sécurisé, combinant la puissance de calcul historique et la stricte intégrité de **GnuCOBOL** avec l'agilité d'orchestration moderne de **Python**. 

L'objectif est d'éliminer les risques de corruption des données financières en isolant le moteur de calcul (Backend batch) du superviseur d'analyse (Front-end / Reporting).

---

## ⚙️ Les Piliers du Système

1. **La Base de Données Statique (`portfolio.txt`) :**
   * Structure à enregistrements à taille fixe (`LINE SEQUENTIAL`).
   * Données de transactions financières rigoureusement formatées.

2. **Le Moteur de Calcul Backend (`batch_process.cob`) :**
   * **Norme de compilation :** Conforme aux directives de format libre (`>>SOURCE FORMAT FREE`) et aux standards POSIX (terminaison par saut de ligne, compilation `-static` pour l'autonomie du binaire).
   * **Intégrité de la donnée :** Filtrage par signature de ligne (`TXN(1:3)`) pour éliminer les enregistrements fantômes induits par les retours chariots du système d'exploitation (`CRLF`).
   * **Précision comptable :** Utilisation de masques de mémoire de type `PIC 9(8)V99` et de la fonction native `FUNCTION NUMVAL` pour garantir l'absence d'erreurs d'arrondi sur les flux monétaires.

3. **Le Superviseur et Pont d'Orchestration (`bridge.py`) :**
   * Automatisation du lancement du binaire COBOL via le module `subprocess`.
   * Interception du flux de sortie standard (`stdout`) en mode furtif.
   * Analyse syntaxique par **Expressions Régulières (Regex)** pour extraire chirurgicalement le capital total calculé par le mainframe.
   * Exportation automatisée des données financières au format **CSV** normalisé, horodaté et prêt à l'emploi pour les ERP.

4. **L'Interface Graphique Superviseur (`gui_beezeweb.py`) :**
   * Application de bureau construite avec **Tkinter** (architecture événementielle).
   * Exécution silencieuse du sous-processus COBOL (`CREATE_NO_WINDOW`) sans ouverture de console parasite.
   * Tableau de bord temps réel et génération automatisée du reporting CSV en un clic.

---

## 🚀 Guide d'Utilisation et Compilation

### 1. Compilation du Moteur COBOL
Pour compiler le code source du traitement par lots en un exécutable statique sans dépendances :
```bash
cobc -x -static batch_process.cob
```

### 2. Exécution du Superviseur Python (CLI)
Pour lancer l'orchestrateur en console, capturer les flux du mainframe et générer le rapport financier :
```bash
python bridge.py
```

### 3. Packaging du Superviseur CLI (Standalone)
Pour compiler le superviseur console en un exécutable autonome via PyInstaller :
```bash
pyinstaller --onefile bridge.py
```

### 4. Compilation de l'Interface Graphique (Zéro Console)
Pour générer l'application de bureau autonome (GUI) sans terminal d'arrière-plan :
```bash
pyinstaller --onefile --noconsole gui_beezeweb.py
```

---
*Développé dans le cadre des infrastructures d'ingénierie de Beezeweb.*