import streamlit as st
import pandas as pd
from pathlib import Path


#LOAD CLEANED DATA
folder = Path(__file__).parent
file_path = folder / "Cleaned_Data.xlsx"

equipment = pd.read_excel(
    file_path,
    sheet_name="Equipment_Events"
)
equipment = pd.read_excel(
    file_path,
    sheet_name="Equipment_Events"
)


#LOAD THE TASK 1 EXCEPTION REPORT
exception_file = folder / "Exception_Report.xlsx"

exceptions = pd.read_excel(
    exception_file,
    sheet_name="Exceptions"
)

# Page setup
st.set_page_config(
    page_title="Project Signal - Operational Triage",
    layout="wide"
)

st.title("Project Signal")
st.subheader("Operational Event Triage")

st.write(
    "This prototype provides decision support for reviewing "
    "equipment events. Final operational decisions remain "
    "with an appropriately authorised human reviewer."
)


#SELECT AN EVENT
event_ids = equipment["Event_ID"].dropna().tolist()

selected_event = st.selectbox(
    "Select an equipment event",
    event_ids
)


#GET SELECTED RECORD
event = equipment[
    equipment["Event_ID"] == selected_event
].iloc[0]


st.divider()

st.subheader("Event details")

col1, col2 = st.columns(2)

with col1:
    st.write("**Event ID:**", event["Event_ID"])
    st.write("**Equipment:**", event["Equipment_Name"])
    st.write("**Event type:**", event["Event_Type"])

with col2:
    st.write("**Status:**", event["Status"])
    st.write("**Location:**", event.get("Location", "Not available"))
    st.write("**Event time:**", event["Event_Time"])


#TRIAGE RULES

event_type = str(event["Event_Type"]).strip().lower()
status = str(event["Status"]).strip().lower()

priority = "Low"
reason = "No high-priority trigger identified."
action = "Review during normal operational monitoring."


if event_type == "fault":
    priority = "High"
    reason = "The event is recorded as a fault."
    action = (
        "Review the equipment condition and assign the event "
        "to the appropriate maintenance or operations team."
    )

elif event_type == "stop" and status == "open":
    priority = "High"
    reason = "The equipment has a stop event that is still open."
    action = (
        "Review the stop reason and escalate to the relevant "
        "operations or maintenance team."
    )

elif event_type == "stop":
    priority = "Medium"
    reason = "The equipment has a recorded stop event."
    action = (
        "Review the stop reason and confirm whether any "
        "follow-up action is required."
    )

elif event_type == "inspection":
    priority = "Medium"
    reason = "The event is associated with an inspection."
    action = (
        "Confirm that the inspection has been completed and "
        "that any findings have been appropriately recorded."
    )

elif event_type == "start":
    priority = "Low"
    reason = "The event records equipment start-up activity."
    action = "Continue normal operational monitoring."

elif event_type == "idle":
    priority = "Low"
    reason = "The event records equipment idle activity."
    action = "Review during normal operational monitoring."

#DISPLAY RESULTS
st.divider()

st.subheader("Triage result")

st.metric(
    "Priority",
    priority
)

st.write("**Reason:**", reason)

st.write("**Recommended action:**", action)
#CHECK DATA-QUALITY ISSUES
event_exceptions = exceptions[
    exceptions["Record_ID"].astype(str) == str(selected_event)
]

if not event_exceptions.empty:
    st.warning(
        "This event has a known data-quality exception from the "
        "Task 1 data-quality review. Review the underlying data "
        "before relying on the triage result."
    )

    st.write("**Data-quality issue(s):**")

    for _, issue in event_exceptions.iterrows():
        st.write(
            f"- {issue['Field']}: {issue['Issue']}"
        )


st.divider()

st.subheader("Responsible use")

st.info(
    "This tool provides decision support and does not replace "
    "human judgement. A triage result should not be treated as "
    "proof of fault, misconduct, or individual performance."
)

st.write(
    "**Review requirements:**"
)

st.write(
    "- Check the underlying event and data quality before taking action."
)

st.write(
    "- Do not use the triage result as the sole basis for disciplinary decisions."
)

st.write(
    "- Access and use operational or personal information only for an authorised purpose."
)

st.write(
    "- An appropriately authorised human reviewer remains responsible for the final decision."
)