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
    # Define the PDF template with placeholders for widget outputs
    template = """
    <style>
    .page {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 12pt;
        line-height: 1.5;
        margin: 50px;
    }
    .title {
        font-size: 18pt;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 14pt;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    .widget-output {
        margin-top: 10px;
        margin-bottom: 20px;
    }
    </style>
    <div class="page">
        <div class="title">QuickBOM.ai</div>
        <div class="subtitle">Widget 1</div>
        <div class="widget-output">{widget_1}</div>
        <div class="subtitle">Widget 2</div>
        <div class="widget-output">{widget_2}</div>
        <div class="subtitle">Widget 3</div>
        <div class="widget-output">{widget_3}</div>
        <div class="subtitle">Widget 4</div>
        <div class="widget-output">{widget_4}</div>
    </div>
    """

    # Replace the placeholders with the widget outputs
    template = template.format(
        widget_1=sections[0],
        widget_2=sections[1],
        widget_3=sections[2],
        widget_4=sections[3]
    )

    # Create a new PDF document
    doc = fitz.open()

    # Add a new page for the template
    page = doc.new_page()

    # Draw the template HTML on the page
    html = page.get_pixmap_alpha().add_html(template)

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
