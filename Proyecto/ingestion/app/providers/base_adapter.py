"""
Base adapter interface for external data sources.

This module implements the Adapter Pattern to unify different
air quality data sources (CSV files, APIs) into a common interface.
"""

from abc import ABC, abstractmethod
from typing import List

from app.domain.dto import NormalizedReading


class BaseExternalApiAdapter(ABC):
    """
    **Adapter Pattern Implementation**
    
    Base adapter that unifies different external air quality data sources
    into a common NormalizedReading model.
    
    This allows the ingestion service to work with multiple data sources
    (historical CSV files, real-time APIs) without changing the core logic.
    
    Concrete adapters must implement:
    - fetch_readings(): Retrieve and normalize data from the specific source
    """
    
    @abstractmethod
    def fetch_readings(self) -> List[NormalizedReading]:
        """
        Fetch and normalize readings from the external data source.
        
        This method must:
        1. Retrieve raw data from the source (file, API, etc.)
        2. Parse and validate the data
        3. Normalize it into NormalizedReading objects
        4. Return a list of valid readings
        
        Returns:
            List of NormalizedReading objects
            
        Raises:
            Exception: If data fetching or normalization fails
        """
        pass
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
