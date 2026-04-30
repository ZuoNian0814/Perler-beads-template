import json
from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from Module import get_all_brand, PerlerBeads
import os, sys
import time
import re
from threading import Timer
import socket
import webbrowser
from werkzeug.serving import is_running_from_reloader

# 检测端口占用
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

# 获取可用端口
def get_available_port(start=5000):
    port = start
    while is_port_in_use(port):
        port += 1
    return port

# 打开浏览器
def open_browser(port):
    webbrowser.open(f"http://127.0.0.1:{port}/")

draw_path = "static/result/drawing.png"
clean_path = "static/result/clean.png"
count_path = "static/result/count.json"
pb = PerlerBeads()


os.makedirs("static/result", exist_ok=True)

# 获取 EXE/脚本 所在的真实目录
BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
# 强制指定模板/静态文件路径（解决打包后找不到文件）
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

@app.route('/')
def index():
    brands = get_all_brand()
    return render_template("index.html", brands=brands)


@app.route('/generate', methods=["POST"])
def generate():
    brand = request.form.get("brand")
    sampling = int(request.form.get("sampling"))
    stroke = request.form.get("stroke_type")
    stroke_thickness = int(request.form.get("stroke_thickness"))
    stroke_color = request.form.get("stroke_color")
    pixel = int(request.form.get("pixel"))
    pixel_stroke_color = request.form.get("pixel_stroke_color")
    tolerance = int(request.form.get("tolerance"))

    block_enable = request.form.get("block_enable")
    block_col = request.form.get("block_color") if block_enable else None

    img_file = request.files.get("image")
    if not img_file:
        return jsonify({"error": "请上传图片"}), 400

    img = Image.open(img_file.stream)

    # 调用你的核心模块
    drawing, clean_drawing, count = pb.run(
        img=img,
        brand=brand,
        sampling=sampling,
        stroke=stroke,
        stroke_thickness=stroke_thickness,
        stroke_color=stroke_color,
        pixel=pixel,
        block_col=block_col,
        tolerance=tolerance,
        pixel_stroke_color=pixel_stroke_color
    )

    drawing.save(draw_path)
    clean_drawing.save(clean_path)
    count['brand'] = brand
    with open(count_path, mode='w', encoding='utf-8') as f:
        f.write(json.dumps(count, ensure_ascii=False, indent=4))

    total_count = count.get("sum", 0)
    table_count = {k: v for k, v in count.items() if k != "sum" and k != "brand"}
    count_data = [{"id": k, "count": v} for k, v in table_count.items()]

    ts = int(time.time())
    return jsonify({
        "drawing_url": f"/{draw_path}?t={ts}",
        "clean_url": f"/{clean_path}?t={ts}",
        "count_data": count_data,
        "total_count": total_count
    })


def char_len(s: str) -> int:
    """
    统计字符串长度：中文字符视为2个字符，其他字符视为1个
    :param s: 输入字符串
    :return: 统计后的总长度
    """
    total = 0
    for char in s:
        # 判断是否为中文字符
        if '\u4e00' <= char <= '\u9fff':
            total += 2
        else:
            total += 1
    return total

def fill_char(s, n, fill=' ', top=False):
    if top:
        return (n - char_len(s)) * fill + s
    else:
        return s + (n - char_len(s)) * fill

def get_first_number(key):
    match = re.search(r'\d+', key)
    return int(match.group()) if match else 0

@app.route('/export', methods=["POST"])
def export():
    drawing = Image.open(draw_path)
    w, h = drawing.size
    clean_drawing = Image.open(clean_path)
    with open(count_path, mode='r', encoding='utf-8') as f:
        count_json = json.loads(f.read())

    title_size = int(w * 0.06)
    font_size = int(w * 0.02)

    table_count = {k: v for k, v in count_json.items() if k != "sum" and k != "brand"}
    bg = Image.new("RGB", (int(w * 1.2), int(max((1.5 * h + title_size + 100), h + (len(table_count)+1) * (font_size + 5) + (title_size + 100)))), 'black')
    draw = ImageDraw.Draw(bg)

    y = 25
    font_t = ImageFont.truetype("static/fusion-pixel-12px-monospaced-zh_hans.ttf", title_size)
    font = ImageFont.truetype("static/fusion-pixel-12px-monospaced-zh_hans.ttf", font_size)

    draw.text((y, y), f'Perler Beads - {count_json["brand"]}', fill='white', font=font_t)
    y += (title_size + 5)
    bg.paste(drawing, (int(0.1 * w), y), mask=drawing)
    y += (h + 50)
    clean_drawing = clean_drawing.resize((w // 2, h // 2))
    bg.paste(clean_drawing, (int(w * 1.2 // 2 - w // 2), y), mask=clean_drawing)
    text_x = int(w * 1.2 // 2) + 20
    max_len = max([char_len(m) for m in table_count])
    table_count = dict(reversed(sorted(table_count.items(), key=lambda x: get_first_number(x[0]), reverse=True)))
    for k, v in table_count.items():
        index_dict = pb.id_to_col
        draw.rectangle((text_x, y, text_x+font_size, y+font_size), fill=index_dict[k])
        draw.text((text_x+font_size+5, y), f"{fill_char(k, max_len)} {v}", fill='white', font=font)
        y += font_size + 5

    draw.text((text_x + 5, y), f"Sum: {count_json["sum"]}", fill='white', font=font)

    # 创建内存流存储图片
    img_stream = BytesIO()
    # 保存PIL图片到流
    bg.save(img_stream, format="PNG")
    # 重置流指针到开头
    img_stream.seek(0)

    # 返回图片，浏览器自动下载
    return send_file(
        img_stream,
        mimetype="image/png",
        as_attachment=True,
        download_name="拼豆图纸.png"
    )

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    # 核心：只在【主进程】执行一次，屏蔽重载子进程
    if not is_running_from_reloader():
        port = get_available_port(5000)
        Timer(1, open_browser, args=(port,)).start()
    else:
        port = 5000  # 子进程不占用新端口

    app.run(host='127.0.0.1', port=port, debug=True)