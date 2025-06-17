import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap

st.set_page_config(page_title="キプかわ履歴書ジェネレーター", layout="centered")
st.title("📝 キプかわ モデレーター応募用・履歴書ジェネレーター")
st.write("以下に入力して、あなただけの“履歴書画像”を生成してください。")
st.write("生成された画像を保存し、指定のXアカウントにDMで送ってください 📩")

photo = st.file_uploader("顔写真をアップロード（正方形または4:3にトリミングされます）", type=["png", "jpg", "jpeg"])

name = st.text_input("お名前")
x_account = st.text_input("Xアカウント（@から）")
vc_status = st.radio("VCの可否", options=["可", "不可", "状況による"])
activity = st.text_area("主な活動や経歴")
free_comment = st.text_area("自由記入欄（やってみたいこと、意気込みなど）")

font_title_path = "fonts/NotoSansJP-Bold.ttf"
font_body_path = "fonts/NotoSansJP-Regular.ttf"

if st.button("履歴書画像を生成"):
    if not all([photo, name, x_account, vc_status, activity, free_comment]):
        st.warning("すべての項目を入力し、顔写真をアップロードしてください。")
    else:
        image = Image.new("RGB", (1240, 1754), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        uploaded_img = Image.open(photo).convert("RGB")
        w, h = uploaded_img.size
        min_edge = min(w, h)
        cropped = uploaded_img.crop(((w - min_edge)//2, (h - min_edge)//2, (w + min_edge)//2, (h + min_edge)//2))
        resized = cropped.resize((300, 300))
        image.paste(resized, (50, 50))

        font_title = ImageFont.truetype(font_title_path, 28)
        font_body = ImageFont.truetype(font_body_path, 24)
        line_spacing = 36

        # ヘッダ
        x0, y0 = 380, 64
        draw.rectangle([x0 - 10, y0 - 10, 1150, y0 + 130], outline="black", width=2)
        draw.text((x0, y0), f"お名前：{name}", font=font_body, fill=(0, 0, 0))
        draw.text((x0, y0 + 40), f"X：{x_account}", font=font_body, fill=(0, 0, 0))

        vc_options = ["可", "不可", "状況による"]
        vc_labels = ["☑" if opt == vc_status else "□" for opt in vc_options]
        vc_display = "　".join([f"{mark} {opt}" for mark, opt in zip(vc_labels, vc_options)])
        draw.text((x0, y0 + 80), f"VC可否：{vc_display}", font=font_body, fill=(0, 0, 0))

        # 活動欄
        y1 = y0 + 360
        draw.rectangle([40, y1, 1200, y1 + 300], outline="black", width=2)
        draw.text((50, y1 + 10), "主な活動や経歴：", font=font_title, fill=(0, 0, 0))
        for i, line in enumerate(textwrap.wrap(activity, width=45)):
            draw.text((50, y1 + 60 + i*line_spacing), line, font=font_body, fill=(0, 0, 0))

        # 自由欄
        y2 = y1 + 400
        draw.rectangle([40, y2, 1200, y2 + 580], outline="black", width=2)
        draw.text((50, y2 + 10), "自由記入欄：", font=font_title, fill=(0, 0, 0))
        for i, line in enumerate(textwrap.wrap(free_comment, width=45)):
            draw.text((50, y2 + 60 + i*line_spacing), line, font=font_body, fill=(0, 0, 0))

        buf = io.BytesIO()
        image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.image(image, caption="あなたの履歴書", use_container_width=True)
        st.download_button("⬇️ 履歴書画像をダウンロード", data=byte_im, file_name="vrc_resume.png", mime="image/png")
        st.success("この画像を @haise_rei にDMで送ってください📩")
