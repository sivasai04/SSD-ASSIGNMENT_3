"""
src/quick_sort.py
Quick Sort implementation
"""
from typing import List
from .sorting_base import SortingAlgorithm


class QuickSort(SortingAlgorithm):
    """Quick Sort implementation"""
    
    def sort(self, arr: List[int], ascending: bool = True) -> List[int]:
        """
        Sort array using quick sort algorithm
        
        Args:
            arr: List of integers to sort
            ascending: If True, sort in ascending order, else descending
            
        Returns:
            Sorted list of integers
        """
        result = arr.copy()
        self._quick_sort_helper(result, 0, len(result) - 1, ascending)
        return result
    
    def _quick_sort_helper(self, arr: List[int], low: int, 
                          high: int, ascending: bool) -> None:
        """
        Helper function for quick sort
        
        Args:
            arr: List to sort in-place
            low: Starting index
            high: Ending index
            ascending: Sort order
        """
        if low < high:
            pivot_idx = self._partition(arr, low, high, ascending)
            self._quick_sort_helper(arr, low, pivot_idx - 1, ascending)
            self._quick_sort_helper(arr, pivot_idx + 1, high, ascending)
    
    def _partition(self, arr: List[int], low: int, 
                   high: int, ascending: bool) -> int:
        """
        Partition function for quick sort
        
        Args:
            arr: List to partition
            low: Starting index
            high: Ending index
            ascending: Sort order
            
        Returns:
            Pivot index
        """
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if ascending:
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            else:
                if arr[j] >= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def get_name(self) -> str:
        """Return the name of the sorting algorithm"""
        return "Quick Sort"