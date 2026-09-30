import streamlit as st
from datetime import date
from io import BytesIO
from docx import Document
from reportlab.pdfgen import canvas

st.set_page_config(page_title="LegalEase", page_icon="⚖️")

st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

st.info("Create and download a legal document draft. This is for educational purposes and is not legal advice.")

document_type = st.selectbox(
    "Select Document Type",
    [
        "Employment Contract",
        "Rental Agreement",
        "Non-Disclosure Agreement",
        "Business Agreement",
        "Leave Letter",
        "Custom Legal Document"
    ],
    key="document_type"
)

first_party = st.text_input("First Person", key="first_party")
second_party = st.text_input("Company Name", key="second_party")
start_date = st.date_input("Start Date", value=date.today(), key="start_date")
terms = st.text_area("Terms and Conditions", key="terms")

if st.button("Generate Document", key="generate"):
    if not first_party.strip() or not second_party.strip() or not terms.strip():
        st.warning("Please fill in all the details.")
    else:
        st.session_state["document"] = f"""
{document_type}

Date: {start_date}

First Party: {first_party}
Second Party: {second_party}

Terms and Conditions:
{terms}

Note: This is a draft for educational purposes.
Please obtain professional legal review before use.
"""
        st.success("Document generated!")

if "document" in st.session_state:
    st.subheader("Document Preview")
    edited_document = st.text_area(
        "Edit your document",
        value=st.session_state["document"],
        height=300,
        key="edited_document"
    )

    st.download_button(
        "Download TXT",
        data=edited_document,
        file_name="LegalEase_Document.txt",
        mime="text/plain"
    )

    doc = Document()
    doc.add_heading(document_type, 0)
    doc.add_paragraph(edited_document)
    docx_buffer = BytesIO()
    doc.save(docx_buffer)

    st.download_button(
        "Download DOCX",
        data=docx_buffer.getvalue(),
        file_name="LegalEase_Document.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer)
    text_object = pdf.beginText(50, 800)
    text_object.setFont("Helvetica", 10)

    for line in edited_document.splitlines():
        if text_object.getY() < 50:
            pdf.drawText(text_object)
            pdf.showPage()
            text_object = pdf.beginText(50, 800)
            text_object.setFont("Helvetica", 10)
        text_object.textLine(line[:110])

    pdf.drawText(text_object)
    pdf.save()

    st.download_button(
        "Download PDF",
        data=pdf_buffer.getvalue(),
        file_name="LegalEase_Document.pdf",
        mime="application/pdf"
    )

st.divider()
st.caption("LegalEase | BCA Project 2")