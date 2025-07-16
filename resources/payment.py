from flask_restful import Resource

from mpesa import Mpesa


class PaymentResource(Resource):
    def post(self):
        mpesa_instance = Mpesa()
        mpesa_instance.get_access_token()

        return {"message": "Ok"}
