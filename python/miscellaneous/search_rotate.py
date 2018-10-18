def search_rotate(arr, n, start, end):
    """
        Start, end: search in indices of  [start, end]
        Return the index of n in arr, or -1 if n is not in arr
    """
    if arr[start] == n:
        return start
    else:
        if arr[end] == n:
            return end

    if arr[start] <= arr[end]:
    # encounter a sorted section
        if n > arr[end-1] or n < arr[start] or start == end: # n is not in this section
            return -1
    else:
        # The pivot is in this section
        if arr[start] > n and arr[end] < n: # n is not in this section
            return -1

    mid = (start + end) // 2
    return max(search_rotate(arr, n, start, mid), search_rotate(arr, n, mid+1, end))
 
if __name__ == '__main__':
    arr = [3,4,5,6,1,2]
    n = -1
    print(search_rotate(arr, n, 0, len(arr)-1))
