import json

from responses import post_response
from table_utils import get_item, json_dumps, qa_table


# TODO: プロダクト用に修正する
def lambda_handler(event, context):
    body = event.get("body")
    if body is None:
        return post_response(400, "Bad Request: Invalid body")
    body_json = json.loads(body)

    try:
        question_id = body_json.get("question_id", None)
        free_form = body_json.get("free_form", None)

        # validate
        if question_id is None and free_form is None:
            raise Exception("question_id or free_form is required")
        if question_id is not None and free_form is not None:
            raise Exception("question_id and free_form are exclusive")
        if question_id is not None:
            question_id = int(question_id)
        elif free_form is not None:
            free_form = str(free_form)
    except Exception as e:
        print(e)
        return post_response(400, f"Bad Request: {e}")

    try:
        if question_id is not None:
            response = get_next_question(question_id)
        elif free_form is not None:
            raise NotImplementedError("free_form is not implemented")
    except IndexError as e:
        print(e)
        return post_response(404, f"Not Found: {e}")
    except NotImplementedError as e:
        print(e)
        return post_response(501, f"Not Implemented: {e}")
    except Exception as e:
        print(e)
        return post_response(500, f"Internal Server Error: {e}")

    return post_response(200, json_dumps(response))


def get_next_question(question_id: int):
    return get_item(qa_table, "question_id", str(question_id))
