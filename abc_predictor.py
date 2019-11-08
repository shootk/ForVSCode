def get_max_index(k):
    # 現在の文字列の最大のindexを計算
    return 3 * (2 ** k - 1) - 1


input_line = input()
input_line = input_line.rstrip().split()
k, s, t = int(input_line[0]), int(input_line[1]), int(input_line[2])

top = 0
end = t - s


now_s, now_t = s - 1, t - 1
lv = k

result = [''] * (t - s + 1)
separate = False

while True:
    ###
    print(result, lv)
    ###
    if '' not in result:
        break
    max_index = get_max_index(lv)
    mid_index = max_index // 2
    ###
    print(separate)
    if separate:
        print(now_s, '~', max_index, ',', 0, '~', now_t)
    else:
        print(now_s, '~', now_t)

    ###
    if not separate:
        if now_t - now_s >= get_max_index(lv - 1):
            for i in range(now_s, now_s + end + 1):
                result[top] = i
                top += 1
            break

        if now_s == 0:
            result[top] = 'a'
            top += 1

        elif now_s <= mid_index and mid_index <= now_t:
            separate = True
            result[mid_index - now_s] = 'b'
            now_t -= mid_index
            now_s -= 1

        elif now_t == max_index:
            result[end] = 'c'
            end -= 1

        if now_s > mid_index:
            now_s -= mid_index
            now_t -= mid_index
        if now_s < now_t and now_s > 0:
            now_s -= 1
        if now_t <= max_index and now_t > 0:
            now_t -= 1

    else:
        check = 0
        if now_t >= 0:
            check += now_t + 1
        if now_s <= max_index:
            check += max_index - now_s + 1
        if check >= get_max_index(lv - 1):
            for i in range(now_s, max_index + 1):
                result[top] = i
                top += 1
            for i in range(0, now_t + 1):
                result[end] = now_t - i
                end -= 1
            break

        if now_t >= 0:
            result[end - now_t] = 'a'
        if now_s <= max_index:
            result[max_index - now_s] = 'c'

        if now_t >= 0:
            now_t -= 1
        if now_s <= max_index:
            now_s -= (mid_index + 1)
    lv -= 1

    if lv < 0:
        break
###
print(result, lv)
###
word = ''
result_word = ''
get_words = False
for x in result:
    if type(x) == int:
        get_words = True
if get_words:
    for i in range(1, lv + 1):
        result_word = word.join('abc')
        word = result_word
        ###
        print(result_word)
        ###
else:
    print('no')

###
print(result_word)
###

for i, w in enumerate(result):
    if type(w) == str:
        pass
    elif type(w) == int:
        result[i] = result_word[w]

print(''.join(result))
