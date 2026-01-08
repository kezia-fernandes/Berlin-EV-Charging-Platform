from typing import List

from ...domain.entities.operational_station import OperationalStation
from ...domain.repositories.i_station_repository import IStationRepository
from contexts.shared_kernel.common.station_id import StationId
from contexts.shared_kernel.common.postal_code import PostalCode  # ← ADD THIS


class SearchStationsUseCase:
    """Use case for searching charging stations"""
    
    def __init__(self, station_repository: IStationRepository):
        self._repository = station_repository
    
    def execute_by_postal_code(self, postal_code: str) -> List[OperationalStation]:
        """Search stations by postal code"""
        # PostalCode value object handles all validation
        postal_code_vo = PostalCode(postal_code)
        
        # Use the validated value
        return self._repository.find_by_postal_code(postal_code_vo.value)
    
    def execute_by_id(self, station_id: str) -> OperationalStation:
        """Get specific station by ID"""
        station_id_vo = StationId(station_id)
        station = self._repository.find_by_id(station_id_vo)
        
        if not station:
            raise ValueError(f"Station {station_id} not found")
        
        return station
    
    def execute_all(self) -> List[OperationalStation]:
        """Get all stations"""
        return self._repository.find_all()