"""
test/test_sorting.py
Test cases for sorting algorithms - Minimal output version
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.bubble_sort import BubbleSort
from src.selection_sort import SelectionSort
from src.quick_sort import QuickSort
from src.merge_sort import MergeSort
from src.sorting_factory import SortingFactory


class TestSortingAlgorithms:
    """Test suite for sorting algorithms"""
    
    def __init__(self):
        """Initialize test suite"""
        self.algorithms = [
            BubbleSort(),
            SelectionSort(),
            QuickSort(),
            MergeSort()
        ]
        self.test_cases = self._generate_test_cases()
        self.total_passed = 0
        self.total_failed = 0
    
    def _generate_test_cases(self):
        """Generate test cases"""
        return [
            ([], []),
            ([1], [1]),
            ([1, 2], [1, 2]),
            ([2, 1], [1, 2]),
            ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
            ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
            ([3, 1, 2, 1, 3], [1, 1, 2, 3, 3]),
            ([5, 5, 5, 5], [5, 5, 5, 5]),
            ([64, 34, 25, 12, 22, 11, 90], [11, 12, 22, 25, 34, 64, 90]),
            ([-5, -1, -10, 0, 5], [-10, -5, -1, 0, 5]),
            ([10, -5, 0, -10, 5], [-10, -5, 0, 5, 10]),
            ([2147483647, -2147483648, 0], [-2147483648, 0, 2147483647]),
        ]
    
    def test_ascending_order(self):
        """Test all algorithms for ascending order"""
        print("Testing Ascending Order:")
        
        for algo in self.algorithms:
            passed = 0
            failed = 0
            failed_cases = []
            
            for input_arr, expected in self.test_cases:
                result = algo.sort(input_arr.copy(), ascending=True)
                if result == expected:
                    passed += 1
                else:
                    failed += 1
                    failed_cases.append((input_arr, expected, result))
            
            status = "✓ PASS" if failed == 0 else "✗ FAIL"
            print(f"  {algo.get_name():<20} {passed}/{len(self.test_cases)} {status}")
            
            if failed_cases:
                for inp, exp, got in failed_cases:
                    print(f"    Failed: {inp} -> Expected: {exp}, Got: {got}")
            
            self.total_passed += passed
            self.total_failed += failed
    
    def test_descending_order(self):
        """Test all algorithms for descending order"""
        print("\nTesting Descending Order:")
        
        for algo in self.algorithms:
            passed = 0
            failed = 0
            failed_cases = []
            
            for input_arr, expected_asc in self.test_cases:
                expected_desc = sorted(expected_asc, reverse=True)
                result = algo.sort(input_arr.copy(), ascending=False)
                if result == expected_desc:
                    passed += 1
                else:
                    failed += 1
                    failed_cases.append((input_arr, expected_desc, result))
            
            status = "✓ PASS" if failed == 0 else "✗ FAIL"
            print(f"  {algo.get_name():<20} {passed}/{len(self.test_cases)} {status}")
            
            if failed_cases:
                for inp, exp, got in failed_cases:
                    print(f"    Failed: {inp} -> Expected: {exp}, Got: {got}")
            
            self.total_passed += passed
            self.total_failed += failed
    
    def test_factory(self):
        """Test sorting factory"""
        print("\nTesting Factory Pattern:")
        
        factory = SortingFactory()
        algorithms = ['bubble', 'selection', 'quick', 'merge']
        
        for algo_name in algorithms:
            passed = 0
            failed = 0
            
            for input_arr, expected in self.test_cases:
                result = factory.sort(algo_name, input_arr.copy(), ascending=True)
                if result == expected:
                    passed += 1
                else:
                    failed += 1
            
            status = "✓ PASS" if failed == 0 else "✗ FAIL"
            print(f"  {algo_name:<20} {passed}/{len(self.test_cases)} {status}")
            
            self.total_passed += passed
            self.total_failed += failed
    
    def test_error_handling(self):
        """Test error handling"""
        print("\nTesting Error Handling:")
        
        factory = SortingFactory()
        tests_passed = 0
        tests_total = 3
        
        # Test invalid algorithm
        try:
            factory.sort('invalid', [1, 2, 3])
            print("  Invalid algorithm: ✗ FAIL")
        except ValueError:
            print("  Invalid algorithm: ✓ PASS")
            tests_passed += 1
        
        # Test non-integer elements
        try:
            factory.sort('bubble', [1, 'a', 3])
            print("  Non-integer input: ✗ FAIL")
        except ValueError:
            print("  Non-integer input: ✓ PASS")
            tests_passed += 1
        
        # Test non-list input
        try:
            factory.sort('bubble', "not a list")
            print("  Non-list input: ✗ FAIL")
        except TypeError:
            print("  Non-list input: ✓ PASS")
            tests_passed += 1
        
        self.total_passed += tests_passed
        self.total_failed += (tests_total - tests_passed)
    
    def run_all_tests(self):
        """Run all test suites"""
        print("=" * 60)
        print("SORTING ALGORITHMS TEST SUITE")
        print("=" * 60)
        
        self.test_ascending_order()
        self.test_descending_order()
        self.test_factory()
        self.test_error_handling()
        
        print("\n" + "=" * 60)
        print(f"TOTAL: {self.total_passed} PASSED, {self.total_failed} FAILED")
        if self.total_failed == 0:
            print("RESULT: ✓ ALL TESTS PASSED")
        else:
            print("RESULT: ✗ SOME TESTS FAILED")
        print("=" * 60)


if __name__ == "__main__":
    tester = TestSortingAlgorithms()
    tester.run_all_tests()