"""
src/bubble_sort.py
Bubble Sort implementation
"""
from typing import List
from .sorting_base import SortingAlgorithm


class BubbleSort(SortingAlgorithm):
    """Bubble Sort implementation"""
    def sort(self, arr: List[int], ascending: bool = True) -> List[int]:
        """
        Sort array using bubble sort algorithm
        
        Args:
            arr: List of integers to sort
            ascending: If True, sort in ascending order, else descending
            
        Returns:
            Sorted list of integers
        """
        result = arr.copy()
        n = len(result)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if ascending:
                    if result[j] > result[j + 1]:
                        result[j], result[j + 1] = result[j + 1], result[j]
                        swapped = True
                else:
                    if result[j] < result[j + 1]:
                        result[j], result[j + 1] = result[j + 1], result[j]
                        swapped = True
            if not swapped:
                break
        return result
    
    def get_name(self) -> str:
        """Return the name of the sorting algorithm"""
        return "Bubble Sort"