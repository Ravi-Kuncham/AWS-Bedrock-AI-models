# Here is Python code to implement binary search:

# Python:
def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        
        if arr[mid] == x:
            return mid
        
        elif arr[mid] < x:
            low = mid + 1
            
        else:
            high = mid - 1
            
    return -1

# Example usage:
arr = [2, 4, 6, 8, 10, 12, 14] 
x = 10

result = binary_search(arr, x)
if result != -1:
    print("Element found at index", result)
else:
    print("Element not found in array")

# This implements a recursive binary search algorithm. It takes the sorted array `arr` and value `x` to search for as input. It starts by comparing `x` with the middle element of `arr`. If equal, it returns the index. If `x` is less than the middle, it recurses on the left half of the array. If greater, it recurses on the right half. It returns -1 if `x` is not found.