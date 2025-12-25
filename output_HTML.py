import json
from bs4 import BeautifulSoup

def Html_to_Text(html: str):
    soup = BeautifulSoup(html, 'lxml')
    # Remove <span type="text" class="blankinput"> elements if present
    for span in soup.find_all('span', {'type': 'text', 'class': 'blankinput'}):
        span.decompose()
    # Extract and return plain text
    return ' '.join(soup.stripped_strings)

def generate_html_from_json(file_path, output_html):
    # Read the JSON file
    with open(file_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    # Start HTML content
    html_content = """<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Quiz</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .question {
            margin-bottom: 20px;
        }
        .answer {
            display: none;
            margin-top: 10px;
            color: green;
        }
    </style>
    <script>
        function showAnswer(id) {
            document.getElementById(id).style.display = 'block';
        }
    </script>
</head>
<body>
    <h1>Quiz</h1>
"""

    # Add questions and answers to HTML
    for i, question in enumerate(questions):
        question_text = question.get('title', 'No Question')
        options = question.get('options', [])
        answer = question.get('answer', 'No Answer')
        question_type = question.get('type', 'default')

        html_content += f"<div class=\"question\">\n"

        if question_type == 'match_text' or question_type == 'match':
            # Convert HTML to text, remove <span> elements, and remove the first letter
            plain_text = question_text
            if question_type =='match':
                plain_text = Html_to_Text(question_text)
                modified_question_text = plain_text[1:] if len(plain_text) > 1 else plain_text
                html_content += f"    <p><b>Question {i + 1}:</b> {modified_question_text}</p>\n"
            else:
                html_content += f"    <p><b>Question {i + 1}:</b> {question_text}</p>\n"
        else:
            html_content += f"    <p><b>Question {i + 1}:</b> {question_text}</p>\n"
            html_content += "    <ul>\n"
            for option in options:
                html_content += f"        <li>{option}</li>\n"
            html_content += "    </ul>\n"

        html_content += f"    <button onclick=\"showAnswer('answer{i + 1}')\">Show Answer</button>\n"
        html_content += f"    <p class=\"answer\" id=\"answer{i + 1}\">Answer: {answer}</p>\n"
        html_content += "</div>\n"

    # Close HTML content
    html_content += """</body>\n</html>"""

    # Write to the output HTML file
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

# Example usage
input_file = 'decode.json'  # Replace with the path to your uploaded file
output_file = 'quiz.html'
generate_html_from_json(input_file, output_file)
print(f"HTML file generated: {output_file}")
