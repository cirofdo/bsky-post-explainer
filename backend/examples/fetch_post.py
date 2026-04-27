from backend.app.bluesky import bsky_client, fetch_post

POST_URL = "https://bsky.app/profile/anthonymoser.com/post/3mely74s2ws2y"

client = bsky_client()
post = fetch_post(client, POST_URL)

print("Post Text")
print(post.record.text)
