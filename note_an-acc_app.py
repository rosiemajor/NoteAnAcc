# behaviour_inventory_app.py
# Streamlit app to capture shift details and generate a single-paragraph progress note
import streamlit as st
from datetime import datetime, time, timedelta
from typing import List

st.set_page_config(page_title="DSU AN-ACC Documentation Builder", layout="wide")

# ---------- Constants ----------
SHIFT_SCHEDULE = {
    "Morning": [
        "0600–0730 ADLs upon rising",
        "0730–0900 Breakfast",
        "0900–1130 Lifestyle / activity engagement",
        "1000–1030 Morning tea",
        "1200–1300 Lunch",
        "1300–1330 Activity engagement / Toileting / Transfers / Appointments",
        "1330–1400 End of shift / ATOR",
        "Variable: Visitors, behaviour management",
    ],
    "Afternoon": [
        "1400–1500 Afternoon tea",
        "1500–1700 Lifestyle / activity engagement",
        "1500–1600 Toileting / Shower / Change of clothes (if applicable)",
        "1700–1800 Dinner",
        "1800–1930 ADLs",
        "1930–2100 End of shift / ATOR",
        "Variable: Visitors, behaviour management",
    ],
}

ADL_OPTIONS = [
    "Toileting",
    "Change of incontinence aid",
    "Shower",
    "Sponge",
    "Dressing Upper and Lower Garments",
    "Dressing Upper Garments",
    "Dressing Lower Garments",
    "Skin Care",
    "Oral Care",
    "Shaving",
    "Donning Hearing Aids",
    "Donning Glasses",
    "Grooming hair",
    "Groomed nails",
]
VISITOR_TYPES = [
    "Family",
    "Friends",
    "Internal Companion",
    "NDIS Companion",
    "External carer",
    "Hair-Dresser",
    "Beautician",
]
FOOD_FLUID_LEVELS = ["None", "1/8", "¼", "1/3", "½", "¾", "All"]
ENGAGEMENT_LEVELS = [
    "Actively participated",
    "Observed only",
    "Engaged minimally",
    "Passively engaged",
    "Refused",
]
RECEPTIVENESS = ["Not receptive", "Receptive to assistance"]
ASSIST_LEVEL = ["1x", "2x", "3x"]
ADL_TIME = ["Minimal", "Moderate", "Extensive"]
SETTLEDNESS = ["Settled", "Unsettled"]
EFFECT_SCALE = ["Good", "Limited", "No effect"]
MED_EFFECT = ["Effective", "Partial", "No effect"]
SEVERITY = ["Minimal", "Moderate", "Severe"]
BEHAVIOUR_FLAGS = [
    # All possible exhibited characteristics of AN-ACC BRUA Measure. You can extend this list as required.
    "Refusal of care",
    "Repetitive calling out",
    "Demanding behaviour",
    "Swearing",
    "Shouting",
    "Excessive vocalisation",
    "Frequent questioning",
    "Seeking constant reassurance",
    "Restlessness",
    "Pacing",
    "Reduced engagement and participation",
    "Lack of motivation",
    "Flat affect",
    "Sleep or appetite changes",
    "Tearfulness",
    "Social withdrawal",
    "Preoccupied mind",
    "Verbal threats",
    "Easily angered",
    "Snapping at others",
    "Impatience",
    "Walking without required aids",
    "Entering others’ rooms",
    "Touching others’ belongings",
    "Interfering with others",
    "Movement into unsafe areas",
    "Exit-seeking behaviour",
    "Climbing out of a chair or bed",
    "Attempting to control care through guilt or emotional pressure",
    "Feigning illness",
    "Exaggerating symptoms",
    "Verbalises irrational fear",
    "Hypervigilance",
    "Simulated falls",
    "Repetitive motions such as: Pacing, Organising, Rearranging, Cleaning, Rocking, Tapping, Itching, Picking",
    "Public indecency (e.g., urinating or defecating in public spaces)",
    "Hitting",
    "Pushing",
    "Kicking",
    "Spitting",
    "Biting",
    "Throwing furniture",
    "Damaging property",
    "Sexually or physically inappropriate touching",
    "Public displays of a sexual or physical nature",
    "Racial or sexual slurs",
    "Unsafe smoking or drinking habits",
    "Self-harm",
    "Suicidal Ideation",
    "Constant movement"
    
]

def half_hour_slots(start: time, end: time) -> List[str]:
    slots = []
    dt = datetime.combine(datetime.today(), start)
    end_dt = datetime.combine(datetime.today(), end)
    while dt <= end_dt:
        slots.append(dt.strftime("%H:%M"))
        dt += timedelta(minutes=30)
    return slots

MORNING_SLOTS = half_hour_slots(time(6, 0), time(14, 0))
AFTERNOON_SLOTS = half_hour_slots(time(14, 0), time(21, 0))

# ---------- UI ----------
st.title("Behaviour Inventory – Shift Note Builder")

with st.sidebar:
    st.subheader("Shift Settings")
    shift_type = st.selectbox("Shift Type", ["Morning", "Afternoon"])
    st.caption("Tip: The schedule below is a guide only – use clinical judgement.")

    st.write("**Shift Structure (guide)**")
    for line in SHIFT_SCHEDULE[shift_type]:
        st.write(f"• {line}")

col1, col2 = st.columns(2)

with col1:
    st.header("ADLs & Care")
    adls_done = st.multiselect("ADLs – select all that apply", ADL_OPTIONS)
    behaviour_management_done = st.checkbox("Behaviour management undertaken this shift")

    st.markdown("**Care Requirements**")
    receptiveness = st.selectbox("Receptiveness", RECEPTIVENESS)
    pa_assist = st.selectbox("Physical assistance required", ASSIST_LEVEL, index=0)
    adl_time = st.selectbox("Time required to complete ADLs", ADL_TIME, index=1)

    st.markdown("**Dietary Intake (scheduled meal times)**")
    intake = st.selectbox("Total food & fluid intake", FOOD_FLUID_LEVELS, index=5)
    meal_assist = st.multiselect(
        "Meal assistance (select all that apply)",
        ["Set-up", "Cut-up", "Minimal", "Moderate", "Full"],
    )

with col2:
    st.header("Activity & Visitors")
    engagement_level = st.selectbox("Activity engagement level", ENGAGEMENT_LEVELS, index=0)
    engagement_behaviour_desc = st.text_area(
        "If behaviours occurred during engagement, describe presentation/benefit (optional)",
        placeholder="e.g., Calm with intermittent calling out; benefited from 1:1 and redirection."
    )

    st.markdown("**Visitors**")
    had_visitors = st.radio("Was the resident visited this shift?", ["No", "Yes"], index=0)
    visitor_types = []
    visitor_times = []
    if had_visitors == "Yes":
        visitor_types = st.multiselect("Visitor type(s)", VISITOR_TYPES)
        slot_source = MORNING_SLOTS if shift_type == "Morning" else AFTERNOON_SLOTS
        visitor_times = st.multiselect(
            "Visit times (30-min intervals)",
            options=slot_source
        )

st.markdown("---")
st.header("Behaviour Episodes (optional)")
st.caption("Add any behaviour episodes observed this shift (you can add none, one, or several).")

episodes = []
with st.expander("Add/Review episodes", expanded=False):
    ep_count = st.number_input("Number of episodes to record", min_value=0, max_value=10, value=0, step=1)
    for i in range(ep_count):
        st.subheader(f"Episode {i+1}")
        c1, c2, c3 = st.columns(3)
        with c1:
            behaviour = st.selectbox(f"Behaviour #{i+1}", BEHAVIOUR_FLAGS, key=f"beh_{i}")
        with c2:
            timing_vs_trigger = st.selectbox(
                f"Timing vs potential trigger #{i+1}",
                ["Before", "During", "After"],
                key=f"timevs_{i}"
            )
        with c3:
            severity = st.selectbox(f"Severity #{i+1}", SEVERITY, key=f"sev_{i}")

        trigger_text = st.text_input(
            f"Potential trigger  #{i+1}",
            key=f"trig_{i}",
            placeholder="e.g., overstimulating environment, toileting needs, showering, mealtime, interaction with co-resident"
        )

        disr_col1, disr_col2 = st.columns(2)
        with disr_col1:
            caused_disruption = st.checkbox(f"Occupational disruption caused? #{i+1}", key=f"disr_{i}")
        dur = None
        staff_num = None
        with disr_col2:
            if caused_disruption:
                dur = st.number_input(f"Disruption duration (mins) #{i+1}", min_value=1, max_value=240, value=5, key=f"dur_{i}")
                staff_num = st.number_input(f"Number of staff impacted #{i+1}", min_value=1, max_value=10, value=1, key=f"staff_{i}")

        interventions = st.multiselect(
            f"Interventions provided #{i+1}",
            [
                "Verbal de-escalation",
                "Redirection",
                "1:1 engagement",
                "Environmental modification (quiet area)",
                "Diversional activity",
                "Offer food/fluids",
                "Toileting & hygiene needs",
                "Provide comfort/reassurance",
                "RN informed for review",
            ],
            key=f"int_{i}"
        )

        eff = st.selectbox(f"Effectiveness of strategies #{i+1}", EFFECT_SCALE, index=0, key=f"eff_{i}")

        med_given = st.checkbox(f"Sedative medication administered? #{i+1}", key=f"med_{i}")
        med_effect = None
        if med_given:
            med_effect = st.selectbox(f"Medication effect #{i+1}", MED_EFFECT, index=0, key=f"medeff_{i}")

        when_slot = st.selectbox(
            f"Approximate time of episode #{i+1}",
            MORNING_SLOTS if shift_type == "Morning" else AFTERNOON_SLOTS,
            key=f"slot_{i}"
        )

        episodes.append({
            "behaviour": behaviour,
            "timing": timing_vs_trigger,
            "trigger": trigger_text.strip(),
            "severity": severity,
            "disruption": caused_disruption,
            "duration": dur,
            "staff": staff_num,
            "interventions": interventions,
            "effectiveness": eff,
            "med_given": med_given,
            "med_effect": med_effect,
            "time": when_slot
        })
    if ep_count == 0:
        st.info("No episodes recorded.")

st.markdown("---")
st.header("End of Shift")
settledness = st.selectbox("Resident appears", SETTLEDNESS, index=0)
in_bed = st.checkbox("Resident in bed at time of report")
call_bell = False
sensor_mats = 0
crash_mats = 0
ongoing = st.text_input("Ongoing care/concerns (optional)", placeholder="e.g., continue hourly rounding; monitor for further agitation.")
if in_bed:
    call_bell = st.checkbox("Call bell left within reach", value=True)
    sensor_mats = st.number_input("Sensor mats in situ", min_value=0, max_value=2, value=1)
    crash_mats = st.number_input("Crash mats in situ", min_value=0, max_value=2, value=0)

# ---------- Note Builder ----------
def oxford_join(items: List[str]) -> str:
    items = [i for i in items if i and str(i).strip()]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + f" and {items[-1]}"

def build_note() -> str:
    parts = []

    # Baseline & shift
    parts.append(f"Resident’s baseline varied minimally throughout the {shift_type.lower()} shift.")

    # ADLs
    if adls_done:
        parts.append(f"ADLs completed included {oxford_join(adls_done)}.")
    if behaviour_management_done:
        parts.append("Behaviour management strategies were implemented as required.")

    # Behaviour change (episodes loop)
    if episodes:
        for ep in episodes:
            trig_txt = f" {ep['trigger']}" if ep["trigger"] else ""
            disr_txt = ""
            if ep["disruption"]:
                d = f" for approximately {ep['duration']} minutes" if ep["duration"] else ""
                s = f" affecting {int(ep['staff'])} staff" if ep["staff"] else ""
                disr_txt = f" and caused occupational disruption{d}{s}"
            ints = oxford_join(ep["interventions"])
            ints_txt = f" Staff provided {ints} and made the care team aware." if ints else " Staff informed the care team."
            med_txt = ""
            if ep["med_given"]:
                med_txt = f" Pharmacological intervention was administered with {ep['med_effect'].lower()} reduction in behaviours."
            parts.append(
                f"Resident demonstrated {ep['behaviour'].lower()} at approximately {ep['time']}, "
                f"{ep['timing'].lower()} a potential trigger{trig_txt}. "
                f"The behaviour involved {ep['severity'].lower()} distress{disr_txt}.{ints_txt} "
                f"Care strategies had {ep['effectiveness'].lower()} overall effect.{med_txt}"
            )
    else:
        parts.append("There was no notable change in behaviour, affect, cognition or functional ability.")

    # Engagement
    parts.append(f"Activity engagement: {engagement_level.lower()}.")
    if engagement_behaviour_desc.strip():
        parts.append(engagement_behaviour_desc.strip())

    # Visitors
    if had_visitors == "Yes" and visitor_types:
        when_txt = f" at {oxford_join(visitor_times)}" if visitor_times else ""
        parts.append(f"Visited by {oxford_join(visitor_types)}{when_txt}.")

    # Intake & meal assistance
    parts.append(f"Total intake during scheduled meal times was {intake.lower()}.")
    if meal_assist:
        parts.append(f"Meal assistance required: {oxford_join(meal_assist)}.")

    # Care requirements
    parts.append(
        f"Resident was {receptiveness.lower()} and required {pa_assist.lower()} physical assistance "
        f"with {adl_time.lower()} time to complete ADLs."
    )

    # End of report
    end_bits = [f"resident appears {settledness.lower()}"]
    if in_bed:
        bed_bits = []
        if call_bell:
            bed_bits.append("call bell left within reach")
        if sensor_mats:
            bed_bits.append(f"{sensor_mats} sensor mat(s) in situ")
        if crash_mats:
            bed_bits.append(f"{crash_mats} crash mat(s) in situ")
        if bed_bits:
            end_bits.append(", ".join(bed_bits))
    if ongoing.strip():
        end_bits.append(f"ongoing care: {ongoing.strip()}")
    parts.append("At time of report, " + "; ".join(end_bits) + ".")

    # One paragraph, UK English style
    paragraph = " ".join(parts)
    # Clean spacing
    paragraph = " ".join(paragraph.split())
    return paragraph

if st.button("Generate Shift Note", use_container_width=True):
    note = build_note()
    st.success("Shift note generated.")
    st.text_area("Final paragraph (copy/paste)", note, height=220)
    st.download_button("Download .txt", data=note, file_name="shift_note.txt")

# legal footer
st.caption("This tool helps standardise clinical language in a resedential memory support setting. Always exercise professional judgement and chart per relevant facility policy, juristidiction's ethical codes & legislation.")
