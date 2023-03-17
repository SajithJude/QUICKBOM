import streamlit as st
import io
import fitz

def generate_pdf(word):
    # Create a new PDF document
    doc = fitz.open()

    # Add a new page to the document
    page = doc.new_page()
    p = fitz.Point(50, 72)

   
    # Draw some text on the page
    page.insert_text(p, word)

    # Save the document to a buffer
    buffer = io.BytesIO()
    doc.save(buffer)

    # Close the document
    doc.close()

    # Set the buffer position to the beginning
    buffer.seek(0)

    return buffer

def app():
    # Set the app title
    st.title("PDF Generator")
    
    text = st.text_area("Write something")

    # Add a button to generate the PDF file
    if st.button("Generate PDF"):
        # Generate the PDF file
        buffer = generate_pdf(text)

        # Download the PDF file
        st.download_button(
            label="Download PDF",
            data=buffer,
            file_name="example.pdf",
            mime="application/pdf"
        )


if __name__ == "__main__":
    app()
