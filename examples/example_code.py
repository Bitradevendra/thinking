"""
Example code for analysis
This bubble sort implementation may have issues
"""

def bubble_sort(arr):
    """Sort an array using bubble sort algorithm"""
    n = len(arr)
    
    for i in range(n):
        # Track if any swaps were made
        swapped = False
        
        for j in range(0, n - i - 1):
            # Compare adjacent elements
            if arr[j] > arr[j + 1]:
                # Swap if they're in wrong order
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # If no swaps were made, array is sorted
        if not swapped:
            break
    
    return arr


def fibonacci(n):
    """Calculate nth Fibonacci number"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        # Recursive approach (inefficient for large n)
        return fibonacci(n - 1) + fibonacci(n - 2)


def find_prime_factors(n):
    """Find all prime factors of a number"""
    factors = []
    
    # Check for 2s
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    
    # Check odd numbers from 3 onwards
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n = n // i
        i += 2
    
    # If n is still greater than 1, it's a prime factor
    if n > 1:
        factors.append(n)
    
    return factors


if __name__ == "__main__":
    # Test bubble sort
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    sorted_array = bubble_sort(test_array.copy())
    print("Sorted array:", sorted_array)
    
    # Test fibonacci
    print("\nFirst 10 Fibonacci numbers:")
    for i in range(10):
        print(f"F({i}) = {fibonacci(i)}")
    
    # Test prime factors
    test_number = 315
    print(f"\nPrime factors of {test_number}: {find_prime_factors(test_number)}")
