#####################################################
# ................ A B O U T ..........................
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This  is user-interactive  configuration  management
# program  written  in  python.  Main features of this
# program include configuring following things:
# 1. Hadoop NN/DN configuration in AWS  or on-premises
# 2. Web Server  configuration in AWS  or  on-premises
# 3. Configure/Install   Docker   Community    Edition
# 4. Setup  webserver  in  EC2  instance,  with static
#    content being through CloudFront
# 5. Basic RHEL commands
# 6. LVM Partitioning

# Voice Commands Updated !!!
######################################################


######################################################
# ............... A U T H O R S .......................
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Adarsh Saxena     (linkedin.com/in/theadarshsaxena)
#  Niharika Dhanik	 (linkedin.com/in/niharika-dhanik)
#  Ajmal Muhammed
#  Raghav Khandelwal
######################################################


######################################################
# ....... C O D E ... S T A R T S ... H E R E..........
######################################################


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ...... Importing all the required libraries ........
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import subprocess
import pyttsx3
import sys

# import asyncio
# import boto3
import os
import subprocess
import getpass
import sys


# Introduction
print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
print("Hi,I am Alex, your personal assistant.")
print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
print(
    "\nWelcome to the world of automation. Please type your requests using the menu below and i will automatically configure it for you.")
print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
print(
    "\Following are the automated configurations\n1. Setup Webserver And Docker Configuration on Local and Remote System\n2. Setup Hadoop Cluster\n3. Run RHEL Commands\n4. Setup Webserver in Remote System Using SSH\n5. LVM Partitioning")
main_input = int(input("\nEnter Your Choice : "))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# .................. MENU 1 ..........................
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Webserver And Docker Configuration on Local and Remote System
if main_input == 1:

    while True:
        os.system('clear')
        print("Welcome to the Automated Configuration program".center(80))
        print("python\n\n\n".center(80))

        print("Where Do you want to setup\n1. Local System\n2. Remote System")

        while True:
            c1 = int(input('Enter Your Choice'))
            if c1 == 1:
                sys1 = "Local System"
                break
            elif c1 == 2:
                sys1 = "Remote System"
                break
            else:
                print("choose Correct number")

        os.system('clear')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ................... MENU 2 .........................
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup Hadoop Cluster
elif main_input == 2:
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # .......... TO CONFIGURE HADOOP DN ....................
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def hadoopdn(sys1):
        # write the hadoop datanode configuration inside this block
        # this function takes sys1 variable's value for the type of server = either Remote OS or Local OS, then, do the things accordingly
        if sys1 == "Remote System":
            Remote_ip = input("Please, Enter remote IP: ")
            Key = input("Enter key(*.pem): ")

            if not Key.endswith(".pem"):
                Key += ".pem"
            keypath_subprocess = subprocess.Popen("find / -name {}".format(Key), shell=True, stdout=subprocess.PIPE)
            keypath = keypath_subprocess.stdout.read().decode()

            # Need to add code to check if softwares are installed or not
            # {
            # 	//code here
            # }

            datanode_directory = input("Enter the name which you prefer for Slave node directory: ")

            os.system("sshpass -p {} sudo ssh root@{} 'sudo mkdir -p ~/hadoopautomation/{}'".format(keypath, Remote_ip,
                                                                                                    datanode_directory))
        else:
            datanode_directory = input("Enter the name which you prefer for Slave node directory: ")
            os.system("mkdir -p ~/hadoopautomation/{}".format(datanode_directory))

        Master_IP = input("Enter Master node IP: ")
        f = open("core-site.xml", "w+")
        f.write('''<?xml version="1.0"?>
      <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
    
      <!-- Put site-specific property overrides in this file. -->
    
      <configuration>
    
      <property>
      <name>fs.default.name</name>
      <value>hdfs://{}:9001</value>
      </property>
    
      </configuration>'''.format(Master_IP))
        f.close()

        f = open("hdfs-site.xml", "w+")
        f.write('''<?xml version="1.0"?>
      <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
    
    
      <!-- Put site-specific property overrides in this file. -->
    
    
      <configuration>
    
      <property>
      <name>dfs.data.dir</name>
      <value>~/hadoopautomation/{}</value>
      </property>
    
      </configuration>'''.format(datanode_directory))
        f.close()

        if sys1 == "Remote System":
            os.system('scp -i {} hdfs-site.xml ec2-user@{}:/etc/hadoop'.format(keypath, Remote_ip))
            os.system('scp -i {} core-site.xml ec2-user@{}:/etc/hadoop'.format(keypath, Remote_ip))

        else:
            os.system("mv hdfs-site.xml /etc/hadoop")
            os.system("mv core-site.xml /etc/hadoop")


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # .......... TO CONFIGURE HADOOP NN ....................
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def hadoopnn(sys1):
        # write the hadoop namenode configuration inside this block
        # this function takes sys1 variable's value for the type of server = either Remote OS or Local OS, then, do the things accordingly
        if sys1 == "Remote System":
            Remote_ip = input("Please, Enter remote IP: ")
            Key = input("Enter key(*.pem): ")

            if not Key.endswith(".pem"):
                Key += ".pem"
            keypath_subprocess = subprocess.Popen("find / -name {}".format(Key), shell=True, stdout=subprocess.PIPE)
            keypath = keypath_subprocess.stdout.read().decode()

            # Need to add code to check if softwares are installed or not
            # {
            # 	//code here
            # }

            namenode_directory = input("Enter the name which you prefer for Master node directory: ")
            os.system("sshpass -p {} sudo ssh root@{} 'sudo mkdir -p ~/hadoopautomation/{}'".format(keypath, Remote_ip, datanode_directory))
        else:
            namenode_directory = input("Enter the name which you prefer for Master node directory: ")
            os.system("mkdir -p ~/hadoopautomation/{}".format(namenode_directory))

        Master_IP = "0.0.0.0"

        if sys1 == "Remote System":
            Master_IP = "Enter your public IP: "

        f = open("core-site.xml", "w+")
        f.write('''<?xml version="1.0"?>
        <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
    
        <!-- Put site-specific property overrides in this file. -->
    
        <configuration>
    
        <property>
        <name>fs.default.name</name>
        <value>hdfs://{}:9001</value>
        </property>
    
        </configuration>'''.format(Master_IP))
        f.close()

        f = open("hdfs-site.xml", "w+")
        f.write('''<?xml version="1.0"?>
        <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
    
    
        <!-- Put site-specific property overrides in this file. -->
    
    
        <configuration>
    
        <property>
        <name>dfs.data.dir</name>
        <value>~/hadoopautomation/{}</value>
        </property>
    
        </configuration>'''.format(namenode_directory))
        f.close()

        if sys1 == "Remote System":
            os.system('scp -i {} hdfs-site.xml ec2-user@{}:/etc/hadoop'.format(keypath, Remote_ip))
            os.system('scp -i {} core-site.xml ec2-user@{}:/etc/hadoop'.format(keypath, Remote_ip))
            os.system("sshpass -p {} sudo ssh root@{} 'sudo hadoop namenode -format'".format(keypath, Remote_ip))

        else:
            os.system("mv hdfs-site.xml /etc/hadoop")
            os.system("mv core-site.xml /etc/hadoop")
            os.system("sudo hadoop namenode -format")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ........... TO CONFIGURE WEB SERVER ...................
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    def webconf():
        # webserver configuaration
        # this function takes sys1 variable's value for the type of server = either Remote OS or Local OS, then, do the things accordingly
        if c1 == 1:  # To check if it is local system
            if str(subprocess.run(['rpm', '-q', 'httpd'], stdout=subprocess.PIPE).stdout).split(' ')[3] == 'not':
                subprocess.run(['yum', 'install', '-y', 'httpd'])
            else:
                print("Httpd already present, Starting the httpd service")
            subprocess.run(['systemctl', 'start', 'httpd'])
        # You can change anything over here according to what research you have done


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ........... TO CONFIGURE DOCKER ........................
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def dockersetup():
        # this function takes sys1 variable's value for the type of server = either Remote OS or Local OS, then, do the things accordingly
        if c1 == 1:  # To check if it is local system
            if str(subprocess.run(['rpm', '-q', 'docker'], stdout=subprocess.PIPE).stdout).split(' ')[3] == 'not':
                subprocess.run(['yum', 'install', '-y',
                                'docker'])  # When doing in AWS EC2 instance, code will change for OS present in VM
            else:
                print("Docker already present, Starting the docker service")
            subprocess.run(['systemctl', 'start', 'docker'])


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ......... TO CONFIGURE WEBSERVER IN AWS .................
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def awswebserver():
        os.execl("awscliscript.sh")
        # awcliscript.sh file is present in local system (I will also push that in my github repository)


    # menu starts from here
    print("What do you want to do?")
    print("1. Setup Hadoop Data node in {}".format(sys1))
    print("2. Setup Hadoop Name node in {}".format(sys1))
    print("3. Setup Web Server in {}".format(sys1))
    print("4. Setup Docker in {}".format(sys1))
    print("5. Configure the webserver in AWS with EC2 Instance, static content in CloudFront")
    print("6. Configure Hadoop Cluster (Datanode + NameNode) in AWS with proper security")

    while True:
        c2 = int(input('Enter Your Choice'))
        if c2 == 1:
            hadoopdn(sys1)
            break
        elif c2 == 2:
            hadoopnn(sys1)
            break
        elif c2 == 3:
            webconf()
            break
        elif c2 == 4:
            dockersetup()
            break
        elif c2 == 5:
            awswebserver()
            break
        else:
            print("Enter the correct option")

    askcontinue = input('Do you want to exit(y/n)')
    if askcontinue == 'y':
        exit()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ................... MENU 3 .........................
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# RHEL Basic Commands
elif main_input == 3:
    while True:
        c3 = int(input(
            "\nPress 1: To view todays's date\nPress 2: To view present month's calendar\nPress 3: To start Firewall\nPress 4: To check the status of firewall\nPress 5: To stop firewall\nEnter Your Choice : "))
        if c3 == 1:
            print("\nToday's date is given as below")
            os.system("date")
        if c3 == 2:
            print("\nThis month's calendar is given as below")
            os.system("cal")
        if c3 == 3:
            os.system("systemctl start Firewall")
            pyttsx3.speak("Firewall system is activated")
        if c3 == 4:
            os.system("systemctl start Firewall")
            print("Firewall system status is under observation")
        if c3 == 5:
            os.system("systemctl start Firewall")
            print("Firewall system is deactivated")
            else:
            print("Try again with a valid input")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ................... MENU 5 .........................
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function Definition
elif main_input == 5:
    # Definition 1
    def printing1():
        return ("\nEnter the following commands for the successful creation of paritition\nStep 1. n (to create new partition)\nStep 2. p / e (choose between which type of partition is to be created i.e., primary, extended)\nStep 3. value (choose in which part partition is to done i.e., 1,2 3 or 4, default 1)\nStep 4. Press Enter\nStep 5.value (set partition size)\nStep 6. p (to view the details of created primary partition)\nStep 7. w (to save the partition)")

    # Definition 2
    def disk(disk_choice):
        disk_choice = input("\nEnter name of disk(ie., sda/sdb2/sd1/):")
        return (os.system("fdisk /dev/" + disk_choice))

    # Partitioning
    while True:
        c4 = int(input(
            "\nPress 1: To view the hard drive\nPress 2: To create partiton\nPress 3:To format partition\nPress 6: To load driver\nPress 5: To check the list of existing partitons\nPress 6: To exit\nEnter Your Choice : "))
    if c4 == 1:
        print("\nFollowing is the list of hard disks available")
        print(os.system("fdisk -l"))
    elif c4 == 2:
        print("\nFollowing is the list of hard disks available")
        print(os.system("fdisk -l"))
        printing1()
        disk(disk_choice)
        if c4 == 3:
            os.system("undevadm settle")
        print("Drivers loaded successfully")
    elif c4 == 4:
        os.system("mkfs.ext4 /dev/" + disk_choice)
        print("Partition formatted successfully")
    elif c4 == 5:
        os.system("df -h")
    elif c4 == 6:
        exit()
    else:
        print("Try again with a valid input")

# Another Method for Partitioning using bash script in python

"""  
def printing2():
  return("\n1. o - clear the in memory partition table\n2. n - new partition\n3. p - primary partition\n4. 1 - partition number 1(default - start at beginning of disk)\n5. +100M - 100 MB boot parttion\n6. n - new partition\n7. p - primary partition\n8. 2 - partion number 2(default, start immediately after preceding partition & default, extend partition to end of disk)\n9. a - make a partition bootable\n10. 1 - bootable partition is partition 1 -- /dev/sda1\n11. p - print the in-memory partition table\n12. w - write the partition table\n13. q - done")
	return("Format : s/\s*\([\+0-9a-zA-Z]*\).*/\1/ << EOF | fdisk ${TGTDEV}")



def run_script(script, stdin=None):
    import subprocess
    # Note: by using a list here (['bash', ...]) you avoid quoting issues, as the arguments are passed in exactly this order (spaces, quotes, and newlines won'tcause problems):
    proc = subprocess.Popen(['bash', '-c', script],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode:
        raise ScriptException(proc.returncode, stdout, stderr, script)
    return stdout, stderr

class ScriptException(Exception):
    def __init__(self, returncode, stdout, stderr, script):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        Exception.__init__('Error in script')


printing2()
script_ip = input("Enter your bash script using above menu : ")
while ScriptException(Exception)=True:
	print(run_script_("sed -e '" +script_ip"' << EOF | fdisk ${disk(disk_choice)}"))
else:
	break
"""


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ................... MENU 4 .........................
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup Webserver in Remote System Using SSH
elif main_input == 4:

    os.system('clear')
    print('''Slect option to perform operation 1.Webservice 2.Docker''')
    s = int(input('Enter choice: '))
    if s == 1:
        os.system('clear')
        print('''1.install httpd   2. start httpd  3.Configure httpd  4.open file on webserver ''')
        ii = int(input('enter choice:'))
        if ii == 1:
            os.system("dnf install httpd")
        elif ii == 2:
            os.system('systemctl start httpd')
        elif ii == 3:
            print('Create a html file')
            fl = input('Enter file name:')
            # os.system('vim {}'.format(fl))
            os.system('cat >{}.html | cd /var/www/html/'.format(fl))
        elif ii == 4:
            os.system('ifconfig enp0s3')
            a = input('Enter IP       =')
            b = input('Enter file name=')
            os.system('curl http://{}/{}.html'.format(a, b))
        else:
            print('Enter valid choice')



    os.system("tput setaf 3")
    print("\t\t\t\t...Welcomes you...")
    os.system("tput setaf 7")
    print("\t\t\t\t---------------------")

    password = getpass.getpass('Enter password : ')

    if password != "ajmal":
        print('wrong password')
        exit()


    def webserver():
        os.system('sshpass -p {} ssh root@{} yum install httpd -y'.format('ajmal', ip))
        os.system('sshpass -p {} ssh root@{}  systemctl start httpd'.format('ajmal', ip))
        os.system('sshpass -p {} ssh root@{}  systemctl enable httpd'.format('ajmal', ip))
        os.system('sshpass -p {} ssh root@{}  systemctl status httpd'.format('ajmal', ip))


    r = input('How you want to login as?(local/remote)')
    print('you opted for the option {}'.format(r))

    while True:
        print("\n \n")
        if r == "remote":
            print("""
                        Press 1: configuring_local_webserver
                        Press 2: to exit
                    """)
            i = int(input("Enter ur choice : "))
            if i == 2:
                exit()
            else:
                ip = input('Enter Remote IP:')
                print('Entered ip is {}'.format(ip))
                webserver()
        break

else:
    print("\n\nTHE PROGRAM ENDS")
    exit()
###########################################################
# ......... E N D ... O F ... P R O G R A M ................
###########################################################


# LEARNINGS
# asyncio can be used for asynchronous programming and hence, helpful when some os command take too much time
# help(module/function) == can be used in python to get the manual of module or function
# uses od various attributes of subprocess


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# .............. S O U R C E S .............................
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html
#  https://docs.aws.amazon.com/cli/latest/reference/
#  python.org
#  stackoverflow
