"""Use case for resolving malfunction reports"""
from uuid import UUID
from ..dtos.resolve_report_dto import ResolveReportRequest, ResolveReportResponse
from contexts.reporting.domain.services.malfunction_report_service import MalfunctionReportService


class ResolveMalfunctionUseCase:
    """Use Case: Resolve a malfunction report"""
    
    def __init__(self, report_service: MalfunctionReportService):
        self._report_service = report_service
    
    def execute(self, request: ResolveReportRequest) -> ResolveReportResponse:
        """Execute the use case to resolve a malfunction"""
        try:
            ticket_id = UUID(request.ticket_id)
            
            # Get report details before resolution
            all_reports = self._report_service.get_all_reports()
            report = next(
                (r for r in all_reports if r.ticket_id == ticket_id),
                None
            )
            
            if not report:
                return ResolveReportResponse(
                    success=False,
                    ticket_id=request.ticket_id,
                    station_id=None,
                    message=f"No report found with ticket ID {request.ticket_id}"
                )
            
            station_id = report.station_id.value  # Get just the value, not the whole object string
            
            # Resolve the malfunction
            self._report_service.resolve_malfunction(
                ticket_id=ticket_id,
                operator_notes=request.operator_notes
            )
            
            return ResolveReportResponse(
                success=True,
                ticket_id=request.ticket_id,
                station_id=station_id,
                message=f"Malfunction resolved for station {station_id}"
            )
            
        except ValueError as e:
            return ResolveReportResponse(
                success=False,
                ticket_id=request.ticket_id,
                station_id=None,
                message=str(e)
            )
        except Exception as e:
            return ResolveReportResponse(
                success=False,
                ticket_id=request.ticket_id,
                station_id=None,
                message=f"Unexpected error: {str(e)}"
            )