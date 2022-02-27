from _collections import deque

HISTORY_SIZE = 30


class Status:
    FAIL = 'fail'
    SUCCESS = 'success'
    ALL = [FAIL, SUCCESS]


class History:

    def __init__(self, data=None):
        data = data or []
        self.data = deque(data, HISTORY_SIZE)

    def save_history(self, request, response, status):
        item = {
            "request": request,
            "response": response,
            "status": status
        }
        self.data.append(item)

    def get_history(self, limit=HISTORY_SIZE, status=None):
        out_data = []
        for i in range(-1, -len(self.data) - 1, -1):
            if status is not None and self.data[i]["status"] != status:
                continue
            out_data.append(self.data[i])
            if len(out_data) == limit:
                break
        return out_data

    def validate_attributes(self, limit=None, status=None):
        errors = []
        if limit is not None and (limit < 1 or limit > HISTORY_SIZE):
            err = f"History length error. Wrong length: {limit}"
            errors.append(err)
        if status is not None and status not in Status.ALL:
            err = f"Status error. Wrong status: {status}"
            errors.append(err)
        return errors


history = History()
