# REFACTACY backend

## Installazione

Di seguito i passaggi per installare il progetto localmente.

### Prerequisiti
- Python (3.8+)

### Istruzioni di installazione
   
1. Creare un ambiente virtuale:
   ```bash 
   # Su Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   #Su MacOS
   python3 -m venv venv
   source venv/bin/activate

2. Installare le dipendenze:
   ```bash
   pip install -r requirements.txt

3. Creare file .env nella root principale (Refactacy-backend)

4. Inserire l'api key in .env:
   ```bash
   API_KEY=sk-kleSTW93bSNVqFPto-2YBUC8Ax68q3tgbbTyRgO7shT3BlbkFJdtGvJc_2d6HDWl-sPUqz33r7hBvLc8w89v9AE0zhEA
   
5. Attivare il server locale con Flask:
   ```bash
   #Su Windows
   python main.py

   #Su MacOS
   python3 main.py

6. Output atteso:
   ```bash
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   * Restarting with stat
   * Debugger is active!

## Link di presentazione

Ecco il link a un video di presentazione: [Link al video!](https://youtu.be/lBKG2NLCfx4)

## Autori
Alessandro Iannone, Domenico De Gioia, Giuseppe Simone
