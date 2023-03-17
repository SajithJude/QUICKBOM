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

    # Define the expandable widgets
    expanders = {
        "Widget 1": st.expander("Widget 1"),
        "Widget 2": st.expander("Widget 2"),
        "Widget 3": st.expander("Widget 3"),
        "Widget 4": st.expander("Widget 4")
    }

    # Define the widget selection drop-down
    widget_select = st.sidebar.selectbox("Select a widget", list(expanders.keys()))

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

    # Define the query text area and submit button
    query = st.sidebar.text_area("Ask Something", key="query")
    submit = st.sidebar.button("Submit")

    # Generate text and display in the selected widget
    if submit:
        with st.spinner('Generating...'):
            output = generate_text(query)
            expanders[widget_select].write(output)

            # Store the output in a variable for future use
            if widget_select == "Widget 1":
                widget1_output = output
            elif widget_select == "Widget 2":
                widget2_output = output
            elif widget_select == "Widget 3":
                widget3_output = output
            elif widget_select == "Widget 4":
                widget4_output = output


if __name__ == "__main__":
    app()
