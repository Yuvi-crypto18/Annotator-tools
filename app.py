import streamlit as st
import sqlite3
import os
from pptx import Presentation
from PIL import Image
import io
import base64

# --- Initialize SQLite DB ---
def init_db():
    conn = sqlite3.connect("annotations.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS annotations (
        slide_index INTEGER,
        key TEXT,
        value TEXT
    )''')
    conn.commit()
    conn.close()

def save_annotation(slide_index, annotations):
    conn = sqlite3.connect("annotations.db")
    c = conn.cursor()
    c.execute("DELETE FROM annotations WHERE slide_index = ?", (slide_index,))
    for key, value in annotations.items():
        c.execute("INSERT INTO annotations (slide_index, key, value) VALUES (?, ?, ?)",
                  (slide_index, key, value))
    conn.commit()
    conn.close()

def load_annotations(slide_index):
    conn = sqlite3.connect("annotations.db")
    c = conn.cursor()
    c.execute("SELECT key, value FROM annotations WHERE slide_index = ?", (slide_index,))
    results = c.fetchall()
    conn.close()
    return dict(results)

# --- Process uploaded PPTX ---
def pptx_to_images(pptx_file):
    from pdf2image import convert_from_bytes
    from pptx import Presentation
    import tempfile
    import subprocess

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp:
        tmp.write(pptx_file.getbuffer())
        pptx_path = tmp.name
        pdf_path = pptx_path.replace(".pptx", ".pdf")
        
        subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", pptx_path, "--outdir", os.path.dirname(pdf_path)])
        
        images = convert_from_bytes(open(pdf_path, "rb").read())
        return images

# --- Streamlit App ---
st.set_page_config(layout="wide")
init_db()

st.title("PowerPoint Annotation Tool")
pptx_file = st.file_uploader("Upload a PowerPoint (.pptx)", type="pptx")

if pptx_file:
    if "slides" not in st.session_state:
        st.session_state.slides = pptx_to_images(pptx_file)
        st.session_state.slide_index = 0
        st.session_state.annotations = {}

    slides = st.session_state.slides
    slide_index = st.session_state.slide_index
    current_annotations = load_annotations(slide_index)

    # Slide Display
    st.image(slides[slide_index], caption=f"Slide {slide_index + 1} of {len(slides)}", use_column_width=True)

    # Annotation Interface
    st.subheader("Annotations")
    annotations = {}
    key_input = st.text_input("Key")
    value_input = st.text_input("Value")

    if st.button("Add Annotation Field"):
        if key_input and value_input:
            current_annotations[key_input] = value_input

    for k, v in current_annotations.items():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.text_input("Key", value=k, disabled=True, key=f"k_{k}")
        with col2:
            new_value = st.text_input("Value", value=v, key=f"v_{k}")
            annotations[k] = new_value

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous") and slide_index > 0:
            st.session_state.slide_index -= 1
    with col2:
        if st.button("Next") and slide_index < len(slides) - 1:
            st.session_state.slide_index += 1

    if st.button("Submit Current Slide"):
        save_annotation(slide_index, annotations)
        st.success("Annotations saved!")

    if st.button("Submit All Slides"):
        save_annotation(slide_index, annotations)
        st.success("All annotations saved successfully!")

