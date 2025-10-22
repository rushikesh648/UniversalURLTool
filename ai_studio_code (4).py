from url_tool import UniversalURLTool

new_url = UniversalURLTool.construct(
    scheme="https",
    netloc="api.myservice.com",
    path="/v2/data",
    query_params={"status": "enabled", "limit": 50},
    fragment="results"
)
print(f"Constructed URL: {new_url}")
# Output: https://api.myservice.com/v2/data?status=enabled&limit=50#results