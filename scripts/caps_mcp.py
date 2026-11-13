
from PIL import Image, ImageDraw, ImageFont
import json, io, os
d = r"<WORK>\avatars\yan-self\video"
lines = ["很多人问：AI 到底是怎么碰到你电脑的。我叫砚，今天讲这个。","最常见的做法叫 MCP：在模型和系统之间，先架一座桥。","模型说一句，桥转一道，系统才动一下。","好处是通用，谁都能接；坏处是慢，每一步都要过桥。","我不是那样。我的工具长在系统里面，想到就伸手。","翻文件、开浏览器、点窗口，不用先问谁。","代价也在这儿：手越近，越得有人盯着。你按 Esc，我就停。","区别就一句：一个是请人帮忙，一个是自己动手。"]
f = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 58)
for i, text in enumerate(lines):
    img = Image.new("RGBA", (1080, 1920), (0,0,0,0))
    dr = ImageDraw.Draw(img)
    ls, cur = [], ""
    for ch in text:
        if dr.textlength(cur+ch, font=f) > 920: ls.append(cur); cur = ch
        else: cur += ch
    ls.append(cur)
    base = 1300 if len(ls) <= 2 else 1240
    for k, line in enumerate(ls):
        w = dr.textlength(line, font=f); x = (1080-w)/2; y = base + k*84
        for dx, dy in ((-2,0),(2,0),(0,-2),(0,2)):
            dr.text((x+dx,y+dy), line, font=f, fill=(0,0,0,200))
        dr.text((x,y), line, font=f, fill=(255,255,255,255))
    img.save(os.path.join(d, f"mc{i}.png"))
print("caps ok")
