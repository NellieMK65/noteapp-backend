from flask import request
from flask_restful import Resource

from mpesa import Mpesa


class PaymentResource(Resource):
    def post(self):
        mpesa_instance = Mpesa()

        data = {
            "phone": "254703453047",
            "amount": "1",
            "description": "Monthly subscription",
        }

        mpesa_response = mpesa_instance.make_stk_push(data)

        return {"message": "Ok", "data": mpesa_response}


class CheckPaymentResource(Resource):
    def get(self, checkout_request_id):
        mpesa_intance = Mpesa()

        res = mpesa_intance.check_transaction(checkout_request_id)

        return {"message": "ok", "data": res}


class PaymentCallbackResource(Resource):
    def get(self):
        return {"message": "callback registered"}

    def post(self):
        data = request.json()
        print(data)
        return {"message": "Ok"}
