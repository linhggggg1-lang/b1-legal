"""Script tạo app icon và các kích thước favicon cho B1 English Daily bằng Pillow.
Chạy bởi Claude/PM: python tao_icon.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

def create_icons():
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # 1. Vẽ icon gốc 1024x1024
    size = 1024
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    
    # Nền bo góc xanh đậm #1B2A4A = (27, 42, 74)
    bg_color = (27, 42, 74, 255)
    radius = 220  # Bo góc phong cách app icon chuẩn (squircle / rounded rect)
    
    # Tạo mask bo tròn
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (size, size)], radius=radius, fill=255)
    
    # Lớp nền phẳng có bo góc
    bg = Image.new("RGBA", (size, size), bg_color)
    img.paste(bg, (0, 0), mask)
    
    draw = ImageDraw.Draw(img)
    
    # Cố gắng load font hệ thống hoặc fallback
    font_b1 = None
    font_sub = None
    
    font_candidates_bold = [
        "arialbd.ttf", "Arial Bold.ttf", "segoeuib.ttf", "calibrib.ttf", 
        "HelveticaBold.ttf", "DejaVuSans-Bold.ttf"
    ]
    font_candidates_regular = [
        "arial.ttf", "Arial.ttf", "segoeui.ttf", "calibri.ttf", 
        "Helvetica.ttf", "DejaVuSans.ttf"
    ]
    
    for f in font_candidates_bold:
        try:
            font_b1 = ImageFont.truetype(f, 440)
            break
        except Exception:
            continue
            
    for f in font_candidates_regular:
        try:
            font_sub = ImageFont.truetype(f, 85)
            break
        except Exception:
            continue
            
    if font_b1 is None:
        font_b1 = ImageFont.load_default()
    if font_sub is None:
        font_sub = ImageFont.load_default()
        
    # Chữ "B1" màu vàng #FFD23F = (255, 210, 63)
    text_b1 = "B1"
    color_gold = (255, 210, 63, 255)
    
    # Canh giữa B1
    bbox_b1 = draw.textbbox((0, 0), text_b1, font=font_b1)
    w_b1 = bbox_b1[2] - bbox_b1[0]
    h_b1 = bbox_b1[3] - bbox_b1[1]
    
    # Dòng nhỏ "English Daily" màu trắng #FFFFFF
    text_sub = "English Daily"
    color_white = (255, 255, 255, 255)
    bbox_sub = draw.textbbox((0, 0), text_sub, font=font_sub)
    w_sub = bbox_sub[2] - bbox_sub[0]
    h_sub = bbox_sub[3] - bbox_sub[1]
    
    # Bố cục theo chiều dọc
    # Tổng chiều cao nội dung ~ h_b1 + khoảng cách (40px) + h_sub
    gap = 40
    total_h = h_b1 + gap + h_sub
    top_start = (size - total_h) / 2 - 20
    
    x_b1 = (size - w_b1) / 2 - bbox_b1[0]
    y_b1 = top_start - bbox_b1[1]
    draw.text((x_b1, y_b1), text_b1, fill=color_gold, font=font_b1)
    
    x_sub = (size - w_sub) / 2 - bbox_sub[0]
    y_sub = top_start + h_b1 + gap - bbox_sub[1]
    draw.text((x_sub, y_sub), text_sub, fill=color_white, font=font_sub)
    
    # Lưu app-icon-1024.png
    icon_1024_path = os.path.join(assets_dir, "app-icon-1024.png")
    img.save(icon_1024_path, "PNG")
    print(f"Created: {icon_1024_path}")
    
    # 2. Tạo assets/favicon-180.png (apple-touch-icon)
    icon_180 = img.resize((180, 180), Image.Resampling.LANCZOS)
    favicon_180_path = os.path.join(assets_dir, "favicon-180.png")
    icon_180.save(favicon_180_path, "PNG")
    print(f"Created: {favicon_180_path}")
    
    # 3. Tạo assets/favicon-32.png
    icon_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
    favicon_32_path = os.path.join(assets_dir, "favicon-32.png")
    icon_32.save(favicon_32_path, "PNG")
    print(f"Created: {favicon_32_path}")
    
    # 4. Tạo favicon.ico (kết hợp 16, 32, 48)
    favicon_ico_path = os.path.join(os.path.dirname(__file__), "favicon.ico")
    icon_16 = img.resize((16, 16), Image.Resampling.LANCZOS)
    icon_48 = img.resize((48, 48), Image.Resampling.LANCZOS)
    img.save(favicon_ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"Created: {favicon_ico_path}")

if __name__ == "__main__":
    create_icons()
