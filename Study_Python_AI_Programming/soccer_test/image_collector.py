# 顔認識する対象を決定（検索ワードを入力）
import numpy as np
import cv2
from bs4 import BeautifulSoup
import requests
from urllib import parse
import json
import os


SearchName = ["Messi", "Ronaldo", "Neymar", "Mbappe"]
# 画像の取得枚数の上限
ImgNumber = 600
# CNNで学習するときの画像のサイズを設定（サイズが大きいと学習に時間がかかる）
ImgSize = (250, 250)
input_shape = (250, 250, 3)

# オリジナル画像用のフォルダ
os.makedirs("./Original", exist_ok=True)
# 顔の画像用のフォルダ
os.makedirs("./Face", exist_ok=True)
# ImgSizeで設定したサイズに編集された顔画像用のフォルダ
os.makedirs("./FaceEdited", exist_ok=True)
# テストデータを入れる用のフォルダ
os.makedirs("./test", exist_ok=True)


class Google:
    def __init__(self):
        self.GOOGLE_SEARCH_URL = 'https://www.google.co.jp/search'
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'})

    def Search(self, keyword, type='text', maximum=1000):
        '''Google検索'''
        print('Google', type.capitalize(), 'Search :', keyword)
        result, total = [], 0
        query = self.query_gen(keyword, type)
        while True:
            # 検索
            html = self.session.get(next(query)).text
            links = self.get_links(html, type)

            # 検索結果の追加
            if not len(links):
                print('-> No more links')
                break
            elif len(links) > maximum - total:
                result += links[:maximum - total]
                break
            else:
                result += links
                total += len(links)

        print('-> 結果', str(len(result)), 'のlinksを取得しました')
        return result

    def query_gen(self, keyword, type):
        '''検索クエリジェネレータ'''
        page = 0
        while True:
            if type == 'text':
                params = parse.urlencode({
                    'q': keyword,
                    'num': '100',
                    'filter': '0',
                    'start': str(page * 100)})
            elif type == 'image':
                params = parse.urlencode({
                    'q': keyword,
                    'tbm': 'isch',
                    'filter': '0',
                    'ijn': str(page)})

            yield self.GOOGLE_SEARCH_URL + '?' + params
            page += 1

    def get_links(self, html, type):
        '''リンク取得'''
        soup = BeautifulSoup(html, 'lxml')
        if type == 'text':
            elements = soup.select('.rc > .r > a')
            links = [e['href'] for e in elements]
        elif type == 'image':
            elements = soup.select('.rg_meta.notranslate')
            jsons = [json.loads(e.get_text()) for e in elements]
            links = [js['ou'] for js in jsons]
        return links


# 画像のURLをgoogle検索から取得する
# インスタンス作成
google = Google()
for name in SearchName:
    # 画像検索
    ImgURLs = google.Search(name, type='image', maximum=ImgNumber)
    # 保存先のディレクトリ作成
    os.makedirs("./Original/" + str(name), exist_ok=True)

    # Originalファイルに画像を保存する
    for i, target in enumerate(ImgURLs):  # ImgURLsからtargetに入れる
        try:
            re = requests.get(target, allow_redirects=False)
            with open("./Original/" + str(name) + '/' + str(i) + '.jpg', 'wb') as f:  # imgフォルダに格納
                f.write(re.content)  # .contentにて画像データとして書き込む
        except requests.exceptions.ConnectionError:
            continue
        except UnicodeEncodeError:
            continue
        except UnicodeError:
            continue
        except IsADirectoryError:
            continue

print("保存完了しました")  # 確認


# OpenCVのデフォルトの分類器のpath。(https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xmlのファイルを使う)
cascade_path = '　自分のhaarcascade_frontalface_default.xmlのパスを入力'
# 例
#cascade_path = './opencv-master/data/haarcascades/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascade_path)

for name in SearchName:
    # 画像データのあるディレクトリ
    input_data_path = "./Original/" + str(name)
    # 切り抜いた画像の保存先ディレクトリを作成
    os.makedirs("./Face/" + str(name) + "_face", exist_ok=True)
    save_path = "./Face/" + str(name) + "_face/"
    # 収集した画像の枚数(任意で変更)
    image_count = ImgNumber
    # 顔検知に成功した数(デフォルトで0を指定)
    face_detect_count = 0

    print("{}の顔を検出し切り取りを開始します。".format(name))
    # 集めた画像データから顔が検知されたら、切り取り、保存する。
    for i in range(image_count):
        img = cv2.imread(input_data_path + '/' +
                         str(i) + '.jpg', cv2.IMREAD_COLOR)
        if img is None:
            print('image' + str(i) + ':NoFace')
        else:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face = faceCascade.detectMultiScale(gray, 1.1, 3)
            if len(face) > 0:
                for rect in face:
                    # 顔認識部分を赤線で囲み保存(今はこの部分は必要ない)
                    # cv2.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 0,255), thickness=1)
                    # cv2.imwrite('detected.jpg', img)
                    x = rect[0]
                    y = rect[1]
                    w = rect[2]
                    h = rect[3]
                    cv2.imwrite(
                        save_path + 'cutted' + str(face_detect_count) + '.jpg', img[y:y + h, x:x + w])
                    face_detect_count = face_detect_count + 1
            else:
                print('image' + str(i) + ':NoFace')

print("顔画像の切り取り作業、正常に動作しました。")
