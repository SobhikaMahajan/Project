# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 16:40:41 2022

@author: CNS
"""

import pickle
import streamlit as st
import numpy as np

def model_load():
    with open("mt.pkl","rb") as file:
        data = pickle.load(file)
    return data

data = model_load()

def app():
    st.title(""" Welcome to Car Mileage Calculator """)
    st.image("Image\dashboard-digital-display-mileage-fuel-consumption-speed-modern-car-speedometer-new-colorful-light-indicators-isolatred-71989997.jpg")
    st.header("Please provide the following details to calculate the mileage")
    
    cylinder = ("4","6","8")
    vs = ("V - Shaped"," Straight")
    am = ("Automatic Transmission","Manual Transmission")
    gear = ("3","4","5")
    carb = ("1","2","3","4","6","8")

    cylinders = st.selectbox("No of Cylinders",cylinder)
    shape = st.selectbox("Engine Shape",vs)
    transmission = st.selectbox("Transmission Type",am)
    gears = st.selectbox("No of Gears",gear)
    carbs = st.selectbox("No of Carburators",carb)
    wt = st.slider("Weight of Car",1.51,5.42,2.0,step = 0.001,format = "%.2f")
    hp = st.number_input("Horse Power(in watts)",52,335,52)

    transmission = 0 if transmission == "Automatic Transmission" else 1
    shape = 0 if shape == "V - Shaped" else 1
    
    ok = st.button("Calculate Mileage")

    if ok:
        x = np.array([[cylinders,hp,wt,shape,transmission,gears,carbs]])
        x.astype(float)
        mileage = data.predict(x)
        st.subheader(f"The Estimated Mileage in miles per gallon is {mileage[0]:.2f}")
        kmpl = mileage[0] * 0.425143707
        st.subheader(f"The Estimated Kilometers per liter is {kmpl:.2f}")
app()