"""
Backup and restore UI - Enhanced version with better UX
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


def format_size(size_mb):
    """Format size in MB to human-readable format"""
    if size_mb < 1:
        return f"{size_mb * 1024:.1f} KB"
    elif size_mb < 1024:
        return f"{size_mb:.2f} MB"
    else:
        return f"{size_mb / 1024:.2f} GB"


def format_time_ago(timestamp_str):
    try:
        backup_time = datetime.fromisoformat(timestamp_str)
        now = datetime.now()
        diff = now - backup_time
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    except:
        return "Unknown"


def render_backup_page():
    """Render backup management page"""
    
    st.title("💾 Backup & Restore")
    st.write("Protect your data with automated backups and easy restore")
    
    if not BACKUP_AVAILABLE:
        st.error("⚠️ Backup module not available!")
        st.code(BACKUP_ERROR)
        st.info("Please ensure the backup module is properly installed")
        return
    
    # Quick stats bar
    try:
        backups = list_backups()
        total_size = sum(b.get('backup_size_mb', 0) for b in backups)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("📦 Total Backups", len(backups))
        col2.metric("💾 Total Size", format_size(total_size))
        
        if backups:
            latest = backups[0]
            col3.metric("🕐 Latest", format_time_ago(latest.get('created_at', '')))
    except:
        pass
    
    st.markdown("---")
    
    # Create Backup Section
    st.header("📦 Create New Backup")
    
    # Use form to enable Enter key submission
    with st.form(key="backup_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            description = st.text_input(
                "Backup Name/Description",
                placeholder="e.g., Before major update, Weekly backup, Production snapshot...",
                help="Give your backup a meaningful name so you can identify it later",
                key="backup_description_form"
            )
        
        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            submit_button = st.form_submit_button(
                "🔄 Create Backup",
                use_container_width=True,
                type="primary"
            )
    
    # Handle form submission
    if submit_button:

        backup_desc = description.strip() if description.strip() else f"Backup {datetime.now().strftime('%b %d, %Y %H:%M')}"
        
        try:
            with st.spinner(f"Creating backup '{backup_desc}'..."):
                backup_path = create_backup(backup_desc)
                time.sleep(0.3)  
            
            st.success(f"✅ Backup created successfully!")
            st.balloons()
            
            # Show backup details
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"📝 **Name:** {backup_desc}")
            with col2:
                st.info(f"📁 **Location:** `{Path(backup_path).name}`")
            
            # Auto-refresh to show new backup
            time.sleep(1)
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Backup failed: {e}")
            with st.expander("🔍 Show error details"):
                import traceback
                st.code(traceback.format_exc())
    
    st.caption("💡 **Tip:** Press Enter or click the button to create backup")
    
    st.markdown("---")
    
    # List Backups Section
    st.header("📋 Available Backups")
    
    try:
        backups = list_backups()
        
        if not backups:
            st.info("📦 No backups found. Create your first backup above!")
        else:
            # Action buttons row
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                if st.button("🔄 Refresh List", use_container_width=True):
                    st.rerun()
            
            with col2:
                if st.button("🧹 Delete All Backups", use_container_width=True, type="secondary"):
                    st.session_state.show_delete_all = True
            
            with col3:
                st.metric("Total", len(backups))
            
            # Delete all confirmation
            if st.session_state.get('show_delete_all', False):
                st.warning("⚠️ **Are you sure you want to delete ALL backups?** This cannot be undone!")
                col_yes, col_no = st.columns(2)
                
                with col_yes:
                    if st.button("✅ Yes, Delete All", type="primary", use_container_width=True):
                        deleted = 0
                        for backup in backups:
                            try:
                                delete_backup(Path(backup['path']))
                                deleted += 1
                            except:
                                pass
                        st.success(f"✅ Deleted {deleted} backup(s)")
                        st.session_state.show_delete_all = False
                        time.sleep(1)
                        st.rerun()
                
                with col_no:
                    if st.button("❌ Cancel", use_container_width=True):
                        st.session_state.show_delete_all = False
                        st.rerun()
            
            st.markdown("---")
            
            # Display each backup with enhanced UI
            for idx, backup in enumerate(backups, 1):
                backup_id = backup['name']
                description = backup.get('description', 'No description')
                size_mb = backup.get('backup_size_mb', 0)
                created_at = backup.get('created_at', '')
                timestamp = backup.get('timestamp', '')
                
                if description and description != "No description":
                    header_title = f"📦 {description}"
                else:
                    header_title = f"📦 Backup #{idx}"
                
                header_subtitle = f"{format_size(size_mb)} • {format_time_ago(created_at)}"
                
                with st.expander(
                    f"{header_title} • {header_subtitle}",
                    expanded=(idx == 1)  
                ):
                    # Backup details in a nice layout
                    detail_col1, detail_col2 = st.columns(2)
                    
                    with detail_col1:
                        st.markdown(f"""
                        **📝 Description:** {description}  
                        **📅 Created:** {created_at[:19] if created_at else 'Unknown'}  
                        **⏰ Time Ago:** {format_time_ago(created_at)}
                        """)
                    
                    with detail_col2:
                        st.markdown(f"""
                        **💾 Size:** {format_size(size_mb)}  
                        **🆔 ID:** `{timestamp}`  
                        **📁 Folder:** `{backup_id}`
                        """)
 
                    # Show full path without nested expander
                    st.markdown("**📂 Full Path:**")
                    st.code(backup['path'], language=None)
                    
                    st.markdown("---")
                    
                    # Action buttons
                    action_col1, action_col2, action_col3 = st.columns(3)
                    
                    # Restore button
                    with action_col1:
                        restore_confirm_key = f'confirm_restore_{backup_id}'
                        
                        if not st.session_state.get(restore_confirm_key, False):
                            if st.button("♻️ Restore", key=f"restore_{backup_id}", use_container_width=True, type="primary"):
                                st.session_state[restore_confirm_key] = True
                                st.rerun()
                        else:
                            st.warning("⚠️ Replace current database?")
                            col_a, col_b = st.columns(2)
                            
                            with col_a:
                                if st.button("✅ Yes", key=f"yes_restore_{backup_id}", use_container_width=True):
                                    try:
                                        with st.spinner("Restoring backup..."):
                                            restore_backup(Path(backup['path']))
                                        st.success("✅ Database restored!")
                                        st.info("🔄 Please restart the application for changes to take effect")
                                        st.session_state[restore_confirm_key] = False
                                    except Exception as e:
                                        st.error(f"❌ Restore failed: {e}")
                            
                            with col_b:
                                if st.button("❌ No", key=f"no_restore_{backup_id}", use_container_width=True):
                                    st.session_state[restore_confirm_key] = False
                                    st.rerun()
                    
                    # Delete button
                    with action_col2:
                        delete_confirm_key = f'confirm_delete_{backup_id}'
                        
                        if not st.session_state.get(delete_confirm_key, False):
                            if st.button("🗑️ Delete", key=f"delete_{backup_id}", use_container_width=True):
                                st.session_state[delete_confirm_key] = True
                                st.rerun()
                        else:
                            st.warning("⚠️ Confirm deletion?")
                            col_a, col_b = st.columns(2)
                            
                            with col_a:
                                if st.button("✅ Yes", key=f"yes_delete_{backup_id}", use_container_width=True):
                                    try:
                                        delete_backup(Path(backup['path']))
                                        st.success("✅ Backup deleted!")
                                        st.session_state[delete_confirm_key] = False
                                        time.sleep(0.5)
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Delete failed: {e}")
                            
                            with col_b:
                                if st.button("❌ No", key=f"no_delete_{backup_id}", use_container_width=True):
                                    st.session_state[delete_confirm_key] = False
                                    st.rerun()
                    
                    # Info button
                    with action_col3:
                        if st.button("ℹ️ Info", key=f"info_{backup_id}", use_container_width=True):
                            st.info(f"""
                            **Backup Information:**
                            - Created: {created_at[:19] if created_at else 'Unknown'}
                            - Size: {format_size(size_mb)}
                            - Can be restored to replace current database
                            - Safe to delete if no longer needed
                            """)
    
    except Exception as e:
        st.error(f"❌ Error loading backups: {e}")
        with st.expander("🔍 Show error details"):
            import traceback
            st.code(traceback.format_exc())
    
    st.markdown("---")
    
    # Auto-Backup Section
    st.header("⚙️ Automated Backup System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **🤖 Auto-Backup Features:**
        
        - ✅ Creates timestamped backup automatically
        - ✅ Keeps your 10 most recent backups
        - ✅ Deletes oldest backups when limit reached
        - ✅ Includes safety backup before restore
        - ✅ One-click operation
        
        **Recommended:** Run weekly for data protection
        """)
    
    with col2:
        st.write("")
        st.write("")
        
        if st.button("🔄 Run Auto-Backup Now", use_container_width=True, type="primary", key="auto_backup_btn"):
            try:
                with st.spinner("Running automated backup system..."):
                    backup_path = auto_backup(max_backups=10)
                    time.sleep(0.5)
                
                st.success(f"✅ Auto-backup completed successfully!")
                st.info(f"📁 Backup saved: `{Path(backup_path).name}`")
                st.caption("💡 Old backups have been automatically cleaned up")
                
                time.sleep(1.5)
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Auto-backup failed: {e}")
                with st.expander("🔍 Show error details"):
                    import traceback
                    st.code(traceback.format_exc())
    
    st.markdown("---")
    
    # Tips section
    with st.expander("💡 Backup Best Practices"):
        st.markdown("""
        ### 📚 When to Create Backups:
        
        1. **Before major updates** - Protect against update failures
        2. **Before bulk data operations** - Safe rollback point
        3. **Weekly schedule** - Regular data protection
        4. **Before system migration** - Ensure data portability
        5. **After important data additions** - Preserve new work
        
        ### 🔒 Storage Recommendations:
        
        - Keep at least 3-5 recent backups
        - Store critical backups on external drives
        - Consider cloud storage for off-site backup
        - Test restore process periodically
        - Document backup descriptions clearly
        
        ### ⚡ Quick Tips:
        
        - Use **descriptive names** for easy identification
        - **Auto-Backup** maintains optimal backup count
        - **Restore** creates safety backup automatically
        - Backup files are stored in `backups/` folder
        """)