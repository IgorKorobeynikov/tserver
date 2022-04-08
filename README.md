<h1 align="center">TwisteRServer</h1>

[![](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![](https://img.shields.io/badge/requirements-0-blue)](https://github.com/TwisteRTanks/TwisteRServer/blob/master/requirements.txt)
![](https://img.shields.io/github/forks/TwisteRTanks/TwisteRServer)
![](https://img.shields.io/github/stars/TwisteRTanks/TwisteRServer)
![](https://img.shields.io/github/issues/TwisteRTanks/TwisteRServer?color=blue)
![](https://img.shields.io/tokei/lines/github/TwisteRTanks/TwisteRServer)

Multiplayer game-server for TwisteRTanks.


## Example of simple request:
```json5
/*
    like your own protocol
    *PS: comments are available in json5
*/

{
  "request": "some_request", // required field
  "client_data": {
    "key": "bd3d68462ef04cf490dfa5dd1aa60d27", // required field
    "id": 0, // required field
    "addres": ["127.0.0.1", 58667], // not required field
    "client_timeout_ms": 98, // required field
  },
  "player_data": { 
      /*
          may be empty in this requests:
              * ping
              * disconnect
              * online
              * get_data
              * get_map
      */
      "posx": 0, 
      "posy": 0,
      "rot": 0,
      "turret_rot": 0
  },
  "request_body": {
      // anything data
      "msg_content": "hello",
      "nick": "Someone",
      "rank": 10
  }
}
```

NOTICE: `player_data` and `request_body` are required fields! (but may be empty `{}`)

## Server response:
```json5
{
  "status": 0,
  // `responce` will be renamed to the `responce_body`
  "response": null // any data types that json supports
  
}
```

API Client here: https://github.com/TwisteRTanks/PyTwistAPI

## Some reference about status codes
```haskell
-127 - Unknown error.

-4X - Permission denied.
-40 - Permission denied. Invalid key

-3  - Invalid packet.

-2X - Connection is corrupted.
-21 - Connection is corrupted. Invalid key
-20 - Connection is corrupted. Invalid id


-1 - Error. Maximum connected clients to server
 0 - Succes
```

## Reference about data contained in `core.server.Server.clients`:
```json5
[
  {
    "key": "bd3d68462ef04cf490dfa5dd1aa60d27", 
    "id": 0, 
    "addres": ['127.0.0.1', 58667],
    "client_timeout_ms": 158,
        
    "player_data": {
      "posx": 0,
      "posy": 0,
      "rot": 0,
      "turret_rot": 0
    },
  },
]
```

### Available requests:
`get_online`

`connect`

`disconnect`

`push_data`

`get_data`

`get_messages`

`push_message`

`clear_chat`

`get_map`

`ping`
## TODO:
* Replace all generic typehints
* Map generation
* Chat (~70% done)
* ~~API~~
* ~~Python API wrapper lib~~
* GUI client.
* Base docs
* Async
* Log pull