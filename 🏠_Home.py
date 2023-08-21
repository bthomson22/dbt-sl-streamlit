# stdlib
import json

# third party
import streamlit as st
import streamlit.components.v1 as components

# first party
from client import get_connection_attributes, submit_query
from jdbc_api import queries

        
def prepare_app():
    
    with st.spinner(f'Gathering Metrics...'):
        df = submit_query(st.session_state.conn, queries['metrics'])
        if df is not None:
            df.columns = [col.lower() for col in df.columns]
            try:
                df.set_index(keys='name', inplace=True)
            except KeyError:
                
                # Query worked, but nothing returned
                st.warning(
                    'No Metrics returned!  Ensure your project has metrics defined '
                    'and a production job has been run successfully.'
                )
            else:
                df['dimensions'] = df['dimensions'].str.split(', ')
                df['queryable_granularities'] = (
                    df['queryable_granularities'].str.split(', ')
                )
                df['type_params'] = df['type_params'].apply(
                    lambda x: json.loads(x) if x else None
                )
                st.session_state.metric_dict = df.to_dict(orient='index')
                st.success('Success!  Explore the rest of the app!')


st.set_page_config(
    page_title="dbt Semantic Layer - Home",
    page_icon="👋",
    
)

st.markdown('# Explore the dbt Semantic Layer')

st.markdown(
    """
    Use this app to query and view the metrics defined in your dbt project. It's important to note that this app assumes that you're using the new
    Semantic Layer, powered by [MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow).  The previous semantic layer used the `dbt_metrics`
    package, which has been deprecated and is no longer supported for `dbt-core>=1.6`.
    
    ---
    
    To get started, input your `JDBC_URL` below.  You can find this in your project settings when setting up the Semantic Layer.
    After hitting Enter, wait until a success message appears indicating that the application has successfully retrieved your project's metrics information.
    """
)


jdbc_url = st.text_input(
    label='JDBC URL',
    value='',
    key='jdbc_url',
    help='JDBC URL is found when configuring the semantic layer at the project level',
)

if st.session_state.jdbc_url != '':
    st.cache_data.clear()
    st.session_state.conn = get_connection_attributes(st.session_state.jdbc_url)
    if 'conn' in st.session_state and st.session_state.conn is not None:
        prepare_app()

st.markdown(
    """
    ---
    **👈 Now, select a page from the sidebar** to explore the Semantic Layer!

    ### Want to learn more?
    - Get started with the [dbt Semantic Layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/quickstart-sl)
    - Understand how to [build your metrics](https://docs.getdbt.com/docs/build/build-metrics-intro)
    - View the [Semantic Layer API](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-api-overview)
    - Brief Demo 👇
"""
)

components.html(
    '''<div style="position: relative; padding-bottom: 77.25321888412017%; height: 0;"><iframe src="https://www.loom.com/embed/90419fc9aa1e4680a43525a386645a96?sid=4c3f76ff-21e5-4a86-82e8-c03489b646d5" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>''',
    height=600
)
