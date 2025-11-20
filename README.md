# DineEase - Restaurant Reservation System

An AI-powered restaurant reservation chatbot built with Streamlit and LangChain.

## Features

- 🔍 Search restaurants by area, cuisine, ambience, and rating
- 📅 Check real-time availability
- 🎯 Get personalized recommendations
- 📝 Book tables instantly
- 💬 Natural language conversation interface

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **LLM**: Meta LLaMA 3.1 8B (via OpenRouter)
- **Database**: TinyDB (JSON-based)

## Local Setup

1. Clone the repository:
```bash
git clone https://github.com/Abhiksahu3092/DineEase.git
cd DineEase
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with your OpenRouter API key:
```bash
OPENROUTER_API_KEY=your_api_key_here
```

5. Run the app:
```bash
streamlit run streamlit_app.py
```

## Deployment on Render

1. Push your code to GitHub

2. Go to [Render Dashboard](https://dashboard.render.com/)

3. Click "New +" → "Web Service"

4. Connect your GitHub repository

5. Render will automatically detect the `render.yaml` configuration

6. Add environment variable:
   - Key: `OPENROUTER_API_KEY`
   - Value: Your OpenRouter API key

7. Click "Create Web Service"

Your app will be live at: `https://your-app-name.onrender.com`

## Project Structure

```
DineEase/
├── backend/
│   ├── agent.py          # Main agent logic
│   ├── tools.py          # Restaurant search & booking tools
│   ├── db.py             # Database operations
│   └── data_gen.py       # Generate sample restaurant data
├── data/
│   ├── restaurants.json  # Restaurant database
│   └── reservations.json # Reservations database
├── prompts/
│   └── unified_prompt.txt # Agent system prompt
├── streamlit_app.py      # Main Streamlit app
├── requirements.txt      # Python dependencies
├── render.yaml           # Render deployment config
└── .env                  # Environment variables (not in repo)
```

## Usage Examples

**Search restaurants:**
- "Show me Italian restaurants in Hauz Khas"
- "Find a cozy restaurant with rating above 4"

**Check availability:**
- "Is Pasta Garden available for 4 people at 7pm today?"

**Book a table:**
- "Book Pasta Garden for 4 people at 7pm, name is John, phone 9876543210"

**Get recommendations:**
- "Recommend a romantic restaurant in Connaught Place for 2 people"

## Environment Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key for LLM access

## License

MIT
