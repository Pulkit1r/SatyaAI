"""
Input validation utilities
"""
import re
from datetime import datetime
from pathlib import Path
from core.config import (
    ALLOWED_IMAGE_EXTENSIONS, 
    ALLOWED_VIDEO_EXTENSIONS,
    MAX_UPLOAD_SIZE_MB
)


class ValidationError(Exception):
    """Custom validation error"""
    pass


def validate_year(year):
    """
    Validate year input.
    
    Args:
        year: Year value (int or str)
        
    Returns:
        int: Validated year
        
    Raises:
        ValidationError: If year is invalid
    """
    try:
        y = int(year)
        current_year = datetime.now().year
        
        if 1900 <= y <= current_year + 1:
            return y
        else:
            raise ValidationError(f"Year must be between 1900 and {current_year + 1}")
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid year format: {year}")


def validate_claim_text(text):
    """
    Validate claim text.
    
    Args:
        text (str): Claim text
        
    Returns:
        str: Cleaned claim text
        
    Raises:
        ValidationError: If text is invalid
    """
    if not text or not isinstance(text, str):
        raise ValidationError("Claim text cannot be empty")
    
    text = text.strip()
    
    if len(text) < 10:
        raise ValidationError("Claim too short (minimum 10 characters)")
    
    if len(text) > 5000:
        raise ValidationError("Claim too long (maximum 5000 characters)")
    
    return text


def validate_source(source):
    """
    Validate source/platform name.
    
    Args:
        source (str): Source name
        
    Returns:
        str: Cleaned source name
    """
    if not source:
        return "unknown"
    
    # Remove special characters, keep alphanumeric and basic punctuation
    source = re.sub(r'[^\w\s.-]', '', str(source))
    return source.strip().lower()[:100]


def validate_file_upload(file_path, file_type='image'):
    """
    Validate uploaded file.
    
    Args:
        file_path (str): Path to uploaded file
        file_type (str): 'image' or 'video'
        
    Returns:
        Path: Validated file path
        
    Raises:
        ValidationError: If file is invalid
    """
    path = Path(file_path)
    
    # Check if file exists
    if not path.exists():
        raise ValidationError(f"File not found: {file_path}")
    
    # Check file size
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > MAX_UPLOAD_SIZE_MB:
        raise ValidationError(
            f"File too large: {size_mb:.1f}MB (max: {MAX_UPLOAD_SIZE_MB}MB)"
        )
    
    # Check file extension
    if file_type == 'image':
        allowed = ALLOWED_IMAGE_EXTENSIONS
    elif file_type == 'video':
        allowed = ALLOWED_VIDEO_EXTENSIONS
    else:
        raise ValidationError(f"Unknown file type: {file_type}")
    
    if path.suffix.lower() not in allowed:
        raise ValidationError(
            f"Invalid file extension: {path.suffix}. Allowed: {allowed}"
        )
    
    return path


def sanitize_filename(filename):
    """
    Sanitize filename to prevent path traversal attacks.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Safe filename
    """
    # Get just the filename, remove any path components
    filename = Path(filename).name
    
    # Remove any special characters except alphanumeric, dots, dashes, underscores
    filename = re.sub(r'[^\w\s.-]', '', filename)
    
    # Remove multiple dots (potential security issue)
    filename = re.sub(r'\.+', '.', filename)
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1)
        filename = name[:250] + '.' + ext
    
    return filename or "unnamed_file"


def validate_metadata(metadata):
    """
    Validate and clean metadata dictionary.
    
    Args:
        metadata (dict): Metadata to validate
        
    Returns:
        dict: Cleaned metadata
    """
    clean_metadata = {}
    
    # Validate year if present
    if 'year' in metadata and metadata['year']:
        try:
            clean_metadata['year'] = validate_year(metadata['year'])
        except ValidationError:
            pass  # Skip invalid year
    
    # Validate source if present
    if 'source' in metadata and metadata['source']:
        clean_metadata['source'] = validate_source(metadata['source'])
    
    # Copy other safe fields
    safe_fields = ['type', 'narrative_id', 'reinforced', 'created_at', 
                   'path', 'video_source']
    
    for field in safe_fields:
        if field in metadata:
            clean_metadata[field] = metadata[field]
    
    return clean_metadata   