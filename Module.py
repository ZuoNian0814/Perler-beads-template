import os, json
from PIL import ImageDraw, Image
import math


CROSS = "cross"
BLOCK = "block"
cols_path = "col_mapping"


def hex_to_rgb(color):
    s = color.lstrip('#')
    return tuple([int(s[i:i + 2], 16) for i in (0, 2, 4)])

def dis3d(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

def img_interval_sampling(img, step=2):
    w, h = img.size
    new_img = Image.new('RGBA', (int(w//step), int(h//step)), (0, 0, 0, 0))
    for y in range(int(h//step)):
        for x in range(int(w//step)):
            pixel_col = img.getpixel((int(x * step), int(y * step)))
            new_img.putpixel((int(x), int(y)), pixel_col)
    return new_img

def stroke_cross(img, stroke_thickness=1, color='#ffffff'):
    st = stroke_thickness
    w, h = img.size
    new_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(new_img)
    for y in range(h):
        for x in range(w):
            pixel_col = img.getpixel((x, y))
            if pixel_col[-1] == 0:
                continue
            draw.line((x-st, y, x+st, y), fill=color, width=1)
            draw.line((x, y-st, x, y+st), fill=color, width=1)

    for y in range(h):
        for x in range(w):
            pixel_col = img.getpixel((x, y))
            if pixel_col[-1] != 0:
                new_img.putpixel((x, y), pixel_col)
    return new_img

def stroke_block(img, stroke_thickness=1, color='#ffffff'):
    st = stroke_thickness
    w, h = img.size
    new_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(new_img)
    for y in range(h):
        for x in range(w):
            pixel_col = img.getpixel((x, y))
            if pixel_col[-1] == 0:
                continue
            draw.rectangle((x-st, y-st, x+st, y+st), fill=color, width=1)

    for y in range(h):
        for x in range(w):
            pixel_col = img.getpixel((x, y))
            if pixel_col[-1] != 0:
                new_img.putpixel((x, y), pixel_col)
    return new_img

def get_all_brand():
    # 读取已有的映射表
    brand_list = []
    for f in os.listdir(cols_path):
        if  f.split('.')[1] == 'json':
            brand = f.split('.')[0]
            brand_list.append(brand)
    return brand_list

class PerlerBeads:
    def __init__(self):
        self.col_index_rgb = None
        self.id_to_col = {}
        self.progress = 0.0

    def get_drawing(self, img, pixel=30, block_col=None, tolerance=0, stroke_color='#ffffff'):
        w, h = img.size
        new_img = Image.new("RGBA", (w*pixel, h*pixel), (0, 0, 0, 0))
        clean_img = Image.new("RGBA", (w*pixel, h*pixel), (0, 0, 0, 0))
        draw = ImageDraw.Draw(new_img)
        draw_ = ImageDraw.Draw(clean_img)
        count = {"sum": 0}
        progress = 0
        for y in range(h):
            for x in range(w):
                progress += 1
                self.progress = progress / (w * h)
                pixel_col = img.getpixel((x, y))
                if len(pixel_col) == 4 and pixel_col[-1] == 0:
                    continue
                elif block_col and dis3d(pixel_col[:3], block_col) < tolerance:
                    continue

                match_col = None
                max_sim = 1000.0
                for k, v in self.col_index_rgb.items():
                    cos_sim = dis3d(pixel_col[:3], k)
                    if max_sim > cos_sim:
                        match_col = k
                        max_sim = cos_sim

                col_name = self.col_index_rgb[match_col]
                if col_name not in count:
                    count[col_name] = 1
                else:
                    count[col_name] += 1
                count['sum'] += 1
                draw.rectangle((x*pixel, y*pixel, (x+1)*pixel, (y+1)*pixel), fill=match_col, outline=stroke_color, width=1)
                draw_.rectangle((x*pixel, y*pixel, (x+1)*pixel, (y+1)*pixel), fill=match_col)
                col_id = col_name.split(' ')[0]

                if dis3d((0, 0, 0), match_col) > dis3d((255, 255, 255), match_col):
                    draw.text((x*pixel+2, y*pixel+5), text=col_id, fill='black', font_size=pixel // 3.4)
                else:
                    draw.text((x*pixel+2, y*pixel+5), text=col_id, fill='white', font_size=pixel // 3.4)
        self.progress = 1.0
        return new_img, clean_img, count

    def run(self, img, brand, sampling=1,
            stroke="cross", stroke_thickness=1, stroke_color='#ffffff',
            pixel=30, block_col=None, tolerance=0, pixel_stroke_color='#ffffff'
        ):

        with open(f"{cols_path}/{brand}.json", encoding='utf-8', mode='r') as f:
            content = f.read()
            col_index = json.loads(content)
        self.col_index_rgb = {}
        for k, v in col_index.items():
            col_arr = hex_to_rgb(k)
            self.col_index_rgb[col_arr] = v

        self.id_to_col = {v: k for k, v in col_index.items()}

        img = img_interval_sampling(img, step=sampling)

        if stroke.lower() == "cross":
            img = stroke_cross(img, stroke_thickness=stroke_thickness, color=stroke_color)
        elif stroke.lower() == "block":
            img = stroke_block(img, stroke_thickness=stroke_thickness, color=stroke_color)
        else:
            raise (ValueError, f"描边类型{stroke}不存在：应该是 cross 或 block.")

        if type(block_col) is str:
            print(block_col)
            block_col = hex_to_rgb(block_col)
        drawing, clean_drawing, count = self.get_drawing(
            img, pixel=pixel, block_col=block_col, tolerance=tolerance, stroke_color=pixel_stroke_color
        )

        return drawing, clean_drawing, count

if __name__ == '__main__':
    img = Image.open("测试图像/大蒜.png")
    w, h = img.size
    print(f"大小：{w}x{h}")

    # 获取品牌列表
    brands = get_all_brand()

    # 品牌名称
    brand = "Artkal"
    pb = PerlerBeads()

    drawing, clean_drawing, count = pb.run(
        # 基本参数
        img=img,                # 图像对象
        brand=brand,            # 品牌名称
        sampling=1,         # 采样间隔

        stroke="cross",             # 拼豆描边类型：cross / block
        stroke_thickness=1,         # 描边厚度
        stroke_color='#ffffff',     # 描边颜色

        pixel=50,                       # 图纸放大倍率（清晰度）
        block_col=None,                 # 抠像颜色，此颜色会被视为透明
        tolerance=0,                    # 容差，视为透明的颜色的容差
        pixel_stroke_color='#ffffff'    # 每个像素块的边界颜色，图纸美观
    )

    drawing.show()