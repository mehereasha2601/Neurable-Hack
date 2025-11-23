# Integration Guide

## Complete Component Integration

This guide explains how all components are integrated in the Stress Relief Companion app.

---

## 1. UI/Streamlit Integration ✅

### Custom CSS Styling
- **Location**: `app.py` lines 42-120
- **Features**:
  - Gradient backgrounds for status cards
  - Smooth animations (slideIn, pulse)
  - Responsive design
  - Color-coded connection status
  - Hover effects on buttons

### Streamlit Components Used
- `st.markdown()` for custom HTML/CSS
- `st.columns()` for responsive layouts
- `st.plotly_chart()` for real-time graphs
- `st.spinner()` for loading states
- `st.expander()` for collapsible content

---

## 2. EEG Stream Integration ✅

### Connection Logic
**Location**: `app.py` - `connect_eeg_stream()` function

**Features**:
- Automatic fallback to mock data if connection fails
- Reconnection logic with retry counter
- Background threading for async operations
- Connection status tracking (connected/connecting/disconnected)

**Code Flow**:
```python
1. Check if mock data is enabled
2. If real stream: Initialize NeurableStream with WebSocket URL
3. Connect in background thread (non-blocking)
4. Update connection status
5. Fallback to mock after 3 retries
```

### Data Retrieval
**Location**: `app.py` - `get_eeg_data()` function

**Features**:
- Gets data from real stream if connected
- Generates realistic mock data if stream unavailable
- Handles errors gracefully
- Returns standardized data format

### Usage in Monitoring Loop
- Called every 0.5 seconds during monitoring
- Data passed to stress detector
- Automatic reconnection on failure

---

## 3. AI Integration (Groq) ✅

### Initialization
**Location**: `app.py` - `initialize_session_state()`

```python
st.session_state.ai_helper = AIHelper()
```

### AI Functions Wired Up

#### 1. Calming Messages
**Location**: `render_intervention_panel()`
- Called automatically when intervention panel opens
- Age and stress-level aware
- Shows immediately with no loading

#### 2. Calming Stories
**Location**: `render_intervention_panel()` - "Read Calming Story" button
- Shows spinner during generation
- Caches result for later viewing
- Error handling with fallback message

#### 3. Journal Prompts
**Location**: `render_intervention_panel()` - "Journal Prompts" button
- Generates age-appropriate questions
- Includes journal entry form
- Saves entries to database

### Error Handling
- Try/except around all AI calls
- Fallback messages if API fails
- User-friendly error messages
- No app crashes

---

## 4. Database Integration (Supabase) ✅

### Initialization
**Location**: `app.py` - `initialize_session_state()`

```python
st.session_state.db_helper = DBHelper()
```

### Database Operations

#### 1. Stress Readings
**Location**: `update_monitoring()`
- Saves every 10 readings (not every reading for performance)
- Includes metadata (level, quality, age_group)
- Handles errors gracefully

#### 2. Intervention Results
**Location**: `render_intervention_panel()` - "I'm Feeling Better" button
- Saves when user dismisses intervention
- Tracks intervention effectiveness

#### 3. Journal Entries
**Location**: `render_intervention_panel()` - "Save Entry" button
- Saves journal text and prompts
- Falls back to local storage if DB unavailable
- Shows success/error feedback

### Offline Mode
- Falls back to session state storage
- Data persists during session
- Can be synced later if needed

---

## 5. Testing Modes ✅

### Mock Data Toggle
**Location**: Sidebar settings

**Features**:
- Toggle between real EEG and mock data
- Mock data simulates realistic stress patterns
- Useful for development and testing

### Test Each Component

#### Test EEG Stream
1. Toggle "Use Mock Data" OFF
2. Enter WebSocket URL
3. Click "Start Monitoring"
4. Check connection status

#### Test AI Functions
1. Start monitoring
2. Wait for intervention panel
3. Click each AI button:
   - "Read Calming Story"
   - "Journal Prompts"
4. Verify loading spinners and results

#### Test Database
1. Generate journal entry
2. Save entry
3. Check success message
4. Verify in Supabase dashboard

---

## 6. Polish & UX Enhancements ✅

### Loading States
- Spinners for AI generation
- Progress indicators for baseline calibration
- Connection status indicators

### Error Messages
- User-friendly error messages
- No technical jargon
- Actionable feedback

### Success Feedback
- Green success messages
- Confirmation for saved entries
- Visual indicators for status

### Performance Optimizations
- Data limited to last 120 readings (2 minutes)
- Database saves batched (every 10 readings)
- Cached AI responses
- Efficient graph updates

### Smooth Transitions
- CSS animations for panels
- Fade-in effects
- Hover states on buttons

---

## Integration Checklist

### ✅ Completed
- [x] Custom CSS styling
- [x] EEG stream connection with reconnection
- [x] AI calls with loading states
- [x] Database saves for all data types
- [x] Mock data mode for testing
- [x] Error handling throughout
- [x] Loading indicators
- [x] Success/error feedback
- [x] Offline mode support

### 🔄 How It All Works Together

1. **User selects age group** → Initializes detector with age-specific thresholds

2. **User starts monitoring** → 
   - Connects to EEG stream (or uses mock)
   - Begins collecting baseline data
   - Updates graph in real-time

3. **Baseline calibrated** → 
   - Personal thresholds calculated
   - Stress detection begins
   - Data saved to database

4. **Stress detected** → 
   - Intervention panel appears
   - AI generates calming message
   - User can access activities

5. **User interacts** → 
   - AI generates stories/prompts
   - Journal entries saved
   - Intervention results tracked

6. **Session ends** → 
   - Final data saved
   - Session summary available

---

## Running the App

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GROQ_API_KEY=your_key
export SUPABASE_URL=your_url
export SUPABASE_KEY=your_key

# Run the app
streamlit run app.py
```

---

## Troubleshooting

### EEG Stream Not Connecting
- Check WebSocket URL format
- Verify Neurable device is running
- Enable mock data for testing
- Check connection status in sidebar

### AI Not Working
- Verify GROQ_API_KEY in .env
- Check API quota/limits
- App will use fallback messages

### Database Errors
- Verify SUPABASE_URL and SUPABASE_KEY
- Check table names match schema
- App falls back to local storage

---

## Next Steps

1. **Deploy to Streamlit Cloud**
2. **Add user authentication**
3. **Implement data export**
4. **Add more intervention types**
5. **Create admin dashboard**

---

## Support

For issues or questions:
- Check logs in terminal
- Review error messages in app
- Verify environment variables
- Test with mock data first

