import pandas as pd
from pathlib import Path


#WORKBOOK

folder = Path(__file__).parent

workbooks = [
    f for f in folder.glob("*.xlsx")
    if "Cleaned_Data" not in f.name
    and "Exception_Report" not in f.name
]

if not workbooks:
    raise FileNotFoundError("No Excel workbook was found in the project folder.")

file_path = workbooks[0]

print("Source workbook:", file_path.name)


#ALL SHEETS
sheets = pd.read_excel(file_path, sheet_name=None)

print("Sheets loaded:", list(sheets.keys()))

#RECORD OF CLEANING ACTIONS

exceptions = []
changes = []


def add_exception(dataset, record_id, field, original, issue, action):
    exceptions.append({
        "Dataset": dataset,
        "Record_ID": record_id,
        "Field": field,
        "Original_Value": original,
        "Issue": issue,
        "Action": action
    })


def add_change(dataset, record_id, field, original, cleaned, reason):
    changes.append({
        "Dataset": dataset,
        "Record_ID": record_id,
        "Field": field,
        "Original_Value": original,
        "Cleaned_Value": cleaned,
        "Reason": reason
    })

#EQUIPMENT NAME STANDARDISED

if "Equipment_Events" in sheets:

    df = sheets["Equipment_Events"]

    equipment_map = {
        "TRK 001": "TRK001",
        "TRK-001": "TRK001",
        "truck01": "TRK001",
        "Truck 1": "TRK001",

        "TRK-002": "TRK002",
        "TRK002": "TRK002",
        "truck02": "TRK002",
        "Truck 2": "TRK002",

        "TRK-003": "TRK003",
        "TRK003": "TRK003",
        "truck03": "TRK003",
        "Truck 3": "TRK003",

        "EX 001": "EXC001",
        "EXC-01": "EXC001",
        "EXC001": "EXC001",
        "Excavator 1": "EXC001",

        "EXC-02": "EXC002",
        "EXC002": "EXC002",
        "Excavator 2": "EXC002",

        "DRL001": "DRL001",
        "Drill 01": "DRL001"
    }

    for index, value in df["Equipment_Name"].items():

        if pd.isna(value):
            continue

        if value in equipment_map:
            cleaned = equipment_map[value]

            if value != cleaned:
                record_id = df.loc[index, "Event_ID"]

                add_change(
                    "Equipment_Events",
                    record_id,
                    "Equipment_Name",
                    value,
                    cleaned,
                    "Standardised equipment name using canonical examples in the Data Dictionary."
                )

                df.loc[index, "Equipment_Name"] = cleaned

    sheets["Equipment_Events"] = df

#CORRECTIONS

corrections = {
    "Equipment_Events": {
        "Event_Type": {
            "start": "Start"
        },
        "Status": {
            "closed": "Closed"
        }
    },

    "Delays_Downtime": {
        "Delay_Category": {
            "mechanical": "Mechanical",
            "Mecanical": "Mechanical"
        }
    },

    "Operator_Activities": {
        "Activity_Type": {
            "hualing": "Hauling"
        }
    },

    "Safety_Observations": {
        "Category": {
            "Saftey": "Safety"
        },
        "Severity": {
            "low": "Low"
        }
    }
}


for dataset, fields in corrections.items():

    if dataset not in sheets:
        continue

    df = sheets[dataset]

    for field, mapping in fields.items():

        if field not in df.columns:
            continue

        for index, value in df[field].items():

            if value in mapping:

                cleaned = mapping[value]

                record_id = None

                if "Event_ID" in df.columns:
                    record_id = df.loc[index, "Event_ID"]
                elif "Shift_Record_ID" in df.columns:
                    record_id = df.loc[index, "Shift_Record_ID"]
                elif "Training_Record_ID" in df.columns:
                    record_id = df.loc[index, "Training_Record_ID"]
                elif "Observation_ID" in df.columns:
                    record_id = df.loc[index, "Observation_ID"]

                add_change(
                    dataset,
                    record_id,
                    field,
                    value,
                    cleaned,
                    "Corrected clear spelling/capitalisation inconsistency."
                )

                df.loc[index, field] = cleaned

    sheets[dataset] = df

#RECORD MISSING Equipment_Name AS AN EXCEPTION

if "Equipment_Events" in sheets:

    df = sheets["Equipment_Events"]

    missing = df[df["Equipment_Name"].isna()]

    for index, row in missing.iterrows():

        add_exception(
            "Equipment_Events",
            row["Event_ID"],
            "Equipment_Name",
            "",
            "Missing equipment name",
            "Flagged for review. No value invented."
        )

#REMOVE DUPLICATE RECORDS

for dataset, df in sheets.items():

    duplicate_rows = df[df.duplicated(keep="first")]

    for index, row in duplicate_rows.iterrows():

        record_id = None

        for possible_id in [
            "Event_ID",
            "Shift_Record_ID",
            "Training_Record_ID",
            "Observation_ID",
            "Notification_ID",
            "Access_ID"
        ]:
            if possible_id in df.columns:
                record_id = row[possible_id]
                break

        add_change(
            dataset,
            record_id,
            "Entire record",
            "Duplicate row",
            "Removed duplicate copy",
            "Exact duplicate retained once."
        )

    sheets[dataset] = df.drop_duplicates().reset_index(drop=True)

#NEGATIVE DOWNTIME
if "Delays_Downtime" in sheets:

    df = sheets["Delays_Downtime"]

    if "Duration" in df.columns:

        for index, row in df[df["Duration"] < 0].iterrows():

            record_id = row.get("Delay_ID", row.get("Record_ID", index))

            add_exception(
                "Delays_Downtime",
                record_id,
                "Duration",
                row["Duration"],
                "Negative duration",
                "Flagged for review. Correct value cannot be inferred safely."
            )

    if "Loads" in df.columns:

        for index, row in df[df["Loads"] < 0].iterrows():

            record_id = row.get("Delay_ID", row.get("Record_ID", index))

            add_exception(
                "Delays_Downtime",
                record_id,
                "Loads",
                row["Loads"],
                "Negative load count",
                "Flagged for review. Original value retained."
            )

#SHIFT PERFORMANCE ANOMALIES

if "Shift_Performance" in sheets:

    df = sheets["Shift_Performance"]

    if "Actual_Hours" in df.columns and "Scheduled_Hours" in df.columns:

        bad_hours = df[df["Actual_Hours"] > df["Scheduled_Hours"]]

        for index, row in bad_hours.iterrows():

            add_exception(
                "Shift_Performance",
                row["Shift_Record_ID"],
                "Actual_Hours",
                row["Actual_Hours"],
                "Actual hours exceed scheduled hours",
                "Flagged for review. Original values retained."
            )

    if "Availability_Pct" in df.columns:

        bad_availability = df[
            (df["Availability_Pct"] < 0) |
            (df["Availability_Pct"] > 1)
        ]

        for index, row in bad_availability.iterrows():

            add_exception(
                "Shift_Performance",
                row["Shift_Record_ID"],
                "Availability_Pct",
                row["Availability_Pct"],
                "Outside expected 0% to 100% range",
                "Flagged for review. Original value retained."
            )

#TRAINING ANOMALIES

if "Training_Records" in sheets:

    df = sheets["Training_Records"]

    if "Score" in df.columns:

        bad_scores = df[
            (df["Score"] < 0) |
            (df["Score"] > 100)
        ]

        for index, row in bad_scores.iterrows():

            add_exception(
                "Training_Records",
                row["Training_Record_ID"],
                "Score",
                row["Score"],
                "Training score outside 0-100 range",
                "Flagged for review. Original value retained."
            )

#ENVIRONMENTAL ANOMALIES

if "Environmental_Readings" in sheets:

    df = sheets["Environmental_Readings"]

    if "Value" in df.columns:

        negative_values = df[df["Value"] < 0]

        for index, row in negative_values.iterrows():

            record_id = row.get(
                "Reading_ID",
                row.get("Record_ID", index)
            )

            add_exception(
                "Environmental_Readings",
                record_id,
                "Value",
                row["Value"],
                "Negative environmental reading",
                "Flagged for review. Interpretation requires unit and quality-flag context."
            )

        extreme_values = df[df["Value"] > 1000]

        for index, row in extreme_values.iterrows():

            record_id = row.get(
                "Reading_ID",
                row.get("Record_ID", index)
            )

            add_exception(
                "Environmental_Readings",
                record_id,
                "Value",
                row["Value"],
                "Extremely high environmental reading",
                "Flagged for review. No automatic correction applied."
            )

#TRAINING EXCEPTION

if "Training_Records" in sheets:

    df = sheets["Training_Records"]

    matching = df[
        df["Training_Record_ID"].astype(str) == "TRN0008"
    ]

    for index, row in matching.iterrows():

        add_exception(
            "Training_Records",
            row["Training_Record_ID"],
            "Expiry_Date",
            row["Expiry_Date"],
            "Date format is ambiguous and may place expiry before completion.",
            "Flagged for review. Original value retained."
        )

#ACCESS-CONTROL FUTURE-DATE

if "Access_Control" in sheets:

    df = sheets["Access_Control"]

    for index, row in df.iterrows():

        value = str(row.get("Event_Time", ""))

        if "2027" in value:

            record_id = row.get(
                "Access_ID",
                row.get("Record_ID", index)
            )

            add_exception(
                "Access_Control",
                record_id,
                "Event_Time",
                value,
                "Access event dated in 2027",
                "Flagged for review. Original value retained."
            )

#SAVED CLEANED WORKBOOK

cleaned_file = folder / "Cleaned_Data.xlsx"

with pd.ExcelWriter(cleaned_file, engine="openpyxl") as writer:

    for dataset, df in sheets.items():
        df.to_excel(writer, sheet_name=dataset, index=False)

#SAVED EXCEPTION REPORT

exception_file = folder / "Exception_Report.xlsx"

exception_df = pd.DataFrame(exceptions)

with pd.ExcelWriter(exception_file, engine="openpyxl") as writer:

    exception_df.to_excel(
        writer,
        sheet_name="Exceptions",
        index=False
    )

    pd.DataFrame(changes).to_excel(
        writer,
        sheet_name="Changes_Made",
        index=False
    )

#FINAL PRINT

print("\n" + "=" * 70)
print("TASK 1 CLEANING COMPLETE")
print("=" * 70)

print("\nCleaned workbook:")
print(cleaned_file.name)

print("\nException report:")
print(exception_file.name)

print("\nChanges made:", len(changes))
print("Exceptions recorded:", len(exceptions))

print("\nTask 1 files created successfully.")