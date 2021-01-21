import random
import sys
N = 10
sys.setrecursionlimit(100)


def input_data(data):
    for i in range(N):
        data.append(random.randint(0, N))
    return data


def quick_sort(left, right):
    if left >= right:
        return
    else:
        pivot = data[right]
        partition = division(left, right, pivot)
        print("partition = " + str(partition))
        quick_sort(left, partition - 2)
        quick_sort(partition - 1, right)


def division(left, right, pivot):
    p = left
    print("div start")
    print("left:" + str(left) + ",right:" + str(right))
    print(data)
    for i in range(left, right + 1):
        if data[i] <= pivot:
            data[i], data[p] = data[p], data[i]
            p += 1
    print("div end")
    print(data)
    return p


if __name__ == "__main__":
    print("start")
    data = []
    data = input_data(data)
    print(data)
    quick_sort(0, N - 1)
    print(data)
