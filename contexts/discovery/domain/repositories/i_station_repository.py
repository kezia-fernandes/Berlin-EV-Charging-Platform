from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.operational_station import OperationalStation
from contexts.shared_kernel.common.station_id import StationId


class IStationRepository(ABC):
    """Repository interface for OperationalStation aggregate"""
    
    @abstractmethod
    def save(self, station: OperationalStation) -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, station_id: StationId) -> Optional[OperationalStation]:
        pass
    
    @abstractmethod
    def find_by_postal_code(self, postal_code: str) -> List[OperationalStation]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[OperationalStation]:
        pass
    
    @abstractmethod
    def exists(self, station_id: StationId) -> bool:
        pass