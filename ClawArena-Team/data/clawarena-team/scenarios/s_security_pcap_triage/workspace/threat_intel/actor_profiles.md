# Threat Actor Profile: Cozy Bear (APT29)

**Motivation**: nation-state espionage
**Primary techniques**: spearphishing, credential harvesting

## Observed TTPs

- `T1044.004` — Living-off-the-land via certutil
- `T1459.007` — Command and control via HTTPS on port 443
- `T1460.000` — Use of PowerShell for lateral movement
- `T1070.002` — Living-off-the-land via certutil
- `T1410.009` — DLL side-loading via signed binary
- `T1394.000` — Spearphishing attachment with macro
- `T1621.004` — Spearphishing attachment with macro
- `T1097.001` — Living-off-the-land via certutil
- `T1267.002` — C2 beacon to port 5344
- `T1624.006` — DLL side-loading via signed binary
- `T1084.002` — Valid accounts — compromised credentials
- `T1247.004` — Living-off-the-land via certutil
- `T1548.009` — WMI event subscription for persistence
- `T1442.003` — Command and control via HTTPS on port 443
- `T1183.004` — Network share discovery via net view
- `T1222.006` — Spearphishing attachment with macro
- `T1694.001` — Registry run key persistence
- `T1102.008` — Registry run key persistence
- `T1001.008` — Scheduled task persistence mechanism
- `T1454.007` — Network share discovery via net view
- `T1559.005` — Scheduled task persistence mechanism
- `T1292.006` — Valid accounts — compromised credentials
- `T1385.005` — Valid accounts — compromised credentials
- `T1658.003` — Use of PowerShell for lateral movement
- `T1498.009` — DLL side-loading via signed binary
- `T1115.004` — Credential dumping via LSASS memory access
- `T1066.009` — DLL side-loading via signed binary
- `T1352.009` — Registry run key persistence
- `T1477.007` — Living-off-the-land via certutil
- `T1232.004` — WMI event subscription for persistence
- `T1089.001` — Credential dumping via LSASS memory access
- `T1134.009` — Credential dumping via LSASS memory access
- `T1463.003` — Use of PowerShell for lateral movement
- `T1560.007` — Credential dumping via LSASS memory access
- `T1628.009` — Registry run key persistence
- `T1340.009` — DLL side-loading via signed binary
- `T1329.009` — Spearphishing attachment with macro
- `T1398.005` — Spearphishing attachment with macro
- `T1125.006` — WMI event subscription for persistence
- `T1416.005` — Exfil to 64.138.229.223 via DNS tunneling
- `T1022.004` — Data staged to temp directory prior to exfil
- `T1170.000` — Command and control via HTTPS on port 443
- `T1223.005` — Registry run key persistence
- `T1698.007` — Scheduled task persistence mechanism
- `T1661.009` — Scheduled task persistence mechanism
- `T1032.009` — Use of PowerShell for lateral movement
- `T1613.009` — Exfil to 26.28.150.26 via DNS tunneling
- `T1084.005` — Command and control via HTTPS on port 443
- `T1643.000` — Scheduled task persistence mechanism
- `T1248.003` — Network share discovery via net view
- `T1422.005` — Command and control via HTTPS on port 443
- `T1674.002` — Registry run key persistence
- `T1122.006` — Exfil to 157.102.7.142 via DNS tunneling
- `T1384.003` — Network share discovery via net view
- `T1678.004` — Valid accounts — compromised credentials
- `T1348.001` — Data staged to temp directory prior to exfil
- `T1137.009` — Network share discovery via net view
- `T1259.009` — Registry run key persistence
- `T1503.004` — Credential dumping via LSASS memory access
- `T1302.001` — Valid accounts — compromised credentials
- `T1182.009` — Spearphishing attachment with macro
- `T1321.000` — C2 beacon to port 50658
- `T1387.006` — Valid accounts — compromised credentials
- `T1561.001` — DLL side-loading via signed binary
- `T1198.003` — Living-off-the-land via certutil
- `T1252.001` — Use of PowerShell for lateral movement
- `T1140.000` — Data staged to temp directory prior to exfil
- `T1691.000` — Data staged to temp directory prior to exfil
- `T1666.002` — Data staged to temp directory prior to exfil
- `T1176.008` — C2 beacon to port 25851
- `T1284.009` — Network share discovery via net view
- `T1699.000` — WMI event subscription for persistence
- `T1647.000` — Use of PowerShell for lateral movement
- `T1065.002` — Network share discovery via net view
- `T1096.007` — Valid accounts — compromised credentials
- `T1629.003` — Data staged to temp directory prior to exfil
- `T1283.006` — Use of PowerShell for lateral movement
- `T1406.003` — Scheduled task persistence mechanism
- `T1360.004` — Scheduled task persistence mechanism
- `T1186.007` — Network share discovery via net view
- `T1448.005` — DLL side-loading via signed binary
- `T1325.009` — Valid accounts — compromised credentials
- `T1319.006` — Living-off-the-land via certutil
- `T1517.000` — DLL side-loading via signed binary
- `T1409.007` — Valid accounts — compromised credentials
- `T1435.006` — Living-off-the-land via certutil
- `T1680.009` — Data staged to temp directory prior to exfil
- `T1091.005` — Valid accounts — compromised credentials
- `T1415.008` — Credential dumping via LSASS memory access
- `T1321.006` — DLL side-loading via signed binary
- `T1550.008` — Network share discovery via net view
- `T1161.000` — Network share discovery via net view
- `T1395.005` — Data staged to temp directory prior to exfil
- `T1075.006` — WMI event subscription for persistence
- `T1128.003` — DLL side-loading via signed binary
- `T1124.005` — Registry run key persistence
- `T1080.002` — DLL side-loading via signed binary
- `T1002.008` — Exfil to 103.226.230.22 via DNS tunneling
- `T1091.000` — C2 beacon to port 49816
- `T1042.001` — Data staged to temp directory prior to exfil
- `T1539.000` — Spearphishing attachment with macro
- `T1023.008` — Living-off-the-land via certutil
- `T1136.002` — WMI event subscription for persistence
- `T1388.004` — Living-off-the-land via certutil
- `T1572.005` — DLL side-loading via signed binary
- `T1295.000` — Registry run key persistence
- `T1585.005` — Network share discovery via net view
- `T1574.005` — DLL side-loading via signed binary
- `T1518.007` — Data staged to temp directory prior to exfil
- `T1127.007` — C2 beacon to port 53247
- `T1352.004` — Use of PowerShell for lateral movement
- `T1017.001` — DLL side-loading via signed binary
- `T1152.007` — Living-off-the-land via certutil
- `T1418.003` — Use of PowerShell for lateral movement
- `T1629.007` — C2 beacon to port 55876
- `T1293.007` — Scheduled task persistence mechanism
- `T1242.004` — Exfil to 208.41.242.88 via DNS tunneling
- `T1660.000` — WMI event subscription for persistence
- `T1237.005` — DLL side-loading via signed binary
- `T1639.006` — Data staged to temp directory prior to exfil
- `T1580.001` — Registry run key persistence
- `T1237.004` — DLL side-loading via signed binary
- `T1457.006` — Network share discovery via net view
- `T1145.008` — DLL side-loading via signed binary
- `T1269.006` — WMI event subscription for persistence
- `T1632.000` — Spearphishing attachment with macro
- `T1681.007` — Exfil to 162.168.110.186 via DNS tunneling
- `T1699.007` — C2 beacon to port 4291
- `T1330.004` — Use of PowerShell for lateral movement
- `T1582.008` — Data staged to temp directory prior to exfil
- `T1316.008` — Scheduled task persistence mechanism
- `T1278.009` — Use of PowerShell for lateral movement
- `T1168.004` — Data staged to temp directory prior to exfil
- `T1019.006` — C2 beacon to port 26084
- `T1101.002` — Living-off-the-land via certutil
- `T1171.003` — Exfil to 91.111.253.160 via DNS tunneling
- `T1435.004` — Spearphishing attachment with macro
- `T1001.001` — DLL side-loading via signed binary
- `T1340.008` — C2 beacon to port 36594
- `T1218.004` — Scheduled task persistence mechanism
- `T1548.006` — Scheduled task persistence mechanism
- `T1380.008` — Living-off-the-land via certutil
- `T1178.000` — Data staged to temp directory prior to exfil
- `T1421.000` — Use of PowerShell for lateral movement
- `T1218.002` — Living-off-the-land via certutil
- `T1003.007` — Valid accounts — compromised credentials
- `T1651.009` — Living-off-the-land via certutil
- `T1002.006` — DLL side-loading via signed binary
- `T1023.006` — WMI event subscription for persistence
- `T1073.004` — Living-off-the-land via certutil
- `T1522.000` — C2 beacon to port 52302
- `T1160.008` — Spearphishing attachment with macro
- `T1036.002` — Use of PowerShell for lateral movement
- `T1432.009` — Registry run key persistence
- `T1148.004` — Use of PowerShell for lateral movement
- `T1380.009` — Exfil to 64.11.40.154 via DNS tunneling
- `T1005.009` — Spearphishing attachment with macro
- `T1640.001` — Credential dumping via LSASS memory access
- `T1623.001` — Use of PowerShell for lateral movement
- `T1127.009` — Credential dumping via LSASS memory access
- `T1672.001` — Network share discovery via net view
- `T1452.009` — Living-off-the-land via certutil
- `T1163.000` — DLL side-loading via signed binary
- `T1573.009` — Exfil to 115.57.8.68 via DNS tunneling
- `T1593.009` — Registry run key persistence
- `T1667.007` — Command and control via HTTPS on port 443
- `T1118.002` — WMI event subscription for persistence
- `T1216.003` — Exfil to 3.59.255.218 via DNS tunneling
- `T1009.000` — C2 beacon to port 58012
- `T1530.002` — WMI event subscription for persistence
- `T1596.009` — Valid accounts — compromised credentials
- `T1187.000` — Spearphishing attachment with macro
- `T1443.003` — Scheduled task persistence mechanism
- `T1623.003` — WMI event subscription for persistence
- `T1257.000` — Credential dumping via LSASS memory access
- `T1255.009` — Data staged to temp directory prior to exfil
- `T1015.005` — Scheduled task persistence mechanism
- `T1499.003` — Credential dumping via LSASS memory access
- `T1307.001` — Scheduled task persistence mechanism
- `T1277.001` — Command and control via HTTPS on port 443

## Indicators of Compromise

| Type | Value | Confidence |
|------|-------|------------|
| IP | `188.142.173.195` | MEDIUM |
| Domain | `cdn87-update.nfjeab.com` | HIGH |
| Domain | `cdn2-update.fffbni.com` | LOW |
| Domain | `cdn42-update.jkjmcb.com` | HIGH |
| SHA256 | `8cf8b160abcbaa76974f3c95a3eaeb44154c57cc22ffecc329ec8124f2872231` | HIGH |
| URL | `http://95.47.67.28/payload.php` | LOW |
| IP | `61.166.150.61` | MEDIUM |
| Domain | `cdn39-update.lgjokm.com` | HIGH |
| Domain | `cdn70-update.ejicnb.com` | LOW |
| URL | `http://81.97.143.21/payload.php` | LOW |
| URL | `http://106.141.119.234/payload.php` | HIGH |
| SHA256 | `208f8e779b7ff6a341bd3e244eac1e41fd33b4c4f52c124015bd783447fef27d` | HIGH |
| Domain | `cdn36-update.cdicpn.com` | LOW |
| Domain | `cdn71-update.naacip.com` | HIGH |
| SHA256 | `4e9039fcca44bd2dad42ad15933106f54b1f86a7a630b7c3aafb824ef18547a0` | HIGH |
| SHA256 | `8dd92d6fa14098ed9677295493ffa6171759b460547cc610f679ac4ef31471f5` | HIGH |
| IP | `85.132.60.139` | LOW |
| IP | `142.16.44.12` | MEDIUM |
| SHA256 | `39054272dd769c439b55d4e70e31de9d3918c0407615839f37e04bf5a108f1f5` | LOW |
| SHA256 | `578bf0cca6005b389b221101e4421967cb57b127a2d67e91257e24c2c56af58a` | HIGH |
| URL | `http://69.64.12.228/payload.php` | MEDIUM |
| URL | `http://177.74.241.169/payload.php` | MEDIUM |
| Domain | `cdn97-update.bbfeko.com` | HIGH |
| URL | `http://43.167.129.1/payload.php` | MEDIUM |
| URL | `http://148.224.7.30/payload.php` | LOW |
| SHA256 | `a9718f1cddd42ea7a3bcb144946d17206afd07320fe6b0037574ee849883cc44` | HIGH |
| IP | `145.215.38.173` | MEDIUM |
| URL | `http://204.174.113.245/payload.php` | HIGH |
| IP | `120.196.49.154` | MEDIUM |
| URL | `http://135.103.79.83/payload.php` | MEDIUM |
| SHA256 | `b4eb8a3fe7990b707511da74d83daea7b4948bc41d885865a5e820c7e5cf49e0` | LOW |
| SHA256 | `b1c6d95933d828cc8d0d55fcb085cc30567b4c98ea06cc472eb18f345c9f3cfa` | LOW |
| Domain | `cdn17-update.gcjmdd.com` | MEDIUM |
| SHA256 | `7a7b4012c53998d965472307cc7678525a9da9c7011684c2b469541684b0e672` | MEDIUM |
| IP | `197.118.41.57` | LOW |
| SHA256 | `c7a4cb1379da8f1059234d5ec04e1c471deb9824e5ebd2eef7d83dde2c2a9818` | LOW |
| SHA256 | `c3c18422f4f9a05cafa1077c7e5edce85a7523f829190b3b21e7d84f7adba0fc` | LOW |
| SHA256 | `d76d89245880e98563b3b46e4d6af345573a01e42dbfb62aa56a5dba3ff9196e` | MEDIUM |
| IP | `182.101.113.55` | MEDIUM |
| IP | `222.76.12.107` | LOW |
| SHA256 | `143dac15a2b4b7aa7eb0a2df3f20dbbaf4c953aad1d888734ae22d0d41d6b6ae` | HIGH |
| IP | `145.188.184.44` | MEDIUM |
| IP | `158.191.137.116` | LOW |
| URL | `http://124.244.235.213/payload.php` | HIGH |
| Domain | `cdn17-update.bmpgib.com` | HIGH |
| URL | `http://218.89.21.222/payload.php` | MEDIUM |
| IP | `81.12.86.30` | HIGH |
| SHA256 | `4e7b8494c2eb70b98ace8f3f8c5ccbb50c8a69dd8a6c1248bf67ec7dedce5a8f` | HIGH |
| Domain | `cdn29-update.cffkpn.com` | LOW |
| URL | `http://171.103.173.234/payload.php` | HIGH |
| URL | `http://82.5.69.38/payload.php` | LOW |
| SHA256 | `263a3c4e2c5e3665ede8f156788c4a38ce6848f6e45e8c200aea797aa50c38a5` | LOW |
| SHA256 | `6196df9f265308f1e014f624f21d83511025affba28c7d198f5577c6e7851525` | MEDIUM |
| URL | `http://13.109.53.160/payload.php` | MEDIUM |
| IP | `52.219.25.6` | MEDIUM |
| IP | `214.219.223.121` | MEDIUM |
| IP | `69.159.9.84` | HIGH |
| URL | `http://77.145.166.149/payload.php` | MEDIUM |
| IP | `65.130.37.170` | LOW |
| URL | `http://157.217.144.92/payload.php` | HIGH |


---

# Threat Actor Profile: Lazarus Group (APT38)

**Motivation**: financial theft
**Primary techniques**: watering hole, supply chain compromise

## Observed TTPs

- `T1104.002` — Spearphishing attachment with macro
- `T1246.000` — Spearphishing attachment with macro
- `T1632.008` — Exfil to 98.124.159.135 via DNS tunneling
- `T1453.006` — Valid accounts — compromised credentials
- `T1120.001` — Network share discovery via net view
- `T1063.007` — Valid accounts — compromised credentials
- `T1439.003` — Spearphishing attachment with macro
- `T1043.006` — Exfil to 174.70.200.198 via DNS tunneling
- `T1255.001` — Command and control via HTTPS on port 443
- `T1371.005` — Data staged to temp directory prior to exfil
- `T1514.000` — WMI event subscription for persistence
- `T1244.001` — Network share discovery via net view
- `T1553.009` — DLL side-loading via signed binary
- `T1450.002` — Scheduled task persistence mechanism
- `T1586.006` — Credential dumping via LSASS memory access
- `T1398.009` — C2 beacon to port 58926
- `T1038.007` — Valid accounts — compromised credentials
- `T1140.000` — DLL side-loading via signed binary
- `T1494.004` — Living-off-the-land via certutil
- `T1319.007` — WMI event subscription for persistence
- `T1582.002` — Command and control via HTTPS on port 443
- `T1546.007` — WMI event subscription for persistence
- `T1343.003` — WMI event subscription for persistence
- `T1459.000` — Registry run key persistence
- `T1192.005` — Network share discovery via net view
- `T1566.000` — Credential dumping via LSASS memory access
- `T1689.000` — Data staged to temp directory prior to exfil
- `T1354.009` — Spearphishing attachment with macro
- `T1078.000` — Valid accounts — compromised credentials
- `T1473.008` — Scheduled task persistence mechanism
- `T1123.003` — Credential dumping via LSASS memory access
- `T1303.005` — Registry run key persistence
- `T1445.009` — Registry run key persistence
- `T1346.001` — Data staged to temp directory prior to exfil
- `T1212.005` — WMI event subscription for persistence
- `T1351.000` — C2 beacon to port 48829
- `T1300.008` — Exfil to 113.52.40.145 via DNS tunneling
- `T1132.003` — Scheduled task persistence mechanism
- `T1412.007` — Registry run key persistence
- `T1085.000` — Spearphishing attachment with macro
- `T1493.008` — Spearphishing attachment with macro
- `T1315.002` — C2 beacon to port 56437
- `T1513.004` — Data staged to temp directory prior to exfil
- `T1663.001` — Spearphishing attachment with macro
- `T1063.002` — Living-off-the-land via certutil
- `T1157.004` — Exfil to 128.11.108.8 via DNS tunneling
- `T1662.008` — Exfil to 57.62.159.248 via DNS tunneling
- `T1687.006` — WMI event subscription for persistence
- `T1390.006` — Use of PowerShell for lateral movement
- `T1106.006` — Living-off-the-land via certutil
- `T1275.002` — C2 beacon to port 53552
- `T1235.002` — Exfil to 172.42.243.112 via DNS tunneling
- `T1535.009` — Registry run key persistence
- `T1472.007` — Exfil to 66.90.70.52 via DNS tunneling
- `T1193.009` — Registry run key persistence
- `T1455.007` — Command and control via HTTPS on port 443
- `T1176.001` — DLL side-loading via signed binary
- `T1111.000` — Scheduled task persistence mechanism
- `T1043.002` — Credential dumping via LSASS memory access
- `T1113.005` — Credential dumping via LSASS memory access
- `T1669.000` — Credential dumping via LSASS memory access
- `T1630.004` — C2 beacon to port 45911
- `T1425.001` — Data staged to temp directory prior to exfil
- `T1450.000` — Valid accounts — compromised credentials
- `T1526.009` — Living-off-the-land via certutil
- `T1170.006` — Credential dumping via LSASS memory access
- `T1433.009` — Living-off-the-land via certutil
- `T1612.000` — Data staged to temp directory prior to exfil
- `T1049.008` — Exfil to 169.76.114.243 via DNS tunneling
- `T1129.003` — Registry run key persistence
- `T1178.008` — Registry run key persistence
- `T1561.009` — Use of PowerShell for lateral movement
- `T1629.006` — Exfil to 76.50.117.150 via DNS tunneling
- `T1682.008` — Living-off-the-land via certutil
- `T1700.006` — Scheduled task persistence mechanism
- `T1248.008` — Valid accounts — compromised credentials
- `T1170.003` — Spearphishing attachment with macro
- `T1101.001` — Living-off-the-land via certutil
- `T1649.007` — Exfil to 85.120.114.113 via DNS tunneling
- `T1510.005` — Network share discovery via net view
- `T1334.009` — Command and control via HTTPS on port 443
- `T1206.001` — WMI event subscription for persistence
- `T1491.003` — WMI event subscription for persistence
- `T1573.001` — Valid accounts — compromised credentials
- `T1253.001` — Living-off-the-land via certutil
- `T1233.009` — Data staged to temp directory prior to exfil
- `T1299.005` — DLL side-loading via signed binary
- `T1209.006` — Credential dumping via LSASS memory access
- `T1503.008` — Registry run key persistence
- `T1093.008` — Command and control via HTTPS on port 443
- `T1319.004` — Command and control via HTTPS on port 443
- `T1148.000` — Registry run key persistence
- `T1148.007` — Use of PowerShell for lateral movement
- `T1281.008` — Network share discovery via net view
- `T1422.001` — Spearphishing attachment with macro
- `T1363.000` — Valid accounts — compromised credentials
- `T1486.006` — Living-off-the-land via certutil
- `T1005.009` — Scheduled task persistence mechanism
- `T1117.009` — WMI event subscription for persistence
- `T1002.001` — Registry run key persistence
- `T1215.009` — Exfil to 120.212.183.191 via DNS tunneling
- `T1037.000` — Data staged to temp directory prior to exfil
- `T1309.002` — Command and control via HTTPS on port 443
- `T1310.004` — Credential dumping via LSASS memory access
- `T1146.003` — Credential dumping via LSASS memory access
- `T1623.001` — Living-off-the-land via certutil
- `T1079.001` — Registry run key persistence
- `T1612.000` — Spearphishing attachment with macro
- `T1171.006` — Data staged to temp directory prior to exfil
- `T1578.006` — Network share discovery via net view
- `T1659.000` — Registry run key persistence
- `T1393.004` — DLL side-loading via signed binary
- `T1180.007` — DLL side-loading via signed binary
- `T1092.005` — Command and control via HTTPS on port 443
- `T1206.002` — Spearphishing attachment with macro
- `T1072.003` — Command and control via HTTPS on port 443
- `T1184.004` — Registry run key persistence
- `T1200.006` — Network share discovery via net view
- `T1042.006` — C2 beacon to port 65174
- `T1138.004` — Exfil to 37.138.172.75 via DNS tunneling
- `T1432.004` — Credential dumping via LSASS memory access
- `T1057.003` — Use of PowerShell for lateral movement
- `T1238.007` — Spearphishing attachment with macro
- `T1659.006` — Data staged to temp directory prior to exfil
- `T1446.004` — Valid accounts — compromised credentials
- `T1286.007` — Use of PowerShell for lateral movement
- `T1600.002` — WMI event subscription for persistence
- `T1651.005` — Network share discovery via net view
- `T1290.005` — Command and control via HTTPS on port 443
- `T1357.005` — Scheduled task persistence mechanism
- `T1499.001` — Command and control via HTTPS on port 443
- `T1475.003` — Command and control via HTTPS on port 443
- `T1526.000` — Valid accounts — compromised credentials
- `T1403.007` — Use of PowerShell for lateral movement
- `T1545.000` — Exfil to 207.32.96.75 via DNS tunneling
- `T1222.005` — DLL side-loading via signed binary
- `T1373.003` — Scheduled task persistence mechanism
- `T1633.004` — Scheduled task persistence mechanism
- `T1527.004` — Use of PowerShell for lateral movement
- `T1123.007` — Use of PowerShell for lateral movement
- `T1204.009` — Network share discovery via net view
- `T1636.005` — Living-off-the-land via certutil
- `T1699.005` — Valid accounts — compromised credentials
- `T1306.008` — Scheduled task persistence mechanism
- `T1570.009` — C2 beacon to port 59231
- `T1429.001` — WMI event subscription for persistence
- `T1276.004` — Spearphishing attachment with macro
- `T1203.003` — WMI event subscription for persistence
- `T1486.002` — DLL side-loading via signed binary
- `T1077.002` — Valid accounts — compromised credentials
- `T1078.008` — Use of PowerShell for lateral movement
- `T1148.006` — Credential dumping via LSASS memory access
- `T1192.004` — Data staged to temp directory prior to exfil
- `T1607.006` — Living-off-the-land via certutil
- `T1313.003` — Command and control via HTTPS on port 443
- `T1318.005` — Credential dumping via LSASS memory access
- `T1698.008` — WMI event subscription for persistence
- `T1159.002` — Credential dumping via LSASS memory access
- `T1092.005` — Scheduled task persistence mechanism
- `T1675.003` — Registry run key persistence
- `T1566.006` — Command and control via HTTPS on port 443
- `T1611.005` — Use of PowerShell for lateral movement
- `T1320.009` — WMI event subscription for persistence
- `T1279.006` — Network share discovery via net view
- `T1504.000` — Data staged to temp directory prior to exfil
- `T1431.007` — Network share discovery via net view
- `T1256.007` — WMI event subscription for persistence
- `T1521.004` — Living-off-the-land via certutil
- `T1017.007` — Valid accounts — compromised credentials
- `T1479.009` — Living-off-the-land via certutil
- `T1468.001` — Registry run key persistence
- `T1238.008` — Credential dumping via LSASS memory access
- `T1435.004` — Credential dumping via LSASS memory access
- `T1008.003` — Use of PowerShell for lateral movement
- `T1232.007` — Living-off-the-land via certutil
- `T1494.000` — WMI event subscription for persistence
- `T1196.000` — Data staged to temp directory prior to exfil
- `T1337.006` — Exfil to 209.37.203.85 via DNS tunneling
- `T1671.007` — Valid accounts — compromised credentials
- `T1612.001` — Spearphishing attachment with macro

## Indicators of Compromise

| Type | Value | Confidence |
|------|-------|------------|
| IP | `3.55.245.205` | MEDIUM |
| URL | `http://154.204.24.167/payload.php` | LOW |
| Domain | `cdn58-update.acmcic.com` | HIGH |
| Domain | `cdn11-update.ogjhjk.com` | HIGH |
| URL | `http://55.25.19.216/payload.php` | LOW |
| IP | `159.61.34.35` | LOW |
| URL | `http://187.113.0.155/payload.php` | MEDIUM |
| IP | `140.38.225.123` | HIGH |
| URL | `http://58.245.207.174/payload.php` | LOW |
| URL | `http://145.174.90.227/payload.php` | MEDIUM |
| IP | `112.6.119.89` | LOW |
| Domain | `cdn21-update.omeoak.com` | MEDIUM |
| Domain | `cdn70-update.gijegd.com` | HIGH |
| Domain | `cdn12-update.hjkkbg.com` | HIGH |
| IP | `130.253.134.162` | LOW |
| Domain | `cdn58-update.llcahl.com` | MEDIUM |
| SHA256 | `9fc70622b52277de386f7314100197d9959f2e029e6b123b9d07e380936b3836` | HIGH |
| SHA256 | `81675fcfade5a5c9c38a03a8a53e3f3ef2b072a9da06ce06888720839973c7ae` | MEDIUM |
| URL | `http://109.22.42.52/payload.php` | HIGH |
| IP | `145.70.133.25` | HIGH |
| SHA256 | `1847f2e71140478184d9774f59217a02793cd66251c5414b5e63be4729208755` | HIGH |
| Domain | `cdn74-update.nneegp.com` | LOW |
| SHA256 | `1c2f3310488e17bb95d22bec3787152a2e93da24bd37c1afe89ac645b0a64430` | LOW |
| Domain | `cdn41-update.gonppo.com` | HIGH |
| Domain | `cdn12-update.iiajgi.com` | LOW |
| IP | `30.56.146.109` | LOW |
| SHA256 | `85f2ed2549dae5a29e83b174df864dcf98b63a853121570801e1145a7b526699` | LOW |
| URL | `http://159.230.112.153/payload.php` | MEDIUM |
| IP | `119.237.223.54` | HIGH |
| SHA256 | `30f3b0e923a45950e7a86572effd3669139b95443295773aa6a217617a1ad48e` | HIGH |
| Domain | `cdn98-update.hkdmhh.com` | LOW |
| Domain | `cdn4-update.fbpcni.com` | HIGH |
| Domain | `cdn84-update.bekiof.com` | LOW |
| SHA256 | `64da9a7ade9a6d00bd738dc5632a369ff2fd4c53250d2b0bb0563562121373c9` | LOW |
| SHA256 | `026dc7d5da2176978a0d718fa309e79120a8d43021e1ef93dd0939d04694b7cf` | HIGH |
| SHA256 | `063825195c52783959d351d868d440b1d2a80918cb5507475becba2838f2ba66` | MEDIUM |
| URL | `http://41.219.251.152/payload.php` | MEDIUM |
| IP | `75.97.161.154` | MEDIUM |
| URL | `http://193.179.158.164/payload.php` | HIGH |
| URL | `http://85.215.66.23/payload.php` | HIGH |
| SHA256 | `e5e0a33184f12f74dc4d533fba28008b19401230de7057ccf2b4c91744715282` | LOW |
| URL | `http://67.76.151.223/payload.php` | LOW |
| IP | `78.203.36.52` | MEDIUM |
| URL | `http://6.151.18.158/payload.php` | MEDIUM |
| SHA256 | `f63d870cde85f811062273929fb4e24f5cefdf23f8a76eb8106290d1ed5d7f11` | MEDIUM |
| IP | `13.124.145.61` | LOW |
| IP | `15.180.249.64` | MEDIUM |
| URL | `http://28.135.131.252/payload.php` | HIGH |
| IP | `218.157.156.246` | HIGH |
| Domain | `cdn92-update.jdefae.com` | LOW |
| SHA256 | `19505524eeece2fe38b93984d9228a6cff963b02a40b3ae12f728148cafaa8e1` | LOW |
| URL | `http://116.26.75.103/payload.php` | HIGH |
| IP | `157.61.15.232` | MEDIUM |
| SHA256 | `a593bd95435ef8a26f7d1e58b7029e3ca18bea19d59032fa1a0197b610e9ae36` | MEDIUM |
| SHA256 | `60529122794872f88db92e54a5c5e5994623a2ce06d702c214f8d9458daf6484` | HIGH |
| IP | `76.172.209.100` | MEDIUM |
| SHA256 | `80f5d7d1ecdfb0f45c340f4daa1231fecbceac94a3a21c8b45e02392f27f4b26` | MEDIUM |
| IP | `199.133.233.6` | LOW |
| SHA256 | `298714ea97be32d7f8525d4e578e6bd75332f013e2c6ab8acb8325afa94df996` | HIGH |
| URL | `http://179.229.176.106/payload.php` | HIGH |


---

# Threat Actor Profile: FIN7 (CARBON SPIDER)

**Motivation**: point-of-sale intrusion
**Primary techniques**: spearphishing, Carbanak malware

## Observed TTPs

- `T1106.007` — Command and control via HTTPS on port 443
- `T1134.004` — WMI event subscription for persistence
- `T1261.002` — Spearphishing attachment with macro
- `T1660.007` — Network share discovery via net view
- `T1637.002` — Living-off-the-land via certutil
- `T1624.005` — Spearphishing attachment with macro
- `T1614.006` — Living-off-the-land via certutil
- `T1459.001` — Use of PowerShell for lateral movement
- `T1526.005` — Registry run key persistence
- `T1211.002` — Spearphishing attachment with macro
- `T1224.009` — Spearphishing attachment with macro
- `T1695.001` — Network share discovery via net view
- `T1009.003` — Spearphishing attachment with macro
- `T1038.007` — Scheduled task persistence mechanism
- `T1482.009` — Use of PowerShell for lateral movement
- `T1209.004` — Command and control via HTTPS on port 443
- `T1368.006` — C2 beacon to port 29838
- `T1196.006` — Use of PowerShell for lateral movement
- `T1113.008` — Command and control via HTTPS on port 443
- `T1267.007` — C2 beacon to port 39614
- `T1346.004` — Exfil to 18.227.216.75 via DNS tunneling
- `T1021.007` — Network share discovery via net view
- `T1333.004` — Spearphishing attachment with macro
- `T1239.007` — Exfil to 11.84.18.37 via DNS tunneling
- `T1256.007` — Network share discovery via net view
- `T1398.006` — Data staged to temp directory prior to exfil
- `T1672.005` — Credential dumping via LSASS memory access
- `T1296.006` — DLL side-loading via signed binary
- `T1653.000` — Data staged to temp directory prior to exfil
- `T1128.001` — C2 beacon to port 58912
- `T1379.002` — Spearphishing attachment with macro
- `T1406.000` — Living-off-the-land via certutil
- `T1573.004` — Valid accounts — compromised credentials
- `T1251.006` — Living-off-the-land via certutil
- `T1304.001` — Data staged to temp directory prior to exfil
- `T1028.007` — Registry run key persistence
- `T1587.003` — Use of PowerShell for lateral movement
- `T1023.001` — Credential dumping via LSASS memory access
- `T1426.007` — Valid accounts — compromised credentials
- `T1333.007` — WMI event subscription for persistence
- `T1189.003` — Registry run key persistence
- `T1293.004` — WMI event subscription for persistence
- `T1546.000` — Network share discovery via net view
- `T1578.002` — Registry run key persistence
- `T1400.003` — DLL side-loading via signed binary
- `T1208.006` — Living-off-the-land via certutil
- `T1505.007` — Use of PowerShell for lateral movement
- `T1327.009` — Credential dumping via LSASS memory access
- `T1440.000` — Spearphishing attachment with macro
- `T1396.002` — Credential dumping via LSASS memory access
- `T1662.007` — WMI event subscription for persistence
- `T1013.009` — C2 beacon to port 54008
- `T1192.007` — DLL side-loading via signed binary
- `T1241.000` — Network share discovery via net view
- `T1432.009` — Registry run key persistence
- `T1603.007` — Data staged to temp directory prior to exfil
- `T1163.001` — Living-off-the-land via certutil
- `T1692.008` — Exfil to 178.154.142.146 via DNS tunneling
- `T1389.002` — Valid accounts — compromised credentials
- `T1488.006` — Scheduled task persistence mechanism
- `T1245.001` — WMI event subscription for persistence
- `T1642.006` — WMI event subscription for persistence
- `T1178.000` — DLL side-loading via signed binary
- `T1225.009` — Living-off-the-land via certutil
- `T1255.006` — Data staged to temp directory prior to exfil
- `T1551.006` — Network share discovery via net view
- `T1157.006` — Valid accounts — compromised credentials
- `T1022.006` — DLL side-loading via signed binary
- `T1516.003` — Network share discovery via net view
- `T1204.005` — C2 beacon to port 16231
- `T1409.003` — Scheduled task persistence mechanism
- `T1459.005` — Command and control via HTTPS on port 443
- `T1046.008` — C2 beacon to port 10727
- `T1226.000` — Use of PowerShell for lateral movement
- `T1410.009` — Use of PowerShell for lateral movement
- `T1258.006` — C2 beacon to port 20551
- `T1170.009` — Credential dumping via LSASS memory access
- `T1357.008` — Credential dumping via LSASS memory access
- `T1668.000` — Exfil to 199.13.255.254 via DNS tunneling
- `T1315.008` — Data staged to temp directory prior to exfil
- `T1176.008` — Data staged to temp directory prior to exfil
- `T1242.009` — Credential dumping via LSASS memory access
- `T1593.007` — Command and control via HTTPS on port 443
- `T1642.004` — Valid accounts — compromised credentials
- `T1508.002` — Network share discovery via net view
- `T1230.002` — Use of PowerShell for lateral movement
- `T1369.004` — Command and control via HTTPS on port 443
- `T1376.004` — Spearphishing attachment with macro
- `T1276.000` — Command and control via HTTPS on port 443
- `T1420.000` — Scheduled task persistence mechanism
- `T1335.008` — WMI event subscription for persistence
- `T1583.005` — Exfil to 54.83.16.139 via DNS tunneling
- `T1685.004` — Use of PowerShell for lateral movement
- `T1601.005` — Scheduled task persistence mechanism
- `T1294.003` — Credential dumping via LSASS memory access
- `T1272.001` — Exfil to 114.82.167.114 via DNS tunneling
- `T1577.009` — Valid accounts — compromised credentials
- `T1473.005` — Command and control via HTTPS on port 443
- `T1528.003` — DLL side-loading via signed binary
- `T1443.009` — Data staged to temp directory prior to exfil
- `T1625.001` — Spearphishing attachment with macro
- `T1485.008` — Registry run key persistence
- `T1105.002` — Exfil to 127.249.36.139 via DNS tunneling
- `T1040.001` — C2 beacon to port 64769
- `T1309.002` — Registry run key persistence
- `T1477.006` — Use of PowerShell for lateral movement
- `T1410.006` — Scheduled task persistence mechanism
- `T1101.000` — Spearphishing attachment with macro
- `T1138.000` — DLL side-loading via signed binary
- `T1680.000` — Credential dumping via LSASS memory access
- `T1277.005` — Data staged to temp directory prior to exfil
- `T1143.003` — Exfil to 142.253.102.132 via DNS tunneling
- `T1677.000` — Exfil to 88.196.92.138 via DNS tunneling
- `T1682.002` — Credential dumping via LSASS memory access
- `T1215.000` — Credential dumping via LSASS memory access
- `T1545.006` — Use of PowerShell for lateral movement
- `T1480.008` — Data staged to temp directory prior to exfil
- `T1212.002` — Data staged to temp directory prior to exfil
- `T1421.001` — Credential dumping via LSASS memory access
- `T1678.008` — Registry run key persistence
- `T1366.005` — Registry run key persistence
- `T1370.008` — C2 beacon to port 61267
- `T1502.003` — Use of PowerShell for lateral movement
- `T1245.008` — Data staged to temp directory prior to exfil
- `T1385.005` — Data staged to temp directory prior to exfil
- `T1453.006` — Credential dumping via LSASS memory access
- `T1126.000` — Network share discovery via net view
- `T1611.002` — DLL side-loading via signed binary
- `T1604.006` — Spearphishing attachment with macro
- `T1047.000` — Network share discovery via net view
- `T1539.002` — Valid accounts — compromised credentials
- `T1586.008` — Scheduled task persistence mechanism
- `T1005.005` — C2 beacon to port 38568
- `T1301.008` — WMI event subscription for persistence
- `T1376.006` — C2 beacon to port 56702
- `T1259.002` — Credential dumping via LSASS memory access
- `T1087.002` — DLL side-loading via signed binary
- `T1217.002` — Scheduled task persistence mechanism
- `T1646.005` — Data staged to temp directory prior to exfil
- `T1680.000` — Scheduled task persistence mechanism
- `T1011.002` — Command and control via HTTPS on port 443
- `T1618.006` — C2 beacon to port 48765
- `T1049.004` — WMI event subscription for persistence
- `T1673.003` — Credential dumping via LSASS memory access
- `T1392.001` — Network share discovery via net view
- `T1178.009` — Registry run key persistence
- `T1600.008` — Network share discovery via net view
- `T1577.001` — Registry run key persistence
- `T1315.004` — C2 beacon to port 5982
- `T1082.008` — Exfil to 18.138.80.232 via DNS tunneling
- `T1282.009` — Valid accounts — compromised credentials
- `T1353.001` — Scheduled task persistence mechanism
- `T1170.008` — Registry run key persistence
- `T1127.001` — C2 beacon to port 35637
- `T1684.001` — Command and control via HTTPS on port 443
- `T1167.001` — Living-off-the-land via certutil
- `T1324.009` — Use of PowerShell for lateral movement
- `T1141.009` — Credential dumping via LSASS memory access
- `T1484.003` — Credential dumping via LSASS memory access
- `T1434.001` — Network share discovery via net view
- `T1060.003` — DLL side-loading via signed binary
- `T1634.001` — Credential dumping via LSASS memory access
- `T1361.007` — Exfil to 206.53.51.120 via DNS tunneling
- `T1077.004` — C2 beacon to port 14366
- `T1418.004` — Registry run key persistence
- `T1505.005` — Living-off-the-land via certutil
- `T1454.000` — C2 beacon to port 61234
- `T1150.007` — C2 beacon to port 56286
- `T1012.000` — Valid accounts — compromised credentials
- `T1616.000` — Registry run key persistence
- `T1660.006` — Valid accounts — compromised credentials
- `T1383.005` — Credential dumping via LSASS memory access
- `T1243.009` — Data staged to temp directory prior to exfil
- `T1229.005` — Scheduled task persistence mechanism
- `T1144.001` — WMI event subscription for persistence
- `T1386.008` — Scheduled task persistence mechanism
- `T1300.000` — Valid accounts — compromised credentials
- `T1109.007` — Scheduled task persistence mechanism
- `T1692.008` — Spearphishing attachment with macro
- `T1415.008` — Exfil to 28.222.208.162 via DNS tunneling

## Indicators of Compromise

| Type | Value | Confidence |
|------|-------|------------|
| Domain | `cdn28-update.ppkcdo.com` | HIGH |
| IP | `219.5.151.85` | HIGH |
| SHA256 | `e00a005a590f780ddf3dac03e9059d58a4aca4745b4c86f2967d93539e307ead` | MEDIUM |
| IP | `157.209.86.102` | LOW |
| IP | `197.156.41.43` | HIGH |
| SHA256 | `9518f644369688897317865ce0db97367652350928112a4fdebe49f5104417da` | HIGH |
| IP | `83.49.63.81` | MEDIUM |
| SHA256 | `a14fd8a391ff879f5c764b537a307c72d6bce20e8cc4c74d25894e8a487b6aa2` | LOW |
| SHA256 | `0e8efd28af56467f8ad4c230c2c5a2788d6e2a365dd2ca4a7200377bcd0a2be2` | LOW |
| SHA256 | `d3b46af393324c88331572e6dd12102fe2c04352b572feb5b616de0c777871bb` | MEDIUM |
| URL | `http://115.141.29.193/payload.php` | HIGH |
| Domain | `cdn22-update.hdboeh.com` | HIGH |
| Domain | `cdn68-update.hnopnl.com` | HIGH |
| URL | `http://71.31.127.167/payload.php` | MEDIUM |
| URL | `http://187.207.44.231/payload.php` | MEDIUM |
| Domain | `cdn49-update.ngfmmj.com` | HIGH |
| SHA256 | `3f94d2cc3a51a7511b032e80e9e175530cc79f65b5a9257c6e862150feacc989` | MEDIUM |
| URL | `http://100.166.220.218/payload.php` | MEDIUM |
| URL | `http://211.98.53.143/payload.php` | LOW |
| IP | `158.75.206.220` | LOW |
| IP | `76.200.113.31` | LOW |
| IP | `164.245.80.129` | MEDIUM |
| SHA256 | `cad83f1a8c881d67bfcc5178e08093dc3f2f4c4fe33c37b50a85ff8aa1266187` | LOW |
| IP | `155.153.46.97` | MEDIUM |
| URL | `http://111.143.12.90/payload.php` | MEDIUM |
| IP | `128.224.81.77` | MEDIUM |
| Domain | `cdn23-update.gpklfl.com` | LOW |
| Domain | `cdn66-update.jgfahk.com` | LOW |
| IP | `202.75.191.156` | HIGH |
| SHA256 | `e1fa23064cf63b5717c112a171b4ca22b9d709026efa84266ff93f91ee2be162` | LOW |
| Domain | `cdn69-update.ncacpf.com` | MEDIUM |
| URL | `http://184.27.197.234/payload.php` | MEDIUM |
| IP | `215.46.167.56` | HIGH |
| URL | `http://199.176.15.192/payload.php` | MEDIUM |
| Domain | `cdn85-update.iefdcg.com` | MEDIUM |
| URL | `http://22.140.6.119/payload.php` | MEDIUM |
| IP | `202.70.76.211` | MEDIUM |
| Domain | `cdn71-update.cnnnab.com` | HIGH |
| SHA256 | `ce9442313f5377fc6eea2d02c85020181b2772095a89154d26ccb1944f2de43d` | MEDIUM |
| Domain | `cdn48-update.dbpakl.com` | LOW |
| Domain | `cdn38-update.hnmpkk.com` | MEDIUM |
| SHA256 | `06d83d43bab6742245635031e7b85c5ae2b9f7c1c6c557854e5176ca921c2571` | HIGH |
| URL | `http://159.185.34.111/payload.php` | HIGH |
| URL | `http://74.184.194.119/payload.php` | LOW |
| SHA256 | `c3ae83be811bb4e9b090b2f53450978d6d74b05cc64179b60102c1710009e3ac` | LOW |
| IP | `173.26.159.45` | HIGH |
| SHA256 | `25e82761f61007ea2e78284c16634725cf40f4e0e1c3964a9f7b7dc369e1a47b` | HIGH |
| URL | `http://38.112.123.197/payload.php` | LOW |
| IP | `163.115.59.250` | HIGH |
| IP | `92.165.92.252` | MEDIUM |
| SHA256 | `bb2d2a9dd7a65721a9e38410498dcff987de8b765f1eff5f37db3ef9da04b9ca` | MEDIUM |
| SHA256 | `a9c8fd3be09b8bdf0c86ad7104c841bdd11d342917c982229f421bc040321526` | LOW |
| SHA256 | `c3cd98fc056939c8bcd30401e95610b31445dbf19e633f32870ed9c366f02cb3` | LOW |
| SHA256 | `ec4ec3ab7ca585ead6e72d98d80edef3a2799d745dd69fcba87c4d91ab64d8c1` | HIGH |
| URL | `http://108.80.217.62/payload.php` | LOW |
| URL | `http://8.87.110.175/payload.php` | HIGH |
| IP | `18.138.99.181` | MEDIUM |
| IP | `186.18.2.183` | HIGH |
| IP | `86.218.45.234` | HIGH |
| IP | `128.136.106.76` | HIGH |


---

# Threat Actor Profile: DarkSide (CARBON STORM)

**Motivation**: ransomware
**Primary techniques**: RDP brute-force, living-off-the-land

## Observed TTPs

- `T1453.003` — Scheduled task persistence mechanism
- `T1257.008` — Scheduled task persistence mechanism
- `T1504.002` — Use of PowerShell for lateral movement
- `T1555.009` — Network share discovery via net view
- `T1575.003` — Valid accounts — compromised credentials
- `T1360.007` — Credential dumping via LSASS memory access
- `T1375.001` — Scheduled task persistence mechanism
- `T1482.004` — Scheduled task persistence mechanism
- `T1085.006` — WMI event subscription for persistence
- `T1126.003` — Command and control via HTTPS on port 443
- `T1514.004` — C2 beacon to port 64173
- `T1396.007` — Valid accounts — compromised credentials
- `T1239.000` — Command and control via HTTPS on port 443
- `T1533.000` — Living-off-the-land via certutil
- `T1395.001` — DLL side-loading via signed binary
- `T1332.000` — Network share discovery via net view
- `T1446.006` — Exfil to 128.225.214.220 via DNS tunneling
- `T1267.006` — Registry run key persistence
- `T1082.007` — Valid accounts — compromised credentials
- `T1353.001` — C2 beacon to port 2787
- `T1643.001` — Valid accounts — compromised credentials
- `T1676.004` — C2 beacon to port 56214
- `T1109.009` — Credential dumping via LSASS memory access
- `T1133.000` — Scheduled task persistence mechanism
- `T1351.002` — Scheduled task persistence mechanism
- `T1311.000` — Spearphishing attachment with macro
- `T1250.000` — C2 beacon to port 53273
- `T1691.006` — Registry run key persistence
- `T1590.009` — Network share discovery via net view
- `T1544.006` — Living-off-the-land via certutil
- `T1063.004` — Registry run key persistence
- `T1570.004` — Command and control via HTTPS on port 443
- `T1290.001` — Living-off-the-land via certutil
- `T1036.002` — WMI event subscription for persistence
- `T1669.009` — Command and control via HTTPS on port 443
- `T1643.003` — Living-off-the-land via certutil
- `T1301.006` — Data staged to temp directory prior to exfil
- `T1312.009` — C2 beacon to port 18497
- `T1609.004` — Credential dumping via LSASS memory access
- `T1361.003` — C2 beacon to port 65499
- `T1233.007` — Valid accounts — compromised credentials
- `T1217.006` — DLL side-loading via signed binary
- `T1246.005` — Valid accounts — compromised credentials
- `T1334.006` — Network share discovery via net view
- `T1110.000` — Registry run key persistence
- `T1505.004` — Command and control via HTTPS on port 443
- `T1384.001` — Command and control via HTTPS on port 443
- `T1669.001` — WMI event subscription for persistence
- `T1583.005` — Registry run key persistence
- `T1063.005` — Network share discovery via net view
- `T1346.005` — Scheduled task persistence mechanism
- `T1281.008` — Network share discovery via net view
- `T1196.001` — Use of PowerShell for lateral movement
- `T1583.004` — Exfil to 51.18.145.160 via DNS tunneling
- `T1235.005` — C2 beacon to port 20654
- `T1681.007` — WMI event subscription for persistence
- `T1168.004` — Living-off-the-land via certutil
- `T1155.007` — Spearphishing attachment with macro
- `T1074.003` — Data staged to temp directory prior to exfil
- `T1220.004` — Credential dumping via LSASS memory access
- `T1641.005` — Valid accounts — compromised credentials
- `T1475.000` — Use of PowerShell for lateral movement
- `T1608.003` — Scheduled task persistence mechanism
- `T1278.008` — Scheduled task persistence mechanism
- `T1064.000` — Command and control via HTTPS on port 443
- `T1228.000` — WMI event subscription for persistence
- `T1133.003` — Registry run key persistence
- `T1323.007` — Registry run key persistence
- `T1359.002` — Exfil to 223.22.42.1 via DNS tunneling
- `T1277.005` — Valid accounts — compromised credentials
- `T1611.002` — Spearphishing attachment with macro
- `T1483.007` — Registry run key persistence
- `T1305.006` — Network share discovery via net view
- `T1030.007` — Data staged to temp directory prior to exfil
- `T1523.001` — C2 beacon to port 22575
- `T1572.003` — WMI event subscription for persistence
- `T1254.002` — C2 beacon to port 43233
- `T1700.006` — Valid accounts — compromised credentials
- `T1498.000` — DLL side-loading via signed binary
- `T1604.002` — Data staged to temp directory prior to exfil
- `T1409.008` — Spearphishing attachment with macro
- `T1166.005` — Scheduled task persistence mechanism
- `T1420.004` — C2 beacon to port 50071
- `T1258.008` — Living-off-the-land via certutil
- `T1396.000` — Scheduled task persistence mechanism
- `T1380.000` — Command and control via HTTPS on port 443
- `T1006.003` — Valid accounts — compromised credentials
- `T1278.003` — WMI event subscription for persistence
- `T1532.001` — Valid accounts — compromised credentials
- `T1124.009` — Network share discovery via net view
- `T1436.008` — Data staged to temp directory prior to exfil
- `T1530.001` — Scheduled task persistence mechanism
- `T1601.007` — Credential dumping via LSASS memory access
- `T1623.004` — Credential dumping via LSASS memory access
- `T1369.005` — Scheduled task persistence mechanism
- `T1524.002` — Data staged to temp directory prior to exfil
- `T1246.002` — WMI event subscription for persistence
- `T1529.000` — WMI event subscription for persistence
- `T1283.004` — Living-off-the-land via certutil
- `T1246.006` — Network share discovery via net view
- `T1359.007` — Network share discovery via net view
- `T1552.008` — Network share discovery via net view
- `T1333.004` — DLL side-loading via signed binary
- `T1206.004` — Registry run key persistence
- `T1639.003` — Registry run key persistence
- `T1300.002` — Data staged to temp directory prior to exfil
- `T1150.000` — C2 beacon to port 3115
- `T1403.002` — Command and control via HTTPS on port 443
- `T1059.002` — Command and control via HTTPS on port 443
- `T1452.009` — C2 beacon to port 38776
- `T1677.002` — Valid accounts — compromised credentials
- `T1497.000` — Credential dumping via LSASS memory access
- `T1647.007` — Credential dumping via LSASS memory access
- `T1021.004` — Use of PowerShell for lateral movement
- `T1638.000` — Scheduled task persistence mechanism
- `T1639.000` — Exfil to 51.197.185.249 via DNS tunneling
- `T1289.005` — Network share discovery via net view
- `T1578.002` — Data staged to temp directory prior to exfil
- `T1375.009` — Spearphishing attachment with macro
- `T1497.005` — Spearphishing attachment with macro
- `T1110.005` — Living-off-the-land via certutil
- `T1221.005` — Registry run key persistence
- `T1321.005` — Scheduled task persistence mechanism
- `T1610.002` — Command and control via HTTPS on port 443
- `T1150.008` — Exfil to 113.139.106.11 via DNS tunneling
- `T1424.000` — Data staged to temp directory prior to exfil
- `T1090.008` — Network share discovery via net view
- `T1513.007` — Credential dumping via LSASS memory access
- `T1645.005` — Credential dumping via LSASS memory access
- `T1146.009` — WMI event subscription for persistence
- `T1026.006` — Valid accounts — compromised credentials
- `T1500.002` — Spearphishing attachment with macro
- `T1526.003` — Command and control via HTTPS on port 443
- `T1483.000` — Data staged to temp directory prior to exfil
- `T1534.008` — Exfil to 64.235.2.52 via DNS tunneling
- `T1186.000` — C2 beacon to port 29518
- `T1149.000` — Living-off-the-land via certutil
- `T1449.002` — Data staged to temp directory prior to exfil
- `T1206.004` — Command and control via HTTPS on port 443
- `T1614.002` — C2 beacon to port 36665
- `T1287.002` — C2 beacon to port 1107
- `T1416.000` — Living-off-the-land via certutil
- `T1072.004` — Credential dumping via LSASS memory access
- `T1428.004` — Registry run key persistence
- `T1066.005` — Credential dumping via LSASS memory access
- `T1513.006` — Registry run key persistence
- `T1053.005` — Use of PowerShell for lateral movement
- `T1362.009` — Credential dumping via LSASS memory access
- `T1134.001` — C2 beacon to port 14038
- `T1496.003` — Data staged to temp directory prior to exfil
- `T1325.005` — Network share discovery via net view
- `T1636.001` — Use of PowerShell for lateral movement
- `T1595.000` — Command and control via HTTPS on port 443
- `T1432.005` — Spearphishing attachment with macro
- `T1573.009` — Exfil to 186.131.168.198 via DNS tunneling
- `T1163.008` — Registry run key persistence
- `T1474.007` — Exfil to 85.102.87.15 via DNS tunneling
- `T1189.004` — Network share discovery via net view
- `T1471.000` — C2 beacon to port 44609
- `T1490.002` — Credential dumping via LSASS memory access
- `T1338.008` — Network share discovery via net view
- `T1500.003` — Network share discovery via net view
- `T1190.004` — Data staged to temp directory prior to exfil
- `T1659.005` — Scheduled task persistence mechanism
- `T1278.009` — Use of PowerShell for lateral movement
- `T1114.001` — Credential dumping via LSASS memory access
- `T1177.005` — Valid accounts — compromised credentials
- `T1673.004` — Registry run key persistence
- `T1438.005` — Living-off-the-land via certutil
- `T1549.009` — DLL side-loading via signed binary
- `T1393.004` — Spearphishing attachment with macro
- `T1625.004` — Use of PowerShell for lateral movement
- `T1358.003` — Command and control via HTTPS on port 443
- `T1358.004` — C2 beacon to port 35393
- `T1395.004` — Credential dumping via LSASS memory access
- `T1067.008` — DLL side-loading via signed binary
- `T1262.000` — Spearphishing attachment with macro
- `T1310.003` — DLL side-loading via signed binary
- `T1152.008` — Registry run key persistence
- `T1097.009` — Use of PowerShell for lateral movement

## Indicators of Compromise

| Type | Value | Confidence |
|------|-------|------------|
| SHA256 | `f7c708397460b439b8e9b8cf081c968120cdf23ba65f494c146084263429007b` | LOW |
| Domain | `cdn71-update.eopcdl.com` | LOW |
| IP | `149.67.118.146` | HIGH |
| IP | `28.97.148.145` | LOW |
| SHA256 | `4e20d27179c3fcaabd933c23d555ca9373938487988267a46cbc4482400bfe9f` | LOW |
| URL | `http://86.34.41.129/payload.php` | HIGH |
| URL | `http://200.94.101.95/payload.php` | MEDIUM |
| URL | `http://11.252.59.162/payload.php` | MEDIUM |
| SHA256 | `c538d88aef204abf44cc35142eb9a9db74ee6440fa1616272de9597cf3f9e601` | MEDIUM |
| IP | `162.71.161.167` | MEDIUM |
| URL | `http://190.184.34.83/payload.php` | LOW |
| SHA256 | `3771a86b4a8f66c4cc8c02f2a754f63929abfc2980ea3b626c9165ccafb5f57c` | LOW |
| IP | `85.133.226.247` | MEDIUM |
| URL | `http://134.200.195.41/payload.php` | HIGH |
| Domain | `cdn4-update.hmmnaj.com` | LOW |
| SHA256 | `a4947d5547895b4dd6cc04b5ae08ce218ce459e98be6aa789333b36bab8475f1` | MEDIUM |
| URL | `http://89.46.47.197/payload.php` | LOW |
| IP | `128.95.109.66` | HIGH |
| IP | `13.168.8.58` | MEDIUM |
| SHA256 | `29cfaf75d19c8b502fee4dfb9d2e655774c488b15325ad2c371f5b315cf2fc0d` | HIGH |
| Domain | `cdn56-update.jmacpj.com` | HIGH |
| Domain | `cdn22-update.hdfili.com` | LOW |
| URL | `http://74.82.34.51/payload.php` | LOW |
| IP | `63.120.157.189` | HIGH |
| IP | `131.224.130.119` | MEDIUM |
| IP | `203.20.97.250` | MEDIUM |
| Domain | `cdn62-update.hdbpbl.com` | LOW |
| URL | `http://201.151.86.186/payload.php` | HIGH |
| IP | `37.95.179.234` | MEDIUM |
| SHA256 | `de208f34f25b3f75095627cc8ee0bca9a86410f528f67bc2b2bc32346ce9aef6` | MEDIUM |
| IP | `151.77.11.121` | LOW |
| Domain | `cdn27-update.mhalal.com` | HIGH |
| URL | `http://80.118.13.185/payload.php` | MEDIUM |
| URL | `http://35.135.28.121/payload.php` | HIGH |
| IP | `194.201.225.183` | HIGH |
| Domain | `cdn29-update.mifadf.com` | LOW |
| Domain | `cdn67-update.lieppe.com` | LOW |
| URL | `http://70.189.187.103/payload.php` | LOW |
| SHA256 | `fb32e73867942234b619d5ce49275af091f026830ee129c839652ea962e196be` | HIGH |
| SHA256 | `66310332bfc460150a6989e8d21e97d7736dfe51bd10bc7b5b3cf675f0dd68e5` | LOW |
| SHA256 | `8f5677e98e1d87a6ce1a4f5b4116e45f458f682cb3d15543b1883df17f51cb90` | LOW |
| SHA256 | `afb0bee8bdd2cefc3b5b5e8a53d6b04a93f7d5b770afdb04ae5cb6c0828af706` | HIGH |
| URL | `http://120.34.223.14/payload.php` | MEDIUM |
| SHA256 | `b30d0062e7f09725289a0887b30cb12f9c01f0c8f8f24c672c42dbd369ecfcde` | HIGH |
| Domain | `cdn44-update.lgfblm.com` | HIGH |
| Domain | `cdn87-update.nfheka.com` | LOW |
| SHA256 | `2382a3198989ea790f37aab3e81ade6c69bf5230d532df48a2ca5f85c7b73bd6` | HIGH |
| Domain | `cdn47-update.jblmfm.com` | HIGH |
| IP | `6.136.184.62` | LOW |
| SHA256 | `07dcafde49d57767c05dc2b03fa6f2d969d3cbc8f9bf7b46e2cb6f6a3ed84d09` | HIGH |
| IP | `64.223.210.133` | MEDIUM |
| URL | `http://11.58.163.83/payload.php` | HIGH |
| IP | `189.19.206.39` | MEDIUM |
| SHA256 | `a57d2155ec043d9107252240aad7b92c75af1a7a105e9875f2de359219283b44` | MEDIUM |
| SHA256 | `511e655cfbebe6af6db0161803fcd912077a64f418e4893edb8366b96a28afc2` | LOW |
| URL | `http://139.203.128.115/payload.php` | MEDIUM |
| URL | `http://26.127.45.129/payload.php` | LOW |
| URL | `http://71.70.227.164/payload.php` | HIGH |
| IP | `59.38.105.35` | LOW |
| SHA256 | `b3479053ee8698541f2d7a5eb6d0fdd3642312eed001247f9ff04aa57f44829f` | MEDIUM |


---

# Threat Actor Profile: SilverTerrier (UNKNOWN)

**Motivation**: BEC fraud
**Primary techniques**: phishing, credential stuffing

## Observed TTPs

- `T1275.006` — C2 beacon to port 22614
- `T1408.001` — Command and control via HTTPS on port 443
- `T1487.008` — Data staged to temp directory prior to exfil
- `T1371.004` — Exfil to 55.131.166.115 via DNS tunneling
- `T1431.001` — Registry run key persistence
- `T1210.002` — DLL side-loading via signed binary
- `T1428.007` — Registry run key persistence
- `T1461.008` — Data staged to temp directory prior to exfil
- `T1420.007` — Spearphishing attachment with macro
- `T1565.004` — Valid accounts — compromised credentials
- `T1233.007` — Data staged to temp directory prior to exfil
- `T1634.000` — Spearphishing attachment with macro
- `T1511.006` — Exfil to 80.91.106.167 via DNS tunneling
- `T1467.003` — Credential dumping via LSASS memory access
- `T1236.003` — Credential dumping via LSASS memory access
- `T1164.008` — Network share discovery via net view
- `T1587.001` — DLL side-loading via signed binary
- `T1225.008` — Living-off-the-land via certutil
- `T1580.002` — Scheduled task persistence mechanism
- `T1616.006` — Credential dumping via LSASS memory access
- `T1670.006` — Scheduled task persistence mechanism
- `T1434.006` — WMI event subscription for persistence
- `T1049.007` — Data staged to temp directory prior to exfil
- `T1480.007` — Network share discovery via net view
- `T1652.001` — Exfil to 162.245.150.130 via DNS tunneling
- `T1592.001` — C2 beacon to port 1942
- `T1504.005` — Command and control via HTTPS on port 443
- `T1507.008` — Credential dumping via LSASS memory access
- `T1504.000` — WMI event subscription for persistence
- `T1054.006` — Data staged to temp directory prior to exfil
- `T1328.001` — Network share discovery via net view
- `T1458.002` — Spearphishing attachment with macro
- `T1116.006` — Scheduled task persistence mechanism
- `T1085.003` — Spearphishing attachment with macro
- `T1192.000` — Exfil to 1.11.77.146 via DNS tunneling
- `T1537.004` — Registry run key persistence
- `T1009.007` — Credential dumping via LSASS memory access
- `T1031.005` — DLL side-loading via signed binary
- `T1658.005` — Data staged to temp directory prior to exfil
- `T1344.008` — Use of PowerShell for lateral movement
- `T1292.005` — Scheduled task persistence mechanism
- `T1468.007` — Data staged to temp directory prior to exfil
- `T1555.007` — Data staged to temp directory prior to exfil
- `T1064.005` — Valid accounts — compromised credentials
- `T1064.008` — Valid accounts — compromised credentials
- `T1621.006` — Network share discovery via net view
- `T1520.008` — Command and control via HTTPS on port 443
- `T1643.006` — Spearphishing attachment with macro
- `T1154.001` — Valid accounts — compromised credentials
- `T1667.000` — Credential dumping via LSASS memory access
- `T1330.000` — Living-off-the-land via certutil
- `T1667.002` — Valid accounts — compromised credentials
- `T1381.007` — DLL side-loading via signed binary
- `T1558.001` — Command and control via HTTPS on port 443
- `T1463.002` — C2 beacon to port 18339
- `T1512.008` — Spearphishing attachment with macro
- `T1601.005` — WMI event subscription for persistence
- `T1025.002` — Scheduled task persistence mechanism
- `T1509.007` — WMI event subscription for persistence
- `T1685.009` — Living-off-the-land via certutil
- `T1414.007` — DLL side-loading via signed binary
- `T1151.000` — Registry run key persistence
- `T1422.007` — Credential dumping via LSASS memory access
- `T1472.001` — Spearphishing attachment with macro
- `T1232.008` — Data staged to temp directory prior to exfil
- `T1636.005` — Spearphishing attachment with macro
- `T1601.008` — Spearphishing attachment with macro
- `T1054.008` — Network share discovery via net view
- `T1161.004` — Valid accounts — compromised credentials
- `T1093.008` — Spearphishing attachment with macro
- `T1190.005` — Registry run key persistence
- `T1048.006` — Exfil to 173.210.142.38 via DNS tunneling
- `T1461.009` — Command and control via HTTPS on port 443
- `T1574.008` — Exfil to 192.70.33.105 via DNS tunneling
- `T1200.006` — Exfil to 109.240.33.225 via DNS tunneling
- `T1573.003` — DLL side-loading via signed binary
- `T1352.001` — Exfil to 192.135.51.11 via DNS tunneling
- `T1180.004` — Credential dumping via LSASS memory access
- `T1333.001` — Data staged to temp directory prior to exfil
- `T1209.009` — DLL side-loading via signed binary
- `T1613.007` — Data staged to temp directory prior to exfil
- `T1595.009` — DLL side-loading via signed binary
- `T1622.002` — Valid accounts — compromised credentials
- `T1333.008` — Exfil to 22.211.143.153 via DNS tunneling
- `T1494.008` — C2 beacon to port 21518
- `T1161.009` — Living-off-the-land via certutil
- `T1512.002` — Registry run key persistence
- `T1424.001` — Registry run key persistence
- `T1558.000` — Use of PowerShell for lateral movement
- `T1032.004` — Credential dumping via LSASS memory access
- `T1128.005` — DLL side-loading via signed binary
- `T1402.009` — Scheduled task persistence mechanism
- `T1573.004` — Data staged to temp directory prior to exfil
- `T1010.009` — Network share discovery via net view
- `T1234.009` — Command and control via HTTPS on port 443
- `T1033.008` — Living-off-the-land via certutil
- `T1502.003` — Command and control via HTTPS on port 443
- `T1041.006` — C2 beacon to port 23605
- `T1059.009` — Credential dumping via LSASS memory access
- `T1366.002` — Use of PowerShell for lateral movement
- `T1216.004` — C2 beacon to port 2262
- `T1613.004` — WMI event subscription for persistence
- `T1616.006` — Scheduled task persistence mechanism
- `T1333.006` — Scheduled task persistence mechanism
- `T1420.004` — Use of PowerShell for lateral movement
- `T1331.001` — Network share discovery via net view
- `T1372.007` — Data staged to temp directory prior to exfil
- `T1632.008` — Registry run key persistence
- `T1642.006` — Credential dumping via LSASS memory access
- `T1526.000` — DLL side-loading via signed binary
- `T1512.000` — Use of PowerShell for lateral movement
- `T1188.004` — Network share discovery via net view
- `T1167.002` — WMI event subscription for persistence
- `T1355.000` — Command and control via HTTPS on port 443
- `T1469.008` — C2 beacon to port 46736
- `T1374.000` — Spearphishing attachment with macro
- `T1584.003` — Data staged to temp directory prior to exfil
- `T1560.001` — DLL side-loading via signed binary
- `T1416.009` — Network share discovery via net view
- `T1623.004` — Living-off-the-land via certutil
- `T1580.006` — Exfil to 165.13.158.11 via DNS tunneling
- `T1185.005` — Exfil to 34.140.171.103 via DNS tunneling
- `T1331.005` — WMI event subscription for persistence
- `T1534.000` — Data staged to temp directory prior to exfil
- `T1468.003` — Command and control via HTTPS on port 443
- `T1368.002` — Spearphishing attachment with macro
- `T1515.004` — C2 beacon to port 19728
- `T1207.009` — Valid accounts — compromised credentials
- `T1617.002` — Exfil to 151.69.241.202 via DNS tunneling
- `T1370.004` — Data staged to temp directory prior to exfil
- `T1103.001` — Valid accounts — compromised credentials
- `T1243.005` — Living-off-the-land via certutil
- `T1670.000` — Scheduled task persistence mechanism
- `T1351.006` — WMI event subscription for persistence
- `T1368.004` — DLL side-loading via signed binary
- `T1050.006` — Credential dumping via LSASS memory access
- `T1622.000` — Registry run key persistence
- `T1080.009` — DLL side-loading via signed binary
- `T1527.000` — WMI event subscription for persistence
- `T1573.008` — Scheduled task persistence mechanism
- `T1480.007` — Command and control via HTTPS on port 443
- `T1034.009` — DLL side-loading via signed binary
- `T1356.005` — C2 beacon to port 46379
- `T1457.000` — Scheduled task persistence mechanism
- `T1479.006` — WMI event subscription for persistence
- `T1165.004` — Command and control via HTTPS on port 443
- `T1667.001` — Network share discovery via net view
- `T1524.000` — DLL side-loading via signed binary
- `T1457.001` — Scheduled task persistence mechanism
- `T1057.006` — Valid accounts — compromised credentials
- `T1616.004` — Spearphishing attachment with macro
- `T1652.000` — WMI event subscription for persistence
- `T1386.003` — Credential dumping via LSASS memory access
- `T1423.009` — Credential dumping via LSASS memory access
- `T1284.002` — C2 beacon to port 8305
- `T1089.008` — Spearphishing attachment with macro
- `T1314.005` — Command and control via HTTPS on port 443
- `T1623.003` — Valid accounts — compromised credentials
- `T1072.000` — Scheduled task persistence mechanism
- `T1109.000` — Valid accounts — compromised credentials
- `T1695.004` — Exfil to 103.209.203.61 via DNS tunneling
- `T1213.008` — Valid accounts — compromised credentials
- `T1455.002` — Registry run key persistence
- `T1460.004` — WMI event subscription for persistence
- `T1563.000` — Network share discovery via net view
- `T1223.004` — Living-off-the-land via certutil
- `T1466.002` — Exfil to 195.24.48.19 via DNS tunneling
- `T1158.005` — Valid accounts — compromised credentials
- `T1448.007` — Living-off-the-land via certutil
- `T1016.002` — Registry run key persistence
- `T1036.009` — C2 beacon to port 32442
- `T1346.007` — Scheduled task persistence mechanism
- `T1618.003` — Scheduled task persistence mechanism
- `T1694.004` — Use of PowerShell for lateral movement
- `T1153.004` — Credential dumping via LSASS memory access
- `T1496.006` — Registry run key persistence
- `T1597.003` — Exfil to 6.24.91.200 via DNS tunneling
- `T1609.004` — C2 beacon to port 50508
- `T1041.008` — Command and control via HTTPS on port 443
- `T1276.001` — Network share discovery via net view

## Indicators of Compromise

| Type | Value | Confidence |
|------|-------|------------|
| SHA256 | `6bfc0efd1bb325629e1489f878784de5048524c09e18e52db95d57441fa4a7a5` | HIGH |
| SHA256 | `b11fb55f36d8997bab22069bc0e4c95a8bd5e97036cb4734d0d5137ec709be85` | HIGH |
| Domain | `cdn73-update.noanbo.com` | MEDIUM |
| IP | `68.136.47.101` | HIGH |
| IP | `198.246.135.21` | LOW |
| IP | `71.135.85.205` | MEDIUM |
| URL | `http://114.120.79.185/payload.php` | HIGH |
| URL | `http://4.7.81.28/payload.php` | HIGH |
| SHA256 | `c7cc8a01ea4302fed7afdfce9b4dd6c2d9955a7ab2b89ea50f795b96d45551fc` | MEDIUM |
| Domain | `cdn26-update.foenpf.com` | MEDIUM |
| SHA256 | `c9400de40d9968f5e5e8db7cb672f1749a38f09e9aace33b925669938ac4e633` | HIGH |
| IP | `39.115.154.226` | LOW |
| URL | `http://151.96.39.124/payload.php` | HIGH |
| URL | `http://119.151.8.237/payload.php` | HIGH |
| SHA256 | `79feed6107228620fa2afa6db0e708da408918930c50f7be3cc727d252204561` | HIGH |
| URL | `http://223.137.129.209/payload.php` | HIGH |
| URL | `http://180.126.71.165/payload.php` | LOW |
| URL | `http://44.99.114.120/payload.php` | MEDIUM |
| IP | `209.28.137.13` | MEDIUM |
| SHA256 | `26b9d9e6177e207afd19d16f1e7930a162011654e10138df84910590768930bc` | MEDIUM |
| URL | `http://213.90.82.193/payload.php` | LOW |
| URL | `http://214.51.95.237/payload.php` | LOW |
| IP | `84.73.139.251` | HIGH |
| SHA256 | `e67ecda61b30abbfbc24e31f52ed801f68629001ffc30e6813df3e803f8c6f47` | LOW |
| SHA256 | `edab279be6dfe9c3fa8521546e04ca4cd9ff1b63ba2226fd4a34ee6d44172aa2` | LOW |
| SHA256 | `70cb686fbc5a6ed1e3dc6f8746617b8918bd8e269ffbe1b5813db93aaef42d00` | HIGH |
| Domain | `cdn54-update.pihdbf.com` | LOW |
| URL | `http://92.103.246.104/payload.php` | HIGH |
| IP | `198.110.68.236` | HIGH |
| Domain | `cdn38-update.mdjhlf.com` | MEDIUM |
| URL | `http://128.50.63.116/payload.php` | MEDIUM |
| SHA256 | `f52e5adff9c75a3bb27f84b2e6c5d5edb5ec0b7b7ff2a2eda0317a66b203e84f` | MEDIUM |
| SHA256 | `a23f775913511af3fd2da3a05a70b50000f73cd5aacc7f6ecb67878fc1b4832d` | MEDIUM |
| IP | `194.16.78.35` | MEDIUM |
| URL | `http://182.36.121.132/payload.php` | HIGH |
| IP | `112.240.125.171` | HIGH |
| IP | `150.167.104.210` | LOW |
| IP | `25.173.140.22` | HIGH |
| Domain | `cdn49-update.amlmop.com` | LOW |
| SHA256 | `1331f3a6b1a90805d5b2d8feda45cbeddbbb01a5b57c9c9f4a453b54ba39bfc8` | MEDIUM |
| URL | `http://11.162.219.238/payload.php` | HIGH |
| Domain | `cdn84-update.ccnkgn.com` | HIGH |
| URL | `http://132.108.41.245/payload.php` | MEDIUM |
| Domain | `cdn58-update.omclbh.com` | MEDIUM |
| Domain | `cdn27-update.jdmhgj.com` | LOW |
| SHA256 | `78dce1af9f756a6a4fc2049a19adff54a5e4e18f9cf36d651b22e7e492cf4adf` | LOW |
| Domain | `cdn15-update.fhnfmg.com` | HIGH |
| SHA256 | `6afb798410a9a15a9cefb8a96bcd9f8f92c8e6f9724a9d95e0d227e1db6ede68` | MEDIUM |
| Domain | `cdn87-update.efcdni.com` | MEDIUM |
| SHA256 | `fb9ef80ccb57b343df4972af3f71232eb7bc9661b6e67a738c73df0d3d816acc` | MEDIUM |
| URL | `http://59.178.22.136/payload.php` | MEDIUM |
| IP | `18.247.163.132` | LOW |
| Domain | `cdn16-update.kkieba.com` | MEDIUM |
| IP | `134.27.172.253` | LOW |
| Domain | `cdn29-update.npdean.com` | LOW |
| IP | `58.75.54.145` | MEDIUM |
| IP | `144.156.252.96` | HIGH |
| Domain | `cdn54-update.iillmd.com` | LOW |
| Domain | `cdn79-update.dhgjhf.com` | LOW |
| SHA256 | `ccfd84db73c53697b719d376691ec48d28b66a7bec4fa3e0b6f250faf1ec4c2a` | HIGH |

