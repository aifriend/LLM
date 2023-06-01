import json


class DocLoad:
    INFILE_TYPE_JSON = 'json'
    INFILE_TYPE_TEXT = 'txt'
    JSON_ID_KEY = 'id'
    JSON_ID_DOC = 'doc'
    ENCODING = 'utf-8'

    @staticmethod
    def parse_input_documents(infile_path, infile_type: str = INFILE_TYPE_JSON):
        document_list = list()

        with open(infile_path, "r") as ftext:
            if infile_type == DocLoad.INFILE_TYPE_TEXT:
                for i, doc in enumerate(ftext.readlines()):
                    document_list.append({
                        "id": i,
                        "text": doc
                    })
            elif infile_type == DocLoad.INFILE_TYPE_JSON:
                with open(infile_path, "r", encoding=DocLoad.ENCODING) as fjson:
                    input_json = json.load(fjson)

                type_err_msg = "Input JSON must be an array of objects"
                assert isinstance(input_json, list), type_err_msg
                assert isinstance(input_json[0], dict), type_err_msg
                for idx, doc_data in enumerate(input_json):
                    document_list.append({
                        "id": doc_data[DocLoad.JSON_ID_KEY] if DocLoad.JSON_ID_KEY in doc_data else idx,
                        "text": doc_data[DocLoad.JSON_ID_DOC]
                    })

        return document_list
