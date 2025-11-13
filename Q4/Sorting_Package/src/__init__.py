"""
src/__init__.py
Package initialization for sorting algorithms
"""
from .sorting_base import SortingAlgorithm
from .bubble_sort import BubbleSort
from .selection_sort import SelectionSort
from .quick_sort import QuickSort
from .merge_sort import MergeSort
from .sorting_factory import SortingFactory
from .shell_sort import ShellSort 

__all__ = [
    'SortingAlgorithm',
    'BubbleSort',
    'SelectionSort',
    'QuickSort',
    'MergeSort',
    'SortingFactory'
    'Shellsort'
]

__version__ = '1.0.0'
