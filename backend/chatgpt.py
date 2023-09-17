!pip3 install openai
import openai
openai.api_key = "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"
def chatGPT(GPTquery):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        temperature = 1,
        max_tokens = 2000,
        messages = [
            { "role": "user","content": GPTquery}
        ]
    )
    
    print(response['choices'][0]['message']['content'])
emotionsDict = {"Happy": 0.3, "Sad":0.4,"Angry":0.1, "Surprised": 0.8}

emotions = sorted(emotionsDict.items(), key=lambda x:x[1])[:2]

prompt = "The top two emotions you can hear in my voice are "+ emotions[0]+emotions[1]+". Is this a sign of wellbeing, and if not, in what ways can I deal with these emotions?"

chatGPT(prompt)

prompt2 = "Are there any mental health illnesses that could result from or be indicated from me being "+ emotions[0]+ " and " + emotions[1]+" for prolonged periods of time?"
chatGPT(prompt)
