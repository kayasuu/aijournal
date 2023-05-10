import openai
import os

openai.api_key = open('key.txt').read().strip('\n')

def gpt_classify_sentiment(prompt):
    # system_prompt = f'''You are an emotionally intelligent assistant.
    # Classify the sentiment of the user's text with ONLY ONE OF THE FOLLOWING EMOTIONS:
    # {emotions}.
    # After classifying the text, responpint with the emotion ONLY.'''
    
    system_prompt = f'''
    You are an AI trained to provide top-tier advice on personal growth and self-improvement, 
    with the expertise of a professional clinical psychologist and performance coach. 
    Your mission is to help users reflect on their day and come up with actionable steps
    to optimize their performance the following day. Based on the user's input, generate a thoughtful response
    that addresses their concerns or thoughts, and provide meaningful questions or suggestions
    to help them take action tomorrow. Your response should be concise, empathetic, supportive, and focused on promoting positive change.
    '''
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo', 
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        # max_tokens=20,
        temperature=0
    )
    r = response['choices'][0]['message']['content']
    if r == '':
        r = 'N/A'
    return r

emotions = 'Happy, Sad, Angry, Anxious, Excited, Frustrated, Confident, Fearful, Bored, Grateful, Nervous, Surprised, Calm, Jealous, Lonely, Content, Embarrassed, Overwhelmed, Curious, Disappointed, Amused, Inspired, Disgusted, Guilty, Relieved, Proud, Ashamed, Hopeful, Shy, Skeptical, Apathetic, Melancholic, Agitated, Loving, Envious, Tired, Suspicious, Eager, Hesitant, Shocked, Compassionate, Energized, Bewildered, Resentful, Regretful, Admiration, Despair, Nostalgic, Serene, Vulnerable'
