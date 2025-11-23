"""
Age-specific stress relief intervention activities.

Exact port from mindful-monitor React components to Streamlit.
Matches all UI elements, colors, layouts, and interactions.
"""

import streamlit as st
from typing import List, Dict
import time
import random


class InterventionManager:
    """Manages age-specific stress relief intervention activities."""
    
    def __init__(self):
        """Initialize the intervention manager."""
        self.interventions = {
            'child': self._child_intervention,
            'teen': self._teen_intervention,
            'adult': self._adult_intervention
        }
    
    def render_intervention(self, age_group: str, on_close_callback=None):
        """
        Render age-appropriate intervention panel.
        
        Args:
            age_group: 'child', 'teen', or 'adult'
            on_close_callback: Function to call when intervention is closed
        """
        if age_group in self.interventions:
            return self.interventions[age_group](on_close_callback)
        else:
            st.error(f"Unknown age group: {age_group}")
    
    def _child_intervention(self, on_close_callback=None):
        """Child intervention: Story Time & Calm Activities - exact port from ChildIntervention.tsx"""
        
        # Main card with exact styling from React
        st.markdown("""
        <style>
        .child-intervention-card {
            background: hsl(0, 0%, 100%);
            border-left: 4px solid hsl(28, 95%, 65%);
            border-radius: 0.75rem;
            padding: 1.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            background: linear-gradient(135deg, hsl(45, 100%, 97%), hsl(28, 95%, 95%));
        }
        </style>
        <div class="child-intervention-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">😰</div>
            <h2 style="font-size: 1.5rem; font-weight: bold; margin-bottom: 0.5rem; color: hsl(220, 15%, 20%);">
                You seem stressed! Let's try something fun!
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tabs matching React TabsList
        tab1, tab2 = st.tabs(["📖 Story Time", "🎨 Calm Activities"])
        
        with tab1:
            # Initialize session state for story
            if 'child_story' not in st.session_state:
                st.session_state.child_story = None
            if 'child_generating' not in st.session_state:
                st.session_state.child_generating = False
            
            # Generate button with exact styling
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("✨ Generate New Story", 
                            key="child_gen_story", 
                            use_container_width=True,
                            type="secondary"):
                    st.session_state.child_generating = True
                    # Simulate story generation (in real app, call AI helper)
                    with st.spinner("Creating Your Story..."):
                        time.sleep(2)
                        story = (
                            "Once upon a time, in a magical forest filled with friendly animals, "
                            "there lived a little bunny named Fluffy. Fluffy loved to hop around and make new friends. "
                            "One sunny day, Fluffy felt a bit worried about meeting new friends. "
                            "But then, a wise old owl told Fluffy a secret: 'When you feel worried, just take three deep breaths "
                            "and think of something that makes you smile!' Fluffy tried it, and it worked like magic! "
                            "Soon, Fluffy was hopping happily and making lots of new friends. The end."
                        )
                        st.session_state.child_story = story
                        st.session_state.child_generating = False
                    st.rerun()
            
            # Story display card
            if st.session_state.child_story:
                st.markdown(f"""
                <div style="background: hsl(0, 0%, 100%); 
                            padding: 1.5rem; 
                            border-radius: 0.5rem; 
                            margin: 1rem 0;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <p style="font-size: 1.25rem; line-height: 1.75; color: hsl(220, 15%, 20%);">
                        {st.session_state.child_story}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Read aloud button
                if st.button("🔊 Read Story Aloud", key="child_read_aloud", use_container_width=True):
                    st.info("📢 Text-to-speech would play here")
        
        with tab2:
            # Calm activities with exact border styling
            st.markdown("""
            <div style="border: 4px solid hsl(142, 70%, 55%); border-radius: 0.75rem; overflow: hidden; margin-top: 1rem;">
                <div style="background: hsl(142, 70%, 55%); 
                            color: white; 
                            padding: 0.75rem; 
                            text-align: center; 
                            font-weight: 600;">
                    🎨 Follow Along: Guided Painting
                </div>
                <div style="aspect-ratio: 16/9; 
                            background: hsl(220, 20%, 92%); 
                            display: flex; 
                            align-items: center; 
                            justify-content: center; 
                            flex-direction: column;
                            padding: 2rem;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">🎨</div>
                    <p style="color: hsl(220, 15%, 45%); font-size: 1rem;">Calming painting video will play here</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Footer button - exact match
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ I feel better now", 
                    key="child_done", 
                    use_container_width=True,
                    type="primary"):
            if on_close_callback:
                on_close_callback()
            st.session_state.intervention_active = False
            st.rerun()
    
    def _teen_intervention(self, on_close_callback=None):
        """Teen intervention: Reading, Art, Meditation & Journaling - exact port from TeenIntervention.tsx"""
        
        # Header card
        st.markdown("""
        <div style="background: hsl(0, 0%, 100%); 
                    border-left: 4px solid hsl(210, 75%, 65%); 
                    border-radius: 0.75rem; 
                    padding: 1.5rem; 
                    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
            <h2 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; color: hsl(220, 15%, 20%);">
                Hey, looks like you could use a break 💙
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 4 tabs exact match
        tab1, tab2, tab3, tab4 = st.tabs(["📖 Reading", "🎨 Art", "🧘 Meditation", "📝 Journal"])
        
        with tab1:
            st.markdown("""
            <div style="background: hsl(220, 20%, 92%); padding: 1.5rem; border-radius: 0.5rem;">
                <p style="font-size: 1.125rem; line-height: 1.75; color: hsl(220, 15%, 20%);">
                    Mindfulness reading content will be generated here. Focus on the present moment, 
                    your breath, and remember that this feeling is temporary.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("""
            <div style="aspect-ratio: 16/9; 
                        background: hsl(220, 20%, 92%); 
                        border-radius: 0.5rem; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center;">
                <p style="color: hsl(220, 15%, 45%);">Art therapy video placeholder</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("""
            <div style="background: hsl(220, 20%, 92%); padding: 1.5rem; border-radius: 0.5rem; text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🧘</div>
                <p style="font-size: 1.125rem; margin-bottom: 1rem; color: hsl(220, 15%, 20%);">5-minute guided meditation</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("▶️ Start Meditation", key="teen_meditation", use_container_width=True):
                st.success("Meditation started! Focus on your breathing.")
        
        with tab4:
            # Feelings grid - exact 3-column layout
            st.markdown("#### How are you feeling?")
            feelings = [
                ("😰", "Anxious"), ("😢", "Sad"), ("😤", "Frustrated"),
                ("😴", "Tired"), ("😨", "Overwhelmed"), ("😶", "Numb"),
                ("🤔", "Confused"), ("😠", "Angry"), ("😖", "Stressed")
            ]
            
            if 'teen_feelings' not in st.session_state:
                st.session_state.teen_feelings = []
            
            # 3-column grid layout
            for row in range(0, len(feelings), 3):
                cols = st.columns(3)
                for idx, col in enumerate(cols):
                    if row + idx < len(feelings):
                        emoji, label = feelings[row + idx]
                        with col:
                            is_selected = label in st.session_state.teen_feelings
                            button_label = f"{emoji}\n\n{label}"
                            
                            if st.button(button_label, 
                                        key=f"feeling_{label}", 
                                        use_container_width=True,
                                        type="primary" if is_selected else "secondary"):
                                if label in st.session_state.teen_feelings:
                                    st.session_state.teen_feelings.remove(label)
                                else:
                                    st.session_state.teen_feelings.append(label)
                                st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Triggers
            st.markdown("#### What's on your mind?")
            triggers = ["School/Work", "Relationships", "Family", "Health", 
                       "Money", "Future", "Social Media", "Other"]
            
            if 'teen_triggers' not in st.session_state:
                st.session_state.teen_triggers = []
            
            selected_triggers = st.multiselect(
                "Select what's bothering you:",
                triggers,
                default=st.session_state.teen_triggers,
                key="teen_triggers_select",
                label_visibility="collapsed"
            )
            st.session_state.teen_triggers = selected_triggers
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Notes textarea
            st.markdown("#### Any other thoughts?")
            notes = st.text_area(
                "Optional: Share what's on your mind...",
                height=120,
                key="teen_notes",
                label_visibility="collapsed",
                placeholder="Optional: Share what's on your mind..."
            )
            
            # Save button and prompt logic
            if 'teen_saved' not in st.session_state:
                st.session_state.teen_saved = False
            
            if not st.session_state.teen_saved:
                if st.button("💾 Save Journal Entry", 
                            key="teen_save", 
                            use_container_width=True,
                            type="primary"):
                    st.session_state.teen_saved = True
                    prompts = [
                        "What small step could you take today to ease one of these feelings?",
                        "When have you felt this way before, and what helped?",
                        "Who in your life could you reach out to about this?",
                        "What would you tell a friend who felt this way?",
                    ]
                    st.session_state.teen_prompt = random.choice(prompts)
                    st.success("Journal saved!")
                    st.rerun()
            else:
                # Reflection prompt card
                st.markdown(f"""
                <div style="background: hsl(210, 85%, 92%); 
                            border: 1px solid hsl(210, 75%, 65%); 
                            border-radius: 0.5rem; 
                            padding: 1rem; 
                            margin: 1rem 0;">
                    <div style="display: flex; gap: 0.75rem; align-items: start;">
                        <span style="font-size: 1.5rem;">💭</span>
                        <div>
                            <p style="font-weight: 600; margin-bottom: 0.5rem; color: hsl(220, 15%, 20%);">
                                Reflection Prompt:
                            </p>
                            <p style="color: hsl(220, 15%, 20%);">{st.session_state.teen_prompt}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Done", 
                            key="teen_done", 
                            use_container_width=True):
                    st.session_state.teen_saved = False
                    if on_close_callback:
                        on_close_callback()
                    st.session_state.intervention_active = False
                    st.rerun()
    
    def _adult_intervention(self, on_close_callback=None):
        """Adult intervention: Reading, Meditation, Body Scan & Journal - exact port from AdultIntervention.tsx"""
        
        # Header card
        st.markdown("""
        <div style="background: hsl(0, 0%, 100%); 
                    border-left: 4px solid hsl(270, 55%, 65%); 
                    border-radius: 0.75rem; 
                    padding: 1.5rem; 
                    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
            <h2 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; color: hsl(220, 15%, 20%);">
                Take a moment for yourself
            </h2>
            <p style="color: hsl(220, 15%, 45%);">Professional stress relief techniques</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 4 tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📖 Reading", "🧘 Meditation", "🫁 Body Scan", "📝 Journal"])
        
        with tab1:
            st.markdown("""
            <div style="background: hsl(220, 20%, 92%); padding: 1.5rem; border-radius: 0.5rem;">
                <p style="font-size: 1.125rem; line-height: 1.75; color: hsl(220, 15%, 20%);">
                    Mindfulness content: When stress rises, remember that you have the power to pause. 
                    Take three deep breaths. Notice the sensation of air entering and leaving your body. 
                    This moment is yours.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("""
            <div style="background: hsl(220, 20%, 92%); padding: 1.5rem; border-radius: 0.5rem; text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🧘</div>
                <h3 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 0.5rem; color: hsl(220, 15%, 20%);">
                    5-7 Minute Guided Meditation
                </h3>
                <p style="color: hsl(220, 15%, 45%); margin-bottom: 1rem;">
                    Find a comfortable position and focus on your breath
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("▶️ Start Meditation", key="adult_meditation", use_container_width=True):
                st.success("Meditation started! Focus on your breathing.")
        
        with tab3:
            # Body scan with exact styling
            st.markdown("### 15-Minute Body Scan Meditation")
            st.markdown("""
            <p style="color: hsl(220, 15%, 45%); margin-bottom: 1.5rem;">
                Systematically relax your entire body, releasing tension from head to toe
            </p>
            """, unsafe_allow_html=True)
            
            # Initialize state
            if 'body_scan_active' not in st.session_state:
                st.session_state.body_scan_active = False
            if 'body_scan_progress' not in st.session_state:
                st.session_state.body_scan_progress = 0
            if 'current_body_part' not in st.session_state:
                st.session_state.current_body_part = 0
            
            body_parts = ["feet", "calves", "thighs", "hips", "abdomen", "chest", 
                         "shoulders", "arms", "hands", "neck", "face", "head"]
            
            # Start/Pause button
            button_text = "⏸ Pause Body Scan" if st.session_state.body_scan_active else (
                "Resume Body Scan" if st.session_state.body_scan_progress > 0 else "▶️ Start Body Scan"
            )
            
            if st.button(button_text, 
                        key="adult_body_scan_toggle", 
                        use_container_width=True,
                        type="primary"):
                st.session_state.body_scan_active = not st.session_state.body_scan_active
                if st.session_state.body_scan_active and st.session_state.body_scan_progress == 0:
                    st.session_state.body_scan_progress = 1
                st.rerun()
            
            # Progress display
            if st.session_state.body_scan_progress > 0:
                progress = min(st.session_state.body_scan_progress, 100)
                st.progress(progress / 100)
                
                current_idx = int((progress / 100) * len(body_parts))
                if current_idx >= len(body_parts):
                    current_idx = len(body_parts) - 1
                
                time_remaining_min = int((15 * (100 - progress)) / 100)
                time_remaining_sec = int(((15 * 60 * (100 - progress)) / 100) % 60)
                
                st.markdown(f"""
                <div style="background: hsl(0, 0%, 100%); 
                            padding: 1.5rem; 
                            border-radius: 0.5rem; 
                            text-align: center; 
                            margin: 1rem 0;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🧘</div>
                    <p style="font-size: 1.125rem; font-weight: 600; color: hsl(220, 15%, 20%);">
                        Focus on your <span style="color: hsl(270, 55%, 65%);">{body_parts[current_idx]}</span>
                    </p>
                    <p style="color: hsl(220, 15%, 45%); margin-top: 0.5rem; font-size: 0.875rem;">
                        {time_remaining_min}:{time_remaining_sec:02d} remaining
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Pulsing circle animation
                st.markdown("""
                <div style="display: flex; justify-content: center; margin: 1.5rem 0;">
                    <div style="width: 6rem; height: 6rem; border-radius: 50%; 
                                background: hsla(220, 95%, 68%, 0.2);
                                display: flex; align-items: center; justify-content: center;
                                animation: pulse 2s ease-in-out infinite;">
                        <div style="width: 4rem; height: 4rem; border-radius: 50%; 
                                    background: hsla(220, 95%, 68%, 0.4);"></div>
                    </div>
                </div>
                <style>
                @keyframes pulse {
                    0%, 100% { transform: scale(1); opacity: 1; }
                    50% { transform: scale(1.1); opacity: 0.7; }
                }
                </style>
                """, unsafe_allow_html=True)
                
                # Completion
                if progress >= 100:
                    st.success("✅ Body scan complete! How do you feel?")
                    if st.button("✅ Complete Session", 
                                key="adult_complete_scan", 
                                use_container_width=True):
                        st.session_state.body_scan_active = False
                        st.session_state.body_scan_progress = 0
                        st.session_state.current_body_part = 0
                        if on_close_callback:
                            on_close_callback()
                        st.session_state.intervention_active = False
                        st.rerun()
                elif st.session_state.body_scan_active:
                    # Auto-increment progress
                    time.sleep(0.1)
                    st.session_state.body_scan_progress = min(
                        st.session_state.body_scan_progress + (100 / (15 * 10)), 
                        100
                    )
                    st.rerun()
        
        with tab4:
            # Stressors
            st.markdown("#### Current stressors")
            stressors = ["Career", "Health", "Finances", "Relationships", "Future", "World Events"]
            
            # Badge-style multiselect display
            cols = st.columns(3)
            if 'adult_stressors' not in st.session_state:
                st.session_state.adult_stressors = []
            
            for idx, stressor in enumerate(stressors):
                with cols[idx % 3]:
                    is_selected = stressor in st.session_state.adult_stressors
                    if st.button(stressor, 
                                key=f"stressor_{stressor}",
                                use_container_width=True,
                                type="primary" if is_selected else "secondary"):
                        if stressor in st.session_state.adult_stressors:
                            st.session_state.adult_stressors.remove(stressor)
                        else:
                            st.session_state.adult_stressors.append(stressor)
                        st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Reflection
            st.markdown("#### Reflection")
            journal_text = st.text_area(
                "What's on your mind? What are you grateful for today?",
                height=120,
                key="adult_journal",
                label_visibility="collapsed",
                placeholder="What's on your mind? What are you grateful for today?"
            )
            
            if st.button("💾 Save Entry", 
                        key="adult_save", 
                        use_container_width=True,
                        type="primary"):
                st.success("✅ Journal entry saved!")
                if on_close_callback:
                    on_close_callback()


__all__ = ['InterventionManager']
