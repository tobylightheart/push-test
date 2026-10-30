## Model
Margaret uses **Gemma 4** (`gemma-4-26b-a4b-it`) through the Gemini API with the `google-genai` SDK. Each question is one Gemma call.
- Licence: [Gemma 4 Apache 2.0](https://ai.google.dev/gemma/apache_2) · [Gemini API Additional Terms](https://ai.google.dev/gemini-api/terms)

## Run it
```
pip install -r requirements.txt
echo GEMINI_API_KEY=your-key > .env
streamlit run app.py
```

## AI tools we used
Claude Code (Claude Opus 5.5) helped write the Gemma backend and Streamlit page.
