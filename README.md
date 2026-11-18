Project Signal — Evidence-Grounded Operational Assistant
OVERVIEW

This project is an operational data analysis and decision-support solution built with Python and Streamlit.

It processes operational data from a fictional mining environment and provides three main capabilities:

Data cleaning and quality checking
Equipment-event triage
Evidence-grounded operational investigation

The system is designed to support human decision-making rather than make autonomous operational decisions.

The project identifies data-quality issues, provides evidence for findings and highlights situations where further human verification is required.

DESIGN OVERVIEW
COMPONENTS
-DATA CLEANING

Listed as task1.py on files, it loads the supplied Project_Signal_Source.xlsx workbook, performs data-quality checks and produces:

Cleaned_Data.xlsx
Exception_Report.xlsx

The cleaning process standardises supported inconsistencies while retaining issues that cannot safely be corrected without additional evidence.

-EQUIPMENT TRIAGE

The equipment-event application uses the cleaned equipment-event data to classify events according to their operational priority.

It considers information such as:

Event type
Status
Equipment
Location
Known data-quality issues

The application provides:

Priority
Reason
Recommended action
-OPERATIONAL INVESTIGATION

Listed as task3.py / the Task 3 Streamlit application on files, it investigates operational questions using the cleaned data.

The application provides an evidence-based finding, supporting information, data-quality warnings and recommended next steps.

DATA FLOW

-Source workbook

-Data cleaning and quality checks

-Cleaned_Data.xlsx

-Equipment-event triage / Operational investigation

-Evidence-grounded findings

-Human review and decision

TASK 1 — DATA CLEANING

The source workbook contains multiple operational datasets.

The cleaning process checks for issues including:

Missing values
Duplicate or inconsistent identifiers
Inconsistent equipment names
Inconsistent category values
Date and time format differences
Invalid or negative durations
Values outside expected ranges
Data-quality exceptions

The final Task 1 run reported:

103 changes made

9 exceptions recorded

The original source workbook remains unchanged.

TASK 2 — EQUIPMENT EVENT TRIAGE

The equipment-event application provides a structured triage result for each selected event.

Example:

EVT0039

Event type: Fault

Status: Closed

Priority: High

Reason: The event is recorded as a fault.

Recommended action: Review the equipment condition and assign the event to the appropriate maintenance or operations team.

For an open Stop event such as EVT0014, the application identifies the event as high priority because the equipment has a Stop event that is still open.

Known data-quality issues are also surfaced rather than hidden.

TASK 3 — EVIDENCE-GROUNDED OPERATIONAL INVESTIGATION

The Task 3 application investigates operational questions using the cleaned data.

Example question:

Which asset had the highest recorded downtime?

Finding:

TRK-002 — 14,535 minutes

However, the application does not present this number without context.

One supporting TRK-002 record reports: 14,400 minutes

while its recorded timestamps span only: 60 minutes

The system therefore warns that the recorded downtime should be verified before it is used for an operational decision.

EVIDENCE VS DECISION

The system separates:

FINDING

What the available data shows.

EVIDENCE

The records supporting the finding.

DATA-QUALITY CONCERN

Any issue that could affect confidence in the finding.

RECOMMENDED NEXT ACTION

What should be verified before making an operational decision.

The system does not automatically convert a data finding into an operational decision.

RESPONSIBLE USE

The project is designed as decision support.

The system:

Surfaces data-quality issues
Avoids unsupported corrections
Provides evidence for findings
Highlights uncertainty
Recommends human verification
Avoids treating sensitive information as an automatic performance driver

Operational decisions should remain subject to human review.

HOW TO RUN THE APPLICATION LOCALLY:
REQUIREMENTS

Python 3.12+

Pandas

OpenPyXL

Streamlit

SETUP

Open the project folder in VS Code.

Open the terminal.

Install the required packages:
pip install pandas openpyxl streamlit

RUN TASK 1
python task1.py

This produces:

Cleaned_Data.xlsx
Exception_Report.xlsx

RUN THE STREAMLIT APPLICATION (Task 2)

Use the correct application file:

streamlit run app.py

For the Task 3 application:

streamlit run task3_app.py

The terminal will provide a local URL.
