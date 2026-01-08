"""PostalCode Value Object for Berlin postal codes"""
from dataclasses import dataclass


@dataclass(frozen=True)
class PostalCode:
    """
    Value Object representing a Berlin postal code.
    
    Business Rules:
    - Must be numeric only
    - Must be exactly 5 digits
    - Must start with '1' (Berlin postal codes: 10xxx-14xxx)
    """
    value: str
    
    def __post_init__(self):
        """Validate postal code on creation"""
        if not self.value or not self.value.strip():
            raise ValueError("Postal code cannot be empty")
        
        if not self.value.isdigit():
            raise ValueError("Postal code must be numeric only")
        
        if len(self.value) != 5:
            raise ValueError("Postal code must be exactly 5 digits")
        
        if not self.value.startswith('1'):
            raise ValueError("Must be a Berlin postal code (starts with 1)")
    
    def __str__(self) -> str:
        return self.value