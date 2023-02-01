# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 13:55:40 2022

@author: bmoul
"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d


st.header("Level Pool Routing")

st.write("Level pool routing is a procedure for calculating the outflow hydrograph from a reservoir assuming a horizontal water surface, given its inflow hydrograph and storage-outflow characteristics.")
st.write("Level pool routing is used for routing.Reservoir routing is actually simply the numerical solution of a differential equation.")   
st.write("Mass balance equation: ")
st.latex(r'''  \left(\frac{dS(t)}{dt}\right) = I(t) - Q(t) ''')
st.write("Storage function relation: ")
st.latex(r'''  S(t) = fn[Q(t)] ''')
st.write("Reservoir Outlet flow depends only on the storage.Outlet flow has no backwater effects. ")
st.write("Rearranging the terms in the mass balance equation above we get the following equation: ")
st.latex("Using:  dS = S_{j+1} - S_{j} ")
st.latex(r'''  \left(\frac{2S_{j+1}}{dt} +  Q_{j+1}\right) = I_{j} + I_{j+1} + \left(\frac{2Sj}{dt}\right) - Q_{j} ''')
st.write("  ")
st.write("  ")

st.text("Step 1 : Compute 2S/dt + Q from Q and S")
st.text("Step 2 : Compute ")
st.latex(r''' I_{j} + I_{j+1}  {  } \!+ {  } \left(\frac{2S_{j}}{dt}\right) - Q_{j}       ''')
st.text("The value obtained above is equal to RHS in the rearranged equation")
st.text("Step 3 : Obtain Qj by linear-interpolation from the obtained values in Step 1. ")
st.text("Step 4 : Repeat Step 2 for the next time. ")


with st.sidebar:
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        start = True
    else:
        start = False
        
if start:
    
    Q = df.Q
    S = df.S
    t = df.t
    I = df.I
    deltat = (df.t[2] - df.t[1])*60 
    

    P = np.empty(len(Q))

    for i in range(0,len(Q)):
        P[i] = ((2*S[i])/deltat) + Q[i]
        
    T = np.empty(len(Q)) # Ij + Ij+1

    for i in range(1,len(Q)):
        T[i] = I[i] + I[i - 1]

    R = np.empty(len(Q)) # 2Sj/t - Qj
    R[0] = 0

    Y = np.empty(len(Q)) # 2Sj+1 + Qj+1 
    Q1 = np.empty(len(Q))  # Final Output
    for i in range (1,len(Q)):
        Y[i] = T[i] + R[i - 1]
        f = interp1d(P, Q)
        Q1 = f(Y)
        #df['Q1'].interpolate(method="linear")
        #df.interpolate(method="pad", limit=2)
        #Q1.interpolate()
        R[i] = Y[i] - 2*Q1[i]
        
    df['Q1'] = Q1    
    
    
    
    fig, ax = plt.subplots()
    ax =plt.plot(t,Q1, label = 'Outflow')
    ax = plt.plot(t,I, label = 'Inflow')
    ax = plt.xlabel('time')
    ax = plt.ylabel('Flow')
    ax = plt.legend()
    st.pyplot(fig)
    st.write(df)
    
