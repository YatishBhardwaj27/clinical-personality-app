# =========================================================
# 1. IMPORTS & DEPENDENCIES
# =========================================================
import streamlit as st
from fpdf import FPDF
import tempfile

# Set the tab title and layout
st.set_page_config(page_title="Clinical Personality Assessment", layout="centered")

# =========================================================
# 2. SIDEBAR: DEVELOPER CREDENTIALS & AUTHORITY STATEMENT
# WHY: A sidebar keeps your credentials visible and creates a professional SaaS layout.
# =========================================================
st.sidebar.title("About the Developer")
st.sidebar.info(
    "**Architected by Yatish Kumar**\n\n"
    "*M.Sc. Psychology | UGC-NET (JRF) & GATE Scholar*\n\n"
    "This clinical application was developed to democratize access to empirically validated psychometric tools. "
    "By bridging the gap between rigorous clinical and biological psychology research and public accessibility, "
    "this initiative provides high-fidelity, open-source psychological assessments at zero cost to the user."
)
st.sidebar.markdown("---")
st.sidebar.caption("Version 1.0.0 | Clinical Build")

# =========================================================
# 3. MAIN UI & ETHICS
# =========================================================
st.title("Clinical Personality Assessment")

st.info("**Research Ethics & Privacy Notice:** This application does not use a database. Your responses are processed temporarily in server memory to generate your report and are immediately, permanently deleted once you close this page. No data is tracked, stored, or shared.")

with st.expander("📖 Understand the Science (Click to Expand)", expanded=False):
    st.markdown("""
    ### What is Personality?
    Personality refers to the enduring characteristics and behavior that comprise a person's unique adjustment to life, including major traits, interests, drives, values, self-concept, abilities, and emotional patterns.
    
    ### The OCEAN Framework (Five-Factor Model)
    The Five-Factor Model represents the clinical consensus on the fundamental dimensions of human personality:
    * **O**penness to Experience: Intellectual curiosity and creative imagination.
    * **C**onscientiousness: Organization, productiveness, and responsibility.
    * **E**xtraversion: Sociability, assertiveness, and energy levels.
    * **A**greeableness: Compassion, respectfulness, and trust in others.
    * **N**euroticism: Emotional volatility and vulnerability to stress.
    
    ### The Mini-IPIP Instrument
    This assessment utilizes the **Mini-IPIP** (Donnellan et al., 2006), a rigorously validated 20-item short form of the International Personality Item Pool. 
    * **Reliability:** Demonstrates acceptable internal consistency across all five trait scales.
    * **Validity:** Shows strong convergent, discriminant, and criterion-related validity when compared to longer, proprietary clinical inventories.
    """)

st.header("Subject Information & Consent")
name = st.text_input("Full Name:")

# The mandatory consent checkbox
consent = st.checkbox("I have read the privacy notice, understand the theoretical framework, and consent to participate.")

# =========================================================
# 4. PSYCHOMETRIC SCALE SETUP
# =========================================================
scale = {
    "Very Inaccurate": 1,
    "Moderately Inaccurate": 2,
    "Neither Accurate Nor Inaccurate": 3,
    "Moderately Accurate": 4,
    "Very Accurate": 5
}
options_list = list(scale.keys())

st.header("Clinical Questionnaire")
st.write("Please select how accurately each statement describes you.")

answers = {}

questions = {
    1: "1. Am the life of the party.",
    2: "2. Sympathize with others' feelings.",
    3: "3. Get chores done right away.",
    4: "4. Have frequent mood swings.",
    5: "5. Have a vivid imagination.",
    6: "6. Don't talk a lot.",
    7: "7. Am not interested in other people's problems.",
    8: "8. Often forget to put things back in their proper place.",
    9: "9. Am relaxed most of the time.",
    10: "10. Am not interested in abstract ideas.",
    11: "11. Talk to a lot of different people at parties.",
    12: "12. Feel others' emotions.",
    13: "13. Like order.",
    14: "14. Get upset easily.",
    15: "15. Have difficulty understanding abstract ideas.",
    16: "16. Keep in the background.",
    17: "17. Am not really interested in others.",
    18: "18. Make a mess of things.",
    19: "19. Seldom feel blue.",
    20: "20. Do not have a good imagination."
}

for q_num, q_text in questions.items():
    user_choice = st.radio(q_text, options_list, key=f"q{q_num}")
    answers[q_num] = scale[user_choice]

def reverse_score(val):
    return 6 - val

def get_trait_description(trait, score):
    if score >= 15:
        level = "High"
        if trait == "Extraversion": desc = "You are highly outgoing, energetic, and draw energy from social interactions."
        elif trait == "Agreeableness": desc = "You are highly empathetic, cooperative, and value harmony in relationships."
        elif trait == "Conscientiousness": desc = "You are highly organized, disciplined, and goal-oriented."
        elif trait == "Neuroticism": desc = "You may experience emotional reactivity and stress more intensely than others."
        elif trait == "Openness": desc = "You are highly imaginative, curious, and open to new and abstract experiences."
    elif score >= 10:
        level = "Moderate"
        if trait == "Extraversion": desc = "You balance social engagement with a need for personal downtime."
        elif trait == "Agreeableness": desc = "You are generally warm but can maintain objective boundaries when necessary."
        elif trait == "Conscientiousness": desc = "You are reliable but flexible, balancing structure with spontaneity."
        elif trait == "Neuroticism": desc = "You generally handle stress well but may feel overwhelmed in high-pressure situations."
        elif trait == "Openness": desc = "You appreciate both traditional methods and new ideas in equal measure."
    else:
        level = "Low"
        if trait == "Extraversion": desc = "You are introverted, reserved, and recharge by spending time alone."
        elif trait == "Agreeableness": desc = "You are competitive, analytical, and prioritize logic over social harmony."
        elif trait == "Conscientiousness": desc = "You prefer flexibility and spontaneity over strict schedules and routines."
        elif trait == "Neuroticism": desc = "You are emotionally highly resilient, calm, and rarely easily upset."
        elif trait == "Openness": desc = "You are highly practical, concrete, and prefer familiar routines over abstract concepts."
    
    return level, desc

# =========================================================
# 5. DATA PROCESSING TRIGGER
# =========================================================
if st.button("Generate Clinical Profile"):
    if not consent:
        st.error("⚠️ Please check the informed consent box before proceeding.")
    elif not name:
        st.error("⚠️ Please enter the subject's name before executing scoring protocols.")
    else:
        st.success("Executing scoring protocols...")

        ext = answers[1] + answers[11] + reverse_score(answers[6]) + reverse_score(answers[16])
        agr = answers[2] + answers[12] + reverse_score(answers[7]) + reverse_score(answers[17])
        con = answers[3] + answers[13] + reverse_score(answers[8]) + reverse_score(answers[18])
        neu = answers[4] + answers[14] + reverse_score(answers[9]) + reverse_score(answers[19])
        ope = answers[5] + reverse_score(answers[10]) + reverse_score(answers[15]) + reverse_score(answers[20])

        st.subheader("Your Big Five Trait Scores (Out of 20)")
        st.write(f"**Extraversion:** {ext}")
        st.write(f"**Agreeableness:** {agr}")
        st.write(f"**Conscientiousness:** {con}")
        st.write(f"**Neuroticism:** {neu}")
        st.write(f"**Openness (Intellect):** {ope}")

        # PDF COMPILATION
        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_fill_color(30, 41, 59) 
        pdf.rect(0, 0, 210, 40, 'F')
        
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 22)
        pdf.cell(0, 15, txt="CLINICAL PERSONALITY PROFILE", ln=True, align='C')
        pdf.set_font("Arial", 'I', 14)
        pdf.cell(0, 5, txt="Mini-IPIP Big Five Assessment", ln=True, align='C')
        
        pdf.set_y(50)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, txt=f"Prepared For: {name}", ln=True)
        pdf.line(10, 60, 200, 60) 
        pdf.ln(5)

        traits = [
            ("Extraversion", ext),
            ("Agreeableness", agr),
            ("Conscientiousness", con),
            ("Neuroticism", neu),
            ("Openness", ope)
        ]

        for trait, score in traits:
            level, description = get_trait_description(trait, score)
            
            pdf.set_font("Arial", 'B', 12)
            pdf.set_text_color(41, 128, 185) 
            pdf.cell(0, 10, txt=f"{trait} - Score: {score}/20 ({level})", ln=True)
            
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(50, 50, 50) 
            pdf.multi_cell(0, 6, txt=description)
            pdf.ln(4)

        # DOWNLOAD BUTTON
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf.output(tmp_file.name)
            
            with open(tmp_file.name, "rb") as f:
                st.download_button(
                    label="Download Clinical Report (PDF)",
                    data=f,
                    file_name=f"{name}_clinical_profile.pdf",
                    mime="application/pdf"
                )