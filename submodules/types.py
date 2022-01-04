from typing import TypedDict
client = dict[str, ...]
clients = list[Client]


response = dict[str, status | list[dict[str, str]]]
# response = dict[str, status | response]
# response = dict[str, Union[int, str, Iterable[dict | list]]

Status = int
UserData = dict[]


class UserData(TypedDict):
    key: str
    id: int
    addres: list[str, int]
    posx: int
    posy: int
    rot: int
    turret_rot: int


class Response(TypedDict):
    status: Status


class ListResponse(Response):
    response: list[UserData]
