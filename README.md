# AI for Smarter Patient Care    -- MIMIC-IV Patient Analytics
------------------------------------------------------------------------

Link: "https://ai-for-smarter-patient-care.streamlit.app/"

## From scattered clinical records to one patient story

> **A clinical analytics platform built on MIMIC-IV data to make complex
> patient information easier to find, understand, validate, and act
> on.**



## At a glance


  **Patients**              **100**
  **Hospital admissions**   **275**
  **ICU stays**             **140**
  **Laboratory events**     **107,727**
  **Chart events**          **668,862**
  **Laboratory items**      **498**

# Why this project matters

A patient's information does not live in one place.

One table tells us about the patient. Another tells us about the
admission. Another describes the ICU stay. Laboratory results,
medications, microbiology, diagnoses, procedures, and chart events each
add another piece of the picture.

For a doctor, analyst, or decision-maker, the problem is not a lack of
information.

**The problem is finding the right information, understanding what it
means, and knowing whether it can be trusted.**

That is the problem this project was picked to address.

The goal was to turn a collection of complex clinical datasets into an
analytical application where the information can be explored from a
higher-level view down to an individual patient's timeline.

### For clinicians

The platform is designed to make the patient's story easier to follow
without requiring someone to manually move between multiple datasets and
reconstruct the sequence of events themselves.

Instead of asking:

> *Where is the information I need?*

the user can start with:

> *What happened to this patient, and when?*

### For analysts and hospital teams

The same structure makes it easier to answer questions about:

-   patient demographics
-   admissions and length of stay
-   ICU utilization
-   laboratory activity and abnormal results
-   medications
-   diagnoses and procedures
-   microbiology
-   clinical events
-   data completeness and integrity

The dashboard is therefore only the visible layer.

**The real project is the analytical foundation underneath it.**

------------------------------------------------------------------------

# What we built

The application brings together the major clinical areas of MIMIC-IV
into a single Streamlit analytics platform.

### The user can move from:

**Population → Admissions → ICU → Clinical Events → Medications →
Diagnoses → Data Quality → Patient Timeline**

That progression matters.

A stakeholder can begin with the overall population and gradually move
toward the details of a particular clinical story, while the underlying
system keeps track of the different levels of the data.

The platform also includes a **Data Quality** layer and a **Patient
Timeline** rather than treating visualization as the final step.

------------------------------------------------------------------------

# The 15 problems that mattered most

These were not cosmetic issues. They were the problems that could have
produced misleading numbers, broken relationships, slow analysis, or an
application that could not be maintained.

------------------------------------------------------------------------

## 01 --- The data was not one dataset

MIMIC-IV contains multiple datasets, and they are not comparable in size
or structure.

The difference was substantial:

-   `patients` → **100 rows**
-   `chartevents` → **668,862 rows**

The tables also use different identifiers, timestamps, and levels of
detail.

### What we changed

We built a centralized data-loading structure so datasets could be
loaded and profiled consistently before being used by the analytical
modules.

### Why stakeholders should care

Without this foundation, every dashboard page can end up making its own
assumptions about the data.

**We made the data layer consistent before making the dashboard look
consistent.**

------------------------------------------------------------------------

## 02 --- Missing data was a clinical-data problem, not just a cleaning problem

Some datasets contained very large amounts of missing information:

  Dataset           Missing cells
  --------------- ---------------
  `pharmacy`              131,168
  `labevents`             362,091
  `chartevents`           964,967

The tempting solution is to delete missing records or replace them with
something convenient.

That would be dangerous.

A missing value does not automatically mean that the underlying clinical
event did not happen.

### What we changed

We built a **Data Quality Engine** to measure and report missingness
before deciding how it should be interpreted.

### Why it matters

The system distinguishes between:

**"we know this was not present"**

and

**"the source did not give us this information."**

That distinction is critical in clinical analytics.

------------------------------------------------------------------------

## 03 --- One patient does not equal one row

The dataset contained:

-   **100 patients**
-   **275 hospital admissions**
-   **140 ICU stays**

If those levels are mixed together, basic metrics can become wrong
without looking obviously wrong.

### What we changed

We explicitly separated:

-   patient-level analysis
-   admission-level analysis
-   ICU-stay-level analysis

### Why it matters

When the dashboard says **100 patients**, it is not simply counting rows
from an admissions table.

**The grain of the data is treated as part of the meaning of the
metric.**

------------------------------------------------------------------------

## 04 --- We had to prove that the clinical records actually connected

A dashboard can display data beautifully while relationships underneath
it are broken.

We therefore checked whether records in child datasets pointed back to
valid parent records.

The integrity checks showed:

  Relationship                  Unmatched
  --------------------------- -----------
  Admissions → Patients             **0**
  ICU stays → Admissions            **0**
  Lab events → Admissions           **0**
  Microbiology → Admissions         **0**

### Why it matters

Before building analysis on top of these relationships, we had evidence
that the major links were intact.

**The numbers were not simply assumed to be connected. They were
checked.**

------------------------------------------------------------------------

## 05 --- ICU activity had its own level of detail

There were **140 ICU stays**, but only **128 unique hospital
admissions** associated with them.

That means an admission can contain more than one ICU stay.

Using `hadm_id` and `stay_id` interchangeably would therefore change the
meaning of ICU metrics.

### What we changed

We preserved:

-   `hadm_id` → hospital admission
-   `stay_id` → ICU stay

and used the appropriate identifier for each analysis.

### Why it matters

A metric such as ICU length of stay should describe an ICU stay --- not
accidentally describe a hospital admission.

------------------------------------------------------------------------

## 06 --- We did not blindly trust the supplied ICU length of stay

The ICU data already contained `los`.

We still independently calculated it using:

``` text
outtime - intime
```

and compared the result with the supplied value.

The difference was effectively zero, apart from floating-point
differences around **10⁻¹⁵**.

### Why it matters

A supplied value becoming a dashboard KPI is not the same thing as
validating that value.

**We checked the calculation against the underlying timestamps.**

------------------------------------------------------------------------

## 07 --- Laboratory data could not be reduced to simple averages

The laboratory dataset contained:

-   **107,727 events**
-   **498 laboratory items**

Not all results were numeric. Some were textual, and reference ranges
and flags were not always available.

### What we changed

We separated numeric and non-numeric results, checked the laboratory
dictionary, examined reference ranges, and summarized abnormal results
separately.

We also verified that laboratory item IDs used by the events had
dictionary entries.

**Result: 0 laboratory item IDs without a dictionary entry.**

### Why it matters

The dashboard does not force fundamentally different laboratory results
into one simplistic calculation.

------------------------------------------------------------------------

## 08 --- Missing abnormality flags were not treated as "normal"

The laboratory data contained:

-   `NaN` → **67,452**
-   `abnormal` → **40,275**

A missing flag could easily be mistaken for a normal result.

We deliberately did not make that assumption.

### What we changed

Missing flags were preserved as missing, while abnormal results were
summarized separately.

### Why it matters

**The system does not manufacture clinical certainty where the source
data does not provide it.**

------------------------------------------------------------------------

## 09 --- Medication information was distributed across three sources

Medication activity appeared across:

-   `prescriptions`
-   `pharmacy`
-   `emar`

These sources represent different parts of the medication process and do
not necessarily describe the same event in the same way.

### What we changed

We analyzed the sources separately and then created a medication
analysis layer that summarizes medication activity across them.

### Why it matters

The dashboard can bring the information together without pretending that
three different sources are one identical dataset.

------------------------------------------------------------------------

## 10 --- EMAR had different coverage from the other medication sources

EMAR contained:

-   **35,835 events**
-   **65 unique patients**
-   **181 unique admissions**

But prescriptions and pharmacy covered all **100 patients**.

That creates an important analytical trap:

> **No EMAR record does not necessarily mean no medication activity.**

### What we changed

We treated EMAR as its own clinical-event source and preserved its
coverage difference rather than interpreting absence as zero.

### Why it matters

Coverage limitations remain visible instead of becoming misleading
results.

------------------------------------------------------------------------

## 11 --- High-volume clinical events created a scalability problem

Some datasets were simply too large to repeatedly push through a
dashboard at raw-event level.

For example:

  Dataset           Records
  --------------- ---------
  `chartevents`     668,862
  `labevents`       107,727
  `emar_detail`      72,018
  `emar`             35,835

Showing everything is not the same as providing useful information.

### What we changed

We shifted the application toward:

-   summaries
-   aggregations
-   patient-level views
-   targeted drill-downs

rather than repeatedly rendering the entire raw event history.

### Why it matters

The application is designed around **questions people need answered**,
not around displaying every row that exists.

------------------------------------------------------------------------

## 12 --- The patient story was scattered across many clinical sources

Admissions, ICU stays, laboratories, microbiology, medications,
diagnoses, procedures, and chart events all describe different parts of
a patient's journey.

The challenge was to turn these separate records into something a person
could actually follow chronologically.

### What we changed

We standardized different clinical records into a common event structure
containing fields such as:

``` text
event_time
event_type
source
description
```

That structure became the basis for the **Patient Timeline**.

### Why it matters

Instead of forcing a user to mentally reconstruct the patient's journey
from multiple tables, the application presents the events as a
chronological story.

**This is one of the most important usability improvements in the
project.**

------------------------------------------------------------------------

## 13 --- Microbiology required context, not just counts

Microbiology contained very different specimen types:

-   urine
-   blood
-   sputum
-   tissue
-   swab
-   abscess
-   pleural fluid

It also contained different organisms, including *E. coli*, *Staph
aureus*, *Klebsiella*, and *Pseudomonas*.

A single total such as "number of microbiology events" would hide most
of the useful information.

### What we changed

We summarized microbiology at several levels:

**Specimen → Test → Organism → Interpretation**

### Why it matters

A stakeholder can move from the size of the activity to the details
behind it.

------------------------------------------------------------------------

## 14 --- Turning the analysis into an application introduced software problems

The project evolved from analysis into a multi-module application
containing:

``` text
src/
pages/
data/
app.py
```

That introduced dependencies between modules.

We encountered import and naming mismatches such as:

``` text
ImportError:
cannot import name 'profile_dataset'
from 'src.data_loader'
```

and:

``` text
ImportError:
cannot import name 'lab_value_summary'
from 'src.clinical_events'
```

There were also inconsistencies between expected and actual dataset
names, such as `diagnoses` versus `diagnoses_icd`.

### What we changed

We checked the actual functions and variables defined in the project,
corrected imports, aligned naming conventions, and separated
functionality into dedicated analytical modules.

### Why it matters

The goal was not just to make one notebook run.

**The goal was to build an application that can be maintained, extended,
and trusted.**

------------------------------------------------------------------------

## 15 --- The final test was whether the whole chain could be trusted

Individual functions can work while the final dashboard is still wrong.

So the final validation was treated as a chain:

``` text
DATA
  ↓
RELATIONSHIPS
  ↓
DATES
  ↓
DUPLICATES
  ↓
CLINICAL EVENTS
  ↓
AGGREGATIONS
  ↓
DASHBOARD
```

The final checks confirmed:

  Validation                                      Result
  ---------------------------------------- -------------
  Patients                                       **100**
  Admissions                                     **275**
  ICU stays                                      **140**
  Unmatched admission relationships                **0**
  Duplicate rows across checked datasets           **0**
  Invalid tested datetime values                   **0**
  Patient timeline                           **Working**
  Streamlit application                      **Working**

### Why it matters

The dashboard was not considered complete simply because it looked
right.

**The data underneath it had to survive the checks first.**

------------------------------------------------------------------------

# What the project delivers

The final application gives users a single place to explore:

**Population** → demographics and overall coverage

**Admissions** → volume, length of stay, and admission patterns

**ICU** → critical-care activity and utilization

**Clinical Events** → laboratory, chart, and microbiology activity

**Medications** → prescriptions, pharmacy, and medication administration
records

**Diagnoses** → ICD diagnoses, procedures, and severity-related
information

**Data Quality** → completeness, integrity, and validation checks

**Patient Timeline** → a chronological view across clinical sources

------------------------------------------------------------------------

# The bigger takeaway

The strongest part of this project is not the dashboard itself.

It is the decision to put **data meaning and data trust before
visualization**.

The work required us to understand the grain of clinical records,
validate relationships, handle missing information carefully, work
around large event tables, reconcile multiple clinical sources, and turn
all of that into an application that a user can actually navigate.

That is what turns raw MIMIC-IV data into an analytics product.

> ### **The dashboard answers "what do we see?"**
>
> ### **The data-quality and analytical layers answer "can we trust it?"**

And for clinical analytics, the second question is the one that matters
most.
