
from PIL import Image
import os
src = r"<WORK>\avatars\yan-self\avatar-ideo\yan-avatar-final.png"
out_dir = r"<WORK>\avatars\yan-self\avatar-ideo"
im = Image.open(src).convert("RGB")
for size, name in [(460, "yan-avatar-460.jpg"), (800, "yan-avatar-800.jpg"), (1024, "yan-avatar-1024.jpg")]:
    im2 = im.resize((size, size), Image.LANCZOS)
    p = os.path.join(out_dir, name)
    q = 92
    while True:
        im2.save(p, "JPEG", quality=q, optimize=True)
        if os.path.getsize(p) <= 900 * 1024 or q <= 60:
            break
        q -= 6
    print(name, os.path.getsize(p) // 1024, "KB", "q=" + str(q))
