import streamlit as st
import pandas as pd

from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title='Lockcode Assistant', page_icon='🔐')

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container
{
    padding-top: 1rem;
    margin-top: 1rem;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


connection = st.connection("gsheets", type=GSheetsConnection)
bike_data  = connection.read(worksheet=st.secrets['spreadsheet']['bike_tab'], ttl="10m")
gart_data  = connection.read(worksheet=st.secrets['spreadsheet']['gart_tab'], ttl="10m")

passcode_col = st.secrets['spreadsheet']['passcode']
bike_data[passcode_col] = bike_data[passcode_col].apply(lambda x: str(int(x)) if pd.notnull(x) else "")
gart_data[passcode_col] = gart_data[passcode_col].apply(lambda x: str(int(x)) if pd.notnull(x) else "")


st.caption('VACAYZEN')
st.title('Lockcode Assistant')
st.success('Thank you for filling out your waiver!')
st.info('Please read the following and then enter your confirmation code to receive your lock combination.')
st.header('Terms & Conditions')

st.subheader('🚲 Bicycles')
"""
🔒 Bikes not being ridden must be locked up.

🏠 Bikes must be returned to the property of origin upon your departure.
"""

st.subheader('🚙 Low Speed Vehicles')
"""
🧓🏼 All drivers must be 21 and older with a valid driver's license and proof of insurance.

✍🏼 Only authorized drivers who have signed the waiver are able to drive the Low Speed Vehicle (LSV).

🚫 Driving an LSV on Highway 98 is prohibited.

🐢 LSVs can only be driven on roads with a speed limit of 35 MPH or less.

🚚 Failure to abide by the rules and regulations will result in the LSV being picked up, without compensation, and subject to service fees and/or damage repair costs.

🔒 Please keep the key locked in the lockbox when not in use and upon departure or return.

⛑️ Safety first, always wear seat belts and adhere to the maximum capacity of the LSV.

🚫 LSVs are not allowed to drive through the communities of: Rosemary Beach, Alys Beach, or Seacrest Beach East. Please check with your property management company on any neighborhood-specific rules and regulations. 
"""

st.info('Please enter the confirmation code provided to you by your property management company.')


code = st.text_input('Confirmation Code')
if st.button('Get Access', icon='🔑', use_container_width=True, type='primary'):

    bf = bike_data[bike_data[passcode_col] == code.strip()]
    gf = gart_data[gart_data[passcode_col] == code.strip()]

    if len(bf) > 0:
        value = str(bf[st.secrets['spreadsheet']['bike_lock']].values[0]).zfill(4)
        st.metric('BIKE LOCK', value)
    if len(gf) > 0:
        value = str(gf[st.secrets['spreadsheet']['gart_lock']].values[0]).zfill(4)
        st.metric('GART LOCKBOX', value)
    if len(bf) == 0 and len(gf) == 0:
        st.warning('Please provide a valid confirmation code.')
