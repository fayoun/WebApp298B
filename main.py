import streamlit as st
import pandas as pd
import dbconnect
import folium
from streamlit_folium import st_folium, folium_static


def listing(list_address):
    st.sidebar.header('Listing information')
    ticker = st.sidebar.selectbox(
        'select the address to verify amenities',
        list_address)
    button = st.sidebar.button("upload available amenities")
    return ticker, button


def main():
    username = st.sidebar.text_input('username')
    #username = 'bobby'
    mydb = dbconnect.connect_db()
    cursor = mydb.cursor()
    cursor.execute(
        "SELECT A.ADDRESSID, A.LONGITUDE, A.LATITUDE, CONCAT(A.STREET1, ' ',A.STREET2,' ', A.CITY, ' ',A.STATE, ' ',A.ZIPCODE) FROM ADDRESS A, USER_LIST B WHERE A.USERID = B.USERID and B.USERNAME = %s;",
        [username])

    df = pd.DataFrame(cursor.fetchall(), columns=['ADDRESSID', 'longitude', 'latitude', 'ADDRESS'])
    # mappoint = df[['latitude', 'latitude']]
    list_address = list(df['ADDRESS'])
    listing(list_address)

    m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()],
                   zoom_start=10, control_scale=True)

    # Loop through each row in the dataframe
    for i, row in df.iterrows():
        # Setup the content of the popup
        iframe = folium.IFrame('address:' + str(row["ADDRESS"]))

        # Initialise the popup using the iframe
        popup = folium.Popup(iframe, min_width=300, max_width=300)

        # Add each row to the map
        folium.Marker(location=[row['latitude'], row['longitude']],
                      popup=popup, c=row['ADDRESS']).add_to(m)

    st_data = st_folium(m, width=300)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
