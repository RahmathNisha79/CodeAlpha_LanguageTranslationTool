
import streamlit as st
import requests

st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 Language Translation Tool")
st.write("Translate text easily from one language to another.")

languages = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "Telugu": "te",
    "Malayalam": "ml",
    "Kannada": "kn",
    "French": "fr",
    "Spanish": "es",
    "German": "de"
}

col1, col2 = st.columns(2)

with col1:
    source = st.selectbox(
        "Translate From",
        list(languages.keys()),
        index=0
    )

with col2:
    target = st.selectbox(
        "Translate To",
        list(languages.keys()),
        index=1
    )

text = st.text_area(
    "Enter your text",
    placeholder="Type your text here..."
)

if st.button("Translate", type="primary"):
    if not text.strip():
        st.warning("Please enter some text.")

    elif source == target:
        st.warning("Please select different languages.")

    else:
        try:
            with st.spinner("Translating..."):
                response = requests.get(
                    "https://api.mymemory.translated.net/get",
                    params={
                        "q": text,
                        "langpair": (
                            f"{languages[source]}|"
                            f"{languages[target]}"
                        )
                    },
                    timeout=20
                )

                response.raise_for_status()
                data = response.json()

                translated = data.get(
                    "responseData", {}
                ).get("translatedText", "")

                if (
                    data.get("responseStatus") != 200
                    or not translated
                ):
                    st.error(
                        "Translation failed. Please try again."
                    )
                else:
                    st.subheader("Translated Result")
                    st.text_area(
                        "Output",
                        value=translated,
                        height=120
                    )

                    st.caption(
                        "Translation is provided by an "
                        "external service."
                    )

        except requests.RequestException:
            st.error(
                "Could not connect to the translation service. "
                "Check your internet and try again."
            )

