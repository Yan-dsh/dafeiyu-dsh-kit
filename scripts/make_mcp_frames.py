
from PIL import Image, ImageDraw, ImageFont
import math, os

d = r"<WORK>\avatars\yan-self\video\mcpframes"
os.makedirs(d, exist_ok=True)
W, H, FPS, DUR = 1080, 1920, 15, 46.6
N = int(FPS * DUR)
F_TITLE = "C:\Windows\Fonts\msyhbd.ttc"
F_BODY = "C:\Windows\Fonts\msyh.ttc"
ft = lambda s: ImageFont.truetype(F_TITLE, s)
fb = lambda s: ImageFont.truetype(F_BODY, s)

BG1 = (11, 18, 32)
BG2 = (18, 28, 48)
CYAN = (90, 200, 255)
BLUE = (60, 120, 220)
WHITE = (240, 246, 255)
GREY = (120, 140, 170)
AMBER = (255, 190, 90)

def bg(t):
    img = Image.new("RGB", (W, H), BG1)
    dr = ImageDraw.Draw(img)
    for y in range(0, H, 6):
        k = y / H
        c = (int(11 + 12 * k), int(18 + 16 * k), int(32 + 24 * k))
        dr.rectangle([0, y, W, y + 6], fill=c)
    # 网格
    off = int((t * 12) % 60)
    for x in range(-60, W + 60, 60):
        dr.line([(x + off, 0), (x + off, H)], fill=(255, 255, 255, 0), width=1)
    return img

def grid(img, t):
    dr = ImageDraw.Draw(img)
    off = int((t * 14) % 72)
    for x in range(-72, W + 72, 72):
        dr.line([(x + off, 0), (x + off, H)], fill=(28, 44, 70), width=1)
    for y in range(0, H, 72):
        dr.line([(0, y), (W, y)], fill=(28, 44, 70), width=1)
    return img

def rrect(dr, box, r, fill=None, outline=None, w=3):
    dr.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=w)

def center(dr, text, y, font, fill=WHITE):
    w = dr.textlength(text, font=font)
    dr.text(((W - w) / 2, y), text, font=font, fill=fill)

def scene_title(img, t, local):
    dr = ImageDraw.Draw(img)
    a = min(1, local / 0.8)
    center(dr, "AI 是怎么碰到你电脑的", 560, ft(74), (int(240*a), int(246*a), 255))
    center(dr, "MCP 与「长在系统里的手」", 690, fb(44), (int(120*a), int(180*a), 220))
    return img

def arrow(dr, x1, y1, x2, y2, color, w=4):
    dr.line([(x1, y1), (x2, y2)], fill=color, width=w)
    ax, ay = x2, y2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    dr.polygon([(ax, ay), (ax - ux*18 + px*9, ay - uy*18 + py*9), (ax - ux*18 - px*9, ay - uy*18 - py*9)], fill=color)

def scene_bridge(img, t, local):
    """模型 -> 桥 -> 系统，点循环走"""
    dr = ImageDraw.Draw(img)
    boxes = [("模型", (240, 430, 800, 600)), ("桥 MCP", (240, 700, 800, 860)), ("你的系统", (240, 960, 800, 1130))]
    for name, box in boxes:
        rrect(dr, box, 24, fill=(20, 32, 54), outline=(70, 110, 170), w=3)
        f = ft(52)
        w = dr.textlength(name, font=f)
        dr.text(((box[0]+box[2]-w)/2, (box[1]+box[3])/2 - 34), name, font=f, fill=WHITE)
    cyc = 2.6
    p = (local % cyc) / cyc
    def lerp(a, b, u): return a + (b - a) * u
    if p < 0.4:
        u = p / 0.4; x = 520; y = lerp(608, 692, u)
    elif p < 0.8:
        u = (p - 0.4) / 0.4; x = 520; y = lerp(868, 952, u)
    else:
        x, y = 520, 952
    dr.ellipse([x-14, y-14, x+14, y+14], fill=CYAN)
    dr.ellipse([x-26, y-26, x+26, y+26], outline=(60, 180, 240), width=2)
    labels = [(620, "请求"), (890, "转接"), (1150, "动作")]
    for (yy, s), on in zip(labels, [p < 0.4, 0.4 <= p < 0.8, p >= 0.8]):
        col = CYAN if on else (90, 110, 140)
        dr.text((846, yy - 26), s, font=fb(40), fill=col)
    return img

def scene_hand(img, t, local):
    dr = ImageDraw.Draw(img)
    rrect(dr, (200, 900, 880, 1140), 26, fill=(20, 32, 54), outline=(70, 110, 170), w=3)
    f = ft(46)
    w = dr.textlength("系统内部", font=f)
    dr.text(((200+880-w)/2, 1000), "系统内部", font=f, fill=WHITE)
    p = min(1, (local % 2.4) / 1.2)
    palm_top = 900 - int(230 * p)
    # 手掌
    dr.rounded_rectangle([470, palm_top, 600, 910], radius=34, fill=(70, 150, 220))
    # 四指
    for i, dx in enumerate((-58, -6, 46, 96)):
        h = 120 + 26 * (i % 2)
        dr.rounded_rectangle([500 + dx, palm_top - h, 542 + dx, palm_top + 40], radius=21, fill=(96, 178, 242))
    # 拇指
    dr.rounded_rectangle([600, palm_top + 30, 668, palm_top + 92], radius=24, fill=(96, 178, 242))
    rrect(dr, (620, 470, 900, 650), 14, fill=(28, 44, 72), outline=(120, 200, 255), w=3)
    dr.text((650, 520), "窗口", font=fb(40), fill=(200, 230, 255))
    if p > 0.8:
        # 光标
        cx, cy = 700, 600
        dr.polygon([(cx, cy), (cx, cy+34), (cx+10, cy+26), (cx+18, cy+40), (cx+26, cy+34), (cx+18, cy+20), (cx+30, cy+20)], fill=AMBER)
    return img

def scene_compare(img, t, local):
    dr = ImageDraw.Draw(img)
    hi = int(local / 2.2) % 2
    cols = [((110, 500), "MCP", "每步都要过桥", (60, 140, 220)), ((600, 500), "我", "手长在系统里", (255, 190, 90))]
    for (x, y), name, desc, col in cols:
        on = (0 if name == "MCP" else 1) == hi
        rrect(dr, (x, y, x + 360, y + 420), 24, fill=(20, 32, 54) if not on else (30, 52, 82), outline=col, w=4 if on else 2)
        fname = ft(64)
        w = dr.textlength(name, font=fname)
        dr.text((x + (360 - w) / 2, y + 90), name, font=fname, fill=col if on else (140, 160, 190))
        f2 = fb(34)
        ls = [desc[i:i+6] for i in range(0, len(desc), 6)]
        for i, s in enumerate(ls):
            w2 = dr.textlength(s, font=f2)
            dr.text((x + (360 - w2) / 2, y + 220 + i * 52), s, font=f2, fill=(210, 226, 245))
    # ESC 键
    blink = (math.sin(local * 3) + 1) / 2
    rrect(dr, (440, 1010, 640, 1100), 16, fill=(40, 30, 40), outline=(255, 120, 120), w=3)
    center(dr, "ESC", 1030, ft(40), (int(255*blink), 140, 140))
    return img

def chrome(img, t):
    dr = ImageDraw.Draw(img)
    if t < 7: chap = "00 / 开场"
    elif t < 22: chap = "01 / 桥 MCP"
    elif t < 31: chap = "02 / 长在系统里的手"
    else: chap = "03 / 区别"
    dr.text((72, 96), chap, font=fb(38), fill=(120, 160, 205))
    dr.text((72, 150), "砚 · 科普 01", font=fb(28), fill=(80, 110, 150))
    # 进度条
    dr.rectangle([72, 1856, 1008, 1866], fill=(30, 44, 66))
    w = int(936 * (t / DUR))
    dr.rectangle([72, 1856, 72 + w, 1866], fill=CYAN)
    return img

for n in range(N):
    t = n / FPS
    img = bg(t)
    grid(img, t)
    if t < 7:
        img = scene_title(img, t, t)
    elif t < 22:
        img = scene_bridge(img, t, t - 7)
    elif t < 31:
        img = scene_hand(img, t, t - 22)
    else:
        img = scene_compare(img, t, t - 31)
    img = chrome(img, t)
    img.save(os.path.join(d, f"{n:04d}.png"))
print("frames", N)
