def ascending(A):
    if len(A) > 2:
        current_max = A[0]
        current_min = A[-1]
        asc_streak = 0
        des_streak = 0
        for i in range(len(A)):
            if A[i] < current_max:
                des_streak += 1
            current_max = max(A[i], current_max)
            if A[len(A)-i-1] > current_min:
                asc_streak += 1
            current_min = min(A[len(A)-i-1], current_min)
            if des_streak >= 2 and asc_streak >= 2:
                return False
    return True

if __name__ == '__main__':
    tc = [[-1, 4, 2, 3],
          [-1, 4, 3, 2],
          [-1, 4, 3, 5, 6],
          [-1, 4, 3, 5, 4],
          [2, 3, 3, 2, 4],
          [4, 2, 1],
          [4, 2, 3]]
    for case in tc:
        print(case, ascending(case))
