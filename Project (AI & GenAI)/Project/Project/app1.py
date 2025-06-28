import streamlit as st
import tempfile

from modules.extract import extract_text_from_pdf
from modules.chunk import split_text
from modules.embed_store import embed_and_store
from modules.rag_answer import summarize_report, answer_question_with_context
from modules.language_selector import language_selector, translate_summary
from modules.nutrition_chart import generate_diet_from_summary_ai

# App configuration
st.set_page_config(page_title="Medical Report Analyzer", layout="centered")
st.title("RAG-based Medical Report Analyzer")
st.markdown("Upload your medical report PDF to generate a summary and personalized diet chart.")

# 🌐 Language selection
lang_code, lang_name = language_selector()
st.markdown("---")

# 📄 File uploader
uploaded_file = st.file_uploader("📄 Upload your medical report (PDF only)", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.info("⏳ Extracting and processing the report...")
    raw_text = extract_text_from_pdf(tmp_path)
    chunks = split_text(raw_text)
    index, model_embed, stored_chunks = embed_and_store(chunks)

    # Session state init
    if "summary_generated" not in st.session_state:
        st.session_state.summary_generated = False
    if "translated_summary" not in st.session_state:
        st.session_state.translated_summary = ""
    if "diet_chart" not in st.session_state:
        st.session_state.diet_chart = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "user_question" not in st.session_state:
        st.session_state.user_question = ""

    # 🢾 Generate Summary button
    if not st.session_state.summary_generated:
        if st.button("🢾 Generate Summary"):
            with st.spinner("Generating medical summary..."):
                summary = summarize_report(stored_chunks)
                translated = translate_summary(summary, lang_code)
                st.session_state.translated_summary = translated
                st.session_state.summary_generated = True

    # ✅ Show summary if generated
    if st.session_state.summary_generated:
        st.success("✅ Summary generated!")
        st.markdown(f"### 📋 Medical Summary ({lang_name})")
        st.markdown(st.session_state.translated_summary, unsafe_allow_html=True)

        # 📅 Download Summary
        st.download_button(
            label="📅 Download Summary",
            data=st.session_state.translated_summary,
            file_name="medical_summary.txt",
            mime="text/plain"
        )

        # 🥗 Generate Diet Plan button (after summary)
        if st.button("Generate Diet Plan"):
            with st.spinner("Creating personalized diet plan..."):
                diet_chart = generate_diet_from_summary_ai(st.session_state.translated_summary)

                if lang_code != "en":
                    with st.spinner(f"🔄 Translating diet chart to {lang_name}..."):
                        translated_diet = translate_summary(diet_chart, lang_code)
                else:
                    translated_diet = diet_chart

                st.session_state.diet_chart = translated_diet

    # ✅ Show diet chart if generated
    if st.session_state.diet_chart:
        st.success("Diet plan generated!")
        st.markdown(f"### Personalized Nutritional Diet Chart ({lang_name})")
        st.markdown(st.session_state.diet_chart, unsafe_allow_html=True)

        # 📅 Download Diet Plan
        st.download_button(
            label="📅 Download Diet Plan",
            data=st.session_state.diet_chart,
            file_name="diet_plan.txt",
            mime="text/plain"
        )

        # 💬 Chatbot interface
        st.markdown("---")
        st.header("💬 Ask a Question about Your Report")

        def submit_question():
            user_question = st.session_state.user_question
            if user_question:
                with st.spinner("💭 Thinking..."):
                    response = answer_question_with_context(
                        user_question,
                        stored_chunks,
                        index,
                        model_embed
                    )
                st.session_state.chat_history.append((user_question, response))
                st.session_state.user_question = ""

        st.text_input(
            "Ask anything from your medical report:",
            key="user_question",
            on_change=submit_question,
        )

        # Display full chat history
        for question, answer in st.session_state.chat_history:
            st.markdown(f"**🧑 You:** {question}")
            st.markdown(f"**🤖 Assistant:** {answer}")

# 🔄 Reset App Button (always visible)
st.markdown("---")
if st.button("🔄 Reset App"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()
