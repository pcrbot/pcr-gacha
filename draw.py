# conding=utf-8
import io
import os
import random
import sys

from flask import Flask, send_file
from PIL import Image

# 抽卡图片在背景图上的位置
PASTE_POSITION = (413, 253)  # 第一张图的粘贴位置
PASTE_SPACING = 290  # 粘贴的图片间距
PASTE_SIZE = 220  # 粘贴的图片大小
SAVE_SIZE = (640, 360)  # 保存的图片大小


def gacha_one(guarantee=False):
    key = random.randint(0, 999)
    if key < 7:
        return 'up'
    # elif key < 10:
    #     return 'sub_up'
    elif key < 25:
        return '3'
    elif key < 205 or guarantee:
        return '2'
    else:
        return '1'


def gacha_pic(path, guarantee=False):
    gacha_rare = gacha_one(guarantee)
    pic_lib = os.listdir(os.path.join(path, gacha_rare))
    pic_name = os.path.join(path, gacha_rare, random.choice(pic_lib))
    pic = Image.open(pic_name)
    return pic


def gen_pic():
    filepath = os.path.dirname(__file__)
    with Image.open(os.path.join(filepath, 'backgroud.jpg')) as result_pic:
        for row in range(2):
            for column in range(5):
                result_one = gacha_pic(
                    path=filepath,
                    guarantee=(row, column) == (1, 4)
                ).resize((PASTE_SIZE, PASTE_SIZE), Image.ANTIALIAS)
                position = (PASTE_POSITION[0]+PASTE_SPACING * column,
                            PASTE_POSITION[1]+PASTE_SPACING * row)
                result_pic.paste(result_one, position)
        pic_bytes = io.BytesIO()
        result_pic = result_pic.resize(SAVE_SIZE, Image.ANTIALIAS)
        result_pic.save(pic_bytes, format='JPEG')
    pic_bytes.seek(0)
    return pic_bytes


app = Flask(__name__)


@app.route('/gacha.jpg')
def _():
    pic = gen_pic()
    response = send_file(pic, mimetype='image/jpeg')
    response.headers['Cache-Control'] = 'max-age=0, no-cache, no-store, must-revalidate'
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
