"""
Test input validation functions
"""
import pytest
from core.utils.validators import (
    validate_year,
    validate_claim_text,
    validate_source,
    sanitize_filename,
    ValidationError
)


class TestYearValidation:
    """Test year validation"""
    
    def test_valid_year(self):
        """Test valid year input"""
        assert validate_year(2024) == 2024
        assert validate_year("2020") == 2020
    
    def test_invalid_year_too_old(self):
        """Test year before 1900"""
        with pytest.raises(ValidationError):
            validate_year(1899)
    
    def test_invalid_year_future(self):
        """Test year too far in future"""
        with pytest.raises(ValidationError):
            validate_year(2101)
    
    def test_invalid_year_format(self):
        """Test invalid year format"""
        with pytest.raises(ValidationError):
            validate_year("invalid")


class TestClaimValidation:
    """Test claim text validation"""
    
    def test_valid_claim(self):
        """Test valid claim"""
        claim = "This is a valid test claim about misinformation"
        result = validate_claim_text(claim)
        assert result == claim
    
    def test_claim_too_short(self):
        """Test claim that's too short"""
        with pytest.raises(ValidationError):
            validate_claim_text("Too short")
    
    def test_claim_too_long(self):
        """Test claim that's too long"""
        long_claim = "x" * 6000
        with pytest.raises(ValidationError):
            validate_claim_text(long_claim)
    
    def test_empty_claim(self):
        """Test empty claim"""
        with pytest.raises(ValidationError):
            validate_claim_text("")
    
    def test_whitespace_claim(self):
        """Test whitespace-only claim"""
        with pytest.raises(ValidationError):
            validate_claim_text("   ")


class TestSourceValidation:
    """Test source validation"""
    
    def test_valid_source(self):
        """Test valid source"""
        assert validate_source("twitter") == "twitter"
        assert validate_source("Facebook") == "facebook"
    
    def test_empty_source(self):
        """Test empty source defaults to 'unknown'"""
        assert validate_source("") == "unknown"
        assert validate_source(None) == "unknown"
    
    def test_special_characters_removed(self):
        """Test special characters are removed"""
        result = validate_source("twitter@#$%")
        assert "@" not in result
        assert "#" not in result


class TestFilenameValidation:
    """Test filename sanitization"""
    
    def test_safe_filename(self):
        """Test already safe filename"""
        assert sanitize_filename("test_image.jpg") == "test_image.jpg"
    
    def test_path_traversal_removed(self):
        """Test path traversal attempt is blocked"""
        result = sanitize_filename("../../etc/passwd")
        assert ".." not in result
        assert "/" not in result
    
    def test_special_characters_removed(self):
        """Test special characters removed"""
        result = sanitize_filename("test@#$image.jpg")
        assert "@" not in result
        assert "#" not in result