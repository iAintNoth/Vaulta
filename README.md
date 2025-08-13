# Vaulta - IT

## Descrizione
Questa applicazione permette di gestire configurazioni e schedulazioni di backup per le cartelle sul tuo computer.  
Al momento, **è possibile salvare solo cartelle**, non singoli file.

---

## Funzionalità principali
- Aggiunta di cartelle da salvare
- Avvio manuale o programmato dei backup
- Configurazioni modificabili direttamente dall'app
- Interfaccia grafica semplice e intuitiva

---

## Installazione

1. Clona o scarica il progetto:
```bash
git clone <link-del-progetto>
cd NomeProgetto
```
2. Crea un virtual environment:

```bash
python -m venv venv
```
3. Attiva il virtual environment:
Windows (cmd):

```bash
Copia
Modifica
venv\Scripts\activate
```

Windows (PowerShell):
```bash
venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source venv/bin/activate
```

4. Installa le dipendenze


```bash

pip install -r requirements.txt

```
## Uso
Avvia l'app


```bash
python main.py

```

### Nell'interfaccia grafica:

- Clicca su Aggiungi cartella per selezionare le cartelle da salvare

- Imposta la frequenza dei backup se vuoi usare lo scheduler

- Premi Avvia backup per eseguire il salvataggio manualmente

### Limitazioni
- Attualmente è possibile salvare solo cartelle.

- Non è ancora previsto il backup di singoli file.

- Alcune funzionalità dello scheduler potrebbero essere limitate nella versione iniziale.


Ecco il tuo testo completo tradotto in inglese, pronto per essere usato:

---

# Vaulta - EN

## Description

This application allows you to manage backup configurations and schedules for folders on your computer.
Currently, **only folders can be saved**, not individual files.

---

## Main Features

* Add folders to be backed up
* Start backups manually or on a schedule
* Modify configurations directly from the app
* Simple and intuitive graphical interface

---

## Installation

1. Clone or download the project:

```bash
git clone <project-link>
cd NomeProgetto
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

Windows (cmd):

```bash
venv\Scripts\activate
```

Windows (PowerShell):

```bash
venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Start the app:

```bash
python main.py
```

### In the graphical interface:

* Click **Add Folder** to select folders to back up
* Set the backup frequency if you want to use the scheduler
* Press **Start Backup** to manually run the backup

### Limitations

* Currently, only folders can be backed up.
* Individual file backups are not yet supported.
* Some scheduler functionalities may be limited in the initial version.

---

## Licenza
```bash
MIT License

Copyright (c) 2025 iAintNoth

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```