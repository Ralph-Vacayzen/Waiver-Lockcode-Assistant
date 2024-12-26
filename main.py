import streamlit as st
import pandas as pd

from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title='Lockcode Assistant', page_icon='🔐')

connection = st.connection("gsheets", type=GSheetsConnection)
bike_data  = connection.read(worksheet=st.secrets['spreadsheet']['bike_tab'], ttl="10m")
gart_data  = connection.read(worksheet=st.secrets['spreadsheet']['gart_tab'], ttl="10m")


st.caption('VACAYZEN')
st.title('Lockcode Assistant')
st.success('Thank you for filling out your waiver!')
st.info('Please read the following terms and then enter your passcode to receive your lock combination.')
st.header('Terms & Conditions')

st.subheader('🚲 Bicycles')
"""
🔒 Bikes not being ridden must be locked up.

🏠 Bikes must be returned to the property of origin upon your departure.
"""

st.subheader('🚙 Golf Carts')
"""
🧓🏼 All drivers must be 21 and older with a valid driver's license and proof of insurance.

✍🏼 Note, only authorized drivers who have signed the waiver are able to drive the vehicle.

🚫 Driving on Highway 98 is prohibited.

🐢 Golf Carts can only be driven on roads with a speed limit of 35 MPH or less.

🚚 Failure to abide by the rules and regulations will result in the golf cart being picked up, without compensation, and subject to service fees and/or damage repair costs.

🔒 Please keep the key locked in the lockbox when not in use and upon departure or return.

⛑️ Safety first, always wear seat belts and adhere to the maximum capacity of the vehicle.

🚫 Vehicles are not allowed to drive through the communities of Rosemary Beach Alys Beach or Seacrest Beach East. Please check with your property management company on any neighborhood specific rules and regulations. 

"""

st.info('Please enter the passcode provided to you by your property management company.')


code = st.text_input('Passcode')
if st.button('Get Access', icon='🔑', use_container_width=True, type='primary'):

    bf = bike_data[bike_data['ORDER #'].astype(str) == code]
    gf = gart_data[gart_data['ORDER #'].astype(str) == code]

    if len(bf) > 0: st.metric('BIKE LOCK',str(bf[st.secrets['spreadsheet']['bike_lock']].values[0]))
    if len(gf) > 0: st.metric('GART LOCKBOX',str(gf[st.secrets['spreadsheet']['gart_lock']].values[0]))
    if len(bf) == 0 and len(gf) == 0:
        st.warning('Please provide a valid passcode.')