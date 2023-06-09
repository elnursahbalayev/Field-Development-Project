import streamlit as st
import pandas as pd
import numpy as np


def upload_file():
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df
    
def get_necessary_data():
    necessary_values = pd.DataFrame()

    necessary_values['Rig Elevation (m)'] = [st.number_input('Rig Elevation (m)', value=27.3)]
    necessary_values['Top of Reservoir'] = [st.number_input('Top of Reservoir (m)', value=1300)]
    necessary_values['Gas Oil Contact (GOC)'] = [st.number_input('Gas Oil Contact (GOC) (m)', value=1466.7)]
    necessary_values['Water Oil Contact (WOC)'] = [st.number_input('Water Oil Contact (WOC) (m)', value=1508)]

    necessary_values['Brine Density'] = [1.1]
    necessary_values['Gas Effect Brine'] = [0.7]
    necessary_values['Shale Density'] = [2.747]
    necessary_values['Sandstone Density'] = [2.650]
    necessary_values['Limestone Density'] = [2.710]

    necessary_values['Sand Sonic Time'] = [53.45]
    necessary_values['Brine Sonic Time'] = [186.40]

    necessary_values['SIM_A'] = [0.3]
    necessary_values['SIM_Rw'] = [st.number_input('SIM_Rw', value=0.265)]
    necessary_values['SIM_Rsh'] = [st.number_input('SIM_Rsh', value=2.623)]
    necessary_values['SIM_A_FITTING_COEFFICIENT'] =[1.110196874]
    necessary_values['SIM_M_CEMENTATION_FACTOR'] = [1.5568]
    necessary_values['SIM_N_SATURATION_EXPONENT'] = [2]

    return necessary_values

@st.cache_data    
def replace_null(df):
    df.replace(-999.25, np.nan, inplace=True)
    return df

@st.cache_data
def rename_columns(df):
    df.rename({'DEPT':'Depth (m)',
           'RDEEP_1':'Deep Resistivity',
           'RSHAL_1':'Shallow Resistivity',
           'RMICRO_1':'Micro Resistivity',
           'DENB_1':'Bulk Density',
           'CALI_1':'Caliper',
           'NEUT_1':'Neutron Porosity',
           'GR_1':'Gamma Ray',
           'SP_1':'Spontaneous Potential',
           'DTCOMP_1':'Sonic Compressional',
           'PEF_1':'Photoelectric Factor',
           'DTSH_1':'Sonic Shear'}, axis=1, inplace=True)
    return df

@st.cache_data
def calculate_msl(df, drill_rig_height):
    df['Depth (MSL)'] = df['Depth (m)'] - drill_rig_height.values[0]
    return df

@st.cache_data
def calculate_vshale(df):
    df['Vsh'] = (df['Gamma Ray'] - df['Gamma Ray'].min()) / (df['Gamma Ray'].max() - df['Gamma Ray'].min())
    df['Vsh Corrected'] = np.clip(df['Vsh'], 0, 1)
    df['Vsh (Larionov Old)'] = 0.33 * (np.power(2, 2 * df['Vsh Corrected'])-1)
    df['Vsh (Larionov Tertiary)'] = 0.083 * (np.power(2, 3.7*df['Vsh Corrected'])-1)
    df['Lithology'] = np.where(df['Vsh (Larionov Tertiary)'] > 0.5, 'Shale', 'Sandstone')
    return df

@st.cache_data
def calculate_density_log(df, necessary_values):
    df['Matrix Density'] = df['Vsh (Larionov Tertiary)'] * necessary_values['Shale Density'].values[0] + (1-df['Vsh (Larionov Tertiary)']) * necessary_values['Sandstone Density'].values[0]
    df['Fluid Density'] = np.where((df['Depth (MSL)'] < necessary_values['Gas Oil Contact (GOC)'].values[0]) & (df['Depth (MSL)'] > necessary_values['Top of Reservoir'].values[0]), necessary_values['Gas Effect Brine'].values[0], necessary_values['Brine Density'].values[0])
    df['Porosity (Density)'] = (df['Matrix Density'] - df['Bulk Density']) / (df['Matrix Density'] - df['Fluid Density'])
    return df

@st.cache_data
def calculate_neutron_log(df):
    # df['Porosity (Neutron)'] = -0.5 * np.power(df['Neutron Porosity'],2) + 1.31 * df['Neutron Porosity'] + 0.021
    df['Porosity (Neutron)'] = df['Neutron Porosity']
    return df

@st.cache_data
def calculate_sonic_log(df, necessary_values):
    df['Porosity (Sonic)'] = (df['Sonic Compressional'] - necessary_values['Sand Sonic Time'].values[0]) / (necessary_values['Brine Sonic Time'].values[0] - necessary_values['Sand Sonic Time'].values[0])
    return df

@st.cache_data
def calculate_average_porosity(df):
    df['Average Gas Porosity'] = np.sqrt((np.power(df['Porosity (Density)'],2) + np.power(df['Porosity (Neutron)'],2))/2)
    df['Average Porosity'] = (df['Porosity (Density)'] + df['Porosity (Neutron)']) / 2
    df['Effective Porosity'] = df['Average Porosity'] * (1 - df['Vsh (Larionov Tertiary)'])
    return df

@st.cache_data
def calculate_sw_simandoux(df, necessary_values):
    df['Sw (Simandoux)'] = np.power((necessary_values['SIM_A_FITTING_COEFFICIENT'].values[0]*necessary_values['SIM_Rw'].values[0]*(1-df['Vsh (Larionov Tertiary)'])/(2*np.power(df['Effective Porosity'],necessary_values['SIM_M_CEMENTATION_FACTOR'].values[0])))*(np.sqrt(np.power(df['Vsh (Larionov Tertiary)']/necessary_values['SIM_Rsh'].values[0],2)+(4*np.power(df['Effective Porosity'],necessary_values['SIM_M_CEMENTATION_FACTOR'].values[0]))/(necessary_values['SIM_A_FITTING_COEFFICIENT'].values[0]*necessary_values['SIM_Rw'].values[0]*(1-df['Vsh (Larionov Tertiary)'])*df['Deep Resistivity'])) - df['Vsh (Larionov Tertiary)']/necessary_values['SIM_Rsh'].values[0]), 2/necessary_values['SIM_N_SATURATION_EXPONENT'].values[0])
    df['Sw (Simandoux Corrected)'] = np.clip(df['Sw (Simandoux)'], 0, 1)
    df['Hydrocarbon column'] = np.append(np.diff(df['Depth (MSL)']), np.nan) * df['Effective Porosity'] * (1 - df['Sw (Simandoux Corrected)'])
    return df

@st.cache_data
def cut_off_prep_vsh(df):
    df.sort_values(by='Vsh (Larionov Tertiary)', inplace=True)
    df['Hydrocarbon cumulative'] = df['Hydrocarbon column'].cumsum() * 100 / df['Hydrocarbon column'].cumsum().max()
    df.dropna(inplace=True)
    return df


@st.cache_data
def process_data(df, necessary_values):
    df = replace_null(df)
    df = rename_columns(df)
    df = calculate_msl(df, necessary_values['Rig Elevation (m)'])
    df = calculate_vshale(df)
    df = calculate_density_log(df, necessary_values)
    df = calculate_neutron_log(df)
    df = calculate_sonic_log(df, necessary_values)
    df = calculate_average_porosity(df)
    df = calculate_sw_simandoux(df, necessary_values)

    return df
