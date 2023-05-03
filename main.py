import io
import streamlit as st
import pandas as pd
import numpy as np

turniket_dict =  {1:470,2:470,3:470,4:910,5:470,\
                  6:580,7:580,8:470,9:470,10:470,\
                  11:470,12:470,13:470,14:580,15:470,\
                  16:470,17:470,18:470,19:470,20:850,\
                  21:430,22:430,23:430,24:430,25:510,\
                  26:510,27:510,28:510,29:510,30:510,\
                  31:430,32:0,33:0,34:0,35:0,\
                  36:430,37:0,38:430,39:430,40:430,\
                  41:0,42:430,43:0\
                }
        #-------------------------
def load_vid():
    t = st.text_input("Введите имя файла (без расширения) (1-43) и нажмите Enter")
    www = st.text_input("html-link. Уровень турникета для видеороликов - 1,2,3,5,8,9,10,11,12,13,15,16,17,18,19")
    
    return t, www
#==================================================================   
col1, col2 = st.columns(2)

st.title('YOLOv8_tracking людей, касок, жилетов')
st.write('Загрузка видеоролика (из репозитория)')

t, www = load_vid()
if www is not '':
    st.write(www)
    turniket = 470
    st.video(www)
    #st.video(vd)
    yolo_weights = 'last_8n_e120.pt'
    import yolov8_tracking.track as track
    opt = track.parse_opt(yolo_weights,www)
    fstr = track.main(opt)
    if(len(fstr)) != 0:
        import treatment as obr
        df = obr.END(fstr,turniket)
        st.write('Результат роботы нейросети')

    st.write(df)


if t is not '':
    
    d = int(t)
    st.write(t+'.mp4')

    if (d <= 43):

        ts = str(t)
        p = 'Video/'+ts+'.mp4'
        vd = open(p,'rb')
        st.video(vd)
        yolo_weights = 'last_8n_e120.pt'
        import yolov8_tracking.track as track
        opt = track.parse_opt(yolo_weights,p)
        fstr = track.main(opt)
        
        if(len(fstr)) != 0:
            import treatment as obr
            df = pd.DataFrame(columns=['files','in','out','каски','жилеты'])
            dl = obr.END(fstr,turniket_dict[int(t)],t) # df =  fstr,turniket_dict[t]
            df.loc[0] = dl
            
            st.write('Результат роботы нейросети')
            
            st.write(df)
        else :
            df = pd.DataFrame(columns=['files','in','out','каски','жилеты'])
            #st.write('Результат роботы нейросети')
            df.loc[0] = [1,0,0,0,0]
            st.write(df)


'''
import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(layout="wide", page_title="Image Background Remover")

st.write("## Remove background from your image")
st.write(
    ":dog: Try uploading an image to watch the background magically removed. Full quality images can be downloaded from the sidebar. This code is open source and available [here](https://github.com/tyler-simons/BackgroundRemoval) on GitHub. Special thanks to the [rembg library](https://github.com/danielgatis/rembg) :grin:"
)
st.sidebar.write("## Upload and download :gear:")


# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


def fix_image(upload):
    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)

    fixed = remove(image)
    col2.write("Fixed Image :wrench:")
    col2.image(fixed)
    st.sidebar.markdown("\n")
    st.sidebar.download_button("Download fixed image", convert_image(fixed), "fixed.png", "image/png")


col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if my_upload is not None:
    fix_image(upload=my_upload)
else:
    fix_image("./zebra.jpg")

'''
