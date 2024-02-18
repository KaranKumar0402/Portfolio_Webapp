import streamlit as st
import tensorflow as tf
import numpy as np
from streamlit_image_select import image_select
from pathlib import Path

current_directory = Path(__file__).parent if '__file__' in locals() else Path.cwd()
image_path = current_directory / 'demo_images' / 'mnist_imgs'
img_path = [
    image_path / 'one.jpg', image_path / 'two.jpg', image_path / 'three.jpg', image_path / 'four.jpg',
    image_path / 'five.jpg',
    image_path / 'six.jpg', image_path / 'seven.jpg', image_path / 'eight.jpg'
]
img_cap = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight']

model_path = 'MNIST_NN_Classifier.h5'


@st.cache_resource(show_spinner=True)
def loading_model(mp):
    loaded_model = tf.keras.models.load_model(mp)
    return (loaded_model)


@st.cache_data()
def img_processing(img):
    # Manual Image processing
    resized_image = tf.keras.preprocessing.image.load_img(img, target_size=(28, 28))  # Resizing it to 28x28
    resized_image = np.array(resized_image)  # Converting it to Array for further processes
    resized_image = resized_image / 255.  # Normalising
    tensorImg = tf.image.rgb_to_grayscale(resized_image)  # Convert Grayscale(28,28,1) instead of RGB(28,28,3)
    tensorImg = tf.squeeze(tensorImg, axis=-1)  # shape is (28, 28)
    tensorImg = 1.0 - tensorImg  # Altering the colour Black -> White & White -> Black to make background Black
    imagearr = np.array(tensorImg)  # Converting into np.array bcz now it is tensor (TensorFlow Object)
    finalimg = imagearr.reshape(1, 784)  # Converting 28 x 28 to 1 x 784 2D Array

    # Filtering out unnecessary pixels by converting it to 0 or 1 to increase accuracy
    for i in range(784):
        if finalimg[0][i] <= 0.39:
            finalimg[0][i] = 0.0
        elif finalimg[0][i] >= 0.66:
            finalimg[0][i] = 1.0

    return finalimg


# write a function for toggle functionality
def toggle():
    if st.session_state.button:
        st.session_state.button = False
    else:
        st.session_state.button = True


@st.cache_resource(experimental_allow_widgets=True)
def runmnist():
    NNModel = loading_model(model_path)  # Loading the trained Neural Network
    colT1, colT2 = st.columns([1.2, 8])
    with colT2:
        st.title("MNIST Digit Recogniser🔢")

    if "button" not in st.session_state:
        st.session_state.button = False

    # create the button
    st.button('Show Demo Images🖼️', on_click=toggle, key='Demo')

    if st.session_state.button:
        fimg_path = image_select(label="You can also select demo images", images=img_path, captions=img_cap,
                                 use_container_width=False, return_value='index')
        image2 = img_path[fimg_path]
        st.button('Go to Upload⬆️ Image🖼️', on_click=toggle, key='upload')

    if not st.session_state.button:
        st.warning('Please try to insert small size images, as there is limited RAM in streamlit🥲.')
        image2 = st.file_uploader(label="Upload the image of your DIGIT", type=['jpg', 'png'])

    if st.button("Predict the DIGIT 🤔"):
        if image2 is not None:
            # Processing the image
            finalimg = img_processing(image2)
            pred = NNModel.predict(finalimg)

            # Final Prediction
            st.subheader(f"Predicted DIGIT ➡️  {np.argmax(pred)}")

            # Preparing the final input image to show
            showimg = finalimg.reshape((28, 28)) * 25
            st.image(showimg, clamp=True, width=500)
            st.success("That's what the computer sees in 28x28 pixels 👆")
        else:
            st.success("Make sure you image is in JPG/PNG Format 🥲")


if __name__ == '__main__':
    runmnist()
