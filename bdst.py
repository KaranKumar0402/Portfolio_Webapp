import plotly.express as pex
import streamlit as st

# Defining Factorial method with a new way
@st.cache_data
def fact(x: int):
    facto: int = 1
    if x>=0:
        try:
            for i in range(2,x+1):
                facto*=i
        except:
            return st.success('Please Enter an Integer')
    else:
        facto: str = st.success('Sorry, but there is no Factorial for negetive numbers')
    return facto

# It is for number of all possible order or way the event can occur
def Binomial_Coefficient(n: int, k: int):
    try:
        bc: int = fact(n)/(fact(k)*fact(n-k))
    except:
        return 'Please enter true value for n and k'
    return bc

# Binomial distribution from Scratch
def Binomial_Distribution(n: int, k: int,px: float, each_dis_chart = True, bar_plot = True):
    dis = []
    kx = []
    if each_dis_chart:
        for ki in range(0,k+1):
            PMF = Binomial_Coefficient(n,ki)*(px**ki)*((1-px)**(n-ki))  # Probability Mass Function
            dis.append(round(PMF,6))
            kx.append(ki)
    else:
        PMF = Binomial_Coefficient(n,k)*(px**k)*((1-px)**(n-k))
        kx = [str(k),'Other']
        dis = [PMF,1-PMF]
    if bar_plot:
        fig = pex.bar(dis, x=kx, y=dis,title = 'Binomial Distribution').update_layout(xaxis_title = 'Count of Event Kx',yaxis_title = 'Probability Px')
        return st.plotly_chart(fig, use_container_width=True)
@st.cache_data(experimental_allow_widgets=True)
def runbdst():
    colT1, colT2 = st.columns([0.7, 8])
    with colT2:
        st.header('Binomial Distribution from scratch :1234:')
    col1,col2 = st.columns(2)

    # Main
    # Taking all the inputs

    col1.subheader('Sample Size')
    N = col1.number_input(label = 'Enter the number of sample/s (n)', step = 1, value = 10)

    col2.subheader('Event Count')
    K = col2.number_input(label = 'Enter the event counts (k)', step = 1, value = 10)
    st.subheader('Probability of event on each sample')
    Px = st.slider(label = 'Slide to probability (px)',min_value = 0.0, max_value = 1.0, value=0.5)

    Binomial_Distribution(int(N),int(K),Px)

if __name__ == '__main__':
    runbdst()