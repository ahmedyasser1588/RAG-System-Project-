import streamlit as st
from Src.Config.Settings import settings
from Src.Application.rag_service import RAGService

st.set_page_config(page_title="Engineering Knowledge Base", page_icon="🤖")
st.title("🤖 Engineering Knowledge Assistant")

if not settings.llm_api_key:
    st.error(
        "⚠️ **Groq API Key missing!**\n\n"
        "Please add `llm_api_key` to your `.env` locally or in **Streamlit Cloud Settings → Secrets**."
    )
    st.stop()


@st.cache_resource
def get_rag() -> RAGService:
    return RAGService()


rag = get_rag()

retriever_type = st.sidebar.radio(
    label="Pick Retriever Type",
    options=["similarity", "hybrid", "mmr"],
)

question = st.text_input("What is your question?")

if st.button("Ask RAG"):
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Thinking..."):
            answer = rag.ask(question, retriever_type=retriever_type)

        st.subheader("Answer:")
        st.write(answer["answer"])

        st.subheader("Sources:")
        for source in answer["sources"]:
            with st.expander(source["source"]):
                st.write(source["content"])
