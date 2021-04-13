import configparser, glob, os, shutil
from os.path import join
from time import sleep
from FTPClient import FTPClient

dirname = os.path.dirname(__file__)

config = configparser.ConfigParser()
config.read(join(dirname, 'config.ini'))

ftp_ip = config['SERVER']['IP']
ftp_usr = config['SERVER']['FTP_USERNAME'] 
ftp_pwd = config['SERVER']['FTP_PASSWORD']

ftp_client = FTPClient(ftp_ip, ftp_usr, ftp_pwd)

pending_path = 'pending'
extension = 'csv'
os.chdir(join(dirname, pending_path))

def listFilenames():
    files = glob.glob('*.{}'.format(extension))
    return files

def sendFiles(files):
    try:
        for file in files:
            filename = file.replace(":", "_")
            with open(file, "rb") as file_stream:
                ftp_client.conn.storbinary("{CMD} {FileName}".format(CMD="STOR", FileName=filename), file_stream)

            if not os.path.exists(join(dirname, '../records')):
                os.mkdir(join(dirname, '../records'))
            shutil.move(file, join(dirname, '../records/{}'.format(file)))
    except:
        ftp_client.conn.close()
        try:
            ftp_client.reconnect()
        except:
            pass

def main():
    while True:
        files = listFilenames()
        if (len(files)):
            sendFiles(files)

if __name__ == "__main__":
    main()