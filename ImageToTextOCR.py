import streamlit as st
import easyocr
from streamlit_cropperjs import st_cropperjs
from streamlit_image_select import image_select
import cv2
import imageio.v3 as iio
from pathlib import Path

current_directory = Path(__file__).parent if '__file__' in locals() else Path.cwd()
image_path = current_directory / 'demo_images' / 'ocr_images'
img_path = [
    image_path / 'hindi.jpeg', image_path / 'bangali.jpg', image_path / 'urdu.jpeg', image_path / 'telugu.jpg',
    image_path / 'tamil.jpg',
    image_path / 'french.jpg', image_path / 'spanish.jpg', image_path / 'german.jpg'
]
img_cap = ['hindi', 'Bengali', 'Urdu', 'Telugu', 'Tamil', 'French', 'Spanish', 'German']

langdict = {'Abaza': 'abq',
            'Adyghe': 'ady',
            'Afrikaans': 'af',
            'Angika': 'ang',
            'Arabic': 'ar',
            'Assamese': 'as',
            'Avar': 'ava',
            'Azerbaijani': 'az',
            'Belarusian': 'be',
            'Bulgarian': 'bg',
            'Bihari': 'bh',
            'Bhojpuri': 'bho',
            'Bengali': 'bn',
            'Bosnian': 'bs',
            'Simplified Chinese': 'ch_sim',
            'Traditional Chinese': 'ch_tra',
            'Chechen': 'che',
            'Czech': 'cs',
            'Welsh': 'cy',
            'Danish': 'da',
            'Dargwa': 'dar',
            'German': 'de',
            'English': 'en',
            'Spanish': 'es',
            'Estonian': 'et',
            'Persian (Farsi)': 'fa',
            'French': 'fr',
            'Irish': 'ga',
            'Goan Konkani': 'gom',
            'Hindi': 'hi',
            'Croatian': 'hr',
            'Hungarian': 'hu',
            'Indonesian': 'id',
            'Ingush': 'inh',
            'Icelandic': 'is',
            'Italian': 'it',
            'Japanese': 'ja',
            'Kabardian': 'kbd',
            'Kannada': 'kn',
            'Korean': 'ko',
            'Kurdish': 'ku',
            'Latin': 'la',
            'Lak': 'lbe',
            'Lezghian': 'lez',
            'Lithuanian': 'lt',
            'Latvian': 'lv',
            'Magahi': 'mah',
            'Maithili': 'mai',
            'Maori': 'mi',
            'Mongolian': 'mn',
            'Marathi': 'mr',
            'Malay': 'ms',
            'Maltese': 'mt',
            'Nepali': 'ne',
            'Newari': 'new',
            'Dutch': 'nl',
            'Norwegian': 'no',
            'Occitan': 'oc',
            'Pali': 'pi',
            'Polish': 'pl',
            'Portuguese': 'pt',
            'Romanian': 'ro',
            'Russian': 'ru',
            'Serbian (cyrillic)': 'rs_cyrillic',
            'Serbian (latin)': 'rs_latin',
            'Nagpuri': 'sck',
            'Slovak': 'sk',
            'Slovenian': 'sl',
            'Albanian': 'sq',
            'Swedish': 'sv',
            'Swahili': 'sw',
            'Tamil': 'ta',
            'Tabassaran': 'tab',
            'Telugu': 'te',
            'Thai': 'th',
            'Tajik': 'tjk',
            'Tagalog': 'tl',
            'Turkish': 'tr',
            'Uyghur': 'ug',
            'Ukranian': 'uk',
            'Urdu': 'ur',
            'Uzbek': 'uz',
            'Vietnamese': 'vi'}

lang = [key for key in langdict]

@st.cache_resource(show_spinner=True)
def loading_model(langlist):
    rdr = easyocr.Reader(langlist, gpu = True)
    return (rdr)

def toggle():
    if st.session_state.button:
        st.session_state.button = False
    else:
        st.session_state.button = True
@st.cache_data(show_spinner=True)
def cropping(img, alpha, beta):
    cropped_pic = iio.imread(img)
    cropped_pic = cv2.convertScaleAbs(cropped_pic, alpha=alpha, beta=beta)
    return cropped_pic

def toggle():
    if st.session_state.button:
        st.session_state.button = False
    else:
        st.session_state.button = True

@st.cache_resource(experimental_allow_widgets=True)
def runOCR():
    st.header('Image to Text Converter Using EasyOCR 🔠', divider='rainbow')

    keys = st.multiselect(label='Select preferred LANGUAGES 🗣️!!',options = lang, default=['English'])
    flang = [langdict[key] for key in keys]

    if 'load_state' not in st.session_state:
        st.session_state.load_state = False
    if st.button('Done with Languages') or st.session_state.load_state:
        st.session_state.load_state = True
        reader = loading_model(flang)
        st.success("Now you can upload the image or can select demo images 👇")
        st.warning('Please try to insert small size images, as there is limited RAM in streamlit🥲.')

        if "button" not in st.session_state:
            st.session_state.button = False

        # create the button
        st.button('Show Demo Images🖼️', on_click=toggle, key='Demo')

        if st.session_state.button:
            fimg_path = image_select(label="You can also select demo images", images=img_path, captions=img_cap,
                                     use_container_width=False, return_value='index')
            img = img_path[fimg_path]
            img = open(img, 'rb')
            st.button('Go to Upload⬆️ Image🖼️', on_click=toggle, key='upload')

        if not st.session_state.button:
            img = st.file_uploader('Upoad Image Here 📸!!', type=['png', 'jpg', 'jpeg'], key='uploaded_pic')

        if img is not None:
            cropped_pic = st_cropperjs(pic=img.read(), btn_text="Submit the Cropped Picture ☝️")
            if cropped_pic:
                col1, col2 = st.columns(2)
                col2.write('##### You can adjust contrast and brightness here👇')
                alpha = col2.slider(label='Contrast Adjustment', min_value=0.0, max_value=2.0, value=1.0)
                beta = col2.slider(label='Brightness Adjustment', min_value=-50, max_value=50, value=0)
                cropped_pic = cropping(cropped_pic, alpha, beta)
                col1.image(cropped_pic)

                if st.button('Show Output Text 😊', key='final'):
                    st.toast('This will take a while...')
                    st.toast('Kindly wait...😅')
                    result = reader.readtext(cropped_pic, detail=0, paragraph=True)
                    st.toast('Done 😊')
                    st.subheader(result)

if __name__ == '__main__':
    runOCR()