"""
Backup and restore UI - SAFE VERSION (No infinite loops)
"""
import streamlit as st
from pathlib import Path
from datetime import datetime
import time

try:
    from core.backup.backup_manager import (
        create_backup,
        restore_backup,
        list_backups,
        delete_backup,
        auto_backup
    )
    BACKUP_AVAILABLE = True
except ImportError as e:
    BACKUP_AVAILABLE = False
    BACKUP_ERROR = str(e)


def render_backup_page():
    """Render backup management page"""
    
    st.title("💾 Backup & Restore")
    st.write("Manage database backups for data protection and recovery")
    
    if not BACKUP_AVAILABLE:
        st.error("⚠️ Backup module not available!")
        st.code(BACKUP_ERROR)
        st.info("Please ensure the backup module is properly installed")
        return
    
    st.markdown("---")
    
    # Create Backup Section
    st.header("📦 Create New Backup")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        description = st.text_input(
            "Backup Description (optional)",
            placeholder="e.g., Before major update, Weekly backup, etc.",
            key="backup_description"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        
        # CRITICAL: Use on_click callback instead of if statement
        def create_backup_callback():
            """Callback to create backup - prevents infinite loops"""
            if 'creating_backup' not in st.session_state:
                st.session_state.creating_backup = False
            
            if not st.session_state.creating_backup:
                st.session_state.creating_backup = True
                try:
                    desc = st.session_state.get('backup_description', '')
                    backup_path = create_backup(desc)
                    st.session_state.last_backup_path = str(backup_path)
                    st.session_state.backup_success = True
                except Exception as e:
                    st.session_state.backup_error = str(e)
                    st.session_state.backup_success = False
                finally:
                    st.session_state.creating_backup = False
        
        st.button(
            "🔄 Create Backup", 
            use_container_width=True, 
            type="primary", 
            key="create_backup_btn",
            on_click=create_backup_callback
        )
    
    # Show results AFTER button (not in callback)
    if st.session_state.get('backup_success', False):
        st.success(f"✅ Backup created successfully!")
        st.info(f"📁 Location: `{st.session_state.get('last_backup_path', 'Unknown')}`")
        # Clear the flag so it doesn't show again
        if st.button("✅ Acknowledge", key="ack_backup"):
            st.session_state.backup_success = False
            st.rerun()
    
    if st.session_state.get('backup_error', None):
        st.error(f"❌ Backup failed: {st.session_state.backup_error}")
        if st.button("✅ Acknowledge", key="ack_error"):
            st.session_state.backup_error = None
            st.rerun()
    
    st.markdown("---")
    
    # List Backups Section
    st.header("📋 Available Backups")
    
    try:
        backups = list_backups()
        
        if not backups:
            st.info("📦 No backups found. Create your first backup above!")
        else:
            st.write(f"**Total backups:** {len(backups)}")
            
            # Manual refresh button
            if st.button("🔄 Refresh List", key="refresh_list"):
                st.rerun()
            
            st.markdown("---")
            
            # Display each backup
            for idx, backup in enumerate(backups, 1):
                backup_id = backup['name']
                
                with st.expander(
                    f"🗂️ Backup #{idx} - {backup['timestamp']} ({backup['backup_size_mb']} MB)",
                    expanded=False
                ):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Created:** {backup['created_at'][:19]}")
                        st.write(f"**Size:** {backup['backup_size_mb']} MB")
                        st.write(f"**Description:** {backup.get('description', 'No description')}")
                    
                    with col2:
                        st.write(f"**Location:**")
                        st.code(backup['path'], language=None)
                    
                    st.markdown("---")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    # Restore button
                    with col1:
                        restore_confirm_key = f'confirm_restore_{backup_id}'
                        
                        if not st.session_state.get(restore_confirm_key, False):
                            if st.button("♻️ Restore", key=f"restore_{backup_id}", use_container_width=True, type="primary"):
                                st.session_state[restore_confirm_key] = True
                                st.rerun()
                        else:
                            st.warning("⚠️ Replace database?")
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("✅ Yes", key=f"yes_restore_{backup_id}", use_container_width=True):
                                    try:
                                        with st.spinner("Restoring..."):
                                            restore_backup(Path(backup['path']))
                                        st.success("✅ Restored! Restart app.")
                                        st.session_state[restore_confirm_key] = False
                                    except Exception as e:
                                        st.error(f"❌ Failed: {e}")
                            
                            with col_b:
                                if st.button("❌ No", key=f"no_restore_{backup_id}", use_container_width=True):
                                    st.session_state[restore_confirm_key] = False
                                    st.rerun()
                    
                    # Delete button
                    with col2:
                        delete_confirm_key = f'confirm_delete_{backup_id}'
                        
                        if not st.session_state.get(delete_confirm_key, False):
                            if st.button("🗑️ Delete", key=f"delete_{backup_id}", use_container_width=True):
                                st.session_state[delete_confirm_key] = True
                                st.rerun()
                        else:
                            st.warning("⚠️ Delete?")
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("✅ Yes", key=f"yes_delete_{backup_id}", use_container_width=True):
                                    try:
                                        delete_backup(Path(backup['path']))
                                        st.success("✅ Deleted!")
                                        st.session_state[delete_confirm_key] = False
                                        time.sleep(0.3)
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Failed: {e}")
                            
                            with col_b:
                                if st.button("❌ No", key=f"no_delete_{backup_id}", use_container_width=True):
                                    st.session_state[delete_confirm_key] = False
                                    st.rerun()
                    
                    # Download button
                    with col3:
                        st.button(
                            "⬇️ Download",
                            key=f"download_{backup_id}",
                            use_container_width=True,
                            disabled=True,
                            help="Coming soon"
                        )
    
    except Exception as e:
        st.error(f"❌ Error loading backups: {e}")
    
    st.markdown("---")
    
    # Auto-Backup Section
    st.header("⚙️ Automatic Backup")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Auto-Backup Features:**
        - Creates 1 new backup
        - Keeps last 10 backups
        - Deletes oldest automatically
        """)
    
    with col2:
        st.write("")
        st.write("")
        
        def auto_backup_callback():
            """Callback for auto-backup"""
            if 'running_auto_backup' not in st.session_state:
                st.session_state.running_auto_backup = False
            
            if not st.session_state.running_auto_backup:
                st.session_state.running_auto_backup = True
                try:
                    backup_path = auto_backup(max_backups=10)
                    st.session_state.auto_backup_success = True
                    st.session_state.auto_backup_path = str(backup_path)
                except Exception as e:
                    st.session_state.auto_backup_error = str(e)
                    st.session_state.auto_backup_success = False
                finally:
                    st.session_state.running_auto_backup = False
        
        st.button(
            "🔄 Run Auto-Backup", 
            use_container_width=True, 
            key="auto_backup_btn",
            on_click=auto_backup_callback
        )
    
    # Show auto-backup results
    if st.session_state.get('auto_backup_success', False):
        st.success(f"✅ Auto-backup completed!")
        if st.button("✅ Acknowledge", key="ack_auto"):
            st.session_state.auto_backup_success = False
            st.rerun()
    
    if st.session_state.get('auto_backup_error', None):
        st.error(f"❌ Auto-backup failed: {st.session_state.auto_backup_error}")
        if st.button("✅ Acknowledge", key="ack_auto_error"):
            st.session_state.auto_backup_error = None
            st.rerun()