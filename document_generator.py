import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)


def sample_document(document_type, details):

    if document_type == "Employment Contract":
        return f"""EMPLOYMENT CONTRACT

Employer:
ABC Company

Employee:
Kumar

Position:
Software Developer

Salary:
Rs. 25,000 per month

Start Date:
1 October 2026

TERMS AND CONDITIONS

1. The employee agrees to perform the duties assigned by the employer.
2. The employee shall follow the rules and policies of the organization.
3. Salary shall be paid according to the agreed employment terms.
4. Any changes to this agreement should be made in writing.

Employee Signature: __________________

Employer Signature: __________________

Date: __________________

This document is an AI-generated draft and should be reviewed by a qualified legal professional before use.
"""

    if document_type == "Rental Agreement":
        return f"""RENTAL AGREEMENT

This Rental Agreement is prepared based on the following details:

{details}

TERMS AND CONDITIONS

1. The tenant agrees to pay the agreed rent on time.
2. The property shall be used for lawful purposes.
3. The tenant shall maintain the property properly.
4. Any changes to this agreement should be made in writing.

Tenant Signature: __________________

Landlord Signature: __________________

Date: __________________

This document is an AI-generated draft and should be reviewed by a qualified legal professional before use.
"""

    if document_type == "Non-Disclosure Agreement":
        return f"""NON-DISCLOSURE AGREEMENT

PARTIES AND DETAILS

{details}

CONFIDENTIALITY

1. The receiving party agrees to keep confidential information private.
2. Confidential information shall not be disclosed to unauthorized persons.
3. Confidential information shall only be used for the agreed purpose.

Party 1 Signature: __________________

Party 2 Signature: __________________

Date: __________________

This document is an AI-generated draft and should be reviewed by a qualified legal professional before use.
"""

    if document_type == "Business Agreement":
        return f"""BUSINESS AGREEMENT

PARTIES AND DETAILS

{details}

TERMS AND CONDITIONS

1. Both parties agree to perform their agreed responsibilities.
2. Each party shall comply with the terms of this agreement.
3. Any amendments should be made in writing.
4. Disputes should be handled according to the agreed terms.

Party 1 Signature: __________________

Party 2 Signature: __________________

Date: __________________

This document is an AI-generated draft and should be reviewed by a qualified legal professional before use.
"""

    if document_type == "Leave Letter":
        return f"""LEAVE LETTER

To,
The Concerned Authority

Subject: Leave Request

Dear Sir/Madam,

I am requesting leave based on the following details:

{details}

I kindly request you to consider and approve my leave.

Thank you.

Yours faithfully,

Name: __________________

Date: __________________

This document is an AI-generated draft and should be reviewed by a qualified legal professional before use.
"""

    return f"""LEGAL DOCUMENT

DOCUMENT DETAILS

{details}

TERMS AND CONDITIONS

1. The parties agree to the information provided in this document.
2. Any important changes should be made in writing.
3. The document should be reviewed before use.

Signature: __________________

Date: __________________

This document is an AI-generated draft and should be reviewed by a qualified legal professional before use.
"""


def generate_document(document_type, details):

    prompt = f"""
You are LegalEase, an AI-powered legal document drafting assistant.

Create a professional draft for:

Document Type:
{document_type}

User Details:
{details}

Requirements:
1. Use clear professional language.
2. Include suitable headings and sections.
3. Use only the information provided.
4. Use placeholders for missing information.
5. Make the document easy to edit.
6. Add a legal review disclaimer at the end.

Return only the document.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception as error:

        error_text = str(error)

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:

            return sample_document(
                document_type,
                details
            )

        if "503" in error_text or "UNAVAILABLE" in error_text:

            return sample_document(
                document_type,
                details
            )

        raise error