from google import genai
from google.genai import types
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
chat = client.chats.create(model="gemini-2.5-flash", config=types.GenerateContentConfig(
        temperature=0.9
    ))


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": [
    "http://localhost:3000",
    "https://internship-experiment-frontend.vercel.app/"
]}})

@app.route('/api/generate', methods=['POST'])
def home():
    data = request.json
    user_prompt = data.get("input", "")
    response = chat.send_message(user_prompt)
    return jsonify({"response": f"{response.text}"}), 200
# response = chat.send_message_stream("I have 2 dogs in my house.")
# # for chunk in response:
# #     print(chunk.text, end="")

# response = chat.send_message_stream("How many paws are in my house?")
# # for chunk in response:
#     print(chunk.text, end="")

# print("\n\nChat history:")
# for message in chat.get_history():
#     print(f'role - {message.role}', end=": ")
#     print(message.parts[0].text)


if __name__ == '__main__':
    app.run()
