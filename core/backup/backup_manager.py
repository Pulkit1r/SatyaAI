"""
Database backup and restore functionality
"""
import shutil
from datetime import datetime
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

BACKUP_DIR = Path("backups")
QDRANT_DIR = Path("qdrant_data")


def create_backup(description: str = "") -> Path:
    """
    Create a backup of the Qdrant database.
    
    Args:
        description: Optional description for the backup
        
    Returns:
        Path: Path to the backup directory
    """
    # Create backup directory if it doesn't exist
    BACKUP_DIR.mkdir(exist_ok=True)
    
    # Generate timestamped backup name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"qdrant_backup_{timestamp}"
    backup_path = BACKUP_DIR / backup_name
    
    try:
        # Check if Qdrant directory exists
        if not QDRANT_DIR.exists():
            raise FileNotFoundError(f"Qdrant data directory not found: {QDRANT_DIR}")
        
        # Copy Qdrant data directory with ignore for lock files
        def ignore_lock_files(dir, files):
            return [f for f in files if f.endswith('.lock')]
        
        shutil.copytree(QDRANT_DIR, backup_path, ignore=ignore_lock_files)
        
        # Create metadata file
        metadata = {
            "timestamp": timestamp,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "backup_size_mb": get_dir_size(backup_path)
        }
        
        with open(backup_path / "backup_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Backup created successfully: {backup_path}")
        return backup_path
        
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        # Cleanup failed backup
        if backup_path.exists():
            shutil.rmtree(backup_path)
        raise


def restore_backup(backup_path: Path) -> bool:
    """
    Restore database from backup.
    
    Args:
        backup_path: Path to backup directory
        
    Returns:
        bool: True if successful
    """
    if not backup_path.exists():
        raise FileNotFoundError(f"Backup not found: {backup_path}")
    
    safety_backup = None
    
    try:
        # Create a safety backup of current data if it exists
        if QDRANT_DIR.exists():
            safety_backup = create_backup("Pre-restore safety backup")
            logger.info(f"Safety backup created: {safety_backup}")
        
        # Remove current Qdrant data
        if QDRANT_DIR.exists():
            shutil.rmtree(QDRANT_DIR)
        
        # Restore from backup (ignore lock files)
        def ignore_metadata_and_locks(dir, files):
            return [f for f in files if f == 'backup_metadata.json' or f.endswith('.lock')]
        
        shutil.copytree(backup_path, QDRANT_DIR, ignore=ignore_metadata_and_locks)
        
        logger.info(f"Database restored successfully from: {backup_path}")
        return True
        
    except Exception as e:
        logger.error(f"Restore failed: {e}")
        # Try to restore safety backup
        if safety_backup and safety_backup.exists():
            try:
                if QDRANT_DIR.exists():
                    shutil.rmtree(QDRANT_DIR)
                shutil.copytree(safety_backup, QDRANT_DIR)
                logger.info("Rolled back to safety backup")
            except Exception as rollback_error:
                logger.critical(f"Rollback failed: {rollback_error}")
        raise


def list_backups() -> list:
    """
    List all available backups.
    
    Returns:
        list: List of backup info dictionaries
    """
    if not BACKUP_DIR.exists():
        return []
    
    backups = []
    
    # Only list directories that start with 'qdrant_backup_'
    for backup_dir in sorted(BACKUP_DIR.iterdir(), reverse=True):
        if backup_dir.is_dir() and backup_dir.name.startswith('qdrant_backup_'):
            metadata_file = backup_dir / "backup_metadata.json"
            
            if metadata_file.exists():
                try:
                    with open(metadata_file, "r") as f:
                        metadata = json.load(f)
                except Exception as e:
                    logger.warning(f"Failed to read metadata for {backup_dir.name}: {e}")
                    metadata = create_default_metadata(backup_dir)
            else:
                metadata = create_default_metadata(backup_dir)
            
            metadata["path"] = str(backup_dir)
            metadata["name"] = backup_dir.name
            backups.append(metadata)
    
    return backups


def create_default_metadata(backup_dir: Path) -> dict:
    """Create default metadata for backups without metadata file"""
    try:
        created_at = datetime.fromtimestamp(backup_dir.stat().st_ctime).isoformat()
    except:
        created_at = datetime.now().isoformat()
    
    return {
        "timestamp": backup_dir.name.replace("qdrant_backup_", ""),
        "description": "No description",
        "created_at": created_at,
        "backup_size_mb": get_dir_size(backup_dir)
    }


def delete_backup(backup_path: Path) -> bool:
    """
    Delete a backup.
    
    Args:
        backup_path: Path to backup directory
        
    Returns:
        bool: True if successful
    """
    try:
        if backup_path.exists():
            shutil.rmtree(backup_path)
            logger.info(f"Backup deleted: {backup_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to delete backup: {e}")
        raise


def get_dir_size(path: Path) -> float:
    """
    Calculate directory size in MB.
    
    Args:
        path: Directory path
        
    Returns:
        float: Size in MB
    """
    total_size = 0
    try:
        for file in path.rglob('*'):
            if file.is_file():
                total_size += file.stat().st_size
    except Exception as e:
        logger.warning(f"Error calculating directory size: {e}")
    return round(total_size / (1024 * 1024), 2)


def auto_backup(max_backups: int = 10) -> Path:
    """
    Create automatic backup and manage backup retention.
    
    Args:
        max_backups: Maximum number of backups to keep
        
    Returns:
        Path: Path to created backup
    """
    # Create backup
    backup_path = create_backup("Automatic backup")
    
    # Clean old backups (keep only max_backups)
    backups = list_backups()
    
    # If we have more than max_backups, delete the oldest ones
    if len(backups) > max_backups:
        # Sort by creation time (oldest first)
        backups_sorted = sorted(backups, key=lambda x: x['created_at'])
        
        # Calculate how many to delete
        num_to_delete = len(backups_sorted) - max_backups
        old_backups = backups_sorted[:num_to_delete]
        
        for backup in old_backups:
            try:
                delete_backup(Path(backup['path']))
                logger.info(f"Deleted old backup: {backup['name']}")
            except Exception as e:
                logger.warning(f"Failed to delete old backup: {e}")
    
    return backup_path


def cleanup_old_backups(max_backups: int = 10):
    """
    Clean up old backups, keeping only the most recent max_backups.
    
    Args:
        max_backups: Maximum number of backups to keep
    """
    backups = list_backups()
    
    if len(backups) > max_backups:
        # Sort by creation time (oldest first)
        backups_sorted = sorted(backups, key=lambda x: x['created_at'])
        
        # Calculate how many to delete
        num_to_delete = len(backups_sorted) - max_backups
        old_backups = backups_sorted[:num_to_delete]
        
        deleted_count = 0
        for backup in old_backups:
            try:
                delete_backup(Path(backup['path']))
                deleted_count += 1
                logger.info(f"Deleted old backup: {backup['name']}")
            except Exception as e:
                logger.warning(f"Failed to delete old backup: {e}")
        
        return deleted_count
    
    return 0