import streamlit as st
import functions as f
import plots as p

# Adding a title to the app
st.title('Field Development Project')
st.subheader('by Elnur Shahbalayev')

# Creating tabs
data_tab, logs_tab, cut_offs_tab, deterministic_stoip, monte_carlo_tab = st.tabs(["Data", "Well Logs", "Cut Offs","Deterministic STOIP", "Monte Carlo Simulation"])

# Adding content to the data tab-

with data_tab:
    df = f.upload_file()

    st.divider()

    necessary_values = f.get_necessary_data()

    df = f.process_data(df, necessary_values)

    st.divider()
    

# Adding content to the well logs tab
with logs_tab:

    ready_plots_tab, custom_plots_tab = st.tabs(['Ready Plots', 'Custom Plot'])

    with ready_plots_tab:
        fig = p.compare_densities_plot(df)
        st.pyplot(fig)

    with custom_plots_tab:
        choice = st.selectbox('Pick a column to display vs Depth (MSL)', df.columns[1:])
        fig = p.plot_vs_depth(df, choice)
        st.pyplot(fig)

with cut_offs_tab:
    df_cutted, cut_offs = f.process_cut_offs(df)

with deterministic_stoip:
    df_reservoir = f.process_stoip(df, cut_offs, necessary_values)

with data_tab:
    st.download_button(label='Whole data before cutoff', data=df.to_csv(), file_name='before_cutoff.csv', mime='text/csv')
    st.download_button(label='Whole data after cutoff', data=df_cutted.to_csv(), file_name='after_cutoff.csv', mime='text/csv')
    st.download_button(label='Reservoir data', data=df_reservoir.to_csv(), file_name='reservoir.csv', mime='text/csv')

with monte_carlo_tab:
    pass