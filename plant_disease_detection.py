import torch
import torch.nn as nn
import torchvision.transforms as transforms
import streamlit as st
from PIL import Image
from streamlit_image_select import image_select
from pathlib import Path

current_directory = Path(__file__).parent if '__file__' in locals() else Path.cwd()
image_path = current_directory / 'demo_images' / 'plantdd_images'
img_path = [
    image_path / 'AppleBlackRoot.JPG', image_path / 'AppleCedarRust05.jpg', image_path / 'AppleScab.JPG', image_path / 'CornGreyLeaf.jpg',
    image_path / 'PotatoEarlyBlight1.JPG', image_path / 'TomatoEarlyBlight2.JPG', image_path / 'TomatoHealthy1.JPG', image_path / 'TomatoYellowCurlVirus1.JPG'
]
img_cap = ['Apple Black Root', 'Apple Cedar Rust', 'Apple Scab', 'Corn Cercospora Gray Leaf', 'Potato Early Blight',
           'Tomato Early Blight', 'Healthy Tomato', 'Tomato Yellow Curl Virus']
def to_device(data, device):
    if isinstance(data, (list, tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)

@st.cache_data
def ConvBlock(in_channels, out_channels, pool=False):
    layers = [nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
              nn.BatchNorm2d(out_channels),
              nn.ReLU(inplace=True)]
    if pool:
        layers.append(nn.MaxPool2d(4))
    return nn.Sequential(*layers)


# resnet architecture
@st.cache_resource()
class ResNet9(nn.Module):
    def __init__(self, in_channels, num_diseases):
        super().__init__()

        self.conv1 = ConvBlock(in_channels, 64)
        self.conv2 = ConvBlock(64, 128, pool=True)  # out_dim : 128 x 64 x 64
        self.res1 = nn.Sequential(ConvBlock(128, 128), ConvBlock(128, 128))

        self.conv3 = ConvBlock(128, 256, pool=True)  # out_dim : 256 x 16 x 16
        self.conv4 = ConvBlock(256, 512, pool=True)  # out_dim : 512 x 4 x 44
        self.res2 = nn.Sequential(ConvBlock(512, 512), ConvBlock(512, 512))

        self.classifier = nn.Sequential(nn.MaxPool2d(4),
                                        nn.Flatten(),
                                        nn.Linear(512, num_diseases))

    def forward(self, xb):  # xb is the loaded batch
        out = self.conv1(xb)
        out = self.conv2(out)
        out = self.res1(out) + out
        out = self.conv3(out)
        out = self.conv4(out)
        out = self.res2(out) + out
        out = self.classifier(out)
        return out


classes = [' Apple Scab',
           ' Apple Black Root',
           ' Apple Cedar Rust',
           ' Healthy Apple',
           ' Healthy Blueberry',
           ' Cherry Powdery Mildew',
           ' Healthy Cherry',
           ' Corn(Maize) Cercospora Leaf Spot Gray Leaf Spot',
           ' Corn(Maize) Common Rust',
           ' Corn(Maize) Northern Leaf Blight',
           ' Corn(Maize) Healthy',
           ' Grape Black Rot',
           ' Grape Esca(Black Measles)',
           ' Grape Leaf Blight(Isariopsis Leaf Spot)',
           ' Healthy Grape',
           ' Orange Haunglongbing(Citrus Greening)',
           ' Peach Bacterial Spot',
           ' Healthy Peach',
           ' Bell Pepper Bacterial Spot',
           ' Healthy Bell Pepper',
           ' Potato Early Blight',
           ' Potato Late Blight',
           ' Healthy Potato',
           ' Healthy Raspberry',
           ' Healthy Soybean',
           ' Squash Powdery Mildew',
           ' Strawberry Leaf Scorch',
           ' Healthy Strawberry',
           ' Tomato Bacterial Spot',
           ' Tomato Early Blight',
           ' Tomato Late Blight',
           ' Tomato Leaf Mold',
           ' Tomato Septoria Leaf Spot',
           ' Tomato Spider Mites, Two-spotted Spider Mite',
           ' Tomato Target Spot',
           ' Tomato Yellow Leaf Curl Virus',
           ' Tomato Mosaic Virus',
           ' Healthy Tomato']

@st.cache_resource(show_spinner=True)
def loading_model(model_path,device):
    model = ResNet9(3, 38)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return (model)


def predict_image(img, model):
    xb = to_device(img.unsqueeze(0), device)
    yb = model(xb)
    _, preds = torch.max(yb, dim=1)
    return classes[preds[0].item()]


transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor()
])
device = torch.device("cpu")

def toggle():
    if st.session_state.button:
        st.session_state.button = False
    else:
        st.session_state.button = True

@st.cache_resource(experimental_allow_widgets=True)
def runpdd():

    model_path = 'plant-disease-model.pth'
    model = loading_model(model_path,device)
    colT1, colT2, colT3 = st.columns([2, 5.6, 2])
    with colT2:
        st.header('Plant Disease Detector 🥬', divider='rainbow')
    st.subheader('Supported Plants🌱')
    st.success('Apple🍎 Blueberry🫐 Cherry🍒 Corn🌽 Grape🍇 Orange🍊 Peach🍑 Bell Pepper🫑 Potato🥔 Strawberry🍓 Tomato🍅 Raspberry🫐 Soybean🫘 Squash🍐')

    if "button" not in st.session_state:
        st.session_state.button = False

    # create the button
    st.button('Show Demo Images🖼️', on_click=toggle, key='Demo')

    if st.session_state.button:
        fimg_path = image_select(label="You can also select demo images", images=img_path, captions=img_cap,
                                 use_container_width=False, return_value='index')
        inp_img = str(img_path[fimg_path])
        to_pass = '..'+inp_img.split(':')[1]
        st.button('Go to Upload⬆️ Image🖼️', on_click=toggle, key='upload')

    if not st.session_state.button:
        st.warning('Please try to insert small size images, as there is limited RAM in streamlit🥲.')
        inp_img = st.file_uploader('Upload image of your plant leaf here!!',type=['png','jpg','jpeg'])
        to_pass = inp_img

    if st.button('Predict the Disease🍂'):
        if inp_img is not None:
            img = Image.open(inp_img)
            img = transform(img)
            st.success("Predicted Disease ⬇️")
            colT3, colT4 = st.columns([1, 8])
            with colT4:
                st.header(predict_image(img, model))
                st.image(to_pass,width=550,caption='Uploaded Leaf Image!!')

        else:
            st.success('Upload Leaf Picture Above ⤴️')
if __name__ == '__main__':
    runpdd()