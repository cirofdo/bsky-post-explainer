from backend.app.bluesky import bsky_client_auth, fetch_post, search_posts
from backend.app.llm import (
    openai_client_auth,
    generate_queries,
    extract_entities,
    summarize,
    embed,
    cosine_similarity,
)


def explain(post_url: str) -> str:
    """
    Full agent pipeline:
    1. Fetch the post from Bluesky
    2. Generate contextual search queries via LLM
    3. Search Bluesky using each query to gather context
    4. Synthesize a bullet-point explanation via LLM
    """
    bsky_client = bsky_client_auth()
    llm_client = openai_client_auth()

    # 1. Fetch post
    post = fetch_post(bsky_client, post_url)
    post_text = post.record.text

    # 2. Generate search queries and entities
    queries = generate_queries(llm_client, post_text)
    entities = extract_entities(llm_client, post_text)

    # 3. Rank the queries
    post_text_vector = embed(llm_client, post_text)
    post_text_vector = post_text_vector.data[0].embedding

    all_texts = queries + entities
    result = embed(llm_client, all_texts)

    all_candidates = [
        (text, item.embedding)
        for text, item in zip(all_texts, result.data)
    ]

    scored = []
    for candidate_text, candidate_vector in all_candidates:
        similarity = cosine_similarity(post_text_vector, candidate_vector)
        scored.append((similarity, candidate_text))
    top_scored = [s for _, s in scored[:3]]
    print(top_scored)

    # 4. Search Bluesky for each query
    context = []
    context_texts = []

    for query in top_scored:
        results = search_posts(bsky_client, query, limit=2)
        context.extend(results)

    for i in range(len(context)):
        context_texts.append(context[i].record.text)

    # 5. Synthesize explanation
    summary = summarize(llm_client, post_text, context_texts)

    return summary
