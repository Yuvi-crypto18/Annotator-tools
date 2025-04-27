import streamlit as st
import sqlite3
import io
from PIL import Image

# --- DB Functions ---
def get_slides():
    conn = sqlite3.connect("your_database.db")
    cur = conn.cursor()
    cur.execute("SELECT slide_id, slide_number, name, image FROM input ORDER BY slide_number")
    slides = cur.fetchall()
    conn.close()
    return slides

def get_annotations(slide_id):
    conn = sqlite3.connect("your_database.db")
    cur = conn.cursor()
    cur.execute("SELECT key, value FROM annotations WHERE slide_id = ?", (slide_id,))
    rows = cur.fetchall()
    conn.close()
    return dict(rows)

def save_annotations(slide_id, annotations):
    conn = sqlite3.connect("your_database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM annotations WHERE slide_id = ?", (slide_id,))
    for key, value in annotations.items():
        cur.execute("INSERT INTO annotations (slide_id, key, value) VALUES (?, ?, ?)",
                    (slide_id, key, value))
    conn.commit()
    conn.close()

# --- App Setup ---
st.set_page_config(layout="wide")
st.title("Slide Annotation Viewer")

slides = get_slides()
if not slides:
    st.warning("No slides found in the database.")
    st.stop()

if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0

slide_id, slide_number, presentation_name, image_blob = slides[st.session_state.slide_index]

# Show slide
st.markdown(f"### {presentation_name} - Slide {slide_number}")
image = Image.open(io.BytesIO(image_blob))
st.image(image, use_column_width=True)

# Load existing annotations
annotations = get_annotations(slide_id)

st.subheader("Annotations")
new_annotations = {}

# Dynamic fields for existing annotations
for k, v in annotations.items():
    new_value = st.text_input(f"{k}", value=v, key=f"annot_{k}")
    new_annotations[k] = new_value

# Add new key-value field
new_key = st.text_input("New Key", key="new_key")
new_value = st.text_input("New Value", key="new_value")
if st.button("Add Annotation Field"):
    if new_key and new_value:
        new_annotations[new_key] = new_value

# Save
if st.button("Submit Current Slide"):
    save_annotations(slide_id, new_annotations)
    st.success("Annotations saved!")

# Navigation
col1, col2 = st.columns(2)
with col1:
    if st.button("Previous") and st.session_state.slide_index > 0:
        st.session_state.slide_index -= 1
with col2:
    if st.button("Next") and st.session_state.slide_index < len(slides) - 1:
        st.session_state.slide_index += 1
