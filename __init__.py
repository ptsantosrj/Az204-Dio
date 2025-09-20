import logging
import json
import azure.functions as func

def validate_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        sum_val = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
        check = ((sum_val * 10) % 11) % 10
        if check != int(cpf[i]):
            return False
    return True

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processando requisição de validação de CPF.')

    try:
        req_body = req.get_json()
        cpf = req_body.get('cpf')
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "JSON inválido"}),
            status_code=400,
            mimetype="application/json"
        )

    if not cpf:
        return func.HttpResponse(
            json.dumps({"error": "CPF não fornecido"}),
            status_code=400,
            mimetype="application/json"
        )

    is_valid = validate_cpf(cpf)
    result = {
        "cpf": cpf,
        "valid": is_valid,
        "message": "CPF válido" if is_valid else "CPF inválido"
    }

    return func.HttpResponse(
        json.dumps(result),
        status_code=200,
        mimetype="application/json"
    )
