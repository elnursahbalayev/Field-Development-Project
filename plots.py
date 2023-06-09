import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def compare_densities_plot(df):

    fig = plt.figure(figsize=(10, 20))

    plt.subplot(1, 4, 1)
    plt.plot(df['Porosity (Density)'],df['Depth (MSL)'])
    plt.ylim(max(df['Depth (MSL)']), min(df['Depth (MSL)']))
    plt.xlim(0,1)
    plt.xlabel('Porosity (Density)')
    plt.ylabel('Depth (MSL) (ft)')

    ax = plt.gca()
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.xaxis.set_ticks_position('none')

    plt.subplot(1, 4, 2)
    plt.plot(df['Porosity (Neutron)'],df['Depth (MSL)'])
    plt.ylim(max(df['Depth (MSL)']), min(df['Depth (MSL)']))
    plt.xlim(0,1)
    plt.xlabel('Porosity (Neutron)}')

    ax = plt.gca()
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.xaxis.set_ticks_position('none')

    plt.subplot(1, 4, 3)
    plt.plot(df['Porosity (Sonic)'],df['Depth (MSL)'])
    plt.ylim(max(df['Depth (MSL)']), min(df['Depth (MSL)']))
    plt.xlim(0,1)
    plt.xlabel('Porosity (Sonic)')

    ax = plt.gca()
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.xaxis.set_ticks_position('none')

    plt.subplot(1, 4, 4)
    plt.plot(df['Porosity (Density)'],df['Depth (MSL)'])
    plt.plot(df['Porosity (Neutron)'],df['Depth (MSL)'])
    plt.plot(df['Porosity (Sonic)'],df['Depth (MSL)'])
    plt.ylim(max(df['Depth (MSL)']), min(df['Depth (MSL)']))
    plt.xlim(0,1)
    plt.xlabel('Porosity (Comparison)')
    plt.legend(['Density', 'Neutron', 'Sonic'])

    ax = plt.gca()
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.xaxis.set_ticks_position('none')

    plt.tight_layout()
    plt.show()

    return fig
