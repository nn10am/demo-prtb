import os
import paramiko

# Define the list of hosts, usernames, and passwords
hosts = ['192.168.0.109', '192.168.0.108']
usernames = ['rolex', 'omega']
passwords = ['123456', '123456']

# Define the remote and local paths
remote_paths = ['/home/rolex/Documents/prtb/Results', '/home/omega/Documents/prtb/Results']
local_path = '/home/nhat/Documents/Distributed-Downloads/'

# Create a list to store the SSH client objects
ssh_clients = []

# Loop through each host and establish an SSH connection
for i in range(len(hosts)):
    host = hosts[i]
    username = usernames[i]
    password = passwords[i]
    remote_path = remote_paths[i]
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)
        print(f"{host} is online")
        ssh_clients.append((ssh, remote_path, host))
    except paramiko.AuthenticationException:
        print(f"Authentication failed for {host}")
    except paramiko.SSHException as e:
        print(f"Unable to establish SSH connection to {host}: {e}")
    except Exception as e:
        print(f"Error while connecting to {host}: {e}")

# Loop through the SSH clients and download the CSV files
for ssh, remote_path, host in ssh_clients:
    # Use SFTP to navigate to the remote directory
    sftp = ssh.open_sftp()
    sftp.chdir(remote_path)

    # Loop through the files in the remote directory
    for filename in sftp.listdir():
        if filename.endswith('.csv'):
            # Get the file from the remote machine and save it locally
            remote_file = os.path.join(remote_path, filename)
            local_file = os.path.join(local_path, f"{host}_{filename}")
            sftp.get(remote_file, local_file)
            print(f"{filename} downloaded from {host}")

    # Close the SFTP connection
    sftp.close()

# Close the SSH connections
for ssh, _, _ in ssh_clients:
    ssh.close()
