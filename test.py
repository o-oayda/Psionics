import re

def replace_subparagraphs(text):
  # Define the regular expression pattern
  pattern = r'\*\*\*([\S\s]*?)\.\*\*\*'
  
  # Replace the pattern with the desired format
  replaced_text = re.sub(pattern, r'\\subparagraph{\1}', text)
  
  return replaced_text

# Example usage
text = "This is a test ***Cold.*** and another ***Hot.***"
result = replace_subparagraphs(text)
print(result)