import paramiko

#Define the list of hosts, including IP address, username, password
hosts =     ['192.168.0.109', '192.168.0.108']
usernames = ['rolex', 'omega']
passwords = ['123456', '123456']
#Directory containing downloaded files from remote clients
#Define the commands to execute on remote machines
commands = [
    "gnome-terminal --disable-factory -- bash -c \
    'cd Documents/prtb/build/bin; \
    ./PrtbBtwnDrHrd_MultiThreaded \
    -r 4 \
    -j 1 \
    -i ~/Documents/prtb/ \
    -o ~/Documents/prtb/Results/; \
    read -p \"Press Enter to exit...\"'",
]
#Create a list to store ssh client objects
ssh_clients = []

#Loop through each host and establish SSH connection
for i in range(len(hosts)):
    host = hosts[i]
    username = usernames[i]
    password = passwords[i]
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)
        print(f"{host} is online")
        ssh_clients.append(ssh)
    except paramiko.AuthenticationException as e:
        print(f"Unable to establish SSH connection to {host}: {e}")
    except Exception as e:
        print(f"Error while connecting to {host}: {e}")
#Loop through each host end execute the command
for ssh in ssh_clients:
    for command in commands:
        stdin, stdout, stderr = ssh.exec_command(command)
    ssh.close() #Close the SSH connection