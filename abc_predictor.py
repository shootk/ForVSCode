def get_max_index(k):
    # 現在の文字列の最大のindexを計算
    return 3 * (2 ** k - 1) - 1


input_line = input()
input_line = input_line.rstrip().split()
k, s, t = int(input_line[0]), int(input_line[1]), int(input_line[2])

top = 0
end = now_t - now_s
now_s, now_t = s, t
lv = k

result = [''] * (t - s)
separate = False

while True:
    if not separate:
        if now_t - now_s >= get_max_index(lv - 1):
            break

        if now_s == 0:
            result[top] = 0
            top += 1

        elif now_s <= mid_index and mid_index <= now_t:
            separate = True
            result[mid_index - now_s] = 'b'
            now_t -= mid_index

        elif now_t == max_index:
            result[end] = max_index
            end -= 1

    else:

    if not separate:
        if now_s > mid_index:
            now_s -= mid_index
            now_t -= mid_index
        now_s -= 1
        now_t -= 1

    else:
