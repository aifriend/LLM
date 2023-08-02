# GPT Document Extraction

## Q&A task by generative models

This is a proof-of-concept for using ChatGPT to extract structured data from messy text documents like scanned/OCR'd
PDFs and difficult forms.

It works by asking ChatGPT to turn text documents (found in an input JSON file or a text file) into a JSON record that
matches a given JSON Schema specification.

If your input data is a text file where each line is a document, you can use the script like this:

```
./gpt-extract.py --input-type text infile.txt schema.json output.json
```

This would extract each line in infile, using schema.json and write extracted data to output.json. You can find an
example JSON schema down below in the "JSON schema file" section.

If your input data is JSON, you'll need to tell the script how to find the documents (and, optionally how to find a
unique ID for each recod). The only kind of supported JSON is a list of JSON objects. Your JSON input data should look
something like this:

```
[{
  "id": 1
  "doc": "My text here..."
}, {
  "id": 2,
  "doc": "Another record..."
}]
```

You can run the script like this:

```
./gpt-extract.py --input-type json --keydoc doc --keyid id infile.json schema.json output.json
```

Note that the output file (`output.json`), if it exists, needs to be valid JSON (not a blank file) as the script will
attempt to load it and continue where the extraction left off.

## Setup

### Installing the OpenAI Python Library

Next, to use Python to call ChatGPT, install the OpenAI Python library (<https://github.com/openai/openai-python>) using
the pip command:

!pip install openai

*At the time of this update, the version of the openai package is**0.27.2**. Be sure to update to this version for the
code in this article to work correctly.*

Once the library is installed, you can now use the openai package by setting your API key:

import openai
openai.api\_key = "YOUR\_API\_KEY"

### Displaying supported models

As mentioned, ChatGPT is based on GPT-3 family of models. There are four main models that GPT-3 model offers:

- **Davinci**— Most capable GPT-3 model. Can do any task the other models can do, often with higher quality, longer
  output and better instruction-following. Also supports inserting completions within text.
- **Curie**— Very capable, but faster and lower cost than Davinci.
- **Babbage**— Capable of straightforward tasks, very fast, and lower cost.
- **Ada**— Capable of very simple tasks, usually the fastest model in the GPT-3 series, and lowest cost.

*Source:[https://platform.openai.com/docs/models/gpt-3*](https://platform.openai.com/docs/models/gpt-3)*

U**PDATE. OpenAI has since made available GPT-3.5 (which is what ChatGPT is based on) for API access. GPT-4, which is
the latest announced version at the time of this update, is currently in limited beta and you have to join a waitlist in
order to gain access. The code in this article have been updated to use GTP-3.5.**

Let’s list the various models supported:

models = openai.Model.list()
print(models)

You will see a JSON response showing the various models supported:

```
{
`  `"data": [
`    `{
`      `"created": 1649358449,
`      `"id": "**babbage**",
`      `"object": "model",
`      `"owned\_by": "openai",
`      `"parent": null,
`      `"permission": [
`        `{
`          `"allow\_create\_engine": false,
`          `"allow\_fine\_tuning": false,
`          `"allow\_logprobs": true,
`          `"allow\_sampling": true,
`          `"allow\_search\_indices": false,
`          `"allow\_view": true,
`          `"created": 1669085501,
`          `"group": null,
`          `"id": "modelperm-49FUp5v084tBB49tC4z8LPH5",
`          `"is\_blocking": false,
`          `"object": "model\_permission",
`          `"organization": "\*"
`        `}
`      `],
`      `"root": "babbage"
`    `},
`    `{
`      `"created": 1649359874,
`      `"id": "**davinci**",
`      `"object": "model",
`      `"owned\_by": "openai",
`      `"parent": null,
`      `"permission": [
`        `{
`          `"allow\_create\_engine": false,
`          `"allow\_fine\_tuning": false,
`          `"allow\_logprobs": true,
`          `"allow\_sampling": true,
`          `"allow\_search\_indices": false,
`          `"allow\_view": true,
`          `"created": 1669066355,
`          `"group": null,
`          `"id": "modelperm-U6ZwlyAd0LyMk4rcMdz33Yc3",
`          `"is\_blocking": false,
`          `"object": "model\_permission",
`          `"organization": "\*"
`        `}
`      `],
`      `"root": "davinci"
`    `},
`    `{
`      `"created": 1651172509,
`      `"id": "**babbage-code-search-code**",
`      `"object": "model",
`      `"owned\_by": "openai-dev",
`      `"parent": null,
`      `"permission": [
```

It is quite a long list, but the values of the id keys contains the model names. So let’s use list comprehension to show
the list of models:

[model['id'] for model in models['data']]

Here is the list of models:

```
['babbage',
` `'davinci',
` `'babbage-code-search-code',
` `'text-similarity-babbage-001',
` `'text-davinci-001',
` `'ada',
` `'curie-instruct-beta',
` `'babbage-code-search-text',
` `'babbage-similarity',
` `'**gpt-3.5-turbo**',
` `'code-search-babbage-text-001',
` `'gpt-3.5-turbo-0301',
` `'code-cushman-001',
` `'code-search-babbage-code-001',
` `'text-ada-001',
` `'text-embedding-ada-002',
` `'text-similarity-ada-001',
` `'text-davinci-insert-002',
` `'code-davinci-002',
` `'ada-code-search-code',
` `'ada-similarity',
` `'whisper-1',
` `'text-davinci-003',
` `'code-search-ada-text-001',
` `'text-search-ada-query-001',
` `'text-curie-001',
` `'text-davinci-edit-001',
` `'davinci-search-document',
` `'ada-code-search-text',
` `'text-search-ada-doc-001',
` `'code-davinci-edit-001',
` `'davinci-instruct-beta',
` `'text-similarity-curie-001',
` `'code-search-ada-code-001',
` `'ada-search-query',
` `'text-search-davinci-query-001',
` `'curie-search-query',
` `'davinci-search-query',
` `'text-davinci-insert-001',
` `'babbage-search-document',
` `'ada-search-document',
` `'text-search-curie-query-001',
` `'text-search-babbage-doc-001',
` `'text-davinci-002',
` `'curie-search-document',
` `'text-search-curie-doc-001',
` `'babbage-search-query',
` `'text-babbage-001',
` `'text-search-davinci-doc-001',
` `'text-search-babbage-query-001',
` `'curie-similarity',
` `'curie',
` `'text-similarity-davinci-001',
` `'davinci-similarity',
` `'cushman:2020-05-03',
` `'ada:2020-05-03',
` `'babbage:2020-05-03',
` `'curie:2020-05-03',
` `'davinci:2020-05-03',
` `'if-davinci-v2',
` `'if-curie-v2',
` `'if-davinci:3.0.0',
` `'davinci-if:3.0.0',
` `'davinci-instruct-beta:2.0.0',
` `'text-ada:001',
` `'text-davinci:001',
` `'text-curie:001',
` `'text-babbage:001']
```

“**gpt-3.5-turbo**” is the latest publicly available version and this is the model that I will use for this article.

### Creating a completion

To have a conversation with ChatGPT, you perform a***completion***. The idea behind completion is that you provide some
text as a prompt, and the model will attempt to*complete*your sentence. Let’s use the ChatCompletion.create()function to
ask ChatGPT to tell us a joke:

completion = openai.ChatCompletion.create(
`    `model="gpt-3.5-turbo",
`    `messages = [{"role": "user", "content": "Tell me a joke"}],
`    `max\_tokens = 1024,
`    `temperature = 0.8)

print(completion)

The ChatCompletion.create()function takes in the following arguments:

- **model**— the model to use
- **messages**— the message to sent to the chat bot; must be packaged as a list of dictionaries
- **max\_tokens**—the maximum number of tokens to generate in the completion. If you set this to a small number, the
  response returned may not be complete.
- **temperature**— a value between 0 and 2. Lower value makes the output more deterministic. If you set it to a higher
  value like 0.8, the output are more likely to be different when you call the function multiple times.

*Tokens can be thought of as pieces of words. Before the API process your prompt, it is broken down into tokens.
Approximately, a 1500 words sentence is equivalent to about 2048 tokens. For more information on tokens, refer
to:[https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them*](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)*

Questions to be sent to ChatGPT must be enclosed in list of dictionaries. For example, the above questions are sent to
ChatGPT in the following format:

![](./asset/Aspose.Words.92ac3385-a2fe-4323-adc8-2558f231a6fc.001.png)

For questions sent to ChatGPT, the dictionary must contain the role key set to user. The question to ask is set in the
content key.

The response from ChatGPT will look something like this:

```
{
  "choices": [
    {
      "finish\_reason": "stop",
      "index": 0,
      "message": {
        "content": "\n\nWhy was the math book sad? Because it had too many problems.",
        "role": "assistant"
      }
    }
  ],
  "created": 1679289285,
  "id": "chatcmpl-6w28zImP6uLHVHLujNDBCeIru1kRw",
  "model": "gpt-3.5-turbo-0301",
  "object": "chat.completion",
  "usage": {
    "completion\_tokens": 15,
    "prompt\_tokens": 11,
    "total\_tokens": 26
  }
}
```

The result in JSON contains numerous information. In particular, the value of the choices key is an array, of which the
first element contains the result that we want, stored in the message dicationary in the content key:

message = completion.choices[0].message.content
print(message)

And here is the response returned by ChatGPT:

Why was the math book sad? Because it had too many problems.

**Getting the user to ask ChatGPT**

Now that you are able to interface with ChatGPT using Python, let’s modify our code a little so that our users can
interact with ChatGPT directly:

```
while True:
`    `prompt = input('\nAsk a question: ')
`    `completion = openai.ChatCompletion.create(
`        `model="gpt-3.5-turbo",
`        `messages = [{"role": "user", "content": prompt}],
`        `max\_tokens = 1024,
`        `temperature = 0.8)
`    `message = completion.choices[0].message.content
`    `print(message)
```

When you run the above code, the user can now type in a question to pass to ChatGPT:

!![](./asset/Aspose.Words.92ac3385-a2fe-4323-adc8-2558f231a6fc.002.png)

And the reply looks like this:

!![](./asset/Aspose.Words.92ac3385-a2fe-4323-adc8-2558f231a6fc.003.png)

**Following up on your question**

ChatGPT does not remember your previous questions. So in order for you to have a meaningful conversation with it, you
need to feed the conversation back to the API. Remember the list of dictionaries you need to pass to the API?

To feed the previous conversation back to ChatGPT, you first append the reply from ChatGPT to the list:

!![](./asset/Aspose.Words.92ac3385-a2fe-4323-adc8-2558f231a6fc.004.png)

Then, you append your follow-up question:

!![](./asset/Aspose.Words.92ac3385-a2fe-4323-adc8-2558f231a6fc.005.png)

This way, ChatGPT would be able to know the previous questions that you have asked and the responses it provided.

Here’s the updated code to allow the user to have a meaningful conversation with ChatGPT:

```
messages = []   

while True:
`    `prompt = input('\nAsk a question: ')    
`    `messages.append(
`        `{
`            `'role':'user',
`            `'content':prompt
`        `})    
`    `completion = openai.ChatCompletion.create(
`        `model="gpt-3.5-turbo",
`        `messages = messages)

`    `response = completion['choices'][0]['message']['content']
`    `print(response)    
`    `messages.append(
`        `{
`            `'role':'assistant',
`            `'content':response
`        `})
```

And here’s a sample conversation:

!![](./asset/Aspose.Words.92ac3385-a2fe-4323-adc8-2558f231a6fc.006.png)

## Extraction

Once you're set up, you can extract structured data,

```
./gpt-extract.py --headless --input-type infile.txt schema.json output.json
```

### Input data spec

You can provide one of two options:

1. text file, with one record per row (`--input-type txt`)
2. a JSON file with an array of objects (`--input-type json`). You can specify which keys to use with the `--keydoc`
   and `--keyid` options which tell the script how to find the document text and the record ID.

### JSON schema file

You need to provide a JSON Schema file that will instruct ChatGPT how to transform the input text. Here's an example
that I used:

```
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "name of person this document is from": {
      "type": "string"
    },
    "name of person this document is written to": {
      "type": "string"
    },
    "name of person this document is about": {
      "type": "string"
    },
    "violation": {
      "type": "string"
    },
    "outcome": {
      "type": "string"
    },
    "date": {
      "type": "string"
    },
    "summary": {
      "type": "string"
    }
  }
}
```
