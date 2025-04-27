import streamlit as st
import sqlite3
import os
from datetime import datetime
import time

# === Setup ===
UPLOAD_DIR = "uploads"
DB_PATH = "pptx_files.db"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# === SQLite Setup ===
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS pptx_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            size_mb REAL,
            upload_time TEXT,
            path TEXT
        )
    """)
    conn.commit()
    return conn, c

# === Streamlit UI ===
st.set_page_config(page_title="PowerPoint Annotation Tool", layout="wide")
st.title("🧠 PowerPoint Annotation Tool")
st.caption("Upload a PowerPoint file to begin annotating slides.")

# === File Upload ===
uploaded_file = st.file_uploader("Choose a PowerPoint file", type=["pptx"])

if uploaded_file:
    with st.spinner("Processing PowerPoint file..."):
        conn, c = init_db()

        # Save file
        save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        file_size_mb = round(len(uploaded_file.getbuffer()) / (1024 * 1024), 2)

        # Insert metadata
        c.execute("""
            INSERT INTO pptx_files (filename, size_mb, upload_time, path)
            VALUES (?, ?, ?, ?)
        """, (uploaded_file.name, file_size_mb, datetime.now().isoformat(), save_path))
        conn.commit()
        conn.close()

        # Simulate processing delay
        time.sleep(2)

        st.success(f"✅ {uploaded_file.name} uploaded ({file_size_mb} MB) and processed!")

# === File List ===
st.subheader("📁 Uploaded Files")
conn, c = init_db()
c.execute("SELECT filename, size_mb, upload_time FROM pptx_files ORDER BY upload_time DESC")
rows = c.fetchall()
conn.close()

if rows:
    for filename, size, timestamp in rows:
        st.markdown(f"🗂 **{filename}** — {size} MB — _{timestamp}_")
else:
    st.info("No files uploaded yet.")
