import streamlit as st
import io
import fitz
import openai
import os

openai.api_key = os.getenv("API_KEY")

# Initialize session state
if "widget_outputs" not in st.session_state:
    st.session_state.widget_outputs = {
        "Widget 1": "",
        "Widget 2": "",
        "Widget 3": "",
        "Widget 4": "",
    }

def generate_pdf(sections):
    # Create a new PDF document
    doc = fitz.open()

    # Define the style for the section headings and text
    style_heading = "<style>\nh1 {font-family: Arial, sans-serif; font-size: 20pt; font-weight: bold; color: #000000;}\n</style>"
    style_text = "<style>\np {font-family: Arial, sans-serif; font-size: 12pt; color: #000000;}\n</style>"

    # Define the page template for each section
    template = style_heading + style_text + "<h1>{}</h1><p>{}</p>"

    # Add a new page for each section
    for section in sections:
        if ":" in section:
            heading, text = section.split(":", 1)
        else:
            heading, text = section, ""
    # rest of the code

        # Create a new page
    page = doc.new_page()

    # Draw the section heading and text on the page
    p1 = fitz.Point(50, 100)
    p2 = fitz.Point(50, 150)
    page.insert_text(p1, heading, fontname="Arial", fontsize=20)
    page.insert_text(p2, text, fontname="Arial", fontsize=12)

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


# Define the expandable widgets
def app():
    # Set the app title
    st.title("QuickBOM.ai")

    widget1 = st.expander("Widget 1")
    widget2 = st.expander("Widget 2")
    widget3 = st.expander("Widget 3")
    widget4 = st.expander("Widget 4")

    # Define the query text area and submit button
    query = st.sidebar.text_area("Ask Something", key="query")
    submit = st.sidebar.button("Submit")

    # Define the widget selection drop-down
    widget_select = st.sidebar.selectbox("Select a widget", ["Widget 1", "Widget 2", "Widget 3", "Widget 4"])

    # Generate text and display in the selected widget
    if submit:
        with st.spinner('Generating...'):
            output = generate_text(query)

            # Update the selected widget output in session state
            st.session_state.widget_outputs[widget_select] = output

            # Update all the widget outputs
            widget1.write(st.session_state.widget_outputs["Widget 1"])
            widget2.write(st.session_state.widget_outputs["Widget 2"])
            widget3.write(st.session_state.widget_outputs["Widget 3"])
            widget4.write(st.session_state.widget_outputs["Widget 4"])

    # Collect the outputs of all the widgets into a list
    widget_outputs = [
        st.session_state.widget_outputs["Widget 1"],
        st.session_state.widget_outputs["Widget 2"],
        st.session_state.widget_outputs["Widget 3"],
        st.session_state.widget_outputs["Widget 4"],
    ]

    # Add a button to generate the PDF file
    if st.button("Generate PDF"):
        # Generate the PDF file
        buffer = generate_pdf(widget_outputs)

        # Download the PDF file
        st.download_button(
            label="Download PDF",
            data=buffer,
            file_name="example.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    app()
