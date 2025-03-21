import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

output_df = pd.DataFrame({
    'timestamp': pd.date_range('2022-01-01', periods=1000, freq='1min'),
    'sensor1': np.random.normal(10, 2, 1000),
    'sensor2': np.random.normal(20, 5, 1000),
    'prediction': np.random.normal(15, 3, 1000)
})

performance_df = pd.DataFrame({
    'model': ['Model A', 'Model B', 'Model C'],
    'accuracy': [0.85, 0.92, 0.78],
    'latency': [50, 60, 80],
    'power_consumption': [100, 120, 150]
})

device_params = {
    'data_collection': True,
    'model_params': {
        'learning_rate': 0.001,
        'batch_size': 32,
        'num_epochs': 10
    },
    'device_commands': ['reset', 'calibrate']
}

st.set_page_config(page_title='Device Observing Dashboard')

st.title('Device Observing Dashboard')
st.subheader('Device Output')
device_output = st.empty()
device_output.dataframe(output_df)

st.subheader('Data Visualization')
chart_type = st.selectbox('Select Chart Type', ['Line Chart', 'Scatter Plot'])
if chart_type == 'Line Chart':
    st.line_chart(output_df.set_index('timestamp'))
else:
    scatter_chart = alt.Chart(output_df).mark_circle().encode(
        x='sensor1',
        y='sensor2',
        color='prediction',
        tooltip=['sensor1', 'sensor2', 'prediction']
    ).interactive()
    st.altair_chart(scatter_chart, use_container_width=True)

st.subheader('Model Performance')
st.dataframe(performance_df)

st.subheader('Device Control')
st.checkbox('Enable Data Collection', value=device_params['data_collection'])
st.slider('Learning Rate', min_value=0.001, max_value=0.1, step=0.001, value=device_params['model_params']['learning_rate'])
st.slider('Batch Size', min_value=16, max_value=128, step=16, value=device_params['model_params']['batch_size'])
st.slider('Number of Epochs', min_value=1, max_value=20, step=1, value=device_params['model_params']['num_epochs'])
st.multiselect('Device Commands', options=device_params['device_commands'], default=device_params['device_commands'])
