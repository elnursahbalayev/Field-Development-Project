import streamlit as st
import functions as f
import plots as p

# Adding a title to the app
st.title('Field Development Project')
st.subheader('by Elnur Shahbalayev')

# Creating tabs
data_tab, logs_tab, cut_offs_tab, monte_carlo_tab = st.tabs(["Data", "Well Logs", "Cut Offs", "Monte Carlo Simulation"])

# Adding content to the data tab
with data_tab:
    df = f.upload_file()
    st.divider()
    necessary_values = f.get_necessary_data()

    df = f.process_data(df, necessary_values)

    st.divider()
    st.write('download the file will be here')
    

# Adding content to the well logs tab
with logs_tab:
    fig = p.compare_densities_plot(df)
    st.pyplot(fig)