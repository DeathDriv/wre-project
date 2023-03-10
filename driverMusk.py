# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 18:38:00 2022

@author: bmoul
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


st.header("Muskingum Method")

st.markdown("Flood Routing is the technique of determining the flood hydrograph \
            at a section of a river by utilizing the data of flood flow at one or more upstream sections.\
 The Muskingum routing method uses a conservation of mass approach to route an inflow hydrograph. The Muskingum method can also account for “looped” storage vs. outflow relationships that commonly exist in most rivers.\
 Muskingum method is used for channel routing.If the flow were to be uniform throughout, the water surface line would wave been parallel to channel bed.However because of non-uniform condition due to flood,there will be water level will not be parallel to channel bed. ")
st.write("Mass balance equation: ")
st.latex(r'''  \left(\frac{dS(t)}{dt}\right) = I(t) - Q(t) ''')
st.write("Storage function relation: ")
st.latex(r'''  S(t) = K[xI(t) + (1-x)Q(t)] ''')

st.write("The volume of water stored in a channel reach is comprised of:")
st.write("1.Prism storage : A constant uniform flow ")
st.latex("S(t) = KQ(t)")
st.write("2.Wedge storage : A variable flow ")
st.latex("S(t) = Kx[I(t)-Q(t)]")
st.write("Constraints: ")
st.latex(r'''  x < \left(\frac{0.5 Δt}{K}\right) < 1 - x ''')
st.write("The outflow equation for this method: ")
st.latex(r'''  Q_{j+1} = C1I_{j+1} + C2I_j + C3Q_j ''') 
st.text("Where:")
st.text("      Qj+1 is the Current Outflow ")
st.text(" Ij is the Past Inflow ")
st.latex(r'''  C1 = \left(\frac{-2Kx+∆t}{2K(1-x)+∆t}\right) ''') 
st.latex(r'''  C2 = \left(\frac{2Kx+∆t}{2K(1-x)+∆t}\right) ''') 
st.latex(r'''  C3 = \left(\frac{2K(1-x)-∆t}{2K(1-x)+∆t}\right) ''')

#K = st.number_input("K",min_value=0.0,max_value=1.0,value=0.5,step=0.1)
with st.sidebar:

    k = st.slider("K",min_value=0.0,max_value=15.0,value=0.9,step=0.01)
    x = st.slider("x",min_value=0.0,max_value=1.0,value=0.2,step=0.01)
    Q1 = st.slider("Q1",min_value=0.0,max_value=1000.0,value=0.2,step=1.0)

    uploaded_file = st.file_uploader("Choose a file")
    
    #st.write(k)
    #st.write(x)
    
        
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        start = True
    else:
        start = False

if start:
    deltat = df.t[2] - df.t[1]    # st.write(df)
        
        # st.write(K)
       
        #df = pd.read_excel(r'muskinguminput.xlsx')
    I = df.I
    t = df.t
    c1 = ((deltat-2*k*x)/(2*k*(1-x)+ deltat))
    c2 = ((deltat+2*k*x)/(2*k*(1-x)+ deltat))
    c3 = ((2*k*(1-x)-deltat)/(2*k*(1-x)+ deltat))
    #st.text("C1 = "+str(c1)+"\nC2 = "+str(c2)+"\nC3 = "+str(c3))
    if(c1>=0 and c2>=0 and c3>=0):
        Q = np.empty(20)
        Q[0] = Q1
    
        for i in range(1,20):
            Q[i] = c1*I[i] + c2*I[i - 1] + c3*Q[i - 1]
    
        df['Q'] = Q
    
        #st.write("An approximate hydrological method of flood routing through a reach of river, based on the equation of continuity and a storage equation expressing the linear dependence of the water volume in the reach on the weighted inflow and outflow.")
        
        
        st.text("C1 = "+str(c1)+"\nC2 = "+str(c2)+"\nC3 = "+str(c3)) 

        fig, ax = plt.subplots()
        ax =plt.plot(t,Q, label = 'Outflow')
        ax = plt.plot(t,I, label = 'Inflow')
        ax = plt.xlabel('time')
        ax = plt.ylabel('Flow')
        ax = plt.legend()
        st.pyplot(fig)
        st.write(df)
        #print(Q)
    # st.show()
