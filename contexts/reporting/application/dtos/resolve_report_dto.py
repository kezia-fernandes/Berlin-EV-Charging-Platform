"""DTOs for resolving malfunction reports"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ResolveReportRequest:
    """Request DTO for resolving a report"""
    ticket_id: str
    operator_notes: Optional[str] = None
    
    def __post_init__(self):
        """Validate DTO fields"""
        if not self.ticket_id or not self.ticket_id.strip():
            raise ValueError("Ticket ID cannot be empty")


@dataclass(frozen=True)
class ResolveReportResponse:
    """Response DTO for report resolution"""
    success: bool
    ticket_id: str
    station_id: Optional[str]
    message: str