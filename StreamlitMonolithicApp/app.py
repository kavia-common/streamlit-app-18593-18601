import os
import streamlit as st
st.title('StreamlitMonolithicApp - Dev Scaffold')
st.write('Workspace:', os.getcwd())
if not os.path.exists('data'):
    os.makedirs('data')
st.write('Data dir exists:', os.path.exists('data'))
