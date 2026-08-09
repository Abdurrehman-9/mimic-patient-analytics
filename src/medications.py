# ============================================================
# MIMIC PATIENT ANALYTICS
# MEDICATION ANALYTICS
# ============================================================

import pandas as pd


# ============================================================
# LOADERS
# ============================================================

def load_prescriptions(load_dataset):
    """Load prescription records."""
    return load_dataset("prescriptions")


def load_pharmacy(load_dataset):
    """Load pharmacy records."""
    return load_dataset("pharmacy")


def load_emar(load_dataset):
    """Load electronic medication administration records."""
    return load_dataset("emar")


def load_emar_detail(load_dataset):
    """Load detailed medication administration records."""
    return load_dataset("emar_detail")


def load_ingredientevents(load_dataset):
    """Load medication ingredient events."""
    return load_dataset("ingredientevents")


def load_inputevents(load_dataset):
    """Load ICU input events."""
    return load_dataset("inputevents")


# ============================================================
# PRESCRIPTION ANALYTICS
# ============================================================

def prescription_summary(prescriptions):
    """
    High-level prescription statistics.
    """

    return {
        "total_prescriptions": len(prescriptions),

        "unique_patients": prescriptions[
            "subject_id"
        ].nunique(),

        "unique_admissions": prescriptions[
            "hadm_id"
        ].nunique(),

        "unique_medications": prescriptions[
            "drug"
        ].nunique()
    }


def prescriptions_by_drug(prescriptions):
    """
    Rank prescribed drugs by frequency.
    """

    result = (
        prescriptions
        .groupby("drug", dropna=False)
        .agg(
            prescription_count=(
                "drug",
                "size"
            ),

            unique_patients=(
                "subject_id",
                "nunique"
            ),

            unique_admissions=(
                "hadm_id",
                "nunique"
            )
        )
        .reset_index()
        .sort_values(
            "prescription_count",
            ascending=False
        )
    )

    return result


def prescriptions_by_drug_type(prescriptions):
    """
    Summarize prescriptions by drug type.
    """

    return (
        prescriptions
        .groupby("drug_type", dropna=False)
        .size()
        .reset_index(
            name="prescription_count"
        )
        .sort_values(
            "prescription_count",
            ascending=False
        )
    )


def prescriptions_by_route(prescriptions):
    """
    Summarize prescriptions by administration route.
    """

    return (
        prescriptions
        .groupby("route", dropna=False)
        .size()
        .reset_index(
            name="prescription_count"
        )
        .sort_values(
            "prescription_count",
            ascending=False
        )
    )


# ============================================================
# PHARMACY ANALYTICS
# ============================================================

def pharmacy_summary(pharmacy):
    """
    High-level pharmacy statistics.
    """

    return {
        "total_pharmacy_records": len(pharmacy),

        "unique_patients": pharmacy[
            "subject_id"
        ].nunique(),

        "unique_admissions": pharmacy[
            "hadm_id"
        ].nunique(),

        "unique_medications": pharmacy[
            "medication"
        ].nunique()
    }


def pharmacy_by_medication(pharmacy):
    """
    Rank pharmacy records by medication.
    """

    result = (
        pharmacy
        .groupby("medication", dropna=False)
        .agg(
            pharmacy_events=(
                "medication",
                "size"
            ),

            unique_patients=(
                "subject_id",
                "nunique"
            ),

            unique_admissions=(
                "hadm_id",
                "nunique"
            )
        )
        .reset_index()
        .sort_values(
            "pharmacy_events",
            ascending=False
        )
    )

    return result


def pharmacy_by_status(pharmacy):
    """
    Summarize pharmacy records by status.
    """

    return (
        pharmacy
        .groupby("status", dropna=False)
        .size()
        .reset_index(
            name="event_count"
        )
        .sort_values(
            "event_count",
            ascending=False
        )
    )


# ============================================================
# eMAR ANALYTICS
# ============================================================

def emar_summary(emar):
    """
    High-level eMAR statistics.
    """

    return {
        "total_emar_events": len(emar),

        "unique_patients": emar[
            "subject_id"
        ].nunique(),

        "unique_admissions": emar[
            "hadm_id"
        ].nunique(),

        "unique_medications": emar[
            "medication"
        ].nunique()
    }


def emar_by_medication(emar):
    """
    Rank administered medications by eMAR frequency.
    """

    result = (
        emar
        .groupby("medication", dropna=False)
        .agg(
            administration_events=(
                "medication",
                "size"
            ),

            unique_patients=(
                "subject_id",
                "nunique"
            ),

            unique_admissions=(
                "hadm_id",
                "nunique"
            )
        )
        .reset_index()
        .sort_values(
            "administration_events",
            ascending=False
        )
    )

    return result


# ============================================================
# eMAR DETAIL ANALYTICS
# ============================================================

def emar_detail_summary(emar_detail):
    """
    High-level eMAR detail statistics.
    """

    return {
        "total_emar_detail_records": len(
            emar_detail
        ),

        "unique_patients": emar_detail[
            "subject_id"
        ].nunique(),

        "unique_emar_events": emar_detail[
            "emar_id"
        ].nunique()
    }


def dose_summary(emar_detail):
    """
    Summarize numeric administered doses.
    """

    result = emar_detail.copy()

    result["dose_given_numeric"] = pd.to_numeric(
        result["dose_given"],
        errors="coerce"
    )

    return (
        result[
            result["dose_given_numeric"].notna()
        ]
        .groupby("dose_given_unit", dropna=False)
        ["dose_given_numeric"]
        .agg(
            count="count",
            mean="mean",
            median="median",
            min="min",
            max="max"
        )
        .reset_index()
    )


# ============================================================
# INPUT EVENTS
# ============================================================

def inputevent_summary(inputevents):
    """
    High-level ICU input event statistics.
    """

    return {
        "total_input_events": len(
            inputevents
        ),

        "unique_patients": inputevents[
            "subject_id"
        ].nunique(),

        "unique_admissions": inputevents[
            "hadm_id"
        ].nunique(),

        "unique_items": inputevents[
            "itemid"
        ].nunique()
    }


def inputevents_by_category(inputevents):
    """
    Summarize ICU inputs by order category.
    """

    return (
        inputevents
        .groupby(
            "ordercategoryname",
            dropna=False
        )
        .size()
        .reset_index(
            name="event_count"
        )
        .sort_values(
            "event_count",
            ascending=False
        )
    )


# ============================================================
# INGREDIENT EVENTS
# ============================================================

def ingredientevent_summary(ingredientevents):
    """
    High-level ingredient event statistics.
    """

    return {
        "total_ingredient_events": len(
            ingredientevents
        ),

        "unique_patients": ingredientevents[
            "subject_id"
        ].nunique(),

        "unique_admissions": ingredientevents[
            "hadm_id"
        ].nunique(),

        "unique_items": ingredientevents[
            "itemid"
        ].nunique()
    }


# ============================================================
# CROSS-SOURCE MEDICATION SUMMARY
# ============================================================

def medication_coverage_summary(
    prescriptions,
    pharmacy,
    emar
):
    """
    Compare patient and admission coverage
    across medication-related sources.
    """

    return pd.DataFrame(
        [
            {
                "source": "prescriptions",
                "rows": len(prescriptions),
                "unique_patients":
                    prescriptions[
                        "subject_id"
                    ].nunique(),
                "unique_admissions":
                    prescriptions[
                        "hadm_id"
                    ].nunique()
            },
            {
                "source": "pharmacy",
                "rows": len(pharmacy),
                "unique_patients":
                    pharmacy[
                        "subject_id"
                    ].nunique(),
                "unique_admissions":
                    pharmacy[
                        "hadm_id"
                    ].nunique()
            },
            {
                "source": "emar",
                "rows": len(emar),
                "unique_patients":
                    emar[
                        "subject_id"
                    ].nunique(),
                "unique_admissions":
                    emar[
                        "hadm_id"
                    ].nunique()
            }
        ]
    )
