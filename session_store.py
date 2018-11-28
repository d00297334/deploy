import os, base64

class SessionStore:
    def __init__(self):
        # this is your file cabinet
        # will contain many dictionaries
        # one per session
        self.sessions = {}
        return

    def generateSessionId(self):
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode("utf-8")
        return rstr

    def createSession(self):
        sessionId = self.generateSessionId()
        # add a new session (dictionary) to the "file cabinet"
        # use the generated session ID
        self.sessions[sessionId] = {}
        return sessionId

    def getSession(self, sessionId):
        if sessionId in self.sessions:
            # return existing session by ID
            return self.sessions[sessionId]
        else:
            return None

    def deleteSession(self, sessionId):
        if sessionId in self.sessionStore:
            del self.sessionstore[sessionId]
        return self.getSession[sessionId]

    def exists(self, session):
        return session in self.sessionStore