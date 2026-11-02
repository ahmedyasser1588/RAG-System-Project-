import streamlit as st
from Src.Config.Settings import settings
from Src.Application.rag_service import RAGService

st.set_page_config(page_title="Engineering Knowledge Base", page_icon="🤖")
st.title("🤖 Engineering Knowledge Assistant")
st.caption("Ask questions about engineering architecture, runbooks, APIs, and incidents.")

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

# Sample questions from evaluation dataset
sample_questions = [
    "Why does the platform use Kafka for payment events instead of RabbitMQ?",
    "What is the current authentication mechanism for the Orders API?",
    "How do I roll back the Payment Service in production?",
    "What caused the duplicate payment charge incident?",
    "Where should production secrets be stored?",
    "What should a client do when it receives HTTP 429?",
    "Why does the search platform use two retrieval stages?",
    "What should I check first when Kafka consumer lag increases?",
]

if "user_question" not in st.session_state:
    st.session_state.user_question = ""


def on_sample_change():
    chosen = st.session_state.sample_selector
    if chosen != "-- Choose a sample question --":
        st.session_state.user_question = chosen


st.markdown("##### 💡 Try a sample question:")
st.selectbox(
    label="Sample Questions",
    options=["-- Choose a sample question --"] + sample_questions,
    key="sample_selector",
    on_change=on_sample_change,
    label_visibility="collapsed",
)

# Quick clickable shortcuts
col1, col2, col3 = st.columns(3)
if col1.button("⚡ Kafka Architecture", use_container_width=True):
    st.session_state.user_question = sample_questions[0]
    st.rerun()

if col2.button("🔐 Orders API Auth", use_container_width=True):
    st.session_state.user_question = sample_questions[1]
    st.rerun()

if col3.button("🚨 Payment Rollback", use_container_width=True):
    st.session_state.user_question = sample_questions[2]
    st.rerun()

question = st.text_input(
    label="What is your question?",
    key="user_question",
    placeholder="Type your question or choose one from the samples above...",
)

if st.button("Ask RAG", type="primary"):
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
                with st.expander(f"📄 {source['source']}"):
                    st.write(source["content"])

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
