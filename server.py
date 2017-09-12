from bottle import post, run, request, response
from DB import AnalyticsDB

db = AnalyticsDB()

validations = {
    "uuid": str,
    "ver": str
}


def validate_request(req: request):
    for i in validations:
        if i not in req.json:
            return False
        if type(req.json[i]) != validations[i]:
            return False

    return True


@post("/installed")
def installed():
    if not validate_request(request):
        response.status = 401
        return

    ip = int(request.get_header("CF-Connecting-IP", "0.0.0.0").split(".")[-1])
    loc = request.get_header("CF-IPCountry", "XX")

    db.insert_anal(request.json["ver"], loc, ip, request.json["uuid"])
    return

run(host="0.0.0.0", port=9615)
