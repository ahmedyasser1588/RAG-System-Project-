from langchain_core.prompts import ChatPromptTemplate


def get_rag_prompt():
    return ChatPromptTemplate.from_template(
        """
You are an engineering Knowledge assistant.
Answer the user's question using ONLY the provided contexts.

If the context doesn't contain enough information to answer the question, say that the available knowledge base doesn't contain enough evidence.
Do not invent facts.

Context:
<context>
{context}
</context>

Question:
{question}

Answer:
"""
    )
