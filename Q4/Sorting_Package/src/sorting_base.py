"""
src/sorting_base.py
Abstract base class for sorting algorithms
"""
from abc import ABC, abstractmethod
from typing import List

class SortingAlgorithm(ABC):
    """Abstract base class for sorting algorithms"""
    @abstractmethod
    def sort(self, arr: List[int], ascending: bool = True) -> List[int]:
        """
        Sort the given array
        
        Args:
            arr: List of integers to sort
            ascending: If True, sort in ascending order, else descending
            
        Returns:
            Sorted list of integers
        """
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of the sorting algorithm"""
