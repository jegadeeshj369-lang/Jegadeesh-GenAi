import streamlit as st
from io import BytesIO

from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import mm

from backend.main import create_legal_document


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")


# -----------------------------
# DOCUMENT TYPE
# -----------------------------

document_type = st.selectbox(
    "Select Document Type",
    [
        "Employment Contract",
        "Rental Agreement",
        "Non-Disclosure Agreement",
        "Business Agreement",
        "Leave Letter",
        "Custom Legal Document"
    ]
)


# -----------------------------
# DETAILS
# -----------------------------

details = st.text_area(
    "Enter Document Details",
    height=250,
    placeholder="Enter names, dates, terms and other required information..."
)


# -----------------------------
# DOCX CREATOR
# -----------------------------

def create_docx(text):
    document = Document()

    for line in text.split("\n"):
        document.add_paragraph(line)

    file = BytesIO()
    document.save(file)
    file.seek(0)

    return file


# -----------------------------
# PDF CREATOR
# -----------------------------

def create_pdf(text):

    file = BytesIO()

    pdf = SimpleDocTemplate(
        file,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    normal_style = styles["BodyText"]
    normal_style.fontName = "Helvetica"
    normal_style.fontSize = 11
    normal_style.leading = 16
    normal_style.alignment = TA_LEFT

    title_style = styles["Title"]
    title_style.fontName = "Helvetica-Bold"
    title_style.fontSize = 16
    title_style.leading = 20

    story = []

    lines = text.split("\n")

    for index, line in enumerate(lines):

        line = line.strip()

        if not line:
            story.append(Spacer(1, 8))
            continue

        line = line.replace("₹", "Rs.")

        if index == 0:
            story.append(
                Paragraph(line, title_style)
            )
        else:
            story.append(
                Paragraph(line, normal_style)
            )

    pdf.build(story)

    file.seek(0)

    return file


# -----------------------------
# GENERATE DOCUMENT
# -----------------------------

if st.button("Generate Document"):

    if not details.strip():

        st.warning("Please enter the document details.")

    else:

        with st.spinner("Generating your document..."):

            try:

                document = create_legal_document(
                    document_type,
                    details
                )

                st.success(
                    "Document generated successfully!"
                )

                st.subheader("📄 Document Preview")

                edited_document = st.text_area(
                    "Edit Document",
                    value=document,
                    height=500
                )


                # -----------------------------
                # DOWNLOAD BUTTONS
                # -----------------------------

                col1, col2, col3 = st.columns(3)


                with col1:

                    st.download_button(
                        "📄 Download TXT",
                        data=edited_document,
                        file_name="LegalEase_Document.txt",
                        mime="text/plain"
                    )


                with col2:

                    docx_file = create_docx(
                        edited_document
                    )

                    st.download_button(
                        "📝 Download DOCX",
                        data=docx_file,
                        file_name="LegalEase_Document.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )


                with col3:

                    pdf_file = create_pdf(
                        edited_document
                    )

                    st.download_button(
                        "📕 Download PDF",
                        data=pdf_file,
                        file_name="LegalEase_Document.pdf",
                        mime="application/pdf"
                    )


            except Exception as e:

                st.error(
                    f"Error: {e}"
                )


