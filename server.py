from flask import Flask,request,jsonify
import stream_chat
from chatUtils import processPrompt
from flask_cors import CORS

app=Flask(__name__)
CORS(app)


server_client= stream_chat.StreamChat(
    api_key="mxnzfu5g3w7t",
    api_secret="qnfr4pp48dkadsahd8jxh2n2bykg9eu6cr5ybwdsdh74qnryzyrcpgkqs2mnpa8z"
)

@app.before_request
def create_bot_user():


    bot_username ="GenCartBot"
    try:
        response=server_client.query_users({"id": bot_username})
        if not response["users"]:
            server_client.upsert_user({"id": bot_username,"name":"GenCartBot"})
            print(f"Bot user '{bot_username} created successfully")
        else:
            print(f"Bot user '{bot_username} already exists")
    except Exception as e:
        print(f"Error creating bot user: {e}")

@app.route('/create_user',methods=['POST'])
def create_user():
    username=request.json.get('username')
    token=server_client.create_token(username)
    return jsonify({"token": token})


@app.route('/chatbot_prompt', methods=[ 'POST' ])
def chatbot_prompt():
    prompt =request.json.get('prompt')
    # Specify the channel type and ID
    channel_type = 'messaging'
    channel_id = 'gencart-bot'
    channel = server_client.channel(channel_type, channel_id)
    promptResponse = processPrompt (prompt)
    response = channel.send_message({
    "text": promptResponse
    }, user_id="GenCartBot") # Provide the user_id argument correctly
    return response
    # Function block can be empty


if __name__ =='__main__':
    app.run(debug=True)