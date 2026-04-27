# Bluesky AI Agent — Planning

## Goal

```
Input (URL or text)
        │
        ▼
1. FETCH  → Get post text + thread replies (if URL given)
        │
        ▼
2. EXTRACT → Pull out key entities/terms (LLM call)
             e.g. "Ralph Wiggum technique", "Geoffrey Huntley", "coding agents"
        │
        ▼
3. SEARCH → For each entity, search:
             - Bluesky posts (keyword search via AT Protocol)
             - Web (Tavily or just requests to search)
        │
        ▼
4. SUMMARIZE → LLM reads post + search results → bullet-point explanation
        │
        ▼
Output: 3-5 bullet points explaining the post
```

---

## Steps

### 1 - Setup env
- Bluesky
- Groq
- Create uv env
- Create simple project structure

### 2 - Test scripts for each of the steps
- Write an example script that fetches a Bluesky post
- Write an example script that extract entities
- Write an example script that search posts

### 3 - Build agent
- Build agente following the format
        1. Fetch the post from Bluesky
        2. Extract key entities/topics via LLM
        3. Search Bluesky for each entity to gather context
        4. Synthesize a bullet-point explanation via LLM
- Create query to search instead of entities

### 4 - Build evaluation feature
- Gather 10 different posts with different topics
- Built the expected expected outputs with the assistance of a different LLM (claude 4.5) and my inputs as well

### 5 - Build API and frontend
- I have very little experience on this, so I mainly used the outputs of the AI assistant

### 6 - Ranking system to get best search queries
- Used cosine similarity between post vector and the search vectors to get the 3 top ones to search for posts
---

## Ideas / Next steps

### Improve posts understanding
  - extract text from image
  - add image explainer
  - access post answers
  - access posts URLs

### Explore ways to optimize context to pass to the LLM
  - embedding to get closer vectors
  - improve the search query to decide to use entities or queries
  - Use langgraph conditional edges to retry after getting bad results
  - Search different sources like wikipedia, other social networks or even google

### Software engineering best practices
  - Add functions docstrings
  - Add logs
  - Add pytest 