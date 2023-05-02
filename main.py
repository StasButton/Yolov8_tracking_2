import io
import streamlit as st
import pandas as pd
import numpy as np

turniket = 0 
def turnlevel(d):
    ff = []; 
    f1 = [1,2,3,5,8,9,10,11,12,13,15,16,17,18,19]
    ff.append(f1)
    f2 = [6,7,14]
    ff.append(f2)
    f3 = [20]
    ff.append(f3)
    f4 = [21,22,23,24,31,36,38,39,40,42]
    ff.append(f4)
    f5 = [25,26,27,29,30]
    ff.append(f5)
    f6 = [4]
    ff.append(f6)

    for i in range(len(ff)):
        for i2 in ff[i]:
            if i2 == d:
              if i == 0:
                turniket = 470
              if i == 1:
                turniket = 580
              if i == 2:
                turniket = 850
              if i == 3:
                turniket = 430
              if i == 4:
                turniket = 510
              if i == 5:
                turniket = 910
    return  turniket
        #-------------------------
def load_vid():
    t = st.text_input("Введите имя файла (без расширения) (1-43) и нажмите Enter")
    www = st.text_input("html-link. Уровень турникета для видеороликов - 1,2,3,5,8,9,10,11,12,13,15,16,17,18,19")
    
    return t, www
#==================================================================   

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
    turniket = turnlevel(d)

    if (d <= 43):

        t = str(t)
        p = 'Video/'+t+'.mp4'
        vd = open(p,'rb')
        st.video(vd)
        yolo_weights = 'last_8n_e120.pt'
        import yolov8_tracking.track as track
        opt = track.parse_opt(yolo_weights,p)
        fstr = track.main(opt)
        
        if(len(fstr)) != 0:
            import treatment as obr
            df = obr.END(fstr,turniket)
            st.write('Результат роботы нейросети')
            
            st.write(df)
        else :
            df = pd.DataFrame(columns=['files','in','out','каски','жилеты'])
            #st.write('Результат роботы нейросети')
            df.loc[0] = [1,0,0,0,0]
            st.write(df)


