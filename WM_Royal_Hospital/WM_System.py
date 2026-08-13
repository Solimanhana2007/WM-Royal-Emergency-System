import pandas as pd
import os

folder = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(folder, "WM_Royal_Emergency_System_Data.xlsx")

patients = pd.read_excel(file, sheet_name="Patients_150")
ambulances = pd.read_excel(file, sheet_name="Ambulances_20")
facilities = pd.read_excel(file, sheet_name="Facilities")


def triage_patient(patient):
    complaint = str(patient["Call_Transcript"]).lower()
    heart_rate = float(patient["Heart_Rate"])
    spo2 = float(patient["SpO2"])

    if (
        spo2 < 90
        or any(
            x in complaint
            for x in ["unresponsive", "icu", "newborn", "severe chest pain"]
        )
    ):
        severity = "Critical"
    elif (
        spo2 < 94
        or heart_rate > 120
        or any(x in complaint for x in ["severe", "breathing difficulty"])
    ):
        severity = "High"
    elif heart_rate > 100 or any(x in complaint for x in ["moderate", "persistent"]):
        severity = "Medium"
    else:
        severity = "Low"

    if "newborn" in complaint:
        capability = "Neonatal"
    elif "pregnant" in complaint:
        capability = "Maternal"
    elif "icu" in complaint or severity == "Critical":
        capability = "Critical Care"
    else:
        capability = "General Emergency"

    return severity, capability


for i, patient in patients.iterrows():
    severity, capability = triage_patient(patient)
    patients.at[i, "AI_Severity"] = severity
    patients.at[i, "AI_Required_Capability"] = capability


def select_facility(patient):
    severity = patient["AI_Severity"]
    capability = patient["AI_Required_Capability"]
    location = str(patient["Location"])

    if severity == "Critical" or capability in ["Critical Care", "Maternal", "Neonatal"]:
        hospital = facilities[facilities["Facility_ID"] == "H-01"]
        return hospital["Facility_Name"].iloc[0]

    for _, facility in facilities.iterrows():
        if (
            facility["Facility_ID"] != "H-01"
            and location in str(facility["Facility_Name"])
            and severity in str(facility["Accepts_Severity"])
        ):
            return facility["Facility_Name"]

    hospital = facilities[facilities["Facility_ID"] == "H-01"]
    return hospital["Facility_Name"].iloc[0]


patients["Assigned_Facility"] = patients.apply(select_facility, axis=1)


def select_ambulance(patient):
    capability = patient["AI_Required_Capability"]
    available = ambulances[ambulances["Status"] == "Available"].copy()

    if available.empty:
        return "No Ambulance Available"

    if capability == "Critical Care":
        specialized = available[available["Critical_Care"] == "Yes"]
        if not specialized.empty:
            ambulance_id = specialized.iloc[0]["Ambulance_ID"]
            ambulances.loc[ambulances["Ambulance_ID"] == ambulance_id, "Status"] = "Dispatched"
            return ambulance_id

    elif capability == "Neonatal":
        specialized = available[available["Neonatal"] == "Yes"]
        if not specialized.empty:
            ambulance_id = specialized.iloc[0]["Ambulance_ID"]
            ambulances.loc[ambulances["Ambulance_ID"] == ambulance_id, "Status"] = "Dispatched"
            return ambulance_id

    elif capability == "Maternal":
        specialized = available[available["Maternal"] == "Yes"]
        if not specialized.empty:
            ambulance_id = specialized.iloc[0]["Ambulance_ID"]
            ambulances.loc[ambulances["Ambulance_ID"] == ambulance_id, "Status"] = "Dispatched"
            return ambulance_id

    general = available[
        (available["Can_Handle_General_Emergency"] == "Yes")
        & (available["Equipment_Level"].isin(["Full", "Critical Care"]))
    ]

    if not general.empty:
        ambulance_id = general.iloc[0]["Ambulance_ID"]
        ambulances.loc[ambulances["Ambulance_ID"] == ambulance_id, "Status"] = "Dispatched"
        return ambulance_id

    fallback = available[available["Can_Handle_General_Emergency"] == "Yes"]

    if not fallback.empty:
        ambulance_id = fallback.iloc[0]["Ambulance_ID"]
        ambulances.loc[ambulances["Ambulance_ID"] == ambulance_id, "Status"] = "Dispatched"
        return ambulance_id

    return "No Ambulance Available"


patients["Assigned_Ambulance"] = patients.apply(select_ambulance, axis=1)


def run_trip(ambulance_id):
    if ambulance_id == "No Ambulance Available":
        return "Not Dispatched"

    index = ambulances.index[ambulances["Ambulance_ID"] == ambulance_id]

    if len(index) == 0:
        return "Not Dispatched"

    i = index[0]

    ambulances.at[i, "Status"] = "At Patient"
    ambulances.at[i, "Status"] = "Transporting"
    ambulances.at[i, "Status"] = "Arrived"
    ambulances.at[i, "Status"] = "Available"

    return "Completed"


patients["Trip_Status"] = patients["Assigned_Ambulance"].apply(run_trip)

print("Patients loaded:", len(patients))
print("Ambulances loaded:", len(ambulances))
print("Facilities loaded:", len(facilities))

print("\n--- PATIENT PROCESSING COMPLETE ---")
print(patients["AI_Severity"].value_counts())

print("\n--- FIRST 10 PATIENTS ---")
print(
    patients[
        [
            "Patient_ID",
            "Call_Transcript",
            "AI_Severity",
            "AI_Required_Capability",
        ]
    ].head(10)
)

print("\n--- FACILITY SELECTION COMPLETE ---")
print(
    patients[
        [
            "Patient_ID",
            "Location",
            "AI_Severity",
            "AI_Required_Capability",
            "Assigned_Facility",
        ]
    ].head(15)
)

print("\n--- AMBULANCE SELECTION COMPLETE ---")
print(
    patients[
        [
            "Patient_ID",
            "AI_Severity",
            "AI_Required_Capability",
            "Assigned_Facility",
            "Assigned_Ambulance",
            "Trip_Status",
        ]
    ].head(20)
)

print("\n--- AMBULANCE STATUS ---")
print(ambulances[["Ambulance_ID", "Status"]])