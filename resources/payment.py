from flask import request
from flask_restful import Resource

from mpesa import Mpesa
from models import Payment, db


class PaymentResource(Resource):
    def post(self):
        mpesa_instance = Mpesa()

        data = {
            "phone": "254703453047",
            "amount": "1",
            "description": "Monthly subscription",
        }

        mpesa_response = mpesa_instance.make_stk_push(data)

        # payment_data = Payment(checkout_id=mpesa_response["CheckoutRequestID"])
        # db.session.add(payment_data)
        # db.session.commit()

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
        # extract CheckoutRequestID from mpesa response
        # CheckoutRequestID = None
        # payment = Payment.query.filter_by(checkout_id = CheckoutRequestID).one_or_none()
        # payment.mpesa_code = ""

        # persist to db
        return {"message": "Ok"}
