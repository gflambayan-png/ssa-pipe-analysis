# ssa-pipe-analysis
# 🌊 SSA Pipe Analysis Tool

A Python tool for sanitizing Storm & Sanitary Analysis (SSA) CSV exports and evaluating pipe hydraulics using Manning’s equation.  
It automatically cleans SSA output, detects the correct diameter/height column, and computes flow capacity, velocity, and pipe status safely.

---

## ⚙️ Features
- 🧹 Automatic SSA CSV sanitization  
- 🧾 Header row detection  
- 📏 Auto-detection of pipe height/diameter column  
- 🔢 Cleans numeric fields (slope, height, flow)  
- 💧 Safe Manning capacity and velocity calculations  
- 🚫 Skips junk rows, blank rows, and invalid pipes  
- 📊 Outputs pipe flow, capacity, velocity, and status  

---

## 🧰 Requirements
- Python 3.10+
- pandas  

Install dependencies:

pip install pandas

▶️ Usage
Place your SSA CSV file in the project folder and run:
python storm_sanitary_analysis.py

📈 Example Output
{'Pipe': 'L-PIPE113', 'Flow': 0.0, 'Capacity': 0.475, 'Velocity': 0.0, 'Status': 'OK'}
{'Pipe': 'L-PIPE115', 'Flow': 0.0, 'Capacity': 0.514, 'Velocity': 0.0, 'Status': 'OK'}

🚀 Future Improvements
- Export results to CSV

- Add velocity limit warnings

- Add undersized pipe alerts

- Add storm/sanitary flow calculators

👤 Author
Gener Francis Lambayan

🏗️ Project Design
This project follows a clean, modular structure:
SSA PROJECT/
│
├── storm_sanitary_analysis.py   # Main script
├── ProjectFinal.csv             # SSA data file
└── README.md                    # Documentation
