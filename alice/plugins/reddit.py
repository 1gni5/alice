def context_builder(subreddit: str, no_posts: int):
    """Emulate the Reddit API and returns dummy posts."""

    context = {"posts": []}
    for x in range(no_posts):
        context["posts"].append({
            "subreddit": subreddit,
            "text": f"Lorem ipsum {x}"
        })

    return context