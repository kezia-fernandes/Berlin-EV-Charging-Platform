from typing import Optional, List, Dict

from ...domain.entities.operational_station import OperationalStation
from contexts.shared_kernel.common.station_id import StationId
from ...domain.repositories.i_station_repository import IStationRepository


class InMemoryStationRepository(IStationRepository):
    """In-memory implementation of station repository"""
    
    def __init__(self):
        self._stations: Dict[str, OperationalStation] = {}
    
    def save(self, station: OperationalStation) -> None:
        key = station.station_id.value
        self._stations[key] = station
    
    def find_by_id(self, station_id: StationId) -> Optional[OperationalStation]:
        return self._stations.get(station_id.value)
    
    def find_by_postal_code(self, postal_code: str) -> List[OperationalStation]:
        return [
            station for station in self._stations.values()
            if station.postal_code == postal_code
        ]
    
    def find_all(self) -> List[OperationalStation]:
        return list(self._stations.values())
    
    def exists(self, station_id: StationId) -> bool:
        return station_id.value in self._stations
