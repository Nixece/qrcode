import cv2
import numpy as np
import streamlit as st
from PIL import Image

# ฟังก์ชันสำหรับการสแกน QR Code ด้วย OpenCV
def scan_qr_code(image):
    # แปลงภาพเป็นฟอร์แมตที่ OpenCV เข้าใจ
    image = np.array(image)
    detector = cv2.QRCodeDetector()

    # ตรวจจับและถอดรหัส QR Code
    data, bbox, _ = detector.detectAndDecode(image)
    if bbox is not None:
        return data
    return None

# ส่วนหลักของแอป Streamlit
st.title("QR Code Scanner")

uploaded_file = st.file_uploader("เลือกภาพที่ต้องการสแกน", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="ภาพที่อัปโหลด", use_column_width=True)

    # สแกน QR Code
    qr_data = scan_qr_code(image)
    if qr_data:
        st.success(f"พบข้อมูลใน QR Code: {qr_data}")
    else:
        st.error("ไม่พบ QR Code ในภาพนี้")
