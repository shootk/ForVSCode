def get_max_index(k):
    # 現在の文字列の最大のindexを計算
    return 3 * (2 ** k - 1) - 1


def level_down(now_s, now_t, lv):
    max_index = get_max_index(lv)
    mid_index = max_index / 2
    if get_max_index(lv - 1) < t - s:
        get_result()


def get_result():
    pass


input_line = input()

input_line = input_line.rstrip().split()
k, s, t = int(input_line[0]), int(input_line[1]), int(input_line[2])

separate = False
separate_index = 0

max_index = get_max_index(k)
mid_index = max_index / 2

result = [0] * (t - s + 1)
