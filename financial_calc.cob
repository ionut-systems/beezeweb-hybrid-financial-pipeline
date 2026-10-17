>>SOURCE FORMAT FREE
IDENTIFICATION DIVISION.
PROGRAM-ID. FinancialCalc.

DATA DIVISION.
WORKING-STORAGE SECTION.
01  WS-PRINCIPAL      PIC 9(6)V99 VALUE 10000.00.
01  WS-RATE           PIC V99     VALUE 0.05.
01  WS-YEARS          PIC 9(2)    VALUE 5.
01  WS-FINAL-AMOUNT   PIC 9(8)V99 VALUE 0.00.
01  WS-COUNTER        PIC 9(2)    VALUE 1.
01  WS-PAUSE          PIC X VALUE SPACE.

PROCEDURE DIVISION.
MAIN-LOGIC.
DISPLAY "==========================================".
DISPLAY "   COBOL QUANTITATIVE FINANCIAL MODULE   ".
DISPLAY "==========================================".

DISPLAY "Capital initial : " WS-PRINCIPAL.
DISPLAY "Taux d'interet  : 5%".
DISPLAY "Horizon (ans)   : " WS-YEARS.
DISPLAY "------------------------------------------".

MOVE WS-PRINCIPAL TO WS-FINAL-AMOUNT.
           
PERFORM WS-YEARS TIMES
COMPUTE WS-FINAL-AMOUNT = WS-FINAL-AMOUNT * (1 + WS-RATE)
END-PERFORM.

DISPLAY "Montant final estime : " WS-FINAL-AMOUNT.
DISPLAY "==========================================".

DISPLAY "Appuyez sur Entree pour quitter...".
ACCEPT WS-PAUSE.
STOP RUN.
