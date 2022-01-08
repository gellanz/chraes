import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    sub_options = req.params.get('subjects_options')
    num_subjects = req.params.get('num_subjects')
    

    if not sub_options or not num_subjects :
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            sub_options = req_body.get('subjects_options')
            num_subjects = req_body.get('num_subjects')

    if sub_options and num_subjects:
        return func.HttpResponse(f"tus opciones son {sub_options}\n buscaremos {num_subjects}")
    else:
        return func.HttpResponse(
             "mising data error",
             status_code=200
        )
