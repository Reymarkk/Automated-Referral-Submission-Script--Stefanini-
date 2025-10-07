# Form Automation — Windows + VS Code Quickstart

This README expands the previous quickstart with step-by-step instructions tailored for **Windows** and **Visual Studio Code**, plus notes for editing the script (e.g., changing the job title target). The repo used in examples:

`https://github.com/Reymarkk/Automated-Referral-Submission-Script--Stefanini-.git`

---

## Prerequisites

* **Windows 10/11** with an administrative user.
* **Python 3.10+** installed and on `PATH`.
* **Git** installed.
* **Visual Studio Code** installed.
* At least one modern browser installed (Chrome/Chromium or Firefox).

> Selenium 4.6+ includes Selenium Manager which usually auto-downloads the correct browser driver for you if a browser is installed.

---

## Clone the repo

Open PowerShell (recommended) or CMD and run:

```powershell
# PowerShell
git clone https://github.com/Reymarkk/Automated-Referral-Submission-Script--Stefanini-.git
cd Automated-Referral-Submission-Script--Stefanini-
```

---

## Create a virtual environment and install dependencies (Windows)

⚠️ **Always activate your virtual environment before running `pip install`.** If you forget, packages may end up in your global Python instead of `.venv`.

### PowerShell (recommended)

```powershell
# Create virtualenv
python -m venv .venv

# Activate (PowerShell)
.venv\Scripts\Activate.ps1

# If activation is blocked by policy, run once as admin (or current user):
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

# Copy the env template to create your .env file
Copy-Item -Path .env.example -Destination .env
```

### CMD (legacy)

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

### Git Bash / WSL users

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

---

## Edit `.env`

Open `.env` in VS Code and set these (minimum):

```ini
TARGET_URL="https://jobs2.smartsearchonline.com/stefanini/jobs/process_jobsearch.asp?jobTitle=&cityZip=&country=Phillip&proximity="
JOB_TITLE="Helpdesk Technician [Work setup: Full onsite]"
BROWSER="firefox"
HEADLESS="false"
RESUME_FILE="data/resume.pdf"
```

---

## Open in VS Code and configure the interpreter

```powershell
code .
```

### Select the correct interpreter

1. Press `Ctrl+Shift+P` -> `Python: Select Interpreter`.
2. Choose the interpreter at: `${workspaceFolder}\.venv\Scripts\python.exe`.

Optional: update `.vscode/settings.json` to point to the venv interpreter (Windows path):

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
  "editor.formatOnSave": true,
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["-q"]
}
```

---

## Activate virtual environment (Windows)

Depending on the shell you use:

* **PowerShell** (recommended):

  ```powershell
  .venv\Scripts\Activate.ps1
  ```

  If you get an error about execution policy:

  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  .venv\Scripts\Activate.ps1
  ```

* **CMD**:

  ```cmd
  .venv\Scripts\activate.bat
  ```

* **Git Bash**:

  ```bash
  source .venv/Scripts/activate
  ```

Once activated, your prompt should show `(.venv)` at the beginning.

---

## Run the script and tests

From the integrated terminal (with the venv active):

```powershell
# Run the sample script
python src/automation/main.py

# Run tests
pytest -q
```

---

## requirements.txt (latest)

These are the packages currently required:

```
selenium>=4.24.0,<5
python-dotenv>=1.0,<2
pytest>=8,<9
ruff>=0.5,<1
black>=24,<25
mypy>=1.10,<2
```

> If you ever see `ModuleNotFoundError`, make sure your venv is active and run:
>
> ```powershell
> pip install -r requirements.txt --force-reinstall
> ```

---

## Common troubleshooting

* **`ModuleNotFoundError: No module named 'dotenv'`** → venv not active during install. Fix: activate `.venv` and reinstall requirements.
* **Activation blocked in PowerShell** → `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.
* **Selenium can’t find browser/driver** → ensure Firefox or Chrome is installed. Selenium Manager downloads drivers automatically.
* **Headless problems** → set `HEADLESS=false` in `.env` while debugging.

---

## Commit & push changes

```powershell
git add -A
git commit -m "Update README with activation and requirements info"
git push origin main
```

---

This ensures you always have the right environment setup and dependencies in place before running your script.
