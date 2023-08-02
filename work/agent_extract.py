import json
import os
import time

from api_key import ApiKey
from lib.ChatGPT import ChatGPT
from lib.DocLoad import DocLoad

os.environ["OPENAI_API_KEY"] = ApiKey.OPENAI_API_KEY


def upsert_result(results, result):
    pk = result["id"]
    for r_ix, r_result in enumerate(results):
        if r_result["id"] != pk:
            continue
        # overwrite
        results[r_ix] = result
        return
    # if we're here we did not update an existing result
    results.append(result)


def run(document,
        f_schema,  # Path to JSON Schema file
        outfile  # Path to output results JSON file
        ):
    # TODO: Check for login prompt
    # TODO: Optionally clear all prev sessions

    chat_gpt = ChatGPT()

    results = []
    if os.path.exists(outfile):
        with open(outfile, "r") as fjson:
            results = json.load(fjson)

    already_scraped = set([
        r.get("id") for r in results
    ])
    if already_scraped:
        print("Already scraped: ", already_scraped)

    print(len(document), "total documents to scrape")

    # flag so that we only sleep after the first try
    first_scrape = True
    for p_ix, page_data in enumerate(document):
        pk = page_data["id"]
        page_text = page_data["text"]
        if not page_text:
            print("Blank text for ID:", pk, "Skipping...")
            continue

        print("Doc ID:", pk, "Text length:", len(page_text))

        if not first_scrape:
            print("Sleeping for rate limiting")
            time.sleep(60)

        prompt, response = chat_gpt.get_prompt(page_text, f_schema)
        first_scrape = False

        if response is None:
            print("Skipping page due to blank response")
            continue

        try:
            data = json.loads(response.split("```")[1])
        except Exception as e:
            print("Bad result on ID:", pk)
            print("Parse error:", e)
            continue

        result = {
            "id": pk,
            "text": page_text,
            "prompt": prompt,
            "response": response,
            "data": data,
        }
        upsert_result(results, result)

        print("Saving results to:", outfile)
        with open(outfile, "w") as fout:
            fout.write(json.dumps(results, indent=2))
        print("ID", pk, "complete")


if __name__ == "__main__":
    SOURCE_DOC_FILE = 'infile.json'
    SCHEMA_PATH = 'schema.json'
    OUTPUT_FILE = 'output.json'
    infile_path = os.path.join(SOURCE_DOC_FILE)
    documents = DocLoad.parse_input_documents(infile_path)

    with open(SCHEMA_PATH, "r") as fschema:
        schema_file = json.load(fschema)

    run(documents, schema_file, OUTPUT_FILE)
