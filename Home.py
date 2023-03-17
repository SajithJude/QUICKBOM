import streamlit as st
import io
import fitz
import openai
import os

openai.api_key = os.getenv("API_KEY")


def generate_pdf(text):
    # Create a new PDF document
    doc = fitz.open()

    # Add a new page to the document
    page = doc.new_page()
    p = fitz.Point(50, 72)

    # Draw some text on the page
    page.insert_text(p, text)

    # Save the document to a buffer
    buffer = io.BytesIO()
    doc.save(buffer)

    # Close the document
    doc.close()

    # Set the buffer position to the beginning
    buffer.seek(0)

    return buffer


def generate_text(input):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=input,
        temperature=0.56,
        max_tokens=2066,
        top_p=1,
        frequency_penalty=0.35,
        presence_penalty=0
    )
    return response.choices[0].text


def app():
    # Set the app title
    st.title("QuickBOM.ai")

    # Add expandable widgets to display generated text
    expanders = {}
    for i in range(4):
        with st.beta_expander(f"Output {i+1}"):
            expanders[i] = st.empty()

    # Add a button to generate the PDF file
    if st.button("Generate PDF"):
        # Generate the PDF file
        text = "Hello, World!"
        buffer = generate_pdf(text)

        # Download the PDF file
        st.download_button(
            label="Download PDF",
            data=buffer,
            file_name="example.pdf",
            mime="application/pdf"
        )

    # Add a sidebar to generate text
    query = st.sidebar.text_area("Ask Something", key="query")
    submit = st.sidebar.button("Submit")
    if submit:
        with st.spinner('Generating...'):
            # Generate text and display it in the selected expander
            for i in range(4):
                if expanders[i].button(f"Select Region {i+1}"):
                    output = generate_text(query)
                    expanders[i].write(output)
                    break

if __name__ == "__main__":
    app()
