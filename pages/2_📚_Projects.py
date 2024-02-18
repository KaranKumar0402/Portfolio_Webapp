import streamlit as st
from streamlit_option_menu import option_menu
import bdst as bd
import MNIST as mnist
import plant_disease_detection as pdd
import ImageToTextOCR as ocr
import webbrowser

# --- PAGE CONFIG ---
st.set_page_config(
    page_title='Projects | Karan Kumar Singh',
    page_icon='🗃️',
)

st.write('These all are my minor projects, intentionally made for fun during my initial days of learning journey!! *So kindly enjoy😄!!')
link = 'https://www.kaggle.com/code/karankumar0402/amazon-web-scraper/notebook'
label = 'See more details about the Project🗃️'

with st.sidebar:
    selected = option_menu(
        menu_title='Projects Menu',
        menu_icon= 'kanban',
        options=['Plant Disease Detection', 'Textron', 'Amazon Web Scraper↗️','MNIST Digit Recogniser', 'Binomial Distribution'],
        icons =['tree-fill','images','browser-edge','123','calculator'],
        default_index=0,
        styles={
            "container": {"padding": "5!important"},
            "icon": {"font-size": "17px"},
            "nav-link": {"font-size": "13px", "margin":"0px"},
            "nav-link-selected": {"font-size": "13px"},}
        )

if selected == 'Binomial Distribution':
    bd.runbdst()
    with st.expander(label=label):
        st.markdown(
            """
            - Binomial Distribution Calculator is developed from scratch without using any python library.
            - This returns Binomial Distribution Graph and it is also interactive.
            - **Probability Mass Function:**
            f'<img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/b872c2c7bfaa26b16e8a82beaf72061b48daaf8e">'
            """, unsafe_allow_html=True
        )

if selected == 'MNIST Digit Recogniser':
    mnist.runmnist()
    with st.expander(label=label):
        st.markdown(
            """
            - Trained a Neural Network on the famous MNIST Digit Dataset from Kaggle.
            - Used Tensorflow ML Framework to train and process the Input Images.
            """
        )

if selected == 'Amazon Web Scraper↗️':
    webbrowser.open(link)
    with st.expander(label=label):
        st.markdown(
            """
            - This Web Scraper is a powerful tool designed to simplify the process of gathering product data from the Amazon marketplace. Whether you're a researcher, e-commerce enthusiast, or data analyst, our scraper provides a seamless solution for extracting essential information from Amazon listings.
            - It is developed using python BeautifulSoup and requests python libraries which are very powerful tools for web scraping.
            """
        )

if selected == 'Plant Disease Detection':
    pdd.runpdd()
    with st.expander(label=label):
        st.markdown(
            """
            - Used pytorch and torchvision for image processing.
            - Deployed a pre-trained ResNet9 classifier model to predict plant diseases from it's leaf photos.
            """
        )

if selected == 'Textron':
    ocr.runOCR()
    with st.expander(label=label):
        st.markdown(
            """
            - Used EasyOCR python library to recognise text from images.
            - Added more features and flexibility to crop and tune the image.
            - Used OpenCV Scale converter to tune the brightness and adjust contrast.
            """
        )

st.sidebar.success("Select Project Above! 👆")