### A. Setup Notes for VM (`setup_notes_vm.md`)

## Cloud & Region

- **Cloud:** Microsoft Azure
- **Region:** (Norway East)
- **DBA:** classdbnetid

## Ordered steps you executed:**

1. Connect to Your VM
   •	Use SSH to connect from your terminal:
   ssh phil@51.120.121.142      pw: Informatics!

•	<azure_user> is your VM's admin username.
•	<public_ip> is shown in the Azure

---

2. Update and Harden OS
   •	Keep your system updated:
   sudo apt update && sudo apt upgrade -y

---

3. Install MySQL Server
   •	Install MySQL:
   sudo apt install mysql-server mysql-client -y
   •	Verify installation:
   mysql --version
   sudo systemctl status mysql

---

4. Configure MySQL for Remote Access
   •	Edit config file for remote connections:
   sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
   •	Change:
   bind-address = 0.0.0.0
   •	Restart MySQL:
   sudo systemctl restart mysql

---

5. Create MySQL User and Database
   •	Log into MySQL shell:
   sudo mysql
   •	Execute:
   CREATE USER 'phil'@'%' IDENTIFIED BY 'Informatics!';
   CREATE DATABASE classdbnetid;
   GRANT ALL PRIVILEGES ON classdbnetid.* TO 'phil'@'%';
   FLUSH PRIVILEGES;
   EXIT;

---

6. Configure Azure Network Security
   •	Verify Firewall Rules:
   Your screenshot confirms inbound rules for:
   •	Port 22 (SSH): required for admin access
   •	Port 3306 (MySQL): required for remote DB connections

---

7. Test Remote Connection (from your computer or another VM)
   •
   mysql -u phil -p -h 51.120.121.142 -P 3306

---

8. Set Up Python Connection
   •	Use connection string in your .env file:
   text
   VMDBHOST=51.120.121.142
   VMDBPORT=3306
   VMDBUSER=vmuser
   VMDBPASS=Informatics!
   VMDBNAME=classdbnetid

- MySQL installation and configuration instructions
- Network/firewall setup
- User/database creation commands
- Security hardening
- Issues/troubleshooting (with timestamps)

## Start-to-finish elapsed time**

(5.1 s) measured by me
