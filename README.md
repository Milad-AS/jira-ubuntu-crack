# jira-ubuntu-crack
How to Install and Crack Jira on Ubuntu (Without Docker)

# 🚀 Atlassian Jira Activation Guide (Ubuntu Native Version)

<div dir="ltr">

This document is dedicated to the **Atlassian Agent** method, which is considered the cleanest and most stable approach for bypassing Atlassian licenses (Jira, Confluence, Bitbucket) in Linux environments.

</div>

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Step 1: Installing Jira on Ubuntu](#step-1-installing-jira-on-ubuntu)
- [Step 2: Download Required Files](#step-2-download-required-files)
- [Step 3: Preparing the Agent File](#step-3-preparing-the-agent-file)
- [Step 4: Running the Python Patch Script](#step-4-running-the-python-patch-script)
- [Step 5: Injecting Agent into Jira JVM](#step-5-injecting-agent-into-jira-jvm)
- [Step 6: Cleanup and Restart](#step-6-cleanup-and-restart)
- [Step 7: Verify Agent Loading](#step-7-verify-agent-loading)
- [Step 8: Generating License Code](#step-8-generating-license-code)
- [Key Points for Future](#key-points-for-future)
- [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## 🛠 Prerequisites

<div dir="ltr">

Before starting, ensure the following prerequisites are installed on your system:

</div>

```bash
# Update repositories
sudo apt update && sudo apt upgrade -y

# Install Java (version 11 or 17 for Jira)
sudo apt install -y openjdk-11-jdk

# Install Python and prerequisites
sudo apt install -y python3 python3-pip

# Install required tools
sudo apt install -y wget curl net-tools

# Check Java version
java -version

# Check Python version
python3 --version
```

---

## Step 1: Installing Jira on Ubuntu

### 1.1 Download and Install Jira

<div dir="ltr">

Download the latest version of Jira from the official website:

</div>

```bash
# Create installation directory
sudo mkdir -p /opt/atlassian/jira
cd /opt/atlassian/jira

# Download Jira (version 9.12 or higher)
sudo wget https://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-software-9.12.0.tar.gz

# Extract files
sudo tar -xzf atlassian-jira-software-9.12.0.tar.gz --strip-components=1 -C /opt/atlassian/jira/

# Create Jira user
sudo useradd --create-home --home-dir /opt/atlassian/jira-home --shell /bin/bash jira

# Set file ownership
sudo chown -R jira:jira /opt/atlassian/jira
sudo mkdir -p /opt/atlassian/jira-home
sudo chown -R jira:jira /opt/atlassian/jira-home
```

> **⚠️ IMPORTANT NOTE**: Make sure Jira is installed in the `/opt/atlassian/jira` path. If your installation is in a different directory (e.g., in `/home/gulfgate/...`), you will need to edit the paths in the following steps accordingly.

### 1.2 Configure Port and Database

<div dir="ltr">

Edit the port configuration file:

</div>

```bash
sudo nano /opt/atlassian/jira/conf/server.xml
```

<div dir="ltr">

Find the Connector line and change the port (default is 8080):

</div>

```xml
<Connector port="8080" protocol="HTTP/1.1"
           connectionTimeout="20000"
           redirectPort="8443"
           maxThreads="200"
           minSpareThreads="25"
           enableLookups="false"
           acceptCount="100"
           URIEncoding="UTF-8"/>
```

### 1.3 Initial Jira Setup

```bash
# Run Jira for the first time
sudo -u jira /opt/atlassian/jira/bin/start-jira.sh

# Check logs
sudo tail -f /opt/atlassian/jira-home/log/atlassian-jira.log
```

<div dir="ltr">

Now open your browser and navigate to `http://your-server-ip:8080`. Follow the installation steps until you reach the **Server ID** page. Save this ID for the license generation step.

</div>

---

## Step 2: Download Required Files

<div dir="ltr">

Download both the agent file and the Python patch script:

</div>

```bash
# Create agent directory
sudo mkdir -p /opt/atlassian/jira/agent
cd /tmp

# Download the atlassian-agent.jar file
# (Replace the URL with your actual download link)
wget https://example.com/path/to/atlassian-agent.jar

# Download the Python patch script
wget https://example.com/path/to/atlassian_patch.py

# Make the Python script executable
chmod +x atlassian_patch.py
```

---

## Step 3: Preparing the Agent File

<div dir="ltr">

Set up the agent file with proper permissions:

</div>

```bash
# Copy agent file to installation directory
sudo cp atlassian-agent.jar /opt/atlassian/jira/agent/

# Set ownership (very important)
sudo chown -R jira:jira /opt/atlassian/jira/agent/
sudo chmod 644 /opt/atlassian/jira/agent/atlassian-agent.jar

# Verify settings
ls -la /opt/atlassian/jira/agent/
```

---

## Step 4: Running the Python Patch Script

<div dir="ltr">

The Python patch script (`atlassian_patch.py`) is designed to verify and fix any permission or configuration issues. This script only uses standard Python libraries, so no additional packages are needed.

</div>

```bash
# First, ensure your Jira path is correct
# If Jira is installed in a custom location, edit the script or specify the path

# Run the Python patch script
sudo python3 atlassian_patch.py
```

<div dir="ltr">

### What the Python Script Does:

- Checks if Jira is installed in the expected location
- Verifies file permissions
- Tests if the agent can be loaded
- Identifies any access issues
- Provides recommendations for fixes

### About the "Unknown" Version Issue:

If you see "Unknown" when checking the Jira version, it means Jira does not allow the current user to access its internal files. This is a permission issue that can be resolved by:

1. **Running commands with `sudo`** - This gives you the necessary privileges
2. **Checking ownership** - Ensure all Jira files are owned by the `jira` user
3. **Verifying file permissions** - Make sure files have the correct read/write permissions

</div>

```bash
# If you encounter "Unknown" version issues, try:
sudo -u jira python3 atlassian_patch.py

# Or fix permissions manually:
sudo chown -R jira:jira /opt/atlassian/jira
sudo chmod -R 755 /opt/atlassian/jira
```

---

## Step 5: Injecting Agent into Jira JVM

<div dir="ltr">

For Jira to recognize the agent at startup, we need to add the `-javaagent` parameter to the Java variables.

### Method 1: Edit setenv.sh (Recommended)

</div>

```bash
# Edit setenv.sh file
sudo nano /opt/atlassian/jira/bin/setenv.sh
```

<div dir="ltr">

Add this line at the beginning of the file (after the first line):

</div>

```bash
export JVM_SUPPORT_RECOMMENDED_ARGS="-javaagent:/opt/atlassian/jira/agent/atlassian-agent.jar ${JVM_SUPPORT_RECOMMENDED_ARGS}"
```

### Method 2: Edit catalina.sh (Alternative Method)

```bash
sudo nano /opt/atlassian/jira/bin/catalina.sh
```

<div dir="ltr">

At the beginning of the file, after the `#!/bin/sh` line, add this line:

</div>

```bash
JAVA_OPTS="$JAVA_OPTS -javaagent:/opt/atlassian/jira/agent/atlassian-agent.jar"
```

---

## Step 6: Cleanup and Restart

<div dir="ltr">

Before starting, make sure no interfering processes are occupying the ports.

</div>

```bash
# Stop Jira
sudo /opt/atlassian/jira/bin/stop-jira.sh

# Stop all Java processes (optional - use with caution)
sudo pkill -9 java

# Check ports in use
sudo netstat -tlnp | grep 8080

# Clean cache and temporary files
sudo rm -rf /opt/atlassian/jira-home/logs/*.log
sudo rm -rf /opt/atlassian/jira/work/*

# Restart Jira
sudo -u jira /opt/atlassian/jira/bin/start-jira.sh

# Check logs to ensure execution
sudo tail -f /opt/atlassian/jira-home/log/catalina.out
```

---

## Step 7: Verify Agent Loading

<div dir="ltr">

We need to ensure the agent is actually loaded.

</div>

```bash
# Check for javaagent in processes
ps aux | grep javaagent

# More detailed check by viewing logs
sudo grep -i "agent" /opt/atlassian/jira-home/log/catalina.out

# Or check Jira logs
sudo grep -i "atlassian-agent" /opt/atlassian/jira-home/log/atlassian-jira.log

# Run the Python patch script again to verify
sudo python3 atlassian_patch.py --verify
```

<div dir="ltr">

> **Note**: If you see the path `/opt/atlassian/jira/agent/atlassian-agent.jar` in the output, everything is correct.

</div>

---

## Step 8: Generating License Code

<div dir="ltr">

Now, using the same agent file, we'll generate our custom license code.

### License Generation Formula:

</div>

```bash
# General structure
java -jar /opt/atlassian/jira/agent/atlassian-agent.jar \
  -d -m [email] \
  -n [organization name] \
  -p [product] \
  -o [server address] \
  -s [server ID code]

# Real example
java -jar /opt/atlassian/jira/agent/atlassian-agent.jar \
  -d -m admin@example.com \
  -n "My Company" \
  -p jsm \
  -o http://192.168.1.100:8080 \
  -s BCDE-FGHJ-KLMN-PQRS
```

<div dir="ltr">

### Parameter Explanation:

| Parameter | Description |
|-----------|-------------|
| `-p jsm` | This is the golden switch! It activates both Jira Software and Service Management |
| `-s` | Take the Server ID code from the Jira settings page |
| `-d` | Debug mode (optional) |
| `-m` | Desired email for the license |
| `-n` | Company or organization name |
| `-o` | Full server address (with protocol and port) |

### Activatable Products:

</div>

| Product Code | Description |
|--------------|-------------|
| `jira` | Jira Software |
| `jsm` | Jira Service Manager (Recommended) |
| `conf` | Confluence |
| `bamboo` | Bamboo |
| `bitbucket` | Bitbucket |
| `fisheye` | FishEye |
| `crucible` | Crucible |

---

## 💡 Key Points for Future

<div dir="ltr">

### 1. Jira Updates

If you update Jira, remember to perform Step 5 again (edit setenv.sh), as this file gets overwritten during updates. Also re-run the Python patch script to verify everything is working:

```bash
sudo python3 atlassian_patch.py --after-update
```

### 2. .bat Files

Never go near `.bat` files in Linux; they are decorative and only work on Windows.

### 3. Docker Interference

Always remember that Jira cannot run simultaneously on both Docker and Ubuntu (Native) on the same port.

### 4. Custom Installation Paths

If you installed Jira in a custom location (e.g., `/home/gulfgate/jira`), remember to:
- Update all paths in the agent configuration
- Modify the Python patch script or use the `--path` parameter
- Adjust the service files accordingly

### 5. Regular Backups

</div>

```bash
# Create backup of settings
sudo cp /opt/atlassian/jira/bin/setenv.sh /opt/atlassian/jira/bin/setenv.sh.backup
sudo cp /opt/atlassian/jira/bin/catalina.sh /opt/atlassian/jira/bin/catalina.sh.backup

# Backup the Python patch script
sudo cp atlassian_patch.py /opt/atlassian/jira/agent/

# Backup entire configuration
sudo tar -czf /tmp/jira-backup-$(date +%Y%m%d).tar.gz /opt/atlassian/jira /opt/atlassian/jira-home
```

### 6. Create systemd Service (for auto-start)

```bash
sudo nano /etc/systemd/system/jira.service
```

<div dir="ltr">

File content:

</div>

```ini
[Unit]
Description=Atlassian Jira
After=network.target

[Service]
Type=forking
User=jira
Group=jira
ExecStart=/opt/atlassian/jira/bin/start-jira.sh
ExecStop=/opt/atlassian/jira/bin/stop-jira.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable service
sudo systemctl daemon-reload
sudo systemctl enable jira.service
sudo systemctl start jira.service
sudo systemctl status jira.service
```

---

## 🔧 Troubleshooting Common Issues

<div dir="ltr">

### Issue 1: "Unknown" in Jira Version

If it still shows "Unknown" version, it means Jira doesn't allow the current user to access its internal files. Running the command with `sudo` will solve this.

</div>

```bash
# Check permissions
sudo -u jira ls -la /opt/atlassian/jira/agent/

# Run the Python patch script with sudo
sudo python3 atlassian_patch.py --fix-permissions

# Manual permission fix
sudo chown -R jira:jira /opt/atlassian/jira
sudo chmod -R 755 /opt/atlassian/jira
```

### Issue 2: Agent Not Loading

```bash
# Comprehensive log check
sudo cat /opt/atlassian/jira-home/log/catalina.out | grep -i "javaagent"

# Check environment variables
sudo -u jira cat /opt/atlassian/jira/bin/setenv.sh | grep -i "javaagent"

# Run Python diagnostic
sudo python3 atlassian_patch.py --diagnose
```

### Issue 3: Port Already in Use

```bash
# Find process using the port
sudo lsof -i :8080

# Or
sudo netstat -tlnp | grep 8080

# Stop the process (with caution)
sudo kill -9 [PID]
```

### Issue 4: File Permission Errors

```bash
# Reset permissions
sudo chown -R jira:jira /opt/atlassian/jira
sudo chown -R jira:jira /opt/atlassian/jira-home
sudo chmod -R 755 /opt/atlassian/jira

# Run the Python patch script to verify
sudo python3 atlassian_patch.py --check-permissions
```

### Issue 5: Custom Installation Path

```bash
# If Jira is installed in a custom location, update the Python script
# or use environment variables
export JIRA_HOME="/custom/path/to/jira"
sudo python3 atlassian_patch.py --jira-path="$JIRA_HOME"

# Update agent path in setenv.sh accordingly
# Change: /opt/atlassian/jira/agent/atlassian-agent.jar
# To: /custom/path/to/jira/agent/atlassian-agent.jar
```

---

## 📝 Important Commands Summary

<div dir="ltr">

| Operation | Command |
|-----------|---------|
| Start Jira | `sudo -u jira /opt/atlassian/jira/bin/start-jira.sh` |
| Stop Jira | `sudo -u jira /opt/atlassian/jira/bin/stop-jira.sh` |
| Check Logs | `sudo tail -f /opt/atlassian/jira-home/log/catalina.out` |
| Verify Agent | `ps aux \| grep javaagent` |
| Run Python Patch | `sudo python3 atlassian_patch.py` |
| Fix Permissions | `sudo python3 atlassian_patch.py --fix-permissions` |
| Generate License | `java -jar /opt/atlassian/jira/agent/atlassian-agent.jar -d -m email -n company -p jsm -o url -s server-id` |

</div>

---

## 📥 Download Links

<div dir="ltr">

| File | Description | Download Link |
|------|-------------|---------------|
| `atlassian-agent.jar` | Main agent file for license bypass | [Download](#) |
| `atlassian_patch.py` | Python patch script for verification and fixes | [Download](#) |

> **Note**: Replace the download links above with your actual file hosting locations.

</div>

---

<div dir="ltr">

**✅ Congratulations!** Your Jira is now activated with a valid license and ready to use. The Python patch script has verified that everything is configured correctly.

</div>
