import requests as r

ERROR_BAD_MASTER_KEY = {'error': 1, 'error_text': 'bad_master_key',
                        'details': "Only master key allowed for this method"}

class Response:
    def __init__(self, resp):
        """
        Response object

        :param resp: JSON deserialized response
        """
        self.dict = resp  # Full response as dict
        self.time = None  # Execution time
        self.count = None  # Row count fetched
        self.data = resp['data']  # SQL execution status
        if 'status' in self.data:  # Task fetch results
            self.time = self.data['result']['time']
            self.count = self.data['result']['count']
            self.data = self.data['result']['data']
        else:  # Normal SQL
            self.time = resp['time']
            self.count = resp['count']

    def __repr__(self):
        return f"<Response [Count: {self.count}]>"


class TaskException(Exception):
    def __init__(self, task_id, error_text, details):
        """
        Task execution exception

        :param task_id: ID of the executed task
        :param error_text: Short description
        :param details: Long details
        """
        self.task_id = task_id
        self.error_text = error_text
        self.details = details

    def __str__(self):
        return f"[ID: {self.task_id}] '{self.error_text}' -> {self.details}"


class ConnectException(Exception):
    def __init__(self, error_text="timed_out", details="The request has timed out. Make sure your script is running"):
        """
        Connect exception (mostly time out)

        :param error_text: Short description
        :param details: Long details
        """
        self.error_text = error_text
        self.details = details

    def __str__(self):
        return f"'{self.error_text}' -> {self.details}"


class KeyException(Exception):
    def __init__(self, error_text, details):
        """
        Bad key

        :param error_text: Short description
        :param details: Long details
        """
        self.error_text = error_text
        self.details = details

    def __str__(self):
        return f"'{self.error_text}' -> {self.details}"


class GeneralException(Exception):
    def __init__(self, error_text, details):
        """
        General exception (e.g on execution failure, raised when request returns 'error': 1)

        :param error_text: Short description
        :param details: Long details
        """
        self.error_text = error_text
        self.details = details

    def __str__(self):
        return f"'{self.error_text}' -> {self.details}"


class Task:
    def __init__(self, url, key, task_id):
        """
        Task object

        :param url: URL of the service
        :param key: Key to use to check execution status
        :param task_id: Task ID to check
        """
        self.url = url
        self.key = key
        self.task_id = task_id

    def get_status(self):
        """
        Get task status

        :return: None (pending) / Response (done) / TaskException (error)
        """
        if not self.key:
            raise KeyException('bad_key', "Key was not specified")
        try:
            resp = r.get(self.url + f"/task/{self.task_id}", json={"key": self.key}, timeout=5).json()
        except:
            return ConnectException()
        if resp['status'] == 'pending':
            return None
        elif resp['status'] == 'error':
            raise TaskException(self.task_id, resp['error_text'], resp['details'])
        return Response(resp['data'])

    def __repr__(self):
        return f"<Task [ID: {self.task_id}]>"


class Tasks:
    def __init__(self, url, key, resp):
        """
        Tasks list (statistics)

        :param url: Server url
        :param key: Normal key
        :param resp: Response from /tasks
        """
        self.url = url
        self.key = key
        self.total = resp['data']['total']
        self.pending = resp['data']['pending']
        self.error = resp['data']['error']
        self.done = resp['data']['done']

    def get_task(self, task_id):
        """
        Get Task object for specified task_id

        :param task_id: Task ID
        :return: None / Task
        """
        if not self.key:
            raise KeyException('bad_key', "Key was not specified")
        if task_id < 0 or task_id >= self.total:
            return None
        return Task(self.url, self.key, task_id)

    def __repr__(self):
        return f"<Tasks [Total: {self.total}. P/E/D: {self.pending}/{self.error}/{self.done}]>"


class Connection:
    def __init__(self, url, key, master_key=None):
        """
        Main class

        :param url: Service url
        :param key: Key for SQL requests
        :param master_key: (optional)
        """
        self.url = url[:-1] if url.endswith("/") else url
        self.key = key
        self.master_key = master_key
        status = self._check()  # Check the key
        if not status[0]:
            raise KeyException(self.key, status[1], status[2])

    def _request(self, path, params, timeout, get=False):
        """
        Send a POST

        :param path: e.g "/sql"
        :param params: JSON parameters
        :param timeout: Timeout after which ConnectException will be raised
        :param get: GET method?
        :return: Deserialized JSON
        """
        try:
            resp = r.request("POST" if not get else "GET", self.url + path, json=params, timeout=timeout).json()
        except:
            raise ConnectException()
        return resp

    def _check(self):
        """
        Validate key

        :return: True/False
        """
        if not self.key:
            raise KeyException('bad_key', "Key was not specified")
        resp = self._request("/creds", {"key": self.key}, 3)
        if not resp['error']:
            return [True]
        else:
            return [False, resp['error_text'], resp['details']]

    def execute(self, query, db=None, values=None, ret_dict=True, background=False):
        """
        Execute SQL query

        :param query: SQL Query
        :param db: Short DB name to execute on (must be available in remote_sql script)
        :param values: Insert/Update values
        :param ret_dict: Whether return dict or list
        :param background: Background execution?
        :return: Task (background) / Response
        """
        if not self.key:
            raise KeyException('bad_key', "Key was not specified")
        resp = self._request("/sql", {"key": self.key, "query": query, "db": db, "values": values, "ret_dict": ret_dict,
                                      "background": background}, 5)
        if resp['error']:
            raise GeneralException(resp['error_text'], resp['details'])
        return Response(resp) if not background else Task(self.url, self.key, resp['data']['task_id'])

    def get_tasks(self):
        """
        Get tasks statistics

        :return: Tasks object
        """
        if not self.master_key:
            raise KeyException('bad_master_key', "Master key was not specified")
        resp = self._request("/tasks", {"key": self.master_key}, 3, True)
        if resp['error']:
            raise GeneralException(resp['error_text'], resp['details'])
        return Tasks(self.url, self.key, resp)

    def clear_tasks(self):
        """
        Clear task list on server

        :return: 'error': 0
        """
        if not self.master_key:
            raise KeyException('bad_master_key', "Master key was not specified")
        resp = self._request("/cleartasks", {"key": self.master_key}, 3)
        if resp['error']:
            raise GeneralException(resp['error_text'], resp['details'])
        return resp

    def __repr__(self):
        return f"<Connection ['{self.url}']>"
