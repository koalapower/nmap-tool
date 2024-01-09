# nmap-tool: tool for import asset from nmap report to KUMA
# Description
nmap-tool - tool for import asset from nmap report to KUMA. It supports import of ip, fqdn, mac addresses, OS, vulnerabilities, open ports.
For nmap-tool kumaPublicApiV1 is required: https://github.com/koalapower/kumaPublicApiV1

# Quick start
1. Donwload nmap-tool.py, params.json and kumaPublicApiV1 and place then in the same folder
2. Run nmap and save report into XML format
```
nmap -sS 10.0.0.1/24 -F -sV -O -oX scan.xml
```
3. Edit config file params.json
4. Run nmap-tool
```
python3 nmap-tool.py
```

# About params.json
1. kumaAddress - KUMA Core component address (may be FQDN or IP)
2. kumaAPIPort - KUMA REST API port (7223 by default)
3. tenantName - name of the tenant for import assets
4. useCustomFieldForPorts - true/false if you need to add information about open ports in asset struct (you should create custom field for ports manualy in KUMA web-interface)
5. useCustomFieldForScanner - true/false if you need to add information about scanner (nmap) in asset struct (you should create custom field for scanner manualy in KUMA web-interface)
6. settingsID - settings id from KUMA web-interface (Go to Settings -> Assets, press F12, choose Network then press Save under Asset settings. In Network you should see id of KUMA settings)
7. customFieldForPortsName - name of custom filed to store ports information (you should create custom field for ports manualy in KUMA web-interface)
8. customFieldForScannerName - name of custom filed to store scanner information (you should create custom field for scanner manualy in KUMA web-interface)
9. reportPath - path to nmap report

If you dont need custom fileds, set 4 and 5 parameter false and igonre parameters 6-8.
