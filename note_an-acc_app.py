# note_an_acc_app.py
# Streamlit app: Behaviour Inventory – Care Shift Note Builder (v2)
# UK English, Australian Standards

import streamlit as st
from datetime import datetime, time, timedelta
from typing import Dict, List, Tuple

st.set_page_config(page_title="Behaviour Inventory – Shift Note Builder", layout="wide")

# =========================
# Utility helpers
# =========================
def slots_30m(start: time, end: time) -> List[str]:
    out = []
    dt = datetime.combine(datetime.today(), start)
    end_dt = datetime.combine(datetime.today(), end)
    while dt <= end_dt:
        out.append(dt.strftime("%H:%M"))
        dt += timedelta(minutes=30)
    return out

def oxford_join(items: List[str]) -> str:
    items = [i for i in items if i and str(i).strip()]
    if not items: return ""
    if len(items) == 1: return items[0]
    return ", ".join(items[:-1]) + f" and {items[-1]}"

def keyify(s: str) -> str:
    return s.lower().replace(" ", "_").replace("/", "_").replace("-", "_").replace("&", "and")

# =========================
# Constants 
# =========================

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

MORNING_SLOTS = slots_30m(time(6, 0), time(14, 0))
AFTERNOON_SLOTS = slots_30m(time(14, 0), time(21, 0))

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

DEFAULT_ADLS = {
    "Morning": {
        "Toileting", "Oral Care", "Donning Glasses", "Donning Hearing Aids",
        "Dressing Upper and Lower Garments", "Skin Care", "Grooming hair"
    },
    "Afternoon": {
        "Toileting", "Change of incontinence aid", "Shower",
        "Skin Care", "Grooming hair"
    },
}

VISITOR_TYPES = [
    "Family", "Friends", "Regis Companion", "NDIS Companion",
    "External carer", "Hair-Dresser", "Beautician"
]

FOOD_FLUID_LEVELS = ["None", "1/8", "¼", "1/3", "½", "¾", "All"]
MEAL_ASSIST = ["Set-up", "Cut-up", "Minimal", "Moderate", "Full"]
ENGAGEMENT_LEVELS = [
    "Actively participated", "Observed only", "Engaged minimally",
    "Passively engaged", "Refused"
]
RECEPTIVENESS = ["Not receptive", "Receptive to assistance"]
ASSIST_LEVEL = ["1x", "2x", "3x"]
ADL_TIME = ["Minimal", "Moderate", "Extensive"]
SETTLEDNESS = ["Settled", "Unsettled"]
EFFECT_SCALE = ["Good", "Limited", "No effect"]
MED_EFFECT = ["Effective", "Partial", "No effect"]

# ---- Behaviour structure: Domains → Subdomains → Behaviours
DOMAINS: Dict[str, Dict[str, List[str]]] = {
    "Agitation": {
        "Physical": [
            "Physically aggressive", "Disinhibition", "Care resistance"
        ],
        "Verbal": [
            "Abusive language", "Verbally disruptive"
        ],
        "Emotional Dependence": [
            "Passive resistance", "Attention seeking", "Manipulative",
            "Withdrawal & apathy", "Depression", "Anxiety", "Irritable"
        ],
    },
    "Wandering": {
        "Locomotion": [
            "Problem wandering", "Intrusive behaviour"
        ]
    },
    "Other": {
        "Risk/Pattern/Perception": [
            "High-risk behaviour", "Aberrant motor behaviour",
            "Sleep & night-time behaviour", "Appetite & eating changes",
            "Hallucinations", "Delusions"
        ]
    }
}

# ---- Behaviour Inventory detail lists (examples condensed for UI clarity; extend as needed)
INVENTORY_DETAILS: Dict[str, List[str]] = {
    # Agitation / Physical
    "Physically aggressive": [
        "Upset when approached", "Attempted to hurt others",
        "Violence toward staff", "Violence toward co-resident",
        "Damaged property", "Uncooperative with help",
        "Physically resisted care", "Demanded own way"
    ],
    "Disinhibition": [
        "Inappropriate touching", "Public displays", "Public indecency",
        "Insensitive remarks", "Overly personal disclosures"
    ],
    "Care resistance": [
        "Refusal of care", "Non-compliance with hygiene",
        "Non-compliance with medication", "Non-compliance with activity"
    ],

    # Agitation / Verbal
    "Abusive language": [
        "Swearing", "Shouting", "Racial or sexual slurs", "Verbal threats"
    ],
    "Verbally disruptive": [
        "Repetitive calling out", "Excessive vocalisation", "Demanding behaviour"
    ],

    # Agitation / Emotional Dependence
    "Passive resistance": [
        "Hesitant with care", "Reluctant to participate"
    ],
    "Attention seeking": [
        "Seeking constant reassurance", "Feigning illness",
        "Exaggerating symptoms"
    ],
    "Manipulative": [
        "Emotional pressure", "Guilt-inducing statements"
    ],
    "Withdrawal & apathy": [
        "Reduced engagement", "Flat affect", "Lack of motivation",
        "Less spontaneous", "Less enthusiastic"
    ],
    "Depression": [
        "Tearfulness", "Sleep cycle affected", "Socially withdrawn",
        "Slow but coherent speech", "Negative self-image",
        "Feelings of guilt", "Expressions of wanting to die"
    ],
    "Anxiety": [
        "Catastrophising statements", "Preoccupied thought content",
        "Restlessness", "Pacing", "Hypervigilance",
        "Irrational fears", "Frequent questioning",
        "Excessive worry about future", "Tension / unable to relax",
        "Gasping/sighing due to nerves", "Racing heart (not medically explained)",
        "Avoidance of places/situations", "Upset when separated from trusted others"
    ],
    "Irritable": [
        "Easily irritated", "Impatient with delays", "Argued",
        "Difficult to get along with", "Snapped at others"
    ],

    # Wandering
    "Intrusive behaviour": [
        "Interfering with others", "Entering others’ rooms",
        "Touching others’ belongings"
    ],
    "Problem wandering": [
        "Constant movement", "Exit-seeking", "Movement into unsafe areas"
    ],

    # Other
    "High-risk behaviour": [
        "Walking without required aids", "Climbed from chair/bed",
        "Simulated falls", "Unsafe actions", "Exit-seeking"
    ],
    "Aberrant motor behaviour": [
        "Repetitive pacing/organising/rearranging/cleaning",
        "Rocking/tapping", "Itching/picking", "Excessive fidgeting"
    ],
    "Hallucinations": [
        "Responding to voices", "Talking to unseen people",
        "Acting as if seeing figures", "Smelling things others cannot",
        "Tactile sensations not present", "Tasting things not present"
    ],
    "Delusions": [
        "False skin sensations", "Interacted with voices",
        "Saw figures not present", "False smells/tastes"
    ],
    "Sleep & night-time behaviour": [
        "Night wandering", "Difficulty sleeping",
        "Packing/planning to leave at night"
    ],
    "Appetite & eating changes": [
        "Pooling food in mouth", "Poor appetite", "Unusually good appetite",
        "Change in preferred foods", "Playing with/destroying meal"
    ],
}

# ---- Triggers (modifiable / non-modifiable) and Management (prevention / intervention)
TRIGGERS_MOD: Dict[str, List[str]] = {
    "Physically aggressive": [
        "Environmental overstimulation", "Unmet needs (pain/hunger/toilet)",
        "Personal space issues on approach", "Poor communication", "Frustration/confusion"
    ],
    "Disinhibition": [
        "Environmental factors", "Lack of privacy", "Boredom",
        "Misread social cues", "Medication side effects"
    ],
    "Abusive language": [
        "Frustration", "Communication barriers", "Pain",
        "Sensory overload", "Environmental stressors"
    ],
    "Verbally disruptive": [
        "Anxiety", "Loneliness", "Boredom", "Environmental/routine changes"
    ],
    "Passive resistance": [
        "Lack of trust", "Poor communication", "Staff inconsistency",
        "Fear of losing autonomy"
    ],
    "Attention seeking": ["Unmet emotional needs", "Loneliness", "Boredom"],
    "Manipulative": ["Staff inconsistency", "Lack of boundaries", "Unmet emotional needs"],
    "Withdrawal & apathy": [
        "Pain", "Under-stimulation", "Poor lighting/noise", "Co-occurring depression"
    ],
    "Depression": [
        "Change in routine/environment", "Social isolation", "Grief", "Comfort needs"
    ],
    "Anxiety": [
        "Uncertainty", "Change in routine/environment", "Lack of reassurance",
        "Physical discomfort", "Hearing/vision impairment", "Recent event"
    ],
    "Irritable": [
        "Pain", "Discomfort", "Fatigue", "Hunger", "Toileting needs",
        "Overstimulation"
    ],
    "Intrusive behaviour": [
        "Confusing layout", "Boredom",
        "Insufficient supervision/meaningful activity"
    ],
    "Problem wandering": [
        "Restlessness", "Unmet physical needs",
        "Searching for comfort (familiar person/place)", "Change in routine/environment"
    ],
    "High-risk behaviour": [
        "Frustration/confusion", "Unmet needs", "Environmental obstacles"
    ],
    "Aberrant motor behaviour": [
        "Boredom", "Anxiety", "Medication side effects"
    ],
}

TRIGGERS_NONMOD: Dict[str, List[str]] = {
    "Physically aggressive": ["Cognitive impairment", "Dementia progression", "Neurological condition", "Personality"],
    "Disinhibition": ["Frontal lobe changes", "Frontotemporal dementia", "Historical hypersexuality"],
    "Abusive language": ["Cognitive decline", "Personality", "Cultural background", "Psychiatric illness"],
    "Verbally disruptive": ["Cognitive decline", "Hearing impairment", "Psychiatric disorders"],
    "Passive resistance": ["Cognitive impairment", "Trauma history", "Personality style"],
    "Attention seeking": ["Personality traits", "Lifelong coping mechanisms"],
    "Manipulative": ["Personality disorder traits", "Past relational patterns"],
    "Withdrawal & apathy": ["Cognitive impairment", "Chronic illness", "Existing psychiatric illness"],
    "Depression": ["Genetic predisposition", "Chronic illness", "Cognitive decline"],
    "Anxiety": ["Personality", "Dementia subtype", "Cognitive decline"],
    "Irritable": ["Cognitive decline", "Severe memory loss", "Personality traits", "Chronic conditions"],
    "Intrusive behaviour": ["Cognitive impairment", "Disorientation", "Frontal lobe changes", "Personality"],
    "Problem wandering": ["Cognitive impairment", "Sundowning", "Neurological damage"],
    "High-risk behaviour": ["Cognitive impairment", "Physical disability", "Psychiatric illness"],
    "Aberrant motor behaviour": ["Cognitive/neurological/psychiatric illness"],
}

MANAGEMENT_PREVENT: Dict[str, List[str]] = {
    "Physically aggressive": [
        "Maintain calm environment", "Consistent routine",
        "Person-centred care and validation techniques"
    ],
    "Disinhibition": [
        "Maintain dignity and privacy", "Clear communication", "Structured routine",
        "Gender-appropriate staff", "Orient to place and person"
    ],
    "Abusive language": [
        "Therapeutic communication", "Validate emotions", "Calm reassurance",
        "Maintain calm environment"
    ],
    "Verbally disruptive": [
        "Meaningful engagement", "Maintain routine",
        "Comfort items", "1:1 or group companionship"
    ],
    "Passive resistance": [
        "Empowerment and choice", "Explain each action", "Build rapport"
    ],
    "Attention seeking": [
        "Positive interactions", "Scheduled re-approaches",
        "Encourage group participation", "Encourage independence"
    ],
    "Manipulative": [
        "Set firm but kind limits", "Consistent team approach", "Focus on quality care"
    ],
    "Withdrawal & apathy": [
        "Encourage social interaction", "Structured activities",
        "Promote autonomy", "Check unmet ADL needs"
    ],
    "Depression": [
        "Foster social connection", "Positive communication",
        "Daylight exposure", "Familiar environment"
    ],
    "Anxiety": [
        "Consistent routine/environment", "Calm tone", "Avoid rushing"
    ],
    "Irritable": [
        "Monitor comfort needs", "Ensure rest periods", "Calm surroundings"
    ],
    "Intrusive behaviour": [
        "Structured activity", "Secure environment",
        "Signage/barriers", "Reality orientation"
    ],
    "Problem wandering": [
        "Secure exits", "Notify nearby staff",
        "Offer hydration/food/toileting", "Routine and exercise"
    ],
    "High-risk behaviour": [
        "Maintain safe environment", "Provide supervision",
        "Ensure aids within reach", "Educate"
    ],
    "Aberrant motor behaviour": [
        "Sensory stimulation", "Maintain structure", "Allow safe expression"
    ],
    "Sleep & night-time behaviour": [
        "Dim lights", "Comfort drink/snack", "Ensure toileting",
        "Comfortable temperature", "Calming music", "Orienting activities"
    ],
}

MANAGEMENT_INTERVENT: Dict[str, List[str]] = {
    "Physically aggressive": [
        "De-escalation strategies", "Ensure safety",
        "Redirect behaviour", "Diversional activity", "RN review"
    ],
    "Disinhibition": [
        "Calm redirection", "Clear boundaries", "Neutral body language",
        "Document behaviour", "Inform RN"
    ],
    "Abusive language": [
        "Avoid confrontation", "Redirect conversation",
        "Acknowledge feelings", "Short clear sentences",
        "Relaxed posture", "RN review"
    ],
    "Verbally disruptive": [
        "Acknowledge feelings", "Redirect", "Reality orientation (visual cues)",
        "Involve family", "Inform RN"
    ],
    "Passive resistance": [
        "Gentle encouragement", "Offer choices", "Familiar carer", "RN review"
    ],
    "Attention seeking": [
        "Redirect to activities", "Reinforce independence",
        "Duty of care for all residents", "RN review"
    ],
    "Manipulative": [
        "Avoid power struggles", "Team debriefing",
        "Refocus to goals/routine", "RN review"
    ],
    "Withdrawal & apathy": [
        "Positive reinforcement", "Small achievable tasks", "RN review"
    ],
    "Depression": [
        "Emotional support", "Involve Psychologist/GP",
        "Monitor suicidality", "Review meds and adherence", "RN review"
    ],
    "Anxiety": [
        "Provide reassurance", "Relaxation strategies",
        "RNOD call if needed", "Consider GP review", "Inform RN"
    ],
    "Irritable": [
        "Validate feelings", "Short simple statements",
        "Redirect to calming activity", "Move to calm area",
        "Ensure comfort needs met", "RN review"
    ],
    "Intrusive behaviour": [
        "Gentle redirection", "Meaningful activity",
        "Reassure and validate", "Separate triggering co-residents", "Inform RN"
    ],
    "Problem wandering": [
        "Regular support/supervision", "Purposeful task", "RN involved"
    ],
    "High-risk behaviour": [
        "Prompt response to unsafe acts", "Falls prevention plan",
        "MDT involvement", "Redirect to calming activity",
        "Ensure safety", "Monitor distress severity", "RN review"
    ],
    "Aberrant motor behaviour": [
        "Redirect to calming activities", "Ensure safety",
        "Minimise distress/harm", "RN review"
    ],
    "Sleep & night-time behaviour": [
        "Redirect to bed", "Dim lights", "Warm drink/snack",
        "Ensure toileting", "Comfortable temperature",
        "Calming music", "RN review"
    ],
}

# =========================
# User Interface – Header & Sidebar
# =========================
st.title("Behaviour Inventory – Shift Note Builder (v2)")

with st.sidebar:
    st.subheader("Shift Settings")
    shift_type = st.selectbox("Shift Type", ["Morning", "Afternoon"])
    st.caption("The schedule below is a guide only — use clinical judgement.")

    st.write("**Shift Structure (guide)**")
    for line in SHIFT_SCHEDULE[shift_type]:
        st.write(f"• {line}")

# =========================
# Section: ADLs & Care
# =========================
c1, c2 = st.columns(2)

with c1:
    st.header("ADLs & Care")

    # Select/Clear controls
    b1, b2 = st.columns(2)
    with b1:
        if st.button("Select all ADLs"):
            for opt in ADL_OPTIONS:
                st.session_state[f"adl_{keyify(opt)}"] = True
    with b2:
        if st.button("Clear all ADLs"):
            for opt in ADL_OPTIONS:
                st.session_state[f"adl_{keyify(opt)}"] = False

    st.caption("Pre-ticked based on shift; untick anything not completed.")

    # Render checkboxes with shift-aware defaults
    preselected = DEFAULT_ADLS.get(shift_type, set())
    adls_done = []
    for opt in ADL_OPTIONS:
        k = f"adl_{keyify(opt)}"
        chk = st.checkbox(opt, value=st.session_state.get(k, opt in preselected), key=k)
        if chk:
            adls_done.append(opt)

    behaviour_management_done = st.checkbox("Behaviour management undertaken this shift")

    st.markdown("**Care Requirements**")
    receptiveness = st.selectbox("Receptiveness", RECEPTIVENESS)
    pa_assist = st.selectbox("Physical assistance required", ASSIST_LEVEL, index=0)
    adl_time = st.selectbox("Time required to complete ADLs", ADL_TIME, index=1)

    st.markdown("**Dietary Intake (scheduled meal times)**")
    intake = st.selectbox("Total food & fluid intake", FOOD_FLUID_LEVELS, index=5)
    meal_assist_sel = st.multiselect("Meal assistance (select all that apply)", MEAL_ASSIST)

with c2:
    st.header("Activity & Visitors")

    engagement_level = st.selectbox("Activity engagement level", ENGAGEMENT_LEVELS, index=0)
    engagement_behaviour_desc = st.text_area(
        "If behaviours occurred during engagement, describe presentation/benefit (optional)",
        placeholder="e.g., Calm with intermittent calling out; benefited from 1:1 and redirection."
    )

    st.markdown("**Visitors**")
    had_visitors = st.radio("Was the resident visited this shift?", ["No", "Yes"], index=0, horizontal=True)
    visitor_types = []
    visitor_times = []
    if had_visitors == "Yes":
        visitor_types = st.multiselect("Visitor type(s)", VISITOR_TYPES)
        slot_source = MORNING_SLOTS if shift_type == "Morning" else AFTERNOON_SLOTS
        visitor_times = st.multiselect("Visit times (30-min intervals)", options=slot_source)

# =========================
# Behaviour Section
# =========================
st.markdown("---")
st.header("Behaviour Inventory")
st.caption("Record behaviour episodes by **Domain → Subdomain → Behaviour(s)** with frequency, severity, and disruption. Inclusion rules are applied automatically.")

domain = st.selectbox("Domain", list(DOMAINS.keys()))
subdomain = st.selectbox("Subdomain", list(DOMAINS[domain].keys()))
behaviour_pick = st.multiselect("Behaviours (tick all that apply)", DOMAINS[domain][subdomain])

episodes: List[dict] = []

if behaviour_pick:
    st.markdown("#### Episodes (set scoring for each selected behaviour)")
    for i, beh in enumerate(behaviour_pick):
        with st.container(border=True):
            st.markdown(f"**{i+1}. {beh}**")

            # Specific manifestations (from inventory details)
            specifics = INVENTORY_DETAILS.get(beh, [])
            selected_specifics = []
            if specifics:
                selected_specifics = st.multiselect(
                    f"Specific manifestations of {beh} (optional)",
                    specifics, key=f"spec_{i}"
                )

            cA, cB, cC, cD = st.columns([1,1,1,1])
            with cA:
                freq = st.slider("Frequency (1–4)", 1, 4, 1, key=f"freq_{i}",
                                 help="1: once; 2: at times; 3: often; 4: very often")
            with cB:
                sev = st.slider("Severity (1–4)", 1, 4, 1, key=f"sev_{i}",
                                help="1: minimal; 2: mild; 3: moderate; 4: severe")
            with cC:
                disrupt = st.slider("Occupational disruption (0–4)", 0, 4, 0, key=f"disr_{i}",
                                    help="0: nil; 1: minimal; 2: mild; 3: moderate; 4: severe")
            with cD:
                when_slot = st.selectbox(
                    "Approx. time",
                    MORNING_SLOTS if shift_type == "Morning" else AFTERNOON_SLOTS,
                    key=f"slot_{i}"
                )

            # Triggers (modifiable / non-modifiable) + free text
            trig_mod_opts = TRIGGERS_MOD.get(beh, [])
            trig_nonmod_opts = TRIGGERS_NONMOD.get(beh, [])
            t1, t2 = st.columns(2)
            with t1:
                trig_mod = st.multiselect("Modifiable triggers (select as applicable)", trig_mod_opts, key=f"tmod_{i}")
            with t2:
                trig_nonmod = st.multiselect("Non-modifiable triggers", trig_nonmod_opts, key=f"tnon_{i}")
            trig_free = st.text_input("Additional trigger context (optional)", key=f"tfree_{i}")

            # Management (prevention used this shift? / interventions applied?)
            prev_opts = MANAGEMENT_PREVENT.get(beh, [])
            int_opts = MANAGEMENT_INTERVENT.get(beh, [])
            m1, m2 = st.columns(2)
            with m1:
                used_prevent = st.multiselect("Preventative strategies utilised", prev_opts, key=f"prev_{i}")
            with m2:
                interventions = st.multiselect("Interventions applied", int_opts, key=f"int_{i}")

            eff = st.selectbox("Effectiveness of strategies", EFFECT_SCALE, index=0, key=f"eff_{i}")
            med_given = st.checkbox("Sedative medication administered?", key=f"med_{i}")
            med_eff = st.selectbox("Medication effect", MED_EFFECT, index=0, key=f"me_{i}") if med_given else None

            episodes.append({
                "behaviour": beh,
                "specifics": selected_specifics,
                "freq": freq,
                "sev": sev,
                "disrupt": disrupt,
                "time": when_slot,
                "trig_mod": trig_mod,
                "trig_nonmod": trig_nonmod,
                "trig_free": trig_free.strip(),
                "prevent": used_prevent,
                "interventions": interventions,
                "eff": eff,
                "med_given": med_given,
                "med_eff": med_eff
            })

# =========================
# End of Shift
# =========================
st.markdown("---")
st.header("End of Shift")
settledness = st.selectbox("Resident appears", SETTLEDNESS, index=0)
in_bed = st.checkbox("Resident in bed at time of report")
call_bell = False
sensor_mats = 0
crash_mats = 0
ongoing = st.text_input("Ongoing care/concerns (optional)",
                        placeholder="e.g., Continue hourly rounding; monitor for further agitation.")
if in_bed:
    call_bell = st.checkbox("Call bell left within reach", value=True)
    sensor_mats = st.number_input("Sensor mats in situ", min_value=0, max_value=2, value=1)
    crash_mats = st.number_input("Crash mats in situ", min_value=0, max_value=2, value=0)

# =========================
# Inclusion Logic & Note Builder
# =========================
def include_episode(freq: int, sev: int, disrupt: int) -> bool:
    """
    Include if:
      - freq >= 3 OR
      - sev >= 3 OR
      - freq * sev > 4 OR
      - disruption >= 3
    Otherwise do not include.
    """
    return (freq >= 3) or (sev >= 3) or (freq * sev > 4) or (disrupt >= 3)

def build_note() -> str:
    parts: List[str] = []

    # Baseline intro: will change to 'no notable change' only if no episodes included
    included_any = False

    # ADLs
    if adls_done:
        parts.append(f"ADLs completed included {oxford_join(adls_done)}.")
    if behaviour_management_done:
        parts.append("Behaviour management strategies were implemented as required.")

    # Behaviours
    for ep in episodes:
        if include_episode(ep["freq"], ep["sev"], ep["disrupt"]):
            included_any = True

            spec = f" ({oxford_join(ep['specifics'])})" if ep["specifics"] else ""
            trig_bits = []
            if ep["trig_mod"]: trig_bits.append(oxford_join(ep["trig_mod"]))
            if ep["trig_nonmod"]: trig_bits.append(oxford_join(ep["trig_nonmod"]))
            if ep["trig_free"]: trig_bits.append(ep["trig_free"])
            trig_txt = f" and potentially triggered by {oxford_join(trig_bits)}" if trig_bits else ""

            disr_txt = ""
            if ep["disrupt"] >= 3:
                disr_map = {3: "moderate", 4: "severe"}
                disr_txt = f" and caused {disr_map.get(ep['disrupt'], 'notable')} occupational disruption"

            ints = oxford_join(ep["interventions"])
            ints_txt = f" Staff provided {ints} and made the care team aware." if ints else " Staff informed the care team."

            med_txt = ""
            if ep["med_given"]:
                med_txt = f" Pharmacological intervention was administered with {ep['med_eff'].lower()} reduction in behaviours."

            # Frequency to words
