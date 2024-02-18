from pathlib import Path
import streamlit as st
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(
    page_title='Digital CV | Karan Kumar Singh',
    page_icon='💻',
)

st.sidebar.success('To see some Projects, pLease select 📚Projects Page Above👆')

# --- PATH SETTINGS ---
current_directory = Path(__file__).parent if '__file__' in locals() else Path.cwd()
resume_file = current_directory / 'assets' / 'Karan Kumar Singh.pdf'
profile_pic = current_directory / 'assets' / 'profile_pic.png'

# --- SOCIAL MEDIA ---
SOCIAL_MEDIA = {
    'https://www.svgrepo.com/show/110195/linkedin.svg': 'https://www.linkedin.com/in/karan-kumar-singh-742b5624a/',
    'https://www.svgrepo.com/show/303115/twitter-3-logo.svg': 'https://twitter.com/KarannKumar0402/',
    'https://www.svgrepo.com/show/503359/github.svg': 'https://github.com/KaranKumar0402/',
    'https://www.svgrepo.com/show/349378/gmail.svg': 'mailto:skarankumar690@gmail.com'
}

# --- LOAD PDF & PROFILE PIC ---
with open(resume_file, 'rb') as pdf_file:
    PDFbyte = pdf_file.read()

profile_pic = Image.open(profile_pic)

# --- HERO SECTION ---
col1, col2 = st.columns([1,2], gap='medium')

with col1:
    st.image(profile_pic, width=180)

with col2:
    st.header("Karan Kumar Singh", divider='blue')
    st.write("Computer Science undergraduate, exploring the domains of **Data Science**, **Machine Learning** and **Artificial Intelligence**.")
    st.download_button(
        label='📄 Download Resume',
        data=PDFbyte,
        file_name=resume_file.name,
        mime='application/octet-stream',
    )
# --- CONTACT ---
st.write('#')
cols = st.columns(len(SOCIAL_MEDIA))

for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f'<a href="{link}"><img src="{platform}" alt="HTML tutorial" style="width:42px;height:42px;"></a>', unsafe_allow_html=True)

# --- SKILLS ---
div = [1,2]
st.write('#')
st.subheader('Skills', divider='red')

cols = st.columns(div, gap='small')
cols[0].markdown('<p style="margin-bottom: -10px;"><strong>Programming Languages</strong></p>', unsafe_allow_html=True)
cols[1].markdown('<p style="margin-bottom: -10px;">Python, Java, C/C++</p>', unsafe_allow_html=True)

cols = st.columns(div, gap='small')
cols[0].markdown('<p style="margin-bottom: -10px;"><strong>Databases</strong></p>', unsafe_allow_html=True)
cols[1].markdown('<p style="margin-bottom: -10px;">MySQL, MongoDB</p>', unsafe_allow_html=True)

cols = st.columns(div, gap='small')
cols[0].markdown('<p style="margin-bottom: -10px;"><strong>Libraries/Frameworks</strong></p>', unsafe_allow_html=True)
cols[1].markdown('<p style="margin-bottom: -10px;">NumPy, Pandas, Matplotlib, OpenCV, PIL, Tensorflow, Keras, PyTorch(Basic), Streamlit, Flask(Basic)</p>', unsafe_allow_html=True)

cols = st.columns(div, gap='small')
cols[0].markdown('<p style="margin-bottom: -10px;"><strong>Developer Tools</strong></p>', unsafe_allow_html=True)
cols[1].markdown('<p style="margin-bottom: -10px;">Git, Amazon Web Services(Basic), Anaconda</p>', unsafe_allow_html=True)

# --- QUALIFICATIONS ----
div2 = [3.5, 2, 1.5, 2]
st.write('#')
st.subheader('Education', divider='red')

cols = st.columns(div2)
cols[0].write('🎓 **B.Tech in Information Technology**')
cols[1].write('*Parul University*')
cols[2].write('2022--Present')
cols[3].write('CGPA: 7.48/10')

cols = st.columns(div2)
cols[0].write('🎓 **Class XII (CBSE)**')
cols[1].write('*Kendriya Vidyalaya AFS, Wadsar*')
cols[2].write('2022')
cols[3].write('Percentage: 79.4%')

cols = st.columns(div2)
cols[0].write('🎓 **Class X (CBSE)**')
cols[1].write('*Kendriya Vidyalaya AFS, Wadsar*')
cols[2].write('2020')
cols[3].write('Percentage: 88.6%')

# ---ACHIEVEMENTS---
st.write('#')
st.subheader('Achievements', divider='rainbow')
st.write(
'''
- Won **Vadodara Hackathon 4.0 2023** organised by **Parul University**, also got a cash price and funding offer from **PIERC**.
'''
)

# ---CO-CURRICULARS---
st.write('#')
st.subheader('Co-Curricular Activities', divider='red')
st.write(
    '''
- **Sub-committee member** @ The Coder's Den: *Competitive Coding Club of PU*
'''
)