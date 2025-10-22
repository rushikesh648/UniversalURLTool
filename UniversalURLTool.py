from url_tool import UniversalURLTool

# Initialize with a URL
my_url = "https://user:pass@www.example.com:8080/path/to/resource;param1=value1?name=Alice&id=123&tags=tech,dev#section-about"
tool = UniversalURLTool(my_url)

# Or parse a URL later
# tool = UniversalURLTool()
# tool.parse("http://another.example.com/page")

# Get parsed components
components = tool.get_components()
if components:
    for key, value in components.items():
        print(f"{key}: {value}")
