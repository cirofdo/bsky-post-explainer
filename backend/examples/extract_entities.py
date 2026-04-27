from backend.app.llm import openai_client, extract_entities


POST_TEXT = """Ralph Wiggum is the craziest thing to happen in the coding agents space in 2026 so far
not the technique itself, just the fact that someone was like "here's a technique it's called the Ralph Wiggum technique because of the Simpsons guy" and everyone was like "OK sounds good" """

client = openai_client()
response = extract_entities(client, POST_TEXT)

print(response.choices[0].message.content)
