import pandas as pd
import math

# ---------------------------------------------------------
# FILE SANITIZER (auto-detect header, clean numeric columns)
# ---------------------------------------------------------
def sanitize_ssa_file(path):
    # Load raw file with no header
    df = pd.read_csv(path, header=None)

    # 1. Find the real header row (the one containing "Element ID")
    header_row = None
    for i in range(len(df)):
        row_values = df.iloc[i].astype(str).str.strip().tolist()
        if "Element ID" in row_values:
            header_row = i
            break

    if header_row is None:
        raise ValueError("Could not find 'Element ID' header row in file.")

    # 2. Reload using the correct header row
    df = pd.read_csv(path, header=header_row)
    df.columns = df.columns.str.strip()

    # 3. Drop fully empty columns
    df = df.dropna(axis=1, how="all")

    # 4. Clean numeric columns
    numeric_cols = [
        "Average Slope (%)",
        "Channel Height (m)",
        "Initial Flow (cms)"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("%", "", regex=False)
                .str.replace(",", "", regex=False)
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


# ---------------------------------------------------------
# STORM METHODS
# ---------------------------------------------------------
def storm_flow(method, **k):
    if method == "rational":
        return k["C"] * k["I"] * k["A"]
    elif method == "scs":
        S = (1000 / k["CN"]) - 10
        Q = ((k["P"] - 0.2*S)**2) / (k["P"] + 0.8*S)
        return Q * k["A"]
    elif method == "user":
        return k["formula"](k)
    else:
        raise ValueError("Unknown storm method")


# ---------------------------------------------------------
# SANITARY METHODS
# ---------------------------------------------------------
def sanitary_flow(method, **k):
    if method == "harmon":
        PF = 1 + (14 / (4 + k["population"]**0.5))
        return PF * k["avg_flow"]
    elif method == "babitt":
        return k["avg_flow"] * 3.0
    elif method == "user":
        return k["formula"](k)
    else:
        raise ValueError("Unknown sanitary method")


# ---------------------------------------------------------
# HYDRAULICS (MANNING + VELOCITY)
# ---------------------------------------------------------
def manning_capacity(d, s, n=0.013):
    A = math.pi * (d**2) / 4
    R = d / 4
    return (1/n) * A * (R**(2/3)) * math.sqrt(s)

def velocity(Q, d):
    if d <= 0:
        return 0
    A = math.pi * (d**2) / 4
    if A == 0:
        return 0
    return Q / A

# ---------------------------------------------------------
# PIPE EVALUATION
# ---------------------------------------------------------
def evaluate_pipe(pipe_id, d, s, Q):
    cap = manning_capacity(d, s)
    vel = velocity(Q, d)
    status = "OK" if Q < cap else "UNDERSIZED"
    return {
        "Pipe": pipe_id,
        "Flow": Q,
        "Capacity": cap,
        "Velocity": vel,
        "Status": status
    }


# ---------------------------------------------------------
# LOAD + SANITIZE FILE
# ---------------------------------------------------------
df = sanitize_ssa_file("ProjectFinal.csv")
# ---------------------------------------------------------
# AUTO-DETECT HEIGHT / DIAMETER COLUMN
# ---------------------------------------------------------
height_col = None
for col in df.columns:
    if "height" in col.lower() or "diameter" in col.lower():
        height_col = col
        break

if height_col is None:
    raise ValueError("Could not find a pipe height/diameter column.")

# Clean height column
df[height_col] = pd.to_numeric(df[height_col], errors="coerce").fillna(0)

# ---------------------------------------------------------
# FINAL LOOP THROUGH CLEANED CSV
# ---------------------------------------------------------
for _, row in df.iterrows():

    # Skip rows with no pipe ID
    if pd.isna(row["Element ID"]) or row["Element ID"] == "":
        continue

    # Skip rows with no diameter/height
    if row[height_col] <= 0:
        continue

    result = evaluate_pipe(
        row["Element ID"],
        row[height_col],
        row["Average Slope (%)"] / 100,
        row["Initial Flow (cms)"]
    )
    print(result)
