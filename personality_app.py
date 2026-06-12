# =========================================================
# 1. IMPORTS & DEPENDENCIES
# WHY: Load external libraries required to run the app.
# - 'streamlit' (st) builds the interactive web interface.
# - 'FPDF' is the engine that writes and formats our PDF report.
# - 'tempfile' safely handles file creation in the cloud without crashing the server.
# =========================================================
import streamlit as st
from fpdf import FPDF
import tempfile

# =========================================================
# 2. UI INITIALIZATION
# WHY: Set up the visual entry point for the user.
# =========================================================
st.title("Clinical Personality Assessment (Mini-IPIP)")
st.write("This 20-item assessment measures the Big Five personality traits.")

st.header("Patient / Subject Information")
name = st.text_input("Full Name:")

# =========================================================
# 3. PSYCHOMETRIC SCALE SETUP
# WHY: Map the qualitative Likert scale to quantitative values for scoring.
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

# The standardized 20 items from the Mini-IPIP
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

# =========================================================
# 4. INTERFACE AUTOMATION
# WHY: Loop through the questions dictionary to automatically render 
# 20 radio buttons and store the numerical value of the user's choices.
# =========================================================
for q_num, q_text in questions.items():
    user_choice = st.radio(q_text, options_list, key=f"q{q_num}")
    answers[q_num] = scale[user_choice]

# =========================================================
# 5. REVERSE SCORING FUNCTION
# WHY: Mitigate acquiescence bias. Flips the score mathematically 
# (e.g., Maximum Scale Value + 1 - Raw Score).
# =========================================================
def reverse_score(val):
    return 6 - val

# =========================================================
# 6. CLINICAL INTERPRETATION ENGINE
# WHY: Translates raw mathematical scores into descriptive clinical profiles 
# based on standardized thresholds (High, Moderate, Low).
# =========================================================
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
# 7. DATA PROCESSING & PDF GENERATION TRIGGER
# =========================================================
if st.button("Generate Clinical Profile"):
    if name:
        st.success("Executing scoring protocols...")

        # Calculate Trait Scores using the Mini-IPIP key
        ext = answers[1] + answers[11] + reverse_score(answers[6]) + reverse_score(answers[16])
        agr = answers[2] + answers[12] + reverse_score(answers[7]) + reverse_score(answers[17])
        con = answers[3] + answers[13] + reverse_score(answers[8]) + reverse_score(answers[18])
        neu = answers[4] + answers[14] + reverse_score(answers[9]) + reverse_score(answers[19])
        ope = answers[5] + reverse_score(answers[10]) + reverse_score(answers[15]) + reverse_score(answers[20])

        # Display results on the web app interface
        st.subheader("Your Big Five Trait Scores (Out of 20)")
        st.write(f"**Extraversion:** {ext}")
        st.write(f"**Agreeableness:** {agr}")
        st.write(f"**Conscientiousness:** {con}")
        st.write(f"**Neuroticism:** {neu}")
        st.write(f"**Openness (Intellect):** {ope}")

        # =========================================================
        # 8. AESTHETIC PDF COMPILATION
        # WHY: Construct a professional, colored, and dynamically formatted document.
        # =========================================================
        pdf = FPDF()
        pdf.add_page()
        
        # Draw a dark slate-grey rectangular header
        pdf.set_fill_color(30, 41, 59) 
        pdf.rect(0, 0, 210, 40, 'F')
        
        # White Header Text
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 22)
        pdf.cell(0, 15, txt="CLINICAL PERSONALITY PROFILE", ln=True, align='C')
        pdf.set_font("Arial", 'I', 14)
        pdf.cell(0, 5, txt="Mini-IPIP Big Five Assessment", ln=True, align='C')
        
        # User Info Section (Reset to black text)
        pdf.set_y(50)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, txt=f"Prepared For: {name}", ln=True)
        pdf.line(10, 60, 200, 60) # Visual divider line
        pdf.ln(5)

        # Loop through calculated traits to print them into the PDF
        traits = [
            ("Extraversion", ext),
            ("Agreeableness", agr),
            ("Conscientiousness", con),
            ("Neuroticism", neu),
            ("Openness", ope)
        ]

        for trait, score in traits:
            level, description = get_trait_description(trait, score)
            
            # Trait Name and Score (Blue bold text)
            pdf.set_font("Arial", 'B', 12)
            pdf.set_text_color(41, 128, 185) 
            pdf.cell(0, 10, txt=f"{trait} - Score: {score}/20 ({level})", ln=True)
            
            # Clinical Description (Dark grey regular text)
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(50, 50, 50) 
            pdf.multi_cell(0, 6, txt=description)
            pdf.ln(4) # Spacing between traits

        # =========================================================
        # 9. SECURE CLOUD FILE HANDLING & DOWNLOAD
        # WHY: Create a temporary file buffer so the user can download the PDF 
        # without requiring server-side storage permissions.
        # =========================================================
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf.output(tmp_file.name)
            
            with open(tmp_file.name, "rb") as f:
                st.download_button(
                    label="Download Clinical Report (PDF)",
                    data=f,
                    file_name=f"{name}_clinical_profile.pdf",
                    mime="application/pdf"
                )
    else:
        st.error("Please enter the subject's name before executing scoring protocols.")