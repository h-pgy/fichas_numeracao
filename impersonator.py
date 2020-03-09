import win32security
import win32con

class Impersonate:

    def __init__(self,login,password):

        self.domain='REDE'

        self.login=login

        self.password=password

    def logon(self):

        self.handel=win32security.LogonUser(self.login,self.domain,self.password,

                win32con.LOGON32_LOGON_INTERACTIVE,win32con.LOGON32_PROVIDER_DEFAULT)

        win32security.ImpersonateLoggedOnUser(self.handel)

    def logoff(self):

        win32security.RevertToSelf() #terminates impersonation

        self.handel.Close() #guarantees cleanup

