# Python Data Workflow Guide (VS Code)

A general guide for setting up a clean Python environment, installing dependencies, reading CSV files, and visualizing data.

---

## 1. Core Concept

Each project should have:

- Its own environment (`.venv`)
- Its own dependencies
- Its own data and scripts

---

## 2. Standard Project Structure

```
project-name/
│
├── .venv/                # Virtual environment
├── data/                 # CSV or dataset files
│   └── data.csv
│
├── src/                  # Python scripts
│   └── main.py
│
├── requirements.txt      # Dependencies
└── README.md
```

---

## 3. Environment Setup (One-Time per Project)

### Step 1: Create Virtual Environment

```bash
python -m venv .venv
```

---

### Step 2: Activate Environment

#### Windows (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

#### Mac / Linux

```bash
source .venv/bin/activate
```

---

### Step 3: Verify Environment

You should see:

```
(.venv)
```

---

## 4. Install Dependencies

```bash
pip install pandas matplotlib numpy
```

---

### Save Dependencies

```bash
pip freeze > requirements.txt
```

---

### Reinstall Later

```bash
pip install -r requirements.txt
```

---

## 5. Running Python Scripts

```bash
python src/main.py
```

---

## 6. Reading CSV Files

```python
import pandas as pd

df = pd.read_csv("data/data.csv")
```

---

## 7. Basic Plotting Pattern

```python
import matplotlib.pyplot as plt

plt.figure()
plt.plot(x, y)

plt.title("Title")
plt.xlabel("X")
plt.ylabel("Y")

plt.grid()
plt.show()
```

---

## 8. Recommended Workflow

1. Create project folder  
2. Create `.venv`  
3. Activate environment  
4. Install dependencies  
5. Write script  
6. Run script  

---

## 9. Common Issues

### ModuleNotFoundError

Cause: Package not installed in `.venv`

Fix:

```bash
pip install <package-name>
```

---

### Wrong Python Environment

Cause: Using system Python instead of `.venv`

Fix: Ensure terminal shows:

```
(.venv)
```

---

### File Not Found

Cause: Incorrect file path

Fix:

- Use relative paths
- Keep data in `/data` folder

Example:

```python
pd.read_csv("data/data.csv")
```

---

## 10. Best Practices

- Use one `.venv` per project
- Avoid installing packages globally
- Keep file names simple
- Avoid spaces in file names
- Separate code and data
- Use `requirements.txt` for reproducibility

---

## 11. Minimal Template

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/data.csv")

x = df["x"]
y = df["y"]

plt.plot(x, y)
plt.show()
```

---

## 12. Mental Model

- `.venv` = isolated Python environment  
- `pip install` = install tools into that environment  
- `requirements.txt` = environment snapshot  
- script = logic  
- CSV = data  

---

## 13. Goal

This workflow ensures:

- Clean environment  
- No dependency conflicts  
- Reproducible results  
- Scalable projects  

---

## 14. Next Extensions

You can extend this workflow to:

- Sensor data analysis  
- Signal processing  
- Kalman filtering  
- Machine learning pipelines  
