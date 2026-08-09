# ============================================================
# MIMIC PATIENT ANALYTICS
# PATIENT TIMELINE
# ============================================================

import pandas as pd


# ============================================================
# PATIENT OVERVIEW
# ============================================================

def patient_overview(
    subject_id,
    patients,
    admissions,
    icustays
):
    """
    Return a high-level overview for one patient.
    """

    patient = patients[
        patients["subject_id"] == subject_id
    ].copy()

    patient_admissions = admissions[
        admissions["subject_id"] == subject_id
    ].copy()

    patient_icu = icustays[
        icustays["subject_id"] == subject_id
    ].copy()

    return {
        "patient": patient,
        "admissions": patient_admissions,
        "icu_stays": patient_icu,
        "total_admissions": len(
            patient_admissions
        ),
        "total_icu_stays": len(
            patient_icu
        )
    }


# ============================================================
# ADMISSION TIMELINE
# ============================================================

def admission_timeline(
    subject_id,
    hadm_id,
    admissions=None,
    icustays=None,
    diagnoses=None,
    procedures=None,
    prescriptions=None,
    pharmacy=None,
    emar=None,
    microbiology=None,
    labevents=None,
    chartevents=None
):
    """
    Build a unified event timeline for one admission.

    Each source contributes its own event type.
    """

    events = []

    # --------------------------------------------------------
    # Admission
    # --------------------------------------------------------

    if admissions is not None:

        adm = admissions[
            (admissions["subject_id"] == subject_id)
            & (admissions["hadm_id"] == hadm_id)
        ].copy()

        for _, row in adm.iterrows():

            if pd.notna(row.get("admittime")):

                events.append({
                    "event_time":
                        row["admittime"],
                    "event_type":
                        "Admission",
                    "source":
                        "admissions",
                    "description":
                        row.get(
                            "admission_type",
                            ""
                        )
                })

            if pd.notna(row.get("dischtime")):

                events.append({
                    "event_time":
                        row["dischtime"],
                    "event_type":
                        "Discharge",
                    "source":
                        "admissions",
                    "description":
                        row.get(
                            "discharge_location",
                            ""
                        )
                })

    # --------------------------------------------------------
    # ICU
    # --------------------------------------------------------

    if icustays is not None:

        icu = icustays[
            (icustays["subject_id"] == subject_id)
            & (icustays["hadm_id"] == hadm_id)
        ].copy()

        for _, row in icu.iterrows():

            events.append({
                "event_time":
                    row["intime"],
                "event_type":
                    "ICU Admission",
                "source":
                    "icustays",
                "description":
                    row.get(
                        "first_careunit",
                        ""
                    )
            })

            events.append({
                "event_time":
                    row["outtime"],
                "event_type":
                    "ICU Discharge",
                "source":
                    "icustays",
                "description":
                    row.get(
                        "last_careunit",
                        ""
                    )
            })

    # --------------------------------------------------------
    # Diagnoses
    # --------------------------------------------------------

    if diagnoses is not None:

        dx = diagnoses[
            (diagnoses["subject_id"] == subject_id)
            & (diagnoses["hadm_id"] == hadm_id)
        ].copy()

        for _, row in dx.iterrows():

            events.append({
                "event_time": pd.NaT,
                "event_type":
                    "Diagnosis",
                "source":
                    "diagnoses_icd",
                "description":
                    str(
                        row.get(
                            "icd_code",
                            ""
                        )
                    )
            })

    # --------------------------------------------------------
    # Procedures
    # --------------------------------------------------------

    if procedures is not None:

        proc = procedures[
            (procedures["subject_id"] == subject_id)
            & (procedures["hadm_id"] == hadm_id)
        ].copy()

        for _, row in proc.iterrows():

            events.append({
                "event_time":
                    row.get(
                        "chartdate",
                        pd.NaT
                    ),
                "event_type":
                    "Procedure",
                "source":
                    "procedures_icd",
                "description":
                    str(
                        row.get(
                            "icd_code",
                            ""
                        )
                    )
            })

    # --------------------------------------------------------
    # Prescriptions
    # --------------------------------------------------------

    if prescriptions is not None:

        meds = prescriptions[
            (prescriptions["subject_id"] == subject_id)
            & (prescriptions["hadm_id"] == hadm_id)
        ].copy()

        for _, row in meds.iterrows():

            events.append({
                "event_time":
                    row.get(
                        "starttime",
                        pd.NaT
                    ),
                "event_type":
                    "Prescription",
                "source":
                    "prescriptions",
                "description":
                    row.get(
                        "drug",
                        ""
                    )
            })

    # --------------------------------------------------------
    # Pharmacy
    # --------------------------------------------------------

    if pharmacy is not None:

        pharm = pharmacy[
            (pharmacy["subject_id"] == subject_id)
            & (pharmacy["hadm_id"] == hadm_id)
        ].copy()

        for _, row in pharm.iterrows():

            events.append({
                "event_time":
                    row.get(
                        "starttime",
                        pd.NaT
                    ),
                "event_type":
                    "Pharmacy",
                "source":
                    "pharmacy",
                "description":
                    row.get(
                        "medication",
                        ""
                    )
            })

    # --------------------------------------------------------
    # eMAR
    # --------------------------------------------------------

    if emar is not None:

        medication_events = emar[
            (emar["subject_id"] == subject_id)
            & (emar["hadm_id"] == hadm_id)
        ].copy()

        for _, row in medication_events.iterrows():

            events.append({
                "event_time":
                    row.get(
                        "charttime",
                        pd.NaT
                    ),
                "event_type":
                    "Medication Administration",
                "source":
                    "emar",
                "description":
                    row.get(
                        "medication",
                        ""
                    )
            })

    # --------------------------------------------------------
    # Microbiology
    # --------------------------------------------------------

    if microbiology is not None:

        micro = microbiology[
            (microbiology["subject_id"] == subject_id)
            & (microbiology["hadm_id"] == hadm_id)
        ].copy()

        for _, row in micro.iterrows():

            events.append({
                "event_time":
                    row.get(
                        "charttime",
                        pd.NaT
                    ),
                "event_type":
                    "Microbiology",
                "source":
                    "microbiologyevents",
                "description":
                    row.get(
                        "test_name",
                        ""
                    )
            })

    # --------------------------------------------------------
    # Laboratory Events
    # --------------------------------------------------------

    if labevents is not None:

        labs = labevents[
            (labevents["subject_id"] == subject_id)
            & (labevents["hadm_id"] == hadm_id)
        ].copy()

        for _, row in labs.iterrows():

            events.append({
                "event_time":
                    row.get(
                        "charttime",
                        pd.NaT
                    ),
                "event_type":
                    "Laboratory",
                "source":
                    "labevents",
                "description":
                    str(
                        row.get(
                            "itemid",
                            ""
                        )
                    )
            })

    # --------------------------------------------------------
    # Chart Events
    # --------------------------------------------------------

    if chartevents is not None:

        charts = chartevents[
            (chartevents["subject_id"] == subject_id)
            & (chartevents["hadm_id"] == hadm_id)
        ].copy()

        for _, row in charts.iterrows():

            events.append({
                "event_time":
                    row.get(
                        "charttime",
                        pd.NaT
                    ),
                "event_type":
                    "Chart Event",
                "source":
                    "chartevents",
                "description":
                    str(
                        row.get(
                            "itemid",
                            ""
                        )
                    )
            })

    # --------------------------------------------------------
    # Build DataFrame
    # --------------------------------------------------------

    timeline = pd.DataFrame(events)

    if timeline.empty:
        return timeline

    timeline["event_time"] = pd.to_datetime(
        timeline["event_time"],
        errors="coerce"
    )

    timeline = timeline.sort_values(
        "event_time",
        na_position="last"
    ).reset_index(drop=True)

    return timeline


# ============================================================
# PATIENT EVENT COUNTS
# ============================================================

def patient_event_counts(
    subject_id,
    admissions,
    icustays,
    diagnoses,
    procedures,
    prescriptions,
    pharmacy,
    emar,
    microbiology,
    labevents,
    chartevents
):
    """
    Count events associated with one patient.
    """

    return {
        "admissions":
            len(
                admissions[
                    admissions["subject_id"]
                    == subject_id
                ]
            ),

        "icu_stays":
            len(
                icustays[
                    icustays["subject_id"]
                    == subject_id
                ]
            ),

        "diagnoses":
            len(
                diagnoses[
                    diagnoses["subject_id"]
                    == subject_id
                ]
            ),

        "procedures":
            len(
                procedures[
                    procedures["subject_id"]
                    == subject_id
                ]
            ),

        "prescriptions":
            len(
                prescriptions[
                    prescriptions["subject_id"]
                    == subject_id
                ]
            ),

        "pharmacy":
            len(
                pharmacy[
                    pharmacy["subject_id"]
                    == subject_id
                ]
            ),

        "emar":
            len(
                emar[
                    emar["subject_id"]
                    == subject_id
                ]
            ),

        "microbiology":
            len(
                microbiology[
                    microbiology["subject_id"]
                    == subject_id
                ]
            ),

        "lab_events":
            len(
                labevents[
                    labevents["subject_id"]
                    == subject_id
                ]
            ),

        "chart_events":
            len(
                chartevents[
                    chartevents["subject_id"]
                    == subject_id
                ]
            )
    }
