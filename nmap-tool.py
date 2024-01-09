import xmltodict
import json
from kumaPublicApiV1 import Kuma


class Host:

    def __init__(self, host):

        self.host = host

        self.up = False
        if self.host['status']['@state'] == 'up':
            self.up = True

        # os version removed
        self.asset_struct = {
            "name": "",
            "fqdn": "",
            "ipAddresses": [],
            "macAddresses": [],
            "owner": "",
            "os": {
                "name": ""
            },
            "software": [],
            "vulnerabilities": [],
            "customFields": []
        }

        self.get_hostname()
        self.get_address()
        self.get_os()
        self.get_software()

    def get_address(self):
        if not self.up:
            return self.asset_struct
        if type(self.host['address']) is dict:
            address = self.host['address']
            if address['@addrtype'] in ('ipv4', 'ipv6'):
                self.asset_struct['ipAddresses'].append(address['@addr'])
            if address['@addrtype'] == 'mac':
                self.asset_struct['macAddresses'].append(address['@addr'])
            return self.asset_struct
        for address in self.host['address']:
            if address['@addrtype'] in ('ipv4', 'ipv6'):
                self.asset_struct['ipAddresses'].append(address['@addr'])
            if address['@addrtype'] == 'mac':
                self.asset_struct['macAddresses'].append(address['@addr'])
        return self.asset_struct

    def get_hostname(self):
        if not self.up:
            return self.asset_struct
        if type(self.host['hostnames']) is not type(None):
            self.asset_struct['fqdn'] = self.host['hostnames']['hostname']['@name']
        return self.asset_struct

    def get_os(self):
        if not self.up or type(self.host['os']) is type(None) or type(self.host['os'].get('osmatch')) is type(None):
            # removing os struct
            self.asset_struct.pop('os')
            return self.asset_struct
        if type(self.host['os']['osmatch']) is dict:
            self.asset_struct['os']['name'] = self.host['os']['osmatch']['@name']
        elif type(self.host['os']['osmatch']) is list:
            self.asset_struct['os']['name'] = self.host['os']['osmatch'][0]['@name']
        return self.asset_struct

    def get_software(self):
        if not self.up or type(self.host.get('ports')) is type(None) or type(self.host['ports'].get('port')) is type(None):
            return self.asset_struct
        if type(self.host['ports']['port']) is dict:
            port = self.host['ports']['port']
            soft = {"name": "", "version": ""}
            if type(port['service'].get('@product')) is type(None):
                return self.asset_struct
            soft['name'] = port['service']['@product']
            if type(port['service'].get('@version')) is not type(None):
                soft['version'] = port['service']['@version']
            self.asset_struct['software'].append(soft)
            return self.asset_struct
        for port in self.host['ports']['port']:
            soft = {"name": "", "version": ""}
            if type(port['service'].get('@product')) is type(None):
                continue
            soft['name'] = port['service']['@product']
            if type(port['service'].get('@version')) is not type(None):
                soft['version'] = port['service']['@version']
            self.asset_struct['software'].append(soft)
        # deduplicate software
        self.asset_struct['software'] = [dict(t) for t in {tuple(d.items()) for d in self.asset_struct['software']}]
        return self.asset_struct

    def get_ports(self, ports_filed_name, ports_field_id):
        ports_list = []
        if not self.up or type(self.host.get('ports')) is type(None) or type(self.host['ports'].get('port')) is type(None):
            return self.asset_struct
        if type(self.host['ports']['port']) is dict:
            port = self.host['ports']['port']
            ports_list.append(f"{port['@portid']}/{port['@protocol']}({port['state']['@state']})")
            self.asset_struct['customFields'].append({
                "id": ports_field_id,
                "name": ports_filed_name,
                "value": ', '.join(ports_list)
            })
            return self.asset_struct
        for port in self.host['ports']['port']:
            ports_list.append(f"{port['@portid']}/{port['@protocol']}({port['state']['@state']})")
        self.asset_struct['customFields'].append({
            "id": ports_field_id,
            "name": ports_filed_name,
            "value": ', '.join(ports_list)
        })
        return self.asset_struct

    def set_scanner(self, scanner_field_name, scanner_field_id):
        scanner_field = {
            "id": scanner_field_id,
            "name": scanner_field_name,
            "value": "nmap"
        }
        self.asset_struct['customFields'].append(scanner_field)
        return self.asset_struct


def main():
    with open('params.json') as param_file:
        params = json.load(param_file)

    NewKuma = Kuma(params['kumaAddress'], params['kumaAPIPort'], params['kumaToken'])

    tenants = NewKuma.get_tenant_by_name(params['tenantName'])

    if len(tenants) != 0:
        params['tenantID'] = tenants[0]['id']
    else:
        raise Exception(f"Tenant with name {params['tenantName']} not found")

    if params['useCustomFieldForPorts'] or params['useCustomFieldForScanner']:
        custom_fields = NewKuma.get_asset_custom_fields(params['settingsID'])
        for custom_field in custom_fields['customFields']:
            if custom_field['name'] == params['customFieldForPortsName'] and params['useCustomFieldForPorts']:
                params['customFieldForPortsID'] = custom_field['id']
            if custom_field['name'] == params['customFieldForScannerName'] and params['useCustomFieldForScanner']:
                params['customFieldForScannerID'] = custom_field['id']

    report_path = params['reportPath']

    with open(report_path) as xml_file:
        report_dict = xmltodict.parse(xml_file.read())

    hosts = report_dict['nmaprun']['host']

    for host in hosts:
        NewHost = Host(host)
        if NewHost.asset_struct['fqdn'] != '' or NewHost.asset_struct['ipAddresses'] != []:
            if params['useCustomFieldForPorts']:
                NewHost.get_ports(params['customFieldForPortsName'], params['customFieldForPortsID'])
            if params['useCustomFieldForScanner']:
                NewHost.set_scanner(params['customFieldForScannerName'], params['customFieldForScannerID'])
            NewKuma.import_assets(params['tenantID'], [NewHost.asset_struct])


if __name__ == "__main__":
    main()