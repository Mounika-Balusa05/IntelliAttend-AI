import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subject, get_student_attendance, unenroll_student_to_subject
import time
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Logout", type='secondary', key='logoutbtn'):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.session_state.show_registration = False
            st.session_state.photo_source = None
            st.session_state.last_processed_camera = None  # ✅ reset
            st.rerun()

    st.header(f"Welcome, {student_data['name']}")
    st.space()

    c1, c2 = st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('Enroll in Subject', type='primary', width='stretch'):
            enroll_dialog(student_id)

    st.divider()

    with st.spinner('Loading your enrolled subjects...'):
        subjects = get_student_subject(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}
    for log in logs:
        sid = log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]['total'] += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']
        stats = stats_map.get(sid, {"total": 0, "attended": 0})

        def unenroll_button(sid=sid):
            if st.button('Unenroll from this course', type='tertiary', icon=':material/delete_forever:', width='stretch', key=f"unenroll_{sid}"):
                unenroll_student_to_subject(student_id, sid)
                st.toast(f"Unenrolled successfully!")
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended'])
                ],
                footer_callback=unenroll_button
            )


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to home", type='secondary', key='loginbackbtn'):
            st.session_state['login_type'] = None
            st.session_state.show_registration = False
            st.session_state.photo_source = None
            st.session_state.last_processed_camera = None  # ✅ reset
            st.rerun()

    st.header("Login Using Face", text_alignment='center')
    st.space()

    # ✅ Initialize all session state keys safely
    if 'show_registration' not in st.session_state:
        st.session_state.show_registration = False
    if 'photo_source' not in st.session_state:
        st.session_state.photo_source = None
    if 'last_processed_camera' not in st.session_state:
        st.session_state.last_processed_camera = None

    photo_source = st.camera_input("Position your face in the center — look straight at the camera", key="camera")

    # ✅ Only process if this is a NEW photo we haven't scanned yet
    if photo_source is not None and photo_source != st.session_state.last_processed_camera:
        st.session_state.last_processed_camera = photo_source  # mark as processed
        st.session_state.photo_source = photo_source

        img = np.array(Image.open(photo_source))
        with st.spinner('AI is scanning...'):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning('Face not found! Please look straight at the camera.')
                st.session_state.show_registration = False
            elif num_faces > 1:
                st.warning('Multiple faces found! Please make sure only you are in the frame.')
                st.session_state.show_registration = False
            else:
                # ✅ num_faces == 1: face detected
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == student_id), None)
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.session_state.show_registration = False
                        st.session_state.last_processed_camera = None  # ✅ reset for next login
                        st.toast(f"Welcome Back {student['name']}!")
                        time.sleep(1)
                        st.rerun()
                else:
                    # ✅ Face detected but not recognised — always show registration
                    st.info('Face not recognised! You might be a new student.')
                    st.session_state.show_registration = True

    # ✅ Registration form — persists across reruns because we only set it above on new photos
    if st.session_state.show_registration:
        with st.container(border=True):
            st.header('Register new profile')
            new_name = st.text_input("Enter your name: ", placeholder='E.g. John')
            st.subheader('Optional: Voice Enrollment')
            st.info("Enroll your rollno for voice over")
            audio_data = None
            try:
                audio_data = st.audio_input('Record a short phrase like im present mam!')
            except Exception as e:
                st.error('Audio input failed')

            if st.button('Create Account', type='primary'):
                if new_name:
                    with st.spinner('Creating profile...'):
                        img = np.array(Image.open(st.session_state.photo_source))
                        encodings, _ = get_face_embeddings(img)  # ✅ unpack tuple
                        if encodings:
                            face_emb = encodings[0].tolist()
                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())
                            response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)
                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.session_state.show_registration = False
                                st.session_state.photo_source = None
                                st.session_state.last_processed_camera = None  # ✅ reset
                                st.toast(f'Profile Created {new_name}!')
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error('Could not capture your facial features. Please retake the photo looking straight at the camera.')
                else:
                    st.warning('Please enter your name')