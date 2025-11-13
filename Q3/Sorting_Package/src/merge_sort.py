"""
src/merge_sort.py
Merge Sort implementation
"""
from typing import List
from .sorting_base import SortingAlgorithm


class MergeSort(SortingAlgorithm):
    """Merge Sort implementation"""
    
    def sort(self, arr: List[int], ascending: bool = True) -> List[int]:
        """
        Sort array using merge sort algorithm
        
        Args:
            arr: List of integers to sort
            ascending: If True, sort in ascending order, else descending
            
        Returns:
            Sorted list of integers
        """
        result = arr.copy()
        self._merge_sort_helper(result, 0, len(result) - 1, ascending)
        return result
    
    def _merge_sort_helper(self, arr: List[int], left: int, 
                          right: int, ascending: bool) -> None:
        """
        Helper function for merge sort
        
        Args:
            arr: List to sort in-place
            left: Starting index
            right: Ending index
            ascending: Sort order
        """
        if left < right:
            mid = (left + right) // 2
            self._merge_sort_helper(arr, left, mid, ascending)
            self._merge_sort_helper(arr, mid + 1, right, ascending)
            self._merge(arr, left, mid, right, ascending)
    
    def _merge(self, arr: List[int], left: int, mid: int, 
               right: int, ascending: bool) -> None:
        """
        Merge two sorted subarrays
        
        Args:
            arr: List containing subarrays
            left: Starting index of left subarray
            mid: Ending index of left subarray
            right: Ending index of right subarray
            ascending: Sort order
        """
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]
        
        i = j = 0
        k = left
        
        while i < len(left_part) and j < len(right_part):
            if ascending:
                if left_part[i] <= right_part[j]:
                    arr[k] = left_part[i]
                    i += 1
                else:
                    arr[k] = right_part[j]
                    j += 1
            else:
                if left_part[i] >= right_part[j]:
                    arr[k] = left_part[i]
                    i += 1
                else:
                    arr[k] = right_part[j]
                    j += 1
            k += 1
        
        while i < len(left_part):
            arr[k] = left_part[i]
            i += 1
            k += 1
        
        while j < len(right_part):
            arr[k] = right_part[j]
            j += 1
            k += 1
    
    def get_name(self) -> str:
        """Return the name of the sorting algorithm"""
        return "Merge Sort"