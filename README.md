# Student Performance Analyzer

## Overview
A Python-based application to analyze student academic performance using structured data.

## Features
- Subject-wise average and median calculation
- Automatic grade assignment
- Top-performing and weakest student identification
- Visual performance analysis
- Exportable reports (CSV, TXT, PNG)

## Tech Stack
- Python
- Pandas
- NumPy
- Matplotlib

## 🚀 How to Run

### Prerequisites
- Python 3.8+ installed on your machine

### 1. Clone the repository
```bash
git clone https://github.com/roy-a11y/student-performance-analyzer.git
cd student-performance-analyzer
```

### 2. Set up virtual environment
```bash
python -m venv .venv

# Activate on Windows:
.venv\Scripts\activate

# Activate on Mac/Linux:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the analyzer
```bash
python src/main.py
```
This will process the data in `data/students.csv` and generate analytical reports and plots in the `output/` directory.

## 📁 Project Structure
```
student_performance_analyzer/
├── data/
│   └── students.csv         # Input data
├── src/
│   ├── main.py              # Main entry point
│   ├── data_handler.py      # Handles data loading and processing
│   ├── analyzer.py          # Contains analysis logic
│   └── visualize.py         # Generates plots
├── output/                  # Generated reports and plots
├── .venv/                   # Virtual environment (ignored in git)
├── .gitignore
├── requirements.txt
└── README.md
```
