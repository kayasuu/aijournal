import openai

def chatbot_response(message: str):
    openai.api_key = open('key.txt').read().strip('\n')

    questions = list()
    bot_responses = list()
    messages = list()

    # system_prompt = input('System Prompt:')
    system_prompt = '''You are an exceptional journalling assistant, with decades of experience in Clinical Psychology.
    You are familiar with the importance of active listening. The first input, the user will write a journal entry.
    From there, you will have a dialog. As consicely as possible, support the user by demonstrating active listening and by
    providing meaningful questions that the user can reflect upon for their next message.'''

    messages.append(
        {'role': 'system', 'content': system_prompt},
    )

    messages.append({'role': 'user', 'content': message})

    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.7
    )

    current_response = completion.choices[0]['message']['content']
    messages.append({'role': 'assistant', 'content': current_response})

    return current_response
