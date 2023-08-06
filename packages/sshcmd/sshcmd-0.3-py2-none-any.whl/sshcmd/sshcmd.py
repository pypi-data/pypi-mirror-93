import paramiko


class SshCmd(object):
    def __init__(self, hostname, username, password):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=hostname, port=22, username=username, password=password)
        except Exception as e:
            raise

    def close(self):
        self.client.close()

    def exec_cmd(self, cmdstr):
        try:
            stdin, stdout, stderr = self.client.exec_command(cmdstr)
            result = stdout.read()
            result = result.decode(encoding='UTF-8', errors='strict')

            errmsg = stderr.read()
            errmsg = errmsg.decode(encoding='UTF-8', errors='strict')

            if errmsg != "":
                raise Exception(errmsg)

            return result

        except Exception as e:
            raise
