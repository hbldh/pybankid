from typing_extensions import Literal, NotRequired, TypedDict

class SignResponse(TypedDict):
    orderRef: str
    autoStartToken: str
    qrStartToken: str
    qrStartSecret: str


class PhoneSignResponse(TypedDict):
    orderRef: str


class AuthenticateResponse(TypedDict):
    orderRef: str
    autoStartToken: str
    qrStartToken: str
    qrStartSecret: str


class PhoneAuthenticateResponse(TypedDict):
    orderRef: str


class Device(TypedDict):
    ipAddress: str
    uhi: str


class StepUp(TypedDict):
    mrtd: bool


class User(TypedDict):
    personalNumber: str
    name: str
    givenName: str
    surname: str


class CompletionData(TypedDict):
    user: User
    device: Device
    stepUp: StepUp
    bankIdIssueDate: str
    signature: str
    ocspResponse: str
    risk: NotRequired[str]


class _CollectResponse(TypedDict):
    orderRef: str


class CollectPendingResponse(_CollectResponse):
    status: Literal["pending"]
    hintCode: str


class CollectCompleteResponse(_CollectResponse):
    status: Literal["complete"]
    completionData: CompletionData


class CollectFailedResponse(_CollectResponse):
    status: Literal["failed"]
    hintCode: str
