
# AI Voice Bot
This is a voicebot which talkes voice as a Input and Give Response to User Queries


## Setup
1. Clone the repo: `git clone <repo_link>`
3. Install dependencies: `pip install -r requirements.txt`
4. Set API Key: `export GROQ_API_KEY="your_api_key"`
5. Run FastAPI: `uvicorn voice_bot:app --host 0.0.0.0 --port 8000 --reload`
6. Run Streamlit: `streamlit run app.py`
