# Corporate Network Topology — Internal Reference — Confidential

## VLAN Table

| VLAN ID | Name | Subnet | Gateway | Purpose |
|---------|------|--------|---------|---------|
| 100 | USERS | 10.10.0.0/24 | 10.10.0.1 | Users traffic |
| 110 | SERVERS | 10.11.0.0/24 | 10.11.0.1 | Servers traffic |
| 120 | DMZ | 10.12.0.0/24 | 10.12.0.1 | Dmz traffic |
| 130 | MGMT | 10.13.0.0/24 | 10.13.0.1 | Mgmt traffic |
| 140 | VOICE | 10.14.0.0/24 | 10.14.0.1 | Voice traffic |
| 150 | GUEST | 10.15.0.0/24 | 10.15.0.1 | Guest traffic |
| 160 | IOT | 10.16.0.0/24 | 10.16.0.1 | Iot traffic |
| 170 | STORAGE | 10.17.0.0/24 | 10.17.0.1 | Storage traffic |
| 180 | BACKUP | 10.18.0.0/24 | 10.18.0.1 | Backup traffic |
| 190 | MONITORING | 10.19.0.0/24 | 10.19.0.1 | Monitoring traffic |
| 200 | QUARANTINE | 10.20.0.0/24 | 10.20.0.1 | Quarantine traffic |

## Device Inventory

| Hostname | IP | MAC | Role | OS | Managed |
|----------|----|-----|------|----|---------|
| host-000 | 10.30.1.19 | f9:09:dd:cb:de:18 | workstation | Firmware | NO |
| host-001 | 10.68.0.155 | 28:97:7a:83:78:4e | switch | macOS 14 | YES |
| host-002 | 10.33.1.209 | 09:a1:61:02:4b:a6 | router | RHEL 9 | YES |
| host-003 | 10.59.0.13 | da:5e:55:ed:58:26 | printer | Firmware | NO |
| host-004 | 10.29.4.40 | 26:8c:9c:52:81:f8 | camera | Windows 11 | YES |
| host-005 | 10.92.3.228 | ec:83:09:6b:d5:64 | printer | macOS 14 | YES |
| host-006 | 10.45.3.109 | 89:09:54:55:f6:1a | printer | Ubuntu 22.04 | YES |
| host-007 | 10.31.4.65 | 32:5f:c0:df:21:84 | camera | Ubuntu 22.04 | YES |
| host-008 | 10.104.4.205 | 8d:47:50:dd:29:2b | router | Ubuntu 22.04 | NO |
| host-009 | 10.21.0.198 | 92:0c:53:8e:87:d6 | switch | Firmware | YES |
| host-010 | 10.50.1.205 | dd:20:a1:4b:92:e5 | printer | RHEL 9 | YES |
| host-011 | 10.50.2.60 | 50:69:d8:78:8d:00 | router | RHEL 9 | YES |
| host-012 | 10.77.4.208 | a2:bf:a4:4c:99:4b | router | Firmware | NO |
| host-013 | 10.30.4.13 | 25:01:dc:81:8c:08 | camera | Windows 11 | NO |
| host-014 | 10.59.0.155 | 93:60:49:59:39:40 | router | Firmware | YES |
| host-015 | 10.50.3.80 | 1d:5b:90:25:91:d6 | workstation | Ubuntu 22.04 | YES |
| host-016 | 10.11.4.183 | b0:75:f3:7e:44:b4 | router | macOS 14 | NO |
| host-017 | 10.17.5.101 | 54:d3:f7:8c:d5:bd | server | macOS 14 | YES |
| host-018 | 10.105.5.22 | dd:e3:41:bc:f3:b5 | workstation | Ubuntu 22.04 | NO |
| host-019 | 10.73.5.74 | 17:8e:75:ff:da:4d | switch | macOS 14 | YES |
| host-020 | 10.39.4.119 | 16:68:da:ab:91:ac | camera | Firmware | NO |
| host-021 | 10.77.1.83 | 2c:14:40:f2:67:cc | switch | macOS 14 | NO |
| host-022 | 10.96.4.120 | 8f:e9:9a:20:c0:e2 | camera | Windows 11 | YES |
| host-023 | 10.108.0.143 | 57:30:e9:aa:a6:d0 | switch | macOS 14 | NO |
| host-024 | 10.27.5.70 | c4:c2:8b:e6:0b:e9 | camera | macOS 14 | NO |
| host-025 | 10.37.1.126 | 51:96:82:91:9c:dd | switch | Ubuntu 22.04 | NO |
| host-026 | 10.45.2.121 | 55:b2:88:b2:f2:7a | camera | Firmware | YES |
| host-027 | 10.86.5.124 | 65:12:7a:21:ea:8d | workstation | RHEL 9 | YES |
| host-028 | 10.37.4.131 | 63:4a:6a:f7:ad:ef | printer | Ubuntu 22.04 | NO |
| host-029 | 10.40.5.49 | 46:33:ae:7b:49:82 | server | Windows 11 | NO |
| host-030 | 10.26.0.115 | 4d:d2:3c:c8:14:bf | printer | Firmware | YES |
| host-031 | 10.91.0.132 | be:a9:3f:17:8d:08 | printer | Windows 11 | YES |
| host-032 | 10.89.5.122 | 02:74:c2:aa:19:56 | router | Windows 11 | NO |
| host-033 | 10.99.2.206 | 17:0a:32:98:20:c3 | router | Ubuntu 22.04 | NO |
| host-034 | 10.52.1.44 | ea:82:30:6a:c4:3a | server | macOS 14 | NO |
| host-035 | 10.71.4.232 | 35:43:3f:1e:c6:36 | router | Firmware | NO |
| host-036 | 10.70.5.134 | ad:ec:62:2e:83:05 | server | macOS 14 | YES |
| host-037 | 10.77.4.186 | 6a:75:5d:0b:93:a5 | printer | macOS 14 | YES |
| host-038 | 10.48.2.254 | 6b:8d:fd:e6:ff:b9 | workstation | Windows 11 | YES |
| host-039 | 10.49.5.143 | 5b:ad:ae:c5:c4:91 | workstation | RHEL 9 | YES |
| host-040 | 10.58.5.4 | e6:2b:69:0a:e1:60 | printer | macOS 14 | NO |
| host-041 | 10.81.4.201 | 1a:0b:0b:2a:8d:56 | server | Firmware | YES |
| host-042 | 10.55.2.245 | 5d:25:6f:fd:d2:63 | switch | macOS 14 | NO |
| host-043 | 10.36.0.239 | 24:b3:36:2d:b0:52 | workstation | macOS 14 | NO |
| host-044 | 10.93.0.53 | 3f:ed:1b:1b:0b:c5 | server | macOS 14 | NO |
| host-045 | 10.54.1.162 | 58:51:31:1f:4d:c8 | printer | RHEL 9 | NO |
| host-046 | 10.39.4.123 | a0:b2:ee:53:7a:bf | server | Windows 11 | YES |
| host-047 | 10.79.0.218 | 18:8d:dd:8d:79:a0 | switch | Firmware | YES |
| host-048 | 10.67.3.47 | bd:7e:82:54:5d:9b | server | RHEL 9 | NO |
| host-049 | 10.101.3.128 | 2b:38:b8:97:44:43 | printer | Windows 11 | YES |
| host-050 | 10.21.0.169 | a5:68:81:f3:df:4e | camera | Windows 11 | YES |
| host-051 | 10.27.4.110 | 1d:0b:18:03:85:96 | server | Firmware | YES |
| host-052 | 10.98.2.145 | 68:90:0e:0c:ab:33 | server | Ubuntu 22.04 | YES |
| host-053 | 10.79.5.87 | 8c:9f:b0:0a:b5:b6 | server | macOS 14 | NO |
| host-054 | 10.65.2.136 | 0d:95:ae:5d:19:7b | switch | RHEL 9 | NO |
| host-055 | 10.40.4.230 | 7c:0c:94:b5:40:9e | router | Windows 11 | NO |
| host-056 | 10.57.1.134 | 77:e5:5e:86:90:e1 | workstation | Ubuntu 22.04 | NO |
| host-057 | 10.26.3.44 | 1e:90:03:1e:9e:e3 | printer | macOS 14 | NO |
| host-058 | 10.60.2.166 | fb:48:64:1a:30:7d | switch | macOS 14 | YES |
| host-059 | 10.58.3.185 | ee:72:5f:09:9f:1e | printer | Windows 11 | NO |
| host-060 | 10.84.0.116 | 9c:9b:16:5b:dd:44 | server | Windows 11 | NO |
| host-061 | 10.67.3.102 | 08:86:3e:f2:38:22 | router | Windows 11 | NO |
| host-062 | 10.76.1.180 | 98:44:b1:04:99:92 | camera | macOS 14 | YES |
| host-063 | 10.79.2.98 | c7:40:ac:3b:00:b4 | switch | Ubuntu 22.04 | YES |
| host-064 | 10.88.5.241 | 80:42:66:ee:0d:99 | switch | Firmware | NO |
| host-065 | 10.81.0.4 | 8c:91:db:78:0f:33 | switch | macOS 14 | NO |
| host-066 | 10.70.1.59 | 2b:dd:d8:f9:73:95 | router | Ubuntu 22.04 | YES |
| host-067 | 10.94.4.173 | 57:88:c2:5c:e7:52 | workstation | macOS 14 | NO |
| host-068 | 10.99.1.54 | 92:8a:5a:80:cc:32 | server | Windows 11 | YES |
| host-069 | 10.84.1.150 | 25:46:20:d2:ab:ba | switch | RHEL 9 | YES |
| host-070 | 10.47.1.252 | cb:77:13:ea:c4:8c | printer | Ubuntu 22.04 | YES |
| host-071 | 10.110.4.87 | db:d1:4d:cf:9b:7e | workstation | Ubuntu 22.04 | NO |
| host-072 | 10.90.2.94 | 9c:eb:7b:e1:9b:d1 | camera | RHEL 9 | NO |
| host-073 | 10.83.0.31 | 1b:0d:23:db:49:47 | router | Firmware | YES |
| host-074 | 10.26.1.189 | 11:d5:db:11:61:17 | camera | Firmware | YES |
| host-075 | 10.81.4.132 | 2c:38:d6:75:96:93 | printer | macOS 14 | YES |
| host-076 | 10.23.1.3 | ac:02:52:e5:3e:a1 | server | RHEL 9 | NO |
| host-077 | 10.10.2.139 | 1f:cf:3b:00:fa:51 | printer | macOS 14 | YES |
| host-078 | 10.50.0.147 | 66:12:62:fe:78:04 | printer | Windows 11 | YES |
| host-079 | 10.75.2.1 | 56:d4:46:32:48:79 | workstation | Ubuntu 22.04 | YES |
| host-080 | 10.51.2.199 | 1f:86:93:c5:ae:a6 | server | Windows 11 | NO |
| host-081 | 10.97.1.111 | dd:b1:a1:09:df:8d | printer | RHEL 9 | NO |
| host-082 | 10.54.4.207 | 38:8c:45:2f:25:14 | camera | Firmware | YES |
| host-083 | 10.10.2.89 | bb:62:ed:e4:7f:e4 | workstation | Firmware | NO |
| host-084 | 10.23.1.101 | 73:ac:dd:49:e8:70 | workstation | Windows 11 | YES |
| host-085 | 10.69.1.153 | 16:a6:a1:0b:37:7d | router | Firmware | NO |
| host-086 | 10.81.0.54 | 00:f2:cb:2f:f7:5e | server | macOS 14 | YES |
| host-087 | 10.70.0.114 | fd:a6:ef:ac:72:5a | server | Ubuntu 22.04 | NO |
| host-088 | 10.44.4.53 | e1:13:1b:50:61:16 | workstation | Windows 11 | NO |
| host-089 | 10.10.3.31 | bb:23:60:0a:42:0a | router | RHEL 9 | YES |
| host-090 | 10.44.4.73 | 5a:04:27:ed:50:9f | switch | Firmware | YES |
| host-091 | 10.91.0.223 | 7f:0f:db:d1:7f:aa | camera | RHEL 9 | YES |
| host-092 | 10.69.2.41 | a9:fa:dc:04:9d:53 | router | Windows 11 | YES |
| host-093 | 10.26.1.64 | e8:38:0a:08:9d:47 | server | Windows 11 | NO |
| host-094 | 10.18.0.89 | aa:1e:10:05:03:72 | router | Windows 11 | NO |
| host-095 | 10.10.3.50 | ff:ab:7b:33:34:cd | camera | RHEL 9 | NO |
| host-096 | 10.24.5.164 | 20:11:5c:89:b3:cf | workstation | Firmware | NO |
| host-097 | 10.13.0.82 | 5e:28:3a:b9:9f:25 | router | Ubuntu 22.04 | NO |
| host-098 | 10.53.2.140 | 07:10:72:e6:25:a1 | camera | Firmware | NO |
| host-099 | 10.102.3.153 | 3c:c6:bb:81:11:63 | printer | Firmware | YES |
| host-100 | 10.12.0.87 | dd:b5:44:85:b1:02 | router | Firmware | YES |
| host-101 | 10.16.3.8 | 00:5a:91:74:b6:74 | server | RHEL 9 | NO |
| host-102 | 10.74.5.73 | 9b:94:19:93:fe:31 | server | macOS 14 | YES |
| host-103 | 10.104.0.42 | 3e:ef:b9:08:f9:42 | workstation | Ubuntu 22.04 | YES |
| host-104 | 10.58.1.117 | 89:01:8c:6a:99:68 | workstation | Ubuntu 22.04 | YES |
| host-105 | 10.63.0.27 | a6:c7:eb:be:97:a2 | router | macOS 14 | NO |
| host-106 | 10.100.5.36 | 62:09:39:9f:aa:87 | camera | Firmware | YES |
| host-107 | 10.46.2.38 | 37:5f:e7:d9:8a:2e | printer | macOS 14 | NO |
| host-108 | 10.46.0.213 | 3a:0a:bf:28:92:81 | camera | Firmware | YES |
| host-109 | 10.52.3.134 | 2f:3e:ff:91:72:a5 | printer | macOS 14 | NO |
| host-110 | 10.108.3.81 | 29:3b:7d:98:93:5f | switch | Windows 11 | NO |
| host-111 | 10.43.4.151 | 62:ed:f6:86:16:6d | switch | RHEL 9 | YES |
| host-112 | 10.45.3.66 | e8:e9:64:0d:09:a6 | printer | Firmware | YES |
| host-113 | 10.82.4.218 | a5:ac:1e:49:94:30 | printer | Windows 11 | YES |
| host-114 | 10.53.2.233 | 31:13:4c:ea:b3:2b | printer | macOS 14 | YES |
| host-115 | 10.50.2.201 | 64:cf:f7:70:eb:c7 | printer | Windows 11 | YES |
| host-116 | 10.44.2.222 | e9:9e:78:1b:43:64 | workstation | Windows 11 | NO |
| host-117 | 10.63.0.55 | 02:86:99:79:a6:8c | printer | Ubuntu 22.04 | YES |
| host-118 | 10.82.2.138 | a0:0d:f9:ff:6f:b2 | workstation | Windows 11 | YES |
| host-119 | 10.11.1.243 | 87:b9:ab:27:ed:bd | switch | Windows 11 | YES |
| host-120 | 10.76.1.104 | 25:15:01:c8:ba:f0 | printer | RHEL 9 | YES |
| host-121 | 10.42.1.176 | 9a:b3:a0:17:be:e7 | switch | Firmware | YES |
| host-122 | 10.54.4.19 | 03:fe:b8:b3:ce:5f | router | Firmware | YES |
| host-123 | 10.42.4.15 | 0c:c0:27:57:3f:5a | printer | Ubuntu 22.04 | NO |
| host-124 | 10.83.3.206 | 1b:60:c2:00:79:c9 | camera | Windows 11 | YES |
| host-125 | 10.40.4.4 | e5:16:24:1b:3e:9c | switch | macOS 14 | YES |
| host-126 | 10.22.1.197 | 40:41:7d:90:ae:a6 | printer | Firmware | YES |
| host-127 | 10.68.3.107 | aa:3e:5b:72:73:59 | router | Ubuntu 22.04 | YES |
| host-128 | 10.62.2.75 | c7:15:5f:76:eb:eb | workstation | RHEL 9 | YES |
| host-129 | 10.83.1.222 | ed:b0:14:e5:0b:1c | server | macOS 14 | YES |
| host-130 | 10.50.5.92 | db:e2:6d:9c:32:42 | router | macOS 14 | YES |
| host-131 | 10.71.2.20 | 4f:1f:8b:e8:68:3a | workstation | Ubuntu 22.04 | YES |
| host-132 | 10.29.1.209 | 54:08:67:74:66:06 | router | macOS 14 | NO |
| host-133 | 10.32.4.151 | 2c:bf:64:5d:a2:3c | switch | Ubuntu 22.04 | NO |
| host-134 | 10.36.1.181 | 52:4b:1a:c6:0f:fc | switch | Ubuntu 22.04 | NO |
| host-135 | 10.36.1.211 | 9c:b8:f8:6d:54:e6 | router | macOS 14 | YES |
| host-136 | 10.85.1.206 | f5:d6:22:74:5d:79 | camera | Windows 11 | YES |
| host-137 | 10.48.3.205 | 9d:c3:21:d5:52:22 | camera | Windows 11 | YES |
| host-138 | 10.27.5.243 | 51:b7:0b:f2:19:61 | workstation | macOS 14 | YES |
| host-139 | 10.39.3.60 | 4b:91:00:66:96:76 | switch | Firmware | NO |
| host-140 | 10.51.0.157 | 12:ce:24:95:81:56 | camera | macOS 14 | YES |
| host-141 | 10.75.3.39 | aa:26:46:6b:f6:74 | server | Firmware | NO |
| host-142 | 10.70.1.58 | 02:19:99:48:99:d3 | workstation | Windows 11 | NO |
| host-143 | 10.53.1.78 | ec:c8:fe:3f:83:d0 | camera | RHEL 9 | YES |
| host-144 | 10.69.5.205 | d0:b1:03:1f:60:af | router | Windows 11 | YES |
| host-145 | 10.13.1.173 | 01:78:9d:37:8f:1e | printer | RHEL 9 | NO |
| host-146 | 10.104.5.94 | 0f:4a:a1:10:97:94 | workstation | Firmware | YES |
| host-147 | 10.12.3.78 | 5d:40:e0:2d:fe:b5 | router | Windows 11 | YES |
| host-148 | 10.17.1.243 | 97:47:9b:da:26:73 | server | Firmware | NO |
| host-149 | 10.106.3.176 | d6:34:ad:78:8f:ea | server | Windows 11 | NO |
| host-150 | 10.109.2.172 | 93:1e:7b:42:5c:25 | workstation | Ubuntu 22.04 | YES |
| host-151 | 10.103.2.245 | 5d:cc:e5:b9:43:d5 | camera | macOS 14 | NO |
| host-152 | 10.74.1.237 | 61:03:8c:6b:7a:d3 | camera | Ubuntu 22.04 | NO |
| host-153 | 10.22.4.220 | d5:ce:9c:5e:a0:d4 | printer | RHEL 9 | NO |
| host-154 | 10.35.2.64 | e4:4f:f5:dc:75:49 | server | macOS 14 | NO |
| host-155 | 10.52.3.48 | 8d:45:b2:d9:54:9f | server | Firmware | NO |
| host-156 | 10.16.2.67 | f7:fc:c1:1e:ed:fe | printer | macOS 14 | YES |
| host-157 | 10.39.4.182 | 3d:c2:25:38:8c:87 | server | Firmware | NO |
| host-158 | 10.73.1.217 | c0:e2:21:24:ae:e8 | switch | Ubuntu 22.04 | NO |
| host-159 | 10.21.5.168 | 00:d4:20:83:e4:53 | camera | Firmware | YES |
| host-160 | 10.84.5.23 | c4:35:70:0b:67:a4 | router | Windows 11 | YES |
| host-161 | 10.49.4.218 | b8:9b:00:0f:ff:da | router | macOS 14 | NO |
| host-162 | 10.69.1.71 | c4:11:56:e3:0c:2c | server | Windows 11 | YES |
| host-163 | 10.28.2.197 | 2d:c7:73:ab:4f:21 | camera | Firmware | YES |
| host-164 | 10.20.5.18 | 22:ae:57:9c:b3:df | workstation | Firmware | YES |
| host-165 | 10.80.1.105 | c5:1c:bf:10:6d:0d | switch | Windows 11 | YES |
| host-166 | 10.45.0.130 | f1:5b:8e:f6:7f:2e | server | macOS 14 | YES |
| host-167 | 10.93.2.73 | cd:65:32:60:2c:82 | server | Firmware | NO |
| host-168 | 10.31.0.205 | 63:e6:5c:db:2b:c7 | router | macOS 14 | NO |
| host-169 | 10.47.1.114 | 84:89:2e:45:1a:5c | switch | RHEL 9 | NO |
| host-170 | 10.65.1.205 | b8:bf:5b:e0:ed:82 | server | Ubuntu 22.04 | YES |
| host-171 | 10.22.1.138 | 41:5c:48:e2:6a:81 | workstation | Ubuntu 22.04 | NO |
| host-172 | 10.28.0.179 | 04:87:58:21:e8:99 | switch | Ubuntu 22.04 | NO |
| host-173 | 10.23.2.57 | 13:f2:c5:28:3e:5d | switch | RHEL 9 | NO |
| host-174 | 10.32.5.131 | 25:a5:b2:09:17:0d | server | Ubuntu 22.04 | NO |
| host-175 | 10.29.5.252 | d3:eb:a4:50:dc:c5 | workstation | macOS 14 | NO |
| host-176 | 10.107.2.120 | 7e:4d:bf:54:2e:02 | switch | RHEL 9 | YES |
| host-177 | 10.93.0.71 | 4e:01:69:3d:be:01 | switch | Ubuntu 22.04 | NO |
| host-178 | 10.97.3.98 | 6c:50:82:75:06:07 | server | Windows 11 | NO |
| host-179 | 10.36.4.159 | 4e:32:be:c3:61:a1 | camera | Ubuntu 22.04 | NO |
| host-180 | 10.59.1.183 | 22:64:08:97:d5:df | router | RHEL 9 | YES |
| host-181 | 10.98.1.65 | b6:ec:8a:2c:ab:e7 | printer | RHEL 9 | NO |
| host-182 | 10.82.4.243 | 97:92:d8:c9:ae:dd | router | Ubuntu 22.04 | YES |
| host-183 | 10.75.2.199 | 7a:81:44:60:08:93 | server | Firmware | NO |
| host-184 | 10.28.2.62 | 80:a0:17:bf:f8:c9 | switch | Windows 11 | NO |
| host-185 | 10.106.4.212 | c6:ee:91:10:8b:e6 | workstation | Windows 11 | NO |
| host-186 | 10.88.5.244 | c0:c5:50:32:af:71 | router | Ubuntu 22.04 | YES |
| host-187 | 10.82.5.34 | 81:b3:a2:a7:58:a7 | workstation | RHEL 9 | YES |
| host-188 | 10.95.5.171 | 4e:33:e2:c9:b1:2d | printer | macOS 14 | NO |
| host-189 | 10.110.1.88 | f3:e1:74:a0:7c:10 | router | Windows 11 | YES |
| host-190 | 10.45.1.124 | ac:ed:07:90:5d:5a | router | Windows 11 | NO |
| host-191 | 10.12.3.74 | b2:99:76:22:6a:c6 | camera | Windows 11 | YES |
| host-192 | 10.82.2.26 | 00:ce:0f:23:7d:1a | camera | Ubuntu 22.04 | YES |
| host-193 | 10.18.1.201 | 8f:02:95:84:01:71 | switch | RHEL 9 | NO |
| host-194 | 10.83.2.42 | 35:3c:63:7c:19:23 | camera | RHEL 9 | NO |
| host-195 | 10.48.4.196 | 37:00:79:7c:50:06 | camera | macOS 14 | NO |
| host-196 | 10.58.0.248 | 3f:64:bf:64:08:af | workstation | macOS 14 | NO |
| host-197 | 10.87.1.130 | f3:a3:31:4a:b4:9d | switch | Windows 11 | YES |
| host-198 | 10.71.2.38 | 4b:62:0b:82:4e:30 | workstation | Firmware | NO |
| host-199 | 10.64.3.105 | 10:a4:8c:8b:df:14 | printer | macOS 14 | YES |
| host-200 | 10.25.3.172 | 5f:c8:87:9f:df:c8 | server | RHEL 9 | YES |
| host-201 | 10.34.5.215 | 49:62:13:70:82:82 | camera | Firmware | NO |
| host-202 | 10.11.4.145 | 26:df:bc:2c:c3:fd | server | RHEL 9 | YES |
| host-203 | 10.32.3.95 | c1:be:41:aa:2e:78 | camera | macOS 14 | YES |
| host-204 | 10.32.0.254 | 0d:85:f8:03:4c:66 | workstation | RHEL 9 | YES |
| host-205 | 10.69.0.55 | 1d:73:d6:8f:94:c5 | workstation | Ubuntu 22.04 | NO |
| host-206 | 10.66.1.241 | 74:0b:d3:00:10:e4 | workstation | macOS 14 | NO |
| host-207 | 10.89.5.39 | d0:82:c6:24:92:ff | server | Ubuntu 22.04 | NO |
| host-208 | 10.76.2.138 | 29:c9:9e:10:2d:3b | camera | Ubuntu 22.04 | YES |
| host-209 | 10.32.2.80 | e9:49:0e:ec:4c:29 | printer | macOS 14 | NO |
| host-210 | 10.108.1.79 | 9c:8d:d2:1d:9f:b3 | printer | Windows 11 | YES |
| host-211 | 10.54.5.245 | 4f:66:7f:5b:cc:bb | workstation | Firmware | YES |
| host-212 | 10.78.4.208 | f3:bd:3f:d6:e4:fb | router | Windows 11 | NO |
| host-213 | 10.68.0.208 | b7:cc:88:3d:13:60 | server | Ubuntu 22.04 | YES |
| host-214 | 10.52.3.37 | 3c:23:55:4c:a0:ff | workstation | Ubuntu 22.04 | NO |
| host-215 | 10.85.2.24 | b7:d2:7a:33:f6:17 | camera | Firmware | YES |
| host-216 | 10.57.4.77 | 71:0c:48:e4:10:fa | workstation | Windows 11 | NO |
| host-217 | 10.51.0.37 | bb:b4:51:85:c2:5d | switch | macOS 14 | NO |
| host-218 | 10.28.0.215 | 6d:1d:53:84:52:1b | camera | macOS 14 | YES |
| host-219 | 10.86.5.174 | b3:1a:a1:6b:ed:85 | workstation | macOS 14 | NO |
| host-220 | 10.81.2.146 | 10:0d:12:03:e3:9f | router | RHEL 9 | NO |
| host-221 | 10.44.1.42 | de:3a:7f:5e:83:94 | server | Firmware | NO |
| host-222 | 10.63.4.84 | e9:80:0a:f6:03:a2 | workstation | RHEL 9 | NO |
| host-223 | 10.94.2.207 | 7b:cf:9b:f4:42:2f | server | Ubuntu 22.04 | NO |
| host-224 | 10.71.4.129 | 00:54:0d:4f:51:bf | server | Windows 11 | NO |
| host-225 | 10.102.3.162 | ae:de:54:58:9d:86 | server | Ubuntu 22.04 | NO |
| host-226 | 10.32.2.187 | dc:71:68:56:72:90 | router | macOS 14 | NO |
| host-227 | 10.72.3.247 | d4:b3:d5:2c:a6:eb | router | Firmware | YES |
| host-228 | 10.41.2.156 | ba:f8:0a:05:0e:f8 | camera | RHEL 9 | YES |
| host-229 | 10.67.3.152 | 3e:5c:49:9b:e2:00 | switch | Windows 11 | YES |
| host-230 | 10.79.3.24 | b1:59:42:ff:4f:9e | camera | Firmware | NO |
| host-231 | 10.78.1.83 | a3:59:a1:5e:11:31 | router | RHEL 9 | YES |
| host-232 | 10.65.5.208 | fa:1a:f8:a2:f3:7c | server | macOS 14 | YES |
| host-233 | 10.105.3.69 | ca:97:40:76:60:55 | workstation | macOS 14 | NO |
| host-234 | 10.15.3.233 | c0:86:3d:a7:da:17 | workstation | Ubuntu 22.04 | YES |
| host-235 | 10.50.0.12 | b9:28:58:92:1f:76 | workstation | macOS 14 | NO |
| host-236 | 10.59.0.248 | c4:98:60:88:4c:b0 | workstation | Ubuntu 22.04 | NO |
| host-237 | 10.67.5.77 | 40:1c:d4:13:3e:33 | camera | macOS 14 | NO |
| host-238 | 10.15.3.65 | f4:d6:7a:e6:5f:f0 | workstation | RHEL 9 | YES |
| host-239 | 10.68.0.172 | 77:b8:fd:2c:d1:dc | server | macOS 14 | YES |
| host-240 | 10.108.5.150 | 2f:b7:08:46:0b:8a | camera | Ubuntu 22.04 | NO |
| host-241 | 10.37.0.176 | 4e:1f:9c:7f:2c:51 | router | Firmware | NO |
| host-242 | 10.96.1.101 | 0a:5c:a4:56:f2:f1 | switch | Windows 11 | YES |
| host-243 | 10.63.4.42 | 35:f0:b2:51:85:54 | router | Windows 11 | NO |
| host-244 | 10.19.3.225 | 45:9a:32:4d:b1:69 | switch | RHEL 9 | YES |
| host-245 | 10.82.4.171 | 54:c5:e6:b6:ae:55 | workstation | Windows 11 | YES |
| host-246 | 10.69.5.144 | f5:61:ae:c3:d8:57 | workstation | RHEL 9 | NO |
| host-247 | 10.64.1.206 | 9c:af:25:a7:58:be | server | Windows 11 | YES |
| host-248 | 10.59.4.85 | f4:6c:b9:c5:28:40 | workstation | RHEL 9 | NO |
| host-249 | 10.85.1.161 | 72:2b:75:0a:b3:88 | server | RHEL 9 | NO |
| host-250 | 10.108.3.207 | cc:75:b9:dd:ba:cc | switch | Windows 11 | NO |
| host-251 | 10.56.3.163 | 18:8a:5c:a7:2b:26 | workstation | Windows 11 | NO |
| host-252 | 10.58.3.79 | 97:9a:35:60:55:5c | camera | Firmware | NO |
| host-253 | 10.59.2.123 | ff:e8:60:ce:13:e6 | workstation | macOS 14 | NO |
| host-254 | 10.40.5.157 | cd:23:ef:1f:e8:49 | camera | macOS 14 | NO |
| host-255 | 10.55.3.234 | b1:c1:b6:52:5b:9b | printer | macOS 14 | YES |
| host-256 | 10.30.3.117 | 4b:cb:3e:ed:10:be | server | macOS 14 | NO |
| host-257 | 10.80.5.218 | ad:61:4f:cb:a3:d1 | printer | RHEL 9 | NO |
| host-258 | 10.21.0.106 | 2e:46:5e:3e:7b:8e | camera | Firmware | NO |
| host-259 | 10.53.4.16 | dc:cf:18:76:79:34 | printer | macOS 14 | NO |
| host-260 | 10.72.0.38 | f0:3c:c3:cf:b7:6c | printer | RHEL 9 | YES |
| host-261 | 10.71.3.61 | 74:bf:cb:27:ba:f5 | router | Ubuntu 22.04 | NO |
| host-262 | 10.46.3.196 | 02:ab:20:93:27:0c | workstation | Ubuntu 22.04 | YES |
| host-263 | 10.79.1.67 | 44:5a:68:93:2d:14 | workstation | Ubuntu 22.04 | YES |
| host-264 | 10.85.1.219 | 1c:c3:d8:b4:8b:8f | workstation | Windows 11 | NO |
| host-265 | 10.12.3.100 | b3:e9:b4:81:75:86 | workstation | Ubuntu 22.04 | YES |
| host-266 | 10.43.3.37 | 07:e1:8e:a6:70:f6 | camera | macOS 14 | NO |
| host-267 | 10.22.4.139 | e4:46:84:17:9f:d5 | server | RHEL 9 | NO |
| host-268 | 10.84.2.217 | 42:05:35:7c:47:df | printer | RHEL 9 | NO |
| host-269 | 10.92.0.101 | bd:eb:b2:1b:85:66 | camera | Windows 11 | YES |
| host-270 | 10.24.2.43 | 23:82:5d:94:8f:aa | workstation | Firmware | NO |
| host-271 | 10.60.2.178 | 6a:84:18:28:14:68 | switch | macOS 14 | NO |
| host-272 | 10.106.4.248 | e0:b3:f2:ca:a2:9f | printer | Ubuntu 22.04 | NO |
| host-273 | 10.94.0.130 | d9:8d:35:04:7b:02 | switch | Windows 11 | NO |
| host-274 | 10.50.1.223 | 0a:bf:07:4c:12:3a | router | Firmware | NO |
| host-275 | 10.24.5.253 | a6:8f:c9:53:a9:6c | camera | Windows 11 | NO |
| host-276 | 10.23.1.73 | 60:4a:ec:bf:05:91 | printer | RHEL 9 | NO |
| host-277 | 10.78.5.238 | e2:d0:1a:07:3e:9c | router | Ubuntu 22.04 | YES |
| host-278 | 10.53.5.197 | 07:e1:ef:21:f7:6c | server | Ubuntu 22.04 | YES |
| host-279 | 10.36.4.28 | fc:eb:39:cc:8c:4e | router | RHEL 9 | NO |
| host-280 | 10.64.4.166 | fa:03:74:f3:d3:b3 | server | RHEL 9 | NO |
| host-281 | 10.105.5.57 | 90:21:0a:5c:fc:6c | camera | Ubuntu 22.04 | NO |
| host-282 | 10.68.3.67 | 92:10:48:d9:01:66 | camera | macOS 14 | YES |
| host-283 | 10.20.1.138 | 36:64:fe:04:e8:59 | router | Firmware | YES |
| host-284 | 10.27.1.121 | a5:78:f6:19:ee:1c | server | Firmware | NO |
| host-285 | 10.28.3.231 | 57:cd:1f:5f:24:85 | workstation | RHEL 9 | NO |
| host-286 | 10.44.0.98 | d6:26:fb:25:9c:98 | printer | macOS 14 | NO |
| host-287 | 10.103.0.157 | 20:0b:82:5b:c9:11 | workstation | Windows 11 | NO |
| host-288 | 10.42.4.187 | 3c:9e:88:e6:05:26 | workstation | Firmware | NO |
| host-289 | 10.15.1.5 | 57:93:06:98:38:dd | printer | Windows 11 | NO |
| host-290 | 10.77.0.73 | 24:b3:06:85:f5:22 | switch | RHEL 9 | YES |
| host-291 | 10.79.5.221 | 5d:cd:a8:7a:53:3d | server | RHEL 9 | YES |
| host-292 | 10.13.4.42 | 49:64:cd:84:35:13 | router | macOS 14 | YES |
| host-293 | 10.59.1.242 | 22:e7:1f:56:2c:8a | camera | Windows 11 | YES |
| host-294 | 10.54.0.10 | f9:d7:7b:c5:19:fb | workstation | Windows 11 | NO |
| host-295 | 10.90.4.155 | 4b:09:81:64:cb:31 | camera | Windows 11 | YES |
| host-296 | 10.60.4.11 | ce:7a:90:5c:33:28 | workstation | Firmware | YES |
| host-297 | 10.28.5.247 | de:c2:06:1f:98:e3 | server | RHEL 9 | YES |
| host-298 | 10.53.5.169 | b1:f2:7e:f2:81:35 | printer | RHEL 9 | YES |
| host-299 | 10.104.5.189 | 3e:b1:fa:49:e5:f2 | server | Firmware | NO |
| host-300 | 10.78.5.108 | c1:bd:a3:42:3f:32 | printer | Windows 11 | YES |
| host-301 | 10.73.5.56 | d9:86:66:e7:60:6a | printer | RHEL 9 | NO |
| host-302 | 10.54.5.97 | 72:6e:86:6a:1e:72 | router | Ubuntu 22.04 | NO |
| host-303 | 10.55.4.248 | 36:c0:a4:4e:a8:17 | router | Firmware | NO |
| host-304 | 10.34.4.8 | 7f:3d:96:87:50:a9 | switch | Firmware | YES |
| host-305 | 10.12.3.200 | dd:93:8b:47:ab:3b | router | RHEL 9 | YES |
| host-306 | 10.39.2.220 | c4:3a:0f:a4:ba:7b | workstation | RHEL 9 | YES |
| host-307 | 10.38.4.135 | ae:bc:65:43:95:68 | printer | Firmware | YES |
| host-308 | 10.89.0.97 | 1d:45:a9:29:54:6f | switch | Ubuntu 22.04 | YES |
| host-309 | 10.110.0.219 | 5a:e2:6f:16:18:a2 | camera | Firmware | YES |
| host-310 | 10.51.0.28 | 8a:34:6e:27:9f:50 | workstation | Ubuntu 22.04 | YES |
| host-311 | 10.109.5.21 | 70:77:7c:e1:f4:51 | camera | Ubuntu 22.04 | YES |
| host-312 | 10.31.3.253 | 3a:27:9a:ab:02:6b | server | RHEL 9 | NO |
| host-313 | 10.22.5.9 | b9:1a:9a:c3:40:2e | printer | Firmware | YES |
| host-314 | 10.51.0.19 | 3a:5d:7e:f5:72:d8 | camera | RHEL 9 | NO |
| host-315 | 10.102.4.146 | 00:d9:00:6b:62:31 | server | Firmware | NO |
| host-316 | 10.71.1.70 | da:52:1e:f7:11:7d | switch | Ubuntu 22.04 | NO |
| host-317 | 10.52.4.76 | b1:2d:c9:26:ed:1e | workstation | Windows 11 | YES |
| host-318 | 10.51.4.196 | 20:ec:9f:bb:a6:85 | printer | macOS 14 | YES |
| host-319 | 10.104.3.5 | 63:68:1e:ca:c8:03 | camera | Ubuntu 22.04 | YES |
| host-320 | 10.29.0.165 | 84:cb:ec:4f:be:9a | server | Windows 11 | NO |
| host-321 | 10.18.1.105 | 15:37:3d:c1:be:d7 | router | Windows 11 | YES |
| host-322 | 10.10.1.137 | 7e:e2:7a:8e:45:c1 | router | Firmware | NO |
| host-323 | 10.63.0.229 | 82:31:03:cf:32:dc | printer | Ubuntu 22.04 | YES |
| host-324 | 10.61.5.58 | ef:8d:7b:5c:69:98 | printer | Firmware | YES |
| host-325 | 10.101.3.91 | c0:ac:a0:ec:5a:b1 | switch | macOS 14 | NO |
| host-326 | 10.39.0.88 | 20:00:c1:86:cc:6c | printer | Windows 11 | NO |
| host-327 | 10.74.2.136 | 07:90:95:02:b6:dd | router | RHEL 9 | YES |
| host-328 | 10.30.2.150 | 2c:d8:28:29:28:65 | router | Windows 11 | YES |
| host-329 | 10.19.5.192 | 01:5d:52:d8:23:03 | switch | Ubuntu 22.04 | NO |
| host-330 | 10.66.2.228 | 40:3b:a0:c5:35:25 | printer | macOS 14 | YES |
| host-331 | 10.90.5.106 | fe:9d:e7:6e:31:3f | switch | RHEL 9 | NO |
| host-332 | 10.13.1.134 | a3:1d:87:4a:d1:44 | printer | macOS 14 | NO |
| host-333 | 10.107.2.180 | 5c:e4:b9:98:3a:c2 | workstation | RHEL 9 | YES |
| host-334 | 10.30.0.3 | ed:29:9a:b0:d4:e9 | router | macOS 14 | YES |
| host-335 | 10.85.5.236 | 0d:33:9d:03:6f:07 | router | Windows 11 | YES |
| host-336 | 10.66.1.192 | 3c:5f:fc:30:96:e4 | printer | macOS 14 | NO |
| host-337 | 10.46.3.45 | be:c7:93:1e:87:4d | server | macOS 14 | NO |
| host-338 | 10.59.4.131 | 44:9b:dd:53:8f:4f | workstation | Ubuntu 22.04 | YES |
| host-339 | 10.109.2.153 | 5a:17:88:db:f8:17 | workstation | Ubuntu 22.04 | YES |
| host-340 | 10.76.4.87 | e4:4d:51:b8:cb:95 | switch | Windows 11 | YES |
| host-341 | 10.96.5.42 | c0:54:a4:e3:2c:8a | printer | Windows 11 | NO |
| host-342 | 10.64.2.185 | 81:98:2f:c9:b6:38 | switch | RHEL 9 | NO |
| host-343 | 10.92.2.252 | f5:98:62:3a:0a:72 | workstation | Windows 11 | YES |
| host-344 | 10.106.0.161 | 07:08:51:f3:b4:db | server | Firmware | YES |
| host-345 | 10.75.3.154 | b9:73:de:1e:1a:08 | camera | Windows 11 | YES |
| host-346 | 10.50.5.6 | d4:12:23:52:b0:3f | printer | macOS 14 | YES |
| host-347 | 10.27.0.50 | e1:6a:10:22:58:2a | server | Windows 11 | NO |
| host-348 | 10.47.0.12 | 3b:b9:90:12:21:14 | router | Windows 11 | NO |
| host-349 | 10.22.4.207 | 05:ad:4d:24:fb:52 | camera | Windows 11 | YES |
| host-350 | 10.105.5.51 | 01:af:1b:02:02:44 | router | Firmware | YES |
| host-351 | 10.101.2.153 | 0a:0a:93:98:2f:3b | server | Windows 11 | YES |
| host-352 | 10.41.4.212 | 4a:c0:0d:85:80:8a | server | Firmware | YES |
| host-353 | 10.48.1.173 | 37:18:62:ef:39:a1 | camera | RHEL 9 | YES |
| host-354 | 10.26.1.32 | fb:fd:72:bc:8b:7c | camera | Windows 11 | YES |
| host-355 | 10.70.0.191 | ba:9f:f4:8c:e0:27 | router | macOS 14 | NO |
| host-356 | 10.88.4.32 | 5c:36:eb:e8:76:04 | router | macOS 14 | NO |
| host-357 | 10.28.4.134 | 61:fc:52:ca:3c:e6 | switch | Ubuntu 22.04 | NO |
| host-358 | 10.53.5.24 | ef:94:49:30:87:aa | workstation | Firmware | NO |
| host-359 | 10.81.3.201 | f9:0a:a9:fd:e6:43 | server | macOS 14 | YES |
| host-360 | 10.27.3.235 | db:e5:e1:e6:0f:a6 | printer | macOS 14 | YES |
| host-361 | 10.23.1.149 | 69:ec:cd:b5:d1:07 | switch | Windows 11 | NO |
| host-362 | 10.37.2.115 | 58:04:f6:88:76:3d | router | Windows 11 | NO |
| host-363 | 10.33.2.162 | 17:2e:17:5b:f2:39 | switch | Ubuntu 22.04 | NO |
| host-364 | 10.89.5.119 | fb:ac:8f:5b:ee:28 | server | Firmware | NO |
| host-365 | 10.17.4.176 | 3a:97:d8:99:b2:bb | server | RHEL 9 | NO |
| host-366 | 10.12.3.25 | 67:10:e0:e0:c2:a7 | workstation | Windows 11 | NO |
| host-367 | 10.39.2.218 | bc:9a:18:80:de:11 | printer | Ubuntu 22.04 | NO |
| host-368 | 10.14.3.230 | 5d:8c:5b:4b:13:49 | camera | Ubuntu 22.04 | YES |
| host-369 | 10.82.3.220 | 19:15:9d:42:9b:f2 | switch | RHEL 9 | NO |
| host-370 | 10.44.1.249 | bf:8d:0f:e7:61:8c | switch | Ubuntu 22.04 | NO |
| host-371 | 10.79.5.79 | c8:19:ea:99:74:f3 | router | Firmware | YES |
| host-372 | 10.81.5.127 | d7:6c:76:5d:c8:4e | server | Ubuntu 22.04 | YES |
| host-373 | 10.70.1.224 | 13:b6:5a:97:09:09 | camera | RHEL 9 | YES |
| host-374 | 10.108.5.197 | 45:cb:b4:f1:40:63 | workstation | Ubuntu 22.04 | NO |
| host-375 | 10.91.0.208 | d2:45:3b:d4:6e:46 | router | macOS 14 | NO |
| host-376 | 10.70.4.221 | e6:c7:ef:6b:78:03 | switch | Firmware | NO |
| host-377 | 10.91.5.127 | 32:f3:7e:25:7d:9c | router | Firmware | NO |
| host-378 | 10.82.2.253 | 15:45:d6:01:11:3f | workstation | RHEL 9 | YES |
| host-379 | 10.70.2.143 | 00:5e:09:72:02:91 | router | Ubuntu 22.04 | YES |
| host-380 | 10.34.1.140 | 4e:8b:c7:80:2e:09 | server | Ubuntu 22.04 | YES |
| host-381 | 10.100.5.120 | 9e:c2:71:84:68:ef | router | macOS 14 | YES |
| host-382 | 10.43.3.73 | 26:70:03:67:da:68 | printer | Firmware | YES |
| host-383 | 10.18.0.116 | 53:e3:2b:65:13:48 | workstation | Ubuntu 22.04 | YES |
| host-384 | 10.43.5.254 | 53:a2:af:ce:47:6c | router | Ubuntu 22.04 | YES |
| host-385 | 10.94.5.75 | 1c:4b:3d:3b:d4:8b | camera | macOS 14 | YES |
| host-386 | 10.81.4.134 | 0a:50:49:fb:40:29 | camera | Firmware | YES |
| host-387 | 10.77.2.10 | d3:96:00:3a:7e:4c | camera | Ubuntu 22.04 | YES |
| host-388 | 10.49.4.44 | 27:7d:ca:dd:05:77 | printer | Windows 11 | YES |
| host-389 | 10.34.1.10 | b6:e2:e6:da:e6:2d | router | macOS 14 | YES |
| host-390 | 10.102.1.153 | 7c:2e:3e:e7:3e:52 | workstation | Windows 11 | YES |
| host-391 | 10.70.3.206 | 55:d1:10:f3:1c:9e | server | Firmware | YES |
| host-392 | 10.99.4.91 | 6a:9d:6f:d8:68:59 | switch | Ubuntu 22.04 | NO |
| host-393 | 10.43.2.87 | cf:04:a1:54:76:d6 | server | macOS 14 | YES |
| host-394 | 10.17.2.169 | 2c:70:29:0a:8c:32 | workstation | RHEL 9 | NO |
| host-395 | 10.61.0.91 | 38:1e:cf:54:d0:2c | printer | RHEL 9 | YES |
| host-396 | 10.68.1.152 | 02:d2:92:66:03:01 | workstation | Windows 11 | YES |
| host-397 | 10.60.3.211 | 2a:96:b2:9f:10:de | printer | Ubuntu 22.04 | YES |
| host-398 | 10.20.5.97 | 60:14:8e:23:6c:be | router | Ubuntu 22.04 | YES |
| host-399 | 10.88.5.144 | 32:59:83:a5:6b:39 | printer | macOS 14 | YES |

## Firewall Rules (abbreviated)

RULE 1: src=10.56.0.0/24 dst=0.0.0.0/0 dport=3389 proto=TCP action=DROP
RULE 2: src=10.58.0.0/24 dst=ANY dport=3306 proto=TCP action=REJECT
RULE 3: src=10.67.0.0/24 dst=10.80.0.0/24 dport=22 proto=TCP action=DROP
RULE 4: src=10.52.0.0/24 dst=ANY dport=443 proto=TCP action=DROP
RULE 5: src=10.62.0.0/24 dst=ANY dport=3389 proto=TCP action=DROP
RULE 6: src=10.63.0.0/24 dst=0.0.0.0/0 dport=3306 proto=TCP action=ACCEPT
RULE 7: src=10.70.0.0/24 dst=ANY dport=3306 proto=TCP action=DROP
RULE 8: src=10.52.0.0/24 dst=ANY dport=3306 proto=TCP action=ACCEPT
RULE 9: src=10.81.0.0/24 dst=ANY dport=53 proto=TCP action=DROP
RULE 10: src=10.58.0.0/24 dst=0.0.0.0/0 dport=8080 proto=TCP action=REJECT
RULE 11: src=10.34.0.0/24 dst=10.77.0.0/24 dport=3389 proto=TCP action=REJECT
RULE 12: src=10.46.0.0/24 dst=10.47.0.0/24 dport=8080 proto=TCP action=DROP
RULE 13: src=10.41.0.0/24 dst=ANY dport=80 proto=TCP action=DROP
RULE 14: src=10.43.0.0/24 dst=10.102.0.0/24 dport=22 proto=TCP action=ACCEPT
RULE 15: src=10.81.0.0/24 dst=10.30.0.0/24 dport=8080 proto=TCP action=ACCEPT
RULE 16: src=10.32.0.0/24 dst=ANY dport=443 proto=TCP action=ACCEPT
RULE 17: src=10.48.0.0/24 dst=0.0.0.0/0 dport=80 proto=TCP action=ACCEPT
RULE 18: src=10.70.0.0/24 dst=ANY dport=443 proto=TCP action=DROP
RULE 19: src=10.82.0.0/24 dst=10.52.0.0/24 dport=80 proto=TCP action=ACCEPT
RULE 20: src=10.85.0.0/24 dst=0.0.0.0/0 dport=3306 proto=TCP action=ACCEPT
RULE 21: src=10.99.0.0/24 dst=10.22.0.0/24 dport=8080 proto=TCP action=REJECT
RULE 22: src=10.90.0.0/24 dst=0.0.0.0/0 dport=3389 proto=TCP action=DROP
RULE 23: src=10.33.0.0/24 dst=10.82.0.0/24 dport=3389 proto=TCP action=DROP
RULE 24: src=10.103.0.0/24 dst=10.30.0.0/24 dport=80 proto=TCP action=DROP
RULE 25: src=10.15.0.0/24 dst=0.0.0.0/0 dport=3389 proto=TCP action=ACCEPT
RULE 26: src=10.60.0.0/24 dst=0.0.0.0/0 dport=5432 proto=TCP action=ACCEPT
RULE 27: src=10.48.0.0/24 dst=10.74.0.0/24 dport=3389 proto=TCP action=DROP
RULE 28: src=10.10.0.0/24 dst=ANY dport=443 proto=TCP action=DROP
RULE 29: src=10.110.0.0/24 dst=0.0.0.0/0 dport=3389 proto=TCP action=DROP
RULE 30: src=10.30.0.0/24 dst=10.101.0.0/24 dport=22 proto=TCP action=DROP
RULE 31: src=10.85.0.0/24 dst=ANY dport=3389 proto=TCP action=REJECT
RULE 32: src=10.30.0.0/24 dst=ANY dport=80 proto=TCP action=ACCEPT
RULE 33: src=10.85.0.0/24 dst=0.0.0.0/0 dport=80 proto=TCP action=ACCEPT
RULE 34: src=10.92.0.0/24 dst=10.58.0.0/24 dport=5432 proto=TCP action=REJECT
RULE 35: src=10.39.0.0/24 dst=10.87.0.0/24 dport=3389 proto=TCP action=REJECT
RULE 36: src=10.35.0.0/24 dst=10.94.0.0/24 dport=53 proto=TCP action=DROP
RULE 37: src=10.61.0.0/24 dst=10.31.0.0/24 dport=5432 proto=TCP action=DROP
RULE 38: src=10.106.0.0/24 dst=10.31.0.0/24 dport=443 proto=TCP action=DROP
RULE 39: src=10.36.0.0/24 dst=10.106.0.0/24 dport=443 proto=TCP action=DROP
RULE 40: src=10.77.0.0/24 dst=0.0.0.0/0 dport=5432 proto=TCP action=REJECT
RULE 41: src=10.75.0.0/24 dst=ANY dport=3306 proto=TCP action=REJECT
RULE 42: src=10.30.0.0/24 dst=10.42.0.0/24 dport=3389 proto=TCP action=DROP
RULE 43: src=10.38.0.0/24 dst=10.40.0.0/24 dport=53 proto=TCP action=ACCEPT
RULE 44: src=10.39.0.0/24 dst=10.12.0.0/24 dport=53 proto=TCP action=REJECT
RULE 45: src=10.59.0.0/24 dst=10.53.0.0/24 dport=22 proto=TCP action=ACCEPT
RULE 46: src=10.26.0.0/24 dst=0.0.0.0/0 dport=8080 proto=TCP action=ACCEPT
RULE 47: src=10.11.0.0/24 dst=ANY dport=443 proto=TCP action=REJECT
RULE 48: src=10.92.0.0/24 dst=0.0.0.0/0 dport=3306 proto=TCP action=DROP
RULE 49: src=10.94.0.0/24 dst=ANY dport=3389 proto=TCP action=REJECT
RULE 50: src=10.89.0.0/24 dst=0.0.0.0/0 dport=22 proto=TCP action=DROP
RULE 51: src=10.98.0.0/24 dst=0.0.0.0/0 dport=8080 proto=TCP action=REJECT
RULE 52: src=10.14.0.0/24 dst=ANY dport=443 proto=TCP action=DROP
RULE 53: src=10.19.0.0/24 dst=0.0.0.0/0 dport=53 proto=TCP action=ACCEPT
RULE 54: src=10.71.0.0/24 dst=10.28.0.0/24 dport=53 proto=TCP action=DROP
RULE 55: src=10.57.0.0/24 dst=10.30.0.0/24 dport=22 proto=TCP action=ACCEPT
RULE 56: src=10.45.0.0/24 dst=ANY dport=3389 proto=TCP action=ACCEPT
RULE 57: src=10.52.0.0/24 dst=ANY dport=443 proto=TCP action=DROP
RULE 58: src=10.81.0.0/24 dst=0.0.0.0/0 dport=22 proto=TCP action=DROP
RULE 59: src=10.40.0.0/24 dst=10.79.0.0/24 dport=53 proto=TCP action=REJECT
RULE 60: src=10.65.0.0/24 dst=ANY dport=443 proto=TCP action=REJECT
RULE 61: src=10.58.0.0/24 dst=10.90.0.0/24 dport=22 proto=TCP action=DROP
RULE 62: src=10.26.0.0/24 dst=0.0.0.0/0 dport=3389 proto=TCP action=ACCEPT
RULE 63: src=10.75.0.0/24 dst=ANY dport=3306 proto=TCP action=REJECT
RULE 64: src=10.15.0.0/24 dst=ANY dport=22 proto=TCP action=DROP
RULE 65: src=10.55.0.0/24 dst=10.77.0.0/24 dport=443 proto=TCP action=REJECT
RULE 66: src=10.90.0.0/24 dst=10.67.0.0/24 dport=3389 proto=TCP action=DROP
RULE 67: src=10.61.0.0/24 dst=ANY dport=3389 proto=TCP action=ACCEPT
RULE 68: src=10.76.0.0/24 dst=ANY dport=8080 proto=TCP action=ACCEPT
RULE 69: src=10.71.0.0/24 dst=0.0.0.0/0 dport=80 proto=TCP action=REJECT
RULE 70: src=10.31.0.0/24 dst=10.61.0.0/24 dport=3306 proto=TCP action=REJECT
RULE 71: src=10.64.0.0/24 dst=10.59.0.0/24 dport=3306 proto=TCP action=REJECT
RULE 72: src=10.98.0.0/24 dst=0.0.0.0/0 dport=5432 proto=TCP action=REJECT
RULE 73: src=10.70.0.0/24 dst=10.67.0.0/24 dport=53 proto=TCP action=DROP
RULE 74: src=10.11.0.0/24 dst=0.0.0.0/0 dport=53 proto=TCP action=ACCEPT
RULE 75: src=10.53.0.0/24 dst=ANY dport=3306 proto=TCP action=REJECT
RULE 76: src=10.77.0.0/24 dst=0.0.0.0/0 dport=443 proto=TCP action=DROP
RULE 77: src=10.13.0.0/24 dst=0.0.0.0/0 dport=80 proto=TCP action=REJECT
RULE 78: src=10.49.0.0/24 dst=0.0.0.0/0 dport=22 proto=TCP action=DROP
RULE 79: src=10.53.0.0/24 dst=0.0.0.0/0 dport=443 proto=TCP action=DROP
RULE 80: src=10.14.0.0/24 dst=ANY dport=443 proto=TCP action=DROP
RULE 81: src=10.72.0.0/24 dst=10.83.0.0/24 dport=53 proto=TCP action=ACCEPT
RULE 82: src=10.101.0.0/24 dst=ANY dport=8080 proto=TCP action=DROP
RULE 83: src=10.85.0.0/24 dst=ANY dport=3389 proto=TCP action=ACCEPT
RULE 84: src=10.98.0.0/24 dst=10.54.0.0/24 dport=3306 proto=TCP action=DROP
RULE 85: src=10.34.0.0/24 dst=ANY dport=80 proto=TCP action=ACCEPT
RULE 86: src=10.52.0.0/24 dst=10.68.0.0/24 dport=3306 proto=TCP action=DROP
RULE 87: src=10.86.0.0/24 dst=0.0.0.0/0 dport=22 proto=TCP action=DROP
RULE 88: src=10.54.0.0/24 dst=0.0.0.0/0 dport=3306 proto=TCP action=REJECT
RULE 89: src=10.75.0.0/24 dst=ANY dport=8080 proto=TCP action=ACCEPT
RULE 90: src=10.28.0.0/24 dst=ANY dport=3389 proto=TCP action=REJECT
RULE 91: src=10.41.0.0/24 dst=0.0.0.0/0 dport=8080 proto=TCP action=DROP
RULE 92: src=10.58.0.0/24 dst=ANY dport=80 proto=TCP action=ACCEPT
RULE 93: src=10.108.0.0/24 dst=ANY dport=443 proto=TCP action=ACCEPT
RULE 94: src=10.40.0.0/24 dst=10.15.0.0/24 dport=8080 proto=TCP action=DROP
RULE 95: src=10.43.0.0/24 dst=10.19.0.0/24 dport=22 proto=TCP action=REJECT
RULE 96: src=10.68.0.0/24 dst=0.0.0.0/0 dport=5432 proto=TCP action=DROP
RULE 97: src=10.71.0.0/24 dst=ANY dport=53 proto=TCP action=REJECT
RULE 98: src=10.13.0.0/24 dst=ANY dport=53 proto=TCP action=ACCEPT
RULE 99: src=10.110.0.0/24 dst=10.52.0.0/24 dport=443 proto=TCP action=REJECT
RULE 100: src=10.71.0.0/24 dst=ANY dport=80 proto=TCP action=REJECT
RULE 101: src=10.41.0.0/24 dst=0.0.0.0/0 dport=8080 proto=TCP action=ACCEPT
RULE 102: src=10.26.0.0/24 dst=10.105.0.0/24 dport=22 proto=TCP action=ACCEPT
RULE 103: src=10.60.0.0/24 dst=ANY dport=53 proto=TCP action=REJECT
RULE 104: src=10.56.0.0/24 dst=10.33.0.0/24 dport=3389 proto=TCP action=ACCEPT
RULE 105: src=10.85.0.0/24 dst=ANY dport=5432 proto=TCP action=REJECT
RULE 106: src=10.36.0.0/24 dst=0.0.0.0/0 dport=3389 proto=TCP action=ACCEPT
RULE 107: src=10.34.0.0/24 dst=ANY dport=8080 proto=TCP action=ACCEPT
RULE 108: src=10.65.0.0/24 dst=10.35.0.0/24 dport=53 proto=TCP action=ACCEPT
RULE 109: src=10.109.0.0/24 dst=ANY dport=8080 proto=TCP action=ACCEPT
RULE 110: src=10.85.0.0/24 dst=10.34.0.0/24 dport=80 proto=TCP action=ACCEPT
RULE 111: src=10.68.0.0/24 dst=0.0.0.0/0 dport=53 proto=TCP action=ACCEPT
RULE 112: src=10.56.0.0/24 dst=ANY dport=3389 proto=TCP action=DROP
RULE 113: src=10.84.0.0/24 dst=0.0.0.0/0 dport=8080 proto=TCP action=DROP
RULE 114: src=10.96.0.0/24 dst=10.36.0.0/24 dport=22 proto=TCP action=DROP
RULE 115: src=10.55.0.0/24 dst=0.0.0.0/0 dport=5432 proto=TCP action=DROP
RULE 116: src=10.48.0.0/24 dst=10.56.0.0/24 dport=8080 proto=TCP action=REJECT
RULE 117: src=10.43.0.0/24 dst=0.0.0.0/0 dport=443 proto=TCP action=REJECT
RULE 118: src=10.18.0.0/24 dst=0.0.0.0/0 dport=8080 proto=TCP action=ACCEPT
RULE 119: src=10.43.0.0/24 dst=ANY dport=80 proto=TCP action=ACCEPT
RULE 120: src=10.37.0.0/24 dst=ANY dport=5432 proto=TCP action=ACCEPT
RULE 121: src=10.22.0.0/24 dst=ANY dport=443 proto=TCP action=ACCEPT
RULE 122: src=10.14.0.0/24 dst=0.0.0.0/0 dport=8080 proto=TCP action=REJECT
RULE 123: src=10.110.0.0/24 dst=ANY dport=80 proto=TCP action=DROP
RULE 124: src=10.83.0.0/24 dst=ANY dport=3306 proto=TCP action=DROP
RULE 125: src=10.85.0.0/24 dst=ANY dport=80 proto=TCP action=REJECT
RULE 126: src=10.41.0.0/24 dst=10.85.0.0/24 dport=8080 proto=TCP action=DROP
RULE 127: src=10.107.0.0/24 dst=10.11.0.0/24 dport=3389 proto=TCP action=DROP
RULE 128: src=10.51.0.0/24 dst=0.0.0.0/0 dport=53 proto=TCP action=ACCEPT
RULE 129: src=10.68.0.0/24 dst=ANY dport=8080 proto=TCP action=REJECT
RULE 130: src=10.73.0.0/24 dst=ANY dport=53 proto=TCP action=REJECT
RULE 131: src=10.68.0.0/24 dst=ANY dport=53 proto=TCP action=DROP
RULE 132: src=10.16.0.0/24 dst=0.0.0.0/0 dport=3389 proto=TCP action=DROP
RULE 133: src=10.88.0.0/24 dst=ANY dport=5432 proto=TCP action=ACCEPT
RULE 134: src=10.29.0.0/24 dst=0.0.0.0/0 dport=3306 proto=TCP action=ACCEPT
RULE 135: src=10.35.0.0/24 dst=10.30.0.0/24 dport=53 proto=TCP action=REJECT
RULE 136: src=10.107.0.0/24 dst=ANY dport=443 proto=TCP action=REJECT
RULE 137: src=10.80.0.0/24 dst=0.0.0.0/0 dport=443 proto=TCP action=REJECT
RULE 138: src=10.46.0.0/24 dst=ANY dport=5432 proto=TCP action=REJECT
RULE 139: src=10.46.0.0/24 dst=10.16.0.0/24 dport=3389 proto=TCP action=DROP
RULE 140: src=10.95.0.0/24 dst=ANY dport=80 proto=TCP action=ACCEPT
RULE 141: src=10.27.0.0/24 dst=0.0.0.0/0 dport=22 proto=TCP action=REJECT
RULE 142: src=10.84.0.0/24 dst=0.0.0.0/0 dport=80 proto=TCP action=REJECT
RULE 143: src=10.37.0.0/24 dst=0.0.0.0/0 dport=3389 proto=TCP action=ACCEPT
RULE 144: src=10.81.0.0/24 dst=10.40.0.0/24 dport=8080 proto=TCP action=ACCEPT
RULE 145: src=10.96.0.0/24 dst=ANY dport=3306 proto=TCP action=ACCEPT
RULE 146: src=10.21.0.0/24 dst=10.53.0.0/24 dport=53 proto=TCP action=REJECT
RULE 147: src=10.48.0.0/24 dst=ANY dport=3389 proto=TCP action=DROP
RULE 148: src=10.25.0.0/24 dst=0.0.0.0/0 dport=5432 proto=TCP action=ACCEPT
RULE 149: src=10.32.0.0/24 dst=10.95.0.0/24 dport=3389 proto=TCP action=REJECT
RULE 150: src=10.102.0.0/24 dst=ANY dport=53 proto=TCP action=ACCEPT
RULE 151: src=10.10.0.0/24 dst=0.0.0.0/0 dport=80 proto=TCP action=REJECT
RULE 152: src=10.57.0.0/24 dst=0.0.0.0/0 dport=22 proto=TCP action=ACCEPT
RULE 153: src=10.84.0.0/24 dst=0.0.0.0/0 dport=443 proto=TCP action=REJECT
RULE 154: src=10.57.0.0/24 dst=ANY dport=5432 proto=TCP action=REJECT
RULE 155: src=10.70.0.0/24 dst=0.0.0.0/0 dport=22 proto=TCP action=DROP
RULE 156: src=10.87.0.0/24 dst=10.102.0.0/24 dport=3306 proto=TCP action=ACCEPT
RULE 157: src=10.21.0.0/24 dst=0.0.0.0/0 dport=5432 proto=TCP action=REJECT
RULE 158: src=10.11.0.0/24 dst=10.77.0.0/24 dport=5432 proto=TCP action=ACCEPT
RULE 159: src=10.53.0.0/24 dst=ANY dport=3389 proto=TCP action=ACCEPT
RULE 160: src=10.76.0.0/24 dst=10.13.0.0/24 dport=8080 proto=TCP action=REJECT
RULE 161: src=10.43.0.0/24 dst=ANY dport=53 proto=TCP action=ACCEPT
RULE 162: src=10.10.0.0/24 dst=10.38.0.0/24 dport=443 proto=TCP action=REJECT
RULE 163: src=10.26.0.0/24 dst=10.78.0.0/24 dport=3389 proto=TCP action=DROP
RULE 164: src=10.56.0.0/24 dst=10.45.0.0/24 dport=5432 proto=TCP action=REJECT
RULE 165: src=10.101.0.0/24 dst=ANY dport=80 proto=TCP action=ACCEPT
RULE 166: src=10.53.0.0/24 dst=0.0.0.0/0 dport=5432 proto=TCP action=REJECT
RULE 167: src=10.109.0.0/24 dst=10.39.0.0/24 dport=53 proto=TCP action=DROP
RULE 168: src=10.42.0.0/24 dst=ANY dport=22 proto=TCP action=ACCEPT
RULE 169: src=10.74.0.0/24 dst=ANY dport=3306 proto=TCP action=REJECT
RULE 170: src=10.59.0.0/24 dst=0.0.0.0/0 dport=8080 proto=TCP action=ACCEPT
RULE 171: src=10.78.0.0/24 dst=0.0.0.0/0 dport=80 proto=TCP action=REJECT
RULE 172: src=10.61.0.0/24 dst=ANY dport=3306 proto=TCP action=DROP
RULE 173: src=10.45.0.0/24 dst=10.29.0.0/24 dport=8080 proto=TCP action=DROP
RULE 174: src=10.90.0.0/24 dst=ANY dport=3306 proto=TCP action=REJECT
RULE 175: src=10.91.0.0/24 dst=10.71.0.0/24 dport=3306 proto=TCP action=REJECT
RULE 176: src=10.65.0.0/24 dst=10.45.0.0/24 dport=443 proto=TCP action=DROP
RULE 177: src=10.97.0.0/24 dst=10.37.0.0/24 dport=5432 proto=TCP action=REJECT
RULE 178: src=10.95.0.0/24 dst=0.0.0.0/0 dport=80 proto=TCP action=DROP
RULE 179: src=10.88.0.0/24 dst=0.0.0.0/0 dport=3306 proto=TCP action=DROP
RULE 180: src=10.62.0.0/24 dst=10.23.0.0/24 dport=3389 proto=TCP action=REJECT
RULE 181: src=10.102.0.0/24 dst=0.0.0.0/0 dport=3389 proto=TCP action=DROP
RULE 182: src=10.35.0.0/24 dst=10.77.0.0/24 dport=3306 proto=TCP action=ACCEPT
RULE 183: src=10.38.0.0/24 dst=0.0.0.0/0 dport=3306 proto=TCP action=REJECT
RULE 184: src=10.59.0.0/24 dst=ANY dport=8080 proto=TCP action=DROP
RULE 185: src=10.18.0.0/24 dst=ANY dport=22 proto=TCP action=DROP
RULE 186: src=10.94.0.0/24 dst=0.0.0.0/0 dport=53 proto=TCP action=ACCEPT
RULE 187: src=10.14.0.0/24 dst=ANY dport=8080 proto=TCP action=REJECT
RULE 188: src=10.108.0.0/24 dst=0.0.0.0/0 dport=53 proto=TCP action=DROP
RULE 189: src=10.78.0.0/24 dst=ANY dport=80 proto=TCP action=REJECT
RULE 190: src=10.35.0.0/24 dst=10.20.0.0/24 dport=8080 proto=TCP action=DROP
RULE 191: src=10.53.0.0/24 dst=10.52.0.0/24 dport=443 proto=TCP action=REJECT
RULE 192: src=10.101.0.0/24 dst=0.0.0.0/0 dport=53 proto=TCP action=REJECT
RULE 193: src=10.90.0.0/24 dst=ANY dport=53 proto=TCP action=REJECT
RULE 194: src=10.65.0.0/24 dst=0.0.0.0/0 dport=3306 proto=TCP action=DROP
RULE 195: src=10.88.0.0/24 dst=0.0.0.0/0 dport=3389 proto=TCP action=ACCEPT
RULE 196: src=10.22.0.0/24 dst=ANY dport=3306 proto=TCP action=DROP
RULE 197: src=10.70.0.0/24 dst=0.0.0.0/0 dport=53 proto=TCP action=REJECT
RULE 198: src=10.94.0.0/24 dst=10.49.0.0/24 dport=80 proto=TCP action=REJECT
RULE 199: src=10.98.0.0/24 dst=10.63.0.0/24 dport=443 proto=TCP action=REJECT
RULE 200: src=10.60.0.0/24 dst=0.0.0.0/0 dport=80 proto=TCP action=ACCEPT
