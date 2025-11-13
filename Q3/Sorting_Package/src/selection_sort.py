"""
src/selection_sort.py
Selection Sort implementation
"""
from typing import List
from .sorting_base import SortingAlgorithm


class SelectionSort(SortingAlgorithm):
    """Selection Sort implementation"""
    
    def sort(self, arr: List[int], ascending: bool = True) -> List[int]:
        """
        Sort array using selection sort algorithm
        
        Args:
            arr: List of integers to sort
            ascending: If True, sort in ascending order, else descending
            
        Returns:
            Sorted list of integers
        """
        result = arr.copy()
        n = len(result)
        
        for i in range(n):
            extreme_idx = i
            
            for j in range(i + 1, n):
                if ascending:
                    if result[j] < result[extreme_idx]:
                        extreme_idx = j
                else:
                    if result[j] > result[extreme_idx]:
                        extreme_idx = j
            
            result[i], result[extreme_idx] = result[extreme_idx], result[i]
        
        return result
    
    def get_name(self) -> str:
        """Return the name of the sorting algorithm"""
        return "Selection Sort"