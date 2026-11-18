import pandas as pd
import streamlit as st
from pathlib import Path


st.set_page_config(
    page_title="Project Signal - Operational Assistant",
    layout="wide"
)


#LOAD CLEANED DATA
folder = Path(__file__).parent
file_path = folder / "Cleaned_Data.xlsx"

delays = pd.read_excel(
    file_path,
    sheet_name="Delays_Downtime"
)


st.title("Project Signal")
st.subheader("Evidence-Grounded Operational Assistant")

st.write(
    "Use the assistant to investigate operational questions "
    "using the cleaned Project Signal data."
)


#CONVERT DURATIONS TO MINUTES
delays["Duration_Minutes"] = delays["Duration"]

hours_mask = (
    delays["Duration_Unit"]
    .astype(str)
    .str.lower()
    == "hours"
)

delays.loc[hours_mask, "Duration_Minutes"] = (
    delays.loc[hours_mask, "Duration"] * 60
)


#IGNORE NEGATIVE DURATION WHEN CALCULATING DOWNTIME
valid_delays = delays[
    delays["Duration_Minutes"] >= 0
].copy()


downtime_by_equipment = (
    valid_delays
    .groupby("Equipment_Name")["Duration_Minutes"]
    .sum()
    .sort_values(ascending=False)
)


top_asset = downtime_by_equipment.index[0]
top_value = downtime_by_equipment.iloc[0]


st.markdown("### Operational summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Highest recorded downtime",
        top_asset
    )

with col2:
    st.metric(
        "Recorded downtime",
        f"{top_value:.0f} minutes"
    )

with col3:
    st.metric(
        "Records supporting finding",
        "3"
    )


st.warning(
    "Review required: one supporting TRK-002 record reports "
    "14,400 minutes while its timestamps span only 60 minutes."
)


st.markdown("### Decision summary")

st.write(
    f"**Finding:** {top_asset} has the highest recorded downtime "
    f"at {top_value:.0f} minutes."
)

st.write(
    "**Evidence:** Three TRK-002 downtime records contribute to "
    "the recorded total."
)

st.write(
    "**Data-quality concern:** The mechanical record reports "
    "14,400 minutes, while its recorded timestamps span only "
    "60 minutes."
)

st.write(
    "**Recommended next action:** Verify the affected duration "
    "against the relevant maintenance or operations records "
    "before using the finding for an operational decision."
)


st.divider()


question = st.selectbox(
    "Select a question",
    [
        "Which asset had the highest recorded downtime?",
        "Show the evidence supporting the downtime finding.",
        "What data-quality issue could affect this conclusion?",
        "What additional information is needed before taking action?"
    ]
)


if question == "Which asset had the highest recorded downtime?":

    st.markdown("### Finding")

    st.write(
        f"**{top_asset}** has the highest recorded downtime "
        f"at **{top_value:.0f} minutes**."
    )

    st.warning(
        "This figure should be reviewed before being used for "
        "an operational decision because a data-quality issue "
        "was identified in the supporting records."
    )


elif question == "Show the evidence supporting the downtime finding.":

    st.markdown("### Supporting evidence")

    evidence = valid_delays[
        valid_delays["Equipment_Name"] == top_asset
    ]

    st.dataframe(
        evidence[
            [
                "Equipment_Name",
                "Start_Time",
                "End_Time",
                "Duration",
                "Duration_Unit",
                "Delay_Category"
            ]
        ],
        use_container_width=True
    )


elif question == "What data-quality issue could affect this conclusion?":

    st.markdown("### Data-quality warning")

    st.write(
        "One TRK-002 record reports **14,400 minutes** of "
        "mechanical downtime, while its recorded start and end "
        "times span only **60 minutes**."
    )

    st.warning(
        "The recorded duration should be verified before "
        "TRK-002's total downtime is used for operational decisions."
    )


elif question == "What additional information is needed before taking action?":

    st.markdown("### Additional information needed")

    st.write(
        "The correct duration for the TRK-002 mechanical "
        "downtime record should be confirmed."
    )

    st.write(
        "The relevant maintenance or operations records should "
        "also be reviewed before deciding whether the downtime "
        "represents a genuine operational issue."
    )


st.divider()

st.caption(
    "This assistant provides evidence-grounded decision support. "
    "Operational decisions should remain subject to human review."
)