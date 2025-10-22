import urllib.parse
import re

class UniversalURLTool:
    def __init__(self, url=None):
        self.url = url
        self.parsed_components = None
        if url:
            self.parse(url)

    def parse(self, url=None):
        """
        Parses a URL into its components.
        If no URL is provided, it uses the instance's current URL.
        """
        target_url = url if url is not None else self.url
        if not target_url:
            print("Error: No URL provided for parsing.")
            return None

        self.url = target_url # Update instance URL if a new one is provided
        self.parsed_components = urllib.parse.urlparse(target_url)

        # Parse query parameters into a dictionary
        query_params = urllib.parse.parse_qs(self.parsed_components.query)
        self.parsed_components_dict = {
            "scheme": self.parsed_components.scheme,
            "netloc": self.parsed_components.netloc,
            "hostname": self.parsed_components.hostname,
            "port": self.parsed_components.port,
            "path": self.parsed_components.path,
            "params": self.parsed_components.params, # Path parameters (rarely used)
            "query_string": self.parsed_components.query,
            "query_params_dict": query_params,
            "fragment": self.parsed_components.fragment,
            "full_url": self.url # Store the original URL for reference
        }
        return self.parsed_components_dict

    def get_components(self):
        """
        Returns the last parsed URL components as a dictionary.
        """
        if not self.parsed_components_dict:
            print("No URL has been parsed yet.")
            return None
        return self.parsed_components_dict

    def validate(self, url=None):
        """
        Validates if a URL has a scheme and a network location.
        This is a basic validation; more rigorous validation might involve
        checking DNS, specific regex patterns, etc.
        """
        target_url = url if url is not None else self.url
        if not target_url:
            print("Error: No URL provided for validation.")
            return False

        # Use a regex for a more common pattern check, alongside urllib.parse
        # This regex is a simplified version for demonstration.
        # A more robust regex might be very long and complex.
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
            r'localhost|' # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if re.match(regex, target_url):
            # Further check with urllib.parse to ensure it can be parsed meaningfully
            parsed = urllib.parse.urlparse(target_url)
            return bool(parsed.scheme and parsed.netloc)
        return False

    @staticmethod
    def construct(scheme=None, netloc=None, path=None, params=None, query_params=None, fragment=None):
        """
        Constructs a URL from its components.
        query_params should be a dictionary.
        """
        # Encode query parameters from dict to string
        query_string = ""
        if query_params:
            query_string = urllib.parse.urlencode(query_params)

        # Use urlunparse to construct the URL
        # It expects a 6-item tuple: (scheme, netloc, path, params, query, fragment)
        constructed_url = urllib.parse.urlunparse(
            (scheme or '',
             netloc or '',
             path or '',
             params or '',
             query_string,
             fragment or '')
        )
        return constructed_url

# --- Demonstration ---
if __name__ == "__main__":
    print("--- Universal URL Tool Demonstration ---")

    # Example URL
    example_url = "https://www.example.com:8080/path/to/resource;param1=value1?name=Alice&id=123&tags=tech#section-about"
    print(f"\nExample URL: {example_url}")

    # 1. URL Component Extraction
    print("\n--- 1. URL Component Extraction ---")
    url_tool = UniversalURLTool(example_url)
    components = url_tool.get_components()

    if components:
        for key, value in components.items():
            print(f"  {key}: {value}")

    # Illustrative image for extraction
    print("\nVisualizing URL components:")
    

    # 2. URL Validation
    print("\n--- 2. URL Validation ---")
    valid_url = "http://www.google.com/search?q=test"
    invalid_url = "just-a-string"
    local_url = "/local/path/file.html" # No scheme/netloc, so usually considered invalid by web standards

    print(f"Validating '{example_url}': {url_tool.validate(example_url)}")
    print(f"Validating '{valid_url}': {url_tool.validate(valid_url)}")
    print(f"Validating '{invalid_url}': {url_tool.validate(invalid_url)}")
    print(f"Validating '{local_url}': {url_tool.validate(local_url)}")

    print("\nVisualizing URL Validation:")
    

    # 3. URL Construction
    print("\n--- 3. URL Construction ---")
    constructed_url = UniversalURLTool.construct(
        scheme="https",
        netloc="api.example.org",
        path="/v1/users",
        query_params={"status": "active", "limit": 10},
        fragment="top"
    )
    print(f"Constructed URL: {constructed_url}")

    constructed_url_simple = UniversalURLTool.construct(
        scheme="http",
        netloc="localhost:5000",
        path="/dashboard"
    )
    print(f"Constructed URL (simple): {constructed_url_simple}")

    # Example with path parameters (less common, but supported by urlunparse)
    constructed_url_with_params = UniversalURLTool.construct(
        scheme="ftp",
        netloc="data.server.com",
        path="/files/archive",
        params="type=zip;version=2",
        query_params={"user": "guest"},
        fragment="download"
    )
    print(f"Constructed URL (with path params): {constructed_url_with_params}")

    print("\nVisualizing URL Construction:")
    
