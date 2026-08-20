"""
Script to generate high-resolution 1200x630 OpenGraph social share card for ATS MatchProof.
"""

from PIL import Image, ImageDraw, ImageFont


def create_og_image():
    W, H = 1200, 630
    img = Image.new("RGBA", (W, H), (2, 6, 23, 255))  # slate-950 #020617
    draw = ImageDraw.Draw(img)

    # 1. Subtle Background Gradients / Glows
    # Ambient radial gradient top right & bottom left
    for r in range(400, 0, -5):
        alpha = int(22 * (1 - r / 400))
        draw.ellipse([900 - r, -50 - r, 900 + r, -50 + r], fill=(79, 70, 229, alpha))
        draw.ellipse([150 - r, 550 - r, 150 + r, 550 + r], fill=(124, 58, 237, alpha))

    # Grid background dots
    for x in range(40, W, 40):
        for y in range(40, H, 40):
            draw.rectangle([x, y, x + 2, y + 2], fill=(30, 41, 59, 120))

    # 2. Fonts
    font_bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_reg_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    font_brand = ImageFont.truetype(font_bold_path, 34)
    font_badge = ImageFont.truetype(font_bold_path, 16)
    font_title = ImageFont.truetype(font_bold_path, 52)
    font_title_sub = ImageFont.truetype(font_bold_path, 52)
    font_desc = ImageFont.truetype(font_reg_path, 22)
    font_card_title = ImageFont.truetype(font_bold_path, 20)
    font_score = ImageFont.truetype(font_bold_path, 44)
    font_card_sub = ImageFont.truetype(font_reg_path, 15)
    font_tag = ImageFont.truetype(font_bold_path, 14)
    font_url = ImageFont.truetype(font_bold_path, 20)

    # 3. Top Left Header: App Icon + ATS MatchProof Brand
    icon_x, icon_y, icon_s = 70, 65, 56
    # Icon Rounded Squircle
    draw.rounded_rectangle(
        [icon_x, icon_y, icon_x + icon_s, icon_y + icon_s],
        radius=14,
        fill=(79, 70, 229, 255),
        outline=(129, 140, 248, 255),
        width=2,
    )
    # Document inside icon
    doc_x, doc_y = icon_x + 14, icon_y + 12
    draw.rounded_rectangle(
        [doc_x, doc_y, doc_x + 24, doc_y + 32],
        radius=4,
        fill=(255, 255, 255, 255),
    )
    draw.rectangle([doc_x + 5, doc_y + 8, doc_x + 18, doc_y + 11], fill=(99, 102, 241, 255))
    draw.rectangle([doc_x + 5, doc_y + 15, doc_x + 18, doc_y + 17], fill=(148, 163, 184, 255))
    draw.rectangle([doc_x + 5, doc_y + 21, doc_x + 14, doc_y + 23], fill=(148, 163, 184, 255))
    # Green badge on icon
    draw.ellipse(
        [icon_x + 36, icon_y + 34, icon_x + 54, icon_y + 52],
        fill=(16, 185, 129, 255),
        outline=(255, 255, 255, 255),
        width=2,
    )
    draw.line(
        [icon_x + 41, icon_y + 43, icon_x + 44, icon_y + 47],
        fill=(255, 255, 255, 255),
        width=2,
    )
    draw.line(
        [icon_x + 44, icon_y + 47, icon_x + 50, icon_y + 39],
        fill=(255, 255, 255, 255),
        width=2,
    )

    # Brand Title
    draw.text((icon_x + 72, icon_y + 10), "ATS MatchProof", font=font_brand, fill=(255, 255, 255, 255))

    # Free Badge (Pill)
    badge_x = icon_x + 380
    draw.rounded_rectangle(
        [badge_x, icon_y + 10, badge_x + 195, icon_y + 46],
        radius=18,
        fill=(16, 185, 129, 35),
        outline=(16, 185, 129, 200),
        width=1,
    )
    draw.text((badge_x + 16, icon_y + 18), "100% FREE • NO LOGIN", font=font_badge, fill=(52, 211, 153, 255))

    # 4. Main Hero Typography (Left Side)
    hero_y = 175
    draw.text((70, hero_y), "Beat the ATS.", font=font_title, fill=(255, 255, 255, 255))
    draw.text((70, hero_y + 65), "Land More ", font=font_title_sub, fill=(255, 255, 255, 255))
    draw.text((375, hero_y + 65), "Interviews.", font=font_title_sub, fill=(129, 140, 248, 255))

    # Subtitle Paragraph
    desc_line1 = "Instant AI Match Score • Keyword Gap Extraction"
    desc_line2 = "Google XYZ Bullet Optimizations • Zero Data Stored"
    draw.text((70, hero_y + 150), desc_line1, font=font_desc, fill=(203, 213, 225, 255))
    draw.text((70, hero_y + 188), desc_line2, font=font_desc, fill=(148, 163, 184, 255))

    # 5. Bottom Left: Feature Highlights / Badges
    feat_y = 475
    feats = [
        ("⚡ Dual AI Engine", (99, 102, 241)),
        ("🎯 Google XYZ Formula", (168, 85, 247)),
        ("🔒 100% Private (In-Memory)", (16, 185, 129)),
    ]
    cur_fx = 70
    for label, col in feats:
        bbox = draw.textbbox((0, 0), label, font=font_tag)
        tw = bbox[2] - bbox[0]
        draw.rounded_rectangle(
            [cur_fx, feat_y, cur_fx + tw + 24, feat_y + 36],
            radius=8,
            fill=(15, 23, 42, 230),
            outline=(51, 65, 85, 255),
            width=1,
        )
        draw.text((cur_fx + 12, feat_y + 9), label, font=font_tag, fill=(241, 245, 249, 255))
        cur_fx += tw + 36

    # Bottom Domain Tag
    draw.text((70, 560), "https://atsproof.website", font=font_url, fill=(99, 102, 241, 255))

    # 6. Right Side Preview Mockup Card (Card UI Simulation)
    card_x, card_y, card_w, card_h = 710, 110, 430, 465
    # Card Background Glassmorphism
    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=24,
        fill=(15, 23, 42, 240),
        outline=(51, 65, 85, 255),
        width=2,
    )

    # Score Gauge Box
    score_box_y = card_y + 25
    draw.rounded_rectangle(
        [card_x + 25, score_box_y, card_x + card_w - 25, score_box_y + 105],
        radius=16,
        fill=(30, 41, 59, 180),
        outline=(71, 85, 105, 180),
        width=1,
    )

    # Score Circle Indicator
    sc_cx, sc_cy, sc_r = card_x + 75, score_box_y + 52, 38
    draw.ellipse([sc_cx - sc_r, sc_cy - sc_r, sc_cx + sc_r, sc_cy + sc_r], fill=(2, 6, 23, 255), outline=(16, 185, 129, 255), width=4)
    draw.text((sc_cx - 24, sc_cy - 18), "94", font=font_score, fill=(52, 211, 153, 255))

    # Score Details
    draw.text((card_x + 130, score_box_y + 26), "ATS Match Score", font=font_card_title, fill=(255, 255, 255, 255))
    draw.text((card_x + 130, score_box_y + 56), "Strong Interview Match (Top 5%)", font=font_card_sub, fill=(52, 211, 153, 255))

    # Keyword Chips
    kw_y = card_y + 155
    draw.text((card_x + 25, kw_y), "MATCHED KEYWORDS (FOUND)", font=font_tag, fill=(148, 163, 184, 255))

    chips = ["Python", "FastAPI", "PostgreSQL", "Docker", "REST APIs", "AWS"]
    cx, cy = card_x + 25, kw_y + 28
    for chip in chips:
        cbbox = draw.textbbox((0, 0), "✓ " + chip, font=font_tag)
        cw = cbbox[2] - cbbox[0] + 16
        if cx + cw > card_x + card_w - 25:
            cx = card_x + 25
            cy += 36
        draw.rounded_rectangle([cx, cy, cx + cw, cy + 28], radius=6, fill=(16, 185, 129, 30), outline=(16, 185, 129, 150), width=1)
        draw.text((cx + 8, cy + 6), "✓ " + chip, font=font_tag, fill=(110, 231, 183, 255))
        cx += cw + 10

    # Google XYZ Tailored Bullet Box
    tailor_y = cy + 48
    draw.text((card_x + 25, tailor_y), "GOOGLE XYZ REWRITTEN BULLET", font=font_tag, fill=(129, 140, 248, 255))
    box_y = tailor_y + 26
    draw.rounded_rectangle(
        [card_x + 25, box_y, card_x + card_w - 25, card_y + card_h - 25],
        radius=12,
        fill=(2, 6, 23, 220),
        outline=(99, 102, 241, 120),
        width=1,
    )
    bullet_txt = "“Engineered 12+ scalable REST APIs in FastAPI,\nreducing latency by 38% for 150k active users.”"
    draw.text((card_x + 30, box_y + 12), bullet_txt, font=font_card_sub, fill=(226, 232, 240, 255), spacing=6)

    # Save Image
    out_path = "/home/ubuntu/atsproof/static/og-image.png"
    img.save(out_path, "PNG")
    print(f"Generated OG Image successfully at {out_path}")


if __name__ == "__main__":
    create_og_image()
