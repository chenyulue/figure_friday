import os
import streamlit as st


pages24 = []
for file in os.listdir("./ff24"):
    name, _ = os.path.splitext(file)
    pages24.append(
        st.Page(f"ff24/{file}", title=name, url_path=name)
    )

pages = {
    "": [st.Page("Home.py", title="Home")],
    "Figure Friday 2024": pages24,
}

pg = st.navigation(pages)

pg.run()