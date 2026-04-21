import os
import struct

def get_image_size(file_path):
    with open(file_path, 'rb') as f:
        head = f.read(24)
        if len(head) != 24:
            return None
        if head.startswith(b'\x89PNG\r\n\x1a\n'):
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return None
            width, height = struct.unpack('>ii', head[16:24])
            return width, height
        elif head.startswith(b'\xff\xd8'):
            f.seek(0)
            size = 2
            ft = f.read()
            while size < len(ft):
                try:
                    while ft[size] == 0xff:
                        size += 1
                    b = ft[size]
                    size += 1
                    if b >= 0xc0 and b <= 0xc3:
                        return struct.unpack('>HH', ft[size+3:size+7])[::-1]
                    else:
                        size += struct.unpack('>H', ft[size:size+2])[0]
                except Exception:
                    return None
            return None

import glob
path = r"C:\Users\Dell 5490\.gemini\antigravity\brain\35538bdd-7309-4898-9518-c931aa9bc871"
images = glob.glob(os.path.join(path, "*.jpg")) + glob.glob(os.path.join(path, "*.png"))
for img in images:
    size = get_image_size(img)
    print(f"{os.path.basename(img)}: {size}")
