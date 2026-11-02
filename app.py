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

st.sidebar.markdown(f"**Model:** `{settings.llm_model_name}`")
retriever_type = st.sidebar.radio(
    label="Pick Retriever Type",
    options=["similarity", "hybrid", "mmr"],
)

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
            err_msg = str(e)
            if "NotFoundError" in type(e).__name__ or "model_not_found" in err_msg or "404" in err_msg:
                st.error(
                    f"⚠️ **Model Not Found on Groq!** (`{settings.llm_model_name}`)\n\n"
                    "The model specified does not exist in Groq.\n"
                    "Please update `llm_model_name` in **Streamlit Cloud → Settings → Secrets** to:\n"
                    "```toml\n"
                    'llm_model_name = "llama-3.3-70b-versatile"\n'
                    "```\n"
                    "Other supported models: `llama-3.1-8b-instant`, `mixtral-8x7b-32768`."
                )
            else:
                st.error(f"⚠️ Error: {err_msg}")
