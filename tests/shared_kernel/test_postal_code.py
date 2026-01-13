"""Tests for PostalCode Value Object"""
import pytest
from contexts.shared_kernel.common.postal_code import PostalCode


class TestPostalCode:
    """Test suite for PostalCode value object"""
    
    # HAPPY PATH
    def test_create_valid_berlin_postal_code(self):
        postal_code = PostalCode("10115")
        assert postal_code.value == "10115"
    
    def test_create_another_valid_postal_code(self):
        postal_code = PostalCode("14055")
        assert postal_code.value == "14055"
    
    # ERROR SCENARIOS
    def test_empty_postal_code_raises_error(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            PostalCode("")
    
    def test_whitespace_postal_code_raises_error(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            PostalCode("   ")
    
    def test_non_numeric_postal_code_raises_error(self):
        with pytest.raises(ValueError, match="must be numeric only"):
            PostalCode("ABC12")
    
    def test_postal_code_with_letters_raises_error(self):
        with pytest.raises(ValueError, match="must be numeric only"):
            PostalCode("101A5")
    
    # EDGE CASES
    def test_postal_code_too_short(self):
        with pytest.raises(ValueError, match="exactly 5 digits"):
            PostalCode("1234")
    
    def test_postal_code_too_long(self):
        with pytest.raises(ValueError, match="exactly 5 digits"):
            PostalCode("123456")
    
    # DOMAIN RULES
    def test_non_berlin_postal_code_raises_error(self):
        with pytest.raises(ValueError, match="Berlin postal code"):
            PostalCode("20095")  # Hamburg
    
    def test_another_non_berlin_postal_code(self):
        with pytest.raises(ValueError, match="Berlin postal code"):
            PostalCode("80331")  # Munich
    
    def test_postal_code_starting_with_zero(self):
        with pytest.raises(ValueError, match="Berlin postal code"):
            PostalCode("01234")
    
    # VALUE OBJECT PROPERTIES
    def test_postal_code_is_immutable(self):
        postal_code = PostalCode("10115")
        with pytest.raises(Exception):
            postal_code.value = "10116"  # type: ignore
    
    def test_postal_codes_equality(self):
        postal1 = PostalCode("10115")
        postal2 = PostalCode("10115")
        assert postal1 == postal2
    
    def test_postal_codes_inequality(self):
        postal1 = PostalCode("10115")
        postal2 = PostalCode("10116")
        assert postal1 != postal2