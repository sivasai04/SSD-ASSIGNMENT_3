"""
src/shell_sort.py
Shell Sort implementation
"""
from typing import List
from src.sorting_base import SortingAlgorithm


class ShellSort(SortingAlgorithm):
    """Shell Sort implementation"""
    def sort(self, arr: List[int], ascending: bool = True) -> List[int]:
        """
        Sort array using shell sort algorithm
        
        Args:
            arr: List of integers to sort
            ascending: If True, sort in ascending order, else descending
            
        Returns:
            Sorted list of integers
        """
        result = arr.copy()
        n = len(result)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = result[i]
                j = i
                if ascending:
                    while j >= gap and result[j - gap] > temp:
                        result[j] = result[j - gap]
                        j -= gap
                else:
                    while j >= gap and result[j - gap] < temp:
                        result[j] = result[j - gap]
                        j -= gap
                result[j] = temp
            gap //= 2
        return result
    def get_name(self) -> str:
        """Return the name of the sorting algorithm"""
        return "Shell Sort"