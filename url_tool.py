import urllib.parse
import re

class UniversalURLTool:
    def __init__(self, url=None):
        self.url = url
        self.parsed_components = None
        self.parsed_components_dict = None
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

        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
            r'localhost|' # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if re.match(regex, target_url):
            parsed = urllib.parse.urlparse(target_url)
            return bool(parsed.scheme and parsed.netloc)
        return False

    @staticmethod
    def construct(scheme=None, netloc=None, path=None, params=None, query_params=None, fragment=None):
        """
        Constructs a URL from its components.
        query_params should be a dictionary.
        """
        query_string = ""
        if query_params:
            query_string = urllib.parse.urlencode(query_params)

        constructed_url = urllib.parse.urlunparse(
            (scheme or '',
             netloc or '',
             path or '',
             params or '',
             query_string,
             fragment or '')
        )
        return constructed_url

    def generate_connection_string(self, prefix="CONN", include_full_url=True, custom_separator="; "):
        """
        Generates a generic connection string from the parsed URL components.
        This function assumes a format like:
        PREFIX_SCHEME=value; PREFIX_HOST=value; PREFIX_PORT=value; ...
        Optionally includes the full URL.
        """
        if not self.parsed_components_dict:
            print("Error: No URL parsed yet to generate a connection string.")
            return None

        conn_parts = []

        if self.parsed_components_dict["scheme"]:
            conn_parts.append(f"{prefix}_SCHEME={self.parsed_components_dict['scheme']}")
        if self.parsed_components_dict["hostname"]:
            conn_parts.append(f"{prefix}_HOST={self.parsed_components_dict['hostname']}")
        if self.parsed_components_dict["port"]:
            conn_parts.append(f"{prefix}_PORT={self.parsed_components_dict['port']}")
        if self.parsed_components_dict["path"] and self.parsed_components_dict["path"] != '/':
            conn_parts.append(f"{prefix}_PATH={self.parsed_components_dict['path']}")

        # Add query parameters individually
        if self.parsed_components_dict["query_params_dict"]:
            for key, values in self.parsed_components_dict["query_params_dict"].items():
                # If a query param has multiple values, join them
                value_str = ", ".join(values) if isinstance(values, list) else values
                conn_parts.append(f"{prefix}_QUERY_{key.upper()}={value_str}")

        if self.parsed_components_dict["fragment"]:
            conn_parts.append(f"{prefix}_FRAGMENT={self.parsed_components_dict['fragment']}")

        if include_full_url and self.parsed_components_dict["full_url"]:
            conn_parts.append(f"{prefix}_URL={self.parsed_components_dict['full_url']}")

        return custom_separator.join(conn_parts)

# --- Demonstration ---
if __name__ == "__main__":
    print("--- Universal URL Tool Demonstration ---")

    # Example URL with various components
    example_url = "https://user:pass@www.example.com:8080/path/to/resource;param1=value1?name=Alice&id=123&tags=tech,dev#section-about"
    print(f"\nExample URL: {example_url}")

    url_tool = UniversalURLTool(example_url)

    # 1. URL Component Extraction (as before)
    print("\n--- 1. URL Component Extraction ---")
    components = url_tool.get_components()
    if components:
        for key, value in components.items():
            print(f"  {key}: {value}")
    print("\nVisualizing URL components:")
    

    # 2. URL Validation (as before)
    print("\n--- 2. URL Validation ---")
    valid_url = "http://www.google.com/search?q=test"
    invalid_url = "just-a-string"
    print(f"Validating '{example_url}': {url_tool.validate(example_url)}")
    print(f"Validating '{valid_url}': {url_tool.validate(valid_url)}")
    print(f"Validating '{invalid_url}': {url_tool.validate(invalid_url)}")
    print("\nVisualizing URL Validation:")
    

    # 3. URL Construction (as before)
    print("\n--- 3. URL Construction ---")
    constructed_url = UniversalURLTool.construct(
        scheme="https",
        netloc="api.example.org",
        path="/v1/users",
        query_params={"status": "active", "limit": 10},
        fragment="top"
    )
    print(f"Constructed URL: {constructed_url}")
    print("\nVisualizing URL Construction:")
    

    # 4. Generate Connection String (NEW)
    print("\n--- 4. Generate Connection String ---")

    # Generic connection string
    conn_str = url_tool.generate_connection_string(prefix="APP_SERVICE", include_full_url=True)
    print(f"Generic Connection String:\n{conn_str}\n")

    # Another example with a different prefix and no full URL
    db_url = "mysql://dbuser:dbpass@mydbhost.com:3306/mydatabase?charset=utf8mb4&pool_size=10"
    db_tool = UniversalURLTool(db_url)
    db_conn_str = db_tool.generate_connection_string(prefix="DB", include_full_url=False, custom_separator=" | ")
    print(f"Database Connection String Example:\n{db_conn_str}")

    print("\nVisualizing Connection String Generation:")
    
