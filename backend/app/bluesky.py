import os
from dotenv import load_dotenv

from atproto import Client

load_dotenv("backend/.env")


def bsky_client_auth():
    client = Client()
    client.login(os.environ["BSKY_HANDLE"], os.environ["BSKY_APP_PASSWORD"])
    return client


def parse_url(url):
    parts = url.split("/")
    handle = parts[4]
    r_key = parts[6]
    return handle, r_key


def fetch_post(client, url):
    handle, r_key = parse_url(url)
    did = client.resolve_handle(handle).did
    at_uri = f"at://{did}/app.bsky.feed.post/{r_key}"
    thread = client.get_post_thread(uri=at_uri).thread
    return thread.post


def search_posts(client, query, limit=10):
    results = client.app.bsky.feed.search_posts({"q": query, "limit": limit})
    return results.posts
