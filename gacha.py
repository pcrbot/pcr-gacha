# conding=utf-8
import io
import os
import random
from functools import lru_cache

from cachetools import TTLCache, cached
from flask import Flask, send_file
from PIL import Image

# 抽卡图片在背景图上的位置
PASTE_POSITION = (120, 73)  # 第一张图的粘贴位置
PASTE_SPACING = 84  # 粘贴的图片间距
PASTE_SIZE = 64  # 粘贴的图片大小
SAVE_SIZE = (640, 360)  # 保存的图片大小

_basepath = os.path.dirname(__file__)
_background = Image.open(os.path.join(_basepath, 'background.jpg')).resize(
    SAVE_SIZE, Image.ANTIALIAS)


@lru_cache(maxsize=256)
def get_pillow(*filepath):
    pic = Image.open(os.path.join(_basepath, *filepath))
    pic = pic.resize((PASTE_SIZE, PASTE_SIZE), Image.ANTIALIAS)
    return pic


@cached(cache=TTLCache(maxsize=4, ttl=300))
def get_chara_list(chara_type):
    return os.listdir(os.path.join(_basepath, 'icons', chara_type))


def gacha_one(guarantee=False):
    key = random.randint(0, 999)
    if key < 7:
        return 'up'
    elif key < 25:
        return '3'
    elif key < 205 or guarantee:
        return '2'
    else:
        return '1'


def gacha_pic(guarantee=False):
    gacha_rare = gacha_one(guarantee)
    pic_lib = get_chara_list(gacha_rare)
    pic_name = random.choice(pic_lib)
    pic = get_pillow('icons', gacha_rare, pic_name)
    return pic


def gen_pic():
    result_pic = _background.copy()

    for row in range(2):
        for column in range(5):
            result_one = gacha_pic(
                guarantee=(row, column) == (1, 4)
            )
            position = (PASTE_POSITION[0]+PASTE_SPACING * column,
                        PASTE_POSITION[1]+PASTE_SPACING * row)
            result_pic.paste(result_one, position)

    pic_bytes = io.BytesIO()
    result_pic.save(pic_bytes, format='JPEG')
    pic_bytes.seek(0)
    return pic_bytes


app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def gacha(path):
    pic = gen_pic()
    response = send_file(pic, mimetype='image/jpeg')
    response.headers['Cache-Control'] = 'max-age=0, no-cache, no-store, must-revalidate'
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
