import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_base_layout , style_background_home
from src.components.footer import footer_home
# header ante just small heading pyna , ante snap class alaaa
def home_screen():
    

    header_home()
    style_background_home()
    style_base_layout()
    col1, col2 = st.columns(2, gap="large") 
    with col1:
        st.header("Teacher")
        st.image("src/assets/teacher.jpg",width=120)
        if st.button('Teacher Portal',type='primary',icon=':material/chevron_right:',icon_position='right'):
            st.session_state['login_type']='teacher'
            st.rerun()
    with col2:
        st.header("Student")
        st.image("src/assets/student.jpg",width=120)
        if st.button('Student Portal',type='primary',icon=':material/chevron_right:',icon_position='right'):
            st.session_state['login_type']='student'
            st.rerun()
    footer_home()

