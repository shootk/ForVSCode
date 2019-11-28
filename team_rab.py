import urllib.request
import time
import random


def query(url):
    res = urllib.request.urlopen(url)
    return res.read()


token = "SdLl4d1j5ovyzxe9oTa4oGlTjhoQhEcp"
alphabets = 'abcd'
two_word = []
for i in range(4):
    for j in range(4):
        two_word.append(alphabets[i] + alphabets[j])

score = [0, 0, 0, 0, 0, 0]
words = [''] * 6
last_words = []
s = ''
for i in range(6):
    while True:
        w = ''
        for j in range(0, 8):
            r = random.randint(0, 3)
            w += alphabets[r]
        if w not in words:
            words[i] = w
            last_words.append(w)

            url = "https://runner.team-lab.com/q?token=%s&str=%s" % (token, w)
            result = query(url)
            time.sleep(0.99)
            score[i] = result
            break

while True:
    while True:
        w = ''
        for j in range(0, 8):
            r = random.randint(0, 3)
            w += alphabets[r]

        if w not in last_words:
            last_words.append(w)
            url = "https://runner.team-lab.com/q?token=%s&str=%s" % (token, w)
            result = query(url)
            time.sleep(1)
            if result >= min(score):
                words[score.index(min(score))] = w
                score[score.index(min(score))] = result
            break

    for i in range(16):
        r = ''.join(words) + two_word[i]
        url = "https://runner.team-lab.com/q?token=%s&str=%s" % (token, r)
        time.sleep(1)
        result = query(url)
        score.sort()
        print(result)
