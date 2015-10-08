from threading import Thread, Event
import datetime
import logging

sessions = {}
session_creation_time = {}

session_timeout = datetime.timedelta(minutes=1)

class TimeoutThread(Thread):
    def __init__(self, timeout):
        Thread.__init__(self, daemon=True)
        self.timeout = timeout
        self.stopped = Event()

    def run(self):
        while not self.stopped.wait(timeout=self.timeout):
            expired_ids = [sid for sid, creation_time in session_creation_time.items() if datetime.datetime.utcnow() - creation_time > session_timeout]

            if len(expired_ids):
                logging.debug('Expiring sessions: {}'.format(expired_ids))
                sessions = {sid: username for sid, username in sessions.items() if sid not in expired_ids}
                session_creation_time = {sid: creation_time for sid, creation_time in session_creation_time.items() if sid not in expired_ids}

timeout_thread = TimeoutThread(10)
timeout_thread.start()


def validate_session(sid):
    if sid in sessions:
        return True
    return False


def authenticate(self, request, username, password):
    if username == 'test' and password == 'test':
        new_sid = 0
        if len(sessions):
            new_sid = max(sessions.keys()) + 1

        sessions[new_sid] = username
        session_creation_time[new_sid] = datetime.datetime.utcnow()
        return True
    else:
        return False