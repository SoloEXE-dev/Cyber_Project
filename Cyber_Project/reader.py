from paramiko import SSHClient, AutoAddPolicy
import os
import subprocess

ip = '172.22.0.2'
password = 'password'
folders = ('/main/dummy','/backup')
folder_path = '/main/dummy/'


def deletedir():
    # for filename in os.listdir(folder_path):
    #     file_path = os.path.join(folder_path, filename)
    #     if os.path.isfile(file_path):
    #         os.system('sh /programs/removedata.sh')
    #         print(filename, "is removed")
    os.system('rm -r /backup/')
    os.system('rm -r /main/')

client = SSHClient()
client.load_system_host_keys()

client.set_missing_host_key_policy(AutoAddPolicy())

for filename in os.listdir(folder_path):
    if('tps' in filename):
        file_path = os.path.join(folder_path, filename)
        # check file permission change
        output = subprocess.check_output(['stat', '-c', "%a %n", file_path])
        msg = output.decode('utf-8')
        if(msg[0:3] != "755"):
            print( msg , "\n perms not matched\n")
            deletedir()


        else:

        # open file and check if encryption is done

            client.connect(hostname=ip, username='root', password=password)

            sftp_client = client.open_sftp()
            remote_file = sftp_client.open('/main/dummy/tps.txt')
            try:
                localfile = open(file_path)
                for line in remote_file:
                    if(line != localfile.readline()):
                        print("file content do not match\n")
                        deletedir()
                        break
            except:
                print("cannot open file\n")
                deletedir()
