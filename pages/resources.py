import streamlit as st


def app():
    resources = st.container()

    with resources:
        st.header('Resources')
        st.subheader('Official USAPL Website')
        st.write('https://www.usapowerlifting.com/')

        channel1, channel2, channel3 = st.columns(3)

        with channel1:
            st.subheader('Alan Thrall')
            st.text('Powerlifter/Strongman')
            st.video('https://www.youtube.com/watch?v=jEy_czb3RKA')

        with channel2:
            st.subheader('Jeff Nippard')
            st.text('Powerlifter/Trainer')
            st.video('https://www.youtube.com/watch?v=ptpmRrzRtWQ')

        with channel3:
            st.subheader('Russel Orhii')
            st.text('Champion Powerlifter')
            st.video('https://www.youtube.com/watch?v=JNSJZKyc_Lw')