import re

from praw import Reddit
from praw.models import Submission

POST_FETCH_LIMIT = 100


def sanitize(text: str) -> str:
    """Sanitize given text for json encoding."""

    # Delete markdown hyperlinks
    text = re.sub(r"(\[(.*?)\]\()(.+?)(\))", "", text, re.IGNORECASE)

    # Delete zero-length spaces
    text = text.replace("&#x200B", "")

    # Keeping only alpha numeric + spaces
    text = re.sub(r"[^A-Za-z0-9 \']+", " ", text)

    # Delete additional spaces
    text = re.sub(r" +", " ", text)

    return text


def is_valid(post: Submission) -> bool:
    """Define if post should be read or not."""

    # Should be text
    if not post.is_self:
        return False

    # Should not be pinned (admin/meta)
    if post.stickied:
        return False

    return True


def context_builder(subreddit: str, no_posts: int):
    """Connect to Reddit API and retreive posts."""

    client = Reddit(site_name="alice")
    context = {"posts": []}

    posts = client.subreddit(subreddit).hot(limit=POST_FETCH_LIMIT)
    for post in posts:

        # Skip invalid posts
        if not is_valid(post):
            continue

        context["posts"].append(
            {"title": sanitize(post.title), "text": sanitize(post.selftext)}
        )

        # Check if post limit has been reached
        if len(context["posts"]) >= no_posts:
            break

    return context
