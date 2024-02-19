# nmap-tool: tool for import assets from nmap report to KUMA

English version below

## Описание

nmap-tool - скрипт для импорта информации об активах из отчета nmap в KUMA. Поддерживается импорт следующей информации: IP-адреса, FQDN, MAC-адреса, ОС, уязвимости, открытые порты.

## Требования

python 3.6+
- json
- xmltodict
- [kumaPublicApiV1](https://github.com/koalapower/kumaPublicApiV1)

## Быстрый старт
1. Скачайте nmap-tool.py, params.json и [kumaPublicApiV1](https://github.com/koalapower/kumaPublicApiV1) и поместите в одну папку на конечном устройстве
2. Запустите nmap и настройте вывод результатов сканирования в XML-файл
```
nmap -sS 10.0.0.1/24 -F -sV -O -oX scan.xml
```
3. Отредактируйте файл конфигурации params.json
4. Запустите nmap-tool
```
python3 nmap-tool.py
```

## О файле конфигурации params.json
1. `kumaAddress` - адрес сервера ядра KUMA
2. `kumaAPIPort` - API-порт сервера ядра KUMA (`7223` по умолчанию)
3. `kumaToken` - токен для доступа к API KUMA. Должны быть следующие права доступа: `GET /settings/id/:id`, `GET /tenants`, `POST /assets/import`.
5. `tenantName` - имя тенанта для импорта активов
6. `useCustomFieldForPorts` - `true`/`false` если планируется импорт информации об открытых портах в кастомные поля активов (вы должны заранее создать соответствующие поля в интерфейсе KUMA)
7. `useCustomFieldForScanner` - `true`/`false` если планируется импорт информации об имени сканера (nmap) в кастомное поле актива (вы должны заранее создать соответствующие поля в интерфейсе KUMA)
8. `settingsID` - id параметров из веб-интерфейса KUMA (В веб-интерфейсе зайдите Settings -> Assets, нажмите F12 для перехода в режим разработчика, выберите Network, после нажмите Сохранить внизу Asset settings. Во вкладке Network режима разработчика будет id параметров KUMA)
9. `customFieldForPortsName` - имя кастомного поля актива, куда будет записана информации об открытых портах (вы должны заранее создать соответствующие поля в интерфейсе KUMA)
10. `customFieldForScannerName` - имя кастомного поля актива, куда будет записана информация о сканере (вы должны заранее создать соответствующие поля в интерфейсе KUMA)
11. `reportPath` - полный путь к файлу отчета сканирования nmap

Если вы не планируете использовать кастомные поля, установите для параметров 4 и 5 значение false и игнорируйте параметры 6-8.

## Description
nmap-tool - tool for import asset from nmap report to KUMA. It supports import of ip, fqdn, mac addresses, OS, vulnerabilities, open ports.

## Requirements

python 3.6+
- json
- xmltodict
- [kumaPublicApiV1](https://github.com/koalapower/kumaPublicApiV1)

## Quick start
1. Download nmap-tool.py, params.json and [kumaPublicApiV1](https://github.com/koalapower/kumaPublicApiV1) and place them in the same folder
2. Run nmap and save report into XML format
```
nmap -sS 10.0.0.1/24 -F -sV -O -oX scan.xml
```
3. Edit config file params.json
4. Run nmap-tool
```
python3 nmap-tool.py
```

## About params.json
1. `kumaAddress` - KUMA Core component address (may be FQDN or IP)
2. `kumaAPIPort` - KUMA REST API port (`7223` by default)
3. `kumaToken` - KUMA API token with following API rights: `GET /settings/id/:id`, `GET /tenants`, `POST /assets/import`.
4. `tenantName` - name of the tenant for import assets
5. `useCustomFieldForPorts` - `true`/`false` if you need to add information about open ports in asset struct (you should create custom field for ports manualy in KUMA web-interface)
6. `useCustomFieldForScanner` - `true`/`false` if you need to add information about scanner (nmap) in asset struct (you should create custom field for scanner manualy in KUMA web-interface)
7. `settingsID` - settings id from KUMA web-interface (Go to Settings -> Assets, press F12, choose Network then press Save under Asset settings. In Network you should see id of KUMA settings)
8. `customFieldForPortsName` - name of custom filed to store ports information (you should create custom field for ports manualy in KUMA web-interface)
9. `customFieldForScannerName` - name of custom filed to store scanner information (you should create custom field for scanner manualy in KUMA web-interface)
10. `reportPath` - path to nmap report

If you dont need custom fields, set 4 and 5 parameter false and igonre parameters 6-8.
