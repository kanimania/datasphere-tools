# datasphere-tools
Tools for working with datasphere
# Install Pyton
https://www.python.org/downloads/

# Install Node.js
https://www.how2shout.com/how-to/how-to-install-node-js-and-npm-on-windows-10-or-11-using-cmd.html
https://nodejs.org/en/download --> Standalone Binary

# Install Datasphere CLI
https://www.npmjs.com/package/@sap/datasphere-cli?activeTab=readme
## Install / Update command
npm install -g @sap/datasphere-cli@latest
## Get Server Commands
datasphere config cache init -H https://*.sap/

# Install Git
https://git-scm.com/downloads/win
winget install --id Git.Git -e --source winget

# Path Variable hinzufügen!
e.g.: --> ;C:\Users\*\node-v22.13.1-win-x64\
## Windows
Regedit --> Add following to Path value if portable version of node is installed
E.g.: C:\Users\JOHNDOE\node-v22.13.1-win-x64\

# Links
https://help.sap.com/docs/SAP_DATASPHERE/d0ecd6f297ac40249072a44df0549c1a/3f9a42ccde6b4b6aba121e2aab79c36d.html?locale=en-US

# Datasphere Templates
Download Versions with design-time+json acceptance parameter --> Review
# Changing Objects
## Local Tables
1. Download definition
2. Default Acceptance Parameter (Select "None" using download script)
3. Change Json file and upload again
## Local Tables - Delta Enables
**Important**: Delta enabled Tables require changing the underlying Delta Tables for any changes!
1. Download definition of the underlying *_Delta Table!
2. Default Acceptance Parameter (Select "None" using download script)
3. Change Json file and upload again (E.g.: If local-table Name is "TABLE" you need to change "TABLE_Delta")