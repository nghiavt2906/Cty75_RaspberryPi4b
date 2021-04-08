from ftplib import FTP

class FTPClient:
    def __init__(self, ftp_ip, ftp_usr, ftp_pwd):
        self.ftp_ip = ftp_ip
        self.ftp_usr = ftp_usr
        self.ftp_pwd = ftp_pwd
        self.conn = FTP(ftp_ip)
        self.conn.login(user=ftp_usr, passwd=ftp_pwd)

    def close(self):
        self.conn.close()

    def reconnect(self):
        self.conn = FTP(self.ftp_ip)
        self.conn.login(user=self.ftp_usr, passwd=self.ftp_pwd)