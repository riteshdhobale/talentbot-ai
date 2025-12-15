"""Sidebar widgets and status components for TalentScout."""

import streamlit as st
from core.state import (
    get_all_fields,
    get_missing_fields,
    all_fields_collected,
    get_conversation_stage,
    reset_session,
    get_session_id
)
from core.config import config
from core.storage import delete_session, get_session_count


def render_sidebar() -> None:
    """Render the sidebar with application status and controls."""
    with st.sidebar:
        st.header("📊 Application Status")
        
        # Display collected fields
        collected_fields = get_all_fields()
        missing_fields = get_missing_fields()
        
        # Progress indicator
        total_fields = 7  # Total required fields
        collected_count = total_fields - len(missing_fields)
        progress = collected_count / total_fields
        
        st.progress(progress)
        st.caption(f"Progress: {collected_count}/{total_fields} fields collected")
        
        # Field status
        st.subheader("Collected Information")
        
        field_labels = {
            "full_name": "Full Name",
            "email": "Email",
            "phone": "Phone",
            "years_experience": "Years of Experience",
            "desired_position": "Desired Position",
            "current_location": "Current Location",
            "tech_stack": "Tech Stack"
        }
        
        for field_key, field_label in field_labels.items():
            value = collected_fields.get(field_key)
            if value:
                if field_key == "tech_stack" and isinstance(value, list):
                    display_value = ", ".join(value)
                else:
                    display_value = str(value)
                st.success(f"✓ {field_label}: {display_value}")
            else:
                st.info(f"○ {field_label}: Not collected")
        
        # Conversation stage
        st.subheader("Status")
        stage = get_conversation_stage()
        stage_labels = {
            "greeting": "👋 Greeting",
            "collection": "📝 Collecting Information",
            "questions": "❓ Technical Questions",
            "exit": "👋 Completed"
        }
        st.info(f"Stage: {stage_labels.get(stage, stage)}")
        
        # Privacy banner
        st.markdown("---")
        st.info("🔒 **Privacy Notice**\n\nLocal, simulated storage. Your data is stored locally and can be deleted at any time.")
        
        # Delete session button
        if st.button("🗑️ Delete Session", type="secondary"):
            session_id = get_session_id()
            if delete_session(session_id):
                reset_session()
                st.success("Session deleted successfully!")
                st.rerun()
        
        # Optional features toggles
        st.markdown("---")
        st.subheader("⚙️ Settings")
        
        if config.ENABLE_SENTIMENT:
            st.checkbox("Enable Sentiment Analysis", value=False, key="sentiment_enabled")
        
        if config.ENABLE_MULTILINGUAL:
            st.checkbox("Enable Multilingual Support", value=False, key="multilingual_enabled")
        
        # Storage status
        if config.ENABLE_STORAGE:
            session_count = get_session_count()
            st.caption(f"📦 {session_count} session(s) stored")
        
        # Footer
        st.markdown("---")
        st.caption("TalentScout v1.0")


def render_privacy_banner() -> None:
    """Render privacy banner at the top of the sidebar."""
    st.sidebar.info(
        "🔒 **Privacy Notice**\n\n"
        "This application uses local, simulated storage. "
        "Your data is stored locally and can be deleted at any time. "
        "We follow GDPR-aware data handling practices."
    )

