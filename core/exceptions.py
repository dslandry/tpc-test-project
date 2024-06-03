from rest_framework import status
from rest_framework.exceptions import APIException


class UserEmailConflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "conflict"
    default_detail = "E-mail {email} already used by another client."

    def __init__(self, email, code=None):
        detail = self.default_detail.format(email=email)
        super().__init__(detail, code)


class ProductOutOfStock(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "product_out_of_stock"
    default_detail = "Product out of stock"
