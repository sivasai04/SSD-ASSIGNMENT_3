"""
main.py
Main file to demonstrate sorting algorithms
Reads from .txt file and outputs to reports folder
"""
import sys
from src.sorting_factory import SortingFactory


def read_input(filename):
    """
    Read input from text file
    
    Format:
    algorithm_name
    ascending/descending
    comma,separated,numbers
    
    Args:
        filename: Path to input file
        
    Returns:
        List of test cases
    """
    test_cases = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            
            i = 0
            while i < len(lines):
                if i + 2 >= len(lines):
                    break
                    
                algorithm = lines[i].lower()
                order = lines[i + 1].lower()
                ascending = order == 'ascending'
                
                # Parse numbers
                numbers_str = lines[i + 2]
                if numbers_str:
                    input_list = [int(x.strip()) for x in numbers_str.split(',')]
                else:
                    input_list = []
                
                test_cases.append({
                    'algorithm': algorithm,
                    'ascending': ascending,
                    'input_list': input_list
                })
                
                i += 3
                
        return test_cases
        
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid number format - {e}")
        sys.exit(1)


def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file.txt>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Read input
    test_cases = read_input(input_file)
    
    # Initialize factory
    factory = SortingFactory()
    
    print("=" * 70)
    print(" SORTING ALGORITHMS DEMONSTRATION")
    print("=" * 70)
    
    # Process each test case
    for i, test_case in enumerate(test_cases, 1):
        algorithm = test_case['algorithm']
        input_list = test_case['input_list']
        ascending = test_case['ascending']
        
        print(f"\nTest Case {i}:")
        print(f"  Algorithm: {algorithm}")
        print(f"  Order: {'Ascending' if ascending else 'Descending'}")
        print(f"  Input Size: {len(input_list)}")
        print(f"  Input: {input_list}")
        
        try:
            result = factory.sort(algorithm, input_list, ascending)
            print(f"  Output: {result}")
            print(f"  Status: ✓ SUCCESS")
        except Exception as e:
            print(f"  Error: {e}")
            print(f"  Status: ✗ FAILED")
    
    print("\n" + "=" * 70)
    print(" DEMONSTRATION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()