from flask import Blueprint, request, jsonify
from utils import validate_request_model, validate_parameters_model, instantiate_function_class, instantiate_service
import time

sasi_bp = Blueprint('sasi_bp', __name__)

active_services = {}

def process_sasi_request(req_model):
    paramsstart = time.time()
    parameters, param_error = validate_parameters_model(req_model)
    if param_error:
        return None, {"error": str(param_error)}
    paramsend = time.time()
    #print(paramsend - paramsstart)

    funcstart = time.time()
    function_instance, func_error = instantiate_function_class(req_model)
    if func_error:
        return None, {"error": func_error}
    funcend = time.time()
    #print(funcend - funcstart)

    servicestart = time.time()
    current_service = req_model.service
    print(current_service)
    print(active_services)
    if current_service in active_services:
        service_instance = active_services[current_service]
    else:
        service_instance, service_error = instantiate_service(req_model)
        if service_error:
            return None, {"error": service_error}
        active_services[current_service] = service_instance

    serviceend = time.time()
    #print(f"service instant: {serviceend - servicestart}")
    substart = time.time()
    response = function_instance.generate_response(req_model, service_instance)
    subend = time.time()
    #print(f"Subprocess execution time: {subend - substart}")
    return response, None


@sasi_bp.route('/sasi', methods=['POST'])
def sasi_endpoint():
    start_time = time.time()
    #print("request received")
    req_data = request.json
    req_model, req_error = validate_request_model(req_data)
    if req_error:
        return jsonify({"error": "Validation failed", "details": req_error.errors()}), 400

    sasistart = time.time()
    response, logic_error = process_sasi_request(req_model)
    sasistend = time.time()
    print(f"Sasi execution time: {sasistend - sasistart}")
    if logic_error:
        return jsonify(logic_error), 400

    end_time = time.time()
    print(end_time - start_time)
    return jsonify(response), 200
