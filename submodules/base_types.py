from typing import Any, TypedDict, Union, Dict, Optional

__all__ = ("PlayerData", "ClientData", "ServerResponse")

class PlayerData(TypedDict):
    posx: int
    posy: int
    rot: Union[int, float]
    turret_rot: Union[int, float]


class ClientData(TypedDict):
    key: str
    id: int
    addres: list[str, int]
    client_timeout_ms: int

    player_data: Union[
        Dict,
        PlayerData
    ]


class ServerResponse(TypedDict):
    status: int
    response: Optional[Any]
