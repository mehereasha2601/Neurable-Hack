# 🧠 Stress Relief Companion

Real-time stress monitoring and relief application using EEG data, AI assistance, and age-appropriate interventions.

## ✅ Test Results

**File Structure**: ✓ All required files present  
**Python Syntax**: ✓ All files have valid syntax  
**Dependencies**: ⚠ Need to be installed (see Setup below)

## 🚀 Quick Start

### Option 1: Using Setup Script (Recommended)

```bash
cd stress-relief-app
./setup.sh
source venv/bin/activate
streamlit run app.py
```

### Option 2: Manual Setup

```bash
cd stress-relief-app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📋 Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`:
  - streamlit
  - plotly
  - pandas
  - numpy
  - supabase (optional, for database)
  - groq (optional, for AI)
  - websockets
  - python-dotenv

## ⚙️ Configuration

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env`** with your API keys:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   GROQ_API_KEY=your_groq_api_key
   ```

3. **WebSocket URL** (default in app):
   - Real stream: `wss://stream2.mindfulmakers.xyz`
   - Or use mock data for testing

## 🧪 Testing

Run the test script to verify setup:

```bash
python3 test_app.py
```

This will check:
- ✓ File structure
- ✓ Python syntax
- ⚠ Dependencies (will show if missing)

## 📁 Project Structure

```
stress-relief-app/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── setup.sh              # Setup script
├── test_app.py           # Test script
├── utils/
│   ├── stress_detector.py    # Age-aware stress detection
│   ├── ai_helper.py          # Groq AI integration
│   ├── db_helper.py          # Supabase database
│   └── neurable_stream.py    # EEG stream connection
├── components/
│   ├── interventions.py      # Stress relief activities
│   └── visualizations.py     # Charts and graphs
└── data/
    └── stories.json          # Backup calming stories
```

## 🎯 Features

- **Real-time EEG Monitoring**: Connect to Neurable stream or use mock data
- **Age-Aware Detection**: Different thresholds for child/teen/adult
- **AI-Powered Interventions**: Groq AI generates calming stories and prompts
- **Database Integration**: Save readings and journal entries to Supabase
- **Beautiful UI**: Modern design matching mindful-monitor aesthetic
- **Crisis Support**: Emergency resources and immediate calming techniques

## 🔌 WebSocket Connection

The app connects to: `wss://stream2.mindfulmakers.xyz`

- Uses SSL (WSS) with certificate verification disabled for testing
- Automatic reconnection on failure
- Falls back to mock data after 3 retries

## 🐛 Troubleshooting

**Dependencies not installing?**
- Use virtual environment: `python3 -m venv venv`
- Upgrade pip: `pip install --upgrade pip`
- Install individually: `pip install streamlit plotly pandas numpy websockets`

**App won't start?**
- Check Python version: `python3 --version` (needs 3.8+)
- Verify dependencies: `python3 test_app.py`
- Check for errors in terminal

**WebSocket connection fails?**
- Enable "Use Mock Data" in settings for testing
- Check internet connection
- Verify stream server is running

**AI features not working?**
- Check GROQ_API_KEY in `.env`
- App will use fallback messages if API unavailable

**Database errors?**
- Check SUPABASE_URL and SUPABASE_KEY in `.env`
- App falls back to local storage if DB unavailable

## 📝 Usage

1. **Select Age Group**: Choose child, teen, or adult
2. **Start Monitoring**: Click "Start Monitoring" button
3. **Baseline Calibration**: Wait 30 seconds for personal baseline
4. **Monitor Stress**: Watch real-time graph and status
5. **Interventions**: Automatic suggestions when stress detected
6. **Journal**: Record thoughts and feelings

## 🎨 UI Features

- Beautiful gradient backgrounds
- Age-specific color schemes
- Smooth animations
- Responsive design
- Real-time graphs
- Crisis intervention modal

## 📚 Documentation

- `INTEGRATION_GUIDE.md` - Component integration details
- `WEBSOCKET_INTEGRATION.md` - WebSocket connection guide

## ✅ Current Status

- ✓ All files created and validated
- ✓ Python syntax verified
- ⚠ Dependencies need installation
- ✓ Ready to run after setup

## 🚀 Next Steps

1. Run `./setup.sh` or install dependencies manually
2. Configure `.env` with your API keys (optional)
3. Run `streamlit run app.py`
4. Select age group and start monitoring!

---

**Note**: The app works with or without API keys. Mock data mode allows full testing without external services.

