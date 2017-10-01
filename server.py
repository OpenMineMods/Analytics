from bottle import post, run, request, response
from os import environ

from DB import AnalyticsDB

db = AnalyticsDB()

install_validations = {
    "uuid": str,
    "ver": str,
    "mmc": str,
    "inst": str,
    "sys": str
}

crash_validations = {
    "exc": str,
    "email": str,
    "notes": str,
    "uuid": str,
    "ver": str
}

base = ""
if "OMM_BASE_PATH" in environ:
    base = environ["OMM_BASE_PATH"]


def validate_request(req: request, validations: dict):
    for i in validations:
        if i not in req.json:
            return False
        if type(req.json[i]) != validations[i]:
            return False

    return True


@post(base+"/installed")
def installed():
    if not validate_request(request, install_validations):
        response.status = 401
        return

    ip = int(request.get_header("CF-Connecting-IP", "0.0.0.0").split(".")[-1])
    loc = request.get_header("CF-IPCountry", "XX")

    rj = request.json

    db.insert_anal(rj["ver"], loc, ip, rj["uuid"], rj["mmc"], rj["inst"], rj["sys"])
    return


@post(base+"/crash")
def crashed():
    if not validate_request(request, crash_validations):
        response.status = 401
        return

    rj = request.json
    db.insert_crash(rj["ver"], rj["exc"], rj["email"], rj["notes"], rj["uuid"])
    return

run(host="0.0.0.0", port=9615)
