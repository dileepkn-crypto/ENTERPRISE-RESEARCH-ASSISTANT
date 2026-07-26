import streamlit as st

from components.sidebar import render_sidebar
from components.page_header import page_header
from components.source_card import source_card

from core.embeddings import EmbeddingService
from core.vector_store import VectorStore
from core.retriever import ResearchRetriever

from core.hybrid_retriever import HybridRetriever
from core.reranker import CrossEncoderReranker
from core.enterprise_retriever import EnterpriseRetriever
from core.relevance_guard import RelevanceGuard
from core.enterprise_rag_pipeline import EnterpriseRAGPipeline

from services.llm_service import LLMService

from utils.helpers import load_css


st.set_page_config(
    page_title="Research Copilot | ResearchIQ",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


load_css()

render_sidebar()


page_header(
    eyebrow="ENTERPRISE RESEARCH ASSISTANT",

    title="Research",

    highlight="Copilot",

    description=(
        "Ask questions across your academic knowledge base "
        "and receive evidence-grounded answers backed by "
        "retrieved research sources."
    )
)


# =========================================================
# YOUR EXISTING PHASE 6 RESEARCH COPILOT CODE CONTINUES HERE
# =========================================================
# =========================================================
# INITIALIZE ENTERPRISE RAG
# =========================================================

@st.cache_resource
def initialize_rag():
    """
    Initialize the complete ResearchIQ Enterprise RAG stack.

    Pipeline:
        Embeddings
            ↓
        Dense Retrieval
            +
        BM25 Retrieval
            ↓
        Reciprocal Rank Fusion
            ↓
        Cross-Encoder Reranking
            ↓
        Relevance Guard
            ↓
        Gemini
    """

    # -----------------------------------------------------
    # Embedding model
    # -----------------------------------------------------

    embedding_service = EmbeddingService()

    # -----------------------------------------------------
    # Vector database
    # -----------------------------------------------------

    vector_store = VectorStore()

    # -----------------------------------------------------
    # Dense semantic retriever
    # -----------------------------------------------------

    dense_retriever = ResearchRetriever(
        embedding_service,
        vector_store
    )

    # -----------------------------------------------------
    # Hybrid Dense + BM25 retriever
    # -----------------------------------------------------

    hybrid_retriever = HybridRetriever(
        dense_retriever,
        vector_store
    )

    # -----------------------------------------------------
    # Cross-encoder reranker
    # -----------------------------------------------------

    reranker = CrossEncoderReranker()

    # -----------------------------------------------------
    # Enterprise retriever
    # -----------------------------------------------------

    enterprise_retriever = EnterpriseRetriever(
        hybrid_retriever,
        reranker
    )

    # -----------------------------------------------------
    # Relevance guard
    # -----------------------------------------------------

    relevance_guard = RelevanceGuard(
        minimum_score=-2.0,
        minimum_relevant_results=1
    )

    # -----------------------------------------------------
    # Gemini
    # -----------------------------------------------------

    llm_service = LLMService()

    # -----------------------------------------------------
    # Enterprise RAG pipeline
    # -----------------------------------------------------

    rag_pipeline = EnterpriseRAGPipeline(
        enterprise_retriever,
        llm_service,
        relevance_guard
    )

    return rag_pipeline, vector_store


# =========================================================
# START AI ENGINE
# =========================================================

try:

    rag, vector_store = initialize_rag()

    vector_count = vector_store.count()

except Exception as exc:

    st.error(
        f"Unable to initialize ResearchIQ Enterprise RAG: {exc}"
    )

    st.stop()


# =========================================================
# SESSION STATE
# =========================================================

if "researchiq_messages" not in st.session_state:

    st.session_state.researchiq_messages = []


# =========================================================
# HEADER
# =========================================================

header_html = (
    '<div class="ri-eyebrow">'
    'ENTERPRISE RESEARCH ASSISTANT'
    '</div>'

    '<div class="ri-title" '
    'style="font-size:3.2rem;">'

    'Research '

    '<span class="ri-gradient">'
    'Copilot'
    '</span>'

    '</div>'

    '<div class="ri-description">'

    'Ask questions across your academic knowledge base. '
    'ResearchIQ combines dense semantic retrieval, BM25, '
    'reciprocal rank fusion, cross-encoder reranking and '
    'evidence-grounded generation to produce traceable '
    'research answers.'

    '</div>'
)

st.markdown(
    header_html,
    unsafe_allow_html=True
)


st.write("")


# =========================================================
# ENTERPRISE RAG STATUS
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Knowledge Vectors",
        vector_count
    )


with col2:

    st.metric(
        "Retrieval",
        "Hybrid"
    )


with col3:

    st.metric(
        "Reranking",
        "Cross-Encoder"
    )


with col4:

    st.metric(
        "Grounding Guard",
        "Active"
    )


# =========================================================
# ENGINE STATUS
# =========================================================

if vector_count > 0:

    st.success(
        f"Enterprise RAG ready · "
        f"{vector_count} knowledge vectors available"
    )

else:

    st.warning(
        "Knowledge base is empty. "
        "Upload and index research papers first."
    )


st.divider()


# =========================================================
# RETRIEVAL ARCHITECTURE
# =========================================================

with st.expander(
    "Enterprise retrieval architecture"
):

    st.markdown(
        """
**ResearchIQ Retrieval Pipeline**

`User Query`

↓

`Dense Semantic Retrieval + BM25 Keyword Retrieval`

↓

`Reciprocal Rank Fusion (RRF)`

↓

`Cross-Encoder Reranking`

↓

`Relevance Guard`

↓

`Evidence Context`

↓

`Gemini`

↓

`Grounded Answer + Citations`
"""
    )

    st.caption(
        "RRF and cross-encoder scores are ranking signals, "
        "not calibrated confidence probabilities."
    )


# =========================================================
# EMPTY CHAT STATE
# =========================================================

if not st.session_state.researchiq_messages:

    st.markdown(
        "## Explore your research knowledge"
    )

    st.caption(
        "Ask a question based on your indexed "
        "academic papers."
    )


    example_col1, example_col2 = st.columns(2)


    with example_col1:

        st.info(
            "What are the main findings of "
            "the indexed research papers?"
        )

        st.info(
            "Explain the methodology used "
            "in the research."
        )


    with example_col2:

        st.info(
            "What role does deep learning play "
            "in mobile applications?"
        )

        st.info(
            "What limitations are identified "
            "by the researchers?"
        )


    st.write("")


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.researchiq_messages:

    role = message.get(
        "role",
        "assistant"
    )

    content = message.get(
        "content",
        ""
    )


    with st.chat_message(role):

        st.markdown(content)


        # -------------------------------------------------
        # Grounding indicator
        # -------------------------------------------------

        if role == "assistant":

            grounded = message.get(
                "grounded"
            )

            if grounded is True:

                st.success(
                    "Grounded in retrieved "
                    "research evidence."
                )

            elif grounded is False:

                st.warning(
                    "Insufficient relevant evidence "
                    "was found in the indexed library."
                )


        # -------------------------------------------------
        # Sources
        # -------------------------------------------------

        sources = message.get(
            "sources",
            []
        )


        if role == "assistant" and sources:

            st.caption(
                "Retrieved Research Evidence"
            )

            for source in sources:

                source_card(
                    source
                )


# =========================================================
# CHAT INPUT
# =========================================================

question = st.chat_input(
    "Ask ResearchIQ about your research..."
)


# =========================================================
# PROCESS QUESTION
# =========================================================

if question:

    # -----------------------------------------------------
    # Validate knowledge base
    # -----------------------------------------------------

    if vector_count == 0:

        st.warning(
            "Your knowledge base is empty. "
            "Upload and index research papers first."
        )

        st.stop()


    # -----------------------------------------------------
    # Store user message
    # -----------------------------------------------------

    user_message = {
        "role": "user",
        "content": question
    }


    st.session_state.researchiq_messages.append(
        user_message
    )


    # -----------------------------------------------------
    # Render user question
    # -----------------------------------------------------

    with st.chat_message("user"):

        st.markdown(
            question
        )


    # -----------------------------------------------------
    # Assistant
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.status(
            "ResearchIQ is analyzing your query...",
            expanded=True
        ) as status:

            try:

                # -----------------------------------------
                # Retrieval
                # -----------------------------------------

                st.write(
                    "Running dense semantic retrieval..."
                )

                st.write(
                    "Running BM25 lexical retrieval..."
                )

                st.write(
                    "Fusing retrieval rankings..."
                )

                st.write(
                    "Cross-encoder reranking evidence..."
                )

                st.write(
                    "Evaluating evidence relevance..."
                )


                # -----------------------------------------
                # Enterprise RAG
                # -----------------------------------------

                result = rag.ask(
                    question,
                    top_k=5
                )


                answer = result.get(
                    "answer",
                    "No answer was generated."
                )


                sources = result.get(
                    "sources",
                    []
                )


                grounded = result.get(
                    "grounded",
                    False
                )


                guard_reason = result.get(
                    "guard_reason",
                    ""
                )


                # -----------------------------------------
                # Complete
                # -----------------------------------------

                if grounded:

                    status.update(
                        label=(
                            "Evidence retrieved and "
                            "answer generated"
                        ),
                        state="complete",
                        expanded=False
                    )

                else:

                    status.update(
                        label=(
                            "Insufficient relevant evidence"
                        ),
                        state="complete",
                        expanded=False
                    )


            except Exception as exc:

                status.update(
                    label="ResearchIQ request failed",
                    state="error",
                    expanded=True
                )

                st.error(
                    f"Enterprise RAG request failed: {exc}"
                )

                st.stop()


        # =================================================
        # ANSWER
        # =================================================

        st.markdown(
            answer
        )


        # =================================================
        # GROUNDING STATUS
        # =================================================

        if grounded:

            st.success(
                "Answer generated from retrieved "
                "research evidence."
            )

        else:

            st.warning(
                "ResearchIQ did not find sufficient "
                "evidence to generate a reliable "
                "document-grounded answer."
            )


        # =================================================
        # GUARD INFORMATION
        # =================================================

        if guard_reason:

            with st.expander(
                "Grounding information"
            ):

                st.write(
                    guard_reason
                )

                st.caption(
                    "The relevance guard evaluates "
                    "cross-encoder ranking scores. "
                    "These scores are not confidence "
                    "probabilities."
                )


        # =================================================
        # SOURCES
        # =================================================

        if sources:

            st.divider()

            st.markdown(
                "### Research Evidence"
            )

            st.caption(
                f"{len(sources)} evidence passages "
                "were used to construct this answer."
            )


            for source in sources:

                source_card(
                    source
                )


    # =====================================================
    # SAVE ASSISTANT MESSAGE
    # =====================================================

    assistant_message = {
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "grounded": grounded,
        "guard_reason": guard_reason
    }


    st.session_state.researchiq_messages.append(
        assistant_message
    )


# =========================================================
# SIDEBAR CHAT CONTROLS
# =========================================================

with st.sidebar:

    st.markdown("---")

    st.markdown(
        "### Copilot Session"
    )


    message_count = len(
        st.session_state.researchiq_messages
    )


    st.caption(
        f"{message_count} messages in "
        "current research session"
    )


    if st.button(
        "Clear Conversation",
        use_container_width=True
    ):

        st.session_state.researchiq_messages = []

        st.rerun()