from http import HTTPStatus

import requests
from src.main.api.requests.requester import Requester
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.transfer_response import TransferResponse


class TransferRequester(Requester):
    def post(self, transfer_request: TransferRequest):
        url=f"{self.base_url}/account/transfer"
        response = requests.post(
            url=url,
            json=transfer_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            return TransferResponse(**response.json())
        return response