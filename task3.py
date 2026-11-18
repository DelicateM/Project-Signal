import pandas as pd
from pathlib import Path


folder = Path(__file__).parent
file_path = folder / "Cleaned_Data.xlsx"


#LOAD DATASETS NEEDED FOR TASK 3
delays = pd.read_excel(
    file_path,
    sheet_name="Delays_Downtime"
)

equipment = pd.read_excel(
    file_path,
    sheet_name="Equipment_Events"
)


print("Task 3 data loaded successfully.")
print()
print("Delays_Downtime:", delays.shape)
print("Equipment_Events:", equipment.shape)
#DOWNTIME TO MINUTES
delays["Duration_Minutes"] = delays["Duration"]

delays.loc[
    delays["Duration_Unit"].str.lower() == "hours",
    "Duration_Minutes"
] = delays["Duration"] * 60


#IDENTIFY INVALID NEGATIVE DURATIONS
invalid_durations = delays[
    delays["Duration_Minutes"] < 0
]

print("Negative duration records:")
print(
    invalid_durations[
        ["Equipment_Name", "Duration", "Duration_Unit", "Delay_Category"]
    ].to_string(index=False)
)


#EXCLUDE INVALID DURATIONS FROM DOWNTIME TOTAL
valid_delays = delays[
    delays["Duration_Minutes"] >= 0
].copy()


#CALCULATE TOTAL DOWNTIME BY EQUIPMENT
downtime_by_equipment = (
    valid_delays
    .groupby("Equipment_Name")["Duration_Minutes"]
    .sum()
    .sort_values(ascending=False)
)


print()
print("Downtime by equipment:")
print(downtime_by_equipment.to_string())
def investigate_downtime():
    print()
    print("=" * 60)
    print("DOWNTIME INVESTIGATION")
    print("=" * 60)

    top_asset = downtime_by_equipment.index[0]
    top_value = downtime_by_equipment.iloc[0]

    print(f"Highest recorded downtime: {top_asset}")
    print(f"Recorded downtime: {top_value:.0f} minutes")

    asset_records = valid_delays[
        valid_delays["Equipment_Name"] == top_asset
    ]

    print()
    print("Supporting records:")
    print(
        asset_records[
            [
                "Equipment_Name",
                "Start_Time",
                "End_Time",
                "Duration",
                "Duration_Unit",
                "Delay_Category"
            ]
        ].to_string(index=False)
    )

    print()
    print("Data-quality review:")

    for _, row in asset_records.iterrows():
        if row["Duration_Unit"].lower() == "hours":
            recorded_minutes = row["Duration"] * 60
        else:
            recorded_minutes = row["Duration"]

        if recorded_minutes == 14400:
            print(
                "- Duration mismatch: recorded 14400 minutes "
                "but timestamps span 60 minutes."
            )

    print()
    print(
        "Conclusion: The highest recorded downtime should be "
        "reviewed before being used for an operational decision."
    )


investigate_downtime()