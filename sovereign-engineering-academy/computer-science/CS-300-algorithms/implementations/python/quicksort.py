"""
Quicksort implementation in Python
CS-300: Algorithms
SME: Claude (Anthropic)

Quicksort is a divide-and-conquer sorting algorithm.
Average case: O(n log n)
Worst case: O(n²) - when pivot selection is poor
Space: O(log n) - due to recursion stack

Key insight from Claude (Session 23):
"Quicksort is like organizing pipes by length.
 Pick a middle-length pipe (pivot).
 Put shorter pipes on left, longer on right.
 Repeat for each pile."
"""

def quicksort(arr):
    """
    Sort array in-place using quicksort algorithm.
    
    Args:
        arr: List of comparable elements
    
    Returns:
        Sorted list
    
    Example:
        >>> quicksort([3, 1, 4, 1, 5, 9, 2, 6])
        [1, 1, 2, 3, 4, 5, 6, 9]
    """
    if len(arr) <= 1:
        return arr
    
    # Choose pivot (median-of-three for better performance)
    pivot = _choose_pivot(arr)
    
    # Partition into three groups
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    
    # Recursively sort and combine
    return quicksort(less) + equal + quicksort(greater)


def _choose_pivot(arr):
    """
    Choose pivot using median-of-three method.
    Reduces chance of worst-case O(n²) behavior.
    
    Claude's insight (Session 24):
    "Don't just pick the first pipe. That might be the longest or shortest.
     Pick the middle-ish one. That's more balanced."
    """
    if len(arr) <= 3:
        return arr[0]
    
    first = arr[0]
    middle = arr[len(arr) // 2]
    last = arr[-1]
    
    # Return median of three
    return sorted([first, middle, last])[1]


def quicksort_inplace(arr, low=0, high=None):
    """
    In-place quicksort (more memory efficient).
    
    Space complexity: O(log n) - only recursion stack
    vs O(n) for the list comprehension version above
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # Partition and get pivot index
        pivot_idx = _partition(arr, low, high)
        
        # Recursively sort left and right
        quicksort_inplace(arr, low, pivot_idx - 1)
        quicksort_inplace(arr, pivot_idx + 1, high)
    
    return arr


def _partition(arr, low, high):
    """
    Partition array around pivot.
    
    Dom's "aha moment" (Session 23):
    "It's not about sorting YET. It's about ORGANIZING.
     Just make sure everything less is on left.
     THEN sort each side."
    """
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# TRIG6 Application: Sort pipe segments by length
def sort_pipe_segments(segments):
    """
    Sort pipe segments for optimal cutting order.
    
    Real-world use case in TRIG6:
    When cutting pipes to length, sort from longest to shortest.
    Cut longest first (can't reuse mistakes as easily).
    """
    # Each segment is (length, angle, material)
    return quicksort_inplace(segments, key=lambda s: s[0], reverse=True)


if __name__ == "__main__":
    # Test with TRIG6 angles
    angles = [45, 90, 30, 60, 0, 45]
    sorted_angles = quicksort(angles)
    print(f"Sorted TRIG6 angles: {sorted_angles}")
    
    # Performance test
    import random
    import time
    
    test_data = [random.randint(0, 10000) for _ in range(10000)]
    
    start = time.time()
    quicksort(test_data.copy())
    end = time.time()
    
    print(f"Sorted 10,000 elements in {end - start:.4f} seconds")
    print(f"Complexity: O(n log n) = {10000 * 13.3:.0f} operations (theoretical)")
