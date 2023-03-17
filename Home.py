import streamlit as st
import io
import fitz
import openai

openai.api_key =  os.getenv("API_KEY")


def simulate_typing(text):
    for char in text:
        st.write(char, end='', flush=True)
        time.sleep(0.1)
    st.write('')



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

    
    text = col1.text_area("Write something")

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


if __name__ == "__main__":
    app()
