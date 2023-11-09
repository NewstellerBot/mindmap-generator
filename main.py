import base64
import streamlit as st
from trafilatura import fetch_url, extract
from chains import setup_chains
from io import StringIO
from tika import parser


from langchain.text_splitter import CharacterTextSplitter

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

if openai_api_key.startswith("sk-"):
    map_reduce_chain, mind_map_chain = setup_chains(openai_api_key)


text_splitter = CharacterTextSplitter(
    chunk_size=15000,
    chunk_overlap=0,
    length_function=len,
)


def get_content_from_url(url: str) -> str:
    """Parses the html of the website to string"""

    downloaded = fetch_url(url)
    if downloaded is None:
        raise Exception("Could not download the url")

    return extract(downloaded)


def create_summary(content: str) -> str:
    """Creates a summary of the content"""
    split_content = text_splitter.create_documents([content])
    summary = map_reduce_chain.run(split_content)

    return summary


def create_mindmap(summary: str) -> str:
    """Creates a mindmap of the summary"""
    mindmap = mind_map_chain(inputs={"summary": summary})
    print(mindmap["text"])

    return mindmap["text"]


def encode(mindmap: str) -> str:
    """Encodes string into base64"""
    return base64.b64encode(mindmap.encode("utf8")).decode("ascii")


def create_mindmap(summary: str) -> str:
    """Creates a mindmap of the summary"""
    mindmap = mind_map_chain(inputs={"summary": summary})

    return mindmap["text"]


def parse_file(file) -> str:
    """Parses txt or pdf file to string"""

    # txt files
    if file.type == "txt":
        content = StringIO(file.getvalue().decode("utf8"))
    # pdfs
    else:
        parsed = parser.from_buffer(file.getbuffer())
        content = parsed.get("content")

    return content


st.markdown(
    "# Mind Map Generator \n Use an article url or upload a pdf/txt file and generate the summary and mindmap for the text."
)

with st.form("mind_map_form"):
    url = st.text_input("Enter url of the article")
    st.write("or drop a file")
    file = st.file_uploader(
        "Upload a file",
        type=["txt", "pdf"],
    )

    submitted = st.form_submit_button("Submit")

    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your Open API key in side bar!", icon="⚠️")

    if submitted:
        if url and file:
            st.warning("Please enter only one of url or file!", icon="⚠️")
            st.stop()

        # create a variable for the content of pdf/article
        content = None
        # create a variable for summary
        summary = None

        # if url was provided
        if url:
            content = get_content_from_url(url)
        # if file was provided
        elif file:
            content = parse_file(file)
        else:
            st.warning("Please enter a url or pdf!", icon="⚠️")
            st.stop()

        # create summary and mindmap
        if content:
            summary = create_summary(content)

        if summary:
            # display summary
            st.markdown("## Summary")
            st.write(summary)

            # get mindmap code
            mindmap = create_mindmap(summary)

            if mindmap:
                # display img from mermaid
                st.markdown("## Mindmap")
                st.image(f"http://mermaid.ink/img/{encode(mindmap)}")
