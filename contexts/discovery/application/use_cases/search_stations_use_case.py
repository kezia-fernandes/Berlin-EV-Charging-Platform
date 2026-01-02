from typing import List

from ...domain.entities.operational_station import OperationalStation
from ...domain.repositories.i_station_repository import IStationRepository
from contexts.shared_kernel.common.station_id import StationId


class SearchStationsUseCase:
    """Use case for searching charging stations"""
    
    def __init__(self, station_repository: IStationRepository):
        self._repository = station_repository
    
    def execute_by_postal_code(self, postal_code: str) -> List[OperationalStation]:
        """Search stations by postal code"""
        if not postal_code or not postal_code.strip():
            raise ValueError("Postal code cannot be empty")
        
        if not postal_code.isdigit() or len(postal_code) != 5:
            raise ValueError("Invalid postal code format")
        
        if not postal_code.startswith('1'):
            raise ValueError("Must be a Berlin postal code")
        
        return self._repository.find_by_postal_code(postal_code)
    
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