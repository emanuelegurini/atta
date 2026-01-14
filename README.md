# Atta - Attendance Tracker

> **Progetto didattico** realizzato durante il corso **AWS re/Start** (da AWS & Edgemony) per dimostrare l'uso di **AI Agentic Coding** (Copilot/Cursor) nella creazione di prodotti software reali.

**Atta** è un'applicazione da riga di comando (CLI) che permette agli studenti di monitorare la propria frequenza ai corsi in tempo reale, leggendo i dati direttamente da un **Google Sheet** gestito dal docente.

## Caratteristiche
*   **Privacy-First (Pseudonimia)**: Nessun nome studente nel DB pubblico, solo ID segreti (es. `S-101`).
*   **Trasparenza**: Calcolo automatico della percentuale basato sulle lezioni effettivamente svolte.
*   **Zero-Config Backend**: Usa un semplice Google Sheet come database.
*   **Interattiva**: Menu CLI elegante e facile da usare.

---

## Per Iniziare (Setup Sviluppatore/Studente)

### Prerequisiti
*   Python 3.8+
*   Accesso al file `.env` (chiedere al docente/admin per l'URL del foglio)

### Installazione
```bash
# 1. Clona la repo
git clone https://github.com/emanuelegurini/atta.git
cd atta

# 2. Crea ambiente virtuale
python3 -m venv venv
source venv/bin/activate  # (su Mac/Linux)
# venv\Scripts\activate   # (su Windows)

# 3. Installa dipendenze
pip install -r requirements.txt

# 4. Configura le variabili d'ambiente
cp .env.example .env
# Modifica .env inserendo l'URL corretto in ATTA_SHEET_URL
```

### Utilizzo
```bash
python main.py
```
Il menu interattivo ti guiderà:
1.  Inserisci il tuo **Secret Student ID** (ti verrà fornito dal docente).
2.  Visualizza le tue statistiche aggiornate.

---

## Guida per il Trainer (Gestione Dati)

Il sistema si basa su un Google Sheet rigorosamente formattato.

### Regole d'Oro per l'Inserimento Dati
1.  **Colonna A (Obbligatoria)**: Deve chiamarsi `Student_ID`. Contiene i codici univoci degli studenti. Non inserire Nomi/Cognomi qui per privacy.
2.  **Colonne Lezioni (Obbligatorie)**: 
    *   L'intestazione **DEVE** essere una data nel formato `DD/MM/YYYY` (es. `14/01/2025`).
    *   Le colonne con altri nomi (es. "Note", "Totale") verranno **ignorate** automaticamente dal software.
3.  **Presenze/Assenze**:
    *   Scrivi `P` per Presente.
    *   Scrivi `A` per Assente.
    *   Lascia la cella **VUOTA** se la lezione non è ancora avvenuta (così non influisce sulla media).

### Esempio Struttura Foglio
| Student_ID | 14/01/2025 | 15/01/2025 | Note (Ignorata) |
| :--- | :--- | :--- | :--- |
| S-001 | P | P | Ottimo |
| S-002 | A | P | Ritardo |

---

## Tech Stack
*   **Python**: Core logic.
*   **Pandas**: Data processing & CSV parsing.
*   **Rich**: UI/UX da terminale.
*   **Questionary**: Menu interattivi.
*   **Pytest**: Testing automatizzato.

---
*Created by the AWS re/Start Class & AI Agents.*
