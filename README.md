🌊 SSA Pipe Analysis Tool
Project Overview
This Python script sanitizes SSA (Storm & Sanitary Analysis) CSV exports and evaluates pipe hydraulics using Manning’s equation. It cleans messy SSA output, detects the correct diameter/height column, and computes flow capacity, velocity, and pipe status for drainage and sewer design.

⭐ Featured
SSA CSV cleanup and formatting

Automatic header + diameter/height detection

Manning’s equation capacity + velocity calculation

Filters junk rows and invalid pipes

Clear, reusable hydraulic evaluation functions

Easy to extend into larger stormwater or sanitary analysis tools

🧠 Core Function (Manning Capacity Example)
def manning_capacity(diameter_m, slope, n=0.013):
    radius = diameter_m / 2
    area = 3.14159 * radius**2
    hydraulic_radius = radius / 2
    return (1/n) * area * (hydraulic_radius**(2/3)) * (slope**0.5)
▶️ Example Usage
result = evaluate_pipe("L-PIPE113", 0.0, 0.475, 0.0)
print(result)
Output:
{'Pipe': 'L-PIPE113', 'Flow': 0.0, 'Capacity': 0.475, 'Velocity': 0.0, 'Status': 'OK'}
🏃 How to Run:
Install dependencies:
pip install pandas
Run the script:
python storm_sanitary_analysis.py

🚀 Future Improvements
CSV export for results

Velocity limit warnings

Undersized pipe alerts

Storm/sanitary flow calculators

Optional hydraulic plots

🎓 What I Learned
Applying Manning’s equation in Python

Cleaning and sanitizing engineering datasets

Structuring reusable hydraulic functions

Writing clear documentation

Connecting Civil Engineering concepts with automation

👤 Author
Gener Francis Lambayan
