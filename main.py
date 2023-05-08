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
with st.sidebar:
    www = st.file_uploader("Upload file", type='mp4')
    st.write('Загрузка видеоролика (из репозитория)')
    t = st.text_input("Введите имя файла (без расширения) (1-43) и нажмите Enter")
    #www = st.text_input("html-link. Уровень турникета для видеороликов - 1,2,3,5,8,9,10,11,12,13,15,16,17,18,19")
    #st.write(www)
    #t, www = load_vid()

st.title('YOLOv8_tracking людей, касок, жилетов')
st.write(type(www))

if www is not '':

    turniket = 470
    st.video(www)
    yolo_weights = 'last_8n_e120.pt'
    
    import yolov8_tracking.track as track
    
    with fitz.open(stream=www.read(), filetype="mp4") as file:
      output_buffer = io.BytesIO()
      file.save(output_buffer)
      pdf_bytes = output_buffer.getvalue()
    #with io.BytesIO() as f:
       #im.save(f, format='JPEG')
       #data = f.getvalue()
    #opt = track.parse_opt(yolo_weights,www.getvalue())
    #fstr = track.main(opt)
    #st.write(fstr)
    
    #if(len(fstr)) != 0:
      #print(fstr)
     #   import treatment as obr
      #  df = obr.END(fstr,turniket,'1')
       # st.write('Результат роботы нейросети')

  #  st.write(df)

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
            df = pd.DataFrame(columns=['file','in','out','каски','жилеты'])
            dl = obr.END(fstr,turniket_dict[int(t)],t) # df =  fstr,turniket_dict[t]
            df.loc[0] = dl
            
            st.write('Результат роботы нейросети')
            
            st.write(df)
        else :
            df = pd.DataFrame(columns=['file','in','out','каски','жилеты'])
            #st.write('Результат роботы нейросети')
            df.loc[0] = [1,0,0,0,0]
            st.write(df)




