# wikimedia-changes-slack

Usage:

```
docker run \
    -e WMCS_WIKIMEDIA_URL=https://your.wikimedia.url/api.php?action=query&list=recentchanges \
    -e WMCS_SLACK_URL=https://your.slack.webhook/ \
    chauffer/wikimedia-changes-slack
```

Tested with Discord's Slack compatible webhooks.
