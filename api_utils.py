import openai
import time
import random
from wrapt_timeout_decorator import timeout
from openai import AzureOpenAI

#openai.api_type = "azure"
#openai.api_base = ""
#openai.api_version = ""
#openai.api_key = ""

AZURE_OPENAI_ENDPOINT= "https://med-llm.openai.azure.com/openai/deployments/nisumonte-gpt-4o/chat/completions?api-version=2023-03-15-preview"
AZURE_OPENAI_API_KEY="459ae0171f10484abcbd84d89574d0d5"
OPENAI_API_VERSION="2024-07-01-preview"

client = AzureOpenAI(
  azure_endpoint = AZURE_OPENAI_ENDPOINT, 
  api_key= AZURE_OPENAI_API_KEY,  
  api_version= OPENAI_API_VERSION
)

@timeout(200)  # 200 seconds timeout
def generate_response_multiagent(deployment_id, temperature, max_tokens, frequency_penalty, presence_penalty, stop, system_role, user_input):
    print("Generating response for deployment: ", deployment_id)
    start_time = time.time()
    response = client.chat.completions.create(
                    model=deployment_id,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=1,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    stop=stop,
                    messages=[
                        {"role": "system", "content": system_role},
                        {"role": "user", "content": user_input}
                    ],
                )
    end_time = time.time()
    print('Finish!')
    print("Time taken: ", end_time - start_time)

    return response

@timeout(10)  # 10 seconds timeout
def generate_response(deployment_id, temperature, max_tokens, frequency_penalty, presence_penalty, stop, input_text):
    print("Generating response for deployment: ", deployment_id)
    start_time = time.time()
    response = client.chat.completions.create(
                    model=deployment_id,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=1,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    stop=stop,
                    messages=[{"role": "user", "content": input_text}],
                )
    end_time = time.time()
    print('Finish!')
    print("Time taken: ", end_time - start_time)

    return response

@timeout(20)  # 20 seconds timeout
def generate_response_ins(deployment_id, temperature, max_tokens, frequency_penalty, presence_penalty, stop, input_text, suffix, echo):
    print("Generating response for deployment: ", deployment_id)
    start_time = time.time()
    response = client.chat.completions.create(
                        model=deployment_id,
                        prompt=input_text,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        top_p=1,
                        suffix=suffix,
                        frequency_penalty=frequency_penalty,
                        presence_penalty=presence_penalty,
                        stop=stop,
                        echo=echo,
                        logprobs=1,
                    )
    
    end_time = time.time()
    print('Finish!')
    print("Time taken: ", end_time - start_time)

    return response

class api_handler:
    def __init__(self, model):
        self.model = model

        if self.model == 'instructgpt':
            self.deployment_id = 'text-davinci-002'
        elif self.model == 'instructgpt-gen':
            self.deployment_id = 'text-davinci-002'
        elif self.model == 'newinstructgpt':
            self.deployment_id = 'text-davinci-003'
        elif self.model == 'oldinstructgpt':
            self.deployment_id = 'text-davinci-001'
        elif self.model == 'gpt3':
            self.deployment_id = 'davinci'
        elif self.model == 'codex':
            self.deployment_id = 'code-davinci-002'
        elif self.model == 'gpt3-edit':
            self.deployment_id = 'text-davinci-edit-001'
        elif self.model == 'codex-edit':
            self.deployment_id = 'code-davinci-edit-001'
        elif self.model == 'chatgpt':
            self.deployment_id = 'gpt-35-turbo-16k'
        elif self.model == 'gpt4':
            self.deployment_id = 'gpt-4'
        elif self.model == 'gpt4o':
            self.deployment_id = 'gpt-4o'
        else:
            raise NotImplementedError

    def get_output_multiagent(self, system_role, user_input, max_tokens, temperature=0,
                    frequency_penalty=0, presence_penalty=0, stop=None):
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                response = generate_response_multiagent(self.deployment_id, temperature, max_tokens, frequency_penalty, presence_penalty, stop, system_role, user_input)
                if response.choices[0].message.content:
                    return response.choices[0].message.content
                else:
                    return "ERROR." 
            except:
                print(f'Attempt {attempt+1} of {max_attempts} failed with error:')
                if attempt == max_attempts - 1:
                    return "ERROR."


    def get_output(self, input_text, max_tokens, temperature=0,
                   suffix=None, stop=None, do_tunc=False, echo=False, ban_pronoun=False,
                   frequency_penalty=0, presence_penalty=0, return_prob=False):
        try:
            response = generate_response(self.deployment_id, temperature, max_tokens, frequency_penalty, presence_penalty, stop, input_text)
        except (TimeoutError, openai.error.Timeout, Exception):    
            print("Timeout")
            try:
                response = generate_response(self.deployment_id, temperature, max_tokens, frequency_penalty, presence_penalty, stop, input_text)
            except (TimeoutError, openai.error.Timeout, Exception):
                print("Timeout occurred again. Exiting.")
                response = "ERROR."
                return response 
        if response.choices and response.choices[0].message and "content" in response.choices[0].message:
            x = response.choices[0].message.content
        else:
            print(response)
            x = "ERROR."  
            return x

        if do_tunc:
            y = x.strip()
            if '\n' in y:
                pos = y.find('\n')
                y = y[:pos]
            if 'Q:' in y:
                pos = y.find('Q:')
                y = y[:pos]
            if 'Question:' in y:
                pos = y.find('Question:')
                y = y[:pos]
            assert not ('\n' in y)
            if not return_prob:
                return y

        if not return_prob:
            return x

        output_token_offset_real, output_token_tokens_real, output_token_probs_real = [], [], []
        return x, (output_token_offset_real, output_token_tokens_real, output_token_probs_real)
