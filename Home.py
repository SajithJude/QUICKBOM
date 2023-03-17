import streamlit as st
import io
import fitz
import openai
import time
import os

openai.api_key =  os.getenv("API_KEY")


def simulate_typing_in_textarea(text_input):
    for char in text_input:
        st.text_area("Type here", value=text_input[:text_input.index(char)] + char, height=200, key=char)
        time.sleep(0.1)
    st.text_area("Type here", value=text_input, height=200)




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


def Generate_text(input):
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


    col1, col2 = st.columns(2)

    
    # text = col1.text_area("Write something")

    # Add a button to generate the PDF file
    if col1.button("Generate PDF"):
        # Generate the PDF file
        buffer = generate_pdf(text)

        # Download the PDF file
        st.download_button(
            label="Download PDF",
            data=buffer,
            file_name="example.pdf",
            mime="application/pdf"
        )


    query = st.sidebar.text_area("Ask Something",key="query")
    submit = st.sidebar.button("Submit")
    if submit:
        with st.spinner('Generating...'):
            output = Generate_text(query)
            st.write(output)
            # simulate_typing_in_textarea(outpsut)



if __name__ == "__main__":
    app()
