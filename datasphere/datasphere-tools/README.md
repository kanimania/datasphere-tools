# datasphere-tools
Tools for working with datasphere
# Install Node.js
# Path Variable hinzufügen!
## Windows
Regedit --> Add following to Path value if portable version of node is installed
E.g.: C:\Users\JOHNDOE\node-v22.13.1-win-x64\

# Links
https://www.npmjs.com/package/@sap/datasphere-cli?activeTab=readme
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