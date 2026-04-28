import streamlit as st
from PIL import Image

@st.dialog("Capture or upload photos")
def add_photos_dialog():
    st.write('Add classroom photos to scan for attendance')
    
    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)
    with t1:
        if st.button('Camera', type='secondary', width='stretch', icon=':material/photo_camera:'):
            st.session_state.photo_tab = 'camera'
    with t2:
        if st.button('Upload Photos', type='secondary', width='stretch', icon=':material/add_photo_alternate:'):
            st.session_state.photo_tab = 'upload'

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Take Photo', key='dialog_cam')
        if cam_photo:
            img_bytes = cam_photo.getvalue()
            if img_bytes not in st.session_state.attendance_images:  # 👈 duplicate check
                st.session_state.attendance_images.append(img_bytes)
                st.toast('Photo captured!')

    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader('Choose image files', type=['jpg', 'png', 'jpeg'], accept_multiple_files=True, key='dialog_upload')
        if uploaded_files:
            for f in uploaded_files:
                img_bytes = f.getvalue()
                if img_bytes not in st.session_state.attendance_images:  # 👈 duplicate check
                    st.session_state.attendance_images.append(img_bytes)
            st.toast('Photos uploaded successfully!')

    st.divider()
    
    if st.session_state.attendance_images:
        st.success(f"✅ {len(st.session_state.attendance_images)} photo(s) ready!")

    if st.button('Done', type='primary', width='stretch'):
        st.rerun()