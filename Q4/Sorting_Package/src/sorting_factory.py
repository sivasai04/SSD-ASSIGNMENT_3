"""
src/sorting_factory.py
Factory class to invoke different sorting algorithms
"""
from typing import List
from .bubble_sort import BubbleSort
from .selection_sort import SelectionSort
from .quick_sort import QuickSort
from .merge_sort import MergeSort
from .shell_sort import ShellSort


class SortingFactory:
    """Factory class to create and use sorting algorithms"""
    def __init__(self):
        """Initialize the factory with available algorithms"""
        self.algorithms = {
            'bubble': BubbleSort(),
            'selection': SelectionSort(),
            'quick': QuickSort(),
            'merge': MergeSort(),
            'shell': ShellSort()
        }
    def sort(self, algorithm_name: str, input_list: List[int], ascending: bool = True) -> List[int]:
        """
        Sort using the specified algorithm
        
        Args:
            algorithm_name: Name of algorithm ('bubble', 'selection', 
                          'quick', 'merge')
            input_list: List of integers to sort
            ascending: If True, sort ascending, else descending
            
        Returns:
            Sorted list of integers
            
        Raises:
            ValueError: If algorithm name is invalid or list contains 
                       non-integers
            TypeError: If input is not a list
        """
        # Validate input type
        if not isinstance(input_list, list):
            raise TypeError("Input must be a list")
        # Validate all elements are integers
        if not all(isinstance(x, int) for x in input_list):
            raise ValueError("All elements must be integers")
        # Validate list size
        if len(input_list) > 2e5:
            raise ValueError("List size exceeds maximum of 2x10^5 elements")
        # Validate element range (INT32)
        for elem in input_list:
            if elem < -2147483648 or elem > 2147483647:
                raise ValueError(f"Element {elem} outside INT32 range")
        # Get algorithm
        algorithm_name = algorithm_name.lower()
        if algorithm_name not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm_name}. "
                           f"Available: {list(self.algorithms.keys())}")
        algorithm = self.algorithms[algorithm_name]
        return algorithm.sort(input_list, ascending)
    def get_available_algorithms(self) -> List[str]:
        """Return list of available algorithm names"""
        return list(self.algorithms.keys())
    