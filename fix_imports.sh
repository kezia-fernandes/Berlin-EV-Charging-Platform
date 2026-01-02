#!/bin/bash
#!/bin/bash
# Quick fix for import path issues
# Run from: /mnt/d/Advanced_Software/Berlin-EV-Charging-Platform

cd /mnt/d/Advanced_Software/Berlin-EV-Charging-Platform

echo "🔧 Fixing import paths in repository interfaces..."

# Fix i_station_repository.py - it has wrong import
cat > contexts/reporting/domain/repositories/i_station_repository.py << 'EOF'
from abc import ABC, abstractmethod
from typing import Optional, List
from contexts.reporting.domain.entities.operational_station import OperationalStation
from contexts.reporting.domain.value_objects.station_id import StationId


class IStationRepository(ABC):
    """Repository interface for OperationalStation aggregate"""
    
    @abstractmethod
    def save(self, station: OperationalStation) -> None:
        """Save or update a charging station"""
        pass
    
    @abstractmethod
    def find_by_id(self, station_id: StationId) -> Optional[OperationalStation]:
        """Find a station by its ID"""
        pass
    
    @abstractmethod
    def find_by_postal_code(self, postal_code: str) -> List[OperationalStation]:
        """Find all stations in a postal code area"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[OperationalStation]:
        """Get all charging stations"""
        pass
    
    @abstractmethod
    def exists(self, station_id: StationId) -> bool:
        """Check if a station exists"""
        pass
EOF

echo "✅ Fixed i_station_repository.py"

# Now verify all domain files have correct content
echo ""
echo "🔍 Verifying all domain files exist with correct imports..."

# Check if entities have the _updated_at attribute issue
cat > contexts/reporting/domain/entities/malfunction_report.py << 'EOF'
from uuid import UUID
from datetime import datetime
from typing import Optional
from contexts.reporting.domain.value_objects.station_id import StationId
from contexts.reporting.domain.value_objects.report_description import ReportDescription
from contexts.reporting.domain.enums.malfunction_type import MalfunctionType
from contexts.reporting.domain.enums.report_status import ReportStatus


class MalfunctionReport:
    """
    Entity: Malfunction Report
    Represents a user-submitted report about a station malfunction
    """
    
    def __init__(
        self,
        report_id: UUID,
        station_id: StationId,
        malfunction_type: MalfunctionType,
        description: ReportDescription,
        reported_by: Optional[str] = None
    ):
        self._report_id = report_id
        self._station_id = station_id
        self._malfunction_type = malfunction_type
        self._description = description
        self._reported_by = reported_by
        self._status = ReportStatus.SUBMITTED
        self._ticket_id: Optional[UUID] = None
        self._created_at = datetime.now()
        self._updated_at = datetime.now()  # Initialize this!
        self._validation_errors: list[str] = []
    
    @property
    def report_id(self) -> UUID:
        """Get report ID"""
        return self._report_id
    
    @property
    def station_id(self) -> StationId:
        """Get station ID"""
        return self._station_id
    
    @property
    def status(self) -> ReportStatus:
        """Get current status"""
        return self._status
    
    @property
    def ticket_id(self) -> Optional[UUID]:
        """Get associated ticket ID"""
        return self._ticket_id
    
    def validate(self, station_exists: bool, station_is_operational: bool) -> bool:
        """
        Validate the report against business rules
        
        Args:
            station_exists: Whether the station exists in the system
            station_is_operational: Whether the station is available/in-use (not defective)
        
        Returns:
            True if valid, False otherwise
        """
        self._validation_errors.clear()
        
        # Business Rule 1: Station must exist
        if not station_exists:
            self._validation_errors.append("Charging station does not exist")
        
        # Business Rule 2: Station should not already be defective
        if not station_is_operational:
            self._validation_errors.append("Station already marked as defective")
        
        # Update status based on validation
        if self._validation_errors:
            self._status = ReportStatus.INVALID
            return False
        
        self._status = ReportStatus.VALIDATED
        return True
    
    def get_validation_errors(self) -> list[str]:
        """Get validation error messages"""
        return self._validation_errors.copy()
    
    def create_ticket(self, ticket_id: UUID) -> None:
        """
        Create a ticket for this validated report
        
        Args:
            ticket_id: UUID of the ticket being created
        
        Raises:
            ValueError: If report is not validated
        """
        if self._status != ReportStatus.VALIDATED:
            raise ValueError("Cannot create ticket for non-validated report")
        
        self._ticket_id = ticket_id
        self._status = ReportStatus.TICKET_CREATED
        self._updated_at = datetime.now()
    
    def resolve(self) -> None:
        """
        Mark the report as resolved
        
        Raises:
            ValueError: If report doesn't have a ticket
        """
        if self._ticket_id is None:
            raise ValueError("Cannot resolve report without a ticket")
        
        self._status = ReportStatus.RESOLVED
        self._updated_at = datetime.now()
EOF

echo "✅ Fixed malfunction_report.py with _updated_at"

echo ""
echo "🧪 Testing imports..."
python3 << 'PYEOF'
import sys
sys.path.insert(0, '/mnt/d/Advanced_Software/Berlin-EV-Charging-Platform')

try:
    from contexts.reporting.domain.repositories.i_station_repository import IStationRepository
    print("✅ IStationRepository imports correctly")
except Exception as e:
    print(f"❌ IStationRepository import failed: {e}")

try:
    from contexts.reporting.domain.repositories.i_report_repository import IReportRepository
    print("✅ IReportRepository imports correctly")
except Exception as e:
    print(f"❌ IReportRepository import failed: {e}")

try:
    from contexts.reporting.domain.services.malfunction_report_service import MalfunctionReportService
    print("✅ MalfunctionReportService imports correctly")
except Exception as e:
    print(f"❌ MalfunctionReportService import failed: {e}")

try:
    from contexts.reporting.infrastructure.repositories.in_memory_station_repository import InMemoryStationRepository
    print("✅ InMemoryStationRepository imports correctly")
except Exception as e:
    print(f"❌ InMemoryStationRepository import failed: {e}")
PYEOF

echo ""
echo "✅ All fixes applied! Now run: pytest contexts/reporting/tests -v"
