# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title("Customize your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custome smoothie!
    """
)

# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import when_matched

#write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write("""Orders that need to be filled""")

session = get_active_session()
my_dataframe = session.table("smoothies.public.orders")
editable_df = st.experimental_data_editor(my_dataframe)

submited = st.button('Submit')

if submited:
    st.success("Someone clicked the button.", icon="👍")

    og_dataset = session.table("smoothies.public.orders")
    edited_dataset = session.create_dataframe(editable_df)

    try:
        og_dataset.merge(edited_dataset
                         , (og_dataset['order_uid'] == edited_dataset['order_uid'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )
        st.success("Order(s) Updated!", icon="👍")
    except:
        st.write('Something went wrong')

else:
    st.success("There are no pending orders right now", icon="👍")
