from flask import Blueprint, request, jsonify
from utils import validate_request_model, validate_parameters_model, instantiate_function_class, instantiate_service

sasi_bp = Blueprint('sasi_bp', __name__)


def process_sasi_request(req_model):
    parameters, param_error = validate_parameters_model(req_model)
    if param_error:
        return None, {"error": str(param_error)}

    function_instance, func_error = instantiate_function_class(req_model)
    if func_error:
        return None, {"error": func_error}

    service_instance, service_error = instantiate_service(req_model)
    if service_error:
        return None, {"error": service_error}

    response = function_instance.generate_response(req_model, service_instance)
    return response, None


@sasi_bp.route('/sasi', methods=['POST'])
def sasi_endpoint():
    req_data = request.json
    req_model, req_error = validate_request_model(req_data)
    if req_error:
        return jsonify({"error": "Validation failed", "details": req_error.errors()}), 400

    response, logic_error = process_sasi_request(req_model)
    if logic_error:
        return jsonify(logic_error), 400

    return jsonify(response), 200
