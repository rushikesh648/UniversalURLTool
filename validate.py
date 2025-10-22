from url_tool import UniversalURLTool

tool = UniversalURLTool() # No need to provide URL at init for validation

print(f"Is 'https://www.google.com' valid? {tool.validate('https://www.google.com')}")
print(f"Is 'ftp://mydata.com/file.zip' valid? {tool.validate('ftp://mydata.com/file.zip')}")
print(f"Is 'invalid-string' valid? {tool.validate('invalid-string')}")
