import re
import time

import openai


class ChatGPT:
    # max chars to use in prompt
    DOC_MAX_LENGTH = 3000

    def __init__(self):
        api_key = open("API_KEY", 'r').read()
        openai.api_key = api_key

    def ask(self, prompt) -> str:
        print('Extract structured data from text using ChatGPT.')
        response = self.__get_completion(prompt)
        return response

    @staticmethod
    def __get_completion(prompt, model="gpt-3.5-turbo", temp=0) -> str:
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temp,
        )

        return response.choices[0].message["content"]

    def clean_document(self, page_text):
        # cleaned = re.sub("[\n]+", "\n", re.sub("[ \t]+", " ", page_text)).strip()
        cleaned = re.sub(r"[\t ]+", " ", re.sub(r"[\n]+", "\n", page_text)).strip()
        if len(cleaned) < self.DOC_MAX_LENGTH:
            return cleaned
        front = cleaned[:self.DOC_MAX_LENGTH - 500]
        end = cleaned[-500:]
        return f"{front} {end}"

    def get_prompt(self, page_text, schema):
        prompt_json_strict = f"```{self.clean_document(page_text)}```\n\n" \
                             f"For the given text, can you provide a JSON representation that strictly follows this schema:\n\n" \
                             f"```{schema}```"
        prompt_json = f"```{self.clean_document(page_text)}```\n\n" \
                      f"For the given text, can you provide a JSON representation?\n\n"
        prompt = f"```{self.clean_document(page_text)}```\n\n" \
                 f"For the given text, can you provide " \
                 f"a structured based on the information provided?\n\n"
        # f"a key value pair representation?\n\n"

        print("Entering prompt:", len(prompt), "bytes")

        # increasing this increases the wait time
        waited = 0
        current_prompt = prompt
        while True:
            response = self.ask(current_prompt)

            if waited == 0:
                print(f"{'=' * 70}\nPrompt\n{'-' * 70}\n{current_prompt}")
                print(f"{'=' * 70}\nResponse\n{'-' * 70}\n{response}")

            waited += 1

            if waited > 5:
                print("Timed out on this prompt")
                break

            if "unusable response produced by chatgpt" in response.lower():
                wait_seconds = 120 * waited
                print("Bad response! Waiting longer for ", wait_seconds, "seconds")
                time.sleep(wait_seconds)
                continue

            bad_input = (
                "it is not possible to generate a json representation "
                "of the provided text"
            )

            if bad_input in response.lower():
                response = None
                print("Bad input! Skipping this text")
                continue

            if response.strip() == "HTTP Error 429: Too many requests":
                # sleep for one hour
                print("Sleeping for one hour due to rate limiting...")
                time.sleep(60 * 60)
                continue

            if "}" not in response:
                # retry the session if it's not completing the JSON
                print("Broken JSON response, sleeping then retrying")
                time.sleep(20)
                continue

            # we have a good response here
            break

        return prompt, response
