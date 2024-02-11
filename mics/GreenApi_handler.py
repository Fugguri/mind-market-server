from datetime import datetime
from json import dumps


def green_api_handler(type_webhook: str, body: dict) -> None:
    if type_webhook == "incomingMessageReceived":
        return __incoming_message_received(body)
    elif type_webhook == "outgoingMessageReceived":
        return __outgoing_message_received(body)
    elif type_webhook == "outgoingAPIMessageReceived":
        return __outgoing_api_message_received(body)
    elif type_webhook == "outgoingMessageStatus":
        return __outgoing_message_status(body)
    elif type_webhook == "stateInstanceChanged":
        return __state_instance_changed(body)
    elif type_webhook == "deviceInfo":
        return __device_info(body)
    elif type_webhook == "incomingCall":
        return __incoming_call(body)
    elif type_webhook == "statusInstanceChanged":
        return __status_instance_changed(body)


def __get_notification_time(timestamp: int) -> str:
    return str(datetime.fromtimestamp(timestamp))


def __incoming_message_received(body: dict) -> None:
    timestamp = body["timestamp"]
    time = __get_notification_time(timestamp)

    data = dumps(body, ensure_ascii=False, indent=4)

    print(f"New incoming message at {time} with data: {data}", end="\n\n")
    return data


def __outgoing_message_received(body: dict) -> None:
    timestamp = body["timestamp"]
    time = __get_notification_time(timestamp)

    data = dumps(body, ensure_ascii=False, indent=4)

    print(f"New outgoing message at {time} with data: {data}", end="\n\n")
    return data


def __outgoing_api_message_received(body: dict) -> None:
    timestamp = body["timestamp"]
    time = __get_notification_time(timestamp)

    data = dumps(body, ensure_ascii=False, indent=4)

    print(f"New outgoing API message at {time} with data: {data}", end="\n\n")
    return data


def __outgoing_message_status(body: dict) -> None:
    timestamp = body["timestamp"]
    time = __get_notification_time(timestamp)

    data = dumps(body, ensure_ascii=False, indent=4)

    response = (
        f"Status of sent message has been updated at {time} with data: {data}"
    )
    print(response, end="\n\n")
    return data


def __state_instance_changed(body: dict) -> None:
    timestamp = body["timestamp"]
    time = __get_notification_time(timestamp)

    data = dumps(body, ensure_ascii=False, indent=4)

    print(f"Current instance state at {time} with data: {data}", end="\n\n")
    return data


def __device_info(body: dict) -> None:
    timestamp = body["timestamp"]
    time = __get_notification_time(timestamp)

    data = dumps(body, ensure_ascii=False, indent=4)

    response = (
        f"Current device information at {time} with data: {data}"
    )
    print(response, end="\n\n")
    return data


def __incoming_call(body: dict) -> None:
    timestamp = body["timestamp"]
    time = __get_notification_time(timestamp)

    data = dumps(body, ensure_ascii=False, indent=4)

    print(f"New incoming call at {time} with data: {data}", end="\n\n")
    return data


def __status_instance_changed(body: dict) -> None:
    timestamp = body["timestamp"]
    time = __get_notification_time(timestamp)

    data = dumps(body, ensure_ascii=False, indent=4)

    print(f"Current instance status at {time} with data: {data}", end="\n\n")
    return data
