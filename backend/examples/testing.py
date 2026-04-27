# %%
from backend.app.bluesky import bsky_client_auth, fetch_post, search_posts
from backend.app.llm import (
    openai_client_auth,
    generate_queries,
    extract_entities,
    summarize,
    embed,
    cosine_similarity,
)

# %%
bsky_client = bsky_client_auth()
llm_client = openai_client_auth()
POST_URL = "https://bsky.app/profile/anthonymoser.com/post/3mely74s2ws2y"

# %%
# 1. Fetch post
post = fetch_post(bsky_client, POST_URL)
post_text = post.record.text

# %%
# 2. Generate search queries
queries = generate_queries(llm_client, post_text)
print(f"Search queries: {queries}")
entities = extract_entities(llm_client, post_text)
print(f"Search entities: {entities}")

# %%
post_text_vector = embed(llm_client, post_text)
post_text_vector = post_text_vector.data[0].embedding

all_texts = queries + entities
result = embed(llm_client, all_texts)

all_candidates = [(text, item.embedding) for text, item in zip(all_texts, result.data)]

scored = []
for candidate_text, candidate_vector in all_candidates:
    similarity = cosine_similarity(post_text_vector, candidate_vector)
    scored.append((similarity, candidate_text))
top_scored = [s for _, s in scored[:3]]

# %%
# 3. Search Bluesky for each query
context = []
context_texts = []

for query in top_scored:
    results = search_posts(bsky_client, query, limit=2)
    context.extend(results)

for i in range(len(context)):
    context_texts.append(context[i].record.text)

# %%
# 4. Synthesize explanation
summary = summarize(llm_client, post_text, context_texts)
