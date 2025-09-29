
import pandas as pd
from pathlib import Path

CSV = Path("D:\Healthcare Dashboard\healthcare_dataset.csv")
OUT = Path("reports")
OUT.mkdir(exist_ok=True)

def main():
    df = pd.read_csv(CSV)
    for c in ["Date of Admission","Discharge Date"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    if "Date of Admission" in df.columns:
        df["Admission_Date"] = df["Date of Admission"].dt.date

    if "Medical Condition" in df.columns:
        topc = df["Medical Condition"].value_counts().rename_axis("Condition").reset_index(name="Count")
        topc.to_csv(OUT/"top_conditions.csv", index=False)
    if "Medication" in df.columns:
        topm = df["Medication"].value_counts().rename_axis("Medication").reset_index(name="Count")
        topm.to_csv(OUT/"top_medications.csv", index=False)

    if "Admission_Date" in df.columns:
        daily = df.groupby("Admission_Date").agg(
            Admissions=("Admission_Date", "count"),
            Revenue=("Billing Amount", "sum")
        ).reset_index()
        daily.to_csv(OUT/"daily_admissions.csv", index=False)

    with pd.ExcelWriter(OUT/"summary.xlsx", engine="xlsxwriter") as w:
        if "Medical Condition" in df.columns:
            topc.to_excel(w, sheet_name="Conditions", index=False)
        if "Medication" in df.columns:
            topm.to_excel(w, sheet_name="Medications", index=False)
        if "Admission_Date" in df.columns:
            daily.to_excel(w, sheet_name="Admissions", index=False)

    print("Reports generated in", OUT.resolve())

if __name__ == "__main__":
    main()