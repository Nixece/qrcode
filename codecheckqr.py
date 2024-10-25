import streamlit as st
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import io

# ฟังก์ชันสำหรับการแสดงแต้มสะสมปัจจุบัน
def display_points(points):
    st.write(f"แต้มสะสมปัจจุบันของคุณ: **{points}**")

# ฟังก์ชันสำหรับการอัปโหลด QR Code เพื่อแลกแต้มสะสม
def scan_qr_code(image):
    # แปลงภาพให้เป็นขาวดำ
    decoded_objects = decode(image)
    for obj in decoded_objects:
        if obj.data.decode('utf-8') == "รหัสบรรจุภัณฑ์นี้สำหรับสะสม 10 คะแนน":
            return 10
    return 0

# ฟังก์ชันสำหรับการแลกของรางวัล
def redeem_rewards(points):
    st.write("เลือกของรางวัลที่ต้องการแลก:")
    reward_options = {
        "แก้วน้ำ": 30,
        "กระเป๋าผ้า": 50,
        "หมวก": 70,
        "บัตรกำนัล": 100
    }

    selected_reward = st.selectbox("เลือกของรางวัล", list(reward_options.keys()))

    if st.button("แลกของรางวัล"):
        if points >= reward_options[selected_reward]:
            points -= reward_options[selected_reward]
            st.success(f"คุณได้แลก {selected_reward} แล้ว! แต้มสะสมของคุณเหลือ {points} คะแนน")
        else:
            st.error(f"แต้มสะสมของคุณไม่พอสำหรับแลก {selected_reward}")
    
    return points

# ส่วนหลักของโปรแกรม
st.title('ระบบแลกของรางวัล')

# ตั้งค่าเริ่มต้นสำหรับแต้มสะสม
if 'points' not in st.session_state:
    st.session_state.points = 0

# แสดงแต้มสะสมปัจจุบัน
display_points(st.session_state.points)

# ส่วนสำหรับอัปโหลด QR Code
st.write("อัปโหลด QR Code เพื่อสะสมแต้ม:")
uploaded_qr_file = st.file_uploader("เลือกไฟล์ภาพ QR Code", type=["jpg", "png", "jpeg"])

if uploaded_qr_file is not None:
    image = Image.open(uploaded_qr_file)
    st.image(image, caption="QR Code ที่อัปโหลด", use_column_width=True)
    
    # สแกน QR Code และเพิ่มแต้มสะสม
    points_earned = scan_qr_code(image)
    if points_earned > 0:
        st.success(f"คุณได้รับ {points_earned} คะแนน!")
        st.session_state.points += points_earned
    else:
        st.error("QR Code ไม่ถูกต้องหรือไม่สามารถสแกนได้")

# แสดงแต้มสะสมที่อัปเดต
display_points(st.session_state.points)

# ส่วนสำหรับแลกของรางวัล
st.write("-----")
st.session_state.points = redeem_rewards(st.session_state.points)
