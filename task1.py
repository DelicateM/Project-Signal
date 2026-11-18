import pandas as pd
file_path = "Project_Signal_Source.xlsx"
workbook = pd.ExcelFile(file_path)
sheets= [
    "Equipment_Events",
    "Delays_Downtime",
    "Operator_Activities",
    "Shift_Performance",
    "Safety_Observations",
    "Training_Records",
    "Maintenance_Notifications",
    "Environmental_Readings",
    "Access_Control",
]
print("\n" + "=" * 70)
print("PROJECT SIGNAL - TASK 1 DATA INSPECTION")
print("=" * 70)
summary = []
for sheet in sheets:
    df = pd.read_excel(file_path, sheet_name=sheet)
    summary.append({
        "Dataset": sheet,
        "Rows":len(df),
        "Columns":len(df.columns),
        "Missing_Cells":int(df.isna().sum().sum()),
        "Duplicate_Rows":int(df.duplicated().sum())
    })
    summary_df = pd.DataFrame(summary)
    print("\nDATASET SUMMARY")
    print("-" * 70)
    print(summary_df. to_string(index=False))

    print("\n" + "_" * 70)
    print("POTENTIAL DATA-QUALITY ISSUES")
    print("=" * 70)

    df = pd.read_excel(file_path, sheet_name="Delays_Downtime")
    print(
        "\nDelays_Downtime - Negative durations:",
        (df["Duration"] < 0).sum()
    )

    df = pd.read_excel(file_path, sheet_name="Maintenance_Notifications")
    print(
        "Maintenance_Notifications - Negative downtime:",
        (df["Downtime_Hours"] < 0).sum()
    )
    df = pd.read_excel(file_path, sheet_name="Shift_Performance")

print(
    "Shift_Performance - Negative loads:",
    (df["Loads"] < 0).sum()
)

print(
    "Shift_Performance - Actual hours > scheduled hours:",
    (df["Actual_Hours"] > df["Scheduled_Hours"]).sum()
)

print(
    "Shift_Performance - Availability outside 0-1:",
    (
        (df["Availability_Pct"] < 0) |
        (df["Availability_Pct"] > 1)
    ).sum()
)
df = pd.read_excel(file_path, sheet_name="Training_Records")

print(
    "Training_Records - Scores outside 0-100:",
    (
        (df["Score"] < 0) |
        (df["Score"] > 100)
    ).sum()
)
df = pd.read_excel(file_path, sheet_name="Environmental_Readings")

print(
    "Environmental_Readings - Negative values:",
    (df["Value"] < 0).sum()
)

print(
    "Environmental_Readings - Dust values > 1000:",
    (
        (df["Reading_Type"].str.lower() == "dust") &
        (df["Value"] > 1000)
    ).sum()
)
df = pd.read_excel(file_path, sheet_name="Access_Control")

print(
    "Access_Control - Event times containing 2027:",
    df["Event_Time"].astype(str).str.contains("2027").sum()
)
print("\n" + "=" * 70)
print("CATEGORICAL VALUE REVIEW")
print("=" * 70)

checks = {
    "Equipment_Events": ["Equipment_Name", "Event_Type", "Status"],
    "Delays_Downtime": ["Delay_Category"],
    "Operator_Activities": ["Activity_Type"],
    "Safety_Observations": ["Category", "Severity"],
    "Training_Records": ["Course_Code"],
    "Maintenance_Notifications": ["Notification_Type", "Priority"],
    "Access_Control": ["Direction", "Access_Result"]
}

for sheet, columns in checks.items():

    df = pd.read_excel(file_path, sheet_name=sheet)

    print(f"\n{sheet}")

    for column in columns:
        values = sorted(df[column].dropna().astype(str).unique())
        print(f"{column}: {values}")
        print("\n" + "=" * 70)
print("INSPECTION COMPLETE")
print("=" * 70)
print("\n" + "=" * 70)
print("RECORDS REQUIRING REVIEW")
print("=" * 70)

df = pd.read_excel(file_path, sheet_name="Delays_Downtime")

print("\nNegative delay duration:")
print(df[df["Duration"] < 0].to_string(index=False))

df = pd.read_excel(file_path, sheet_name="Maintenance_Notifications")

print("\nNegative maintenance downtime:")
print(df[df["Downtime_Hours"] < 0].to_string(index=False))

df = pd.read_excel(file_path, sheet_name="Shift_Performance")

print("\nNegative loads:")
print(df[df["Loads"] < 0].to_string(index=False))

print("\nActual hours greater than scheduled:")
print(
     df[df["Actual_Hours"] > df["Scheduled_Hours"]]
    .to_string(index=False)
)

print("\nAvailability outside 0-1:")
print(
    df[
        (df["Availability_Pct"] < 0) |
        (df["Availability_Pct"] > 1)
    ].to_string(index=False)
)

df = pd.read_excel(file_path, sheet_name="Training_Records")

print("\nTraining scores outside 0-100:")
print(
    df[
        (df["Score"] < 0) |
        (df["Score"] > 100)
    ].to_string(index=False)
)
df = pd.read_excel(file_path, sheet_name="Environmental_Readings")

print("\nNegative environmental readings:")
print(
    df[df["Value"] < 0].to_string(index=False)
)

print("\nVery high dust readings:")
print(
    df[
        (df["Reading_Type"].str.lower() == "dust") &
        (df["Value"] > 1000)
    ].to_string(index=False)
)


df = pd.read_excel(file_path, sheet_name="Access_Control")

print("\nAccess events containing 2027:")
print(
    df[
        df["Event_Time"].astype(str).str.contains("2027")
    ].to_string(index=False)
)
print("\nAvailability values:")
df = pd.read_excel(file_path, sheet_name="Shift_Performance")
print(df["Availability_Pct"].unique())
print("\nAvailability definition:")
dictionary = pd.read_excel(file_path, sheet_name="Data_Dictionary")

print(
    dictionary[
        dictionary.astype(str).apply(
            lambda row: row.str.contains("Availability_Pct", case=False).any(),
            axis=1
        )
    ].to_string(index=False)
)
print("\nAvailability above 100%:")

print(
    df[df["Availability_Pct"] > 1]
    .to_string(index=False)
)
print("\n" + "=" * 70)
print("CATEGORICAL VALUES TO REVIEW")
print("=" * 70)

checks = {
    "Equipment_Events": ["Equipment_Name", "Event_Type", "Status"],
    "Delays_Downtime": ["Delay_Category"],
    "Operator_Activities": ["Activity_Type"],
    "Safety_Observations": ["Category", "Severity"],
    "Maintenance_Notifications": ["Notification_Type", "Priority"],
    "Access_Control": ["Direction", "Access_Result"]
}

for sheet, columns in checks.items():

    df = pd.read_excel(file_path, sheet_name=sheet)

    print(f"\n{sheet}")

    for column in columns:
        print(f"\n{column}:")
        print(sorted(df[column].dropna().astype(str).unique()))
        print("\n" + "=" * 70)
print("DATA DICTIONARY")
print("=" * 70)

dictionary = pd.read_excel(
    file_path,
    sheet_name="Data_Dictionary"
)

print(dictionary.to_string(index=False))
print("\n" + "=" * 70)
print("DATE AND TIME CHECK")
print("=" * 70)

date_columns = {
    "Equipment_Events": ["Event_Time"],
    "Delays_Downtime": ["Start_Time", "End_Time"],
    "Shift_Performance": ["Shift_Date"],
    "Safety_Observations": ["Observation_Date", "Closed_Date"],
    "Training_Records": ["Completion_Date", "Expiry_Date"],
    "Maintenance_Notifications": ["Raised_Date"],
    "Environmental_Readings": ["Reading_Time"],
    "Access_Control": ["Event_Time"]
}

for sheet, columns in date_columns.items():

    df = pd.read_excel(file_path, sheet_name=sheet)

    print(f"\n{sheet}")

    for column in columns:

        dates = pd.to_datetime(
            df[column],
            errors="coerce",
            dayfirst=True
        )

        print(
            column,
            "- invalid:",
            dates.isna().sum(),
            "| earliest:",
            dates.min(),
            "| latest:",
            dates.max()
        )
        print("\n" + "=" * 70)
print("RAW DATE FORMAT CHECK")
print("=" * 70)

for sheet in [
    "Equipment_Events",
    "Delays_Downtime",
    "Safety_Observations",
    "Training_Records",
    "Maintenance_Notifications",
    "Environmental_Readings",
    "Access_Control"
]:

    df = pd.read_excel(file_path, sheet_name=sheet)

    print(f"\n{sheet}")

    for column in df.columns:

        if "date" in column.lower() or "time" in column.lower():

            values = df[column].dropna().astype(str)

            print(f"{column}:")
            print(values.head(10).tolist())
            training = pd.read_excel(file_path, sheet_name="Training_Records")

print(
    training[
        training["Expiry_Date"].astype(str).str.contains("11/04/2025", na=False)
    ].to_string(index=False)
)