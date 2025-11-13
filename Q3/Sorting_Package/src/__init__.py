"""
src/__init__.py
Package initialization for sorting algorithms
"""

from src.sorting_base import SortingAlgorithm
from src.bubble_sort import BubbleSort
from src.selection_sort import SelectionSort
from src.quick_sort import QuickSort
from src.merge_sort import MergeSort
from src.sorting_factory import SortingFactory

__all__ = [
    'SortingAlgorithm',
    'BubbleSort',
    'SelectionSort',
    'QuickSort',
    'MergeSort',
    'SortingFactory'
]

__version__ = '1.0.0'


# For test/__init__.py, use this simpler version:
"""
test/__init__.py
Test package initialization
"""