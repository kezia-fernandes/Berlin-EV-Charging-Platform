"""DTOs for malfunction report creation"""
from dataclasses import dataclass
from typing import Optional
from contexts.reporting.domain.enums.malfunction_type import MalfunctionType


@dataclass(frozen=True)
class CreateReportRequest:
    """Request DTO for creating a malfunction report"""
    station_id: str
    malfunction_type: MalfunctionType
    description: str
    reported_by: Optional[str] = None
    
    def __post_init__(self):
        """Validate DTO fields"""
        if not self.station_id or not self.station_id.strip():
            raise ValueError("Station ID cannot be empty")
        
        if not self.description or not self.description.strip():
            raise ValueError("Description cannot be empty")
        
        if not isinstance(self.malfunction_type, MalfunctionType):
            raise ValueError("Invalid malfunction type")


@dataclass(frozen=True)
class CreateReportResponse:
    """Response DTO for report creation"""
    report_id: str
    ticket_id: Optional[str]
    success: bool
    errors: list[str]
    
    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0