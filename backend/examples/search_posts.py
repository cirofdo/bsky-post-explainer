from backend.app.bluesky import bsky_client, search_posts

QUERY = "Ralph Wiggum technique"

client = bsky_client()
results = search_posts(client, QUERY, limit=5)

print(f"Found {len(results)} posts for query: '{QUERY}'\n")

for post in results:
    print(f"Author: {post.author.handle}")
    print(post.record.text)
    print(
        f"https://bsky.app/profile/{post.author.handle}/post/{post.uri.split('/')[-1]}"
    )
    print("---")
