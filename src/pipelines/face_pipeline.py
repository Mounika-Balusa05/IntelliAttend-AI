import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector, sp, facerec


def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 1)
    num_detected = len(faces)  # ✅ raw detection count, separate from embeddings
    encodings = []
    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
        encodings.append(np.array(face_descriptor))
    return encodings, num_detected  # ✅ return both


@st.cache_resource
def get_trained_model():
    X = []
    y = []
    student_db = get_all_students()
    if not student_db:
        return None
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))
    if len(X) == 0:
        return None

    # Store raw embeddings always (used for nearest-neighbor)
    model_data = {'clf': None, 'X': X, 'y': y}

    # Only train SVC if we have 2+ unique students
    if len(set(y)) >= 2:
        clf = SVC(kernel='linear', probability=True, class_weight='balanced')
        try:
            clf.fit(X, y)
            model_data['clf'] = clf
        except ValueError:
            pass  # fallback to nearest-neighbor

    return model_data


def train_classifier():
    get_trained_model.clear()
    # Also clear get_all_students cache if it's a cached function
    if hasattr(get_all_students, 'clear'):
        get_all_students.clear()
    model_data = get_trained_model()
    return bool(model_data)


def predict_attendance(class_image_np):
    encodings, num_detected = get_face_embeddings(class_image_np)  # ✅ unpack both
    detected_student = {}
    model_data = get_trained_model()

    if not model_data:
        return detected_student, [], num_detected  # ✅ use raw detection count

    X_train = model_data['X']
    y_train = model_data['y']
    clf = model_data['clf']

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:
        # ✅ SVC narrows candidates, nearest-neighbor makes final decision
        if clf is not None and len(all_students) >= 2:
            probs = clf.predict_proba([encoding])[0]
            top_indices = np.argsort(probs)[-3:]
            candidate_ids = set(clf.classes_[i] for i in top_indices)

            best_distance = float('inf')
            best_id = None
            for emb, sid in zip(X_train, y_train):
                if sid in candidate_ids:
                    distance = np.linalg.norm(np.array(emb) - encoding)
                    if distance < best_distance:
                        best_distance = distance
                        best_id = sid
        else:
            # Single student — pure nearest-neighbor
            best_distance = float('inf')
            best_id = None
            for emb, sid in zip(X_train, y_train):
                distance = np.linalg.norm(np.array(emb) - encoding)
                if distance < best_distance:
                    best_distance = distance
                    best_id = sid

        # ✅ Strict threshold — safe buffer for similar-looking faces
        if best_id is not None and best_distance <= 0.5:
            detected_student[int(best_id)] = True

    return detected_student, all_students, num_detected  # ✅ raw detection count