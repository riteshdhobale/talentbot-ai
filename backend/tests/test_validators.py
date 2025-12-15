"""Tests for validators module."""

import pytest
from core.validators import (
    validate_email,
    validate_phone,
    validate_years_experience,
    validate_tech_stack,
    validate_full_name,
    validate_desired_position,
    validate_current_location,
    normalize_tech_stack
)


class TestEmailValidation:
    """Tests for email validation."""
    
    def test_valid_email(self):
        """Test valid email addresses."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "user123@test-domain.com"
        ]
        for email in valid_emails:
            is_valid, error = validate_email(email)
            assert is_valid, f"Email {email} should be valid: {error}"
    
    def test_invalid_email(self):
        """Test invalid email addresses."""
        invalid_emails = [
            "notanemail",
            "@example.com",
            "user@",
            "user@domain",
            "",
            None
        ]
        for email in invalid_emails:
            is_valid, error = validate_email(email)
            assert not is_valid, f"Email {email} should be invalid"


class TestPhoneValidation:
    """Tests for phone validation."""
    
    def test_valid_phone(self):
        """Test valid phone numbers."""
        valid_phones = [
            "1234567890",
            "+1234567890",
            "(123) 456-7890",
            "123-456-7890",
            "+1 234 567 8900"
        ]
        for phone in valid_phones:
            is_valid, error = validate_phone(phone)
            assert is_valid, f"Phone {phone} should be valid: {error}"
    
    def test_invalid_phone(self):
        """Test invalid phone numbers."""
        invalid_phones = [
            "123",
            "abc1234567",
            "",
            None,
            "12345678901234567890"  # Too long
        ]
        for phone in invalid_phones:
            is_valid, error = validate_phone(phone)
            assert not is_valid, f"Phone {phone} should be invalid"


class TestYearsExperienceValidation:
    """Tests for years of experience validation."""
    
    def test_valid_experience(self):
        """Test valid years of experience."""
        valid_values = [
            ("0", 0.0),
            ("5", 5.0),
            ("10.5", 10.5),
            (5, 5.0),
            (10.5, 10.5)
        ]
        for value, expected in valid_values:
            is_valid, error, normalized = validate_years_experience(value)
            assert is_valid, f"Experience {value} should be valid: {error}"
            assert normalized == expected
    
    def test_invalid_experience(self):
        """Test invalid years of experience."""
        invalid_values = [
            "-5",
            "abc",
            None,
            "100"  # Too high
        ]
        for value in invalid_values:
            is_valid, error, normalized = validate_years_experience(value)
            assert not is_valid, f"Experience {value} should be invalid"


class TestTechStackValidation:
    """Tests for tech stack validation."""
    
    def test_valid_tech_stack(self):
        """Test valid tech stacks."""
        valid_stacks = [
            "Python, Django, PostgreSQL",
            "JavaScript React Node.js",
            "Java, Spring, MySQL, Docker"
        ]
        for stack in valid_stacks:
            is_valid, error, normalized = validate_tech_stack(stack)
            assert is_valid, f"Tech stack '{stack}' should be valid: {error}"
            assert len(normalized) > 0
    
    def test_invalid_tech_stack(self):
        """Test invalid tech stacks."""
        invalid_stacks = [
            "",
            None,
            "   "
        ]
        for stack in invalid_stacks:
            is_valid, error, normalized = validate_tech_stack(stack)
            assert not is_valid, f"Tech stack '{stack}' should be invalid"
    
    def test_normalize_tech_stack(self):
        """Test tech stack normalization."""
        test_cases = [
            ("Python, Django, PostgreSQL", ["Python", "Django", "PostgreSQL"]),
            ("JavaScript  React   Node.js", ["JavaScript", "React", "Node.js"]),
            ("Java\nSpring\nMySQL", ["Java", "Spring", "MySQL"])
        ]
        for input_stack, expected in test_cases:
            normalized = normalize_tech_stack(input_stack)
            assert normalized == expected, f"Expected {expected}, got {normalized}"


class TestFullNameValidation:
    """Tests for full name validation."""
    
    def test_valid_name(self):
        """Test valid full names."""
        valid_names = [
            "John Doe",
            "Mary Jane Watson",
            "Jean-Pierre O'Brien",
            "José García"
        ]
        for name in valid_names:
            is_valid, error = validate_full_name(name)
            assert is_valid, f"Name '{name}' should be valid: {error}"
    
    def test_invalid_name(self):
        """Test invalid full names."""
        invalid_names = [
            "",
            "A",  # Too short
            None,
            "John123",  # Contains numbers
            "A" * 101  # Too long
        ]
        for name in invalid_names:
            is_valid, error = validate_full_name(name)
            assert not is_valid, f"Name '{name}' should be invalid"


class TestDesiredPositionValidation:
    """Tests for desired position validation."""
    
    def test_valid_position(self):
        """Test valid positions."""
        valid_positions = [
            "Software Engineer",
            "Senior Developer",
            "Full Stack Developer, Backend Engineer"
        ]
        for position in valid_positions:
            is_valid, error = validate_desired_position(position)
            assert is_valid, f"Position '{position}' should be valid: {error}"
    
    def test_invalid_position(self):
        """Test invalid positions."""
        invalid_positions = [
            "",
            "A",  # Too short
            None
        ]
        for position in invalid_positions:
            is_valid, error = validate_desired_position(position)
            assert not is_valid, f"Position '{position}' should be invalid"


class TestCurrentLocationValidation:
    """Tests for current location validation."""
    
    def test_valid_location(self):
        """Test valid locations."""
        valid_locations = [
            "New York, NY",
            "San Francisco",
            "London, UK"
        ]
        for location in valid_locations:
            is_valid, error = validate_current_location(location)
            assert is_valid, f"Location '{location}' should be valid: {error}"
    
    def test_invalid_location(self):
        """Test invalid locations."""
        invalid_locations = [
            "",
            "A",  # Too short
            None
        ]
        for location in invalid_locations:
            is_valid, error = validate_current_location(location)
            assert not is_valid, f"Location '{location}' should be invalid"

