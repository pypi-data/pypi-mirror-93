import flask
from flask_socketio import join_room, rooms


def wrap(socketio):
    @socketio.on("disconnect", namespace="/rtc-cafe")
    def socket_disconnect_handler():
        for room in rooms():
            socketio.emit(
                "peer-disconnection",
                {"sid": flask.request.sid},
                room=room,
                namespace="/rtc-cafe",
                include_self=False,
            )

    @socketio.on("request-sid", namespace="/rtc-cafe")
    def socket_request_sid(data):
        sid = flask.request.sid
        socketio.emit("sid", {"sid": sid}, room=sid, namespace="/rtc-cafe")

    @socketio.on("join", namespace="/rtc-cafe")
    def socket_join_room_handler(data):
        join_room(data["room"])
        socketio.emit(
            "acquire-peers",
            {
                "id": data.get("id"),
                "sid": flask.request.sid,
                "prevSid": data.get("prevSid"),
            },
            room=data["room"],
            namespace="/rtc-cafe",
            include_self=False,
        )

    @socketio.on("acquire-peers-response", namespace="/rtc-cafe")
    def socket_acquire_peers_response_handler(data):
        room = data["room"]
        recipient = data["recipient"]
        socketio.emit(
            "acquire-peers-response",
            {
                "id": data.get("id"),
                "sid": flask.request.sid,
                "prevSid": data.get("prevSid"),
            },
            room=recipient,
            namespace="/rtc-cafe",
        )

    @socketio.on("offer", namespace="/rtc-cafe")
    def socket_send_offer_handler(data):
        socketio.emit(
            "offer",
            {"id": data.get("id"), "sid": flask.request.sid, **data},
            room=data["recipient"],
            namespace="/rtc-cafe",
        )

    @socketio.on("answer", namespace="/rtc-cafe")
    def socket_send_answer_handler(data):
        socketio.emit(
            "answer",
            {"id": data.get("id"), "sid": flask.request.sid, **data},
            room=data["recipient"],
            namespace="/rtc-cafe",
        )

    @socketio.on("candidate", namespace="/rtc-cafe")
    def socket_send_candidate_handler(data):
        socketio.emit(
            "candidate",
            {"id": data.get("id"), "sid": flask.request.sid, **data},
            room=data["recipient"],
            namespace="/rtc-cafe",
        )
