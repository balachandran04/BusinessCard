import pandas as pd
import easyocr as eo
import numpy as np
from PIL import Image
import re
import streamlit as st
import io
import sqlite3
from streamlit_option_menu import option_menu

def input_image(paths):
  input_img = Image.open(paths)
  input_arr = np.array(input_img)
  reader = eo.Reader(["en"])
  text = reader.readtext(input_arr,detail=0)
  return text , input_img

def preprocessing(texts):
    dicts = {"name":[], "work":[],"company_name":[],"mobile_number":[],"email":[],"website":[],"address":[],"pincode":[]}
    dicts["name"].append(texts[0])
    dicts["work"].append(texts[1])
    for i in range(2,len(texts)):
        if texts[i].startswith("+") or (texts[i].replace("-"," ").isdigit() and "-" in texts[i]):
            dicts["mobile_number"].append(texts[i])
        elif "@" in texts[i] and ".com" in texts[i]:
            dicts["email"].append(texts[i])
        elif "WWW" in texts[i].upper() or "WWW" in texts[i].lower():
            small = texts[i].lower()
            dicts['website'].append(small)
        elif "Tamil Nadu" in texts[i] or "TamilNadu" in texts[i] or texts[i].isdigit():
            dicts["pincode"].append(texts[i])
        elif re.match(r'^[A-Za-z]', texts[i]):
            dicts["company_name"].append(texts[i])
        else:
            address = re.sub(r'[,;]','',texts[i])
            dicts["address"].append(address)
    for key,value in dicts.items():
      if len(value) > 0:
        con = " ".join(value)
        dicts[key] = [con]
      else:
        value = "NA"
        dicts[key] = [value]

    return dicts


# streamlit
st.set_page_config()
st.title("Business Card Alaysis")
with st.sidebar:
    select = option_menu("Menu",
                         ['home'])
if select == "home":
      st.header("Welcome to Business Card Analysis")
      img = st.file_uploader("uploade the your buiness card")
      if img is not None:
        st.image(img,width=300)

        text_image, input_image = input_image(img)

        dicts = preprocessing(text_image)
        if dicts:
          st.success("Your data extract sucessully ")
        df = pd.DataFrame(dicts)

        byte = io.BytesIO()
        input_image.save(byte,format="PNG")

        image_data = byte.getvalue()
        data = {"image":[image_data]}
        image_df = pd.DataFrame(data)

        marge_df = pd.concat([df,image_df],axis=1)
        st.dataframe(marge_df)
        save = st.button("save")
        if save:
          conn = sqlite3.connect("card.db")
          cursor = conn.cursor()
          # ctrea table
          table = """   create table if not exists bizcard(
                        name varchar(100),
                        work varchar(100),
                        company_name varchar(225),
                        contact varchar(100),
                        email varchar(100),
                        website varchar(100),
                        address varchar(500),
                        pincode varchar(100),
                        image text) """
          cursor.execute(table)
          conn.commit

          insert_qery = """
          INSERT INTO bizcard (name, work, company_name, contact, email, website, address, pincode, image)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
          """
          data = marge_df.values.tolist()[0]
          cursor.execute(insert_qery,data)
          conn.commit()
          st.success("data Store successfully")
      method = st.radio("select the Mode" ,["See","Modify"])
      if method == "See":
        try:
              s = "select * from bizcard"
              conn = sqlite3.connect("card.db")
              cursor = conn.cursor()
              cursor.execute(s)
              table = cursor.fetchall()
              conn.commit()

              table_df= pd.DataFrame(table,columns=["name","Work","Company_name","contact","Email","website","address","pincode","image"])
              st.dataframe(table_df)
        except:
          st.write("insert the Photo")
          

        

















