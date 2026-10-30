import streamlit as st
from margaret_ai import ask_margaret, MODEL

st.set_page_config(page_title="Margaret", page_icon="🌿")
st.title("Margaret")
st.caption("A country care navigator for older Australians who want to stay independent.")

with st.sidebar:
    st.subheader("About you (optional)")
    who = st.radio("Who is asking?", ["I'm asking for myself", "I'm asking for a family member"])
    age = st.number_input("Age", 50, 110, 78)
    town = st.text_input("Town or region", "Clare")
    lives = st.selectbox("Lives", ["alone", "with a partner", "with family", "other"])

examples = [
    "Mum is 84 and struggling with the shopping and cleaning. Where do we start?",
    "I've had a fall and I'm worried about managing at home. What help is there?",
    "What is an aged care assessment and how long does it take?",
]
pick = st.selectbox("Try an example, or write your own below", [""] + examples)
q = st.text_area("Your question", pick, height=100)

if st.button("Ask Margaret", type="primary", disabled=not q.strip()):
    with st.spinner("Margaret is thinking…"):
        try:
            answer = ask_margaret(q, {"who": who, "age": age, "town": town, "lives": lives})
            st.markdown(answer)
            st.caption(f"Answered by Gemma 4 ({MODEL}) via the Gemini API. General information, not medical advice.")
        except Exception as e:
            st.error("Margaret couldn't answer just now. Please try again in a moment.")
            st.caption(str(e)[:200])

st.divider()
st.caption("In an emergency call 000. For aged care services: My Aged Care, 1800 200 422, myagedcare.gov.au.")
