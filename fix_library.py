import agents
import os
import re

agents_path = os.path.dirname(agents.__file__)
target_file = os.path.join(agents_path, 'extensions', 'models', 'litellm_model.py')
print(f"Target file: {target_file}")

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for cached_tokens
# matches getattr( ... "cached_tokens", 0 ) allowing for whitespace/newlines
pattern1 = r'(getattr\(\s*response_usage\.prompt_tokens_details,\s*"cached_tokens",\s*0\s*\))'
replacement1 = r'\1 or 0'

new_content = re.sub(pattern1, replacement1, content)

# Pattern for reasoning_tokens
pattern2 = r'(getattr\(\s*response_usage\.completion_tokens_details,\s*"reasoning_tokens",\s*0\s*\))'
replacement2 = r'\1 or 0'

new_content = re.sub(pattern2, replacement2, new_content)

if content != new_content:
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("File patched successfully.")
else:
    print("No changes made (patterns might not match).")
    # Debug: print a part of the file to see what's wrong if it fails
    start_idx = content.find("InputTokensDetails")
    if start_idx != -1:
        print("Context around InputTokensDetails:")
        print(content[start_idx:start_idx+300])
