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

# Supported models on your Groq key
available_models = [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "qwen/qwen3.8-27b",
    "allam-2-7b",
]

default_index = 0
if settings.llm_model_name in available_models:
    default_index = available_models.index(settings.llm_model_name)

selected_model = st.sidebar.selectbox(
    label="LLM Model",
    options=available_models,
    index=default_index,
)

retriever_type = st.sidebar.radio(
    label="Pick Retriever Type",
    options=["similarity", "hybrid", "mmr"],
)


@st.cache_resource
def get_rag(model_name: str) -> RAGService:
    return RAGService(model_name=model_name)


rag = get_rag(selected_model)

question = st.text_input("What is your question?")

if st.button("Ask RAG"):
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        try:
            with st.spinner("Thinking..."):
                answer = rag.ask(question, retriever_type=retriever_type)

            st.subheader("Answer:")
            st.write(answer["answer"])

            st.subheader("Sources:")
            for source in answer["sources"]:
                with st.expander(source["source"]):
                    st.write(source["content"])

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
