# PowerPoint Annotation Tool

This Streamlit app lets users upload a PowerPoint (.pptx), view each slide, and add editable annotations to each slide.
Annotations are saved locally using SQLite, making it easy to manage notes across slides.

## Features

1. Upload .pptx files and convert slides to images.

2. View slides one by one with easy Previous and Next navigation.

3. Add key-value annotations to any slide.

4. Save annotations per slide or for the entire deck.

5. Persistent storage of annotations with a lightweight SQLite database.

6. Built with Streamlit, python-pptx, pdf2image, and LibreOffice (for conversion).

## Setup
```bash
pip install streamlit sqlite3 python-pptx pdf2image Pillow
```
Make sure LibreOffice is installed on your system for pptx to pdf conversion:

```bash
sudo apt install libreoffice
```
Run the app:

```bash
streamlit run app.py
```
