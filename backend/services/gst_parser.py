import io
import re
from typing import Any, Dict

import pdfplumber


GSTIN_PATTERN = r"\b\d{2}[A-Z]{5}\d{4}[A-Z][A-Z\d][Z][A-Z\d]\b"
AMOUNT_PATTERN = r"(?:Total|Grand Total|Amount Due|Invoice Value)[:\s]*₹?\s*([\d,]+\.?\d*)"


def extract_gst_from_pdf(pdf_bytes: bytes) -> Dict[str, Any]:
    """
    Extract GSTIN and a best-effort total invoice amount from a PDF.
    Returns zero values when extraction fails so scheduler jobs can continue.
    """
    full_text = ""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            full_text = "\n".join((page.extract_text() or "") for page in pdf.pages)
    except Exception:
        return {
            "vendor_gstin": None,
            "total_value": 0.0,
            "raw_text_preview": "",
        }

    gstin_match = re.search(GSTIN_PATTERN, full_text)
    amounts = re.findall(AMOUNT_PATTERN, full_text, re.IGNORECASE)
    total_value = 0.0
    if amounts:
        try:
            total_value = float(amounts[-1].replace(",", ""))
        except ValueError:
            total_value = 0.0

    return {
        "vendor_gstin": gstin_match.group(0) if gstin_match else None,
        "total_value": total_value,
        "raw_text_preview": full_text[:500],
    }
