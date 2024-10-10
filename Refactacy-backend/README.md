# REFACTACY backend

## Installazione

Di seguito i passaggi per installare il progetto localmente.

### Prerequisiti
- Python (3.8+)

### Istruzioni di installazione

1. Clonare la repository del back-end:
   ```bash 
   git clone https://github.com/aleiann/refactacy-be.git
   cd /refactacy-be
   
2. Creare un ambiente virtuale:
   ```bash 
   # Su Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   #Su MacOS
   python3 -m venv venv
   source venv/bin/activate

3. Installare le dipendenze:
   ```bash
   pip install -r requirements.txt
   
4. Attivare il server locale con Flask:
   ```bash
   #Su Windows
   python main.py

   #Su MacOS
   python3 main.py

5. Output atteso:
   ```bash
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   * Restarting with stat
   * Debugger is active!

![Demo](png/traduzione.png)
![Demo](png/documentazione.png)


Ecco il link a un video di presentazione: [Link al video!](https://www.youtube.com/watch?v=1Srlgnn9P0w)
