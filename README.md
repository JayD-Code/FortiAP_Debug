This script helps to check for kernel panic or crash on connected FortiAPs

User need to provide Fortigate IP and password for ssh. Code will SSH to Fortigate and collect details of all connected APs. Then it will SSH to each AP and checks for crash or kernel panics. If crash exists then it will provide info of AP's SN and build.

Requirement:
    All connected APs must have same password.
    FGT should be able to SSH connected APs.
    Requires Paramiko module http://www.paramiko.org/
