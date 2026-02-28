from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from core.llm import get_llm
from memory.session_memory import get_history, add_message


SYSTEM_PROMPT = """
You are an expert YouTube video assistant. Your primary goal is to provide comprehensive, detailed, and accurate answers based EXCLUSIVELY on the provided transcript context.

Instructions:
1. Thoroughly analyze the user's question against the provided chronological video transcript.
2. Synthesize a detailed, fluent, and coherent response. Provide rich context; do not be overly brief.
3. ALWAYS cite specific timestamps from the transcript to support your claims (e.g., "[01:23-01:45] The speaker mentions...").
4. If the topic is not discussed in the transcript context, state clearly that you cannot answer based on the video. Do NOT hallucinate information.
"""


def format_context(docs):
    formatted = []
    for d in docs:
        try:
            start = int(float(d.metadata.get("start", 0)))
            duration = int(float(d.metadata.get("duration", 0)))
            end = start + duration
        except (ValueError, TypeError):
            continue

        start_m, start_s = divmod(start, 60)
        end_m, end_s = divmod(end, 60)

        timestamp = f"{start_m:02d}:{start_s:02d}-{end_m:02d}:{end_s:02d}"
        formatted.append(f"[{timestamp}] {d.page_content}")

    return "\n".join(formatted)


def format_metadata(docs):
    if not docs:
        return ""
    d = docs[0]
    title = d.metadata.get("title", "")
    channel = d.metadata.get("channel", "")
    views = d.metadata.get("views", "")
    published_at = d.metadata.get("published_at", "")
    description = d.metadata.get("description", "")
    
    meta_lines = []
    if title: meta_lines.append(f"Video Title: {title}")
    if channel: meta_lines.append(f"Channel: {channel}")
    if views: meta_lines.append(f"Views: {views}")
    if published_at: meta_lines.append(f"Published At: {published_at}")
    if description: meta_lines.append(f"Description:\n{description}")
    
    if meta_lines:
        return "\n".join(meta_lines) + "\n\n"
    return ""


def generate_answer(session_id, question, docs):

    llm = get_llm()

    def get_start_time(d):
        try:
            return float(d.metadata.get("start", 0))
        except (ValueError, TypeError):
            return 0.0

    # Sort documents chronologically by their start time
    sorted_docs = sorted(docs, key=get_start_time)
    video_metadata_str = format_metadata(sorted_docs)
    context = format_context(sorted_docs)
    chat_history = get_history(session_id)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        SystemMessage(content=f"Video Metadata:\n{video_metadata_str}Transcript Context:\n{context}")
    ]

    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=question))

    response = llm.invoke(messages)

    add_message(session_id, "user", question)
    add_message(session_id, "assistant", response.content)

    return response.content