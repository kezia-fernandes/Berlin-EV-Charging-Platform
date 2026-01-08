"""Use case for creating malfunction reports"""
from ..dtos.create_report_dto import CreateReportRequest, CreateReportResponse
from contexts.reporting.domain.services.malfunction_report_service import MalfunctionReportService


class CreateMalfunctionReportUseCase:
    """Use Case: Create and process a malfunction report"""
    
    def __init__(self, report_service: MalfunctionReportService):
        self._report_service = report_service
    
    def execute(self, request: CreateReportRequest) -> CreateReportResponse:
        """Execute the use case to create a malfunction report"""
        try:
            # Submit the report
            report_id = self._report_service.submit_malfunction_report(
                station_id=request.station_id,
                malfunction_type=request.malfunction_type,
                description=request.description,
                reported_by=request.reported_by
            )
            
            # Process the report
            processing_result = self._report_service.process_malfunction_report(report_id)
            
            # Return response
            return CreateReportResponse(
                report_id=str(report_id),
                ticket_id=str(processing_result.ticket_id) if processing_result.ticket_id else None,
                success=processing_result.success,
                errors=processing_result.errors
            )
            
        except ValueError as e:
            return CreateReportResponse(
                report_id="",
                ticket_id=None,
                success=False,
                errors=[str(e)]
            )
        except Exception as e:
            return CreateReportResponse(
                report_id="",
                ticket_id=None,
                success=False,
                errors=[f"Unexpected error: {str(e)}"]
            )