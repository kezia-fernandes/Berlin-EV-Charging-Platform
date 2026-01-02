from dataclasses import dataclass

@dataclass(frozen=True)
class StationId:
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Station ID cannot be empty")
        if len(self.value) > 50:
            raise ValueError("Station ID too long (max 50 characters)")