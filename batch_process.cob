>>SOURCE FORMAT FREE
IDENTIFICATION DIVISION.
PROGRAM-ID. BatchProcess.

ENVIRONMENT DIVISION.
INPUT-OUTPUT SECTION.
FILE-CONTROL.
*>  Connexion physique au fichier
    SELECT PORTFOLIO-FILE ASSIGN TO "portfolio.txt"
    ORGANIZATION IS LINE SEQUENTIAL.

DATA DIVISION.
FILE SECTION.
*>  Radiographie de la ligne lue
FD  PORTFOLIO-FILE.
01  PORTFOLIO-RECORD.
    05  TXN-ID          PIC X(8).
    05  FILLER          PIC X(1).
    05  TXN-AMOUNT      PIC 9(6).99.
    05  FILLER          PIC X(1).
    05  TXN-RATE        PIC 9(2).99.
WORKING-STORAGE SECTION.
01  WS-EOF              PIC A(1) VALUE 'N'.
01  WS-PAUSE            PIC X(1).

*>  LES VARIABLES DU GRAND LIVRE (L'Accumulateur)
*>  Le 'V' indique la virgule mathematique invisible pour le CPU
01  WS-TOTAL-CAPITAL    PIC 9(8)V99 VALUE ZERO.
*>  Le 'Z' efface les zeros inutiles a gauche pour l'humain
01  WS-DISPLAY-TOTAL    PIC ZZZZ,ZZ9.99.

PROCEDURE DIVISION.
MAIN-LOGIC.
    DISPLAY "=========================================".
    DISPLAY " DEBUT DU TRAITEMENT PAR LOTS (BATCH)".
    DISPLAY "=========================================".

    OPEN INPUT PORTFOLIO-FILE.

    PERFORM UNTIL WS-EOF = 'Y'
        READ PORTFOLIO-FILE
            AT END 
                MOVE 'Y' TO WS-EOF
            NOT AT END
*>              On remplace l'ancienne sécurité par une validation stricte : 
                IF TXN-ID(1:3) = "TXN"
                    DISPLAY "Traitement : " TXN-ID 
                            " | Montant: " TXN-AMOUNT 
                            " | Taux: " TXN-RATE "%"
                            
*>                  Le Moteur Comptable : On extrait la valeur mathematique 
*>                  du texte et on l'ajoute au capital total
                    COMPUTE WS-TOTAL-CAPITAL = WS-TOTAL-CAPITAL + FUNCTION NUMVAL(TXN-AMOUNT)
                END-IF
        END-READ
    END-PERFORM.

    CLOSE PORTFOLIO-FILE.

*>  Formatage final : On transfere le calcul brut vers le masque d'affichage humain
    MOVE WS-TOTAL-CAPITAL TO WS-DISPLAY-TOTAL.

    DISPLAY "-----------------------------------------".
    DISPLAY " GRAND LIVRE - CAPITAL TOTAL : " WS-DISPLAY-TOTAL.
    DISPLAY "=========================================".
    DISPLAY " TRAITEMENT TERMINE AVEC SUCCES.".
    DISPLAY "=========================================".
    DISPLAY "Appuyez sur Entree pour quitter...".
    ACCEPT WS-PAUSE.

    STOP RUN.
