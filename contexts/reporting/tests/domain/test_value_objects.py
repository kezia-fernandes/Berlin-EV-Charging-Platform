import pytest
from contexts.reporting.domain.value_objects.report_description import ReportDescription


def test_create_valid_description():
    """Test creating a valid report description"""
    description = ReportDescription("Station not charging my vehicle properly")
    assert "not charging" in description.value


def test_description_too_short_raises_error():
    """Test minimum length validation"""
    with pytest.raises(ValueError, match="too short"):
        ReportDescription("Bad")


def test_description_too_long_raises_error():
    """Test maximum length validation"""
    with pytest.raises(ValueError, match="too long"):
        ReportDescription("A" * 501)


def test_empty_description_raises_error():
    """Test empty description rejection"""
    with pytest.raises(ValueError):
        ReportDescription("")