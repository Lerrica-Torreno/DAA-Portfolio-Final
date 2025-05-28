import time

def combSort(arr, order='ascending'):
    n = len(arr)
    gap = n
    shrink = 1.3
    sorted_flag = False
    start_time = time.time()

    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True
        for i in range(n - gap):
            if (order == 'ascending' and arr[i] > arr[i + gap]) or (order == 'descending' and arr[i] < arr[i + gap]):
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted_flag = False

    end_time = time.time()
    elapsed_time = end_time - start_time
    return arr, elapsed_time
