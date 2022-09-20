from http.cookiejar import FileCookieJar
from unittest import TestCase
from json import loads

from alice.template import render, build_context


class IntegrationTest(TestCase):
    def test_everything(self):

        filename = "script.json"

        content = render(filename, {"dry_run": True})
        metadata = loads(content)["metadata"]

        # Check if all metadata are correct
        self.assertEqual(
            metadata,
            {
                "plugins": {
                    "reddit": {"subreddit": "relationship_advice", "no_posts": 5}
                }
            },
        )

        context = build_context(metadata)
        context |= {"dry_run": False}

        content = render(filename, context)
        print(content)
        print(loads(content))
