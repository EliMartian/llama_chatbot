from flask import Flask, request, jsonify
import os
import replicate
from getpass import getpass

app = Flask(__name__)

llama2_13b = "meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d"

REPLICATE_API_TOKEN = getpass()
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

def chat_completion(prompt):
    output = replicate.run(
        llama2_13b,
        input={"prompt": prompt,
               "temperature": 1.0,
               "system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information. Always let the user know they can ask you more questions or follow up about the previous response given.",
               "max_new_tokens":1000}
    )
    return "".join(output)

@app.route('/chat-completion', methods=['POST'])
def handle_chat_completion():
    data = request.json
    prompt = data.get('prompt')
    if prompt:
        response = chat_completion(prompt)
        return jsonify({'response': response})
    else:
        return jsonify({'error': 'No prompt provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
