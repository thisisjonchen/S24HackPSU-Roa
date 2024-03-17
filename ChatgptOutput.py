#python -m venv openai-env
#openai-env\Scripts\activate
#pip install --upgrade openai

from openai import OpenAI
client = OpenAI(api_key = "API_KEY_HERE")

def ChatGPT(our_confidence,their_confidence):
    our_output = our_confidence #our confidence
    their_output = their_confidence #their confidence
    message = "write a message with confidence of "

    if isinstance(our_output,list):
        confidence = (100+their_output)/2.0
        message+= str(confidence)+" with the reason being due to "
        for reason in our_output:
            message+=str(reason)+", "

    else:
        confidence = (our_output+their_output)/2.0
        message+=str(confidence)

    if(confidence>0):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """You are writing a message to someone currently driving a car to alert the driver 
                                that the road situation they are in looks like a situation in which a crash has either 
                                happened or is likely to happen.  The message should only be a few words long and does 
                                not need to have proper grammar. I will provide a confidence level for your response
                                on a scale of 0-100. A response with higher confidence should be more assertive and urgent, 
                                while a message with low confidence should be a weaker, less stressed recommendation. 
                                An example of a message with high confidence is 'URGENT, DRIVE SAFE' while an example 
                                for a message with low confidence is 'caution.'"""
                },
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model="gpt-3.5-turbo",
        )
        print(chat_completion.choices[0].message.content)
#from pathlib import Path
#from openai import OpenAI

#speech_file_path = Path(__file__).parent / "speech.mp3"
#response = client.audio.speech.create(
#  model="tts-1",
#  voice="alloy",
#  input=chat_completion.choices[0].message.content
#)

#response.stream_to_file(speech_file_path)

#print(confidence)
#print(message)
