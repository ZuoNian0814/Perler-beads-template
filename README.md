# Perler-beads-template
A local web mini program that automatically generates bean paste templates / 自动生成拼豆模板的本地web小程序

![项目Logo](icon.ico)

# 🎨 像素画转拼豆图纸生成工具
# 🎨 Pixel Art to Perler Bead Pattern Generator
开源免费、无需复杂配置，一键把各类图片转换成拼豆专用高清图纸，自动匹配拼豆色号、统计耗材用量，支持多品牌拼豆色卡适配，手工爱好者必备工具✨
Open-source, free, and easy to use. Convert any image to high-definition perler bead patterns with one click. Automatically match bead colors, count material usage, and support multi-brand color cards—an essential tool for craft lovers✨

---

## ✨ 核心功能
## ✨ Core Features
1. **全类型图片兼容**
   完美像素画、普通照片、模糊像素画、抠图素材，通通能转
1. **All Image Types Supported**
   Works with perfect pixel art, regular photos, blurry pixel art, and cutout materials
2. **智能颜色匹配**
   基于RGB三维距离计算，自动匹配最贴合的拼豆官方色号
2. **Smart Color Matching**
   Automatically match the closest official bead colors using 3D RGB distance calculation
3. **高清图纸输出**
   带色号标注、透明背景，可直接打印使用
3. **High-Def Pattern Output**
   Labeled with color codes, transparent background, ready to print
4. **自动用量统计**
   精准计算总拼豆数+单色系用量，备货零浪费
4. **Auto Usage Count**
   Accurately calculate total beads and per-color usage for zero waste
5. **双模式描边美化**
   十字描边/块状描边，让图案轮廓更清晰
5. **Dual Stroke Beautification**
   Cross stroke / block stroke for clearer pattern outlines
6. **多品牌色卡扩展**
   支持自定义添加拼豆品牌，适配所有主流规格
6. **Multi-Brand Color Card Expansion**
   Support custom bead brands, compatible with all mainstream standards

---

## 🚀 详细使用步骤
## 🚀 Detailed Usage Steps
### 一、完美像素画转换（直接生成）
### 1. Perfect Pixel Art Conversion (Direct Generate)
1. 准备清晰的像素画图片（建议无背景）
2. 导入图片后，程序逐像素读取颜色
3. 自动匹配拼豆色卡，绘制色块并标注色号
4. 导出高清图纸，同时生成颜色用量清单
5. 直接打印图纸，对照色号拼搭即可
1. Prepare a clear pixel art image (background removal recommended)
2. Import the image; the program reads colors pixel by pixel
3. Automatically match bead color cards, draw blocks, and label color codes
4. Export high-def pattern and generate color usage list
5. Print directly and follow the color codes to assemble

### 二、普通图片转换（间隔采样）
### 2. Regular Image Conversion (Interval Sampling)
1. 导入非像素风格的普通图片
2. 程序自动对图片进行间隔采样，简化为像素格
3. 采样后自动匹配拼豆颜色，生成标准图纸
4. 可调整采样密度，优化图案清晰度
5. 导出图纸与用量数据，完成转换
1. Import a non-pixel regular image
2. The program automatically samples the image at intervals and simplifies to pixels
3. Auto-match bead colors after sampling and generate standard pattern
4. Adjust sampling density to optimize clarity
5. Export pattern and usage data to finish conversion

### 三、不完美像素画转换（精细化处理）
### 3. Imperfect Pixel Art Conversion (Refined Processing)
1. 导入大尺寸、边缘模糊的像素画
2. 根据图片尺寸设置采样间隔（推荐8/12/16/20）
3. 程序优化像素细节，规整图案网格
4. 颜色匹配+图纸绘制+用量统计一站式完成
5. 导出最终可用的拼豆图纸
1. Import large, blurry-edge pixel art
2. Set sampling interval based on image size (8/12/16/20 recommended)
3. The program optimizes pixel details and regularizes the grid
4. All-in-one: color matching, pattern drawing, and usage counting
5. Export the final usable perler bead pattern

### 四、图纸描边美化（提升辨识度）
### 4. Pattern Stroke Beautification (Improve Recognition)
1. 适用于已抠图的卡通/人物/图案素材
2. 选择**十字描边**：用线条勾勒像素边缘
3. 选择**块状描边**：用色块包裹像素轮廓
4. 设置描边颜色与厚度，强化图案边界
5. 描边完成后生成最终图纸，拼搭更直观
1. For pre-cut cartoon/character/pattern materials
2. Choose **Cross Stroke**: outline pixels with lines
3. Choose **Block Stroke**: wrap pixel outlines with color blocks
4. Set stroke color and thickness to strengthen boundaries
5. Generate final pattern after stroking for easier assembly

---

## 🎯 拼豆色卡格式说明（附示例）
## 🎯 Bead Color Card Format (with Example)
色卡采用**JSON格式**存储，核心规则：
- 键：颜色十六进制编码（带#号）
- 值：拼豆色号 + 颜色名称
Color cards are stored in **JSON format** with core rules:
- Key: Hex color code (with #)
- Value: Bead color code + color name

### 色卡内容示例
### Color Card Example
```json
{
  "#FFFFFF": "#S01 White",
  "#EFEFEF": "#S77 Ghost White",
  "#D1D1D1": "#S78 Ash Gray",
  "#FFD100": "#S27 Yellow",
  "#BA0C2F": "#S34 Red",
  "#000000": "#S13 Black",
  "#249E6B": "#S20 Green",
  "#41B6E6": "#S10 baby Blue"
}
```

---

## 📊 颜色用量统计示例
## 📊 Color Usage Count Example
转换完成后，程序会自动输出用量数据，格式清晰易懂：
After conversion, the program automatically outputs usage data in a clear format:
```
总拼豆数量：4096
#S115 Mossy Green：1153
#S148 Mocha：373
#S15 Redwood：331
#S01 White：183
#S68 Tan：301
```
```
Total Beads: 4096
#S115 Mossy Green: 1153
#S148 Mocha: 373
#S15 Redwood: 331
#S01 White: 183
#S68 Tan: 301
```
直接按统计数量准备对应色号拼豆，无需手动清点。
Prepare beads by the counted quantity—no manual counting needed.

---

## 🆕 添加新拼豆品牌方法
## 🆕 How to Add New Bead Brands
1. 按照上方**色卡格式示例**，整理新品牌的颜色十六进制码、色号、名称
2. 编写完整的色卡JSON文件（格式与示例完全一致）
3. 将色卡文件放入项目对应目录，程序自动识别
4. 切换品牌后，即可用新色卡生成图纸
1. Organize hex color codes, color codes, and names for the new brand following the **color card example** above
2. Create a complete color card JSON file (exact same format as the example)
3. Place the color card file into the project directory; the program recognizes it automatically
4. Switch brands and generate patterns with the new color card

---

## 💡 实用小技巧
## 💡 Useful Tips
1. 图片提前抠除背景，转换后的图纸无杂色、更整洁
1. Remove the image background first for cleaner, clutter-free patterns
2. 大尺寸图片用大采样间隔，小图片用小间隔，效果最优
2. Use larger intervals for big images, smaller intervals for small images for best results
3. 人物/卡通图案建议加描边，轮廓更立体、不易拼错
3. Add strokes to character/cartoon patterns for clearer outlines and fewer mistakes
4. 生成的图纸为透明背景，可自由调整大小后打印
4. Generated patterns have transparent backgrounds; resize freely before printing
5. 色卡可自行修改，适配小众品牌或自定义配色
5. Color cards are editable to fit niche brands or custom color schemes
