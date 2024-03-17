#python -m venv openai-env
#openai-env\Scripts\activate
#pip install --upgrade openai

from openai import OpenAI
client = OpenAI(api_key = "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")

our_output = ["too Windy","Violent Rain", "Hail", "Tornado"] #our confidence
their_output = -80 #their confidence
message = "You have to write a message to the driver of a car telling them to be careful due to "
if isinstance(our_output,list):
    confidence = (100+their_output)/2.0
    for reason in our_output:
        message+=str(reason)+", "
else:
    confidence = (our_output+their_output)/2.0
    message+="potentially dangerous road situation "

message +="but you are "+str(confidence) + " percent confident. It can only be a few words and does not have to be proper grammer. Be super passive agressive" 
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": message,
        }
    ],
    model="gpt-3.5-turbo",
)
#from pathlib import Path
#from openai import OpenAI

#speech_file_path = Path(__file__).parent / "speech.mp3"
#response = client.audio.speech.create(
#  model="tts-1",
#  voice="alloy",
#  input=chat_completion.choices[0].message.content
#)

#response.stream_to_file(speech_file_path)


print(chat_completion.choices[0].message.content)
#print(confidence)
#print(message)