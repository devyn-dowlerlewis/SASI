def create_message_array(parameters):
    context_prompt = _generate_system_prompt()
    instructions_prompt = _generate_instructions_prompt(parameters["system_message"])
    message_array = [{"role": "system", "content": context_prompt}, {'role': 'user', 'content': instructions_prompt}]
    return message_array


def _generate_system_prompt():
    return "You are an assistant who must analyse a message from a DTMF telephone banking system in which it requests something from the user. \
    You must determine which of several possible request states the system is in, and which dtmf options it has presented the user. You must respond in valid JSON."


def _generate_instructions_prompt(system_message):
    return f"The DTMF system message for you to analyse is the following in triple quotes: '''{system_message}''' \
    Please categorize the current request state of the dtmf system as of this system message and explain your answer. \
    A list of possible request states are as follows: \
    'DTMF Navigation Request': The system presents a menu and requests that \
    the user selects an option by pressing the single corresponding dtmf key. \
    'Personal Information Request': The system requests personal information from the user such as \
    member number, account number, pin, code, random sequence of numbers/characters, or other personally identifiable or account information. \
    'Other' if the system requests something else. \
    If the system provides the user with account information such as a balance, \
    information on deposits or withdrawals or other financial information, please indicate as such and include details in your explanation. \
    If DTMF menu options have been presented, please give descriptions of the options and their corresponding dtmf key values. This should inlcude star (*) and pound (#) if they're presented as options. \
    Include a brief description of the options presented in your explanation. If the system has not explicitly presented dtmf options, return an empty list."