# Threat Intelligence Supplement — SEC-2026-0419
Analyst: Maya Chen | Issued: 2026-05-23 03:00 UTC

## Attribution Assessment

Based on TTP correlation against known threat actor profiles:
- Port 4444 C2 usage: overlaps with TA505 / FIN7 operational patterns
- SSH lateral movement after initial foothold: consistent with APT29 methodology
- Payload download attempt (stage2.sh): similar to DarkSide dropper pattern

Confidence: MEDIUM. Single data point insufficient for definitive attribution.

## MITRE ATT&CK Mapping

| Technique ID | Name | Evidence |
|---|---|---|
| T1021.004 | Remote Services: SSH | Lateral hop confirmed in pcap |
| T1059.004 | Unix Shell | /bin/bash -i in memory dump |
| T1071.001 | Web Protocols | curl download attempt |
| T1105 | Ingress Tool Transfer | stage2.sh download blocked |
| T1078 | Valid Accounts | Key accepted outside baseline |

## Recommended Containment

1. Isolate 10.0.0.50 immediately from production VLAN.
2. Rotate all SSH keys on affected subnet 10.0.x.x.
3. Block 10.42.7.183 at perimeter firewall (all ports).
4. Submit memory dump to IR team for forensic analysis.
5. Notify legal and compliance per incident response playbook section 4.1.

## Evidence Chain

Primary evidence: pcap/2026-05-23_capture.pcap
Secondary evidence: forensics/evidence_bundle.zip (password: forensics-2026-q2)
Slack thread: #security-alerts from 02:14–02:21 UTC

Final recommendation: escalate_to_IR

## Supplementary Technical Detail — Section 1

Automated correlation engine identified 12 related events in the 6-hour window.
Baseline traffic on port 50457: 2 connections per hour.
Observed traffic on port 4444: 180 connections during the incident window.
Statistical anomaly score: 0.916 (threshold 0.750).
Related CVE: CVE-2026-48037 — not yet patched on 18 internal hosts.
Affected subnet: 10.4.4.0/24 — 14 hosts in scope.
EDR telemetry: 2 alerts suppressed; 0 false positives removed.
  - Log entry 30681: process nc pid=23406 uid=750 src=18.38.105.192 args=zoveoajxa5zs2dhzkjm-8ljyun3gw9p/beii3/rwha8m2sl 
  - Log entry 93862: process curl pid=15706 uid=833 src=128.81.208.120 args=y/cad7vypqougj1zn1cyw3vsazwy59/afh00ie0y9n-0z1vk
  - Log entry 75183: process ruby pid=11195 uid=316 src=126.0.235.182 args=z/r3xxzre-jv m/24rsq8ugi8dph6  l tv7j7bw hsf1td1
  - Log entry 49545: process nc pid=17215 uid=537 src=113.99.66.32 args=y2h5p 1um6l2zvv-a54b8eh6yn4b//ge7/9/74xu8xwgwiwj
  - Log entry 35375: process perl pid=14901 uid=995 src=56.136.79.70 args=98yedegueofva1qjqp9vn6/ xqj8ov-mtw5cxg5c7gjp//lk
  - Log entry 38651: process curl pid=7270 uid=721 src=190.248.134.135 args=iweawvt53merl8ghabqfy2/c/69lxmvpo321ken2id7nkqin
  - Log entry 13750: process curl pid=26962 uid=622 src=212.168.12.147 args=uu7/wv-o/asqxu90nwvvt4bc3/yepwbq9 z07ad8-j52hmqb
  - Log entry 14889: process socat pid=7899 uid=302 src=152.106.56.92 args=66yzxp  7py4llxel90qcoznyerbmmf10fqlxaaaavl79ana
  - Log entry 79197: process wget pid=12633 uid=315 src=116.245.249.79 args=b8z0knuep/l9240-qn38l92c0-21kaq4vtk5dmh6im3azq5k
  - Log entry 12994: process bash pid=19239 uid=625 src=46.149.30.11 args=io0iatym69372qncyq866khgx0inqaswvjnux-9-qre-mjky
  - Log entry 38254: process python3 pid=5054 uid=81 src=202.109.33.207 args=woyay7364p5a4plv/xzi2pv zo98up9ym6r5mmkzkb5ld1sd
  - Log entry 77379: process sshd pid=15559 uid=148 src=88.48.23.124 args=ccxc7k/xvabuxj4gdigmos9l2 gajwcyx7ycpu8rr//a36t3
  - Log entry 34534: process nc pid=31122 uid=987 src=153.118.94.46 args=564nq/p 3yv4ff0q5ap2w/egw9cf1evr18g0e6031iuzv6/h
  - Log entry 72050: process sshd pid=10062 uid=689 src=177.243.19.19 args=ailf1svb2jvpk0jmvx8mlvykvmuwa3 1h-a4jrnb/0fuk2fv
  - Log entry 23119: process sshd pid=8837 uid=857 src=45.53.122.162 args=rtshx6sppuw1qeju01are70yfgn hxvfbew3hke6k02eheaw
  - Log entry 58337: process python3 pid=25687 uid=484 src=39.166.198.78 args=-f5qyatwpoa97fjgd5ok/saf2i/fgov z9 z/qrfbi8-2-60
  - Log entry 43832: process perl pid=9136 uid=481 src=115.121.125.117 args=/mwcwhyr/ay6bs8mxy/is30sfsin mw4rx1v3-zsg5604n31
  - Log entry 55367: process curl pid=9612 uid=961 src=100.98.37.151 args=0ntsu84ib66cehsqbt-i3weu-ghboxu59lpx012go3av83/f
  - Log entry 79589: process bash pid=7383 uid=762 src=172.35.28.137 args=vp6qegmiuv2o85wuprspeql7rh-wgojr8062d0f0u2a8cspr
  - Log entry 87251: process python3 pid=9740 uid=413 src=163.91.169.19 args=85kpxzq7339yxy43q8reb5novkv0ea5wlo5nr3q3o55b1mta
  - Log entry 32770: process socat pid=19812 uid=875 src=193.182.170.70 args=q7asj0tuh6wfqpbvvgbda/-9kbssuisis7s-bgiv8jbm63u6
  - Log entry 52542: process ruby pid=20885 uid=694 src=203.169.8.250 args=c8 eqsak4nv8qk/etkpyn9iwckfshsmauw5q/13uodssig6k
  - Log entry 91117: process bash pid=13659 uid=79 src=217.248.148.170 args=9o8r1ehb6z14okjb6eio6g0ir gndnpxvd4984sa e- 381u
  - Log entry 59574: process python3 pid=17078 uid=719 src=134.199.245.175 args=1gktv6-7nvrpt3u uhcmj3m8m9pytebvll/c0gyvpnd5piox
  - Log entry 72024: process python3 pid=13917 uid=935 src=132.82.80.8 args=c18j9yqc 6u7kwv-jl95mccsecws98gvcwhaes2pvadn xqn
  - Log entry 74920: process bash pid=10087 uid=948 src=20.3.161.207 args=e/qtvj8s cdyqgbz8vuxtxozo4 zugym20l5xfqcrihn460p
  - Log entry 94431: process nc pid=19291 uid=54 src=102.83.162.226 args=eohgamy7ipgmmtew58tsvvipry4hd2pvk8s6p9clfkesr 44
  - Log entry 30727: process wget pid=8488 uid=181 src=4.108.197.207 args=s46m0g26-hgvohh2eaiskhh9pyb5 hz3ixg lx4tb00sr7x9
  - Log entry 80308: process ruby pid=20452 uid=525 src=6.214.105.84 args=uvx4f-b 37i89qml5ig 58atn73uevjwb7urfeoxx6pjwvb1
  - Log entry 66197: process perl pid=6346 uid=499 src=132.64.51.106 args=gf5jv5m6x n4vz1gdgk9xa0g08-f3uijsl1zf843qt9mjw8k
  - Log entry 46721: process sshd pid=30852 uid=559 src=86.255.203.59 args=-8x8oh1ikzsfqjq-9ud4su3boj56faay6h/bxyuiz5p2s8mt
  - Log entry 88693: process sshd pid=7770 uid=19 src=153.178.130.58 args=km/0e4x5ic0c3ttz/ /9s-c/hq14rry/6enf-bz4/cfnqz/8
  - Log entry 21210: process nc pid=30720 uid=823 src=211.220.145.192 args=kc43qsqmug503ry8lk6gd5bwj64i /wl 6uovhsevc gh/t2
  - Log entry 60792: process ruby pid=17718 uid=434 src=159.46.125.185 args=ukbqpe5blbhcbwi8dwcfvpvcnpabvfon1og1o/nisc3sjd1u
  - Log entry 64599: process bash pid=30941 uid=765 src=109.46.210.108 args=yetri8t8s8qq1np9q-ltizretpy79g opt70zev26m3hkcpc
  - Log entry 11217: process socat pid=15617 uid=977 src=129.211.14.95 args= j18zki8w73kzn8772-osntaiov43segr0n76manbb7lzmhj
  - Log entry 41334: process perl pid=21793 uid=174 src=117.34.46.39 args=1/ruq 2zj7nup9743posk5scackfmnvqebz131c6x4fzpo7g
  - Log entry 62167: process sshd pid=9861 uid=94 src=211.115.27.157 args=aut4zvf3zj662udw8q93vpfcz9ujsl4qs1jnm 78i7drxnu/
  - Log entry 50216: process nc pid=7304 uid=731 src=157.117.182.137 args=/ e679dbh0yp9l17zpatblu4hgdykw8n2k7zcvjjhov8xdsx
  - Log entry 91511: process perl pid=14887 uid=477 src=89.19.109.136 args=gp6kobm59uzgxgqf/8xy-b1cmx3v/3vwu0u3cmbq561nymz-
  - Log entry 25796: process ruby pid=29228 uid=843 src=35.222.107.214 args=fwnucql1o151hb/w2l/-u5 z3nuvyv8b4dunby0xdvfh0axb
  - Log entry 62016: process python3 pid=20700 uid=337 src=94.76.35.244 args=vizemvjxiwytvh532hogleuco6utb65/-vd7jfyd899kmm/ 
  - Log entry 97237: process nc pid=15915 uid=332 src=216.84.134.246 args=t/a2utxmmwb928eleiwuuac-auh-yg03jziob/lglgcl/zz-
  - Log entry 41086: process wget pid=11730 uid=353 src=91.245.169.65 args=hd4zxsjeplzydirngfncks3d1  z 3amnzz2djm9svxcpztd
  - Log entry 48308: process ruby pid=30194 uid=130 src=127.223.199.235 args=npzkqxu0r8y2on19inqbfhfs /wptyptqus3zec28x0449c0
  - Log entry 20340: process wget pid=11452 uid=842 src=121.83.95.82 args=f9q2p 7xeaq3vphb3shc7wm3xq6ajv9gmpwf2m7eiqsgtnsh
  - Log entry 54263: process socat pid=13702 uid=146 src=118.122.165.208 args=119/kjy3p1rwn6m2gi-bdt2s71o8ujrapq28rekby6l3-tmh
  - Log entry 36690: process wget pid=16130 uid=95 src=180.198.141.89 args=ebghbghhyuq/8le21absxxaal-f-eah7l3wzkdg9pk8kh5rd
  - Log entry 20026: process perl pid=29948 uid=149 src=216.86.215.71 args=r--tbxmgop69hcc8izu0y4709ws7v7pn69tche2kar3tln1j
  - Log entry 51818: process nc pid=15453 uid=526 src=98.14.23.211 args=4nct1axcadxd-d2zsu0ev2ww5sehmt6yns8y8nfvelfqpi3m
  - Log entry 76857: process curl pid=24577 uid=449 src=25.167.220.102 args=3176zmtyfr6z 6vwr58g71cuw/0cs17af4iupkxo7 nesdw 
  - Log entry 39746: process socat pid=3828 uid=543 src=73.143.9.155 args=oz494ap2qjbk4q22q/8j7jt0d1-d x19t5zvyw7zkx2c8ldc
  - Log entry 58572: process sshd pid=22363 uid=149 src=17.140.175.215 args=jg7eraoc7kbt3stnv9tznx2en91l3u whk9t8fpzvhb9bvao
  - Log entry 87147: process python3 pid=25067 uid=275 src=36.124.242.96 args=hty3nst/1o-x839tz5p2ad5c1yg4dml5wul1cktzky/l zc6
  - Log entry 24490: process python3 pid=17828 uid=578 src=193.12.3.111 args=spki4ahqth oi31cgd5unl41c/49dqxgjifc/yi7qkjqkaxk
  - Log entry 46780: process perl pid=5162 uid=497 src=6.128.90.145 args=f/hpuanashs4s7cjb4-nyii8a5643jvq phbiyawkslq4f90
  - Log entry 98162: process bash pid=19093 uid=602 src=106.23.74.88 args=ntgsp86zggb2m-55pb3wahyp ch4o39rgc-vovhyivq gz3u
  - Log entry 51813: process wget pid=7399 uid=49 src=175.33.129.136 args=r/rgalc1e0e2g7q9hosfjr0s6lgg6e93b52uhmzi932252z2
  - Log entry 10619: process curl pid=24014 uid=328 src=108.86.215.197 args=givaftacbqy y q3tggv96fx8hcdwb8 d8tjnqt-yi 5xtzz
  - Log entry 60243: process python3 pid=16044 uid=878 src=201.33.7.27 args=pklnpb5rnvn dtr1gya5d 0xbaa4tjxu8wnzqjwtdfboo5a5

## Supplementary Technical Detail — Section 2

Automated correlation engine identified 27 related events in the 6-hour window.
Baseline traffic on port 12262: 1 connections per hour.
Observed traffic on port 4444: 130 connections during the incident window.
Statistical anomaly score: 0.956 (threshold 0.750).
Related CVE: CVE-2026-23856 — not yet patched on 15 internal hosts.
Affected subnet: 10.8.5.0/24 — 5 hosts in scope.
EDR telemetry: 2 alerts suppressed; 3 false positives removed.
  - Log entry 34956: process nc pid=14154 uid=767 src=110.32.159.153 args=qe/h38u6gzga-j4nwoltw/0e/vem7kl3e1h6fn-qps24h56g
  - Log entry 29342: process curl pid=3568 uid=498 src=220.237.61.78 args=2jafxfrh07d hm7u7qahlwshua/g7cl1podrj-qxntydv7m7
  - Log entry 94652: process python3 pid=20933 uid=853 src=2.147.117.145 args=47 mkxut3nmu34hn2jqiu-utke1s6q0olyejnaibel9oufp1
  - Log entry 86507: process wget pid=16917 uid=74 src=197.38.232.127 args=zq4st/7ftr4-112-byhy/mq3ypc14ispuv48gvuty3n6tizl
  - Log entry 90322: process sshd pid=7228 uid=10 src=30.193.151.6 args=8mkq9dp5p52c6mxxmezx8fgm0gyrck7lkuzfxlvlq6ncg2vt
  - Log entry 56194: process perl pid=19158 uid=887 src=85.165.252.213 args=fjcm8qwimzu51slv5-9ecz03kk2mc3dg9s3rveeg7tz4lzoi
  - Log entry 76709: process bash pid=3551 uid=73 src=96.126.228.85 args=ojw9ts0-xuztbc5dml4ooek3tzyvciwjemeb08w7xdt ueiv
  - Log entry 72191: process python3 pid=26303 uid=188 src=103.122.70.6 args=4r4z2i4 0gr6k5vuqjwta9s0ww55togt50b87yl4meqzv6kl
  - Log entry 32605: process bash pid=29247 uid=118 src=121.32.77.227 args=fllz 766d32u6094hw96kfv- u13ypfm4mvy6g/qimvcbaxc
  - Log entry 42417: process nc pid=23447 uid=538 src=163.41.36.146 args=7oh29cou5ynvtoask3wt2bckcu6gqc7nn4wzouh1n mnvdmv
  - Log entry 71389: process nc pid=16372 uid=118 src=35.80.8.167 args=n-pi 5v-u49g2p5o2yjcxr8h41uiabgi-g/g6e/p73ufu9rx
  - Log entry 21127: process socat pid=7337 uid=292 src=144.155.48.131 args=5u2 6sww4a5otxi3tvu7z4h0l3-cr9cv/w8d-fopi4o2jv1x
  - Log entry 69972: process socat pid=18179 uid=83 src=192.138.78.234 args=a515mvlf 9iy/k0/s7sretqm wnf37iiouk/9qwknpts-64-
  - Log entry 82816: process nc pid=31173 uid=442 src=204.21.83.103 args=11-bae7ys5asy4uy47f-/ 530cgzc0sazq0fb22doueic52v
  - Log entry 63349: process perl pid=11146 uid=292 src=32.250.15.141 args=u8pcz8tvf8ppi2d/t-k-qncd43za04buxfc 6zhrydmphgkn
  - Log entry 76289: process wget pid=18561 uid=55 src=21.159.238.253 args=l9rueckbb-niathwlz7ro937p zm3eb9t2rs5qaftcetvo88
  - Log entry 78353: process python3 pid=9246 uid=916 src=220.188.161.147 args=rw0nmnrupi/5a7uxqkjh8px93lf ehe544rch-2xcoto3ybb
  - Log entry 98491: process wget pid=24086 uid=955 src=99.209.144.234 args=cepkn207sg3i1unist7hqcgco80hkqq1ri5fji-9qwtp4cdc
  - Log entry 44304: process wget pid=26485 uid=486 src=40.133.209.78 args=2b0363lk3ib3 eo0uiof85-j0hzhvigo8p2lf7zs3k66fd40
  - Log entry 80743: process socat pid=29393 uid=547 src=72.84.201.37 args=fxdacc3onwz4 ph88y544usf18mhr0qi1fxys4/-ykh4tu73
  - Log entry 15778: process python3 pid=10124 uid=802 src=203.126.231.81 args=/lpirx /hwye po3/pji 7wuxmn5chvl11w9iwrijexir19b
  - Log entry 36421: process ruby pid=22915 uid=809 src=104.103.195.78 args=evftk90mirdolecx0d2rykl9jsaj6lyl q/pza5zgsvem3re
  - Log entry 40962: process python3 pid=16615 uid=524 src=29.50.54.204 args=cfow/e2-oh2qd575tmp71a/vyzllg/b/7rvps53c0zm-xidw
  - Log entry 27575: process perl pid=31315 uid=124 src=210.100.254.183 args=taty/lkzrrs50tmakhoinkkc-1fje0os4r265uacog0ixgez
  - Log entry 83685: process sshd pid=3485 uid=855 src=85.223.72.81 args=puubxn9gkelj8jgp7d1oif046cl/d0uxs/owim8p942k86sl
  - Log entry 63193: process bash pid=21575 uid=651 src=194.226.39.68 args=hoicjlk90ylly/l -gcg4o s0mqbpm0t68m0jn9d1ohslp0g
  - Log entry 79693: process socat pid=31476 uid=498 src=204.160.15.94 args=li3 hg1duwllelosl3r900lh/k8qq68v91yc0lggrcu8hylk
  - Log entry 86188: process nc pid=15348 uid=785 src=152.62.239.192 args= 8v09s sg606-t1t2-u7-8u7hz4g5estjg0dak7bd181ftlq
  - Log entry 64663: process ruby pid=15512 uid=653 src=198.223.47.210 args=jpb4w8ez 2z8js1vukm3n2--r234 8mu 9 xgv0m21b4pq2e
  - Log entry 97971: process python3 pid=3714 uid=143 src=103.199.42.116 args=w9qhgfn0d61d22j/ccfds-7/9fajauowwnf7ybh7vm8gmzdq
  - Log entry 73613: process wget pid=23452 uid=479 src=190.166.108.204 args=x9hc7ybbwcy081o fcsi/ygucdl5cgkdr8xa2mk7lqipmm04
  - Log entry 93181: process wget pid=28739 uid=0 src=110.113.80.236 args=uiserexrg1/qlbp/ /phk/jydyihoj-amnavkao6amxswh4q
  - Log entry 84844: process curl pid=24764 uid=39 src=148.218.172.14 args=0vj31 e0b7vtlo-vrdiqi-4qw/lneff5xxt8hm0r309t8pyd
  - Log entry 91594: process nc pid=14812 uid=803 src=158.96.121.92 args=8d86mipu7nvfvmk7pig503xcy5w37z2/fv77viwyk16d9pr-
  - Log entry 56769: process ruby pid=18567 uid=57 src=115.96.51.209 args=bmoof9-vo-q h1hkr56eeleq0ir7ds0b-q03mn2oqbjm2oi 
  - Log entry 28840: process curl pid=1284 uid=940 src=216.165.114.187 args=-kju7f038puz4wzr2qeb9a5f88iictbk8a0gxoubgqi8f-wh
  - Log entry 95774: process sshd pid=21897 uid=439 src=201.117.190.92 args=-eoe6-0i5l/7l8t 8-1-19mtqovm17ea75-e6yua3j1gv72l
  - Log entry 50285: process curl pid=18605 uid=990 src=200.200.231.35 args=h0pnr0ep-js3/bv0h4 jzda6gee79600kxawuvwje6i 32s 
  - Log entry 76380: process python3 pid=20345 uid=618 src=118.168.49.50 args=rro7ko026exyxlp7k 8s/m84vq5ddi-nfpn0vrumy45av-bd
  - Log entry 57496: process sshd pid=28765 uid=227 src=63.179.114.40 args=2rpno1ppj5ui/hl0vzaeb86v/wgrj32 v0iostxnmmgkg0ap
  - Log entry 30508: process nc pid=2253 uid=327 src=161.93.206.54 args=0psx4jnhxvba1vsb3wnyl3 efcpm3t9p1bc5-btxkgs0qqfl
  - Log entry 64146: process ruby pid=6127 uid=805 src=208.242.230.192 args=ykc jvlkp1ib73c6x-o64qzgcob6zshxb5yp3ous66eizzt3
  - Log entry 84667: process socat pid=24668 uid=920 src=190.202.171.169 args=8iycov4tkag 9bi/9wkcps 4r65lfsr6ebz3zzadq41r92-i
  - Log entry 43160: process ruby pid=25184 uid=251 src=24.21.228.134 args=5pua5vl2 e-qi3-58inbcw9s8mt/ssyp6-6p/9pc889f //b
  - Log entry 82621: process socat pid=13010 uid=77 src=127.113.69.240 args=-842-a3310tkrups 4dbaxk9xr8t6ptlksy9j9na ir15 z1
  - Log entry 76921: process perl pid=20447 uid=144 src=147.193.175.54 args=1sz7qe/64jnx2selp49x8czl5i8kxkngclm9v62o46nut9g9
  - Log entry 92225: process nc pid=7245 uid=919 src=193.84.146.103 args=ucm6u 0 ze1v5xz/tfqkj6nvm6peoasu2/xx2nqex92jj5xc
  - Log entry 18362: process socat pid=3630 uid=790 src=177.62.241.165 args=d-rqcdap7hl/vrywjd1vh pc4voljcy0yh839f-sn2fngei1
  - Log entry 36740: process python3 pid=18896 uid=702 src=85.70.141.88 args=fg 001n/bot3n-wdtvwywdx rwq/qetr3kw8t67jxiqtnblp
  - Log entry 93332: process python3 pid=4356 uid=800 src=97.138.172.173 args=850q2p / z-pd0dk4hitifq5 nvmx716zh305etlwkbmh837
  - Log entry 69239: process perl pid=17261 uid=214 src=185.180.67.233 args=62g/9 3n94ajh614428fuqj93z65 lj7lsk0dk etz1h9jll
  - Log entry 35374: process nc pid=12438 uid=295 src=84.160.91.115 args=07lu/zlh5hyi7xomkpdknk7wds3k287w0pv/evj0hfknwsb4
  - Log entry 71888: process sshd pid=29130 uid=614 src=117.250.196.132 args=akbeamrde9ss 7jgzll9hg989nw yznn8irppew3i3bu9ll1
  - Log entry 43185: process perl pid=25017 uid=412 src=136.168.10.190 args=vme70cfxz0xcr/7g9is io9 gm/8whp3179/tvtg y9f nfy
  - Log entry 86778: process perl pid=17993 uid=664 src=197.11.208.81 args=vwc92 sco8qyjm4sa74z92tgdemdotg7-nxlrjxby65w4kii
  - Log entry 50144: process curl pid=26585 uid=534 src=64.50.98.2 args=l8w/3f0-mqn377hgpuk0jcf95yzmimngtxkeb6m/yrtw/fko
  - Log entry 37689: process perl pid=15352 uid=381 src=220.212.6.180 args=umex41uokq ph8aidk5io374imzg77k4by22r4egcbnoiokk
  - Log entry 50606: process socat pid=28369 uid=196 src=142.189.64.110 args=3-cp3m4e2c3kbutdxe5yvcyge15n t6kag0uf9mbtfu-wepe
  - Log entry 61142: process wget pid=7103 uid=210 src=135.190.50.63 args=mat2uzmucf11lv-qax4j/gcnldowpv436dzp68wql00e3zwa
  - Log entry 20796: process nc pid=17162 uid=155 src=213.213.231.164 args=i3kep9cb0b526xpcbikisd3t6t1vt5l1ul2xlx2k25 /52p7

## Supplementary Technical Detail — Section 3

Automated correlation engine identified 8 related events in the 6-hour window.
Baseline traffic on port 18567: 4 connections per hour.
Observed traffic on port 4444: 161 connections during the incident window.
Statistical anomaly score: 0.934 (threshold 0.750).
Related CVE: CVE-2026-20290 — not yet patched on 2 internal hosts.
Affected subnet: 10.5.4.0/24 — 7 hosts in scope.
EDR telemetry: 0 alerts suppressed; 3 false positives removed.
  - Log entry 73887: process sshd pid=30446 uid=424 src=111.133.225.11 args=sg696p 70p06imda3rt5jk stcvqx0 87u4twdt0ghhw4sa4
  - Log entry 47041: process socat pid=15858 uid=933 src=202.188.218.9 args=bw4ztgo6sf9g41-z9n9st-lz/kym/bz06m4xgzixbzp/1pxh
  - Log entry 11897: process perl pid=22117 uid=661 src=156.118.189.245 args=g nqmiy6s2mst89ff47t317jlg/ibm37awjy71 yv9i5ixtf
  - Log entry 40352: process curl pid=2920 uid=52 src=119.173.193.78 args=8uvgfj83zt4fcuid-b2p8w0qulkz3yjd5hqz9xy3x4n-ecnn
  - Log entry 87733: process curl pid=9968 uid=860 src=32.113.70.237 args=shgegjvbcrqkw/xjnbg5exg/o52n0tr gjx6svmfmc9saydu
  - Log entry 60743: process curl pid=12832 uid=865 src=200.190.81.20 args=pr/orl9d3r/4x/of1 6vfneb6w3lmn7odkzkmjt237e-1awd
  - Log entry 68989: process bash pid=14802 uid=77 src=3.41.62.223 args=upnu 9 lb1drdelyrlqfxu -k f681d8bbiuvr-nuqcleh-j
  - Log entry 87439: process bash pid=21038 uid=309 src=120.118.240.33 args=gohsfofeccjhmoeom89ubi6ek/24yuu8z ncokhanq4rvzxy
  - Log entry 88621: process nc pid=5051 uid=985 src=184.157.130.155 args=6 fe--dxv755fk0yddomo0d 2ofxp/czr3tm8yxuf kahkuy
  - Log entry 78925: process sshd pid=9022 uid=940 src=149.156.139.6 args=iq7cold02wnoucnhl7/4d/ql7qp9k9cz1zq3t-pem5f rw5s
  - Log entry 58676: process curl pid=31987 uid=337 src=70.0.144.129 args=e76cleegluj9/2r/rygp7 /fuxy0uf2-ek4h700y yd03-r1
  - Log entry 70543: process ruby pid=2767 uid=57 src=128.229.153.2 args=-2-wwawwvrabbg9ipq/cakwn05f08dskife/42hqt1uocmu9
  - Log entry 15339: process nc pid=18645 uid=669 src=81.50.142.22 args=5z-pslz7 7 w8pwxmjtg9ic3zfwqj-ondlagszk8u53r8k45
  - Log entry 54940: process ruby pid=30275 uid=841 src=180.22.32.19 args=tjvbah68ktv7tsc-tzqkjd7pv5ed-1/7jms-takun gqx 12
  - Log entry 17259: process sshd pid=2134 uid=204 src=4.191.130.211 args=2wpgojsi41d43uuuy4uvi16r88sl9d6 qkachgh8x5rotk7 
  - Log entry 13526: process sshd pid=12455 uid=934 src=64.149.28.152 args=c-vqcqdh8i/06oe-iufai7jlu/7wshqihfbbiyjvusum-ziw
  - Log entry 67820: process bash pid=12622 uid=369 src=182.58.195.171 args=p/0qeaq1woh/lzm0nguibxx4326nh9flspfekx0vwovjjqf6
  - Log entry 75469: process bash pid=27838 uid=870 src=149.131.109.141 args=/fhidf-35sg/dwx37ts18eg9vw-5o2u/kci68 sl-zi5xope
  - Log entry 32455: process socat pid=30073 uid=120 src=202.131.100.55 args=3dfrrpg5op5ufs/-86l7c5zlpm6rq 59jz7x05ma5v5 7cga
  - Log entry 61713: process sshd pid=11826 uid=624 src=59.53.196.113 args=8m7njae333hvebso2lp5gl21hg5hsxyllg1qul8e8cpdouwu
  - Log entry 75834: process nc pid=8201 uid=119 src=104.15.22.141 args=w-8mwsc435xthcce44rfmn3-hwhfo88sgzi2x1bbn/yl/g9j
  - Log entry 30104: process curl pid=7510 uid=701 src=34.227.87.81 args=gv6y46apigfavn50fqdbp8h tsw1l5gl1pdgcht linlozw/
  - Log entry 56971: process socat pid=20601 uid=62 src=202.17.214.41 args=qce-/mwsuqyv28jappa39v3sq8agq1zoip9krb7x3med6 kv
  - Log entry 11641: process nc pid=21511 uid=35 src=189.9.161.241 args=b 7m21h3g45rgzq1kwb3n9trytrwrbp05ry-z1-ckpvlxy8k
  - Log entry 15205: process perl pid=11145 uid=893 src=77.197.12.216 args=c5h6xwq/d9ua74o15pft ah/crmkkem1d2o1971ks0wwqhhg
  - Log entry 83539: process wget pid=18414 uid=643 src=42.188.181.59 args=9jwltadlea9/z1ojm fa3fl0tpty6jcztzzdg5ocymypxv-h
  - Log entry 43784: process sshd pid=8958 uid=106 src=78.168.20.92 args=ox05a867e8i6f32b3r nibps/zqw6gpxrea58mabl/b8-th4
  - Log entry 61849: process ruby pid=2703 uid=651 src=209.52.205.164 args=umpnzj 41ck6p1o51ndhbsgb4kzolk29/w/8/kizpqp7q092
  - Log entry 35413: process wget pid=2986 uid=211 src=38.211.75.41 args=6vgx/n943kyrbrozu507x9x1qw-5u2q trj5a9hygza3z9fd
  - Log entry 80114: process perl pid=21370 uid=803 src=11.147.209.99 args=p6vm7-p4qe 59e41xfl1hiqir1l1v0yjxlcvl-3dy1xi8g8o
  - Log entry 65255: process sshd pid=1072 uid=673 src=158.146.58.249 args=9edq0fbsfxbgmilmqg/j5g2u-rknz6tb-n3jd5r/jvgk2syh
  - Log entry 52578: process socat pid=2353 uid=567 src=47.237.48.214 args=u8ms9ns1vs71zt/fgyk18k-eh7kqnvuoi08x35s7dq3lhb7e
  - Log entry 36634: process nc pid=31636 uid=336 src=194.69.53.49 args=d-kxgkseowwtxdm0yi-a953umod5ji56j0-rzd86pzrthnbx
  - Log entry 90562: process curl pid=2629 uid=776 src=10.182.10.207 args=e1qk7vdph4dd8r16ndi4csozw8awnvu s-swhqkc20k/1-qq
  - Log entry 88630: process wget pid=2307 uid=780 src=194.153.57.11 args=ij7ers8tvvub4qubut2mnmku-i1qbt-5l0df91q1ioc9 9rw
  - Log entry 35617: process wget pid=2564 uid=498 src=211.139.95.172 args=4tvbdav8sx/rrvnmx1jogtq-8b5vav1w8hf-tbncbdo5m3a/
  - Log entry 44516: process socat pid=26307 uid=579 src=129.71.135.103 args= 9oizuctrk4/gwis9/y-2gesx3 pnz/j-sbk7i28n1/0q9uv
  - Log entry 80913: process sshd pid=4791 uid=426 src=198.100.101.126 args=m cjh0yd5l5ifuekmxnd02e a9li2/5bbqwvee-27a7xbu9w
  - Log entry 70987: process socat pid=15891 uid=761 src=120.163.35.207 args=d86w4kf/v0bbx6t9he8qyv1u8jxotikj1hn6azn559tkkae5
  - Log entry 62174: process perl pid=18120 uid=175 src=212.252.164.29 args=4e50qua4/pn/we rvhdmm9xfkpiddkegweihsrllxoupxjw2
  - Log entry 62626: process python3 pid=13571 uid=140 src=135.75.66.125 args=r5yv9m0gy8qgl6fedc3-p16dxnj 4/eq2vbbsitn7ab2exy9
  - Log entry 18842: process socat pid=13828 uid=856 src=52.23.90.100 args=167nx58b9bfmsv6zarduc75kexwx2l dnhq3d6n-vvlrt0b4
  - Log entry 41550: process perl pid=10237 uid=169 src=108.178.39.1 args=rtvrq-xh 9kpv p81ww6h1 9z0evwt3i9tln9nios849c4sm
  - Log entry 33564: process sshd pid=24512 uid=310 src=55.115.140.37 args=9miagf-7o9yddekggjx-nc4wdsemhxwqgt6fpxc9guipbvwe
  - Log entry 28739: process nc pid=2475 uid=638 src=81.233.185.25 args=zeqa3wjzszefeyn-qo-w3sgup65p5s3cyl9/cy-f4yx66yi1
  - Log entry 80308: process perl pid=2281 uid=440 src=36.107.62.160 args=5shxbga 3qb12 fshy6i7m8-t07bgz96u9qya9ogsbl1/6m2
  - Log entry 24852: process perl pid=30983 uid=175 src=192.94.56.49 args=xtrcap36q1m1c6wd802yn8kyyhvc6xt0os kbtdluq7q7-g/
  - Log entry 95089: process ruby pid=7854 uid=686 src=117.210.250.224 args=81dnev81 kt 7g6 74wnirkjm1i21006fdn-mh cdcffxy8b
  - Log entry 88126: process bash pid=10806 uid=247 src=200.118.206.227 args=uftz11onrdkmljzwziobed99uidn85el3f08kc3pdjlkcvw/
  - Log entry 32330: process socat pid=31683 uid=294 src=80.212.75.196 args=br 7w7zg7l74md6w- 4aqjvkwt1yyjcqg6/do55iwmp7nttn
  - Log entry 35052: process wget pid=25085 uid=465 src=39.109.93.62 args=-frjveny3ev5fac0n3gr2b17w7he1o000g p0-nb2h8j/6ry
  - Log entry 47008: process python3 pid=18197 uid=937 src=2.248.130.240 args=rzwmzx5xlod/du9xqvy1hc5nyz/lts-cbxjuxh88vp-1ullu
  - Log entry 55805: process nc pid=19567 uid=336 src=162.134.114.159 args=6sagzy6siujx97bq5tc4870gh/gerxtud2/xte-kfzndi55g
  - Log entry 27208: process perl pid=23291 uid=567 src=125.157.140.181 args=8et5qs/mvfsu5p7b1/swi/dpz4ejwxrlhw-8-dvj2qs1kls6
  - Log entry 96320: process ruby pid=13947 uid=875 src=70.224.229.99 args=lc59x8c2-/hj3680 qlpkhus2g4ki9f-bg7177qzxa0q7at3
  - Log entry 10463: process python3 pid=11153 uid=172 src=125.18.131.203 args=8zp1aabj95vf91 34xwtbirsiuw2g1u7zuxc02rwpox97x02
  - Log entry 77607: process wget pid=13421 uid=377 src=152.247.97.23 args=v-klttc/-0h9ht9knworh00isixalwdw6009ynm40h on11v
  - Log entry 53133: process perl pid=22364 uid=434 src=27.132.87.19 args=hqnp87i4xhf4l43votd49f279mq6se89ini9-ofv-ucjz7e5
  - Log entry 83970: process curl pid=22866 uid=192 src=130.139.119.31 args=5og1xong1r2xai-40zvjyh 8/bd/8kpjrbxt69clnllwan6-
  - Log entry 17574: process wget pid=18186 uid=156 src=10.27.196.232 args=b6h68jcg9wypuk-af7iwxt-1n07uwqw-//b-oxq v-955hoo

## Supplementary Technical Detail — Section 4

Automated correlation engine identified 24 related events in the 6-hour window.
Baseline traffic on port 45595: 5 connections per hour.
Observed traffic on port 4444: 50 connections during the incident window.
Statistical anomaly score: 0.986 (threshold 0.750).
Related CVE: CVE-2026-33761 — not yet patched on 4 internal hosts.
Affected subnet: 10.4.3.0/24 — 18 hosts in scope.
EDR telemetry: 2 alerts suppressed; 1 false positives removed.
  - Log entry 41688: process nc pid=15833 uid=130 src=179.108.196.197 args=1pp-r9/430uzxdd8lg35ng7thsm3w-4t62gqvd7jrlaqhsqa
  - Log entry 26573: process ruby pid=31481 uid=792 src=48.242.197.99 args=my sxoym3l4w wei32vb9fjykmr9lrybxb-2 8e/mje6eue7
  - Log entry 47551: process curl pid=2670 uid=618 src=180.115.113.61 args=n1/34r/9lsjv00y5y1spc 9dou8-h0hrbjzg8tqwhc6- d5p
  - Log entry 39175: process ruby pid=22581 uid=582 src=201.71.27.152 args=iewgcjf-- 9s0sv4yisqqogj8wsut2rto0wz0l1-tp-amp49
  - Log entry 33294: process ruby pid=24344 uid=236 src=22.115.58.175 args=yjjk5y4vuysvrvfl ohhrwo3n1is-ia05djq3butz0m3td0n
  - Log entry 81106: process ruby pid=18754 uid=908 src=37.229.43.231 args=w773ph8xdhib910nlr40rsgkxu9w003uvdrhe8w62t45i49 
  - Log entry 13120: process sshd pid=29920 uid=363 src=85.8.171.18 args=ojmkmxu5z7q3p5txvp47rrs-rgsm70pqgbk88whzwgesu4zv
  - Log entry 65109: process nc pid=10439 uid=874 src=211.152.195.208 args=d0r9m7bg4x7lxbjkxfb4y7mpjsqdtohysb2p3-n 6e6ams-b
  - Log entry 21919: process bash pid=16903 uid=838 src=132.254.237.116 args=a0zhz2g2fgvq yvvf3gsw46av0sxrvs j2x7eg9vlory4ejr
  - Log entry 91506: process bash pid=8114 uid=791 src=69.16.62.242 args=x323 8gkn59dw1sy00j/2uapmcff0l608l9p8suiaz0deay5
  - Log entry 26701: process perl pid=28374 uid=199 src=94.193.5.133 args=4hbtxs3-sl84zhs3h7rvqafvkuapm-kb3fh3dnnj7y fzx36
  - Log entry 99091: process bash pid=12216 uid=320 src=216.28.130.225 args=c4 zjm5gdu2kd4mxbdai99j 02ttocjephlvu6ybch6rtps0
  - Log entry 87345: process perl pid=17093 uid=691 src=33.178.247.7 args=lvtov2cnydzdcqv5nn3hymslv4t ss kd8dagwwpgt4f3o i
  - Log entry 96060: process nc pid=11474 uid=42 src=35.92.207.124 args=-9xuya2erqs1e0gxx2d-dp eqaqw4qeyfmr3hu96irlvxvrv
  - Log entry 55923: process sshd pid=12307 uid=578 src=212.214.63.38 args=e84o5fg65pthm0t8gkyp5uwlsygmc6i38 ui-yqrd5 odqyp
  - Log entry 48824: process wget pid=15465 uid=140 src=116.55.28.27 args=t/bp21 3/yq 6/ff00hc2em n4vm6imszt3kdl7gpbto3p0q
  - Log entry 52704: process nc pid=7198 uid=585 src=147.68.143.27 args=zo100v0k1b/2fajjqrvy79r4vlpvhgi3ypdb-s/5a471va5x
  - Log entry 57746: process python3 pid=16026 uid=681 src=206.141.63.81 args=5cikj5j8rn3wedxjcv9qa8m48ttq3wrvuczzbm6udm/69brr
  - Log entry 81384: process curl pid=12526 uid=24 src=26.213.141.5 args=dxa1ibx94/1rzx3z885hjs2l7mhb/jmjbtofu3/oi5 y--iv
  - Log entry 52734: process nc pid=6789 uid=177 src=102.66.217.21 args=amwbdj8voc8/zncimuneveudq7qwepxlz7kqu41v-mi2uujx
  - Log entry 60797: process ruby pid=12669 uid=17 src=187.20.214.184 args=b4tok6q/9a5e/i7j4cjx21kr9c0/d0hkyxmddenyyyhcat6o
  - Log entry 16525: process python3 pid=2429 uid=291 src=109.249.145.197 args=23t1e3qd11ydc-j97l-mw22ramww32h-4s8d1rap6zdbk4-z
  - Log entry 19432: process wget pid=15394 uid=505 src=27.63.40.4 args=pwbh 8wdrbz hgn7/y/470cwpxxhfy7k7m6qbvl76bmilczt
  - Log entry 34811: process perl pid=26774 uid=674 src=9.83.164.142 args=s5sveomnyjp9kh/ycbod1/kj9xsirbjxb0dppmwp-noxuihu
  - Log entry 35722: process nc pid=11436 uid=538 src=199.196.119.25 args=w7d3e3g/nsj-jz9y3pn96zi70xagm2yx00tppahnlyojmv3m
  - Log entry 36027: process socat pid=11604 uid=405 src=206.50.25.20 args=-0/-oudxi43r444eiq6p5lv1tsjwe12xr988/afav-tgm/jq
  - Log entry 99885: process python3 pid=6565 uid=146 src=207.114.229.88 args=/w3b0utn0rmf3jnlviv5jtdktidgrqaax6td3er61vlu6pl2
  - Log entry 20234: process nc pid=5686 uid=694 src=27.229.82.228 args=89isff0kst8a6pioqg5ylo0s2sptjz3fsy7oq-n017g-9j55
  - Log entry 23476: process nc pid=18453 uid=869 src=129.222.161.124 args=5gba9g0sgn2cz06h53p9xseodk88almutd9xw59euc0esh9q
  - Log entry 98075: process bash pid=20927 uid=535 src=103.211.235.128 args=fwi1v4uxnnrxn/ 748j9gvrh 4dbnmdrqcajzl3af2st38gh
  - Log entry 78479: process bash pid=11416 uid=755 src=7.84.243.169 args=hx44/v bdbv7l028qom1 1gckkd y81/enhfw/-yx0kfwnrx
  - Log entry 46581: process perl pid=21348 uid=895 src=21.35.224.159 args=7dao24m/ol1p ylv9vd0zow/u0e 1xq43vf2xvpmj3kdf2gz
  - Log entry 27017: process python3 pid=15156 uid=197 src=84.91.159.171 args=wlm0//1ydq9mi9bbndfys7lx6mcshspqpb8ngy56xqf5ksdh
  - Log entry 49382: process socat pid=28786 uid=527 src=104.242.220.156 args=s02fyng7glyi92e7k2nmjytfeu3pqm3-qzalm0mcz5p8wlru
  - Log entry 53744: process socat pid=12097 uid=367 src=48.143.91.184 args=o labiic/-53ezyy6qkglk/e--c-u 0xh052qi3k5i-c2zmy
  - Log entry 80896: process socat pid=28253 uid=255 src=68.59.250.29 args=-wmus-6co4e21ntdl9a-mda3dup9nvc4uhe65/yumw0h2v42
  - Log entry 70774: process nc pid=5129 uid=625 src=115.247.226.195 args=3k/2v/1am9vcmg4mdgabb8m34jmu7vcimyuezgls13gqkix3
  - Log entry 43101: process python3 pid=1815 uid=727 src=115.123.111.124 args=2r6ujh/y-07v3h4223-bgm6rfy5yfmm1ntwrlsxti7x/vyok
  - Log entry 53702: process bash pid=23979 uid=989 src=68.233.161.218 args=o3xh2r6vacfdgfzzns6i3b d 9h7oa dcoum/0bunechuhk1
  - Log entry 32668: process curl pid=24816 uid=256 src=82.206.93.121 args=vaurehwxweclo7oqzpav41-13243h9m1oma4p2705okp5v8a
  - Log entry 31203: process ruby pid=27498 uid=319 src=141.104.146.186 args=q 1y /06xym vkwrjby2/zw525jq09h04dir 117wi46mgb4
  - Log entry 39563: process ruby pid=23679 uid=657 src=204.251.211.42 args=00vppxtdljjqmb-51mby9us319s83ga uns-sehuxc jf9jl
  - Log entry 33867: process curl pid=14724 uid=165 src=184.227.193.120 args=50hm7eyp/whwt62kn3dl7lx1c0z/heujk3cqnvg8tcq8qvk8
  - Log entry 29487: process curl pid=14749 uid=358 src=51.84.73.84 args=77a558e1gcllv1uyetxb6gt6vix4cczwwk5sz7uwvjrc0xx8
  - Log entry 62137: process perl pid=30168 uid=670 src=144.6.99.44 args=g6ae/6adthid 0dgm-ht45ak-k982skps j 6wvimmlrkk3/
  - Log entry 27766: process wget pid=16487 uid=401 src=150.171.133.102 args=e38lgftuwa9aozf5n2/8np31amhy0-lf8d-6dwzhjt-o3top
  - Log entry 80319: process bash pid=18904 uid=878 src=34.110.84.75 args=6mfht3c0vx0vl5cl-u1tf7mnwnu4wj 9gh/2x2d1eb/-upu2
  - Log entry 29665: process sshd pid=3899 uid=907 src=131.102.112.244 args=l4zpp-  3y-2-tt10-wdh86y7441klzk10yy-d49mgdrlgw1
  - Log entry 74305: process sshd pid=26988 uid=716 src=158.175.145.31 args=lucdga9jbv6uy35e9ipk-43ge2k349yniwt1rl2 6yt2p8wb
  - Log entry 24219: process python3 pid=23733 uid=822 src=199.149.34.39 args=6x26a4h8t9j1oyhsrn62v/jt3s s19jh3pe//q2ad1zfxocq
  - Log entry 38559: process curl pid=15460 uid=792 src=152.1.242.119 args=/d-wq0l0125or792hltgku59hv yrt8r n15s9/ovd0-fi9l
  - Log entry 39474: process ruby pid=31469 uid=546 src=23.42.12.172 args=-8kvtrg/z7lpeaa/j1izkdm dg3 i6yvb9ts/szvv34l/-qy
  - Log entry 86404: process sshd pid=4839 uid=388 src=73.147.115.33 args=sewstv99xo-p1xdwzu6w1fbvaqdclrjmrnahmit4wtju7mjt
  - Log entry 54696: process ruby pid=24554 uid=90 src=184.20.25.47 args=8--s--4ck2 f81esiriey19nal5fr5f672cq3d/r-xkpey-l
  - Log entry 35154: process curl pid=27762 uid=728 src=216.86.194.35 args=k5z0t4as 56 d0octgbg/lpfn09bzqmnpwyxdhh2rr2v1yr1
  - Log entry 59213: process bash pid=2324 uid=44 src=51.7.152.230 args=bt t1hmny ip8-8g4j72n4xfv-zlu707n282w9e-x11gy6v6
  - Log entry 31435: process curl pid=9798 uid=181 src=19.249.112.160 args=xx8tf/10ettnima1glv/udmpn3fczslu6l 9n9fthm/wvdx5
  - Log entry 33044: process nc pid=22702 uid=935 src=210.255.125.182 args=imrkub7s7m ny3/r4ajlsexlk87d0mrwpje7kgoek-0nqch-
  - Log entry 85029: process curl pid=27762 uid=216 src=178.78.140.68 args=0azwxcct5uhwzlotrjj569x0aaqord7bb80jw 1nviaqdbbe
  - Log entry 26376: process nc pid=13949 uid=398 src=207.101.11.3 args=ezjdyz-u0l60a697kw6spv72ak2v08e3u2j-d4zoohfbq/z-

## Supplementary Technical Detail — Section 5

Automated correlation engine identified 23 related events in the 6-hour window.
Baseline traffic on port 41584: 1 connections per hour.
Observed traffic on port 4444: 195 connections during the incident window.
Statistical anomaly score: 0.901 (threshold 0.750).
Related CVE: CVE-2026-42061 — not yet patched on 9 internal hosts.
Affected subnet: 10.7.1.0/24 — 27 hosts in scope.
EDR telemetry: 2 alerts suppressed; 1 false positives removed.
  - Log entry 14956: process nc pid=12200 uid=240 src=110.153.253.154 args=i08c7c4a-vanvbxkk ikbm0sw2eguqbno-n266v 2ow0-h5d
  - Log entry 50101: process socat pid=28305 uid=356 src=67.228.123.144 args=d8 u9rjda8/ro4u9po-6oyux7fbj8qyuxz10ity44umf92r1
  - Log entry 38174: process curl pid=28503 uid=983 src=9.1.41.156 args=1 rgtv2jeee b6d7izjsjyk9ur8kat970niy89d9dfibk/1b
  - Log entry 61329: process socat pid=2520 uid=601 src=135.167.193.219 args=ye82rd6af2/h1nj9g3720zmshft3ar636l2ksy/ zz-quhkn
  - Log entry 79713: process nc pid=20926 uid=957 src=90.194.96.124 args=3y6dwy2d55e23hsy-p9dv/ocgn76i2ja9kjyx6-soj1ilgto
  - Log entry 16694: process bash pid=6676 uid=885 src=159.145.203.128 args=6dzse4v8vn2bwstq9z8jnnhi3x3dl-n14l4lwfmqz0wgl0-1
  - Log entry 86191: process sshd pid=8473 uid=877 src=119.27.37.204 args=z-7p dhtkp3mubnkl/y92mgspdq /-a89/xbbyebcszrs96m
  - Log entry 14693: process python3 pid=15916 uid=597 src=100.30.172.176 args=17o5cmadq/2kj3syff42mjqux9d ql4qs7ginfz7f39okotv
  - Log entry 50895: process python3 pid=13715 uid=430 src=9.24.143.92 args=chm7vtx8l1iph8oem8w0  786xrlinx a16zavc81trz1w50
  - Log entry 43884: process ruby pid=6089 uid=279 src=187.101.243.154 args=olgt1yyiivc87hwc8eo02fuuklr mg2jn9qk/hu0-lkwui84
  - Log entry 84126: process python3 pid=17247 uid=928 src=194.58.138.180 args=fc g4sapts/r-czma1ccvsu3riqabht4 p5nu9f2mk/-ol51
  - Log entry 20473: process wget pid=16188 uid=179 src=110.88.235.134 args=hu18mn2n/co y4fbti4yf-lkt2v87bdcjads3557per2pm9d
  - Log entry 23454: process sshd pid=22061 uid=992 src=162.72.10.19 args=yk4ekfcwczppiozxv/s9lsb0ymz--8dwzsdscrj/9hmn2jj6
  - Log entry 59755: process wget pid=16257 uid=698 src=52.176.143.87 args=s86e/qljo3got231rr9l95b1non6 umj0pg-ozb-n/pi42bs
  - Log entry 60318: process python3 pid=10870 uid=879 src=171.236.102.238 args=y u-80u7h5y89dzt1sxufo7fgfnl3vyogyfg79r09mxp89z2
  - Log entry 84973: process wget pid=12029 uid=732 src=167.213.101.137 args=andtl rbkzjy1i9j640rka/9x 4xaf/v8ozc7xr-ul9o-jad
  - Log entry 18947: process curl pid=18679 uid=919 src=86.116.144.88 args=bsnp wmnzfcffi64g0wvtrs1m8xw1mmsc-oq5 o5n r96lzg
  - Log entry 81041: process socat pid=29466 uid=725 src=92.68.116.86 args=zxvebrr7/u3n9 93h8/nx6cig3op2o2n3cymbw8ky289-p14
  - Log entry 64187: process bash pid=8673 uid=479 src=135.182.22.20 args=fafyo/ofkyqu3xzp-smbu6v-r9tretboalmlphd37otzs5fw
  - Log entry 65673: process bash pid=21490 uid=733 src=21.16.50.195 args=57rxw1bflh 0nds6n58j b6x5z7/juc 82qmxh1-pcxw0h22
  - Log entry 85148: process perl pid=2459 uid=564 src=71.232.80.1 args=n0/nmen8qywj7-7mz9v3qve92/6hsom4k299p9c43hre8-r-
  - Log entry 84599: process socat pid=9821 uid=190 src=217.139.81.46 args=rkweupjduct-ptmoxr22np9a-/lde600ot-kzj1a80/bq9c5
  - Log entry 46995: process python3 pid=10518 uid=497 src=141.196.138.245 args=vr20w713ft367apm8oll1mpvxojba0ebd7493fekbg-0q1 k
  - Log entry 37134: process socat pid=29207 uid=616 src=115.188.162.155 args=wmgt2m7nm4k4-k0gb36n-u8k0m6prscuyfoegb6gv1ekk-6a
  - Log entry 47320: process curl pid=31697 uid=119 src=146.50.185.28 args=/6 -t1-w5w1n0nellh7ke6on2bdwjt7i/o1-77aarufyn6 6
  - Log entry 74635: process bash pid=28318 uid=421 src=169.237.173.218 args=5grydzyoifo v no4j8x93agbs3x1-8uk24dt6ku 38o8yko
  - Log entry 46231: process curl pid=18862 uid=960 src=114.59.254.93 args=xo3ixs-fjgcnrsgnuk-xf4e3dus2fm-i69-y9ogje5o5pdl5
  - Log entry 23464: process socat pid=16619 uid=160 src=190.212.96.154 args=wy7s5/9kwha0ptpgaek-k nzjl4tvugb2l 1tzebt4fio8g3
  - Log entry 36065: process perl pid=19681 uid=736 src=205.118.51.91 args=fz54f5z rvrudxdqkwpsw0znk8/d02gjbfhyut8wfolhct7f
  - Log entry 25953: process sshd pid=20996 uid=223 src=128.203.74.164 args=xgrbz6m9/w47a-13blz/-t7izaw6akd3gxf wllxxr30/7tp
  - Log entry 69265: process ruby pid=6362 uid=866 src=32.15.147.118 args=8sdrkg/zrcftj5nfse12uvvnqi9juesqjun4dws8/0hqx4ys
  - Log entry 97108: process nc pid=7467 uid=607 src=78.149.173.4 args=48slracoro48-un61mkk6j8pz-pznz5pzrg1rsqz80h8-hih
  - Log entry 88630: process nc pid=14182 uid=27 src=133.150.236.60 args=cj5syuo/6l7fqm0/8mk4-2q54at8qmctjmyrh3fu5eexc63/
  - Log entry 30323: process socat pid=9595 uid=180 src=109.159.33.224 args=qyqoyfujzw3vmvj/lwzeq2shei6a cdytyri568te9i32e h
  - Log entry 12533: process python3 pid=19207 uid=373 src=55.227.32.150 args=94oqlc z csczvqlxlz930tel2yu7yipnd7dte2-/j7-7vkt
  - Log entry 21810: process sshd pid=24189 uid=108 src=161.239.238.182 args=3tkw6i-242i5ugqta4s4q4oek sgc30n6urs8zp7ioqmgl2u
  - Log entry 19524: process ruby pid=16984 uid=849 src=132.47.172.200 args=r76a7bwuqh3l2-kqdr9vw-bi5x/vbd-ck0t3jd gxzk 9zwm
  - Log entry 50440: process python3 pid=3477 uid=280 src=159.134.4.108 args=zikndof5dgl6e2dh1bc 1clv/9f2fx08du 27ay5yq2k-4vf
  - Log entry 70307: process ruby pid=7310 uid=18 src=210.208.234.110 args=85ksszitk2cq8 8w/jzx0jbmjytu0tyytuef 4/cgn2voe f
  - Log entry 36979: process socat pid=28411 uid=555 src=138.38.60.1 args=cb xp1esj2tgcx2pt bmw3dxll0fbhqmjom35ejuujrw0a4v
  - Log entry 87710: process python3 pid=6961 uid=292 src=150.89.200.93 args=4mm78izealdqkintmuu5yi0dm0 stfz/h3-eh9wz9nsc3d9s
  - Log entry 92091: process sshd pid=15157 uid=459 src=127.48.216.220 args=yhsk6rha68w86uz0hrcmqhyng7/nb-kp0st-e0zk1q4wv0vb
  - Log entry 41173: process socat pid=9032 uid=160 src=133.99.103.210 args=mp/f47w/otfxjjgg6ra 12hfm5nrsnitgeszrt0q4x8sij-3
  - Log entry 37297: process nc pid=1677 uid=879 src=41.34.146.216 args=5v83y tw1/6ku9e2byvarco iuaufn5nthl-9hj18 uw4gsn
  - Log entry 46323: process ruby pid=27007 uid=480 src=211.48.53.202 args=ze/ctr3kw4u2l2vig7/qfhdzpo0mduzskf2yjydr180dovzw
  - Log entry 59762: process sshd pid=25104 uid=114 src=19.125.131.77 args=s slxy3b/excex84ryqn0o75gbbp4afjk3bz/z1zmcocv58d
  - Log entry 60046: process nc pid=31483 uid=849 src=63.187.143.46 args=7n-8nyax90nr/n tfrdtlvt/hmkf29bo7e8fwkujeyv70a5x
  - Log entry 62129: process curl pid=2866 uid=925 src=152.250.132.53 args=q wlh/nwz7zm2 3c4ubcqt4oq4//dno-hz2z6e9y4ztwp7pw
  - Log entry 31530: process sshd pid=13631 uid=272 src=206.152.71.71 args=-4hyirs0azsw1wvr-dym25gg824jl4is4ged3z33b7amd6ul
  - Log entry 56526: process ruby pid=17310 uid=763 src=68.32.126.59 args=ix fokvvatf87-jnx89gihqfc1dvgcabl0hl/-3xizr ri1g
  - Log entry 33169: process ruby pid=28987 uid=402 src=170.228.70.154 args=h3065gi2jffawu67ewveyuf1v nvfdzw773gkr1ia 6/m9xf
  - Log entry 56457: process python3 pid=11260 uid=87 src=192.21.20.108 args=zd w3u84qggs9rwdaslnnepq9/z0-odmmg/6-we1f/4pzn/w
  - Log entry 54650: process curl pid=10180 uid=286 src=79.168.215.47 args=yaebqb6t4qjyb9j6poi2mt vad 91x8ugsj8nywizcmz6gi/
  - Log entry 43119: process curl pid=11240 uid=971 src=67.196.76.95 args=aqi0fj k5a--miibxjdsomtjflfjf 7a/3umdyafpsy5k5ug
  - Log entry 10365: process bash pid=22990 uid=958 src=118.203.242.190 args=c 21xschj/gv/sdy396z161apt37nr3 b88cuxroz-m5f6us
  - Log entry 62962: process socat pid=7117 uid=839 src=140.238.211.12 args=w6g3d2r53 drzd64v2k6h3pgg4c-f8a1q/j433/umqfxlc6c
  - Log entry 27557: process nc pid=8943 uid=426 src=53.20.249.124 args=hq37msln/0ej76o9rd5btkk93kwl/ax1z7t62-p6wfa3539w
  - Log entry 28030: process ruby pid=24691 uid=116 src=85.183.205.224 args=ukig-oymap-9adil3iur99osz/wdyv4zybuu727w8qj-kfqi
  - Log entry 53005: process socat pid=11458 uid=204 src=186.208.171.73 args=dq6d1q4pt18lbm-q7 yxq/mfa6aa7qd/taxu84005/ i12h2
  - Log entry 57088: process wget pid=20182 uid=749 src=205.226.79.146 args=5ic6wsf -qwki-6mq 0zkfb nf1//4o36maj1rcaqs8dt6xa

## Supplementary Technical Detail — Section 6

Automated correlation engine identified 25 related events in the 6-hour window.
Baseline traffic on port 65155: 4 connections per hour.
Observed traffic on port 4444: 51 connections during the incident window.
Statistical anomaly score: 0.951 (threshold 0.750).
Related CVE: CVE-2026-35347 — not yet patched on 11 internal hosts.
Affected subnet: 10.5.3.0/24 — 14 hosts in scope.
EDR telemetry: 0 alerts suppressed; 3 false positives removed.
  - Log entry 31228: process python3 pid=31010 uid=703 src=66.125.90.213 args=lvq s-z3ieovyc5jgn4yoa9je729xm9gm1uxrh/87k2w5c2p
  - Log entry 11469: process socat pid=27553 uid=783 src=22.146.211.138 args=j3o8 pwvwls6kwnbd6ba/9fucujp1e78e-mt88z gotnhrem
  - Log entry 93995: process ruby pid=14004 uid=647 src=209.91.46.54 args=ryuscbmj95u-3uiuikevdhszg61w- zt3kh b6j8u/jxnivy
  - Log entry 20233: process ruby pid=7629 uid=541 src=48.213.28.35 args=/rtd2-g4/9ou2houhqfobzq-lbfgfw20n4ffp-1dxy7e44nd
  - Log entry 82777: process bash pid=11308 uid=648 src=81.88.230.86 args=1ujrtarn0eqa92frcc iqg/aj1qpto717foswp9c8f42j 84
  - Log entry 62329: process bash pid=27927 uid=109 src=201.113.143.59 args=1hp /y0bl3qd99l 68l5hp3e1ra191fw-kn5y-ninqbkptl5
  - Log entry 50827: process nc pid=21742 uid=866 src=164.20.64.71 args=um4pccss762y4tk/7ujdftmre5nj78q3yhk64-bd9o5wmvx3
  - Log entry 28806: process ruby pid=6336 uid=107 src=197.239.6.223 args=gr4b-yc t3uzrl147h98 u0rqwg-j6zbfkefjcsiset8c52-
  - Log entry 95915: process python3 pid=6687 uid=221 src=157.199.162.105 args=rkmuvx31wde92d 6eq451vg1-7tdqx-5ox0iorrvprulcld5
  - Log entry 89722: process curl pid=17172 uid=373 src=149.244.61.112 args=hjp/8shg-/biu5sqifzpv21zxb/lftysim34nqnzmuj4uaj2
  - Log entry 64514: process sshd pid=16432 uid=404 src=157.140.193.77 args=bgve1c4zzpl1qmpolk5p ynz5fsif7z9j0odkzp04tqmaxu2
  - Log entry 68512: process bash pid=12980 uid=5 src=63.217.95.70 args=mv407mc13sc1fkqgr3wq4xvya6iyfoord41bscvfyq94y-xw
  - Log entry 45607: process wget pid=1172 uid=623 src=91.47.58.178 args=bm8kfulcac/ so0vh/7thm2d1geql8mobbrxev3urgx3f9w/
  - Log entry 46703: process curl pid=10537 uid=991 src=21.250.249.116 args=pds34z3s7ueenpeast1m-7muelrc79u dk4e31au3rxx/5t4
  - Log entry 29221: process curl pid=13325 uid=210 src=125.157.32.244 args=qg57botb jrhe7nmrsfex-3ctix7d2cyezrp0m9xo lfxh6a
  - Log entry 93555: process python3 pid=5005 uid=29 src=183.162.198.232 args=4j1viikqcwm9s8315waen mad/y6vu763vjtdtzjhov5i46a
  - Log entry 76531: process sshd pid=17317 uid=538 src=31.140.72.92 args=9vidz94hqvltfqc6vy 3uhr-3gob2dcn/q3ru4/f 89q5g4f
  - Log entry 68038: process socat pid=12760 uid=925 src=120.49.85.85 args=xnrrzgpubx-9lgsnh 3jm7/25ellvba0krtceqgimtev jpw
  - Log entry 76090: process python3 pid=31627 uid=209 src=32.11.68.153 args=box53tnywi5a-9 i9jve118chxdvkr c2v-d8wm700/mhzg-
  - Log entry 88828: process ruby pid=2815 uid=110 src=202.247.126.132 args=0gc7gkvd4bo-m0zdlszef959zn9giws6x1bay/557cai5qdi
  - Log entry 27272: process ruby pid=8205 uid=290 src=150.140.147.96 args=0hnaoc9ork0x 56 59x /4yh0bpaiv99cvumcou/7xy5n/1u
  - Log entry 47225: process perl pid=14859 uid=432 src=156.154.20.40 args=vxftcfk 5q13t9d9sw17jz53 8nouigykp8u0/6vfalp1m2j
  - Log entry 16880: process bash pid=1147 uid=839 src=186.74.72.182 args=bgck5z3kqx11icqyl6bzt lo6vxjnmo1 1mc/ywg8axtzkjz
  - Log entry 47534: process socat pid=11856 uid=376 src=157.185.250.28 args=h9z3 tadr0 8//qv5ed jln9648h9pqoh603c36eichdflrn
  - Log entry 28346: process python3 pid=23723 uid=282 src=110.38.49.78 args=z iqb4v381v6hg9-k-vk2jd5rr0gzj69bjhtlp4zh2cutppj
  - Log entry 99364: process curl pid=12977 uid=262 src=156.88.53.227 args=ft3vasu-s778cnj8mhbrxfchohcjsh1cxsg2v5yt229chie9
  - Log entry 77700: process sshd pid=10972 uid=0 src=186.235.57.55 args=1z39bbe5stbhskuad6fltlnpb9le8hvkw01rodzsgsacv/4/
  - Log entry 47962: process python3 pid=19631 uid=176 src=100.158.235.231 args=wnor1v rirybb4xc16/upzk/p3x4w6xjoiny3 633x20rspc
  - Log entry 55796: process sshd pid=22692 uid=639 src=100.177.233.85 args=-i--3cyjrlydgbqz8bdcwb0rz0z-ys7nj 7tgtcc90mngd0g
  - Log entry 80279: process sshd pid=26640 uid=616 src=3.55.244.190 args=xmqxa4b3r45dzvp-97/gfm8/a9okm s88hqydvwrjsqv1ib7
  - Log entry 82382: process curl pid=8092 uid=454 src=100.225.31.137 args=drjl2gxyc xpxw9486idsg3qpv db1ytvabh3wmujjnmyw6d
  - Log entry 33738: process curl pid=17564 uid=423 src=51.193.234.141 args=t5x6wpt5tb6/hce9w88la cyidg juwetut9cnbmndud86a2
  - Log entry 54563: process python3 pid=26018 uid=803 src=114.44.7.199 args=9s3cxmpo6nyaypm8tkui9mt4f6ucjefwd5ehk45m5d/y-dtw
  - Log entry 87399: process sshd pid=26708 uid=272 src=161.6.223.136 args=7d-srxl0lxb6ntrrx1xmarrm199hih7gf6xzd2 hrg0mfi2r
  - Log entry 46570: process bash pid=21451 uid=970 src=11.121.242.80 args=am21lz/xgur25jble/a nxrk98vr5rryg6028nelld jr7 q
  - Log entry 66553: process curl pid=27095 uid=188 src=3.228.106.237 args= bgh-spd36icim6wqi8a1r931d0vjc71k9ksuiqzf4imrygl
  - Log entry 58792: process socat pid=6719 uid=327 src=218.107.250.61 args=krfqw6hkwy2zcyrjxihu101dkn0-732xpvaa0xvt-2ipur/e
  - Log entry 18943: process ruby pid=28467 uid=974 src=98.227.48.80 args=kvyt0q 5enhp6ez9ar2jj2/5dxi-96rkxvo2tueev27kp yw
  - Log entry 19075: process perl pid=24241 uid=637 src=106.223.170.187 args=mb0ko zlbk 0ede5snehfuto4zcnhfsi/g6dkypg18i5qtfq
  - Log entry 65674: process bash pid=4630 uid=866 src=115.46.202.11 args=kslwz96448-f19vo6ilpb7at6oet40pwnu6wrj nr3ny2-1v
  - Log entry 84535: process sshd pid=19698 uid=802 src=92.21.37.250 args=danc1r6c- 5hcde182v2exkk--gdeu 8pr ker06slbu asa
  - Log entry 87992: process socat pid=12610 uid=651 src=78.254.16.160 args=wcf4q2h4loj3nzcb7sahkj jx8fhp qf26rtgemfoij20zwr
  - Log entry 71693: process ruby pid=10991 uid=857 src=98.92.135.191 args=zsni4/oalptovu8zskxurrd-n m1pd48rewb-zmckrwsc1 7
  - Log entry 64459: process sshd pid=4098 uid=740 src=130.77.117.164 args=5tc 5cjx-3b57apsddsch91g3-667 7pox12/fz020vzvzyq
  - Log entry 33497: process bash pid=5113 uid=251 src=73.4.230.197 args=pbsy7xooq-7l0-r/lbi2qx0e3tllcyl/v25uk/kgrf8rcj2s
  - Log entry 27512: process python3 pid=13203 uid=202 src=209.135.93.144 args=8bgv clt2iljv6gh5azbf 90sa6y8-krr/rcn8n89bmd0e07
  - Log entry 23394: process bash pid=19018 uid=96 src=75.252.193.220 args=u78dpzc8izq4kjey8kf1g0j/z64i9144/ofr64 /ehkh6pr1
  - Log entry 11174: process wget pid=24209 uid=909 src=214.230.106.220 args=ce49gzqgk4hfcy0-3igm9k11ow-7pe9a5a m-s7c2g0789ny
  - Log entry 69739: process curl pid=2029 uid=760 src=78.141.103.201 args=8gxwmiyi692m4dqu4-5ncqakpyfst-88/0 irwayhoh466d2
  - Log entry 73808: process perl pid=13919 uid=856 src=157.2.233.25 args=lgtifq7lhzg20lu 43xw6ark2ghwx9b/5b5l33jh61soh8c5
  - Log entry 86981: process bash pid=29334 uid=584 src=192.24.47.14 args=9mmz-2j5ck3rtm2wn3qo/p7f7idu1rjqv9wb9/ z-rj-te p
  - Log entry 42273: process ruby pid=6620 uid=664 src=154.184.62.232 args=dakw0s4bm8kiv-k1xajkyd n1k7gyuurdvez muorxxsk7z2
  - Log entry 44250: process sshd pid=25758 uid=786 src=189.192.201.16 args=zeihxk3ctdv-8wjgqtogkv230k-waw89g9rby6lak6qj6a9v
  - Log entry 10744: process curl pid=15952 uid=460 src=151.111.179.127 args=qlyvv8ceozvzux4aktcxs8-66yixd//qnoo/zzw38p74 ffx
  - Log entry 66521: process curl pid=29859 uid=843 src=117.72.148.175 args=288uk83/-ohbg745 sklu/47wiho 1ct66ypqg9vtxpkmg/7
  - Log entry 54171: process socat pid=7375 uid=468 src=155.174.195.146 args=27iomy-ms 0mfpc/9eq dd0t-psdhu021sub3d9zas/24glr
  - Log entry 99490: process nc pid=8088 uid=130 src=120.55.115.146 args=2kuj47vy50x1fue5t1172mk6oi9odtlenmxbo-p1-d53a5/3
  - Log entry 99512: process wget pid=7990 uid=254 src=147.241.138.36 args=-lg096jhz69a5iu972xwy8jj22litv-xsm owbd1kd5ocm 9
  - Log entry 40184: process wget pid=8288 uid=255 src=81.36.173.82 args=zqjbnr2oo fmo0h95z79/rkj81vornu7aaq c0msdc0t1t/q
  - Log entry 26240: process socat pid=20816 uid=733 src=89.107.67.78 args=d/0fntskzxz6iqwu r7g-g-o7os8b  ec2rhx79gugn2sop5

## Supplementary Technical Detail — Section 7

Automated correlation engine identified 43 related events in the 6-hour window.
Baseline traffic on port 10649: 3 connections per hour.
Observed traffic on port 4444: 92 connections during the incident window.
Statistical anomaly score: 0.885 (threshold 0.750).
Related CVE: CVE-2026-20732 — not yet patched on 1 internal hosts.
Affected subnet: 10.5.4.0/24 — 19 hosts in scope.
EDR telemetry: 4 alerts suppressed; 3 false positives removed.
  - Log entry 85278: process wget pid=19500 uid=260 src=193.193.106.65 args=-5a4k0sn-5 env0nh6i06k1e/azt6nr-d2p8-xn0ydvtihqr
  - Log entry 83529: process curl pid=13064 uid=986 src=162.94.236.201 args=ssd d8x-qx2hs4l/plxqub82688llqjev  yjxzuxb 0-550
  - Log entry 35412: process bash pid=15463 uid=261 src=127.187.13.89 args=k/iq-xxy1cmte/ckk3plhp1101ysb14/wmiw195n/iwqjia8
  - Log entry 66395: process nc pid=14346 uid=365 src=34.0.117.50 args=bwezxsho q48n5iozh31i1rvgyatjc0b144io47iqrerw-i3
  - Log entry 16807: process python3 pid=18748 uid=256 src=9.245.94.15 args=eov2/kurgm3qe5vc-dyh jrix1y294lwhfw6k9kdwygmbnw5
  - Log entry 14280: process ruby pid=13510 uid=448 src=158.165.35.119 args=h2hn5e330-6wv2oaiki16rej dix3h/kzjyq6vhid9tshywv
  - Log entry 54830: process sshd pid=23269 uid=657 src=118.186.45.172 args=i58guwd22lw6-p9a10irb33h5vrddsi5d088g2gw87eajv/s
  - Log entry 42500: process perl pid=3101 uid=598 src=146.112.52.47 args=gy31n8yb2t5t8qxelfd1li6z/i3ss16cz1yivtr7wixbftma
  - Log entry 62270: process python3 pid=8473 uid=485 src=55.203.131.56 args=g/ygdj/-syr6ai4h1kcf8s6tvobd8-lteoa0gtp4 pwbuf s
  - Log entry 23914: process python3 pid=20618 uid=482 src=25.113.217.210 args=p8c mzj4kesirabscxa7e3-0z9dn2j3/z ic6ujjes9yzdte
  - Log entry 59242: process bash pid=18054 uid=150 src=203.232.204.195 args=qv30s01hedx-qxf2y3jdkogpk0-lf o2gsg4a9hp0q244t9d
  - Log entry 22236: process sshd pid=10786 uid=4 src=52.84.56.235 args=jo2bxp18z-ik52fu6q43wobhl45w7fonsqu7oo0cnmvd1-n-
  - Log entry 14629: process sshd pid=12110 uid=635 src=100.225.52.238 args=k257e/kaxqjw/r0vjz2/7rz-jowu-tus6n---l6xwej263xh
  - Log entry 51774: process ruby pid=10061 uid=12 src=70.100.32.88 args=1psgnsr er972von1aj5krk4s/oxmwgjbtf8plboi9iwlbzj
  - Log entry 68149: process perl pid=9492 uid=304 src=91.41.165.222 args=n0gxmfmwzv-s-o x8cj8yqqfvrqxox-posn5gwz3bk-a3rjj
  - Log entry 75042: process curl pid=7655 uid=648 src=18.162.48.172 args=28t6eb t7v-mj9e0p8clcgziweg/-0fnhswc8//wcpt3r/4q
  - Log entry 78790: process bash pid=16805 uid=672 src=142.233.226.81 args=l3i6 0o9t1 h7ighzwk5d3e pnugpj302v/f5kilf9k5i ef
  - Log entry 59382: process curl pid=7869 uid=359 src=171.134.60.217 args=q0u7e-7fb9b4cm //89p3mxgr2-54gxfs p8bwi/anvqvlxh
  - Log entry 46932: process nc pid=12331 uid=828 src=109.60.227.209 args=3hylb8iufn6x mmpwge4d8eyrq/x3n2vxzk0ffbabqkwl2ei
  - Log entry 76291: process sshd pid=1204 uid=816 src=70.244.116.240 args=8ptrqinfr73s ggns8 0-qxd45kdor0bq5el34f40ck-xfwz
  - Log entry 49390: process sshd pid=29804 uid=503 src=177.27.78.86 args=0f8gz-a072w7os19jmezvu92/4okl9pf8loeuapgcsaeycdo
  - Log entry 27123: process ruby pid=27068 uid=530 src=2.166.39.170 args=w2zju76vo51/cgebubjrnd hxwg35clsee8svn-xe1tw/mfe
  - Log entry 36524: process bash pid=6283 uid=666 src=42.37.21.4 args=bh8cgkm2t46u0lr54lmr784c16kjdxom62 z870dt7zyxnx7
  - Log entry 73261: process curl pid=26150 uid=591 src=135.243.211.111 args=ibj0m0-b3gp6bedrkp500drviqpka-9n1af9t9gegy27qicr
  - Log entry 52182: process bash pid=30217 uid=930 src=53.90.208.126 args=3hdrl8i0-9dzj4-hjdgj/nve-6yty/0aboh0-241b52qmh76
  - Log entry 64082: process ruby pid=3745 uid=443 src=51.35.77.222 args=2dxwca/5vfjd-o2xv8tviu33a7u/6gxl42u4sts3nauv85kl
  - Log entry 32236: process perl pid=25518 uid=124 src=2.77.187.153 args=l/cxt9074cb18-uo2b3edh/ms8x7d5la3pfp4yb54qovv6tr
  - Log entry 34616: process python3 pid=3627 uid=355 src=80.1.190.31 args=6/cu6rprka9j3qibskb71fvxejy4ji4vz1c5/9a/bn70n1ek
  - Log entry 90098: process wget pid=25427 uid=19 src=98.121.121.49 args=0t/e4y1kvg91f-wof115inulohv6xvhqg zt5bifa-3i5b/2
  - Log entry 97066: process socat pid=15318 uid=714 src=12.231.139.42 args=9qe8ljpmiwler9 qpld7qzo09lq8syn739ks/eogsd/eaosq
  - Log entry 40950: process curl pid=23818 uid=893 src=19.158.123.38 args= fsnb86ea4pm4q89wl7k6i0qb826d7cqagpuziaakgd665z4
  - Log entry 89484: process perl pid=1733 uid=602 src=4.190.205.150 args=1zy5x0rhrb8fucwses48kqz5 69-b t7q5jikn/ge7c2/s7i
  - Log entry 67271: process nc pid=18947 uid=933 src=20.139.57.65 args=vbmkz7024dib6eezjtp5h8a /p 7hwkwnrxwh72qbdfij4of
  - Log entry 70450: process wget pid=24150 uid=50 src=168.13.83.118 args=lr2g-1x307z3lvbwrnz7qxgbbre-3kw dc4zeko/hvqz3rc9
  - Log entry 91103: process wget pid=31612 uid=41 src=98.13.188.176 args=k-aqrvl/97o2oh-32eg9g0yzttcd8clkk9gu/6rco0d2nayd
  - Log entry 67741: process bash pid=15156 uid=880 src=82.114.5.176 args=6u/r2-sbv17umc8ri4let6p/7n-58ka-08qxpjw9zcxdnxv9
  - Log entry 39748: process python3 pid=28571 uid=384 src=74.124.246.161 args=7478e2wj1hisrjz 8c2k-mwog-six0j5a/xzgygots9rsm92
  - Log entry 34154: process perl pid=22296 uid=477 src=94.163.63.9 args=ge9ijtdxni8pqion5/zgaurvlo2j7714k72gra dpfe07psa
  - Log entry 90854: process perl pid=30450 uid=663 src=94.119.64.143 args=z-a9ny19qff9kt8r9ii475a9r40ni9iwzjer-96w13voouib
  - Log entry 53920: process perl pid=21622 uid=825 src=42.237.45.222 args=dfbw00c/8w7lk08aos5ckoxv9uk-jxe4a fq0rkmujyj3sc2
  - Log entry 68645: process sshd pid=1856 uid=746 src=36.80.207.9 args=tgkft1982/uo31lqujor94gqwswig0bjijnwyf664z1irabo
  - Log entry 49803: process socat pid=20122 uid=649 src=9.219.183.138 args=u2-u6bw2l3sey-2rmt224u001zx9o oj1bee/hqs5n8tq0mh
  - Log entry 96963: process perl pid=29911 uid=975 src=208.191.143.221 args=8hk iq/ics1jm4zpyb6lp0su6h xt8z8v6wmh20gex27ykto
  - Log entry 30695: process ruby pid=15161 uid=58 src=129.115.118.56 args=galt53dbi08j91rlzz6bd4bm/7ryqzf3terbxsddhlf2iz1y
  - Log entry 33512: process curl pid=21599 uid=214 src=185.203.3.2 args=799hy0k4jheve5/mkc7hbwm/qqnsvxz732612-8yv/g6ti00
  - Log entry 87695: process bash pid=11543 uid=497 src=41.99.239.229 args=s-1a3wkcktug9tyosiknuzxg1mi1ihig4xt-5logyu78lx0o
  - Log entry 21987: process curl pid=15081 uid=828 src=61.5.33.237 args=/g9v5gspzpo5uq/w5256nc66whjl9e32l7qrfido5 1f3-s-
  - Log entry 54977: process python3 pid=11550 uid=649 src=152.207.142.68 args=4zafxn5gd82 hwmv52j64jg k8okkthph2lzelouk0tphscz
  - Log entry 55221: process perl pid=13854 uid=105 src=12.157.242.71 args=lg1d71rhlbarp8-  78fjhvjbf1jzv l//zsg3-ktci/fbrx
  - Log entry 49057: process bash pid=1718 uid=496 src=105.245.84.178 args=80 8legyx/af6m4xqgskn0924h7cq93oejvwyj7 7dxc4mgf
  - Log entry 80536: process sshd pid=23732 uid=25 src=64.229.169.63 args=5-ul725 x2efg416/-dvl0go04fpp3dw/081ojo51ol2f9zk
  - Log entry 52145: process perl pid=19967 uid=57 src=94.232.19.24 args=zloi29ll-8c6a8jpovxy60ufcooek34nqzn7-6reuh50nj76
  - Log entry 87947: process bash pid=26830 uid=644 src=107.27.214.236 args=k-jdx46i059x8ia b06c0vx2qndt57tx6thhu3ietl329epq
  - Log entry 52749: process wget pid=7329 uid=282 src=180.154.205.59 args=on/5it8g0x4lq80d 5r-gm1ykglizwkobtl5u6e29k5pvvlc
  - Log entry 13918: process sshd pid=23600 uid=434 src=162.61.194.118 args=wc-k32hh70zjp68x0s29q-zgw1zlgouzdjyrxmztx2 /wor7
  - Log entry 78981: process curl pid=3980 uid=928 src=96.238.198.13 args=98iemqdyg6pqck6w3w9v gspkw52ju0 vk4 r0a7oaodkq24
  - Log entry 81623: process nc pid=3747 uid=96 src=128.105.43.195 args=o123g3vdmf21u3q30eyv9-65ja5efsjj wh92-sfn8yxbg8r
  - Log entry 16176: process python3 pid=2516 uid=256 src=1.134.21.113 args=nzsrgej5saw2/h0y3zxzcg8e5oe4ljrw8 aimmspghs/yvdt
  - Log entry 52294: process wget pid=3339 uid=390 src=79.92.49.138 args=s -0  9a15aqgdaz66b5m8mbo4inpg8gjx-on5bhd4e70 gf
  - Log entry 48803: process wget pid=11269 uid=166 src=99.248.34.156 args=8oon8ake8xug0gdmbex4zif-j86pi7kg8y45abz6erk7htbi

## Supplementary Technical Detail — Section 8

Automated correlation engine identified 34 related events in the 6-hour window.
Baseline traffic on port 21040: 0 connections per hour.
Observed traffic on port 4444: 76 connections during the incident window.
Statistical anomaly score: 0.806 (threshold 0.750).
Related CVE: CVE-2026-40635 — not yet patched on 19 internal hosts.
Affected subnet: 10.4.4.0/24 — 16 hosts in scope.
EDR telemetry: 4 alerts suppressed; 2 false positives removed.
  - Log entry 81729: process bash pid=30914 uid=80 src=199.216.84.99 args=wmjdvycm/jmp5619u166j2n3d0t64u69ygoekybclddgv2r8
  - Log entry 65349: process curl pid=19946 uid=457 src=136.9.202.24 args=g4ka7ql9zgq0na0n0w4s3kbz3x7azc8rw0nxjarlv5dt9tik
  - Log entry 36421: process perl pid=26076 uid=800 src=196.114.80.228 args=4t0kgwlc1tg3 zf301ybp57qp755gwzvnnts9 66i8drh1cc
  - Log entry 40395: process nc pid=8596 uid=7 src=217.7.225.207 args=27dd5/w47jaqiv6dslfvnjrgk2rre1hn35i6vrber5lwp-mh
  - Log entry 80401: process nc pid=17084 uid=495 src=210.190.125.96 args=qtt6gpupygz1x0cvm-qkxwdr0hwl9nva95ne92n62/i5z/ve
  - Log entry 24707: process socat pid=12007 uid=599 src=118.126.173.172 args=8//20u rl6xv8ny5ho-oednasspinkx5nz24i0imcdv1rgi9
  - Log entry 88596: process perl pid=25371 uid=115 src=154.235.111.97 args=55f2hdt7yf-7vddm rv2av53gasnx7/aruflqva0rup kyqi
  - Log entry 23099: process nc pid=1616 uid=224 src=128.12.81.14 args=7/p4 ip-pj/vmoxj3zmrkls8c83uhip5s67sxy2-dm5csfe9
  - Log entry 67724: process perl pid=20911 uid=356 src=116.146.97.171 args=- 21-basm7qe8gvpva3/1g/89yly8qtonekds17wjjuz2g8-
  - Log entry 44995: process wget pid=7110 uid=496 src=41.163.121.187 args=stu-n gaxaagyawtxkvsussdrz3j3cq8hzii0m0-lt/u1 4o
  - Log entry 25291: process ruby pid=29524 uid=115 src=34.103.250.232 args=3edooz98pns-y93mj/nijj9wes8ry6gzrajr6z39zad6ajm9
  - Log entry 80941: process bash pid=15904 uid=678 src=133.21.9.209 args=gr9agfmyg4n8a7t06lp9bk9yc5e7mx/kw0s 077gkv0bcco5
  - Log entry 92851: process ruby pid=19037 uid=101 src=137.101.180.99 args=kz4t4s2r-- uyxj060yj364u20c4gn0nosnf2a3zlhqob5ok
  - Log entry 24593: process perl pid=7658 uid=693 src=5.136.191.117 args=1rdj hahtddxm3-p7desb1f-25cy8odeup8bnm76fze/yvjm
  - Log entry 32778: process python3 pid=23555 uid=592 src=63.74.36.133 args=7 x5hzj4xz42ylvtxklxpm4cdqf0n1/iqfv16l-/i5c24vlw
  - Log entry 76354: process ruby pid=19648 uid=178 src=118.151.16.226 args=jlp tslm -wgcdfoow/2bo v as3zwzjd0wn/kx-/p2ec3-q
  - Log entry 77825: process perl pid=30970 uid=297 src=63.70.237.209 args=sg93/tyka-tjojys 7uo-jgneogz86lr9/c3ho6e71sonnh7
  - Log entry 25119: process nc pid=10844 uid=370 src=19.63.246.11 args=n1c-aeot3p-r55mb56n/t7fot57szn8vf 69jn1y3u1rk93a
  - Log entry 16849: process perl pid=14292 uid=462 src=78.112.187.204 args=doltq79u4cq6619usrpc7swatbz02alo1et4b y oej862rn
  - Log entry 33216: process ruby pid=9030 uid=41 src=204.117.151.166 args=oox3rqub9 b3zbykzsu-nfq/6avwey09alwbt6x-6l0jinq-
  - Log entry 39472: process socat pid=7232 uid=500 src=202.110.237.157 args=7jcph4d s xtk8-6zbwo4zjop lqyatl0coay7r9nx08mt8q
  - Log entry 15739: process bash pid=4325 uid=581 src=37.73.111.175 args=wztc7kopnxnwtv13kr7nqht5qfod2r lv6w-02g8j2f36wny
  - Log entry 41986: process perl pid=23772 uid=552 src=80.94.36.218 args=k9sz2h8f2f2olbmjm-f0gia03ak5p2cttr2bjldniamauq/p
  - Log entry 10369: process wget pid=5077 uid=433 src=119.100.127.5 args=3xlle e0spx4u03uw wq -cv121w4vpp4v3t-jrv27libxg-
  - Log entry 92633: process sshd pid=6793 uid=521 src=152.118.184.26 args=cg8jqup-vggf8/g2pswci17k-d6eq2u3uty 4b9mjezn4swu
  - Log entry 11317: process bash pid=8313 uid=882 src=125.205.76.25 args=s/ealla15cwo2vxhjc6i2j8m446e6wcb7hrswk8tyg-1ezt/
  - Log entry 75814: process perl pid=21838 uid=961 src=112.236.4.116 args=oh4da8r/8c1bxu-thnd6i17mfq6vyoxca35/trat4p1uc0zu
  - Log entry 89853: process nc pid=18885 uid=698 src=218.170.209.20 args=3dm qu7jrv6namg2xytn3yb9uw0qr8b0pfxh8i-f6glrvij/
  - Log entry 47187: process perl pid=10747 uid=442 src=221.165.197.68 args=mtqe0i7-c322-ev6krlvotwthvotlcofq 9 4xo8bnt3uznu
  - Log entry 44866: process python3 pid=22946 uid=22 src=146.29.87.50 args=5t-webikwpyms28j4i5u-biq3a5kca12o4/qq1rpa57i /qj
  - Log entry 59664: process bash pid=5431 uid=868 src=77.239.56.227 args=pue4bj1jjuzlbhxqrsz15ump6p6rjnty 23a12g8tw2tf6v 
  - Log entry 93848: process curl pid=22850 uid=561 src=203.193.108.179 args=t1e 9lgxbxs5ogdhk-ly-ve-mo8svwxxkvwhuq61okf7nxz5
  - Log entry 19736: process ruby pid=26291 uid=13 src=21.169.104.91 args=7ydp r698kn80ojqx5rwaehk0pwktq9nn5cnkym10wvz-h/e
  - Log entry 16633: process curl pid=10850 uid=271 src=44.152.235.41 args=w91qpzmad4rikj1ba2x3z9aqkxgd55nt6mnm2xv8a25zcjsz
  - Log entry 57945: process sshd pid=9993 uid=835 src=134.26.10.189 args=elf3xm0vvqb0qmi6/dgqwbo3b4b1vgh7igk8fs9up8ofnktx
  - Log entry 22348: process python3 pid=12023 uid=519 src=139.52.191.93 args=2kmyarwmk9bbc4h4sff/p2vcbaxix2v-a/kmp qmnx4h5u1z
  - Log entry 91414: process sshd pid=24799 uid=888 src=45.61.72.40 args=0lh54qaffiyukxaawd zg-1bpynwkr-txbk1my/2vd9kfvma
  - Log entry 73458: process python3 pid=31342 uid=956 src=63.177.69.214 args=lfrx0j6f7eoe54adlsy51tiol7ekec8cycsq1-0xd-kc0q1t
  - Log entry 64672: process python3 pid=3703 uid=657 src=3.122.208.197 args=vcyhk9jduimrix0qnthe-qe-c6b49gjj/c2imw8b7h8antmm
  - Log entry 94075: process ruby pid=6789 uid=384 src=173.233.199.24 args=kc8q8okght2scea3a7rudqcy4ecar-lootcbyben2a15lual
  - Log entry 38548: process curl pid=22565 uid=312 src=165.227.81.154 args=76sv-lrat3hoy09ub/tfgy/a45wa6wcbjypxutf-j-gwxak-
  - Log entry 47780: process sshd pid=31465 uid=183 src=124.56.12.76 args=jba7wq45bd82z7x8phdf2ljlu4f awxwv1kb6177qtb34x2p
  - Log entry 54873: process wget pid=29195 uid=328 src=218.251.175.102 args= am4/vzz68owbfp4x379f6/1ba46e7l 7/miiiib60 pqkqr
  - Log entry 91871: process nc pid=29534 uid=481 src=42.247.205.124 args=vs r/erwr2kwvhe3w7kvzih-f6c w1cowfpyi3-w4dipb7f 
  - Log entry 25620: process bash pid=13158 uid=536 src=119.254.146.102 args=iorrl2raymhfie2hf6c9 7j7je924fq3isf4zs2r8up d65p
  - Log entry 88181: process sshd pid=31121 uid=971 src=222.4.124.220 args=j9ijzey5st5/m6oy9fepj2ql41mq12flphvnvm-b3df8bal/
  - Log entry 29147: process curl pid=8346 uid=178 src=167.206.250.154 args=7n ktp42ptgyubzoj4rbt8brr9zty0vm0zm5s7ep8efrf5/w
  - Log entry 12471: process curl pid=1222 uid=821 src=75.200.226.128 args=se931c6- jse2ir-cwnqt6osu2 nh845b5hy5lbajwm5 2s3
  - Log entry 79672: process bash pid=27925 uid=320 src=33.59.123.88 args=25cwwwpfv66iv o/zi41k7qb21000esuzk9k2m 3erd87k v
  - Log entry 41127: process python3 pid=13252 uid=533 src=157.70.210.153 args=kkkx44pgsmfx8avwx1xy8 uv6owxe6ts0q 5vycimbp-s4 a
  - Log entry 23925: process ruby pid=27594 uid=819 src=115.169.197.79 args=3fn aykw cf25m/sgzd/ekozktga vfnbpdzc68h-sd2vko3
  - Log entry 60840: process sshd pid=5136 uid=6 src=97.42.241.1 args=6q/ram6 ottnkuk43cticbopo26va4hq4omlp8xein1showz
  - Log entry 94474: process nc pid=21630 uid=174 src=179.180.151.234 args=oi1z94hagu9jf cf1n47a s2lubaoq32fv66vdmlhh 9t5bx
  - Log entry 45577: process ruby pid=12861 uid=732 src=146.132.37.80 args=-l9ub74kk6kewyh ybwo46mab2wy5pt/2sbcr-qqfgpcmpq9
  - Log entry 23673: process socat pid=11318 uid=632 src=106.133.159.178 args=1sbgme-5uhz43mm199kqo0zzek46qaskxlkztg3pqx-rml3l
  - Log entry 35944: process perl pid=18902 uid=448 src=204.182.166.112 args=bic9o36yrttb8g3-wx-cxc8-0wnjn h2pkf7l/2 /mm7uu4l
  - Log entry 68458: process wget pid=10256 uid=805 src=121.192.245.54 args=l66yl/48m902-3a5ccbx bc5hnxdxbvvl4s0a9tf5ruhh4od
  - Log entry 19266: process bash pid=5102 uid=647 src=212.250.207.175 args=yf5/lhvon1lp q7vf6zp wmmj1ekkkdyafdq1x13meiqtvhq
  - Log entry 97797: process nc pid=11903 uid=708 src=12.0.141.9 args=5er7j30-0xnlvf4-mpoox9j/83nfqcc 80en9cel9ttt127l
  - Log entry 83521: process wget pid=9078 uid=552 src=178.253.54.57 args=yy9uka1q5z5h8 w-ja yl /7v fsh4bc1hhv0qp4tb31hhn/

## Supplementary Technical Detail — Section 9

Automated correlation engine identified 21 related events in the 6-hour window.
Baseline traffic on port 41810: 3 connections per hour.
Observed traffic on port 4444: 68 connections during the incident window.
Statistical anomaly score: 0.936 (threshold 0.750).
Related CVE: CVE-2026-26515 — not yet patched on 3 internal hosts.
Affected subnet: 10.7.3.0/24 — 8 hosts in scope.
EDR telemetry: 3 alerts suppressed; 3 false positives removed.
  - Log entry 55118: process socat pid=12112 uid=512 src=123.52.23.67 args=z2y5tv-88y37g31nc6d5/y/6l4wgyjyxokda-thwd0wtc/ h
  - Log entry 86402: process python3 pid=23254 uid=553 src=26.186.46.191 args=mulqktgo7 whmw3h0xviu-kzsx6vmz y0dtbgult7-s63woz
  - Log entry 71540: process python3 pid=12084 uid=36 src=172.137.126.128 args=13i3p6g84ih0o0gzdsk-cm0pcvnyxj2m2s3fpbbhxn39q7ss
  - Log entry 46520: process perl pid=11152 uid=271 src=183.58.85.230 args=eyq0zyhqehcv7vbaisf6gs/0jn6gsif6uk4p0hz1831rfzpp
  - Log entry 35087: process ruby pid=4820 uid=15 src=132.178.218.180 args=d545w099wfsa467/xz63f3ljevrpet8d-7gayyxe63nts 3c
  - Log entry 91253: process bash pid=2470 uid=686 src=27.9.102.84 args=q7twz-4fvuah b4abtcfwcaagobpopco8sdwhsrgp-elrama
  - Log entry 19990: process bash pid=28539 uid=449 src=165.190.0.115 args=f- lu3o0ybkwwoashf8k83m9fyn0xagokpr/-ftpem99zwr2
  - Log entry 52291: process perl pid=20062 uid=37 src=148.247.6.186 args=45fy7 crsmzxcyybkew17-4se/bph0b e0q/r2le8ptugsua
  - Log entry 19962: process bash pid=20030 uid=141 src=56.16.207.100 args=o/d0otw6f9ooc08c--9x iq4ourl917k24/udhcc-8v8n2- 
  - Log entry 88811: process python3 pid=11537 uid=778 src=113.230.120.122 args=q40z x2sgqy3jb-rvy1/pv6db rf42pcwzg5 4kkepp5w2br
  - Log entry 81598: process wget pid=30487 uid=206 src=134.163.136.9 args=ynv9oqkg-4aks72jw0q0dbv8c1il40uvlxyzxzi3-dkmf8m1
  - Log entry 86389: process sshd pid=13054 uid=84 src=126.139.249.4 args=us21qhgme1/wbwi adc/t0v jm2oq977fmtch7eeq8t7 ekp
  - Log entry 85725: process socat pid=7241 uid=236 src=163.93.82.56 args=w5x/7j2/8ocgipj9zq8n7o0lk-lz/rs knh6qua36ntn0gzf
  - Log entry 92912: process python3 pid=13867 uid=27 src=29.104.167.210 args=idvzbh9m0w/0j82xsbgiep9/ r68tufqa0oitlumfxtuu 0f
  - Log entry 51431: process perl pid=6262 uid=31 src=196.112.142.234 args=3u1tywsx342qrec-c7cn3zkgxidqa59o3xuhx-jb 20euj0j
  - Log entry 92177: process curl pid=26546 uid=602 src=167.81.54.45 args=ldwcd1yo j9f59ozzj169-3 5gmfydx 1gzd4wc09e 4tjfe
  - Log entry 88761: process perl pid=20789 uid=313 src=131.118.59.101 args=vhacy4kwb--w9jljiec-tp7p5ctbrur7aiwbc ov5dukkwe1
  - Log entry 89075: process ruby pid=4766 uid=859 src=11.88.202.148 args=/5hk/7l/rd6xwf644ybi/mv0q44y4nxlk0i-4w9r/3gcm/5f
  - Log entry 52464: process sshd pid=30657 uid=158 src=59.135.205.165 args=pbcwva3eua7-o7ye88hs6sy1zj/nwwltfkk/ki3j1e/2mqvb
  - Log entry 48376: process wget pid=11653 uid=739 src=169.80.42.98 args=f1n57hl04tfx6f6jpwwe018q79434s9o0x2xq0htg695qsq 
  - Log entry 26955: process python3 pid=15338 uid=445 src=145.77.219.123 args=jbfhfl4-v -nblfnokevqzhzj808w6xroptvgjw3mhg00a0s
  - Log entry 54947: process perl pid=27083 uid=683 src=108.102.253.214 args=vcvrdopj8agn8x61ah uz7t06-01u/al/roeknuebl okxtm
  - Log entry 78781: process nc pid=27708 uid=76 src=179.57.134.222 args=m07kb-i7he4bb88m4m6jdahlz6wsncc9q5jyo9t7sny0xas8
  - Log entry 63095: process curl pid=9359 uid=191 src=136.85.145.175 args=efs53my3-7jcuphnxb 3ohcuahxyy8byjck 8adtjncj3g-c
  - Log entry 39780: process nc pid=17801 uid=689 src=10.111.171.200 args=2a4ogx6l7tguuy0q8haby4tnp7h2j58cceqmpf1ghf21/1 q
  - Log entry 74147: process bash pid=17747 uid=976 src=157.18.107.236 args=i/1el-b5o5-ir9eahi42b-9 astj1juo89yd/v4nr/6pf4tm
  - Log entry 50638: process ruby pid=12591 uid=476 src=124.9.163.96 args=wgw5c0x2zj0n4-wz0a78qzvm7escl5a7/igr80rzq9cqeb-v
  - Log entry 90158: process sshd pid=18852 uid=216 src=190.51.141.165 args=h6qc3q1nrg18o ms muj3eng7r8j57-4fk41-vp 977lx263
  - Log entry 26124: process wget pid=22876 uid=997 src=140.157.184.110 args=2iiokrmobf5qlw9u26lwf6ryxcy01dx9j//e4blf42ucksg0
  - Log entry 98825: process perl pid=2480 uid=829 src=202.21.175.30 args=vij-p1gwiz2 vjkp8m-s86hbo6 e03grcpp71mvdxs fbb6k
  - Log entry 52165: process python3 pid=31351 uid=887 src=31.91.67.73 args=8i3n360uvj2266ssdl8gtkdxfl/bupjn 79zm5aywyo4j0y5
  - Log entry 88771: process python3 pid=25038 uid=141 src=48.204.172.226 args=tn179i0qsros -y-8lprgaff6z73yr9u78daa7uxkcl5ma l
  - Log entry 90037: process sshd pid=29278 uid=827 src=77.89.183.207 args=c9f7pccpd bdib5na6f3iyljwswdxnzhx4uf9hbnrakv7jf8
  - Log entry 47618: process wget pid=26834 uid=960 src=162.38.104.16 args=9f8t03w1r3c5qq9e2to7-r8hht49cb6/ujwrzg mxmqj94f-
  - Log entry 94784: process nc pid=15843 uid=510 src=151.155.193.78 args=cn7d9tdabj6wr3p2ulb/t/nfgw9fsojbglvdjutqd9q22oyu
  - Log entry 38728: process socat pid=16544 uid=200 src=194.222.72.1 args=e7jod fn4iqx--130e/5az4qzvwz9pe05phkt2as8m4ydqns
  - Log entry 96944: process ruby pid=18297 uid=404 src=95.22.128.61 args=51urcqv/q5 ayimag6jg6v91bq5awvevextlsceqzjem3yd3
  - Log entry 18738: process ruby pid=22755 uid=904 src=114.103.130.191 args=8sylkk9rg/5-pccyw861s8 xpg14dppjcx70np33g2ilj- 6
  - Log entry 11612: process curl pid=9269 uid=503 src=91.110.192.254 args=k5j34ac8bpmf8lilvg8-admzhzal6lcqndel2dhiotz9zw-t
  - Log entry 73905: process wget pid=26137 uid=417 src=36.222.86.102 args=xfaji8uumu2fycfjuc9ryb3wkzqif-8d4dhwcygsn4j4kin4
  - Log entry 41020: process python3 pid=16758 uid=348 src=52.165.58.133 args=tzh5u0trsefp9unruwcou4estytmi5m7cxroeq3kq9oj9axr
  - Log entry 37059: process bash pid=30889 uid=107 src=168.79.34.60 args=e3ww6x70z3/s4 0qt375sur yjvsf24v14wzgboy1d38ux2z
  - Log entry 81650: process python3 pid=3987 uid=390 src=208.155.238.246 args=k1b0c8c0h74xts/fttx0th-0lkq8tr11ww49rf74-5dc3nad
  - Log entry 63436: process curl pid=11621 uid=925 src=145.157.154.48 args=/8bzlpp8s8d92qxr-f6-9q9kd1j7fw  5ogeujjjbjda7bs/
  - Log entry 35983: process python3 pid=20452 uid=9 src=144.233.254.109 args=avzxerw-5d784fe2uzgeo11o37o6d2mczng72xv5b6c0nb/n
  - Log entry 51829: process curl pid=21480 uid=395 src=133.19.79.143 args=0rlhinuhsdu009f 0zu4h481m7/k82s67jn3d7jzpbl3obtn
  - Log entry 83159: process wget pid=15954 uid=731 src=71.42.100.249 args=38urn hbutbx56b--1w127-k/ w2cw0w8ple/39ragtc99t5
  - Log entry 37705: process curl pid=28653 uid=836 src=152.95.177.36 args=3t/mvgebdfi8ui hlul-l8paj/fevfmxtdq4l3sbmusucudi
  - Log entry 21069: process perl pid=25877 uid=537 src=144.118.18.105 args=2ip2641xj qswusau3bs59aboe8av4g k6 /z-y-oinjzsmx
  - Log entry 79189: process sshd pid=7179 uid=854 src=107.237.11.104 args=a85a96pm6v9-3bpby/nbap0r7plradex25ta-rk3gvt2-l0b
  - Log entry 16064: process python3 pid=20673 uid=828 src=139.247.123.14 args=7n3y2g74bt31sl54zx9yihy8kwux9t5dv-tu7px/k7qqmpa0
  - Log entry 96104: process ruby pid=20552 uid=512 src=42.33.139.126 args=8a5lwc1/wzk0bi1yxg2zzqu/kn4iruo60m fbzasuyx0h644
  - Log entry 20662: process perl pid=19233 uid=812 src=148.194.102.223 args=14ekryj9krr5ybdx06jtubsbuqxfs/0gecij/ 8oij8hnyy9
  - Log entry 59893: process nc pid=23720 uid=171 src=25.217.245.102 args=th3saguar30w/9vhtp33by2tipb4kt02cz1mq2-bnj0nz8hy
  - Log entry 82369: process bash pid=26924 uid=157 src=60.229.4.19 args=a-ry- cyl85gyy-vnu22es5 jc6pv v1ct4/n7dmg4bn56q2
  - Log entry 66638: process nc pid=19156 uid=843 src=200.242.242.253 args=1cirar0w2ykvcbccj4ygd77mbm/ppqhe0m9e5dy/0wek6z5h
  - Log entry 61805: process nc pid=29411 uid=174 src=195.171.130.64 args=g fjpg5k1kmc/gezgb4xuq4mqvbcqu av8djqcptsa/4ag h
  - Log entry 11494: process ruby pid=27960 uid=180 src=48.119.92.71 args=ytakk4vf0q8 sssdu28o-awu7l8mthup2zcvgayfi oxf9/5
  - Log entry 60150: process nc pid=29741 uid=848 src=188.37.84.253 args=a9vdp81ukenxzgssi-qsr/jfri39li7j 44iw1fial y29iv
  - Log entry 10292: process wget pid=3496 uid=599 src=18.165.103.20 args=e0hj0jj35w0m38mf08j/pcq9i/g/38sjbxili6y71ojyqdpo

## Supplementary Technical Detail — Section 10

Automated correlation engine identified 11 related events in the 6-hour window.
Baseline traffic on port 2509: 1 connections per hour.
Observed traffic on port 4444: 186 connections during the incident window.
Statistical anomaly score: 0.832 (threshold 0.750).
Related CVE: CVE-2026-10138 — not yet patched on 20 internal hosts.
Affected subnet: 10.9.4.0/24 — 10 hosts in scope.
EDR telemetry: 2 alerts suppressed; 2 false positives removed.
  - Log entry 57434: process ruby pid=15871 uid=38 src=60.38.144.211 args=n wsddv mts/1o hxd-ppj8rzuuy9b64/37l7evw1kmb /66
  - Log entry 87390: process wget pid=12167 uid=293 src=95.56.152.216 args=2o0vbmbmt6id4/dfyll2gct -57-d6ww/nct68e26qib7a4h
  - Log entry 64547: process wget pid=19989 uid=207 src=51.100.23.249 args=5sxnhcv15npuxiiwzfjphp3prz9ug84hy1wbdh/zanz4sk8a
  - Log entry 25436: process nc pid=10168 uid=643 src=77.176.14.108 args=oyc//o3vgs7-mqiiddiojw/ls/58eicdlibzfu78p/df3hbu
  - Log entry 67926: process curl pid=21260 uid=568 src=21.85.149.117 args=26saqkswjcr6j70i2vzwb/qtzfy nf8 es5kmrnckq1-hovj
  - Log entry 46325: process curl pid=10970 uid=10 src=31.231.106.87 args=fd75bfs604yz7gxb2zrsoxa0ktq/48x4ud7x6icc4eudm r-
  - Log entry 26319: process bash pid=16323 uid=37 src=104.66.163.229 args=n-0loqzxe6qahdtrd5j-s7prewj/tlkn4fck4mr0l1ywkyv-
  - Log entry 64840: process python3 pid=3378 uid=297 src=192.78.183.164 args=wd-efv-kfcf s6xeqq5egi8odkq4ss67nx17kdyvh74ecpq2
  - Log entry 72111: process python3 pid=15050 uid=749 src=152.214.79.41 args=kcn2wt3fq7zs2k9qzuapeibiy-52o4567n1b70/7d5j rk29
  - Log entry 71045: process socat pid=30395 uid=237 src=78.53.13.213 args=nevsp5dyrqv3llro-h75y2fyy-3tyz9lvbf30/wc5mtynd75
  - Log entry 72789: process python3 pid=30892 uid=177 src=209.117.33.133 args=rreubvuum3o2jfdk9v01y4iapmnsqco7x1cd64zb9eua2x93
  - Log entry 54726: process socat pid=2918 uid=277 src=137.28.214.141 args=4n5xd6qtj1n1ynbuks58n4hnl1/6k160riz07oe39mynqr9g
  - Log entry 31943: process wget pid=26896 uid=95 src=112.214.20.90 args=3 nv8w79316a0at/g8goc7g/5ztag7jegpon0za9oz365psl
  - Log entry 90011: process perl pid=9288 uid=425 src=77.241.216.101 args=iw/4t54v4kitmiw7gfg-69suzoj22rxvpyycfkqug1tydc-q
  - Log entry 77673: process sshd pid=24927 uid=840 src=54.101.51.223 args=0tk 20507v6onz7znxhseo/yq /-xys6k99hxnylln578q9m
  - Log entry 36253: process wget pid=9619 uid=167 src=201.208.242.133 args=bsurdj6vj/8x3air340a/i118rt2sh8-uz9xiukd8alxairn
  - Log entry 56587: process nc pid=6711 uid=7 src=128.86.235.241 args=3xb3gc3t95ibhhecr/c/qhj-q1ectkhqcyr irb64o5rb 51
  - Log entry 65307: process perl pid=27166 uid=34 src=124.215.159.51 args=19yevmp6z135zlusb-br/vfl2s194j-byj2hguotq9-eu267
  - Log entry 40009: process sshd pid=22344 uid=327 src=61.73.174.134 args=1hwfokk7zwp0xcha9lxxy0d9mcm0u4ia9s42re9sceni4-h2
  - Log entry 72409: process sshd pid=15683 uid=288 src=36.161.237.220 args=-f2f44ff3zbxuo baz1baxspt3/u6huy/2aa0nd7i-xohn3a
  - Log entry 26066: process sshd pid=23229 uid=988 src=131.196.51.82 args=ua2oc0bkj9fofz2raxb5coqa8ak 45-h uw-4banoqoh42s5
  - Log entry 75608: process bash pid=26771 uid=157 src=20.101.164.151 args=m 2aycl2t12walf8e/bif6cx7ko/l ygaan/0sj0ss0zsp51
  - Log entry 78747: process bash pid=21171 uid=153 src=125.188.236.232 args=3dks ves5t54trj8gejgx 5mqn7rqrvcappztvcb2mxycdar
  - Log entry 74315: process python3 pid=28605 uid=780 src=84.58.3.239 args=gwnk4odcq4nhkzt42u54d20yqj1/jg jxt/05w3j6mxdvnii
  - Log entry 54277: process wget pid=11700 uid=441 src=129.4.57.69 args=3kp/5r4uqystysp2077m7k9eakyp2zmhvxq4o0h4r-2cumr2
  - Log entry 59222: process perl pid=16442 uid=561 src=46.57.198.110 args=z9gy2dzbp7zhwkq-r6d8 tow/by4eisi /88z4b/1u/3ovs8
  - Log entry 80856: process wget pid=18722 uid=945 src=88.122.108.114 args=rs0fqa-nq1-soyoqnll01yc65t8i0p/ly18kllgl15ha4a k
  - Log entry 54703: process nc pid=26656 uid=152 src=205.53.193.247 args=4h0x6w58ne72qsqjs921f5kqxesh2juum lzylg74f4hfndc
  - Log entry 70877: process python3 pid=4831 uid=323 src=68.177.209.104 args=h3chgrz8/zb6tdceq5gb1m8wyqun wkzrfkwo1lj4iwkuorb
  - Log entry 64631: process socat pid=15790 uid=470 src=107.106.2.157 args=woqufc6dtn8 5a8/hardz4os wt4l-omv/-s82ma7rn-1bew
  - Log entry 47063: process bash pid=14946 uid=856 src=157.207.200.34 args=nsom6a6n3n362y2wmcjx0-rf0sqw5x6ok ue-gklx2wjgci 
  - Log entry 12742: process python3 pid=27404 uid=594 src=1.230.227.173 args=tibd1z hj839c5qa1h19xdukk1x2i3flz jcba20adzw8-9j
  - Log entry 35529: process sshd pid=13420 uid=34 src=53.133.89.205 args=55c-kiuqdpm5h3kx4s -nrh98p6gvy1nc38g4atma4u4k5w3
  - Log entry 18100: process socat pid=21556 uid=108 src=156.201.48.33 args=k2ax9tuczlikemrra0vqea124f81bbae1 v0a5c z7q1c7vq
  - Log entry 17407: process nc pid=23329 uid=957 src=63.117.157.180 args=7 rcpitjpowj83/ra4jzobwd8dr8pcu7l4jhvnvkgaqx92qy
  - Log entry 13490: process perl pid=31808 uid=709 src=151.23.254.42 args=465y8pc52 f5p76c8we8h7qvj71s6d11dclxdw fqws/zxo8
  - Log entry 78319: process socat pid=4365 uid=176 src=133.166.102.225 args=f0l9 0v5j j6u0k64xhost 7lk0snwvq2pk3-x7pcrh9krlh
  - Log entry 45037: process perl pid=31338 uid=475 src=177.234.47.192 args=rk9ak9/nka qsk/9j8ylym-vmg3c5simcch8frkb/xt7 h34
  - Log entry 95644: process curl pid=23745 uid=310 src=37.28.35.178 args=j4hadv0unhi/i8v/xx9q/6w10i4r-szetddwgyy1xbxk1qxv
  - Log entry 34396: process python3 pid=24542 uid=73 src=187.11.46.81 args=2c5tart8cr4tvgseqtcadr-2l0/ky7xefxbx8 -cz2bzwari
  - Log entry 55430: process perl pid=29459 uid=275 src=110.151.7.134 args=pqb f fvn9iqn37hxini3yht-cw9ylulkarweffec7d8jhbe
  - Log entry 32563: process ruby pid=22966 uid=340 src=199.228.185.239 args=-05xj1zkiemfc1017fv69y/bbgz4na7n0nro/xit3q64c420
  - Log entry 89861: process sshd pid=1363 uid=180 src=166.41.221.136 args=rcl94ukqq7fk50bxyvjl9h2p74i5/7h4zslc4dnfghyoqw1d
  - Log entry 89323: process python3 pid=21582 uid=981 src=120.61.224.180 args=l1jkozdg189xnoul3shf7ljyth 6nrm8-/eo cz1jwc9ud9n
  - Log entry 73153: process python3 pid=1985 uid=300 src=73.48.147.166 args=8s67gqqsh2lt092jaqhi1utqaoup802mpni 7maw5nr444a6
  - Log entry 57294: process perl pid=1865 uid=143 src=204.74.102.34 args=0c3dowkoaliaiuy/nsk/-mjhcs3pclm0a6vju-1azo9pga f
  - Log entry 34195: process wget pid=20752 uid=862 src=174.191.118.234 args=w-asx6ldlay c767a55tece tke7vdwhmgzgq/1eem0r7 1k
  - Log entry 53420: process socat pid=11632 uid=112 src=5.23.246.185 args=sftx 9ccx8hx5rycbvctjsr223negj tr/bj0/jkro2bt-yj
  - Log entry 43185: process perl pid=19772 uid=133 src=136.28.240.200 args=id8jq20dp0w1ajd46r4m6he6i2or5nhmk49rdqym1icy6wwh
  - Log entry 31623: process sshd pid=29225 uid=527 src=213.142.173.201 args=cw-4ch dlzixflaclhfk0p6vqzzhpy7q2phaqbyioqxji8yr
  - Log entry 84284: process ruby pid=22674 uid=41 src=91.12.243.17 args=uus3dgl-86x0jm0r-tfmjcnwp5y -q-3mpgmxi54gnx/njmg
  - Log entry 39116: process sshd pid=4369 uid=78 src=117.27.41.50 args=5l mxat s3myd8qdin092b9drycqtm37wz-o21s-7mu ta2y
  - Log entry 98636: process bash pid=14607 uid=657 src=101.13.208.158 args=th774-q92ssj/vcg9tseesos1jo65trh6jlhoazn36u/ytnl
  - Log entry 17140: process perl pid=8073 uid=819 src=193.109.28.22 args=jq90rf8wt6i0bnx2yd1spzzb5i70v1w-01m2rg148j2rovp5
  - Log entry 35349: process perl pid=24128 uid=615 src=2.241.91.183 args=-un68y6n5gnw01fv95j09-w03ow-moys7a-4vfs57pzs93zf
  - Log entry 32346: process bash pid=1814 uid=909 src=48.251.48.123 args=po0al95u-/o gk4t65/vrve5y txnh2h9/t2gqpmfhaqkq30
  - Log entry 71953: process perl pid=10647 uid=957 src=139.243.169.65 args=h1 5ailxes28t5iehpv/sbbgma 6y-mjflgl/d n2jl56p9w
  - Log entry 82306: process perl pid=8205 uid=737 src=178.79.126.25 args=r/js56xgw7owvcwkyjkrqjgs6b06iglbtdqyuaohc638whic
  - Log entry 67410: process wget pid=5532 uid=375 src=90.118.86.156 args=g73ilszo5gkre9i5ds mk2n8ff6aeyqk ilxk10gbml3y/wb
  - Log entry 72281: process python3 pid=13861 uid=381 src=193.94.153.78 args=/2ibmosniv89arrjkkb 1u9-fvhgq5w6w7tguy18e40cbze-

## Supplementary Technical Detail — Section 11

Automated correlation engine identified 37 related events in the 6-hour window.
Baseline traffic on port 55421: 3 connections per hour.
Observed traffic on port 4444: 189 connections during the incident window.
Statistical anomaly score: 0.890 (threshold 0.750).
Related CVE: CVE-2026-48346 — not yet patched on 5 internal hosts.
Affected subnet: 10.1.2.0/24 — 24 hosts in scope.
EDR telemetry: 0 alerts suppressed; 3 false positives removed.
  - Log entry 82399: process nc pid=3498 uid=483 src=183.99.203.150 args=yw/uxncbiv98oi  doknm1oegsuw7/9f17wvfwssuzfpb-e5
  - Log entry 75402: process nc pid=18643 uid=701 src=62.224.168.158 args=n5lcx6ilg8gi6d0fro1vgmarbt29s3 g36h whn63olh6npc
  - Log entry 40261: process perl pid=25447 uid=429 src=108.110.143.199 args=kvlhs0-/iadojpco0my6ygtazcy23vapvkx1rvqdhfgjitz8
  - Log entry 83514: process nc pid=17557 uid=877 src=161.160.154.181 args=l770hziuiho29bfvs47vs82dz7ela8-ytr-aarhcgx2blsb3
  - Log entry 13215: process socat pid=1917 uid=379 src=132.166.132.199 args=srgbs-qlft3bhm55677s0f o4/artcqnnsayjddb90a0/e2n
  - Log entry 86765: process sshd pid=27351 uid=587 src=106.30.4.135 args=f81dmn7hsg6cz6xfl/jwh05f1 fmz61-i4imqcenxs5  f76
  - Log entry 19846: process bash pid=10830 uid=31 src=133.207.229.10 args=b8ccqbjox de04do2opo 84//aj8fkwzozd-u/q2bwi3qats
  - Log entry 81530: process nc pid=1172 uid=461 src=175.207.88.27 args=ze3bdmz8f2lhk2g5geocz6a gyzuef2u0ex9/u5675b3ofml
  - Log entry 36219: process wget pid=17052 uid=431 src=203.66.108.226 args=ikvprrn7/ nuzc55tdpkwei912zf kpbin6ritrwm3-n6m69
  - Log entry 36808: process nc pid=30552 uid=235 src=165.112.28.159 args=72z6rci9d91iwhruq25n787swq3t9gmjy3okifspluu1d5zh
  - Log entry 72271: process sshd pid=21460 uid=752 src=115.142.31.39 args=mg6tcaw4k0q8s6k/lplb886ct3hp2wnatmdqtev2w577/b5m
  - Log entry 33061: process socat pid=31326 uid=847 src=128.237.41.50 args=5ies0b0jo0jlm7v 2l7h7u-sb8kq5y18kz8scm99yn8ic z9
  - Log entry 48770: process sshd pid=3044 uid=876 src=145.175.24.125 args=5i39itxd7- 0o/wuecz/- 2t/49d 2dboky1i3tmg-wk9hmv
  - Log entry 66624: process sshd pid=11055 uid=589 src=98.38.100.70 args=/l94wvy6edrtinqcrgi5hlpkwwtt9cfsf13quoqhezjlbyjk
  - Log entry 49195: process bash pid=20205 uid=528 src=151.230.145.207 args=m3-i0nfnzkkjvvhucl/ocfm116 wznluk76cnb2t/gc8k6g8
  - Log entry 70576: process curl pid=20490 uid=454 src=139.153.64.1 args=tb0ca455agwho67qk/8p4qqnv2abpw2gt/y7odtjx8er2tj2
  - Log entry 66173: process curl pid=28035 uid=535 src=25.95.7.150 args=an vjocjsgl-zr1tc-a6mfjc1vu6wolaql8gjkp58to/oryz
  - Log entry 67152: process sshd pid=15221 uid=876 src=57.189.94.225 args=g3/vw7076nv1yf65-hquka4rdez07r2qq2b6rm/cnv463bfg
  - Log entry 91454: process nc pid=26627 uid=747 src=165.72.242.247 args=pna/alcnq984s2o91atyqzj8iddmnpo1o-38j5rnsulg5rbe
  - Log entry 26232: process bash pid=19121 uid=318 src=210.66.193.48 args=jlk/qxs-fisstaom/in-4ewgxyco uq5exl09p5abql4 4m5
  - Log entry 52897: process socat pid=4877 uid=265 src=143.73.61.236 args=3vzyxddx4nhb036euj9-i/i0wq6azmz/ctk1toa lr s9zb1
  - Log entry 80392: process sshd pid=15746 uid=56 src=166.67.3.146 args= fxa0twf56a920i26zd0ke4b50wsnn1p/ 4qhdf3jwnqr-1z
  - Log entry 54280: process curl pid=18734 uid=197 src=83.41.68.60 args=o5z3 b3fqgds/91yr rx8we7eti6s9wxbwp11em8-6ih0hfm
  - Log entry 37813: process socat pid=28873 uid=850 src=137.223.49.163 args=ieg9wy5jb4 g 8 y/18 y4o6qsof2yxj342f x9lnp73-m8w
  - Log entry 84726: process wget pid=9031 uid=362 src=171.197.229.47 args=a49z0u-21 51xkre/c6 lnolh/r8isj4u00on0nientc0axi
  - Log entry 82303: process sshd pid=6487 uid=886 src=135.127.82.204 args=sqifhsm-1k-qup/wu6ol45rs//toorp/l08eywomq3w7l5ex
  - Log entry 73285: process perl pid=5918 uid=461 src=12.46.241.185 args=zp0ll-e2382yxgxru1x hr24aqigc87i88zfxfydhcfx4iaz
  - Log entry 36680: process sshd pid=31247 uid=749 src=164.148.40.4 args=7wmbw9b1io93l-ub7h- dufw0 m--mdlpsx/v3v8bhrkayto
  - Log entry 45461: process wget pid=25691 uid=41 src=92.106.37.222 args=z 5amhtsez5751s2k6v3zj1km tr5k/fpvva6ldi7/46459u
  - Log entry 64442: process ruby pid=4047 uid=628 src=61.178.187.235 args=li8uhwrs6wg31lrmusli2srqck3s689xw-z/pq-7ge/g78ao
  - Log entry 76856: process python3 pid=7544 uid=896 src=179.50.211.53 args=wvsfsp6x-7qkxv9s4375umc iqw9y 9hxr6g5h3tpr0e-a7y
  - Log entry 17865: process python3 pid=16730 uid=947 src=64.139.47.140 args= 7kk5v/ak 2bphiow7 r7rnean/qcw8-6ye zwj88-7-a1el
  - Log entry 96412: process curl pid=31074 uid=806 src=148.84.207.193 args=u96hm rpdnyaqp0 -1jaluf675iih3p/v6ombus6bhw0/cst
  - Log entry 12504: process perl pid=30804 uid=177 src=150.207.155.147 args=qthh2hzdrcoggdkn8ad-xz0/b8drqgys8bgxlnntaswx7-wh
  - Log entry 60572: process nc pid=1219 uid=330 src=192.249.154.164 args=4damc6s 0d4/60b/w6ga4a0gbo/h9f5c5x 60ysy/4a6s07d
  - Log entry 54411: process curl pid=30964 uid=533 src=160.108.23.103 args=d/tlyu4s5b5q4lbpbgyc7tyx8ug-ffoq/pz0pk80wyzaisrn
  - Log entry 45772: process nc pid=5890 uid=508 src=144.8.191.234 args=84udnm5 vfb71dkvo0p5uawj49seom-40xnk7-cmn13rwrfq
  - Log entry 67370: process wget pid=24073 uid=841 src=191.225.16.57 args=5nf3uglwyvzx4138kzub247-dpuavc1c7dxxrm1hvqhrhnnt
  - Log entry 40145: process sshd pid=15885 uid=999 src=29.172.189.15 args=u2gvea38wjgoe/ns5 a8g  w25ebuk89 541a9vakqllbev9
  - Log entry 60019: process bash pid=8333 uid=995 src=128.25.133.231 args=fauopqty-d65- ex3j1ut/82ultce1uvmr9dk-l8au8nd521
  - Log entry 25941: process curl pid=4675 uid=45 src=130.239.75.172 args=2ujeawl3t5q/gc ktk44fcn16bfhaj g9-wdr3dgff5uoe/l
  - Log entry 74255: process perl pid=26123 uid=829 src=106.172.25.47 args=irqy g5sghntpb0jrzin-14q6j9efrgd3gt32keqdcka5wuj
  - Log entry 79312: process curl pid=19292 uid=680 src=221.157.68.241 args= i/alwoomr4 xv4cbnf6/inxev0 u/ifc-0h3d-vgvof218s
  - Log entry 38528: process perl pid=3750 uid=180 src=4.167.186.50 args=yzg69umgyrqxr1pfwn4o/tcu0h370o-qhcuw0ipdkrj/5w/o
  - Log entry 82917: process socat pid=12535 uid=320 src=190.140.71.152 args=6nf-wy48wh2-1pxuxb856r7zj10zfy1qi538ifrjiq4jxxnm
  - Log entry 50105: process bash pid=14686 uid=336 src=115.172.189.104 args=xb6c6/cwiolsu97bmchoqbc465/9bi84cdxf-3275khjtg s
  - Log entry 60318: process bash pid=23188 uid=269 src=132.137.196.191 args=sj6iay5pn8p1r2rk9g0k9yw3rwx2g8kx-mky h/h48c8l/47
  - Log entry 69198: process nc pid=7642 uid=538 src=104.223.214.174 args=u-yro92n8n9/p07/ 8ujf66vfska9db3c5aszpc9trg7wi6/
  - Log entry 88017: process perl pid=16291 uid=687 src=77.83.178.48 args=gfoxno3-ka732974n4zqscmqqq2l733hl5q7 bx0lbunveay
  - Log entry 44887: process nc pid=15237 uid=10 src=167.230.20.18 args=iw/5go7wu1rdmktwt617v-67xfaa/dxn8lo3ypglqikwtydu
  - Log entry 96677: process nc pid=1333 uid=184 src=130.10.40.21 args=hj44ey8fmjaptn4xrn6xqjq9ddqsz4scuz3qg-1-8ll14l9 
  - Log entry 79910: process wget pid=16465 uid=382 src=160.55.83.221 args=20-e3zsqvd8v6xuhbhmt-6kiv33bz99jony1yqz0n/u1yjum
  - Log entry 89428: process bash pid=19448 uid=902 src=165.245.103.190 args=tj0/ws3qsopbo3g55zsu8q9h4x-ge8nmeewn38o6apqadupl
  - Log entry 70263: process ruby pid=19091 uid=498 src=126.132.67.164 args=ogg7rq627hcwe4knq6ioch3m/oya9suk 2hns2lt592qndax
  - Log entry 96932: process nc pid=4075 uid=485 src=82.71.63.13 args=3q56atfi4xa4iinlb2o-0f8n68yt9fgmd45 pqj sm19blyh
  - Log entry 67354: process python3 pid=13772 uid=291 src=199.120.204.138 args=ocud83yr-7y sgximt89izdynekh1zoik8d mb832hf6tfu-
  - Log entry 44258: process python3 pid=27048 uid=736 src=63.123.165.209 args=gzh2j70ozeumoyd e1t7rth-9vy22opak0p28hgt22sfvnc5
  - Log entry 17991: process socat pid=31532 uid=148 src=86.49.127.11 args=0j17uph2icwxowrmrm-6ffhjvh5oc4tt9u6oohb43pde6 1-
  - Log entry 11825: process perl pid=31817 uid=519 src=141.9.51.66 args=19s6-qp8dd2nion9u2mele56qw7 e1ez06hi8hidx5v7j 9i
  - Log entry 94707: process ruby pid=29762 uid=492 src=14.35.76.47 args=xg bebm/npf3ftksh3faolh89mvgdv3l-dvwdjnued5hl8sx

## Supplementary Technical Detail — Section 12

Automated correlation engine identified 9 related events in the 6-hour window.
Baseline traffic on port 23108: 5 connections per hour.
Observed traffic on port 4444: 154 connections during the incident window.
Statistical anomaly score: 0.810 (threshold 0.750).
Related CVE: CVE-2026-13560 — not yet patched on 1 internal hosts.
Affected subnet: 10.6.5.0/24 — 7 hosts in scope.
EDR telemetry: 4 alerts suppressed; 1 false positives removed.
  - Log entry 10011: process python3 pid=25553 uid=808 src=85.172.225.194 args=33oty-5datq0sgxenmq3bhvdegcjjojckzx-yq7arejspbs0
  - Log entry 47799: process python3 pid=21491 uid=249 src=136.206.54.234 args=dxm-x3s wap0pyc65l/8k7atuw5jn yq675q6cpbtoq55lj/
  - Log entry 15098: process python3 pid=28343 uid=492 src=191.84.236.78 args=3z54mrb71m2wqqvy4mhg0z8fhxj5d89ulvus5r7zlekpwz6g
  - Log entry 91888: process ruby pid=18762 uid=748 src=19.128.135.63 args=ffeoqve4bnub54ub/qj1mewilggszih7yq ytb4d-gm1hhdy
  - Log entry 33548: process nc pid=24190 uid=721 src=115.237.253.146 args=j-vkz0othxjqet5u657qq/g5-vgekefdcgrd8t8e6tjtfxbk
  - Log entry 49801: process perl pid=6600 uid=1000 src=98.232.28.113 args=o5nxa973phy1j/i2za 5-r1x5vffn1b/cndai1yb95ipdo34
  - Log entry 30588: process nc pid=3756 uid=494 src=206.46.123.129 args=x9hwdi/3n9oujw2xcx-iwmk1t m3d9684yyvt3k69z2/lu01
  - Log entry 48227: process sshd pid=25766 uid=995 src=14.30.247.87 args=h5xogxsbpy9d252nk/aar qczigcbct9z7rcl8s5 6od892y
  - Log entry 17392: process sshd pid=14780 uid=140 src=157.123.195.42 args=6f zc0ngqyqxrprocl/qs737fbeuz5sv00tswxevfa13vchf
  - Log entry 45029: process curl pid=5210 uid=321 src=68.84.212.153 args=z2spfgc8tzdqhy4 i/w 6orpidxjio-rwc5enk9a4miq2hhu
  - Log entry 95761: process curl pid=30147 uid=994 src=20.170.180.218 args=z6j/8d-bnen vpslrd4apfee3zljnaj58c7ju2ibckhg9lqq
  - Log entry 24405: process sshd pid=25173 uid=311 src=222.64.107.101 args=roy8/dfwq0y6x2znm5keq4jnqpol8i70l5yjwhgdt98xjytr
  - Log entry 58586: process nc pid=5440 uid=568 src=77.78.224.160 args=xcspsu7mkdxslscrlkvlxp 4rnjk/o4wdm6yssiqx4gozcfn
  - Log entry 84264: process python3 pid=1213 uid=16 src=74.245.28.88 args=am8crghm96/e3e2pgbjhiwjwqctq3pvyxeac1x/gkve gy-f
  - Log entry 43424: process ruby pid=19232 uid=513 src=110.41.91.185 args=2lis8yshmt4h/gtkez75kjytv2r3gsxqkrzlfgjvkami123q
  - Log entry 59689: process ruby pid=1170 uid=306 src=154.78.196.142 args=pykojehoiwl jdyrj8m2sk32vcqpk3lqg6yqgfvzghca6j32
  - Log entry 33388: process wget pid=12999 uid=925 src=163.248.27.16 args=323g4ltse5ur3yr9kf/3pnlh1tiawn0 j2/9qkr-7z2b55z9
  - Log entry 96513: process ruby pid=9228 uid=460 src=109.87.185.22 args=chykgslu0g4jb/wgye5i/edst6/4ybzqm81s20xnx0d3jqas
  - Log entry 30196: process wget pid=29461 uid=956 src=109.118.130.127 args=zvkmows-726zkjl-8wfhnx2anjdrx77bt2rny90ormq- ba-
  - Log entry 96971: process nc pid=31499 uid=752 src=199.4.129.225 args=/j208pvx1zzeirlilx-i3pc am5c-8e-yzdlor/f1 14l7hm
  - Log entry 50974: process bash pid=20540 uid=592 src=199.149.169.70 args=nknkepwq/0tm4mirw0e4h/dyczt6u3kjhxvq6vneg78vs0l-
  - Log entry 95551: process wget pid=7761 uid=309 src=65.157.202.224 args=x8mwlx7v4h kpu5rntkue/8p/oi44e0vkuw6iklznh084wos
  - Log entry 41137: process curl pid=10744 uid=718 src=9.160.170.87 args=/gc4gqy09635fskevahok4d 89nflilssrdzom1ig/ewk7p/
  - Log entry 78077: process ruby pid=10008 uid=338 src=162.62.89.157 args=n62g1pmah3f/-bkr-dldct377m3/o04m71zvdymfh5fqyvq1
  - Log entry 83636: process python3 pid=3053 uid=674 src=183.16.159.177 args=arhhvv3iunrac242r7o1/dn/k6hc6q7mvf6zxd8q4c4p42nc
  - Log entry 20828: process perl pid=5968 uid=482 src=71.62.0.98 args=jszl19jaf0jgpo/2pa 8jnk4yv2nr58wt0vb4on y9pittpe
  - Log entry 14430: process curl pid=14049 uid=917 src=149.103.175.181 args=6ee5wc9gcbmo0mt/8kym7nfmzolzlpoofslpnnutz62ca-ra
  - Log entry 69387: process perl pid=29580 uid=290 src=16.152.44.109 args=/z32i5h11mxgg8d973tz15ru7-quy4/r6oiskljf/aubxzig
  - Log entry 62395: process ruby pid=25458 uid=996 src=148.64.130.222 args=a0cd41q1e7b4/nq65zu7od1jedoteodboz56hc-3p tya6e6
  - Log entry 73131: process python3 pid=29845 uid=979 src=68.83.239.167 args=mjraij8lcw-sv5bajgcnmhw38o/gcnh9d50v/5y0b/q27tlm
  - Log entry 22707: process nc pid=7979 uid=932 src=167.120.134.209 args=n2e67nvoockoxhyc-wvt0m/x4g okht3/enqty3g7zcx23kx
  - Log entry 91809: process curl pid=1697 uid=704 src=39.11.74.145 args=ey kogx6131l-0qq6n0s5q21ld36pf53rmt1r32 3nzlpxi3
  - Log entry 43965: process socat pid=6384 uid=918 src=15.168.171.82 args=diy08ch9w1gjk/zg9j5drk5oh5y68c5nf6no4oo1ieatsg9 
  - Log entry 88422: process nc pid=12522 uid=638 src=104.23.6.187 args=j5g6yi4azqrz3i55wfwksd94z88xmq8e7z568mx3mf50qabr
  - Log entry 85057: process nc pid=18849 uid=668 src=43.247.253.233 args=6zl7186e95c159ua4t9y72tde7isnw/ nfti4vaamd2n8qo6
  - Log entry 18990: process bash pid=11610 uid=596 src=2.133.166.140 args=s3sh64rkv5cxm-xqulp6-jl55xhip47hrqaffr4 g07c13be
  - Log entry 42389: process bash pid=1737 uid=622 src=2.28.60.214 args=ol-xqkt9vgegyofl8b6bi0rddw4tc3 g5-s4hmc61zf750b4
  - Log entry 22355: process sshd pid=12582 uid=229 src=117.224.67.49 args=osu0/v-ko2gx4dwlf4xwwsrhmtomvo90xbfta8/tuzd j47r
  - Log entry 86127: process curl pid=23174 uid=189 src=177.17.84.52 args=n9z8-axyp/u/nn3cy9csd/mr1c985m6gnw/okj g0-y 9fwn
  - Log entry 38680: process bash pid=31464 uid=531 src=42.147.211.34 args=k-sae4t-9g5q1i0i 1ggswt7z6oqvdqstyrey5-da5 k-5l7
  - Log entry 90971: process curl pid=6538 uid=748 src=176.33.65.60 args=v6vudkxf4lrmoaoz86pb5yphvoqnrr4alvf9wswhz5h4jav5
  - Log entry 66678: process wget pid=13648 uid=900 src=188.86.89.159 args=cmmo464f2d3drf-/149y/hkb68/oqclb47jydwds3ruwle53
  - Log entry 94664: process wget pid=13041 uid=481 src=6.115.35.112 args=-38y5rjhjpwts6nq6krat8a63ef2901zmzob oopxk073q-p
  - Log entry 26931: process perl pid=4307 uid=173 src=94.120.89.153 args=wljqc7n6wm1lockh /9bo w2gitsaxxejbnuc9858ac1-97d
  - Log entry 85858: process curl pid=25876 uid=931 src=149.135.194.214 args=bnyd5-/29mww4jybm2 cs7updo8ejgbra-n9yd7x53y-coha
  - Log entry 22253: process curl pid=23900 uid=329 src=196.27.20.48 args=bdyja4/ueawl1bs 449pd3dl90ltl83iuc92goar5t21l4wd
  - Log entry 55267: process nc pid=31929 uid=663 src=217.56.62.189 args=noelanfjxbj1qr9fg996 wf/upziauvxw6uwh1sxysy8n4--
  - Log entry 47411: process perl pid=23790 uid=607 src=20.39.52.36 args=mm5xk4c7/vosqn8dq6hpbe-i  plgp k1-hzi/ob5ezp9vs5
  - Log entry 70605: process socat pid=10631 uid=943 src=223.39.137.122 args=ijd4o36rsk-zx3u43n4 1uf/oe2sietf-j2-pj1 eix8pab0
  - Log entry 95552: process perl pid=20440 uid=375 src=23.146.41.184 args=e12z-y0yl25869y6jx7r6odzn4d125uz8f-dh npxz0gi9uz
  - Log entry 41214: process python3 pid=25052 uid=686 src=107.254.225.138 args=ua4okij46tp-y e4mma0vm5l1ki-rg-av awl4s-rbelljlm
  - Log entry 47601: process nc pid=28394 uid=466 src=22.165.230.148 args= 3i23hlq51d3l95 fnae9//ggt675agfd-twjxj4rwsra3sj
  - Log entry 47862: process perl pid=4842 uid=589 src=210.63.48.209 args=-whrw9wagcihoova/tkv7w3gjy6cee24/fr813evs0r/8b4b
  - Log entry 75858: process python3 pid=4364 uid=88 src=90.242.91.230 args= ec3liaeuc43r2lg-j4p30/p3lr9pibyr3uf5h4qn/2-pkvw
  - Log entry 72321: process perl pid=25984 uid=646 src=56.49.130.69 args=77wi  rkod5xemko0pi13xi/m7uo8vbglovmwm1070kogn6j
  - Log entry 59917: process perl pid=26156 uid=483 src=193.61.52.45 args=xv7xk5amw08v0cciimlyz3 09i/znuf-5/16oihzvup0jeik
  - Log entry 92433: process curl pid=23545 uid=400 src=54.177.78.252 args=47/9zmzaxnti2xlw85jqxfv28 qgi5 n5110db-g9637dzbb
  - Log entry 55551: process socat pid=29200 uid=367 src=112.148.221.227 args=h /lxbh/r33tot9l5wn3xrvhd5kzrxqxl8qlwf5oqul0f/dv
  - Log entry 61791: process python3 pid=30184 uid=898 src=26.235.36.181 args=kilnxyq//mejnczt7aw0bp5xbn4yszgpary71hubx-lyh2zs
  - Log entry 99482: process wget pid=27798 uid=51 src=149.218.44.190 args=/i37 zhm  hmoun83zzi7tv/5bbpto4/sn9psmlvyv786ut 

## Supplementary Technical Detail — Section 13

Automated correlation engine identified 33 related events in the 6-hour window.
Baseline traffic on port 39377: 0 connections per hour.
Observed traffic on port 4444: 101 connections during the incident window.
Statistical anomaly score: 0.892 (threshold 0.750).
Related CVE: CVE-2026-14230 — not yet patched on 2 internal hosts.
Affected subnet: 10.9.2.0/24 — 20 hosts in scope.
EDR telemetry: 3 alerts suppressed; 0 false positives removed.
  - Log entry 37922: process bash pid=18666 uid=923 src=195.182.107.197 args=52iz19fmvr klw40-sncqvsuqd64lqjph/ zpmjyvfy0kbay
  - Log entry 57568: process ruby pid=16387 uid=873 src=61.16.241.229 args=f2on9wg4sy1ecfs9b/5q-ycwk2euosja0uu qg/1tsrkcn8-
  - Log entry 99608: process python3 pid=25750 uid=95 src=27.248.11.114 args=g 6apb8029dy7uxca8rd4fsha7 n4hjep-eyfb3tfxxn5g90
  - Log entry 35376: process nc pid=30791 uid=481 src=195.98.48.152 args=i3/5f438htbv/t5zs3inhc8ha3s7ry/h4cqtl4ck6z7 tu7a
  - Log entry 53561: process perl pid=4288 uid=477 src=91.219.85.244 args=ve9cyn263owt1ipl3jp69-p2e5hqdfs/chxw 93bvfo-j1f/
  - Log entry 60498: process socat pid=21286 uid=238 src=215.145.176.8 args= 4hwu228oxp73220ncw27f4b5heq-8o58e2r bdgk6x75vre
  - Log entry 38952: process bash pid=1767 uid=29 src=99.121.246.182 args=hwxffky56-296m16qaqz/a0z0h71z0pzhme-oirk4pw3zkoc
  - Log entry 70016: process socat pid=16891 uid=686 src=94.232.205.194 args=njld-fg6y9kswf5b6a72rym46i8xsky6snzkedvewpgx5jc/
  - Log entry 20871: process bash pid=19634 uid=113 src=89.10.169.107 args=q nq5eo8dgmbjoy7gemg4a4l5v4-/6b4w-dywi9hkuid/63-
  - Log entry 43131: process python3 pid=27085 uid=507 src=223.133.220.52 args=8d6552l pcwp9j/ lrxp4dym9-wypwq1y2ny dm/3blfxvol
  - Log entry 53385: process socat pid=20294 uid=465 src=13.207.217.13 args=t2khqczkxgsy-vr6f o9u4/6dz2wgt8/absb -69qmkatwno
  - Log entry 58884: process curl pid=11095 uid=711 src=169.13.74.12 args=1ntsk6z0wkea8xvvq85i3n4aj94zj6 c7 4cq0q3f43qwsa3
  - Log entry 32600: process bash pid=17472 uid=75 src=194.74.158.83 args=z dae0xucz75q/mik76-v1btctkl4/o4z 4o9fper sakowh
  - Log entry 69324: process ruby pid=19021 uid=268 src=180.115.123.113 args=x6wuzmu3f/cn5bi493n-z4l2wy/sc0 b2gi exti/iqbpu2m
  - Log entry 71078: process ruby pid=4120 uid=404 src=128.43.217.20 args=u7ga52gxb40mpafksxrw4a-52x69f-yc 5yw69-kq/b7xmia
  - Log entry 90871: process python3 pid=8863 uid=728 src=66.25.137.174 args=qq2eg05d4exftw2rvsu1hb/91crj8/p p5igcjp-lkwl5vgk
  - Log entry 20373: process nc pid=10257 uid=790 src=122.32.60.62 args=hzlbbg/1w-7c3z51u0oyz/tm-9khwe 7uu55j/z9qjpaz qd
  - Log entry 37610: process socat pid=12068 uid=649 src=11.218.53.213 args=kbs9tf20t1o0hpw6 8k/pl h-nv j-u/-yahj0nnntg7y7s9
  - Log entry 61776: process python3 pid=11619 uid=9 src=212.190.194.22 args=xp36yamuodmyq 1yhym4mzjjbcviv1--z5q-qy5uvvbn3agj
  - Log entry 38571: process wget pid=31187 uid=912 src=174.218.238.58 args=f3/p6xa987mvoz9bwwddkcwg/7k3ncu-965bsbxnxhkeprid
  - Log entry 72169: process ruby pid=22282 uid=860 src=187.224.159.96 args= 01a1gmx3w-c9v2cy57mxlm-c6qd8uy33jnxcz5mgq5kidry
  - Log entry 27252: process ruby pid=26971 uid=366 src=95.182.1.116 args=zj39ey8a1m-j8p/2hb55kj/z/f6dv8p-6lvhbxo2t9w3wynz
  - Log entry 49990: process nc pid=5368 uid=478 src=41.7.196.186 args=93zhpnd5 l06ii1aq8v4k1/vv6tzzscakm21241d4eer8ruu
  - Log entry 37647: process ruby pid=2743 uid=54 src=94.78.162.174 args=bac2rogj  /mc4x6wqyh9u9114i1dsug08cay5ywa5ipn1tw
  - Log entry 15447: process sshd pid=21536 uid=645 src=121.40.205.38 args=fe5rsdu8ub2fmo t4-nhj6xxyk6kujz5mvucjxsh 63o uao
  - Log entry 92901: process socat pid=21267 uid=554 src=109.7.115.161 args=s5zmki lhuyi3zz1smogx4/w i 274yetm8f5-kwf-8-ol/4
  - Log entry 61531: process socat pid=24574 uid=752 src=179.202.125.14 args=o3fahxyqy5ax4 rl9m85qy8t-z74cm9pik6tfbkim-4o36rd
  - Log entry 25818: process ruby pid=7399 uid=562 src=160.72.79.75 args=43h1xpg7y577j 7taclcvmw alaa6eg23672wfhcri17nu4-
  - Log entry 45472: process python3 pid=25156 uid=731 src=193.17.230.152 args=svf q05ozg7 yjc7wtmgazwy-rihox6rrqqlfppxzb48o/w6
  - Log entry 93711: process python3 pid=25695 uid=420 src=114.253.35.211 args=el2f55zn7o2t1r0es638tmh6hyoxffm r2ghdcm2v 649b8o
  - Log entry 52669: process bash pid=5124 uid=866 src=187.140.202.99 args=m1rvl4t8sc27jy7yiz9fnwp4v4-adf82ii953ws747/1fnp8
  - Log entry 93984: process ruby pid=25085 uid=662 src=142.81.160.34 args=thw459sq4zdcagmeyrn4ktkuemc1ktml3lk321-53b/if9pc
  - Log entry 43696: process python3 pid=10025 uid=655 src=192.43.32.180 args= 91ikgrgq-nltnf88x839afcp9ngo4qncfx92h3s1rfsgo-8
  - Log entry 35368: process perl pid=21716 uid=858 src=4.158.8.65 args=7-a1369gtnxycq0yv7bpcvxyea/qfy/wfy61p-h3l2xxsdp-
  - Log entry 11839: process socat pid=16899 uid=657 src=81.214.118.89 args=je78mfy5qk-ny3o372rl4eynakm1w3lwn0ymzndptq7jdsr/
  - Log entry 13019: process socat pid=27911 uid=806 src=162.215.225.73 args=cf450j0ey68evenvwagyl/k9t/5kylcpmbz4wmqbtafrm-d1
  - Log entry 46913: process curl pid=12396 uid=678 src=153.82.173.131 args=lgiqi5j33vsp7yya4jh8d18i7cs4s/cdkmhr46z-2cxdlru/
  - Log entry 18478: process bash pid=25141 uid=549 src=80.28.17.169 args=y8xh1kros1lu6jn7wnyn--d7fzkmz0adto/yyhhkdoc xu2y
  - Log entry 63647: process wget pid=9577 uid=83 src=169.29.189.132 args=lz2s9 5wduqsmvpdmo7mthua0mvfoo 7mc pscrfewlewtp7
  - Log entry 15490: process sshd pid=6225 uid=440 src=133.46.83.127 args=g  ckf94awt3w55y11tr-ziw6ygg2l8gim9nxhlw /0db/43
  - Log entry 89638: process python3 pid=7253 uid=471 src=158.120.122.208 args=75j29b j0a00/mm4ig5x1gr3sdvzmqll3nyntdb1 0pph1/g
  - Log entry 12331: process perl pid=7258 uid=241 src=51.202.216.141 args=ljx0 uvlcy0l4u-d-sxb5tivpye uhm-wlfnpssb6brm5zmw
  - Log entry 78815: process nc pid=5859 uid=788 src=44.62.112.71 args=4s36-py4o746-6xryohg-hun0la/09zi9nxo32il/s2qh8ab
  - Log entry 10731: process curl pid=31693 uid=599 src=99.108.13.123 args=wcgqvizjlbbl/d0kfl7vwk8108x/j2w3/ntl/1obmdu7l uv
  - Log entry 55444: process socat pid=21093 uid=281 src=124.196.207.58 args=0k0vvw7dlu0-ax gr3p3he430jljf22qg0icy1p86/4qdap4
  - Log entry 45118: process bash pid=12071 uid=640 src=76.106.63.108 args=2cmg0kswn ft g3e0ipyv dosm41k1pwpm8bmjy1348zalxq
  - Log entry 56793: process sshd pid=14475 uid=80 src=120.50.109.150 args=zfpt6g150lqi5jir45xlee5wq/zh4kbwqla0z0ya2luqh5iq
  - Log entry 95913: process ruby pid=27948 uid=514 src=81.39.146.81 args=gt2fj806lhwdxwcgnir7nju99t8l2cb0czjwab8l09lkcud6
  - Log entry 50152: process python3 pid=29575 uid=850 src=192.190.101.91 args=81xl13crj/okr5 fjw-b8dmwy4acx69edhl75il-ifputr7r
  - Log entry 34282: process wget pid=24694 uid=510 src=50.177.158.184 args=x56z31he6w0mllp 0snspobccc666dcj 7usts06mqk5 qf6
  - Log entry 91770: process wget pid=19506 uid=657 src=193.241.115.122 args=os6vajddl/qmlnoaot3jmj7gqdb6geyo5fky-ycrm 0u4x1r
  - Log entry 15470: process bash pid=22387 uid=382 src=219.137.206.22 args=144 81qpc48w0wx9 ehm68seti  ysvgomb0w58i-u-kqq1o
  - Log entry 66022: process ruby pid=5532 uid=87 src=161.162.39.9 args=ai9-3fa3a9jyj6ce xoj piu27cma/y7c9somxomhbie115i
  - Log entry 84185: process ruby pid=14751 uid=438 src=17.84.50.238 args=kv3uxoslrcp6i0r2812tu4gh4m4ly19pgek2w3hgavmzb-vp
  - Log entry 49381: process python3 pid=31228 uid=151 src=21.83.169.181 args=0 0 ildxk8712a70sgmbyk4odcqvisi7z ep1t21o98w8q5/
  - Log entry 77418: process ruby pid=19596 uid=377 src=207.179.93.78 args=b5np4maowmcpol2k180kgx6hw7qchmua50srpt5mbbv-5mea
  - Log entry 58002: process perl pid=25746 uid=28 src=115.59.183.219 args=3dhi780w0s6prr9jipr3xbbmiu7t016mg8bg8d3pb603qquh
  - Log entry 78470: process socat pid=20377 uid=906 src=64.49.139.104 args=46aypn126dm ulahx0jle/9va4ofrsnra6xb 6orolmi/1/z
  - Log entry 37928: process wget pid=13743 uid=571 src=81.125.241.2 args=u3wdoke27oy2p-h7xvjpkupvc6mtcuualbyqzmh-23hqh3g/
  - Log entry 13944: process curl pid=13949 uid=695 src=70.233.9.248 args=ss0y7ley08i zk-uqe3mw9e8k2182mp4lfbuww5h2g6ekdpq

## Supplementary Technical Detail — Section 14

Automated correlation engine identified 15 related events in the 6-hour window.
Baseline traffic on port 65258: 3 connections per hour.
Observed traffic on port 4444: 75 connections during the incident window.
Statistical anomaly score: 0.906 (threshold 0.750).
Related CVE: CVE-2026-21090 — not yet patched on 18 internal hosts.
Affected subnet: 10.10.4.0/24 — 28 hosts in scope.
EDR telemetry: 2 alerts suppressed; 0 false positives removed.
  - Log entry 84591: process python3 pid=28393 uid=769 src=70.220.232.191 args=0t9iv8n ymtgq2yh64ll/9lhszbl/t 50974wg3c30qn9oy1
  - Log entry 37205: process curl pid=25713 uid=448 src=63.37.205.113 args=79v-930qnhf-gqg-eero5gklshl6672wku-jcw-jzs0t79v 
  - Log entry 68600: process socat pid=2697 uid=486 src=82.142.49.190 args=uw8onolm534uh7-ta0ycg4bsytrle-nnh/ a3f1zpay8wlte
  - Log entry 51373: process bash pid=23948 uid=102 src=131.171.128.206 args=jdfqwg1vgr7ib9smbol7rbsab7nnf4z7wk1294ig5tgad8vx
  - Log entry 34954: process socat pid=16082 uid=812 src=100.56.70.196 args=xl9-gsnq7tk10g3e tvi97w4j4m8zieact9-m0nimeudxn8m
  - Log entry 62925: process python3 pid=2531 uid=516 src=156.191.0.172 args=iodkg/a3atj4ra1f9wjvtohvj0llt220pfgsbn7-34sps5fb
  - Log entry 58402: process ruby pid=30872 uid=220 src=104.200.6.170 args=xmqda6wv9ae1-0rf0s46y/zr330k8i6q9wsoz898bzxc89jf
  - Log entry 39116: process wget pid=28459 uid=497 src=177.236.111.156 args=z09nuo6mn/6rqbfy y-rteo4el/o4yv3wzcsih4ln/5f4z9h
  - Log entry 24426: process python3 pid=13889 uid=688 src=84.198.86.60 args=8oe1mq0179k9sp5bk k09s8deab8c7692ev5g1d0g00yeq37
  - Log entry 72360: process curl pid=9454 uid=346 src=162.216.80.4 args=oatsshw1a9zgxg/e/sjxxl2jgq761z6i02vjoiue68w95vsp
  - Log entry 87609: process nc pid=23701 uid=36 src=111.134.39.166 args=v2ia2u7krg6msp2ea01wfj4u09s1 lq mc4wgc urxw9auum
  - Log entry 37785: process perl pid=2603 uid=216 src=16.23.226.46 args= kdgvot9yn9mu37x6fwx-tez5yk2luzr3a0/c6bf4jrx84mr
  - Log entry 52691: process sshd pid=15005 uid=761 src=192.74.98.150 args=8lwha3u6qap0yr-e67 zqsz6nm1egvz2a8i6vlizz1j9r197
  - Log entry 93815: process wget pid=15895 uid=15 src=79.208.163.87 args=0q8nf-306v4glr4pi54k 9w87tmu7pud3ev5d t3sdy4p2og
  - Log entry 65336: process curl pid=22200 uid=860 src=47.104.90.229 args=vfw3-tim7s2/twp62s9x0eeikn830b5fjfzp3t49m43h0ksj
  - Log entry 20866: process bash pid=20248 uid=181 src=48.221.201.65 args=r/s76u2z2sjx9ctpz8q8ohikycvu-26t1y7 9 cswhho6qqj
  - Log entry 70588: process python3 pid=14598 uid=162 src=16.211.79.241 args=nxxc5i114mtao2k6ux9 lh5/q8ify897f7 xnur440x6q xu
  - Log entry 34257: process curl pid=3643 uid=710 src=64.234.128.83 args=2cjiqzaejb93xr1o1boli4x35ak4haqy8/db3ln/81o/e/xe
  - Log entry 27067: process nc pid=17818 uid=529 src=91.97.14.138 args=sfhzofzni0syqr688ruhnhakce3ebwdqx2h cbltcpx2lr5m
  - Log entry 67230: process socat pid=26241 uid=207 src=115.119.72.216 args=um0680v-4fmti-b43c-/crqee-7s 4pvsorarbevzns74s9w
  - Log entry 31119: process curl pid=26070 uid=669 src=142.173.223.39 args=8omp5rn110/fc7gn6/vonij314at/sasafzhl45u15v8hevn
  - Log entry 32907: process curl pid=28222 uid=609 src=181.169.227.117 args=gof57n kic2z39dt9u-njeckark78 121--pluai995i2l97
  - Log entry 76703: process bash pid=18659 uid=142 src=200.124.138.216 args=u1gm7cjnncyt336gxn2rc8jl27e72ilng5z/bgiowx882viq
  - Log entry 90803: process bash pid=30537 uid=262 src=203.120.48.221 args=0/ hdy-5 ejvupfi4ejf  dde tzp0f9hetukjhz4vvq 807
  - Log entry 74807: process bash pid=5387 uid=250 src=89.149.85.26 args=nlj1uvy ichyki2-wgo73l7cngc80ckh1d3rm4i6r7rlspp7
  - Log entry 46339: process socat pid=18070 uid=379 src=103.193.119.80 args=reru/ugx8-1p7wer3ow1gjmci/rvaf98qs6bs-x9fn n1nw0
  - Log entry 39584: process ruby pid=5389 uid=273 src=138.97.191.92 args=2xv2a93msah9 f2irgq p3guw6quzryuielrttb5pku5u  k
  - Log entry 17237: process sshd pid=8599 uid=646 src=189.90.221.199 args=g/kdft/6fk3z0j5sj958dqwor51huf5b3i8a/gzyrk7h2crt
  - Log entry 74092: process sshd pid=25857 uid=527 src=7.233.171.216 args=m2mgq7pkajhxxzg3g4n3e 2ablnqxafg15nqclwbq7exutj4
  - Log entry 63928: process bash pid=21734 uid=914 src=35.71.192.64 args=5 5w9l6b qh0g7az3lw7h7wzf2xd00u4 pzuopxy5nunuozr
  - Log entry 44122: process nc pid=10397 uid=845 src=168.150.46.249 args=nk04mx8imtyk72zcw0gbplpyud2-qe18vzbrf5n fe80dz/7
  - Log entry 74614: process wget pid=26984 uid=855 src=96.17.109.249 args= /yx1q7l46wlnp10pdevxj/3ixo-6lkg2b13//hoxe9sc5wo
  - Log entry 50067: process ruby pid=5588 uid=540 src=197.201.102.52 args=ywow3mvs2r5mimmbqzw0hbswvaue sgt-dde8 03816uw05m
  - Log entry 31259: process wget pid=22196 uid=57 src=118.114.189.156 args=bz6spn7p2aa/tle4b w6nta-te1jf2mhpuh95yg5hwrry0wk
  - Log entry 36374: process sshd pid=28016 uid=328 src=169.194.151.210 args=4fuhh6-ml63943igdyc23v 3-xrxi2unme2c2m agr0/ew0x
  - Log entry 78376: process wget pid=24291 uid=170 src=129.53.172.90 args=xhlqmbusefhrkm0s a1lmqnhmivulxc4or9/p0p9nsr7vwjo
  - Log entry 43132: process socat pid=11436 uid=209 src=176.22.35.141 args=d6jsc6/yogu ps 82f0dwh9p79wbyyla00kh4uvullocpbue
  - Log entry 68346: process perl pid=30757 uid=505 src=94.103.175.136 args=lmy45dzl-rg9awzi01n/9qrulneqsdrtscme0bq-qtzu3e/i
  - Log entry 72594: process wget pid=22494 uid=156 src=114.157.208.41 args=sbld3abj1np9-wy52c2/3 z2zlgfwis1yw35nxpsvjlg8emr
  - Log entry 58536: process nc pid=13209 uid=289 src=181.229.19.249 args=skvrkww/g5t3q-5lz9f/omg7k5gvadsnxqx7cuvf7g744oey
  - Log entry 74374: process socat pid=6562 uid=85 src=101.93.71.222 args=m t/44r/2j6nd6i362mk/3 oqhmxe7c7qxjl2/ct4mlnfa5b
  - Log entry 25984: process perl pid=23481 uid=251 src=18.169.158.121 args=0ps8zrbxk43/sicvfysiakru5k ymfxr94w7q296389vvry7
  - Log entry 23094: process perl pid=30370 uid=190 src=137.230.11.249 args=-1usrdvz7w9-fzpyqrpov5gtirfjme19ulvtubhpxpj-9/7x
  - Log entry 30666: process socat pid=18688 uid=882 src=23.206.240.85 args=fjeiveaapc8 s-tmyo4774rup70dfxz0saffv9616rkbvv1j
  - Log entry 92928: process nc pid=29071 uid=993 src=107.152.208.74 args=z1-fhcqn40os8gwmroqs38-e3nx6mz9mep4u0dv8mc1/0zg 
  - Log entry 46075: process bash pid=4909 uid=5 src=202.212.29.168 args=x 4n56/hyky-2imy10x9drsp/ 0tc6sd5g9m7m7 p qnu097
  - Log entry 24000: process curl pid=4705 uid=385 src=67.86.93.238 args=nrq/gf0a7it63zg4h16s7mok4oeyyof v02kby8c/hwh/k2p
  - Log entry 36447: process socat pid=2105 uid=190 src=193.156.44.130 args=bs45ez/htcrqfqilufp3h6bjh6kgp0xz7kh-fl4j3pnnkg8y
  - Log entry 25193: process sshd pid=15321 uid=325 src=41.86.182.59 args=0j9tbhy4dh9qa58bxrnjwmp1ctytb5fh2sw7wzqyz01bg4/f
  - Log entry 11986: process wget pid=25642 uid=349 src=34.133.195.120 args=p--tlsme/u4rfi7g u6w5h28gxflbw0w83g0a7w-z4chdhc9
  - Log entry 34613: process ruby pid=21422 uid=399 src=74.56.45.246 args=geh4uofq/pf/uuq1wkpc986gfm-wsf- k7purqryd4zxb4cg
  - Log entry 40973: process bash pid=12872 uid=848 src=81.1.138.166 args=wrrgfwxjbeofxyyu9qi1 l0fu- 1xvf-y9v0r7h5cj4-5ff-
  - Log entry 40557: process curl pid=18212 uid=510 src=21.33.4.43 args=ybjuiam818iif/osi-b202oauluyhlsp9i wmz46va24m5kx
  - Log entry 56878: process python3 pid=7227 uid=639 src=173.165.169.10 args=4otd4-k0rmjlybbx/vq0url--r82amlau owhtm3vjzhlspd
  - Log entry 27650: process sshd pid=23383 uid=116 src=145.33.56.116 args=m-aj-uar 2ai2 09/dnr6sylifm2dr3o-kexeox6uer2vpce
  - Log entry 76410: process socat pid=31804 uid=331 src=65.234.2.179 args=xxgir-3x/sef8p79dutvyjqmtv477yp52s5ni6i-xcc6p1vm
  - Log entry 23921: process socat pid=8686 uid=125 src=76.48.230.187 args=guhf-xl89qwgdz22rx8-jcu1qpe9vnphek-rs2hk2ygwfbbq
  - Log entry 81072: process curl pid=30099 uid=758 src=15.180.173.224 args=p75vdhe6rlq0yn-xgqx/uez/-pc8w3gwnjq4bnu4epyau/vk
  - Log entry 63627: process perl pid=3679 uid=719 src=157.9.44.4 args=bcjusdis/w14zjrbyhcu4tlmv1d8 guiin34hzz0khm56r99
  - Log entry 86235: process sshd pid=1948 uid=119 src=126.250.20.126 args=1l/rot49v784jl9kfxj934vrkck1uoye b5gadstc ns04e2

## Supplementary Technical Detail — Section 15

Automated correlation engine identified 46 related events in the 6-hour window.
Baseline traffic on port 58439: 2 connections per hour.
Observed traffic on port 4444: 92 connections during the incident window.
Statistical anomaly score: 0.864 (threshold 0.750).
Related CVE: CVE-2026-19125 — not yet patched on 7 internal hosts.
Affected subnet: 10.8.5.0/24 — 18 hosts in scope.
EDR telemetry: 4 alerts suppressed; 1 false positives removed.
  - Log entry 29884: process socat pid=31259 uid=894 src=115.55.120.208 args=ry11p7tjulrw303ad5ovrr6reb8/6a lukb93cjldiyu6k/8
  - Log entry 78411: process bash pid=21985 uid=917 src=27.76.35.207 args=t-m/fgul1sa6-67u7a2q/4el6ydlkefhi9nr/xo1gejg9cq0
  - Log entry 84371: process curl pid=12956 uid=836 src=157.171.4.61 args=/isv5e132zwascy3741bybg68gn82g8wsyf5mvzhzme7882v
  - Log entry 63758: process perl pid=27658 uid=620 src=143.168.71.240 args=p9nqfjmv2wu1ipx5c5r 3tccalwp86vgp08vom-o531zfnqs
  - Log entry 34143: process nc pid=15316 uid=975 src=23.253.83.230 args=ancjx6alk3ie4bgs7hdpph8vwh7t icn hut5dygr y4j-ae
  - Log entry 36874: process nc pid=8656 uid=28 src=117.23.74.168 args=gnort3a8c0qj3bp64vvsdh8j/6 ub5lkpye c4mbw- e5l/z
  - Log entry 20954: process bash pid=30991 uid=496 src=93.110.53.11 args=48 -d4teh/9kuaik0vjt 5byysjre-n5d-tm5mgm-7q3c7yy
  - Log entry 61345: process socat pid=23730 uid=102 src=93.100.57.74 args=euv2l6t uc6th1e35swyco/robeychvcsbiah998zvkqgqwm
  - Log entry 31011: process bash pid=27301 uid=364 src=159.45.49.11 args=iltxxlj16msf1dourpyuy7ik0 pd/ux-3ma1iy/xuvx5sg28
  - Log entry 42035: process ruby pid=15115 uid=12 src=34.19.80.183 args=xuuzj17gy57y19w1s/u50a32 ep7kcqe5b93kywxzulkzw6w
  - Log entry 19149: process nc pid=2539 uid=504 src=205.115.16.124 args=3mnh-t4l2eisu7jgoh2yrxyjkk72sidmv47 ffi4eftkvgo5
  - Log entry 80024: process wget pid=6187 uid=185 src=191.8.135.1 args=l43owcm7sk3z06f7honbys/9qun3p85vkp7aarwuip188q1v
  - Log entry 72501: process curl pid=27368 uid=483 src=173.225.244.127 args=54xtf-sl0w-1/7bodtmzruk-gatfgkh6kl2rrpnx6/m23p8u
  - Log entry 62038: process python3 pid=2492 uid=725 src=22.216.162.247 args=pfgv54mx8ms-hadgyuh xp2n x5wkb/6ez7677bpoen89ud8
  - Log entry 59317: process sshd pid=8547 uid=976 src=157.143.229.170 args=u5n4ymukh8g5si97lt/ah9owsy-slu4139iyyn 9j5cimup7
  - Log entry 28405: process sshd pid=26074 uid=803 src=60.251.110.155 args=4-40xubjx4mic6m1vnmvuzncmem59cr230434fwxin-khfna
  - Log entry 72476: process socat pid=13672 uid=148 src=30.176.95.215 args=vanpr9f8dudvm0bs luu75wsmhc-skq233j6jggv4//82z-r
  - Log entry 41843: process nc pid=29674 uid=504 src=108.245.67.206 args=0l4dhzzba986hddd5ig8he8yy -fylmqc3hybbs1 /v4wmoy
  - Log entry 44628: process wget pid=28642 uid=406 src=101.118.45.110 args=sw3inad7 4 vn-cgfyuewpxgoyfbqx18samoj j29cjmeom7
  - Log entry 63443: process perl pid=25771 uid=184 src=13.223.107.1 args=ctmyd1y65 35zx8upd8 mn/kl6brezdr7-ymjg89d2 g35kq
  - Log entry 81638: process curl pid=15842 uid=657 src=68.114.243.212 args=o6rc/x798owejnur96gfk1d1wly/17fa111 cs/zy6m3x5 2
  - Log entry 77699: process sshd pid=13048 uid=145 src=26.100.71.215 args=jwbjjdpjtvucdzrzfi07-xugw0 dj2ny1w1h4j6ox6vswoh6
  - Log entry 19598: process python3 pid=19159 uid=487 src=72.212.119.244 args=mq6e7jj2r3e9 j3y d9a-hd2-m-wcge1ngcpu5mgu5pp886s
  - Log entry 16387: process ruby pid=29714 uid=55 src=149.97.153.5 args=f5/f/lk3bh8-b0v-u8aekm49nm2e/-pcx0ufecqglt6bxipi
  - Log entry 25244: process sshd pid=19200 uid=351 src=80.251.103.220 args=4gjfarr0bb0fw8s9nu9zm b45o-h82/p7wkiqaoxt9n2bb13
  - Log entry 34260: process bash pid=8329 uid=256 src=15.153.90.3 args=s1hdk725l61l1aus3-qz 2xeyjd-i8r3myelqaae1iq nreb
  - Log entry 70377: process perl pid=16624 uid=48 src=88.39.119.118 args=ld4tovi6o 7vg8id1p4qbd292s-/3g j8ioe0-s32zwrznl5
  - Log entry 17827: process bash pid=15533 uid=730 src=3.232.237.171 args= p55ohr he7mc-01tz8mvo8vqd48qyy0vwrrmlheyxntlgav
  - Log entry 56776: process nc pid=15305 uid=598 src=21.152.124.213 args=yd63ezorwh js3ae388z-y1vfwrblys/wixo763cmkbly3/1
  - Log entry 90711: process sshd pid=5921 uid=233 src=60.60.49.92 args=xzv/n/6yvey/854/ouik/wxomlydf792qvqv3ndrhb //b5a
  - Log entry 51816: process ruby pid=23015 uid=274 src=57.126.22.124 args=/0fb3x0c/4uzs4hr7kfd7qv528f1q276jx/07vs2w2a lm3z
  - Log entry 98312: process nc pid=2841 uid=118 src=193.235.164.171 args=ergm8d  lqmdksv4nv0iefhehf7zuokgdr4strl1b sh5y8h
  - Log entry 33197: process wget pid=30376 uid=811 src=49.45.190.132 args=b1ius8njnkc1i/7vq41l4rw00cuzjivasc2kfnt3b6lbwmgm
  - Log entry 49490: process bash pid=18360 uid=136 src=54.180.177.41 args=v l0r169w flb d9s9qg1g9/7r7njm25/w-f/dhtyddb3r7-
  - Log entry 15368: process ruby pid=5879 uid=176 src=59.139.210.89 args=v9gz3h/gprcynlx379ce8k5vmcojhbuy-d8tha38fnoqq/gt
  - Log entry 78893: process wget pid=31170 uid=192 src=196.160.233.121 args=ogaa19eaz5m8-npd2fzrzdhgy82kk -htk/8q624ae3cx04s
  - Log entry 52144: process perl pid=17979 uid=645 src=112.87.234.132 args=wf rsse4hxxiqcy3yh55s 3/uj 5y 9-x8799ile7psip/gf
  - Log entry 51927: process bash pid=30575 uid=901 src=120.47.226.104 args=/zxe39c96pkzd1f5lszil0ynumhzxyec/bpdi4s x0658-lr
  - Log entry 29363: process socat pid=16723 uid=606 src=30.250.212.79 args=6m/tiy2k5vn95 -fi4r455tv dx-rpes  0uao1e q739psi
  - Log entry 40342: process nc pid=30791 uid=861 src=133.80.179.103 args=qi0diqn9//wq6-maqn65j--  v7o88zsb9girg735m 1x 7g
  - Log entry 79469: process perl pid=14394 uid=387 src=19.96.184.125 args=lvz/-jwmz37-t7fwcvkg87mcp78-kv2mvacmrhgjh7rlskn3
  - Log entry 54441: process socat pid=19721 uid=683 src=94.248.137.201 args=kit7x62pozcuoqclxdm-ot7clggawwqx4e051clwro625i/k
  - Log entry 34534: process socat pid=11310 uid=540 src=23.42.53.27 args=k9wfk6yg/i5il0 joc8qzem9ipzk/0trah5i6m4usoij5605
  - Log entry 17466: process wget pid=3961 uid=309 src=77.80.63.93 args=b27ls5pwq/4bykvw1r7nu4 1rbr4z5eohh4j3v69wrsufk0i
  - Log entry 43525: process nc pid=31422 uid=827 src=6.200.239.73 args=35i596wg80c6v6al0p- l4kte/mpe6orese6bwde9j--riri
  - Log entry 77895: process nc pid=14449 uid=928 src=153.90.6.98 args=pd8mreegfbktp7w1 ulsf5pf25l2vt54-7417jg6nk2ddv9a
  - Log entry 45336: process perl pid=2166 uid=506 src=177.157.59.139 args=utrx4-7e8t0j hm/di-tm9i0gxr69s9mxcpprsx18omdvp/a
  - Log entry 93337: process socat pid=21512 uid=445 src=138.74.2.138 args=f0z/vu6k-nr1-z4k2he/05c1tsyztec9k9chtzplburdg3kk
  - Log entry 49896: process ruby pid=17705 uid=837 src=33.120.5.147 args=4ungjodfhhquypg6n76l 93cxri44tcizuzdz4ud7qx4morc
  - Log entry 73157: process bash pid=8831 uid=648 src=161.222.8.100 args=u a1wuepk8ttunuf-wdme564pzmyrvg4kwxq5azzzihif6je
  - Log entry 28091: process nc pid=26174 uid=306 src=128.64.60.54 args= 4zweo70ktk70wxwy9rd6xkjxzfap6r/v8sv8rngq6zcdv-o
  - Log entry 80937: process curl pid=17749 uid=418 src=172.2.228.111 args=-8htth 7ljn0gkw-p9azji8//0ke70ohfm11nskd1o5 0saz
  - Log entry 89798: process socat pid=30032 uid=112 src=150.255.42.61 args=myt/ujsapvof8a/s89lhi/t3y-xlkqlt5/lha-36lses5hhb
  - Log entry 74722: process perl pid=7710 uid=242 src=180.189.7.116 args=mqi-c12uy8gjez9-b9qdw6d1zhb3r7b2vsw4h 8q 5ycbov-
  - Log entry 93895: process perl pid=2702 uid=405 src=170.172.178.176 args=pkb7h0o1yfh3ivt0baig2ood204pk2e 3f6p3pocok19-guo
  - Log entry 23596: process wget pid=12105 uid=810 src=161.142.112.90 args=ujy/9c6c1b5lbshnj5va43s0r17whicvm/scbx/7mrv-g lp
  - Log entry 38354: process python3 pid=14751 uid=511 src=105.197.215.199 args=cj8g174m no1 99gyzvfc8f0ztj uqpc9zv--dtb//b6/b8s
  - Log entry 17281: process wget pid=23180 uid=179 src=161.19.107.226 args=b10t9lzasl6l8s 36eqll1r4q0q/cjwh9nv0n5xns51qvuqt
  - Log entry 55602: process ruby pid=4350 uid=224 src=159.16.13.156 args=rvlozwcei2oj9xjugoh381iy7d/9-0ap695tn7e4qzpi4ofz
  - Log entry 86101: process curl pid=30736 uid=789 src=138.168.146.143 args=0to-j6os 8exjabif6wz2w4eqb mv2slzh goxr-/h7/399n

## Supplementary Technical Detail — Section 16

Automated correlation engine identified 42 related events in the 6-hour window.
Baseline traffic on port 22676: 3 connections per hour.
Observed traffic on port 4444: 51 connections during the incident window.
Statistical anomaly score: 0.837 (threshold 0.750).
Related CVE: CVE-2026-40651 — not yet patched on 11 internal hosts.
Affected subnet: 10.4.3.0/24 — 4 hosts in scope.
EDR telemetry: 2 alerts suppressed; 3 false positives removed.
  - Log entry 84090: process curl pid=2001 uid=762 src=93.8.141.80 args=grdeswj6utw2yxv3tjc2vc2bhcmlswqdna5em 8fv51wykhj
  - Log entry 60693: process nc pid=25687 uid=71 src=162.123.33.129 args=asn8q21rwyn7tvppuvq7y0xzt22bvtujf7y1rgkwer0jo--q
  - Log entry 16770: process perl pid=31522 uid=46 src=42.1.131.37 args=hwf gjqvsvb1f7nwk sw--iu80ji42hv3wz3gcxurj2ss4wy
  - Log entry 77076: process bash pid=14417 uid=466 src=184.194.89.215 args=g0el016 wxtm5f348mz-8pmys6bp5zb1r68/5s69vakd7/ec
  - Log entry 26231: process perl pid=11025 uid=36 src=60.100.94.93 args=6yrrsj9pu /onpx3r5ve28k7pr /sybervwlki4-40i6t8q0
  - Log entry 29708: process nc pid=26042 uid=450 src=63.50.242.73 args=o81p876xz6w023lfqwg6240z15gmqb0 bk4d06q5nbaopbnp
  - Log entry 84547: process nc pid=13878 uid=39 src=15.27.245.52 args=p3bowrix27gm9aik0v2pjkau//y98961n8zqao-pow70-ytu
  - Log entry 63010: process socat pid=16861 uid=52 src=181.125.197.174 args=xba9v-0r84fw9lb25phgpv974kco-6hyt4i1h/n91zwbi3lc
  - Log entry 34836: process python3 pid=14886 uid=269 src=212.107.136.198 args=3pm1--cpuioz1vkmwplld2sq1od3elkslbevo 157hqkfjai
  - Log entry 32966: process wget pid=25894 uid=839 src=164.153.73.138 args=lkk61jzvtw xa-pk7bd3f-vqiga0g4z8b7l chcwq7/tvmt5
  - Log entry 59194: process perl pid=2631 uid=697 src=83.225.191.142 args=0nq2z01w2z1rgdm6ump-0jnelfkkjdrdqjy6b80-xwk6zlbk
  - Log entry 18726: process wget pid=7449 uid=56 src=105.182.124.2 args=/3zvy6effnt-wgjp-jhsz275nkm80ai qalcppi2p t9b5o2
  - Log entry 85274: process wget pid=31720 uid=382 src=29.174.0.72 args=p/vy-d8b taybkz hgsrek6zfmc1lsc12c/vp58f951iea//
  - Log entry 60155: process socat pid=26198 uid=897 src=52.91.176.71 args=k304t47ylxjfehvl8hm4-aaz2441784rc3qe9  kij kf2xo
  - Log entry 66740: process sshd pid=6097 uid=28 src=65.135.186.201 args=ja1 mjr2shk-e0/jv8a6d9kxvw01nuvt60481znea5n8wmsz
  - Log entry 74430: process nc pid=8927 uid=619 src=26.228.6.119 args=ow85wih-50qs3tjmu6ssmfsaml1lbf27vahj6g7fcgndog7j
  - Log entry 63829: process python3 pid=13014 uid=21 src=43.208.106.40 args=l04e9wy xun9swxtq4m9pp5h/qrcpcy9po4 90p5-li2j5la
  - Log entry 15868: process bash pid=9856 uid=244 src=222.27.222.176 args=--1u4vqg96l/84225 0vary/0dl9bo1kicbfbz/sg2ztr26 
  - Log entry 78732: process curl pid=23504 uid=473 src=93.125.120.240 args=uvq8tncrplaobpbp9dchygmqk9g5fx/6riv49bsd8w8 yo8x
  - Log entry 43282: process perl pid=13939 uid=775 src=21.195.70.86 args=dgwj6 v9m/ow6/bsbg6xwq4 do4jtb-gwl11xbrsr7hgi-kv
  - Log entry 49577: process perl pid=17455 uid=195 src=179.162.49.177 args=gj0vryj6honoue3zuwxficmk2vvzbp36uynv/2p2f5b1/vo4
  - Log entry 86641: process sshd pid=24505 uid=957 src=190.117.237.173 args=re2caxy1ta62siknvm 515ly-rm5kozrnotreg6ss7zdjmkm
  - Log entry 75396: process curl pid=11963 uid=789 src=79.7.222.50 args=okhvoaprg krfbyh02ailfc0-/d5dski2 5zic-5zvk1bsgr
  - Log entry 76002: process python3 pid=30187 uid=871 src=103.123.212.113 args=1m0ihnai38l/fy8zvnz-8jrd/5ivnr3yn6n0ljl444k9pmbl
  - Log entry 16046: process wget pid=27071 uid=848 src=178.120.226.200 args=lexqx7hgqcbgi178sfe1bsm4cn7ajz9jq2bcf gsl7dzib8a
  - Log entry 25461: process perl pid=18677 uid=446 src=6.149.8.65 args=w/n80xmll2js1rxsncgikba1w26u1lfmsi3s6dm5m-lmg4q2
  - Log entry 61199: process perl pid=27359 uid=700 src=3.162.40.121 args=w5c8xrq1 e-efggq0sbergfscxoleooasbuvnjz86fvbelqn
  - Log entry 79376: process wget pid=13383 uid=376 src=214.86.104.98 args=a2ysdckkn4rb vuxpp6d3y luwmai5horwlnvot853 tb4a6
  - Log entry 71604: process nc pid=27387 uid=351 src=19.83.143.70 args=th1bix4s8rqs33akk1g8iy40366plt -9ddufg085zs8d4mw
  - Log entry 60965: process sshd pid=14418 uid=832 src=112.49.84.151 args=want11ti5e2 3tavq5nfa-0rcn/ellahn0x17be4hjockvcv
  - Log entry 85732: process perl pid=8587 uid=38 src=63.226.49.115 args=gtz4/5z8j-5bqw0 k3ghp 2f325m62xn0hy7f92bhtm4tn f
  - Log entry 68235: process perl pid=18240 uid=70 src=97.101.152.240 args=uxncyxl/eh9rtgoylpwrecxa2-mg3dj6sz 7zbipc-ov3yj9
  - Log entry 75611: process bash pid=14841 uid=569 src=2.186.34.9 args=5lr-u9 kbl7bvu554gp-9nxck9s 3sg1a12asknuw9umcdf2
  - Log entry 66156: process curl pid=12488 uid=699 src=24.136.218.54 args=ekz2pe5s7ii/32nf5f1zff58n7x18a5oovzb4jgkdivg215g
  - Log entry 82751: process wget pid=28463 uid=984 src=113.14.84.87 args=8g4wosojikkjn8eb/zrc88zxl793/xgwet97yjowzbfxb0o8
  - Log entry 42030: process ruby pid=7964 uid=476 src=139.54.123.15 args=dy5o5km//6trbw7c/fkrk8sdmeqws9gq sg084-tu1y0fm5a
  - Log entry 47206: process sshd pid=6769 uid=580 src=187.189.88.211 args=4u/6-rti9x86v74t/gj72gnr1k-p5zzqnhc6bkckwo75k1d/
  - Log entry 44157: process socat pid=28475 uid=901 src=23.231.123.150 args=qq7ra/312752jaw2e9rmmwzu fbsaame/hl131nqny95m-68
  - Log entry 28216: process bash pid=3031 uid=124 src=198.2.184.240 args=r73m68d/n9vlpqy1abix8p/q7bzdh50o5dw21lcxl35xajb6
  - Log entry 69549: process ruby pid=27444 uid=194 src=182.244.115.225 args=adshwhs8jn7bb5nj ghyf--c0ck5szhz4edf/u57axwe7f3r
  - Log entry 85143: process python3 pid=24071 uid=737 src=208.149.108.215 args=-zgxfv5kj36143-9c7c/f04-hhv d3kqmiqae/ 1yv0/depx
  - Log entry 76417: process wget pid=19150 uid=86 src=178.213.117.202 args=2rqoihzo0j35gy3e2/qx7i 16/1of433ucjbeo- 6bipg4t1
  - Log entry 74839: process python3 pid=29493 uid=797 src=90.189.161.3 args=k/ki1im08bczs0wdlcmk3h-cy7b5r5/n00j-1xwt 83x4e8v
  - Log entry 96975: process nc pid=22921 uid=10 src=150.47.29.181 args=milq/ro7p2pv5wuiyqfs movxxrbtg3f75esqcr6xvv54/r1
  - Log entry 87004: process socat pid=17654 uid=440 src=207.74.184.111 args=2faxgogng6641ynhs5ec4eu cv4xa0he5ra8eamt8/2pgfbf
  - Log entry 49952: process nc pid=7061 uid=866 src=5.164.19.28 args=ydee68qf9-/g-3m3jdy2jumvkiizusd9be3xt4mmm7kywwvh
  - Log entry 62099: process ruby pid=19254 uid=11 src=214.71.141.180 args=se0chaba4invft5cay53x vora3rwhr r8q-mrxre t3/4ud
  - Log entry 45744: process perl pid=5425 uid=252 src=60.134.127.165 args=6sea14bitwl2-af14xcx 1id3jfo0r75q lkjpo-kvb4jabb
  - Log entry 75356: process perl pid=2452 uid=513 src=132.132.124.131 args=9r6e44712u6dke8bm8cn7rxjq42d8sq8vct4c1tef961g9hj
  - Log entry 91219: process perl pid=22807 uid=119 src=45.254.117.130 args=u2ssjzlc0g4n1vhb2k07f5rzt5wiyv0k80y30bi05bptq4yc
  - Log entry 33878: process curl pid=7234 uid=140 src=44.251.243.58 args=zth72jcm7zvsx3uoq9prxznj-5vg2hkf/p-kmlglmc4q6moy
  - Log entry 13677: process sshd pid=24103 uid=144 src=98.79.235.31 args=2c742sz92mfsxgsc6wut7y5/-h0ddjgeh8g /g1 zu80k-7z
  - Log entry 15250: process nc pid=11393 uid=862 src=165.32.27.59 args=nplzwm4s1q dqfraip xn4p7kn/zg8g6ibuwswgc4c/zywbj
  - Log entry 49418: process perl pid=24814 uid=292 src=149.206.133.108 args=79t3hbds30j18thdskw6-1dxhcb5qhkq905bc7a5-kxrj72 
  - Log entry 42121: process perl pid=9413 uid=441 src=33.133.81.85 args=s/q417ykulbkppkkowz1m-k8c3vrv50i8cz1llpx7zn29qwt
  - Log entry 64455: process bash pid=27957 uid=794 src=43.37.169.66 args=uo0b2eh3k39cnio9qoe9xn04e2j5timh89pzpwf3cafpq7fe
  - Log entry 69527: process nc pid=27186 uid=733 src=64.73.97.15 args=44d72557l60r56-5mjsv 23z6owz sjf4 d3t-02vfrvrd0a
  - Log entry 62346: process socat pid=9110 uid=140 src=36.112.11.238 args=d12tyikjhin 3rsrhi0hvzbdnnczz311a09l5uuedsszt5j8
  - Log entry 48553: process nc pid=13040 uid=372 src=164.252.72.205 args=xvr-7 fad4a7phwy/wh9c -ctocvshzq1jr9io1p3k0- paf
  - Log entry 24788: process nc pid=16516 uid=834 src=141.48.0.139 args=gjq8ae90favhfsl9uq0matje7akc01j7cz2k bvwu-/ncx 8

## Supplementary Technical Detail — Section 17

Automated correlation engine identified 20 related events in the 6-hour window.
Baseline traffic on port 7507: 2 connections per hour.
Observed traffic on port 4444: 135 connections during the incident window.
Statistical anomaly score: 0.806 (threshold 0.750).
Related CVE: CVE-2026-34770 — not yet patched on 6 internal hosts.
Affected subnet: 10.10.0.0/24 — 19 hosts in scope.
EDR telemetry: 0 alerts suppressed; 1 false positives removed.
  - Log entry 64589: process socat pid=24508 uid=552 src=42.66.193.193 args=eebvxffxfgixj8c2mrxbuwrmi-eiky7l912shw7ad37lzn3j
  - Log entry 59915: process bash pid=14265 uid=314 src=127.178.167.175 args=1zspjr56lnc60lr4dzft6mvvikj2fy8z0z92qyp50j10uaam
  - Log entry 70591: process sshd pid=2374 uid=606 src=2.46.108.212 args=j3k uzqwhnbwi-gxsgjd4w63vy1sivao2zm6c8q4961t6s1s
  - Log entry 53242: process sshd pid=24742 uid=368 src=206.231.177.85 args=uqv7x0yjior49te2lv-fj81ya//q0upbtf6e6af66qdv82cs
  - Log entry 18765: process python3 pid=9274 uid=272 src=29.8.70.212 args=481xmbrfr64yqmbxn4e-8pjz4khm1pehue30svait6m9m2fm
  - Log entry 19923: process nc pid=28347 uid=783 src=36.44.40.75 args=n/6sixpptxgl3zulp1d3ee1-f-5 gop14-0-8zvl7xd89wn3
  - Log entry 19448: process sshd pid=31306 uid=340 src=1.248.107.253 args=a8-/dn0/-xe4wuiysgu4ueucavij5nbvgxpggn3two r-k/h
  - Log entry 68368: process socat pid=27767 uid=560 src=149.195.51.157 args=-lw3 7kxtvvnla020v8rfgamvht2h-qxtwv7w6uxcsiwyeco
  - Log entry 12620: process bash pid=1866 uid=574 src=69.204.88.15 args=tc6n-yrte-tqard4-j-25chrygdou-ia8ta8websj/aiavhz
  - Log entry 46273: process wget pid=31762 uid=608 src=2.85.63.45 args=ypz/tmgn o-l2oca-6p634o4t78ip2ydgcytaeeqqgj14dk0
  - Log entry 92104: process python3 pid=10146 uid=701 src=165.207.27.57 args=pw/ak7966x52n0xd esvupv189to5jkckuzdeh42etts822r
  - Log entry 89673: process sshd pid=3422 uid=13 src=121.215.21.87 args=ysegu26txqppcxy1/07ob10vyehm0awqf9 4irq5nniw6s1n
  - Log entry 74955: process nc pid=4473 uid=612 src=158.230.162.246 args=v138f3zb5qvwho4dziluaemnki7qfdiui-iym6w64r1mx66/
  - Log entry 55894: process wget pid=24484 uid=227 src=120.235.227.210 args=8q0nu/8ru9zqmv/tb1bse4zxoa-b1bxjmmzk7i0wm1e//j8i
  - Log entry 99811: process wget pid=28746 uid=133 src=218.209.17.24 args=jy2fgrt7zrioi7uarb3my72cbvxwxh37j- cmv/q65i8-4qs
  - Log entry 30156: process nc pid=31251 uid=258 src=191.56.242.166 args=l/e0ezwicylspqv8agnfj6191-e/1qgggr4tcr8 sm8q9slf
  - Log entry 95408: process bash pid=6141 uid=713 src=25.32.54.152 args=dss89vii9bjt-zu7tnmwjvxo0h1w4x02jicapsmvc/bth1qo
  - Log entry 35799: process socat pid=15870 uid=896 src=98.140.35.144 args=38k5o 52t-5r9 jcxfit4z 543a9za61z1a5dqspdvp5kjsp
  - Log entry 61445: process wget pid=18338 uid=709 src=89.148.231.202 args=9231lj9f1qx5lmqj/x4bjsgxophohctjttl5hmw0452x5 vt
  - Log entry 47725: process socat pid=27804 uid=91 src=67.115.170.78 args=7/bxo3 njd 90ksiwve0/  c75jldx9ocj0/8n-4dgwwp792
  - Log entry 30765: process perl pid=27346 uid=954 src=202.142.241.243 args=cup2yvrm9/qnjy2g1w4nu 1zld8hx2fmp14roe5gtkzpa783
  - Log entry 87123: process python3 pid=23130 uid=727 src=87.246.17.51 args=xjbw96 nqmwclox30208upt /-s66y/rsn/u9o-2sm9 dy2d
  - Log entry 78598: process perl pid=27496 uid=687 src=204.59.167.244 args=9  bgeztuv2jpajae5rl4zos q00/pd/idnl34rk3-35zhtt
  - Log entry 95949: process perl pid=8149 uid=191 src=199.144.158.220 args=ypw30eszs5upctmiix7thqtvfbx9jc0z1zp47dsv49q0yvzf
  - Log entry 44054: process nc pid=15481 uid=637 src=201.140.24.101 args=ycpqa2oy0-4lnydia k74v0g 4ji/seu/upg24qx25 6tr9o
  - Log entry 54323: process ruby pid=3172 uid=686 src=94.231.99.239 args=b8rn4nn5wym9/ kup3bl2ye27jx1ji3ec4b6nw 81tmymvnm
  - Log entry 76889: process socat pid=20489 uid=237 src=48.245.196.42 args=vun9vgtaqb/yb7797qr767se073w3a0hl0adwzyy75ryrabs
  - Log entry 60890: process socat pid=29836 uid=219 src=35.79.195.124 args=ktm-qttxwso/gs 2mmv44cp-fpd  76r5dst zn8natn5di4
  - Log entry 47333: process socat pid=28126 uid=366 src=134.11.25.93 args=42uqafi4i-xznel01b3-1iedcpich3tm9f82dcedcpokd148
  - Log entry 87706: process ruby pid=29948 uid=301 src=204.198.225.192 args=rxdik/cv5nef8m/r9e-fo80of1kjzc1-jtqgnwldx2rck1qc
  - Log entry 16436: process socat pid=14782 uid=703 src=218.236.26.23 args=miktr 3ynlx5954vy0o9r59cfn49thg7j1ed//f 1nzac0sj
  - Log entry 81605: process socat pid=4268 uid=455 src=21.51.13.224 args=gffvd7nuh-//tm-00f34q61hlskiw20ehf4jun5zdtaah 27
  - Log entry 75613: process python3 pid=28131 uid=914 src=26.165.86.19 args= z0i3vjk7cwnngav2990q10t077hag0l75xxqoici/yp svi
  - Log entry 93405: process python3 pid=25162 uid=505 src=33.63.108.36 args=6zwmzv/z-1n2xx 7mw9yb0 vtkgrs4rkl7tll1 399i4swez
  - Log entry 21213: process python3 pid=30938 uid=10 src=108.4.162.245 args=tj43o7i86jfglsf244ob73ugk-os77 wacvdswu8gqlohq53
  - Log entry 14479: process python3 pid=26114 uid=942 src=201.233.207.14 args=0ncm w5cs6c x7frg1hx3z2wroou931hcmdmi5ubevtj0q1l
  - Log entry 36776: process perl pid=18490 uid=313 src=177.169.20.80 args=imvhdkwgk - vwipar5f87yv0skvu2 wuao7jt65w7o00faj
  - Log entry 16505: process python3 pid=13738 uid=315 src=139.236.26.129 args=kyx yfrfe9yq uapcg05sbat34qwkqqe8g-/0-3 -fn1cdje
  - Log entry 77832: process bash pid=29748 uid=318 src=126.135.192.24 args=/ocpmyzj7/v4-fyudvhgw2ytapf/zoiceo177oo4i1 icdpu
  - Log entry 19710: process socat pid=10278 uid=507 src=146.177.60.114 args=n kja6vcn4lf utn7dfjpgrx70rkcy6ua0tvma2vgzfhbzpv
  - Log entry 23599: process wget pid=10369 uid=858 src=7.153.101.98 args=fwlta-otn08ifvzm7 y dyhh6lmgnxdrqbdm67yc4dr6z6xx
  - Log entry 42048: process perl pid=10538 uid=549 src=135.166.21.245 args=0 kiy4epn75lj-gsqxvt8u 6kmisv5kv3odmhkby-9tuze7b
  - Log entry 12118: process sshd pid=10785 uid=214 src=96.177.128.13 args=keh71hcsm z464jwlgzq1o7-hko4-8tngxpj5uag9q8pndi5
  - Log entry 19052: process socat pid=1146 uid=653 src=37.113.221.251 args=-yo43nrkfphcz3stawzhowoo734ttoa0 yxw7yhyqmpg7v-0
  - Log entry 99226: process ruby pid=22315 uid=586 src=73.157.88.215 args=4s5wx7g8dgl8nu j5mfxh-vq-3e4hufez2p/ev898bvisacx
  - Log entry 17344: process nc pid=31913 uid=798 src=21.134.158.7 args=-vu84r/1vu 2-88-r/3lk-r7jc9z/1vkt7y/91tl6zyvu9ru
  - Log entry 79805: process ruby pid=20433 uid=880 src=143.30.230.95 args=uk/-2a2r/yt/yly 7e3o43mxw382c38m/8eiuqk7/ryo7dd0
  - Log entry 61793: process nc pid=11198 uid=443 src=72.175.160.130 args=ir4n3yeh2hqg9k6u2qvt8cy99bf11anxxuaw7z7kv2ll-4z-
  - Log entry 37000: process curl pid=2719 uid=50 src=91.1.65.241 args=k/5h7ar6h4rp3rt6/5/ycs7rbpkih2aj40bi2k3b8n6io13w
  - Log entry 29249: process sshd pid=16930 uid=98 src=1.177.107.68 args=7va7j5j4j3/7ukhx2igwgtqjgzrc10ucaomcpuvze7b/c qi
  - Log entry 57343: process ruby pid=25717 uid=405 src=111.138.162.46 args=41 bz b6zb7gst9t15um6 3pwl//qu9-jneun/j yn85gy7/
  - Log entry 93028: process curl pid=19682 uid=21 src=135.169.184.12 args=/4/-7syqm9p9 pfni92ugwy354axhczzbpz52316d2 -ofyo
  - Log entry 60107: process python3 pid=14786 uid=645 src=128.214.44.139 args=je-/4utin2lbrv1uk67qx-9dc4sv382ucosyjo2ygctvwkkq
  - Log entry 78235: process wget pid=20608 uid=329 src=81.236.104.147 args=2enjo21dl162/m wujjhp1sq jh4tl7pxf6ldt1jm-7x-iuw
  - Log entry 32734: process socat pid=21037 uid=438 src=157.62.167.95 args=zsp11cnpf5pw1 opb0a75l2p8391dvph0yp1oisud3rck/bq
  - Log entry 34890: process socat pid=22997 uid=511 src=208.210.131.43 args=za6 hymc1mflrvy36mks9ddskjhguny4h732tlkulvlgg90y
  - Log entry 12379: process nc pid=28560 uid=161 src=131.50.68.88 args=s8l1mfw9t-fpjz8/xib65a9tu2fwnlv/vaftp3xrmo7rrtvp
  - Log entry 31812: process perl pid=11537 uid=948 src=187.93.230.19 args=wewfnqbd3z/psa2w8cx1jzggrwph2-df-8ntib/4j 681vf6
  - Log entry 69570: process perl pid=18621 uid=670 src=195.195.254.120 args=w7p6a/ntk-whv5onevxdh49a tp1qxt9s/zpcow6i8 folvp
  - Log entry 40463: process wget pid=27336 uid=248 src=130.73.7.156 args=14a2h9syjnel3-xj3/4aqvdrez/p1-m81e08rpa8m9hxu3s-

## Supplementary Technical Detail — Section 18

Automated correlation engine identified 21 related events in the 6-hour window.
Baseline traffic on port 7852: 5 connections per hour.
Observed traffic on port 4444: 153 connections during the incident window.
Statistical anomaly score: 0.981 (threshold 0.750).
Related CVE: CVE-2026-30520 — not yet patched on 16 internal hosts.
Affected subnet: 10.7.2.0/24 — 19 hosts in scope.
EDR telemetry: 1 alerts suppressed; 3 false positives removed.
  - Log entry 69459: process python3 pid=25993 uid=607 src=149.6.156.19 args=/5-uu9f 9/v8 s9 bn7uqrn8ohcsb22l9djd4gncphs327q2
  - Log entry 67938: process ruby pid=17326 uid=447 src=121.61.6.111 args=n7piq848byrq-jz89w05ijo2u4azapb2xjw0y8fihech-4da
  - Log entry 39126: process wget pid=24343 uid=28 src=104.207.7.109 args=d3ywd977inpl9zcb6ftquau8nb7dy74s /0opzfjbwmw2x-4
  - Log entry 17608: process sshd pid=3391 uid=31 src=37.201.149.237 args=juqzkmyqj2ufir6g/7e2wswpnlfbu0ywvw42bfmiuitr6jk3
  - Log entry 48170: process nc pid=9615 uid=73 src=154.76.54.154 args=3w614qm39e3gdr8 rvq8p357l0ugcyg/ytmr4ojmc65 mel0
  - Log entry 10622: process wget pid=31407 uid=185 src=219.177.108.202 args=hmqk -u430b4-/// n3i/yj1 ixcys77o3jw-ot6u9yvx73-
  - Log entry 79354: process sshd pid=11260 uid=758 src=155.235.90.15 args=ijckiehd9rrw8f/a/5xtgr8xjjbf4 e/bgd/wx-/sk2qtn8g
  - Log entry 39745: process curl pid=25380 uid=496 src=134.157.129.212 args=e1c33zubeu-ag8dk0u/5fid549 waramfm4nht5xdwjrlown
  - Log entry 29461: process curl pid=21641 uid=185 src=78.63.46.150 args=jybj9omzuiicqpp3gj7c5v70dg8yuswen1jhuhjv/cdk3kj0
  - Log entry 68255: process socat pid=31460 uid=590 src=33.22.157.191 args=q0ai2e67gdp8kxbzqgljigeofhuj6re2bylmfltkd9w/pvn-
  - Log entry 41449: process nc pid=27513 uid=125 src=109.62.169.142 args=not6cty62ax1tsqge77j20c9lj6t87h17fi2te 4endfqjfs
  - Log entry 27315: process curl pid=20940 uid=191 src=77.68.219.227 args=j9ztfehezdpn1k9dpl5ave25w2ptli4 2ofi9ty8tnwreh2e
  - Log entry 41325: process socat pid=13320 uid=175 src=185.96.0.2 args=c67g5h90quofsbbc074nzrf/j/drx6zr466uzj9bohruveew
  - Log entry 35655: process nc pid=4133 uid=644 src=195.55.252.174 args=2u6zhxehhjf8ntgb7r-uomkpouuq4u8wlowqp4lgsi3mi1wg
  - Log entry 19214: process python3 pid=28467 uid=964 src=114.203.103.206 args=vbp8bm2e4vu7k-9049dh-zb7e4o8/go5a0kp4wcj1hp583jy
  - Log entry 82582: process python3 pid=8047 uid=293 src=15.107.166.33 args=0cnagqjbstf0nmued8b6qikv-y- -wbifgbbvzcgwz1ntu04
  - Log entry 36940: process ruby pid=9218 uid=810 src=72.147.101.15 args=bojnpc5uwgs/grbbhvvlnrsu-av2v8is vc/mtwj-pftx6h 
  - Log entry 18901: process socat pid=1983 uid=8 src=189.24.181.221 args=goaqzbpms/hszdy1kz4ogwplrvmj67rs1-p8 xyc4p4y g0/
  - Log entry 68792: process curl pid=29919 uid=598 src=58.171.53.178 args=wc0us7nrh01bkbq f-2gl9fngdx4s4933twf1z1zpnpnqjzn
  - Log entry 86478: process ruby pid=20928 uid=118 src=42.244.50.231 args=x r4jh77nvl7pnia5/b14gg0t92m2 tlo3uzwuxatys5d8u0
  - Log entry 30796: process python3 pid=4710 uid=362 src=3.228.4.167 args=r93yfnfrjyuzez9y/pmp06xnose2hxn4e7e0cjari-dxrj42
  - Log entry 98421: process bash pid=23639 uid=815 src=140.22.149.168 args=8vupganetxh0mlb66/s k2/tfr279yx4n  dz3quj0i17rdc
  - Log entry 70971: process socat pid=7484 uid=608 src=93.58.94.60 args=t5nh-a1orwg8/q-tzah9cotb2mx b0l3fsxgn0e-cemc/xk6
  - Log entry 32414: process nc pid=11056 uid=100 src=205.140.129.232 args=42za9cxgqnjnacmhcttvsvtib0a6p2ja5ac37poq  c0w2j7
  - Log entry 46230: process sshd pid=13813 uid=829 src=218.191.55.47 args=5b/dbdrmqg80qg/tyehonvvhhvkys0iox/wc3evo46so1l70
  - Log entry 96987: process nc pid=1256 uid=507 src=131.106.70.38 args=g6fg9xb3k4rfpattdj5ejo3ix75fm49igaamnraltjt3q /z
  - Log entry 61677: process curl pid=17453 uid=792 src=91.174.160.96 args=gy7xuj45i0n88jampp9xcfdlm 9pr1yc4p9pf04lc9ar z-l
  - Log entry 75252: process wget pid=20929 uid=804 src=180.195.138.13 args=fvc7qyapu9awpp-anuyzd086ni5 b28hg7pbxn/ur/z7dp o
  - Log entry 30961: process nc pid=6506 uid=494 src=107.219.139.247 args=ozlfwx1r9ulney7nv4y-k25bupzmyd5klk2dzxcu3ghdg7sp
  - Log entry 59912: process perl pid=25857 uid=716 src=149.143.111.211 args=dksf3c8ub9kdzid5tfkvi5xisz/tzz3rutjm 1i8bd/q9utw
  - Log entry 37241: process curl pid=24387 uid=157 src=171.143.70.138 args=g6k1sf2qr9z7loa98zbf06d4pbrwcouafvw9lzer49qpe3i7
  - Log entry 92529: process bash pid=12648 uid=305 src=125.26.158.108 args=ua5y75ptrmog-hmtdc39vh7 5fv4dj90hsu 6/2nc6nbrorc
  - Log entry 47390: process socat pid=27088 uid=462 src=189.101.57.222 args=/p5pdmcx3pn33u-1wi6yb7sjurx8rq5x31d64be8u8wnub3q
  - Log entry 74946: process nc pid=14345 uid=501 src=131.58.219.115 args=qxxiamvljaeco 3d21wprsyd-3ot7jajz8g sj5e2w9c5bg7
  - Log entry 30379: process socat pid=12830 uid=943 src=164.60.111.172 args=zoejvlpd6qb 4nweqxlcusa9zr 3hqb27idfztm7ru9rh7dk
  - Log entry 64867: process perl pid=6272 uid=935 src=52.253.202.109 args=ctadq1/k2yk9ij4hzk7dk6su-ch6/wucml2usc06gj/j8hlb
  - Log entry 35318: process sshd pid=8513 uid=15 src=43.225.253.108 args=wso4w zqsz85uiq6vdjkej99q1t8e-eq1cfegvvwlkcrjntj
  - Log entry 52137: process ruby pid=19150 uid=959 src=41.30.116.145 args=kidbw46g1i3/yysvueka42x5n5f hw1-5gsw p g-g0fiip-
  - Log entry 10083: process sshd pid=31723 uid=13 src=81.80.47.60 args=51a5l2v0kqi5d-7-wg55yxil7gfwta68-vwe4z2e5-/rf1xr
  - Log entry 71547: process python3 pid=21143 uid=581 src=168.163.7.52 args=qpdxjbomq3hs4m65kmfpwpbv/nho6g1k91vki9tdyze1fcv9
  - Log entry 51210: process bash pid=15515 uid=656 src=101.47.98.200 args=vm0zuavxz275ntc9f4gvti-eynvd6x-1/fn9ho3jet8b nxy
  - Log entry 55251: process wget pid=14254 uid=608 src=122.207.243.21 args=3b5sj47vnvnyaa-nt65a2uw-t/o7p2ww5zz78j5quhum4d55
  - Log entry 37177: process bash pid=30108 uid=661 src=32.223.153.156 args=s1dbzx34ceqe9iwc74ox3spqhs6nl16fhruy1-ku461x27hx
  - Log entry 51177: process ruby pid=24005 uid=13 src=106.166.172.171 args=ywm/eji 2j32/85l4frsq2lca tam-6880xbjehonbu665xy
  - Log entry 24687: process ruby pid=1983 uid=883 src=200.38.42.138 args=6rqfy4zefro/0lwm5/k2smn1j4znslvwp0v9y7iy1xlnc/ws
  - Log entry 61939: process nc pid=6837 uid=840 src=159.184.6.119 args=ormre9es-bo1rt5csgowd/w/ks0 xu7u13t80887wbkw/ipb
  - Log entry 73190: process perl pid=12290 uid=824 src=74.50.174.88 args=iv046punofz9/ 4qdy-lkrs-73vscz7m52lsgzuvirtt9s/i
  - Log entry 17344: process bash pid=21495 uid=455 src=165.15.191.77 args=jolekk6k5myod4e0np456nf-i6r9b-1kdj6vf7taq3ze/o-5
  - Log entry 22641: process sshd pid=20002 uid=237 src=51.74.95.165 args=mbvjnaxmnvr09qop8m7u2agfnwmucx60-763ms27md4c3gle
  - Log entry 15886: process curl pid=9283 uid=498 src=180.127.208.228 args=a 2k2gl5v98gcy62fzy5mwxd1h94--1blp4/ 6ds0dv1roqa
  - Log entry 69824: process nc pid=26287 uid=306 src=144.77.186.247 args=lkxvioeep3ycnqmy2qhnfviu777g/hwb/idr6lnqhwn2vdzl
  - Log entry 39208: process nc pid=29725 uid=128 src=120.174.234.93 args=jfoor7hv125r0//j92ctus4moueqtqptl4ejjwr2 byn4j76
  - Log entry 58098: process ruby pid=10814 uid=760 src=136.152.191.95 args=-j2sr5hgcipwa0-55/0g86rbzms7 071vcng64b7 13aoy5n
  - Log entry 37060: process nc pid=20895 uid=529 src=135.208.143.97 args=fv8rrc22oz1x3zymf 4y49 5srum-1m6/lv8knpklj12ckfv
  - Log entry 98194: process nc pid=24697 uid=207 src=49.188.221.235 args=1m0o9-kc t3eedisj0j321d r-x5ycmf1cn5l45vkr3mp9z6
  - Log entry 15932: process wget pid=9403 uid=281 src=127.191.159.49 args=-nl vwkf0fn5swt8783cegs39x6mm/lzu9ixe/bb5psgs4zr
  - Log entry 18897: process perl pid=6960 uid=297 src=102.0.51.102 args=k1kc7ss7/tay3b4/e9x89c08yq389sa7k85ej-bsh46vqgrn
  - Log entry 92004: process python3 pid=5647 uid=551 src=106.49.147.149 args=l4mg045796afaxc-mzy9l 2ksxnfq/efq8arnjyd2ryl42ht
  - Log entry 14106: process sshd pid=22534 uid=482 src=117.108.81.37 args=6srnrlyq ivlby8vz94kzj8v5zvqal7984gin7nr6w-otqvv
  - Log entry 77527: process python3 pid=24396 uid=736 src=180.99.75.72 args=6lt-o-5uxlhtnh4rb7nwwcyc1ox-xuukalow7eu116-5jm-i

## Supplementary Technical Detail — Section 19

Automated correlation engine identified 36 related events in the 6-hour window.
Baseline traffic on port 55991: 3 connections per hour.
Observed traffic on port 4444: 120 connections during the incident window.
Statistical anomaly score: 0.922 (threshold 0.750).
Related CVE: CVE-2026-44936 — not yet patched on 15 internal hosts.
Affected subnet: 10.8.1.0/24 — 6 hosts in scope.
EDR telemetry: 5 alerts suppressed; 3 false positives removed.
  - Log entry 20651: process bash pid=25361 uid=308 src=63.213.99.155 args=7lbktsc1cclzsyqqfiivjcfqp4d8v10p2p 5vxwwiu640lyi
  - Log entry 34845: process socat pid=27298 uid=334 src=16.152.170.25 args=v6fx9ndnyl8q8/zvku26m8qxrstd3xpem1fxsvbap4l-7wxg
  - Log entry 60866: process wget pid=7820 uid=401 src=26.14.146.137 args=ps3t2qecgnzow3hee01 -df7u-on2cwbx/3/3dylwbugl-9z
  - Log entry 95104: process sshd pid=11684 uid=632 src=151.136.99.141 args=5ih4e5kf17hktwzdrzb0296atib t/ -hzj2bx4g ey/ep36
  - Log entry 26439: process curl pid=31181 uid=217 src=179.148.169.133 args=8ivg3ia5q8yo4u694fisyk0ltgtkbggjdlma1djyq9/8 3tj
  - Log entry 39273: process wget pid=31249 uid=839 src=177.65.7.169 args=z9robr-ibuw3r7j4buyvm5xvf3e9vhbf1i57ppw2cziyitur
  - Log entry 24465: process ruby pid=3765 uid=507 src=206.241.145.21 args=skjjze5mnniblru2wgy0/i7910- b3he8-qwc9bte1wddkvq
  - Log entry 42332: process socat pid=25317 uid=93 src=28.250.205.112 args=e0fnuuqg2085pqj5oogh hglttrnmg8v6fajzahf62t6xwbt
  - Log entry 97624: process bash pid=15839 uid=14 src=20.47.241.235 args=j1uf2rw53-pxz-qj2djpqpgofnsrb1kbp372meu/uz0zmrvx
  - Log entry 34722: process perl pid=2691 uid=703 src=213.121.224.204 args=clypayytgkf/lsy1mlz1b2qe2/oj9wo381k 057yzxtn/fko
  - Log entry 64554: process nc pid=10274 uid=391 src=165.184.27.40 args=grkbp8-qiq6c9w7jynhqj2ly wp/tlr67rm090yrh7nlnyow
  - Log entry 49553: process nc pid=16573 uid=702 src=118.187.255.138 args=8k91ud2jkaq449-24fqotbtf5/f-s m8pey9ht3yx41k7fr8
  - Log entry 13293: process curl pid=23008 uid=545 src=93.238.202.36 args=3vvrfs/dfrb7xv7ruglng-413w1c8nq8ajor21usv/fid12b
  - Log entry 69191: process nc pid=7776 uid=687 src=10.154.70.37 args=6x6lwlnk -0imrr/pbd5cervndfg4737aoacumw30bis8094
  - Log entry 18370: process ruby pid=26135 uid=48 src=138.141.205.17 args=5h/zlh62-fm8beylb7 ejzo4guwghybtdnwpr9rn6n8flqxg
  - Log entry 54258: process socat pid=20057 uid=46 src=140.74.63.60 args=p2/2j95vu ts7kg1g20ucgq/xkk2dez4rqk2muredmq1/ 7 
  - Log entry 93217: process curl pid=26939 uid=87 src=135.189.199.195 args=d4njvms3lawjjv7z3oegp /oboind/u tlqtbb9c93z /l67
  - Log entry 59837: process ruby pid=4187 uid=933 src=100.229.62.243 args=w70zi9y9zi6egj-je5rsovprhrwb84zkt 12zunit57qx5hy
  - Log entry 72378: process python3 pid=18599 uid=923 src=180.156.129.17 args=3z0jgo t6qbmc3ezm43qk kia whxle40frj/hynkclo7u3z
  - Log entry 23173: process wget pid=6071 uid=600 src=132.67.20.99 args=gun88tezp2cifj bh53t 9wpdwld0psw37np sw2mb 5ibyt
  - Log entry 57715: process curl pid=12164 uid=489 src=86.231.8.60 args=xwlwpzj8jwgbv2tb3k98ax5ygp2fkcjqcdd/zl6k1p9z821g
  - Log entry 22477: process bash pid=17335 uid=581 src=77.198.149.222 args=doi -w3fn7mj6tubdz4ewm7ufg4d-qsugb/48/b7qtfooko3
  - Log entry 73464: process curl pid=22110 uid=859 src=222.111.176.3 args=hc2us7nq8awwnkx4ldsw7s240dwisrwldz0yf2an-jzmx9uv
  - Log entry 11262: process bash pid=20730 uid=46 src=89.78.211.10 args=zj-jxa 4awb7vka2lwjrl-oczcvvcqfesm o2p rcm2g6uv7
  - Log entry 13250: process python3 pid=23025 uid=391 src=78.132.143.25 args=wawr3v/0om3-izno-yr1tfuqlh-esfxny9l8itvdjxcfzqg 
  - Log entry 42901: process bash pid=3931 uid=780 src=155.226.2.64 args=084m8giq0o9jiv4s3bh6g0rw-b2e9yz civn91r4hjdrv5q2
  - Log entry 56385: process curl pid=31689 uid=29 src=167.69.163.19 args=vcul-wsms9thctxb9wa4qlb bryh d2q/itw99jd05v735qu
  - Log entry 66762: process nc pid=24577 uid=268 src=169.165.29.254 args=kq9n /msjzgthur1qc3dihw/a7pp0jd-cjjcec9l/ us1 vl
  - Log entry 55163: process nc pid=5400 uid=111 src=180.188.4.19 args=6 k340jim9cml7jx/svw hdu3pycstw8dufr-zcb76y c6n0
  - Log entry 63154: process bash pid=19873 uid=253 src=169.92.90.90 args=-89bna2m8d/mrnume656dk5f-7gcu-irlawzvgw/ z2wk-xl
  - Log entry 96501: process wget pid=2659 uid=104 src=59.92.57.165 args=2cj-n49a6qlbkoq1ks/plxqbxs5737k0wygkd/qm2-id0gks
  - Log entry 98652: process wget pid=24656 uid=905 src=45.175.159.24 args=24dymkaun iii5mr/q1p96ns9mdo1/j3-5zi5x4k1wo53ify
  - Log entry 92954: process socat pid=17947 uid=690 src=145.126.201.100 args=x8z0yv5qt9r/xcv0na4aeq  aa1 1w-3z8x8wxm/d5l0ob 6
  - Log entry 33693: process bash pid=11418 uid=655 src=103.23.89.69 args=kiwxhx5grf/3t/034mnnx0ei/9fty06ry22h-w9etmbjfde-
  - Log entry 78902: process sshd pid=18917 uid=154 src=214.126.211.245 args=l7t1w8bs-qephn9y9t4k8-kdh13y4hy2-p7 7w4eiua8glpx
  - Log entry 66602: process sshd pid=25919 uid=161 src=217.14.251.47 args=ff56x ol5-6dk50ito6yu1cn43mpoahwrla0w8t1vfdcmvbs
  - Log entry 67621: process nc pid=8791 uid=463 src=152.69.13.254 args=-59973z4oy9ilt7kt9bl02jh2p/o6222 u44uz2c5/tjc6p7
  - Log entry 34509: process nc pid=22985 uid=328 src=55.138.129.154 args=k3zs-xo0gnjn7lqg98dyoiuy/ya 8x7v8mwe0xtf5wefumku
  - Log entry 17394: process bash pid=21959 uid=446 src=45.24.224.230 args=ma6hi94pk/ehbqg9agh jvf640e4e7hbx-io1ef7sh 5yn l
  - Log entry 64894: process ruby pid=13042 uid=537 src=187.199.30.62 args=28yj9uxncf6qbmxk3ky6wbpcgtytvl-v8jo2/9ikxt7ge-yv
  - Log entry 93313: process bash pid=14715 uid=34 src=109.195.244.189 args=kgovwk8drs5bf-00xf77 k-7ox merw4-bdgmbztq8705mi3
  - Log entry 41070: process curl pid=18287 uid=927 src=103.177.72.62 args=cgx0102zhpwb9y-moa2f3hxrxgj7cuswxkw/aa2t06y hy6h
  - Log entry 84693: process bash pid=14461 uid=416 src=200.202.198.156 args=z6sa-r3//l4wq37f/yfgiahwmct7c9k76l-0b18zvyh17ivp
  - Log entry 42656: process nc pid=18920 uid=766 src=162.82.103.152 args=1y6 fe4yd7q0hbbv-n70gxbepp0/s4pi y4ni00q3laob055
  - Log entry 54672: process socat pid=19900 uid=432 src=207.189.55.21 args= bj0rfpp j fz51ahp5ytosa/mcaxmo2hptqlasx0v8het48
  - Log entry 59662: process perl pid=18512 uid=48 src=40.85.131.219 args=7q51--1- kse ssmbxt7j9xs9pvi iksr1-1tesgapkg v68
  - Log entry 40964: process curl pid=27481 uid=539 src=36.224.222.128 args=7t785o4w kq-jparxwh9kcue8tv/bbdnu0d2c/6av8omdp8r
  - Log entry 39387: process bash pid=7893 uid=136 src=133.178.171.164 args=lye kj/f37dm84xpcf2sr8zoofo1/u72ztxtk1 1/vrs8n8s
  - Log entry 44121: process sshd pid=18848 uid=862 src=148.61.223.12 args=j60s1xsnnardg3bp22m0blsh-gwsqc89nsa7h156f4lrprdr
  - Log entry 27362: process ruby pid=17546 uid=865 src=85.137.213.160 args=toiv337hlax2gc50cbxubk56oge2/wp27e6vpmibwrivhs5/
  - Log entry 65364: process socat pid=27186 uid=650 src=22.127.57.57 args=m9con8nr1v7phf7c4vusfckca1u8-6/v6a-16dj6a10pfpws
  - Log entry 63929: process socat pid=28250 uid=477 src=102.241.208.146 args=n50/f-z4lco93ffljm5ror1zum1mw/it3p5aln1/y/x12r4/
  - Log entry 44995: process bash pid=8419 uid=182 src=71.102.73.218 args=4j/hb9x wetyhwa2fh-ad3sq6vwmzbx7y4mt/1pcf4uufnb6
  - Log entry 38867: process ruby pid=3674 uid=813 src=134.187.144.238 args=70z2hacnb00sguhafv-p0kf1 j7wutnco2y2mtryvq3fvl f
  - Log entry 39775: process curl pid=28192 uid=132 src=104.66.142.26 args=cgdtxldkhf 76384l42s2zvngjm-23gv941zob698puih-qr
  - Log entry 79265: process sshd pid=30040 uid=152 src=92.152.220.213 args=g9gzrnbko54h4jeu5xaacv8/t/t7as5 2c2xbudfoq 2- k1
  - Log entry 50086: process curl pid=16311 uid=684 src=110.182.90.195 args=nrmzni2t64 k/gwk19qcw9c45u1tllb-5ch4x-ht//qnxf/b
  - Log entry 42031: process bash pid=27424 uid=808 src=203.138.17.40 args=tqgzd3x8xtt3k1f7t qfd2r0l9jhfyssihujzhgpol97m6t6
  - Log entry 78890: process ruby pid=14265 uid=37 src=53.214.120.7 args=0safdjsk0571quxomrkv9b1qzgmrhf5c0dzc3q6c4vqnwrxd
  - Log entry 82771: process wget pid=12353 uid=552 src=1.173.51.72 args=/7ouwba-yobojlsjmcu i/4x50f0f3i4cwc415l3j5ky c h

## Supplementary Technical Detail — Section 20

Automated correlation engine identified 6 related events in the 6-hour window.
Baseline traffic on port 19421: 3 connections per hour.
Observed traffic on port 4444: 136 connections during the incident window.
Statistical anomaly score: 0.932 (threshold 0.750).
Related CVE: CVE-2026-22088 — not yet patched on 3 internal hosts.
Affected subnet: 10.1.5.0/24 — 6 hosts in scope.
EDR telemetry: 5 alerts suppressed; 2 false positives removed.
  - Log entry 35175: process curl pid=29433 uid=457 src=96.107.109.179 args=7 hk9tnst1se1  x1-3mi7m65tg 4hemh302ac7qm36 ow6g
  - Log entry 43163: process bash pid=11318 uid=717 src=73.142.10.79 args=s1vqtod6o3p3mgozdn 4gt5p6s-sixtx31xepl-2pbu-j7uz
  - Log entry 98138: process nc pid=29394 uid=282 src=79.225.226.28 args=snh5h7i307rewdnts/t6m7f y1ke1/qv2h0h9dh-olrt7kmr
  - Log entry 18817: process nc pid=1820 uid=173 src=76.70.161.141 args=9gh4-vvn n/drc2ywhvmegs/1j h3wv8/9x0- b64-ugbhc 
  - Log entry 75364: process nc pid=8889 uid=356 src=128.244.6.158 args=rgomu3v0i-i2bov1byt2g1 zvw3e1hn hficbe0sgy-w28rm
  - Log entry 24085: process perl pid=12364 uid=68 src=59.42.18.115 args=t-xi/0/o-gn4v4q3j9mb24ogf6fg768760su72iqnrf7t ej
  - Log entry 67887: process ruby pid=16941 uid=584 src=160.1.161.218 args=afyiya tz3rfw g7uxj46ueuz96-ce58a4u6beb3d8/61mb 
  - Log entry 58804: process socat pid=22840 uid=919 src=22.163.118.38 args=9bk5aaql1mvi1ri69z-gq1nuloztgjyo-8cv lnkgwr4snzr
  - Log entry 75560: process bash pid=3366 uid=192 src=184.247.235.202 args=3660o8l1a7aw hmrzg n 68x5 pcr8xi6460/jxief47ioal
  - Log entry 34639: process python3 pid=23678 uid=704 src=25.164.207.212 args=77e46 uwc-7uo47mcc1kp8w6wy6yoop69w-x1ogvyc6305a 
  - Log entry 88229: process nc pid=25678 uid=863 src=142.161.200.108 args=mi51qmgnzwjr4e c7eizd49kl7n5ldrq/k mj5kqkg031wwm
  - Log entry 34259: process socat pid=2769 uid=225 src=43.15.159.170 args=tpeewed91rs 4 6x51z5 v08a--pn2us7r9kg1gammh1/cdn
  - Log entry 71613: process python3 pid=8683 uid=253 src=110.60.80.211 args=cnz-bd6yqhj30iddx/3xpvcofubqv9j6zamj32aews3re859
  - Log entry 74719: process sshd pid=2760 uid=178 src=60.132.224.17 args=83eu-3hqpchxiegawl3bjc3t-ihac870t-npcsx4zo3vvjl6
  - Log entry 91253: process sshd pid=4611 uid=163 src=82.229.95.237 args=b-kcbdfhzsr09aw7/3ukgzy3yvfxb928ty9/fmycaugksloc
  - Log entry 20976: process socat pid=7902 uid=946 src=100.197.84.48 args=hfr793y/yfigf1q-x8208aiqe055o2pog2i8z-m5 o76jy50
  - Log entry 97114: process socat pid=25325 uid=24 src=92.255.17.101 args=0xxjp/ejbj4r12k2o-00-ywml7ut3ga5nl9hqhtd/tb0a781
  - Log entry 86229: process bash pid=22563 uid=769 src=108.93.24.130 args=4q589gfo1d5jwbpal38czu8tqa60gdjohoe4vlmq3lqk99a4
  - Log entry 12242: process curl pid=26763 uid=324 src=187.218.221.163 args=ogthpak9rp9j0apk2p9yrn-yd795wrf7-k7e/k8ym-kha0/z
  - Log entry 67786: process socat pid=14128 uid=657 src=174.114.80.91 args=k jdt8-/y8uz8o0h6i09lp 254bopemxvqozyg qdgzg hl9
  - Log entry 53808: process sshd pid=17352 uid=604 src=34.149.199.55 args=vec2/q 4v31xq7bv-aydwm/-9 szwo/5 qiitit78tossyrn
  - Log entry 51641: process nc pid=16199 uid=434 src=48.235.221.35 args=yj946b9ctmiv6ak6es3/j5mjd7p8dz0gv0qo/vbqv7iw65as
  - Log entry 60733: process curl pid=24109 uid=103 src=173.91.240.58 args=h5gel0ko86kzok6ebdfe9qzu43x9--1klbc4lgat6zounz5r
  - Log entry 42856: process bash pid=1443 uid=18 src=131.125.20.115 args=3rm bpw4nwit2yhz6hmkjw9f2dt9xnjm3lnpwtuahls6jdg6
  - Log entry 46182: process wget pid=19995 uid=900 src=116.107.41.101 args=7ron5mvntcvo3bvnycpk7n x5303x0g52w/z2ojphy9ryp4e
  - Log entry 26078: process socat pid=9337 uid=533 src=17.80.189.237 args=hy061sv2ksixdj1ecuc8fmxlddheyafbde9f4im9nbf4unk2
  - Log entry 69261: process perl pid=16362 uid=35 src=173.94.93.186 args=gx4o ffx71y-pdvy1/zhu2iv78 7ka-j810iif0-n-70kzx9
  - Log entry 91932: process socat pid=9896 uid=190 src=171.238.148.17 args=f8cqnpkfkuuh-2v18cwphhx9w-ig/wgxt58shy-ys/gofnsl
  - Log entry 59029: process bash pid=19205 uid=125 src=17.44.229.247 args=vp79w8t0fehxryojd-kkjua15usc9oi qh41chjys/ewt8h6
  - Log entry 51910: process socat pid=19429 uid=938 src=116.216.203.61 args=4lza3ai-z gqe0tasv4ov8ds4d 28ec7znunx4b5g/ltkgm4
  - Log entry 53789: process wget pid=29954 uid=214 src=128.159.206.254 args=fiz280ymla9cd-sx0v13lca-4lo6e6zc18/r42luvpm/l17c
  - Log entry 63407: process socat pid=14561 uid=739 src=114.33.178.233 args=upvz1ncwr/-b9s1c1r2gpl/eulfy6cwfxuveautf2vlhjl4l
  - Log entry 76142: process curl pid=19299 uid=470 src=122.206.85.173 args=6d0dluzwqlmlk5be1fvwr-c078i5kt-i6zy4v6pzeuk3c3k1
  - Log entry 19599: process perl pid=26097 uid=741 src=178.145.224.193 args=m11pz3fv9e3g/gf gpywdkagp/zzklra7dwocdexfak/6s70
  - Log entry 82976: process bash pid=6850 uid=308 src=8.255.64.191 args=aasg7oqrur7tr5xsox224ai59s53iebj88j 8n0f9lfc6sx1
  - Log entry 57904: process wget pid=18185 uid=3 src=46.102.107.96 args=emih0j fdmx9v8vd5x36vu9yyfb/s8tr-hybczqt2fozgz48
  - Log entry 93485: process ruby pid=13485 uid=64 src=99.112.107.53 args=-kzknfri1wsk9bskwsnkm2lejnto22d3sprktcf7y2130ji5
  - Log entry 78525: process ruby pid=14210 uid=664 src=161.86.66.32 args=hftiv9yrb-kvt2ehkdqsb80lbrjeio8qokey57pj7h8udw09
  - Log entry 48060: process python3 pid=9286 uid=105 src=51.244.89.181 args=kv v61j-ixu75jyx8hevi-1bhznyxbgvff2/tstbwujwy1b0
  - Log entry 69749: process bash pid=3958 uid=839 src=106.235.89.81 args=1fyal-rwk4nfk38lsknf0epmd7r0vfn08jlyfep1g6zo2hpd
  - Log entry 46756: process curl pid=11390 uid=983 src=83.197.40.12 args=7uccm3fzb8i/n0pcnmxssbwsue9gg95kaiieg-qkrfip77sm
  - Log entry 55433: process perl pid=25549 uid=342 src=127.208.107.247 args=qncuyn4ajb5/i0tdqg tz5  x80j23- 20/mgcikm03rt/f2
  - Log entry 70070: process socat pid=24264 uid=818 src=38.30.229.196 args=jh7l7wmupxi/p-lfmkjwy7octsbhj62ps-0gon0mhbrg1bec
  - Log entry 47433: process bash pid=27631 uid=906 src=125.210.23.182 args=xt-bsb61au5u2i33xmfcj3ckz66gm pxuf 1aw/aq5g-kiza
  - Log entry 92499: process wget pid=13391 uid=566 src=47.60.174.21 args=-mu9cn//s 9oj90p/su/s3y7p irl7p23d/gpc7kc5wxgskf
  - Log entry 93159: process bash pid=31598 uid=677 src=43.181.152.77 args=7/ix8c67c1zw1nye-c37yx1hwj/-1noapc32q6zwcfbgmpei
  - Log entry 30538: process sshd pid=18870 uid=221 src=164.186.158.49 args=lg7aebwqx23fu8mxplo88d9psjpm 9k-y wxumzbrbbo-p6v
  - Log entry 78748: process socat pid=1016 uid=356 src=178.204.165.73 args=jj3v27ksd2mib04ruu-w e 221 scvxi0knr1xe1ah9a 38i
  - Log entry 52910: process nc pid=2531 uid=124 src=142.221.203.145 args=dg4dv/kkcol-bm8filcd7lnezi-gng9lkvfh2vz wf51zg j
  - Log entry 48604: process curl pid=2230 uid=122 src=209.47.77.1 args=1dxz4gmvo2zdwmih895z3-/tcjm2tktnz9n/99zymdr4gyz6
  - Log entry 52771: process python3 pid=26794 uid=474 src=109.251.24.66 args=h7c7yuo3488mwnsthn6xvps15w9oeyw3uivxbc hgi-2b9m-
  - Log entry 80291: process curl pid=2980 uid=548 src=154.16.184.5 args=c4tg1wlo/3fx285585o9twb1/zalus--q7runttufypq589 
  - Log entry 47918: process curl pid=1374 uid=609 src=84.238.255.143 args=6xwi87lqoh/tjke-yr6 y92xvxd /0aqm7c9p21pwv6nyk/w
  - Log entry 83362: process curl pid=16186 uid=94 src=132.114.50.192 args=7vfr3-rb7i3ad8ye i89wyxx8-n/xf1v/rbwtdpbnpw03zp7
  - Log entry 87407: process socat pid=12764 uid=135 src=41.45.75.163 args=3pnlrwnyi58p-/upt4u98/8wnu5auxi-p74arhf/m52kp/fj
  - Log entry 11183: process bash pid=11022 uid=169 src=94.232.103.218 args=k3i9r4tabl7bv1xmcqr7 014e2vpydpwpz1zp61q7m107rqd
  - Log entry 65267: process nc pid=14749 uid=0 src=162.222.28.119 args=y045sz25jk-1c1tnbriid-p40uzefmt0pix11fj qntw8cr-
  - Log entry 25656: process bash pid=7035 uid=827 src=154.80.187.210 args=c-lizsqq03 1s9dgmpbts8y2kx6t0ts wyge82zwlfnapezs
  - Log entry 53130: process python3 pid=15721 uid=41 src=5.236.83.180 args=rbl07wx7rhnd-6z gyg7mg2lge8msb6vv2wtak rz571wpte
  - Log entry 89464: process socat pid=22688 uid=176 src=20.243.176.148 args=n8gv7k54 fyjtn9qqkyxhyxznp-3tqaaj holchl6k1-m w6

## Supplementary Technical Detail — Section 21

Automated correlation engine identified 41 related events in the 6-hour window.
Baseline traffic on port 19977: 2 connections per hour.
Observed traffic on port 4444: 91 connections during the incident window.
Statistical anomaly score: 0.807 (threshold 0.750).
Related CVE: CVE-2026-44453 — not yet patched on 11 internal hosts.
Affected subnet: 10.6.3.0/24 — 19 hosts in scope.
EDR telemetry: 5 alerts suppressed; 2 false positives removed.
  - Log entry 96438: process ruby pid=25402 uid=863 src=87.223.193.122 args=toun2htu bpllno59sao59prec-rx/o6yq/dk8rnbd031jzk
  - Log entry 12946: process ruby pid=29306 uid=854 src=49.221.154.25 args=lhf1a041 c7vs-1eaub9yw5z0w6nq37jt8ls308hosvnpmz6
  - Log entry 81365: process bash pid=23240 uid=107 src=58.152.210.44 args=4ku9ms89tvo62x4dbe3ux1l9un2u s6b2v5m41d-r0l46p7d
  - Log entry 43968: process curl pid=23274 uid=478 src=93.6.170.47 args=nz-ebcg249sjt75i0x4j/m868v4h2n1nski7uomey-k2wa9e
  - Log entry 56750: process ruby pid=25704 uid=149 src=109.22.99.232 args=5 50j1zvt /bv70iwn8fn90/xinotzrd3d5 0-ztwsgxwp5 
  - Log entry 32044: process nc pid=13980 uid=442 src=189.59.35.231 args=6217d6kuvca4ul5bmxcsuay/yatvvbx4eplf/x/6tq-4/8dj
  - Log entry 70477: process nc pid=3395 uid=971 src=187.210.65.66 args=vnrax-ka9n844ipnt7v19dy/qplw9ytw u2mt49u4nan5ha 
  - Log entry 71452: process socat pid=16588 uid=7 src=182.156.133.79 args=-ozqlr-a-uuki1u 2zww3zaul1c536niuv1epmg8pvagw/a-
  - Log entry 41292: process ruby pid=26327 uid=729 src=164.43.202.234 args=dkwdewig3a2j48fpfvfe65odnfe4libdns93gjgst8c/fknu
  - Log entry 23667: process sshd pid=1528 uid=282 src=138.162.211.126 args= 2v/mb nggluh3mis//a-/h 2dwrnjwmetx2j633fcor93q8
  - Log entry 29033: process sshd pid=26919 uid=241 src=117.31.159.134 args=upcpz8-/h/gpyg1vp1guljtlc8e8hx3m8vdzqjeiekwy3gk0
  - Log entry 93553: process wget pid=16118 uid=778 src=118.22.49.211 args=pa mqw zau4tc35-uk4jetw1 hh-1mwkxn-8a50wq3d76j7k
  - Log entry 46665: process wget pid=14083 uid=941 src=198.106.167.105 args=8qpkg-ufgqfifzpa8bhdrajms2qdye06ep8tzf4jo35ja8e5
  - Log entry 33100: process perl pid=8548 uid=885 src=133.53.202.220 args=0kkg0b6mr273hw 3k5cxxvds7ttyavhwogyuuykv97p3b5l2
  - Log entry 39255: process ruby pid=11962 uid=575 src=189.76.91.173 args=8rrc5j0-f-87l/5k5e16-o-hpdxarxb5zqi4bb8r68d-ouie
  - Log entry 96758: process wget pid=3830 uid=461 src=78.240.224.78 args=5y8hle0rilni9nqgq240h0j u69sfo2o8ngu2qpy230stuug
  - Log entry 98653: process wget pid=28711 uid=627 src=191.0.159.128 args=5bl7 0wvnqqvu9azxdbdzd0ov4bhat9redph29 yuuhe2v4k
  - Log entry 43742: process curl pid=23941 uid=707 src=157.178.231.130 args=vgcvx5s3zfnplzvzr1flmm-bykx/4 aoenn8/ikb21hpk2y-
  - Log entry 34253: process sshd pid=28716 uid=913 src=24.249.10.134 args=8nhe8qy--1qq91ips6ezznn/hlf5jg1moh1v01 def ox4rt
  - Log entry 31478: process wget pid=6620 uid=885 src=161.63.191.168 args= d7njm692d677qzoiemm0k4z4r/ddthtc5n3y0rl8gtz1w40
  - Log entry 50596: process python3 pid=19969 uid=2 src=70.210.124.208 args=uvfxm23c6su-j506m9a8eemeg-i74ers87bbl63l/8rayfhc
  - Log entry 95426: process nc pid=15603 uid=451 src=73.245.94.157 args=wp/ousg0qp8e9f72539er5la75f3u6cu7-3zg0md1ybqzoh-
  - Log entry 63125: process socat pid=19058 uid=910 src=113.124.125.153 args=kesmopc1c-fwt2rhlx8u7kl/s-2b/7g44lg1 9iimyg/rwzq
  - Log entry 11751: process ruby pid=9358 uid=964 src=33.78.250.168 args=hr h8i3meqi9v009ybh/dinrmp6vy0e11n/y/l f3fh61l--
  - Log entry 85884: process wget pid=17634 uid=312 src=47.145.252.38 args=b3c2-55zzdi0u0dofvyxr382gg98n/j0kx7mec6jfgd5 /y8
  - Log entry 60961: process nc pid=16981 uid=60 src=177.45.90.91 args=1ma/3qpydgn8dx7dbt2754 os3ryzfersukf2pon489miczg
  - Log entry 17721: process bash pid=6996 uid=712 src=215.138.83.139 args=w016 5l5tnsherwqwd7kk81/-jejnyrwptl66pavqzzstiok
  - Log entry 36095: process python3 pid=8613 uid=245 src=148.72.91.38 args=xw4w08vgd4n7p8/o6n  9zzatuq3sqalziwa9p7oizcrggh6
  - Log entry 47829: process perl pid=8110 uid=493 src=218.196.52.115 args=rd9480x5n0g1a736ht umvkan-nafm1b-k0848auo ztjsp8
  - Log entry 79220: process curl pid=31240 uid=728 src=217.50.155.215 args=tv2k1j 30z9 eaj1e3hrsr9m9db3jeoghpoxac3rd0k3t4yf
  - Log entry 91907: process bash pid=21230 uid=318 src=176.164.81.212 args=4pyhfxvohwzbei-46i6y8e7 uc3egfvxb37t-iusjhh6vt03
  - Log entry 86582: process sshd pid=6299 uid=323 src=170.84.200.33 args=s9l 3 9zac-b wisom fo0kd62e-98se13g8l2ikdj-6/lft
  - Log entry 17261: process bash pid=22135 uid=333 src=192.152.135.22 args=ogb64rmu/zjjgc86-405y6gmuo-ocz3llt1/ntszjdvopl9b
  - Log entry 70623: process nc pid=5398 uid=452 src=2.158.187.232 args=srtyk0vt c-ul6622yg4sdh5pb7b3tpg0l9wc1gplph1a -r
  - Log entry 42023: process nc pid=13923 uid=68 src=105.136.241.165 args=9fx/itp70szbezqfrhzg73i-cglok3e/i635/nqqquh/g6-s
  - Log entry 70555: process ruby pid=12192 uid=159 src=113.164.85.52 args=0sm7qjm8num/ yx1nul0qhbxebrzgv3qyrfcc6hbz5vfhqq4
  - Log entry 58965: process bash pid=29301 uid=902 src=9.158.114.34 args=qtj-imeku3run 9rt-2n36ty7i/3h86jay vnh3851qgova8
  - Log entry 11178: process sshd pid=3092 uid=249 src=42.47.44.43 args=bv38u1lg2niiowv879--pmu3nd9vyp6odh6hi26b-/9mf4wc
  - Log entry 17557: process sshd pid=12597 uid=421 src=46.37.125.28 args=d83b2r1k03a4sfulg95kl9tbl0j/otz76-nikum5hllpj6of
  - Log entry 24959: process nc pid=15225 uid=279 src=172.182.78.216 args=5n3sru4kiwvmio07r9ow 26p z1ijttvgwervco9dv51w5zg
  - Log entry 39021: process sshd pid=14374 uid=394 src=89.25.171.3 args=f74w/zdzvet1syt3j6oh8x- efkjpphr1lv1d5kpt0y7afus
  - Log entry 72562: process curl pid=4324 uid=77 src=212.164.251.140 args=-pc9pwv0ypoisdz7im5aoxji4dlz8yuxh4ap13ybb61owqto
  - Log entry 54942: process python3 pid=2841 uid=593 src=154.17.181.159 args=fza8jwdpp7dwg/wrx87u390ddyfqazm1y-o0y9t51t5c7z/a
  - Log entry 63999: process perl pid=13755 uid=918 src=148.168.13.95 args=f7y616r3hwre-lio9 g7a togb3efm5l85 ao/3w7f68knjl
  - Log entry 95198: process nc pid=29937 uid=333 src=200.146.213.20 args=g3/33a9ls25-ffmz9rw4frg0n2i67 1c34gw/e/ze3l01-7b
  - Log entry 24646: process ruby pid=19635 uid=179 src=20.50.248.48 args=hjdo/4/fa5wzazyf4un4x24qbw7ro8fjvvmia7hgg-i-68lp
  - Log entry 62935: process wget pid=27181 uid=276 src=19.20.208.192 args=4f8kauip-ry6r4g9r7ijk2twwg02p yj2lqu eekw/d62yx9
  - Log entry 83676: process ruby pid=3976 uid=566 src=183.165.187.118 args=dyr1h8paqrb cafj9qqezd91135o11h/l46-htxgm-awt88l
  - Log entry 21964: process perl pid=5649 uid=271 src=8.140.32.203 args=3njeg2nxh9cepe35wdm i36ri/inm8uu97nvfclpwmbtn1a5
  - Log entry 82767: process bash pid=7020 uid=571 src=42.85.214.63 args=jv/fear17g3ja4tyn8yki8-f6nc9hn2-oypcg/ mmqxu8r20
  - Log entry 46569: process ruby pid=26468 uid=630 src=160.125.213.126 args=29rjxs546h72qrv/pkjtwmhu0rrw5xnea/p/xuhe7mn517m6
  - Log entry 34906: process bash pid=21620 uid=924 src=33.42.172.19 args=lahihsxg8zeiaut1rilthem0 g515mv4cw-m6w2luolwz 3z
  - Log entry 23089: process python3 pid=28696 uid=942 src=48.254.63.250 args=tirzfqw/yjvjqajuakdekygm4ocp631-r95qq5zittzv8kz 
  - Log entry 68406: process python3 pid=16417 uid=730 src=135.60.73.192 args=9w2spyf6kgmuaaykcydx5y4v-etalma/zlgkli52c-5g3962
  - Log entry 74911: process nc pid=30635 uid=164 src=164.230.58.16 args= c6/2mez1gqtm-oufyt9y07kl14y/ vs t1j-0tbq4piw-3i
  - Log entry 96934: process bash pid=13444 uid=591 src=175.240.189.77 args=-dluo2x2frav1etd4k-r015gi 9p-kl6-a3y6texhmtw0icd
  - Log entry 87599: process sshd pid=12200 uid=984 src=103.33.27.126 args=np84h71rmhykxsmita bmzjq3h54znln-04a 30y-lrf33 -
  - Log entry 51771: process socat pid=29925 uid=412 src=106.65.76.47 args=dzwl-61a9j12pq/1wu799-x/ jt -rxe1kf//a4volkm /z6
  - Log entry 70023: process socat pid=17232 uid=345 src=56.158.178.218 args=319z 8xsazk46q2dloa4k48 5p017799d2bp5mcxb84dyao9
  - Log entry 89148: process socat pid=19844 uid=472 src=186.31.215.232 args=sk3g2kb0k migqam08aj85q8701swz4v3zujiu5bb5yhu4qa

## Supplementary Technical Detail — Section 22

Automated correlation engine identified 45 related events in the 6-hour window.
Baseline traffic on port 17633: 1 connections per hour.
Observed traffic on port 4444: 150 connections during the incident window.
Statistical anomaly score: 0.823 (threshold 0.750).
Related CVE: CVE-2026-42218 — not yet patched on 19 internal hosts.
Affected subnet: 10.9.3.0/24 — 14 hosts in scope.
EDR telemetry: 2 alerts suppressed; 2 false positives removed.
  - Log entry 78786: process bash pid=6648 uid=768 src=10.200.198.135 args=i910ybq-6-j0ch5-c1r/hgjfg3 e8x50199 -p7nvmrjpe/a
  - Log entry 76118: process wget pid=27538 uid=238 src=76.241.54.184 args=mg7f441tkw-2yy-lstlzhufgryyw5iv6a5pejirce31/g8bi
  - Log entry 15134: process nc pid=13969 uid=70 src=145.176.118.108 args=q24h0qbb5rsukm9zy9q55pod9i5mz/hiw1qee//y/ymcjqyz
  - Log entry 69943: process sshd pid=12483 uid=896 src=118.164.130.218 args=d5052101ldh9p8iz-oj8fs6bn-m1v-ewbxc5dxy6/ 1itds1
  - Log entry 11352: process curl pid=27529 uid=65 src=149.221.253.66 args=rf8dk8mgwu6ayhnii k8b3-ylc5zoj2593e8y1e3un//u7qu
  - Log entry 91476: process curl pid=12926 uid=789 src=93.11.183.141 args=z63i3m5xnz793oe1sou-cxdg74-/2f/wtm8mkb7vf9cnk2n 
  - Log entry 28293: process sshd pid=18252 uid=254 src=221.22.23.190 args=rnpfwiffw3tej73mwa52tdc0/v6ghrp248fjad68548owyj0
  - Log entry 57176: process curl pid=27142 uid=580 src=37.22.51.129 args=cjeisxdpo6x2fh2dxkqebmndff-j0radgjzq-xnw66sk8mp1
  - Log entry 92832: process sshd pid=30553 uid=257 src=117.254.20.117 args=9mkjzh-k0ldhk1twgniyeg-8tf6g2bo044x8i  6zt4lq402
  - Log entry 96420: process ruby pid=26370 uid=719 src=85.139.190.94 args=nw9-3c2ffqojpr 8kcq57j9 2xcbeo/59s9sc4l5o poou2d
  - Log entry 45863: process curl pid=2980 uid=762 src=56.75.5.35 args=hzm771nitr-6twvipic15ax-2eu8xiwfvai7y2eypnckck b
  - Log entry 34029: process sshd pid=21985 uid=837 src=213.52.127.217 args=68qj9ensuvvwal5l0sex2yl5oy- 8n8kg7cs/e11-hwhot0t
  - Log entry 21944: process python3 pid=5882 uid=408 src=11.130.126.128 args=6hcppibrwfs9igkvuaqj1a6ppjk a2idz2p8ajvx92k4/-zo
  - Log entry 26762: process sshd pid=22068 uid=144 src=203.253.241.47 args=657ecej5qp50 lmtay6-0yjj5wfo9piy0tc-pms8ui9qh85 
  - Log entry 13973: process ruby pid=25929 uid=1000 src=157.152.220.74 args=xepc98/ipsx-1 bzquqadxh5rotjmwlfi95xpwx8ftocjqyz
  - Log entry 64175: process ruby pid=28950 uid=993 src=144.128.116.27 args=/-hkklt8j24kke-p-s/hb/e o10dhyx5htz4gw-ac9gmp1sn
  - Log entry 12370: process curl pid=7203 uid=459 src=170.174.108.12 args=1hkfa8r81j8nr6gy1a5awio6a47jv3k0ruxestgjxg8gos2g
  - Log entry 46018: process sshd pid=22173 uid=42 src=25.8.105.91 args=u9-ofh 1c4smpnil9/76-xs3l 05/mcp 5lc5cz6p l7r9sh
  - Log entry 76907: process bash pid=24591 uid=198 src=106.121.86.189 args=45rt3/990m6go3jtawf6-t56grt8626glwpfjqtalv-wrc/v
  - Log entry 27423: process python3 pid=2872 uid=252 src=146.253.178.148 args=wto37gwn8fve91pvlztvn3unj1apl73fr/nmjlf1fhwyph8n
  - Log entry 92107: process wget pid=10988 uid=503 src=37.205.140.7 args=4obbmq1/bqbhfadxamxgfm-m7l4/mkod/jwnb2uvj79/l5i 
  - Log entry 83339: process socat pid=25509 uid=548 src=127.105.136.170 args=tugmz/l/vwjxz4twx0z0qdc78lin iw4/i2fkbstzxss9b11
  - Log entry 89523: process sshd pid=5628 uid=485 src=141.158.31.29 args=232bjd8dqg9lhgczbo00lj9-htn5di-ki5br45wp2rl4zkhi
  - Log entry 19456: process nc pid=23274 uid=999 src=168.87.137.52 args=8i3txzjgrfu833upi9a-ia03jq5algu67yujbt305-3okwo0
  - Log entry 29411: process ruby pid=1393 uid=440 src=137.116.149.33 args=nqw8rpr51at0x7r--nvwxl7higbc2f5351qz4xmywe-n8620
  - Log entry 36593: process bash pid=23626 uid=412 src=50.120.174.173 args=7e b9yu-06fm5uzivze8qr64onmw41u6yl60-zhj9qpjj2-b
  - Log entry 54882: process perl pid=10063 uid=13 src=195.133.29.36 args=67-jlksqq1i-qzxc/w art16dzzls-cvi5/13k3-1lqykd3t
  - Log entry 77236: process curl pid=10222 uid=1000 src=158.45.158.115 args=1q/ppyn09cl5vtutwmfrj36vqby4ea-ibbtsf6r0oz0e0ur4
  - Log entry 17926: process bash pid=22313 uid=228 src=44.109.1.48 args=dw/ceog/oj0204bpc770pjrbhe5javpt0gxrdwjml03 3mkn
  - Log entry 22985: process ruby pid=26281 uid=746 src=180.78.135.200 args=an vwq6hnoc-8vb-dsmr-t7c 4kk59067j0nggm/oxd3cxcu
  - Log entry 87236: process ruby pid=11322 uid=300 src=16.75.197.31 args=aa2jay75t2yc-d3bfgfbhjxqfyjeabc5o0qf65hr43mwnzae
  - Log entry 36177: process socat pid=31596 uid=352 src=88.117.237.39 args=hezvaktfw7l24-dhuzeh421irvs375yyvjyye/tnc9tk7ed5
  - Log entry 27111: process nc pid=28932 uid=113 src=216.136.123.45 args=j6if56pn/j0dl6ggdjljnqkltfx5glzm-8bckf/x7bqeu8n-
  - Log entry 71327: process curl pid=11606 uid=31 src=110.20.159.130 args=/lp 5t12 q0ybmv-u451eq5w0jem40b rio1ixsaw2q4hywv
  - Log entry 14376: process ruby pid=2582 uid=54 src=201.7.83.74 args=v/nica6lzffv80nmn4-mgvzgpbm/f wl-j-bu2i3wv9y153g
  - Log entry 62448: process wget pid=17452 uid=834 src=12.139.5.102 args=yq1g4imepo4ztdv kx0-e7un3 6jibyzrs0 bfp97j557qix
  - Log entry 78464: process sshd pid=4706 uid=933 src=125.191.153.116 args=lmkl0/ ctsijxqc83kn8szq4g4ppiq39510--g149cyg4k0b
  - Log entry 13709: process nc pid=6405 uid=197 src=97.189.209.28 args=fnu9 vz7vo9y59cyy0edgy4tm4gcym2qk/vhm7838n54ludh
  - Log entry 23037: process socat pid=26238 uid=678 src=203.172.156.244 args=662lxk 9mkg7m1/iofeoraty3mnul2z6o-g0cvycyegabiff
  - Log entry 71295: process wget pid=1809 uid=642 src=52.86.247.116 args=eo72nhf-qlzvtb8o0nm0cle9 o2bn-6c ilxbxg det9cv51
  - Log entry 88098: process socat pid=3466 uid=913 src=140.216.188.235 args=zf1/7a7s6jb8xc-1x34u1l-vjo whrgdo2ugn9frulz/ic/j
  - Log entry 37072: process ruby pid=10473 uid=461 src=132.147.101.188 args=ge5d353-6jbbz29m4vwy-k2mygl tkfhbcet ij74bxjl835
  - Log entry 29930: process sshd pid=16687 uid=317 src=2.113.238.196 args=912x3ewnx9idvep 9hiw1js axudhcnnxyzyuxsu/j68uevw
  - Log entry 69145: process bash pid=2608 uid=376 src=11.32.213.74 args=1zccjkr83gmtmlmgcx0/3s5fma1iht zks4t61hvlpmbd1hf
  - Log entry 36361: process wget pid=15823 uid=733 src=11.23.96.60 args=g mgglh3u/572t--nl32fbczu9xg905z8fwm6cicbvt-wp4q
  - Log entry 60439: process socat pid=23776 uid=229 src=156.206.107.171 args=kruu0ptap6ggp5k/ kblqi7vvq ub1/lpub-3ob/ /1h376i
  - Log entry 75643: process curl pid=6069 uid=308 src=13.55.245.220 args=5co89fpqeet8enco xpjl-jud/l-/ooxruvp3t-/rvv4ibx7
  - Log entry 83193: process perl pid=20621 uid=586 src=79.246.125.109 args=/56hsoyma443uddxcv9k 9mtaciblaj1rv8kba3br/yv1-xh
  - Log entry 56475: process ruby pid=19070 uid=297 src=94.74.76.5 args=ubbu5l7gloc85zetix--txh7nwz rx8sot0paa0c abhkipi
  - Log entry 42755: process bash pid=5022 uid=980 src=142.214.175.140 args= lb0r8i1q6aeeyvfd3621qgeacjh-e9syrsg2m75aujos0/j
  - Log entry 97647: process perl pid=13504 uid=202 src=44.229.52.101 args=vclm-1vzgy5hue- nz8cxi91a2by21ypshj elic6tobsmz7
  - Log entry 65766: process curl pid=30959 uid=256 src=9.73.199.228 args=jqhza 5j60fftuazc9swkdqj39to qo669bwrkjb/2ya0sso
  - Log entry 61573: process nc pid=28853 uid=997 src=110.169.167.249 args=gx63lz6-ndieqp962z85wtur04irhmvybvsty182 57sae43
  - Log entry 99120: process perl pid=10829 uid=247 src=183.211.169.90 args=1x5c/3snu0b4rd1gdp4/djgmnhmb07ofe0m5wb-0cun91wo3
  - Log entry 24574: process ruby pid=21115 uid=712 src=127.123.100.5 args=4fm1odl2uu7fwem4hpzbgxm3ilrglovzwkqf gp6wkzsdrsg
  - Log entry 95207: process socat pid=19697 uid=641 src=196.82.83.182 args=evba62j0sacr/-ibalgruniaaltu7a5dhpxpcbc jew-tvhk
  - Log entry 96438: process perl pid=2963 uid=677 src=15.124.189.54 args= eojxzu/2w-1v/s0095-s5408pgx5bqshr/va9y-lsuwg0 4
  - Log entry 74482: process nc pid=17720 uid=360 src=212.179.123.115 args=i2s2j08zv-9a9gn/wiep/r8he-rbc nog55xdv3dmucjw0 /
  - Log entry 55789: process sshd pid=20156 uid=914 src=214.220.18.177 args=i/whdk2p/zxvufmm9idvjv393j/w2hmee6nawjxbs1fd4hzx
  - Log entry 96000: process python3 pid=6199 uid=800 src=26.123.63.250 args=rfd b40ov78f8u3jfwutpzioah9dddxi6j9zzm1h1mmst36h

## Supplementary Technical Detail — Section 23

Automated correlation engine identified 35 related events in the 6-hour window.
Baseline traffic on port 24608: 3 connections per hour.
Observed traffic on port 4444: 190 connections during the incident window.
Statistical anomaly score: 0.811 (threshold 0.750).
Related CVE: CVE-2026-36609 — not yet patched on 20 internal hosts.
Affected subnet: 10.5.5.0/24 — 22 hosts in scope.
EDR telemetry: 5 alerts suppressed; 0 false positives removed.
  - Log entry 81421: process nc pid=1473 uid=823 src=156.118.109.151 args=3w dy kh bowi8emetz b4ijlbgyvgffzy34u-6t2s1w0yq3
  - Log entry 15643: process perl pid=2366 uid=638 src=82.149.245.249 args=vukilmu2ouo7hsnfo4cg48bz5xfk-71pbj8x4is72j7c/pcz
  - Log entry 28386: process socat pid=19179 uid=488 src=79.52.107.197 args=xok1sftyxyxbox9m2 o91tfs4kmeef9bm 0dxxl5m4eg4f b
  - Log entry 92480: process bash pid=5113 uid=117 src=122.172.116.155 args=xuglzga172hazbzcw1s62yx0s newn73leia/u1uzedp9j61
  - Log entry 50656: process socat pid=3374 uid=4 src=207.50.46.137 args=nl3k745o1/70fomgkjowb9imc7pjcjusm e5j ukm6qv37dq
  - Log entry 64547: process perl pid=12020 uid=498 src=50.131.46.124 args=9j00t4urmhsue-gnqp-o0wu069ven90ca4i6 a5rudh6n40f
  - Log entry 95418: process sshd pid=12973 uid=303 src=144.23.211.10 args=a-yvrtz9aouf6ick5m08h6gqdqful1jt810aucdt lhuozl-
  - Log entry 75375: process python3 pid=4772 uid=557 src=75.60.2.87 args=k53qjiykie29jqt8jaw8-3d1y//fzvle dh9ixr1wk1-q2q/
  - Log entry 18778: process nc pid=12790 uid=995 src=223.196.100.161 args=e-pv0rj31klsl7k-d6-k2rj 55eyl6nuf74kankq9crmox0x
  - Log entry 75480: process perl pid=28913 uid=454 src=220.179.121.44 args=84/bllqojzl9swkwupa5ppju7dv/ehw2qd-7uht63qdqnt4-
  - Log entry 76504: process wget pid=19242 uid=328 src=79.34.45.225 args=/3u43jfp96v-iw-yz1r tq1p8d muak3nvm21qexm45kbk 6
  - Log entry 17646: process nc pid=3595 uid=783 src=127.116.206.251 args=178xcj2rrmqq 4ytvvv88swrisjp5c72yttgse18j9ry4sn/
  - Log entry 82445: process sshd pid=14353 uid=856 src=147.201.236.97 args=//4dvhdtlmt/6zjgme6mfg-f0043gv3b30sxr/a2r8/1b2q2
  - Log entry 30159: process ruby pid=12519 uid=815 src=204.165.247.102 args=qix0xw4g7j2bns0zez8v9pg ms12 96mvpayz9gkahfoof-z
  - Log entry 51221: process python3 pid=2984 uid=580 src=85.135.100.76 args=l8t at8vswkjlbii4slwl hojg6g8qs783be0r6gvmwhqb6b
  - Log entry 25937: process sshd pid=17327 uid=74 src=91.134.40.27 args=0ax/8 u//rhv7sdzv4rah2zfb8jjcdpee2zropbs30h/2w4d
  - Log entry 84213: process socat pid=24666 uid=44 src=27.152.173.230 args=re1agy8uhuw1nszxhiszwlvuvqjntc -k7uejr58qsg9jkky
  - Log entry 31160: process wget pid=18259 uid=196 src=200.4.70.225 args=bl7h0vk 8tch9bgppd5tb1 jeros11rkof-x1lef/w50a/ir
  - Log entry 85541: process ruby pid=11290 uid=241 src=203.184.60.58 args=fefrnr0 ull-6cchix0rmq4q7qk5ttu7typa8i9t1b9teqx7
  - Log entry 33063: process perl pid=19023 uid=457 src=106.211.57.52 args=1 rgh9z9tc0kh4xi0jw6k-cejj6f713 igoiod37co2l6fac
  - Log entry 41151: process socat pid=19535 uid=305 src=38.226.169.237 args=bzzj0ygcj3qa edvx0-mdymlf07rx  vp3t356zitykg7jkx
  - Log entry 98482: process nc pid=13752 uid=905 src=193.171.218.51 args=pe6dle02yjjtm3lr/2al-zzdgd7hq4wm jclu9nxnla69oyf
  - Log entry 88473: process socat pid=13271 uid=443 src=188.7.9.110 args=gahs5d6vagu a0ijm7tlfxg28-3n9rg4/bbbp-rw2z3/019u
  - Log entry 22939: process curl pid=29518 uid=324 src=14.255.99.244 args=ymvh15pv9pws6dir4 r6uck07 7k5dn3 wk4jxxndcb9fhx/
  - Log entry 67964: process perl pid=11829 uid=989 src=191.191.56.143 args=x1zp4akeka1zkumr77kbii4h7056gzhknvrprprsvc10 3kz
  - Log entry 76481: process socat pid=26287 uid=414 src=192.227.89.113 args=4k2japdk0juet26kbg0h1rhempdb5zkg3o2e9sq57lokvxi 
  - Log entry 76198: process curl pid=2763 uid=759 src=105.41.55.111 args=nk18ya29/8p8-/ivggnh242mnyk26--/ kmqs-tf5lk59luh
  - Log entry 51426: process ruby pid=10214 uid=700 src=223.229.201.70 args=nb0yxb58qdxb7mnh2uu/139zsj/v3v41dype y9io7m e57j
  - Log entry 15845: process perl pid=3085 uid=203 src=100.147.93.20 args=nc6colz4jo /m-9ob0-10vl03wog-pryvm82vl-67kypd26t
  - Log entry 93279: process curl pid=13578 uid=286 src=190.63.222.52 args=3ykk2gfun6h5/o5oi2pqe5ij4wik6icvukwz0/mx8xv/k1nd
  - Log entry 75479: process bash pid=14433 uid=608 src=187.8.118.97 args=7ob2u9071pft 7kg6-o0rsj18hi7kpdavi1-x9ecwz3dtytl
  - Log entry 74588: process python3 pid=7793 uid=276 src=212.98.185.139 args=53c39ngkh0-81ieq6obk944 ulqg89g7uwrdyvl8fg3a6zht
  - Log entry 48291: process sshd pid=9250 uid=506 src=116.89.196.156 args=fbq6l774es-idcaj1friuzd4zarh7/7vbccn3uafzce0-kch
  - Log entry 73640: process python3 pid=10760 uid=197 src=90.179.173.13 args=s-c hsemun7mqba4wbjcoq4bmkns6p2dv8mv-0h6l4tpms11
  - Log entry 81374: process sshd pid=4273 uid=537 src=127.211.121.46 args=v5x35c/l81zs 6qpd2/zs6bx31wrf q5t4  zg-32qudnxz4
  - Log entry 63544: process python3 pid=26248 uid=492 src=197.177.115.101 args=pl9djwj3-tg7eoo0zmk/ zl5jkxegwoqt7qhd99twnhhv4/9
  - Log entry 82366: process curl pid=14922 uid=946 src=88.181.110.84 args=xkqfsw1ob9ajk74eu82ca/i/ouk-l/ld8tvku3moysztherh
  - Log entry 30923: process bash pid=28887 uid=209 src=217.46.117.115 args=c6xm14kyxbqebm6g6ouxpm/dylot24ss8qrt7ev64702yuj9
  - Log entry 48899: process sshd pid=25964 uid=31 src=88.29.150.229 args=eyu9r6zjyta4xf29 adnrc/oclc09itx31zhnlioxt8epxzx
  - Log entry 78182: process nc pid=20174 uid=57 src=47.230.57.89 args=jjmti2eniyv5ckk 1qep29q7q/a8url977/qpihmueil8nkv
  - Log entry 81292: process bash pid=17918 uid=905 src=131.36.171.236 args=zt7glrg77hv493/n0id08raoowqxpgfda8gsso seh2r6 nw
  - Log entry 32532: process socat pid=19868 uid=614 src=178.82.234.229 args=1s-t6nmbtsk1k-zlv/kdw545-l287/e3ykco1gv2pqwjmu8t
  - Log entry 34138: process wget pid=25006 uid=951 src=82.84.220.60 args=jq335xl9fg4arin24gxtd249rfxbfakb7li-497gtpye7h97
  - Log entry 40913: process bash pid=18081 uid=724 src=11.70.28.53 args=jh zuv80gaoc88nhlohwf5sb21ncuz8bjzk5ck/co54hmrn3
  - Log entry 42275: process ruby pid=13355 uid=127 src=74.202.69.64 args=0dx1v77 q/mj6bm8f-/w333yoldbib779qx8kpmj 7ofni/z
  - Log entry 67080: process bash pid=7359 uid=363 src=218.52.88.51 args=ivaw4hdip41534g355f-0nda7tlg1d/60ga2p8cn-mqz74o4
  - Log entry 41838: process ruby pid=17504 uid=288 src=223.98.131.33 args=j ugxh6rly0uhnmaln1zojgkc 272viu rb1h8c0kq-aja6m
  - Log entry 48323: process socat pid=20847 uid=664 src=213.216.74.184 args=2y6 7hi6n0j59l2hwfp2c0k0ktnb unqs-r y47dgnipl9qr
  - Log entry 93893: process curl pid=30393 uid=599 src=92.135.21.217 args=7cokldm47dw q-5idvvupvkq8s3-18lysm5lj/thotmy/d93
  - Log entry 45474: process sshd pid=25249 uid=829 src=41.53.45.32 args=hb1xmdyr5qv66eqvf1kn41ywi3oi0ipfex1pyvey/le7nqca
  - Log entry 63115: process sshd pid=14393 uid=750 src=176.169.219.146 args=vlk9vz5bw3c/1dx fh8t3oy5k40hxvi9a-0s9u63q-7ipqoj
  - Log entry 52488: process socat pid=1290 uid=897 src=39.83.126.77 args=yyq54dr3jv6e89b986jdr0n/ds36-9m0b8w1xb4ydqdyx666
  - Log entry 54201: process curl pid=9383 uid=862 src=23.13.161.139 args=rjl1a-nzu/aeplgy1gl2idyy/98-qkcewauojt xf03bbaag
  - Log entry 35069: process curl pid=21301 uid=252 src=189.83.35.5 args=on-t-qxgjs9jgl5jae08-9bxld3p46s5w908jae245x02 b0
  - Log entry 65393: process perl pid=20459 uid=125 src=161.135.89.176 args=s6w dwveitgb2 t4tfhz2vf4pk5z909ihltyjwa-l1jvm/8f
  - Log entry 79554: process socat pid=21034 uid=249 src=40.216.188.112 args=t9ay4ysaqqk3w/2j7ji1difk0wa2zg mmh1ewlw78z-briwl
  - Log entry 39895: process wget pid=5519 uid=699 src=193.243.151.3 args=y10z9id8/8fxd7ao3c038xqx c58v3h-u7fc -p4gekui92d
  - Log entry 91716: process wget pid=24417 uid=535 src=17.154.240.246 args=--m2w214nx2ejy22od2udf7rcuky4gidi84j6hxmdtd95we4
  - Log entry 24109: process sshd pid=14718 uid=644 src=86.123.9.196 args=tjyd8el /-f5q8ifa7a8fldvtia1a q2fb8gfs0r5aecr8zt
  - Log entry 35472: process bash pid=25666 uid=307 src=91.187.246.78 args=4amtvkj5py0n4xxo3g/p8gvobyviich-iw6cycrf2h6 mubl

## Supplementary Technical Detail — Section 24

Automated correlation engine identified 7 related events in the 6-hour window.
Baseline traffic on port 5188: 4 connections per hour.
Observed traffic on port 4444: 149 connections during the incident window.
Statistical anomaly score: 0.864 (threshold 0.750).
Related CVE: CVE-2026-32001 — not yet patched on 15 internal hosts.
Affected subnet: 10.2.4.0/24 — 3 hosts in scope.
EDR telemetry: 2 alerts suppressed; 0 false positives removed.
  - Log entry 31005: process curl pid=16422 uid=529 src=7.51.87.109 args=g5ys5fy0ijs15v29b6vysv1huav xia138ydnifbuuehax0a
  - Log entry 36715: process python3 pid=21338 uid=633 src=159.186.199.76 args=gwmhjxa-enjbkpfa7j8fkgoju- bm1dxryn5uvf059k yyjy
  - Log entry 40605: process curl pid=30009 uid=353 src=141.122.8.209 args=rrcnh0jp/grjefcdw fuet5vqx8vyqgfxeau088niiy4vd9x
  - Log entry 74320: process python3 pid=11272 uid=816 src=20.163.192.216 args=cid35w/tste/gpwdtk0lb0f65tra3r l339uz2mz9gtz1f2y
  - Log entry 71567: process sshd pid=8947 uid=605 src=124.199.127.250 args=tfe/qfwkw828wbszcitk4-e6nh320jbjj0hfqs-o mmra4ip
  - Log entry 34487: process perl pid=15434 uid=181 src=31.90.37.130 args=3olw3ttljt4/ap70or58-3p03m7q tdqix4p1hsnzw/58ngf
  - Log entry 14253: process socat pid=27650 uid=236 src=120.231.157.55 args=b7it0o7//qf7df5lduqqcbaq p3a8ihdc4vdnjupi mau4-c
  - Log entry 44910: process socat pid=28027 uid=2 src=183.21.226.102 args=cii0--ccmig/uffx91rmy-yeaspnht 8k-kb/vplz36amqzy
  - Log entry 55513: process perl pid=20087 uid=905 src=148.89.190.149 args=nslhaqs28wsca4dwbla2aouwsx-51u9u11h4i5z0cx76knnr
  - Log entry 39264: process socat pid=8711 uid=613 src=194.222.123.215 args=fz42zga wtv930h2rozk8i9tz99uueoq3t5701ae3veyoy4l
  - Log entry 67650: process ruby pid=19938 uid=527 src=152.21.210.222 args=h6and459pel3ab7x0qc450vokxt0mnc1m58f1jlhvvkh5hkm
  - Log entry 40526: process perl pid=31984 uid=118 src=196.73.18.198 args=mb4kzaz69g6a7/t5zqpdxdas0eei-d-g8grlf4n5cxrb9i06
  - Log entry 78428: process curl pid=23676 uid=165 src=87.133.212.24 args=/1sj/1p/19 p 8tivfnsz/mey6ey92d9pzoj1-llg4t7v6po
  - Log entry 38873: process sshd pid=29364 uid=449 src=131.159.78.95 args=93lvgxnt5w2dlj1og2iddnvpb5ewhpd9su5cz1jwi7am3 6q
  - Log entry 84756: process socat pid=26109 uid=354 src=7.188.214.47 args=3zgoya/8tj/krchgfpl6rw0rwizulba/b01jlshbb/0g142r
  - Log entry 14298: process sshd pid=5791 uid=550 src=20.188.136.85 args=p61-tc1m1w/ohdw21/1cffc1lvglv90fe14ecu/97nr8zg  
  - Log entry 27067: process ruby pid=14914 uid=12 src=30.255.155.116 args=h7w4cpftedt3wher7y2eytr28ol 35fn7sidp4hlhb5iu8ic
  - Log entry 67212: process python3 pid=11641 uid=16 src=52.120.141.89 args=c300ruz/njjgt/4uzfc62y2jn1q1m8jvm0x3c7njmojj978e
  - Log entry 89237: process bash pid=4160 uid=138 src=65.218.150.78 args=w6qqfbj8gjcmt3-mfkr 205hzug-nn0dx0jkqdiz2ke-bivp
  - Log entry 84615: process wget pid=13244 uid=264 src=107.114.44.42 args=uvx wwg9pfcoq-ojkt6c/tzo6ljo-a cm582a4 v6b42tq/m
  - Log entry 67809: process curl pid=19896 uid=316 src=60.160.15.169 args=spqyem 1-xo3/fsjrd ycd6 o2nrofa77d80dcnubpv076b-
  - Log entry 50900: process sshd pid=22093 uid=612 src=188.53.89.71 args=/tws9ed9xjntra38oeb5tg/u/k5 6kfk50zgkiwj uj7/7ym
  - Log entry 89634: process wget pid=31492 uid=505 src=52.108.65.2 args=ypxbug7 ln8jlxsaprqbp3cc0p4wv0szfntcg7ue6650kq5z
  - Log entry 31208: process ruby pid=12438 uid=534 src=159.205.126.167 args=r7646c0rfvtexh1e/co-j2vk53x02d60whuuzxh04sayo4u 
  - Log entry 19337: process nc pid=1311 uid=411 src=15.236.110.43 args=8kwfb1-nlug7hdfyp70oroal-z28-xktq-k-9ml7jfjcgbz1
  - Log entry 62330: process python3 pid=8065 uid=60 src=66.130.102.214 args=uoxvtx-xoe29-8hptat62xwjt-u1jc1n5r/xqpp4dtftq7zq
  - Log entry 39707: process python3 pid=19781 uid=596 src=93.213.12.65 args=eoc/xe/qcuububz1yg4 oyj8lnf2wcjewu-nwwe38hsf5hwy
  - Log entry 67582: process sshd pid=12318 uid=914 src=20.158.226.202 args=40mkggspb0f7pem0/oqozu12llw8yj6v9l8xwsg6-s7vcbrl
  - Log entry 40554: process ruby pid=10028 uid=839 src=163.59.39.227 args=ccolpxgm3bc4/xbrdn0jq/46lzd1dqrd wmd6s-15zp/mp51
  - Log entry 74488: process wget pid=11752 uid=509 src=198.175.157.124 args=bccixtddjkbtt99v8vus2e8zfatqcy7b70 qndmzyqjwa8fi
  - Log entry 27899: process perl pid=25067 uid=917 src=175.142.75.249 args=j2vleiy1 f8k6u8el0ito54ecrwtgk 12/d5zwks/tz4kyvo
  - Log entry 71529: process wget pid=4687 uid=718 src=2.254.197.96 args=6xq-z2bj3icx hclg1bd99uayititp74surms-5lujbwmqsi
  - Log entry 41087: process sshd pid=26063 uid=833 src=157.10.253.16 args=8-1df900gux/2ojdndtgtlb9mpr1ktt6d29dqc8mpvq7uqbz
  - Log entry 97522: process perl pid=10804 uid=164 src=26.209.72.174 args=lnl /jgo 9sc pvwgp6zfy6miodei89388gfpfqcdopn/ajk
  - Log entry 61207: process socat pid=15729 uid=525 src=139.143.33.231 args=6  65m-e0090numpwcux-cd6-lj58iawl59v1ug4brlt0976
  - Log entry 23862: process nc pid=27016 uid=178 src=124.85.247.183 args=d/zzyn-lyryl28o8/v1l2/2/5i1ijgnw876pg/ccemw5f99 
  - Log entry 25624: process wget pid=23412 uid=266 src=15.173.117.202 args=5o5ltm37vgettuinei/ts-2c2k7kvs1jfrdh36my19qfp21 
  - Log entry 21833: process nc pid=27793 uid=798 src=4.156.220.170 args=tuac4enineklvzw0-v255u5cez-je6h1owtu3o57o8fvfpy 
  - Log entry 88179: process wget pid=19277 uid=503 src=121.42.79.145 args=1w9ocdz5ydgijmaq0/jmhde6vscau98p47y0y t9g3d6b1kg
  - Log entry 69740: process python3 pid=18903 uid=223 src=32.50.108.172 args=3pgkd3t2097yx6u3qcn99 ntmc1qqjxtcunc9u7fgxlk- 7h
  - Log entry 43787: process perl pid=8938 uid=919 src=50.212.58.225 args=rrrn4r2vborsi /9pb7c0gen13acaieuu7vgtnnahogip934
  - Log entry 33148: process socat pid=6520 uid=92 src=147.84.202.14 args=0cxgpxmq ufb13jglr-v0tybzbfblte8taolmdem3dgofy  
  - Log entry 76408: process sshd pid=12633 uid=194 src=170.170.190.86 args=xrwmztq/6p-nay0v8ziemo9cadkg5ds e3yrb67f6dkt13zy
  - Log entry 63848: process socat pid=7196 uid=961 src=116.117.25.209 args=9s5- 5w0ej2ryk8 6fa8blyxgexcwuydy84mm1qs 8kqus/3
  - Log entry 83161: process sshd pid=25451 uid=662 src=130.122.193.117 args=c8c1zm90t5m8x/o7xq44s0i34p- 7qrx6bidgjn4g8m2zedr
  - Log entry 77027: process socat pid=13646 uid=466 src=87.111.53.145 args=k0-m pvyqtwl8c6zvqh8nnmarb a2w-kiu2irwhoub-5hh5r
  - Log entry 52095: process bash pid=23890 uid=635 src=125.102.26.113 args=8fc miorje8emh796 gu3vwgk4kpx nxgawzikbg-d1kb935
  - Log entry 57764: process perl pid=31981 uid=77 src=29.208.216.32 args=nck1g gbmhcv t3lsdu1vv3/2cq7df39ib/c47hxi9s24qvy
  - Log entry 83297: process perl pid=3718 uid=689 src=58.227.3.204 args=jlsmssasplm3d/sx6gen66v1a2lqiuzsgyd/fwm5egoeuzub
  - Log entry 69499: process bash pid=27040 uid=25 src=47.116.25.242 args=hd2jzqlv5m353sn9wr/93s- 4q06wa3x2l1nhwqau54b4xai
  - Log entry 35763: process curl pid=8165 uid=699 src=118.52.54.173 args=azm6-0l9zv2r0zrwjufzx8o 37ovx7/s-tpfjgqwhrkq6mj/
  - Log entry 43957: process ruby pid=29544 uid=736 src=109.112.9.169 args=mlwnzn-4jy6v5r4-mfikzs-e9so22uhjq7s8i0sgmch7uvmk
  - Log entry 93075: process bash pid=18178 uid=565 src=182.239.150.93 args=n 1febebwaa60xihm4uq ukarg3ap7cfuw4/fhgy7jatgq3j
  - Log entry 77032: process python3 pid=12804 uid=198 src=163.96.141.62 args=qq36xqy45cle k/1kh3-1wt4f1a58/rzncrqja80o0b4uvsz
  - Log entry 24323: process socat pid=9434 uid=556 src=220.101.45.106 args=-/jdftk7xmolarziqa0fejqjtjom31yk4rbo0/y87gbldg2e
  - Log entry 76708: process perl pid=1287 uid=690 src=126.142.14.201 args=sqp63ncnnkb/p/u0-0uj-4di2fgp6dok9r y/guwmm3xmix0
  - Log entry 42302: process nc pid=1228 uid=828 src=28.88.201.22 args=66za9s6g4sgponwznhuao/2x/mdoedg6-7oie76k52d-w2uv
  - Log entry 53612: process curl pid=18888 uid=859 src=14.205.27.246 args=-kh1/ea1f606mhow/3tj1tcvr1busi- u4scnkffuk67w5bt
  - Log entry 79987: process sshd pid=1667 uid=796 src=115.218.176.9 args=1pfb6wpapgpf4qot/4xvr3/mbn48gygzg2xqp 8xe6y63xzm
  - Log entry 42028: process perl pid=1826 uid=364 src=144.39.208.22 args=7dgctfi7dt2c1ee-39ktthi2-4v/prb0que xh-j8e7axrlt

## Supplementary Technical Detail — Section 25

Automated correlation engine identified 35 related events in the 6-hour window.
Baseline traffic on port 10613: 2 connections per hour.
Observed traffic on port 4444: 56 connections during the incident window.
Statistical anomaly score: 0.810 (threshold 0.750).
Related CVE: CVE-2026-19448 — not yet patched on 9 internal hosts.
Affected subnet: 10.2.3.0/24 — 13 hosts in scope.
EDR telemetry: 1 alerts suppressed; 1 false positives removed.
  - Log entry 45187: process socat pid=11484 uid=665 src=126.104.118.7 args=grxf27g -9b9zp3 ooilc02bu3hko68jss9yt14sifjkkkv4
  - Log entry 91528: process nc pid=26782 uid=985 src=74.124.166.63 args=nhgbaxx -smvfzd/mah/c2g8di1ehgp3rwzwxbwmrpw6tkmw
  - Log entry 43406: process socat pid=4233 uid=568 src=206.211.124.225 args=9j8x1cfrmup5n vomzigip9oaykb-zcmut-1ujxvlvcwfzm6
  - Log entry 71911: process python3 pid=23048 uid=723 src=220.19.241.115 args=h-5g1t443yh63zkv/sp 4 xod3pr3zrcnr7b8g/06 8p9ame
  - Log entry 63416: process sshd pid=11976 uid=901 src=127.81.55.212 args=3-ug2xb4rx12oov6p5agm1qrkuvrx2ux-u6hqk4bocjxya0h
  - Log entry 55486: process perl pid=4994 uid=523 src=217.162.82.47 args=/6frmyjbe0o3kgk414zwm82359n81bp3iyu0rcstji15osyx
  - Log entry 65013: process ruby pid=7731 uid=479 src=108.176.88.218 args=hfcido72u4/w2xeqawplrgf4mbwfmt fib mf/wi0clp03-t
  - Log entry 17293: process socat pid=10703 uid=963 src=181.179.70.128 args=-q9/ c/yv2w2r-xy5gpbfi7zy6yo904cjc/h6mzt/1z2y3pa
  - Log entry 87376: process wget pid=11516 uid=727 src=97.3.205.243 args=wo6i7i73843uybt16tpdwkoi563jdr-m2uwyaap1rrrnejkg
  - Log entry 22660: process ruby pid=23454 uid=555 src=48.96.7.83 args=q-y17cvhf9gsmk0rm3nouvwfaop3cv770mwa9tm4ofy5wz0j
  - Log entry 55206: process socat pid=9003 uid=326 src=7.10.202.48 args=k6bwbr7v10i90qtcm2ae336i2z xve372zel0083f23ao 9 
  - Log entry 80294: process bash pid=27012 uid=292 src=169.228.78.42 args=ek0e3nzb7789xduikmm-mu7-oyjjmi8bz5gcit1r90m84/9-
  - Log entry 65454: process sshd pid=19196 uid=623 src=93.111.129.16 args=wkb5su8cip5 p1rjayruxrp30n1/oug88xh/zq/ mmrps1yt
  - Log entry 80785: process perl pid=5233 uid=168 src=219.166.251.143 args=5-rivae5aooj49pbmcphstsberw1ejiov6u 1t4la-dy 32r
  - Log entry 91530: process nc pid=17831 uid=580 src=124.132.235.42 args=2oz/ikybgaq3e/1f3/zd125no06-9ua6md8xob7rt5mz5etf
  - Log entry 17584: process bash pid=28301 uid=392 src=66.43.101.143 args=h3hyg/ -nsuk/qx9ysnoe1q4-dypgzkzpfrbl/2jwsfjb1/g
  - Log entry 92634: process socat pid=11367 uid=950 src=161.186.18.105 args=6hugzaro2gcu0r077jrsctalzkcrth8emtopaa grwk3eag8
  - Log entry 91047: process wget pid=19596 uid=404 src=28.68.148.197 args=jaqa1ifgxurit5jd rhsvbezn84ycc325-z8rbra0d8ljoq1
  - Log entry 90958: process ruby pid=14744 uid=81 src=117.220.250.198 args=o6z90tcxnyzrxonzoik9jhrgchqm5y3737-peawfx8o15-jq
  - Log entry 66898: process wget pid=3726 uid=875 src=1.170.233.82 args=3v-xd2a5b9aewb7isa1xds85x it6-qydjprocmr cfcq451
  - Log entry 34327: process nc pid=1206 uid=418 src=53.11.187.131 args= s396tm-w35c76uvlvkyrx5g0--ukpc9h8t8nle6b74-9r4o
  - Log entry 77965: process perl pid=20893 uid=413 src=73.237.165.247 args=9s1muhm-b8m-63p7vl0cguhnpx2jfwl7nu5x5ciwp0l8mzzy
  - Log entry 52363: process bash pid=6211 uid=933 src=12.93.97.28 args=/9i-kybf zvs2-shh--nnub6ihhbn6wl4fuctvpg6t3e8ea8
  - Log entry 91669: process ruby pid=13111 uid=685 src=34.111.247.15 args=1hrdoey30i9g7g5q21ef05nf55n430i6kn43 rhpmi/1lqxi
  - Log entry 10523: process sshd pid=22874 uid=819 src=186.247.218.63 args=2ztunq/bmp5iq0cmhooqqqevf4c47s66aahp 1hknuizvx43
  - Log entry 35667: process sshd pid=1925 uid=759 src=24.2.2.229 args=fs8mc acdxdqlx9z4wo81 3e-081wa529fgrdaeg/uq00lf-
  - Log entry 16329: process sshd pid=6240 uid=941 src=45.30.238.35 args=fcyl utgoyhvxsitekyewg79pckkwntekolhes1rgwbqe0on
  - Log entry 52417: process curl pid=8172 uid=335 src=178.128.8.103 args=98 9930idli2-6oeid8z6qlsqpzztdrjk mun9k/isudc26d
  - Log entry 46630: process bash pid=2291 uid=870 src=7.41.171.205 args=rblwbcge8uyau/k1uranqj7d321di-on2zrw1ang6whw4m8o
  - Log entry 20466: process wget pid=18069 uid=514 src=178.10.41.56 args=3adxhoa1o67w vytlv49k3c1wplap4u51cd-8yi/z ngwd4e
  - Log entry 14343: process nc pid=15867 uid=318 src=182.242.91.69 args=yjog1 8 y9xf45 yfdlj 9x7ps6ni8/yk7uamewrxasniun 
  - Log entry 39018: process python3 pid=5077 uid=891 src=157.93.122.102 args=g1spc1 y0/wc1l1ottfx9ulgc8xlklnnylhwf8mvbj4dly7g
  - Log entry 18585: process wget pid=17793 uid=776 src=66.193.125.243 args=an-dxa1hlye7joil/g-a2wf0w7zavon8zju0ukc980t-v cf
  - Log entry 93778: process socat pid=24102 uid=790 src=169.85.159.222 args= xj6tirxqg19jnyfk0r5pw335rtpe88xmd8coqk4oy 83/uj
  - Log entry 25311: process ruby pid=24744 uid=750 src=212.98.69.9 args=y5eyjjgqmnewrr9eeqv59watnsg0e4rke8yjf5qf9xvoodq 
  - Log entry 17525: process sshd pid=14087 uid=451 src=219.44.0.139 args=ihphc3zxl9zk8bt1igc8orzdfgf7n r1mxf613o09w3oedwu
  - Log entry 31567: process nc pid=25713 uid=81 src=187.235.227.35 args=avxkd w2 psc4ggaxv3uewrnjnhzanlpulr0s48appfawprl
  - Log entry 11414: process bash pid=23319 uid=645 src=203.169.100.66 args=oetnfasjpdayg6sc1--/42rg3i3keloz38m3y14cduh/le4f
  - Log entry 93714: process wget pid=12929 uid=542 src=91.161.243.120 args=2ta-ivu/14jnqrhb1fwkoivmz6mxd63se3r1shpr9233zu6t
  - Log entry 41889: process ruby pid=29004 uid=873 src=180.196.204.134 args=6of8puz73cmvcazaauieomnk9rofw-viiikfe lr98t55jh3
  - Log entry 87840: process python3 pid=7352 uid=803 src=191.1.199.70 args=ea-dxbj0s/37-om0mcknvni0j8kh7br500lr31elc vk49m4
  - Log entry 37962: process sshd pid=27012 uid=498 src=132.219.161.192 args=a1x5qzuwcpfg3bp6gn gbmvyc1eoly9zl gft0ckje49/1dl
  - Log entry 21568: process socat pid=10413 uid=897 src=55.123.114.54 args=tmor3v/6lfx-o-3z3 5ubdky9gomqjgc-n22/amd5042 ada
  - Log entry 36925: process nc pid=7544 uid=599 src=135.63.25.220 args=m3j79zyjvklf//epquxykblfozkyz5zbj3jd0a2lzli3-acu
  - Log entry 84940: process perl pid=2533 uid=103 src=193.176.190.73 args=wb/ iawu624vw4qey 05ch2s bucaf6zysq800 sbi-si4yv
  - Log entry 62609: process ruby pid=31451 uid=203 src=107.160.66.125 args=kybjsqokcx1r 9 li16/aes8eaokf8236jc401p0j3yr1qq5
  - Log entry 64389: process python3 pid=31449 uid=848 src=65.146.211.96 args= yft-b7szro1m0dxt1i5 d v6x43hizzdup61xdcstwns/mg
  - Log entry 81607: process curl pid=19149 uid=892 src=200.157.26.114 args=p5fz7k2z ssa0m67ly5u3c4jxsnxdkw8onvb2zmckc-/ 7vz
  - Log entry 35607: process ruby pid=4664 uid=252 src=190.132.117.72 args=4ucxt6fjad/ytrtp--g-/8-n/2op1ejq1txbcuhnre-jtwyh
  - Log entry 69506: process socat pid=1848 uid=463 src=75.6.188.102 args=gp7gjm0-1msep7fesvzs3o1t5dat 6ma7q4jud-3jzuhu -w
  - Log entry 75620: process ruby pid=4059 uid=150 src=201.240.118.92 args=ymofvp5-crfv0dtmtwdhcfdvf zv71c86tcek73elbga2soc
  - Log entry 11174: process ruby pid=23923 uid=117 src=43.103.206.113 args=erc8v7ss7y59jx03xgltqd5ft8s/x0izfsblf9i9cx2l79d6
  - Log entry 85133: process python3 pid=19254 uid=799 src=166.5.251.227 args=z2g7bw9b7 /lbxx/72pf5quts4a5tds3ds1eg41q82khz-vk
  - Log entry 43880: process sshd pid=19336 uid=505 src=107.115.46.219 args=bdukijvl8udesftynp6uj4zdq ohtbpq-2nw aq31it39xsk
  - Log entry 73711: process bash pid=6709 uid=470 src=15.115.139.142 args=u1kea7e38su5twc0w9o58ee4nwy3nhmah6wji4u0ugl7l84n
  - Log entry 39857: process socat pid=30889 uid=485 src=154.36.31.241 args=1pg9sbvn7 957qhb5nenddro56-dd325z3bmyhjiimbdlrin
  - Log entry 35916: process sshd pid=11671 uid=213 src=96.67.255.28 args=cx8/zm4uo0olwece/a4271az9ddltatyqb48u40g75jdzt5p
  - Log entry 91089: process python3 pid=27342 uid=142 src=161.215.107.95 args=9ccyxkegj2all1/4lxb27hhqe3 g0qibrks3v9ccovc1zmjg
  - Log entry 68733: process nc pid=13400 uid=566 src=157.239.63.17 args=oo8n2o1qrjeecnlxiur6w1m3slp5/7amohh-gj-ipt-jrw8s
  - Log entry 15709: process wget pid=17237 uid=245 src=74.51.45.50 args=u7-w6h98lutx52to0ipdvsx37r/461mpewrv7lpo3jth62dg

## Supplementary Technical Detail — Section 26

Automated correlation engine identified 20 related events in the 6-hour window.
Baseline traffic on port 3948: 5 connections per hour.
Observed traffic on port 4444: 185 connections during the incident window.
Statistical anomaly score: 0.845 (threshold 0.750).
Related CVE: CVE-2026-16842 — not yet patched on 2 internal hosts.
Affected subnet: 10.1.0.0/24 — 11 hosts in scope.
EDR telemetry: 0 alerts suppressed; 2 false positives removed.
  - Log entry 84937: process bash pid=7404 uid=721 src=117.211.218.33 args=iop qo7ou90lj3y44suqf98gjssd109tdvleem5fz04o7hln
  - Log entry 28806: process socat pid=25947 uid=680 src=174.0.228.226 args=nb81p ops6q -68 v-uv7jlq030l6kkgw-xwwliwwjlbkul7
  - Log entry 58908: process ruby pid=13203 uid=123 src=149.15.143.224 args=wvbjg3j9z8ys3l9ihnq-0qb4aywzbeeu9p0qjg9kg9c5ofw1
  - Log entry 46424: process sshd pid=15087 uid=351 src=111.179.76.199 args=wqcue48v00byf21kq54 s526wie7elv0qs6xn9v rru-641c
  - Log entry 81805: process python3 pid=28016 uid=940 src=84.236.38.40 args=ngoeuyy15t7aree4jdh7e xdkciwp08fv88/y3 syqcgaonz
  - Log entry 18553: process python3 pid=26767 uid=565 src=187.105.105.175 args=vp rb1hlv0/tlr8gfivm34ma9pr6x-aau1m5biiowhmm mhz
  - Log entry 89714: process bash pid=15737 uid=859 src=3.123.56.104 args=1d2q9pu47bcmybs4rfmcmzoxd58r8ixlgf9568f1gtaw251f
  - Log entry 47750: process sshd pid=23553 uid=235 src=105.15.88.10 args=jh6pvsfux6i8xjm02gkmqnn3bz6gywfl89cx 9lq2q23/pim
  - Log entry 11944: process socat pid=21351 uid=918 src=57.190.229.72 args=u4/ccqk1/6itimke7cc8ww1msv3g-p6w2horvmfh0ynpx83m
  - Log entry 40498: process ruby pid=5737 uid=617 src=86.107.173.187 args=y/60x6leoxb4zvkwju0heaoyi992h1s4lhs xrl1iygbk44o
  - Log entry 31450: process socat pid=19716 uid=53 src=93.206.148.206 args=n5h v9h7b0vyo-3ulltur8uuxphdtocosyree8-mjl5q55p4
  - Log entry 55217: process wget pid=11989 uid=456 src=178.212.162.212 args=qm347zqd1mrlepayrshkswg/j8h67oad0lhw7jameip75wao
  - Log entry 68470: process python3 pid=14592 uid=374 src=142.5.53.110 args=f90v0am-04km//kdkjhrobk1srgo5vhyqfj 7lczm h9csuk
  - Log entry 69831: process wget pid=16219 uid=661 src=95.198.204.66 args=xi8/nq0//iz5qte3bn4s7y6n2x1/j0zrvsiw-haxl ggj48x
  - Log entry 91155: process curl pid=21346 uid=652 src=112.168.33.208 args=54e6m4xzqg-v2csug7e9b4-f 60l-fqtr628oiuxa4wb1zld
  - Log entry 41728: process ruby pid=15030 uid=493 src=121.11.71.17 args= o2xjvu0 /hqmxqcn3hcbdc7qjlojtberenkzendujs2q-i2
  - Log entry 65898: process wget pid=15799 uid=166 src=36.149.116.162 args=qtv oavepqpgt myun huwyho7i405z-z8lhv6o/kvm00rxs
  - Log entry 22285: process socat pid=12278 uid=813 src=132.131.233.187 args=7fup-339yxepm7sbgfjuzds0-ow98j04fg-j0ffc3z--uelv
  - Log entry 86044: process bash pid=18209 uid=824 src=81.207.83.12 args=y 20j5j7hnmn1zbhocggrg3sf/9zlcdeewy80vxbpd1m6czd
  - Log entry 28961: process sshd pid=13660 uid=229 src=123.141.191.174 args=oijaltwnmx7-8h12t1766mo7yn6tuu9w-xlawp74d25-8- q
  - Log entry 10249: process sshd pid=25017 uid=981 src=69.151.108.178 args=tbxb-rjp/s26sc3k2wsi3o1wf1z0-/ru4ykr1 tq9bkaw7sz
  - Log entry 61603: process curl pid=15563 uid=433 src=109.75.181.215 args=ki0rb/3vvaph8-smi-k5xpjd975q3m0ucx1ewc6zjsygxarm
  - Log entry 92842: process python3 pid=25004 uid=900 src=137.193.53.194 args=hrhe-wk5-gx35yiriomodtdou2squh6kdxs6ur  h7x1mhud
  - Log entry 43847: process nc pid=12498 uid=509 src=15.191.23.138 args=9hber5vvf1eehdi62qggijz4u3t07xf/9 /-f6p0zg8pmc4k
  - Log entry 50897: process socat pid=29888 uid=174 src=25.112.216.114 args=3eygbefmzarvwfgocr7wfpmb5c lpynsby-c5e1xm5y2rmid
  - Log entry 87753: process nc pid=15617 uid=374 src=63.108.151.234 args=2vfpd80h7e7up5ey4stzlt/ ngpu5q5wwihh7e8wgcp jezk
  - Log entry 25759: process socat pid=23501 uid=521 src=118.73.153.205 args=8qo2j3y8idcua3fxz7cih0lwoyux-v -xmb5m2a9ymqopnvo
  - Log entry 47742: process bash pid=21612 uid=593 src=108.125.162.114 args=ysyigctanneo5-i08vqby9f2f3suehypxbbdfzz6m2vw4wd5
  - Log entry 81253: process curl pid=18789 uid=500 src=146.14.234.59 args=7r54ni2q9rlulfrh9wbdxm-flj 58b17b--gcja /e8oz8u-
  - Log entry 41319: process ruby pid=3408 uid=887 src=205.57.84.69 args=/rognz8a77rsk9uz p1zt4jeb9ifd5cag9f2fx 19fkfnoe3
  - Log entry 63731: process wget pid=25976 uid=686 src=112.12.17.246 args=13x090iohggbs3epki8ftmg3cxl36uv8cdft/9-ysg-fehwn
  - Log entry 29132: process curl pid=23424 uid=187 src=65.31.221.103 args=9x1crhz-3g28wcnr240ti9td oxjntjx/5m0m 3pqtv-h33i
  - Log entry 37894: process python3 pid=8995 uid=355 src=180.172.39.141 args=o2zw/kd0-ii7ba//uv7iircnou/n2f9 b8lg4ifq9dfj5t m
  - Log entry 63565: process bash pid=26843 uid=712 src=163.137.71.112 args=9h0f- 1pippba2  1-/xhiu9m9d5ryf5evnenzw58qzmx6nb
  - Log entry 32367: process nc pid=7459 uid=634 src=187.158.244.37 args=xhq1ytdyhfp89gbch7f1an win-y-mdt68ca37zs-nnxcdhe
  - Log entry 62728: process bash pid=5861 uid=958 src=70.21.28.16 args=nvtyvcljlnm07881ny1bp/b7kibdgnkh  -sp9kb ulmckpk
  - Log entry 98274: process python3 pid=6945 uid=812 src=129.189.242.31 args=cdm/6l/vpvcyiph-jep6b5783jnvr81m306-bpoprsgbw25u
  - Log entry 31088: process sshd pid=22555 uid=801 src=84.55.18.151 args=8xvie/d2ln-ts0a8o6a73t-a58nwkv7/wdm0siqvq0mr4khk
  - Log entry 61347: process nc pid=1581 uid=625 src=73.207.86.159 args=ai6byaale f9dr0bqfrm4mdtva56bx840wpyp7jtl5zupw3a
  - Log entry 84231: process nc pid=27573 uid=375 src=103.252.126.126 args=hc69bu1v11irf4vwro-/-8ri40yn9xczfghjo/1y0vsqj6h5
  - Log entry 74156: process socat pid=16799 uid=599 src=17.211.30.120 args=bo-bnafsczec7f19z77qzcl0k/3vqm5timmoeeci7q2abjh-
  - Log entry 14395: process ruby pid=28998 uid=310 src=10.81.21.232 args=-hkr30nvu44r7wpuept-g4x4a97vexx4hv52l/678slhy3i1
  - Log entry 99323: process sshd pid=27902 uid=948 src=160.9.229.100 args=ecjfur1/r5kt95o/ri/n6jdj0u0k5mvik7kfx8rtjhr5jh-o
  - Log entry 95686: process sshd pid=10581 uid=807 src=141.51.37.237 args=j9km3ztsqik2qrbi36a5hx21jyuw7q4jj0-euzw4pj 0mep-
  - Log entry 24349: process curl pid=27793 uid=680 src=196.21.1.14 args=97idbpq7v956n3dq4rupf/4mxnqnaviprj58jf/0h-h-bcjg
  - Log entry 27086: process perl pid=13112 uid=247 src=104.222.99.19 args=rrw5p7m6oq94ug267pa/bba7w97dc7 0 gkv14vh7s3rb5ce
  - Log entry 47852: process perl pid=4510 uid=284 src=111.165.181.40 args=zp0ql8rs15r 6y2hpfh4q6 z0urbidhww30 1zbvahtsw4ya
  - Log entry 43349: process bash pid=8592 uid=504 src=144.164.242.222 args=qv2wh4oean0q0yx3jjdg5gl/0zm5pblii xr-lyt-s8/mgjm
  - Log entry 75997: process bash pid=5893 uid=389 src=152.32.34.79 args=jvw2mvcz6ej-xhl3c1z4mwnnaw98jgpf7a -15vq3 2h7-/s
  - Log entry 44806: process socat pid=20794 uid=478 src=139.41.1.194 args=fiwxl14k9n272q6b2bdqa-5-gkxlkbfi5frm1pqzxqfvuhx 
  - Log entry 51106: process curl pid=29460 uid=683 src=70.45.172.216 args=fmy9fvspc01jx699zen/-2kg-g-p/0kfaqbp/vrxl1wpszkl
  - Log entry 85837: process sshd pid=22177 uid=245 src=59.194.120.25 args=50/npx6begwe0ry87od qch3obi62rukeq665z4k/-dnj x4
  - Log entry 39158: process curl pid=10283 uid=672 src=158.195.53.156 args=pwa-5knc58ta mbkz8yel7y7y d5pbpt6fgmyjyevphyx ep
  - Log entry 39535: process perl pid=27797 uid=102 src=22.132.204.198 args=f r/2bs8lcul401qan7q1x7addtfqrorzonh62o1-9mq47a9
  - Log entry 89690: process socat pid=23761 uid=61 src=152.70.155.188 args=uuh8rj e8dgw6la2c009m0n6tbe8ir5c/lf3mhx-9nuir0je
  - Log entry 15891: process sshd pid=30813 uid=888 src=199.163.242.89 args=rh8egbftpd/pg054thhx3b0560xwkvo7aylfgu  z7v51 /z
  - Log entry 51283: process python3 pid=16219 uid=881 src=207.63.166.10 args=bp1891qaf1/zw ionwhodlylxtjcgvaf/-8x4-k9hw0vwa0a
  - Log entry 37134: process perl pid=1079 uid=604 src=118.5.111.177 args=v01/b pb9396ul4q1z5l7vdc-k4bmb-d/283an m9tvr0nu-
  - Log entry 46795: process bash pid=9464 uid=754 src=67.215.40.181 args=bah7v2ft341 dd8fuep hfeq0087u gusrvlcp0uin//-fpq
  - Log entry 93811: process ruby pid=7505 uid=202 src=32.47.36.145 args=qvgj/ihd7da9lxc1ljq8 knxur3sed6/9xwn0/luv-c9tvf9

## Supplementary Technical Detail — Section 27

Automated correlation engine identified 8 related events in the 6-hour window.
Baseline traffic on port 62675: 2 connections per hour.
Observed traffic on port 4444: 151 connections during the incident window.
Statistical anomaly score: 0.879 (threshold 0.750).
Related CVE: CVE-2026-12787 — not yet patched on 13 internal hosts.
Affected subnet: 10.10.5.0/24 — 14 hosts in scope.
EDR telemetry: 2 alerts suppressed; 0 false positives removed.
  - Log entry 44314: process socat pid=8712 uid=82 src=152.220.89.58 args=/b9 z 6zpq48v84vwnvrb3wk4qgy2gtaciamhwv3svz2yy6r
  - Log entry 80323: process wget pid=16206 uid=971 src=177.42.236.80 args=ren5bx7saw/1vgzg7/cbi10uogdtp2uo8/fdzqp5gtnnbug2
  - Log entry 83460: process socat pid=26173 uid=215 src=44.171.146.74 args=a1ydmr5 qg8r-h9aarc3kw0e2c7bo-iydbj5jccb13c2tl 1
  - Log entry 58403: process nc pid=10731 uid=766 src=174.120.74.110 args=701wlf54hn81g94yv4p2eao 5godjxxkjva8unnt41e-a04v
  - Log entry 38262: process sshd pid=3881 uid=668 src=111.52.95.151 args=o4irdun33hmy17ch9n5u4bpmada636hdhs7zoq29xig9zr27
  - Log entry 84268: process bash pid=6257 uid=603 src=127.142.183.142 args=am4hflb1ce0i7hmd xxoi/0evm3 /pf0nve7rqkrp2e1l2cy
  - Log entry 58052: process curl pid=7201 uid=293 src=192.3.205.39 args=g1m f1dtoy7l7wtkbh2xx7v5p4z82m-k9jouygobfsklx9af
  - Log entry 53173: process perl pid=9433 uid=716 src=103.119.12.143 args=o4qu/g1-rsc24c8-6o5g8v8bksjv514d3xwz3lyxe6hxehse
  - Log entry 68838: process sshd pid=19835 uid=243 src=144.26.130.5 args=rwo1p73owplhzq7l 2eo7z8rc1gw7okgz2v/pj490m0djt 0
  - Log entry 77722: process perl pid=11174 uid=314 src=178.161.179.7 args=z8o/jka-rh67j5ck669usfsem1n9s57bnkh1-d6 3c2yyc64
  - Log entry 40092: process curl pid=5684 uid=785 src=185.172.253.99 args=gcxxo3u/hzar5vbmnbnzh pz7 7r26cag9gov1xm92 ls14m
  - Log entry 27972: process wget pid=4022 uid=271 src=196.249.164.74 args=92f69q90xs6a7/fck9gwht8ofiruaua8jwf435x1z7gavbwp
  - Log entry 68316: process curl pid=15728 uid=354 src=168.206.87.61 args=-xuo06uvu11e-d6qtodc/vw29t9ldhkz4jaqzsn2wd5istfj
  - Log entry 72310: process socat pid=3532 uid=311 src=127.165.86.132 args=4 me9z07sklitcsix/8zgp4wcc52tuk4urc1l396uis9x 1s
  - Log entry 46950: process ruby pid=29983 uid=27 src=143.3.155.240 args=4ca5gc3bda7t1ir 7hb0m597lc axyz14jgjnvgzarpjb07z
  - Log entry 88880: process bash pid=20725 uid=554 src=199.124.26.57 args=v19mr98n5m6b7vu/o7ihv sf49-bkpcij6pycvzd2xr2hrxv
  - Log entry 49796: process perl pid=17140 uid=426 src=21.18.31.170 args=iz56xuv7scy dh889x75rd-zo /kijt8uxx/4eti/nehebzw
  - Log entry 97286: process ruby pid=5232 uid=650 src=138.239.56.249 args=zd-dua jt78pbuwiy9tni7/dygxrpuwjsockuh21al7gkjy0
  - Log entry 80868: process nc pid=31262 uid=497 src=206.5.106.178 args= s/5965sb0uq2clv09vi6jopthtcktojbym8dxg49w7u n2x
  - Log entry 66927: process curl pid=30134 uid=586 src=208.38.194.19 args=di6s8nc9te5 ld3k2x7s31uoe3mdv2gmbw5djfxkgh2ge7p2
  - Log entry 20756: process nc pid=28762 uid=362 src=206.2.103.182 args=-re8ky/a 3rcsftc5l4aizkm2q34q-k1mbeg0-m6-fdl9u69
  - Log entry 50463: process nc pid=16678 uid=771 src=121.232.244.163 args=kywvnpnacvf6/oz 1u89dd7m-38x6ilmcgzfkf7th1l4s42g
  - Log entry 44058: process bash pid=29906 uid=865 src=36.233.54.241 args=pltcfx7ckk9337ec-mlc3q6a0k/gdu8x0t51r6c6dxwyd2uh
  - Log entry 45199: process bash pid=18716 uid=605 src=141.193.36.155 args=gb h2mqbz02cxkn0hw/sml/hy3aq4exxzj-xt ztda92z-k9
  - Log entry 73695: process perl pid=21962 uid=832 src=198.152.100.44 args=y49yk2z0cm7uorl7xbhficiz1l/kgh0dvyisz2i94h6/9vzy
  - Log entry 83140: process wget pid=1262 uid=501 src=146.84.225.215 args=5a zcdfbl8kwx4yrnbilt/7sab2utbhm0v6bo2rmqyr//qbe
  - Log entry 10602: process socat pid=1293 uid=285 src=126.164.143.35 args=n o/r4h0ly 27gny8hulqj qse80pi69vs/zd5bclg-nxca-
  - Log entry 66765: process bash pid=10864 uid=141 src=113.142.226.192 args=atcqba9tk3qui9xq0ucbrpkcq70yzwtmsun81xz/0h3/ryu/
  - Log entry 42910: process python3 pid=6198 uid=278 src=144.234.96.249 args=2ub xtrq tl0hjhzdyveo5ue1hbdo58do k9vh45x2wbwn7n
  - Log entry 70917: process python3 pid=3158 uid=406 src=192.38.37.149 args=/8kqbpd301crhr4v2a1 fdmqrmb6k5b/yyaxwv-fdzwy0x8w
  - Log entry 22793: process nc pid=17768 uid=114 src=80.237.124.24 args=xffbr7hf7dw61-nz5pxp8g7co s67x-1v0508ger39wdynin
  - Log entry 38784: process perl pid=6030 uid=479 src=51.255.16.91 args=occvvyb5k7r/jc7m/adlwrcdntlu/xg9ip1gg6bicajdf1yi
  - Log entry 64708: process ruby pid=11351 uid=836 src=108.209.148.234 args= 8jyf8hjo wi3ff90855tctupvkyro2jzv47a60pkejh98xi
  - Log entry 65358: process perl pid=31968 uid=711 src=57.96.177.127 args=jreaz4/o7-khp4f8ly28twelypkme9 /7dacqnk5/cr200bl
  - Log entry 27376: process wget pid=17043 uid=134 src=134.211.105.94 args=e/jul8p7-njuvmw6i0ao3fwsm2v5czh9g u8z/4wnrfh n59
  - Log entry 46423: process bash pid=9693 uid=212 src=36.108.23.142 args=e-pafktz0-fneys864b43mtgii/tc26erq99-e fw89izq27
  - Log entry 70022: process nc pid=7087 uid=323 src=54.68.12.98 args=6amu-yppks62rulchmypydcol6toeqiwxs-21fk2sq13vb w
  - Log entry 15253: process sshd pid=21750 uid=724 src=63.143.188.176 args=/0alxxnmx30zrf93aoq7762c3 uqys/33 -anyrmw6zhp550
  - Log entry 26937: process ruby pid=17203 uid=733 src=194.9.101.130 args=00l3rd21dbspq hi17k6-1h4pixjbvqaow-bh5/2c0lu9 bh
  - Log entry 16121: process wget pid=9885 uid=966 src=206.111.22.253 args=5 s7jz0o4 mb f713g4ez-o8t6ay0z/td/ct3wk8weukwq6g
  - Log entry 33730: process ruby pid=2437 uid=594 src=156.154.86.209 args=vat105-705vkjvj6ack96pkf8n9hc26-3wq14w3v 3yzqf5q
  - Log entry 73267: process perl pid=14030 uid=356 src=204.159.90.111 args=91/l8h2iiv66ommrvs- jlmkhw/yv-oi3d8w6vpbofdt2qcc
  - Log entry 39163: process ruby pid=7070 uid=360 src=197.21.184.164 args=hod1squvj6ugtkn-zivy6g56v-tf1 8o2q2knj4k725jlhbw
  - Log entry 88956: process ruby pid=6039 uid=30 src=140.15.206.114 args=q/ndrj/fa9p276ur2mcye5i85mj1v/2fp6msjmmqg9dul-es
  - Log entry 47199: process bash pid=20958 uid=843 src=68.194.97.171 args=7kxxm d92d43b sd4skffye2c fn-jvci5pbi42yacfse0lr
  - Log entry 64155: process sshd pid=3502 uid=892 src=104.142.139.85 args=o1ioqyr5f-iu8at kszvb8k6ib/7xo72/kq091ks0upeyfix
  - Log entry 77260: process sshd pid=8999 uid=518 src=127.232.143.175 args=eykmglsat17zl7i2/zw1trol7g/zhq9pd5n9hljkpqiceb/k
  - Log entry 68054: process sshd pid=31303 uid=625 src=154.215.159.5 args=n0thiofdr8346jyfb4yrt7mlk-b6p/0kk84/ziua62gumdxd
  - Log entry 13028: process nc pid=25537 uid=522 src=145.42.88.204 args=566vnrxgte e99-5lsnd149561itoyuvai6xe1jqt/g1tla6
  - Log entry 81649: process curl pid=25182 uid=445 src=113.221.50.26 args=j7 z43p0uf00hxevwr9sk4-utk3autoddw-pbm0nrn0be8b-
  - Log entry 38030: process socat pid=3025 uid=242 src=121.244.235.103 args=ue-uytnwrp-upsxw33zlhrrcuod425dby5v/8 ca9u-/z9b8
  - Log entry 62482: process perl pid=1603 uid=850 src=149.243.175.169 args=0xx9jpm3ywg2i1u6ism9g54dyd4b45fbitxcdct74k9u41-t
  - Log entry 13008: process sshd pid=6099 uid=191 src=111.218.194.166 args=p/hrn63b8b4iu16lnyy 2hfiqjs d2f0bhzh/tl4u4b5vi8t
  - Log entry 53196: process ruby pid=11895 uid=672 src=176.53.171.96 args=4sy m0/kxc/p gi8woeaxvdebzv17xe66--qw563-z1gk689
  - Log entry 93178: process curl pid=29082 uid=298 src=67.75.90.21 args=03xvrlo6onizm9 zj waj5wgtcplfzfjys4 j1cffi6 dkcy
  - Log entry 41904: process wget pid=8499 uid=985 src=4.131.205.23 args=g559 de-/w1uod10t3e/sp70w3u1q827/y78igcnibbe/nzw
  - Log entry 91816: process curl pid=31910 uid=477 src=216.75.211.188 args=bdrt6pogy 2o8i4l7cc58nd8gz/wxenzr2nz6id vol9v9eb
  - Log entry 21546: process nc pid=4410 uid=398 src=3.141.78.170 args=g/cn-5trc/ppi2zn6 nniw0zpx 6w1vccd4o7d/l8ra4p/eh
  - Log entry 62890: process sshd pid=15024 uid=951 src=116.89.223.25 args=ikuwj3g6oqpg0 fdco9z9f7ic9la29ertydto 2jv252nwgr
  - Log entry 58557: process perl pid=21974 uid=210 src=87.253.94.252 args=shzi 5u7eyr3a61zxq/vruf7cm5c5znilzjvzi81zoii ad4

## Supplementary Technical Detail — Section 28

Automated correlation engine identified 10 related events in the 6-hour window.
Baseline traffic on port 1200: 5 connections per hour.
Observed traffic on port 4444: 200 connections during the incident window.
Statistical anomaly score: 0.945 (threshold 0.750).
Related CVE: CVE-2026-45068 — not yet patched on 11 internal hosts.
Affected subnet: 10.0.3.0/24 — 21 hosts in scope.
EDR telemetry: 5 alerts suppressed; 3 false positives removed.
  - Log entry 36011: process sshd pid=8886 uid=942 src=105.233.116.247 args=owzyvm5806d qo jumganq8sa68eimkb2l dx3vb73ii1yg8
  - Log entry 50134: process perl pid=4988 uid=236 src=202.137.8.112 args=74d3an3au-y1kkbkops4frjt9op/e/8p63xbyceetmbtw6um
  - Log entry 80114: process perl pid=17072 uid=965 src=1.150.120.56 args=2acirxxd86opiujg8p0tzoqo4ks80-q79j73pga-7-1dn588
  - Log entry 80798: process curl pid=20224 uid=943 src=164.45.255.40 args=j14n3qzvisee-fn6oguguvyaq517gok1p261td0thc1hrps/
  - Log entry 81960: process curl pid=23536 uid=354 src=70.108.84.149 args=nhgbimogyd/8662gt8x6hku5m9oqgzx54g9lamw85a0b9853
  - Log entry 81291: process bash pid=1631 uid=153 src=91.9.16.168 args=mn94fhx92vmoqmntwih9-dm4a4hib7x/u0xgg3f-/ bvvh/q
  - Log entry 83031: process curl pid=2421 uid=916 src=206.149.140.13 args=keclz3b3/ral9sdmg33l06igdcvpptd94agx6uv1lypn cp5
  - Log entry 25639: process ruby pid=15909 uid=850 src=174.109.121.191 args=3 na8r17hyrkirljk0 2-lupyhng1 2k14n/y65rnmymge8c
  - Log entry 74229: process curl pid=1697 uid=249 src=116.19.32.245 args=gfqz9h8pmcw06hwfdcemhh etk3oe4f9vjj9/v3fuqqbs1j0
  - Log entry 88740: process ruby pid=18564 uid=254 src=104.186.72.168 args=dogmrkd5ga17gf-q6t03ewt82ae5d/4sy ntmnbvajvj5dan
  - Log entry 68145: process ruby pid=10988 uid=555 src=46.17.151.210 args=wgzp9ob/8s0ig50tr0kacare6wxm/dwcca17wt5 tmsb3jzo
  - Log entry 32882: process bash pid=11592 uid=354 src=168.183.22.108 args=dg hz/mbow0whevv5-kf w  pkc-5 aqjb-8gs257yehhn-m
  - Log entry 26844: process perl pid=1409 uid=562 src=63.73.95.90 args=xucd-r2p07pbezrvuvcfg0pkfcb-kl9qsf6t/g0pr-8z21tb
  - Log entry 28050: process python3 pid=1448 uid=932 src=191.156.239.93 args=yn0kihognzr4x7rb4/qp0adezij8ohes/z 4l 8osuck0cb7
  - Log entry 40116: process wget pid=23012 uid=337 src=214.50.92.34 args=9rhwl9y78mh6ttsuqk35a-4up23sgg0kuwkzvwzf2wfw7xde
  - Log entry 51877: process python3 pid=19874 uid=399 src=53.133.192.12 args=ybsknsel6ihs0taf68su653t62/omqnyk/jyqqvppa2gjc59
  - Log entry 57357: process nc pid=27412 uid=916 src=107.200.66.53 args=tpwf/rs6afn17d4q-m78nnyqncbd0omufaenu9xk2/0zku2d
  - Log entry 95985: process socat pid=19146 uid=482 src=171.170.189.48 args=7xbe/1yiey/dqqlwbs/j93phg7k97fhmejj-ld8e7mt kuak
  - Log entry 21304: process socat pid=28955 uid=161 src=13.5.4.120 args=4438xg/-eb9d4c291o3737vcli778ydr 1lo/opp-z417pu-
  - Log entry 28979: process ruby pid=7166 uid=250 src=36.214.80.92 args=uvywaa 4w 8en0dwsw9dvm1bmvbuaaluy60q9-qk69 9tf8a
  - Log entry 45434: process sshd pid=27152 uid=604 src=111.206.70.127 args=9dhoagvto6hk7sfm8n51zk/gha rn8eryp2i/z/d-9ilyhbk
  - Log entry 74309: process python3 pid=13503 uid=398 src=56.68.154.124 args=voh/lew42q7tupf0uin361yxn79r8/0au0ljqq0ffzd4b7iu
  - Log entry 63441: process nc pid=18975 uid=128 src=96.166.47.75 args=5fofk8 515223ecglh-vpagwrdam4aly4mcc/mtu27dy y03
  - Log entry 24394: process socat pid=27023 uid=871 src=42.158.51.216 args=c2d83fi0x44vknfq-wvwjm84fnmq4g rdxiw966i4n rppdh
  - Log entry 24930: process bash pid=15124 uid=862 src=149.218.95.55 args=59qneqhweqzk4io32tdkarg3hb7kj7h0tio5tnkpet7nn5kw
  - Log entry 35850: process wget pid=11825 uid=807 src=81.147.205.65 args=-8u0jnh3-d-il01xb9vqet1146rglgcaorf9qv3hznqj0-8p
  - Log entry 32892: process perl pid=22845 uid=894 src=100.182.212.3 args=q8wd-0j/1l2n67351ryl59f-mf4ds609h8c1crxbunw3n3 l
  - Log entry 46868: process ruby pid=8663 uid=406 src=6.101.84.211 args=vah5z8i9z6g-4puubi3z77e7be3tliipig1p2qlv16bzzfsw
  - Log entry 44823: process bash pid=19074 uid=308 src=166.117.237.55 args=ojn/gudo9peg3o7wlf4jj0dri8sc74gp--7-gy/al 8 1bkj
  - Log entry 46933: process python3 pid=31500 uid=857 src=199.180.226.236 args=y4mz6s243/d66dwidy34m/xm7r/yz-92/w-qthpz4vt8jx6s
  - Log entry 39934: process sshd pid=17697 uid=990 src=4.73.53.86 args=biqv7jzymyekx8z m/q-h35jms8puzqd-vn0pnf6ymgf4-ux
  - Log entry 19495: process python3 pid=24796 uid=639 src=188.165.210.88 args=jzt60xq1n67eb/ces830z23t/uqlkpoke3tx60j7ukse7gzp
  - Log entry 74129: process socat pid=24007 uid=715 src=72.149.34.208 args=gdomj8-rup77jtbh0pjhzr745a2il5zs73zn/gjdzr -qnzr
  - Log entry 92448: process perl pid=4538 uid=317 src=98.252.25.235 args=jtkog7wtvd9-3ofzq4q rhfd29wnap8ypx08/x8hn6swb7h/
  - Log entry 31630: process wget pid=26529 uid=216 src=141.172.156.60 args=gah4w34f3/h5jrankvrg badajsmtr0sgxy-xkl2y50mfasz
  - Log entry 99861: process sshd pid=16975 uid=456 src=104.111.147.248 args=b46ll/9ho19nb7w2h4kts06e6klbevikjarkcmdnwddi rms
  - Log entry 80759: process sshd pid=15188 uid=454 src=7.213.57.124 args=cu-2s9vb2a6x2j6eutjirhusrb3mh3cz04kk 5hib hpoz8x
  - Log entry 70479: process socat pid=21134 uid=174 src=184.68.33.203 args=cfuo3s/-mk7h29pa332g7noskrvy8xw7zh/9oav/f93vl/ch
  - Log entry 78602: process ruby pid=3300 uid=969 src=87.215.182.25 args=76/d7bk9dtsl7qkjeyqv65t0wuwtwq42cexjac4ag3ij5sta
  - Log entry 56130: process socat pid=22682 uid=273 src=214.111.10.156 args=ku/ccyqvws9qxc88wuuclr-a47rr0wiktnxq51ct/h0bd42e
  - Log entry 28315: process sshd pid=20858 uid=908 src=159.151.56.10 args=hjaz9v3kpdpcyrxg u826eorgrs9uzxv-ls-h-v8089zf8d5
  - Log entry 75647: process nc pid=22482 uid=492 src=177.114.23.127 args=b t8r9b74-8ma3 mhiert6bq/26mtz7oamx77irhmkbh2 b-
  - Log entry 58101: process nc pid=14267 uid=836 src=65.112.22.101 args=l82688158xk28gp6ae51zal-ffl6t84hrts-tn8m0om/cud5
  - Log entry 91809: process curl pid=7996 uid=218 src=190.33.7.142 args=jqseo842dvsm3od -bicoua57a1iy76-9ri73n94uivt3zc2
  - Log entry 83477: process socat pid=24026 uid=927 src=108.118.142.186 args=uisfcd/313c0pogb1t9j7v/pm-ivc/gvq7wzvx6rtt8uus5e
  - Log entry 12711: process python3 pid=20024 uid=535 src=184.76.199.199 args=qviws7b7soibcb2grrkth02hxcqzkeyxyqyfb0alu5ickk4q
  - Log entry 77569: process python3 pid=15605 uid=478 src=94.226.46.200 args=2 8e915k8rsf77mev-zxt9 kgp1e4aj1ypuwkjh/iyvgrzoe
  - Log entry 26462: process python3 pid=4135 uid=294 src=103.51.192.113 args=b/s/g/ifq5jv/w1u-jafexbnakirimfeo7uam oququxzm1q
  - Log entry 75024: process bash pid=18364 uid=259 src=2.168.104.184 args=yt5hklh-z74b-jmu-cun8hsvbu1mqd-596d1nlm9e/h9 nfr
  - Log entry 38079: process ruby pid=8082 uid=145 src=159.199.17.18 args=a2v2qxwf63f3zu1j9--r//1vsr/rbx/d-wblvo9ho0ogdf2n
  - Log entry 92566: process python3 pid=14683 uid=694 src=103.25.148.227 args=t0a-ops k7ci95m-r7yyloa67 q9b45roawven8/ghlo r7v
  - Log entry 76680: process curl pid=17884 uid=769 src=201.60.214.188 args= j8rlxrhrvahsxg42-fqbtcut5jf82uk28rz0zdr9/428prq
  - Log entry 20783: process sshd pid=22840 uid=508 src=93.86.131.155 args=e-csesdrziel5umat udco5y98z5e19iggsi38yczv-1k5m3
  - Log entry 76845: process nc pid=20621 uid=966 src=39.196.82.151 args=bj5vstl fe51p9imupm1cn/0ub0z o7kjik-l4q7s5 ai3u9
  - Log entry 63608: process nc pid=25880 uid=937 src=214.141.81.16 args=b6/nrl934v31kph4a5-0 /nqr76fh0krww733cb0gejv47-4
  - Log entry 66382: process curl pid=26499 uid=389 src=144.213.248.216 args=xet32/w-i4ie1d2tmm5x7zpq8a923yrpe0152 ah7he8dsmo
  - Log entry 21078: process ruby pid=24394 uid=117 src=109.91.109.46 args=h6a6xelvgwl  xr0qoj32uizds1zr5ei-9bxlqr60rgkuj2k
  - Log entry 99620: process wget pid=7358 uid=208 src=199.62.39.241 args=qimkzejw6xs6s36yqshek4 pchp35qa9f6fffejvb-bvoek0
  - Log entry 31385: process wget pid=16630 uid=475 src=85.44.36.234 args=wvzwazslpbnhx jq71li127etvk09-68y7cnzbvksk-i4639
  - Log entry 39102: process python3 pid=26731 uid=949 src=51.169.56.38 args=hp06a0f yzsnp sa47/u-4gy5voduy2n9hc980l0bmu j13d

## Supplementary Technical Detail — Section 29

Automated correlation engine identified 12 related events in the 6-hour window.
Baseline traffic on port 25558: 0 connections per hour.
Observed traffic on port 4444: 87 connections during the incident window.
Statistical anomaly score: 0.839 (threshold 0.750).
Related CVE: CVE-2026-17965 — not yet patched on 16 internal hosts.
Affected subnet: 10.0.3.0/24 — 14 hosts in scope.
EDR telemetry: 1 alerts suppressed; 3 false positives removed.
  - Log entry 80590: process wget pid=29780 uid=731 src=33.229.228.51 args=oa6 / epplk8wuz2kpzth64d-dbim73be5peq38g40o15-pk
  - Log entry 61518: process curl pid=11192 uid=243 src=106.32.213.45 args=6jnz90tz7 /dlkfe9e8n5omr23xkmbbctvfcg2riwfqk/2t2
  - Log entry 48916: process nc pid=6564 uid=325 src=50.20.95.118 args=v-l6mkc3pt4jmuwek4lzmk-fu42-7t2pkpl3rlp3hfuwwzfj
  - Log entry 59517: process python3 pid=11267 uid=5 src=175.98.74.115 args=6uigcrsxsrgqnw28tl5cpz46xw5sjicvmn8rqzcr5eoiqep2
  - Log entry 54901: process nc pid=24263 uid=617 src=172.173.43.61 args=/k/gj-z6 a18wb8u8/j79pu8p5wankubl2zcpo80h onyn1r
  - Log entry 29726: process socat pid=22231 uid=78 src=207.162.96.195 args=3gvwh2ko9d-nd 8mxoqz7m8cits-1gl8ow7diqq8be7fdaee
  - Log entry 74580: process nc pid=6380 uid=309 src=192.186.16.225 args=utz0wol rwtrfqfgob9vqajtohwqpluahe5gd5qqwzu/lr0l
  - Log entry 32834: process socat pid=27644 uid=498 src=38.162.115.136 args=/jig569kbk84nud4sicimikz5ygf/614fefmo4l5dh4em1a6
  - Log entry 36598: process socat pid=27390 uid=142 src=194.67.125.193 args=c h4/brofb7o-um-w2up wvywxxcsrin4paf3dmg jvu0hx0
  - Log entry 87466: process socat pid=20389 uid=929 src=75.19.93.244 args=-7ot9t51 py9skdddzzc 27r9/fue686mbxq2nx6/9gjb6 s
  - Log entry 65560: process curl pid=13309 uid=635 src=213.53.238.182 args=g04ysyvp5lwpuy/dsvae18skrvhs72qw/thu bqt9hhm3 r9
  - Log entry 27411: process curl pid=18327 uid=371 src=183.114.60.101 args=i91q4gw/gncjtt9nq0iu6dvm-v0bzmd2/qf-rok8q8mj7a0q
  - Log entry 73446: process sshd pid=25951 uid=318 src=127.152.18.88 args=z40ygyg13ijcipigri1lrp918gqd/ fy/jha3/xpq1h489qi
  - Log entry 66671: process bash pid=4756 uid=202 src=205.71.88.168 args=gmo/lb4mjz7d3z7xeh700djw2otwyij-xkt01m4yxiohcj5a
  - Log entry 65209: process bash pid=27044 uid=169 src=150.112.210.170 args=4d-9xbxd-hy1ybnol4zl73/kc8ab3stfow60uz0z24uwpxht
  - Log entry 24884: process bash pid=6253 uid=58 src=112.127.218.153 args=hcurcrbzc09jqz1yv 0fpp1obq08n6x0bq3ga5cxmwx-8q1g
  - Log entry 17903: process sshd pid=1604 uid=983 src=136.44.13.32 args=0qvwb02auequ8l828w 587fr9c5rdcn856o-q-wavix-jai3
  - Log entry 31595: process nc pid=26267 uid=509 src=133.111.107.90 args=9j rbyg9lxhk0i49ihikuummcohtrbw 9pax32n23pul6 qa
  - Log entry 87079: process wget pid=25605 uid=356 src=12.52.241.42 args=/vhg2/ qqxqex7mog2kc6/h-87h0dtyvu1z2cfj2drj/mfcy
  - Log entry 65350: process ruby pid=15644 uid=238 src=97.122.134.146 args=cwf13wam-ftegdgnf17g35/j4jmpc 4m4zw5jgb4sil2xvh9
  - Log entry 30189: process wget pid=30616 uid=723 src=102.33.7.90 args=kqxbua854jshjgud04-6ipdxvvebowocxx-w8f86n1q9s5f4
  - Log entry 58566: process ruby pid=16962 uid=989 src=46.80.39.145 args=l1uz6bbmyd9ezlfgw1-abhxho180tjg3wydy7ri ibgqit7u
  - Log entry 27079: process wget pid=2832 uid=824 src=75.152.246.242 args=seb1g/1oxqj4-y/sf4bbb-ep6zycjjss5h0pdohoi7-xtugn
  - Log entry 32285: process bash pid=30350 uid=749 src=204.81.47.88 args=qd59mufpvnz1e/cpo4p1h9 ercd856e3crwojub65dweinbt
  - Log entry 73917: process sshd pid=29232 uid=819 src=65.149.27.180 args=zzbcp/bh8veqc /s5r3j5v51yor0y-p86 h1gg2pfgl0v3/6
  - Log entry 61586: process ruby pid=26903 uid=349 src=210.121.192.166 args=5hu 5vogl89kwwo6ko5m22ny64494zqqvk58cmu1v 5gulws
  - Log entry 75848: process nc pid=5923 uid=210 src=69.117.158.52 args=hvqdw7ncpt4lc6sdy3y8h67zk2jzrnt3kqat6u88ab 3gjxv
  - Log entry 32629: process socat pid=8032 uid=690 src=194.136.144.193 args=b2zricq535cmql-y50yidl6bqbqpg1kz9vy6e21ha5m7 92-
  - Log entry 55316: process wget pid=25091 uid=578 src=99.35.97.216 args=pk9u/sg1zxu6fjp4xq3hoxz6x ie6qja1vu44e7qkxnzg2u0
  - Log entry 76011: process sshd pid=12689 uid=772 src=21.21.169.154 args=/pfii-ha9mcrw9prn9hrq42eu6d-f1c7 fs/w50dhewrrsk 
  - Log entry 58515: process nc pid=25193 uid=224 src=97.41.250.229 args=ahtrkp0sqqr50-bch-6woq7jyiq7jqkvol3m52mo/1369q7x
  - Log entry 24154: process wget pid=4528 uid=272 src=155.61.163.241 args=i smtj96fk8xhblaqa vo n2lvf9968rum1jci8k302y0/p/
  - Log entry 43819: process nc pid=13674 uid=354 src=212.209.81.110 args=qg-1/60m3 9jka8v/57lh/1pvpp-oesk-tqr/ec4e2mnwizy
  - Log entry 19235: process perl pid=15565 uid=863 src=66.174.120.59 args=8/bjq28jaafkk 0-hjdmv/3t7pdetfpn t36ngzok3fiyj1c
  - Log entry 68208: process sshd pid=20467 uid=345 src=152.195.129.248 args=2eh4i90x5wm8b1i1ldf9onk/-32 oejtfl2c8aagx 54h8ks
  - Log entry 85520: process socat pid=2499 uid=483 src=16.152.148.120 args=u 9 g-wamyc56vqmkmoru01q503dzs1j /nuutk7kuoj5l40
  - Log entry 69867: process sshd pid=26180 uid=186 src=168.77.225.106 args=x8xytsou8a60ijydyrloquuacbw-n5mk4/xvclc8cu/sjabo
  - Log entry 79132: process wget pid=14078 uid=138 src=4.47.114.218 args=v0z2qabsuh5 228263c9r7np5c3881qbrjf/5ao2erj9m61w
  - Log entry 94259: process sshd pid=15722 uid=528 src=68.134.42.188 args=ut-8u3n8lb/bdbh9zakf 0hmhzedhvoqmx uk-0nseri6w9-
  - Log entry 24132: process perl pid=7736 uid=554 src=175.164.84.233 args=wbec1gbu5w6l t9wd0v3x8twycp3uubnj40i7ue0jxv/stul
  - Log entry 45720: process ruby pid=22724 uid=619 src=62.185.89.74 args=1pw- 9x520d8jeisq7c5lwaygs4p7zcgpv 5u 0rk2o7vm6a
  - Log entry 68658: process curl pid=30546 uid=154 src=106.233.15.184 args=6fwuy213bwjg532gnso2lx8o -sbjs9eack6g5p3v6aerqvk
  - Log entry 22046: process perl pid=29700 uid=93 src=132.82.134.63 args=l5nargjdp9fx/ce uvjf97cl6elpnm5sbrr836o0ebeqkq8d
  - Log entry 82801: process socat pid=14065 uid=734 src=106.22.4.184 args=v5iy8 nhlpbn3uy/0i3hyw5h/zwzp3mhiu-va2iy3v4dj0gz
  - Log entry 16752: process python3 pid=5921 uid=391 src=32.252.43.34 args=ij3 f8xuom2j55ow2hy 02m2qz/l8q-ts7xh5oh7u4kzd2rn
  - Log entry 78192: process ruby pid=14550 uid=923 src=100.56.112.239 args=g090j/7-66pcifgckh9tdu8xa0wx-1ubrc-emkari9tq6id7
  - Log entry 67011: process nc pid=20833 uid=758 src=84.86.16.117 args=s7h4y4vfre3 /x/atqnktmbo5bbs-lpu82gk4mjvwwp jcl6
  - Log entry 68710: process socat pid=17160 uid=529 src=45.220.1.81 args=cizy-1-oeqsunhavm-qe1tu8g m1q1g3oh7j4y5lz7a-wnim
  - Log entry 13294: process ruby pid=28655 uid=467 src=69.213.124.182 args=d9yh0n5t8q8vv qjm9udzi39l8qp0vmddfpyd6gjdg5-9/jj
  - Log entry 49735: process python3 pid=14873 uid=999 src=50.0.84.252 args=oxt79b8lgb1qd4ch9-4of7lcob5409vct2m0en9a2n3nrcvj
  - Log entry 31239: process nc pid=5072 uid=492 src=7.28.65.72 args=1v81gpnmx0ae0rx6yks/jexe7350hjs8ek9sa2kxpfqt2iwn
  - Log entry 72187: process ruby pid=5350 uid=647 src=148.141.0.31 args=uv/pwis8jaedfgcwu7m4rfogwiux tndlcefn7kgs3pxr056
  - Log entry 95120: process wget pid=1931 uid=499 src=74.185.154.100 args=pvfy3x/nk-/ihddv62jfw-wk9l4/nks17tdd3pi xdmu7l7w
  - Log entry 33284: process bash pid=30239 uid=292 src=213.96.146.60 args=5j5u4vmzm14 x1-q1-w6m6yb0oz6a8 qq25gh-al9q1v6qnm
  - Log entry 28265: process wget pid=16673 uid=436 src=212.166.107.5 args=bj2wqlgwacw83e4ngx3ehpwu9cn5 p/ts-okdzvh2u20kpi8
  - Log entry 21165: process bash pid=15354 uid=587 src=83.61.21.111 args=cc5a4jhbxlbydb1rzke8r771f2shamjykw8xt4rdckuib4u6
  - Log entry 48990: process sshd pid=23312 uid=787 src=204.140.178.143 args=5f kyl8ibizorygplfn3o92 ch i5955r8 k4mu0jxwr2-0q
  - Log entry 43787: process perl pid=27119 uid=345 src=51.119.96.202 args=muz32eazu-2mta21m 7 2jff5c3y/ gxhybx9psa77jqej8z
  - Log entry 31282: process perl pid=15683 uid=432 src=157.207.126.43 args=0/n5qxto3d9ixpc epbrc5uqs f9onrjs6mhyru0bvh7/qjc
  - Log entry 97274: process perl pid=26623 uid=159 src=212.239.176.89 args=kes8 7/3wbltojivi8u92q662lxq-k-xdzx5 ssp2b/m4/e0

## Supplementary Technical Detail — Section 30

Automated correlation engine identified 14 related events in the 6-hour window.
Baseline traffic on port 4950: 5 connections per hour.
Observed traffic on port 4444: 151 connections during the incident window.
Statistical anomaly score: 0.867 (threshold 0.750).
Related CVE: CVE-2026-45616 — not yet patched on 14 internal hosts.
Affected subnet: 10.6.0.0/24 — 16 hosts in scope.
EDR telemetry: 2 alerts suppressed; 0 false positives removed.
  - Log entry 93183: process ruby pid=17019 uid=130 src=76.27.185.95 args=qvnbis1ugc c16r /3ykm8x0fg/gneiiflc46dz2293f26bk
  - Log entry 18895: process ruby pid=16126 uid=295 src=106.7.232.159 args=4ete nd5e0ntn/nyzc8/fg9c-ulipkjoj/lz2junr2-ji-e6
  - Log entry 15334: process sshd pid=11078 uid=533 src=204.161.66.81 args=2p8k-d13 8qlt6-le352a c3z3mx-wp6bn76crtu8n1ysvp/
  - Log entry 25200: process perl pid=18935 uid=143 src=195.193.15.208 args=q59kbys3c1l/8hndlwvof6kwxxj1gugxw99f0h4fu/prz-6s
  - Log entry 66627: process python3 pid=19044 uid=35 src=29.119.153.150 args=ptlq1hu0 fheum7-kk1oeu3jzq75tqmw8rdxs/ 9fhyxyv-r
  - Log entry 96665: process socat pid=8368 uid=799 src=34.103.179.147 args=i1ylowk5-kecv0brv/96dnvhzgnvxq7lli7bvd9tciczhxt8
  - Log entry 27163: process nc pid=26219 uid=738 src=93.35.72.4 args=fnfd1a8vuqgftq-c8a-jvhxc-/9gx 47099dj1n4u/i9-91/
  - Log entry 80980: process curl pid=22776 uid=974 src=93.73.181.151 args=q1mvvj8d-kx2purh4pf2709nop8v-2ld2ub1155yfuj/u2qd
  - Log entry 94277: process nc pid=19754 uid=782 src=209.250.243.98 args=/e 1e4xwfdc75k7cj11ck d2vg194xplygqqouhu m04topb
  - Log entry 38135: process python3 pid=27413 uid=950 src=197.232.62.127 args=q1aa49/iohydbt2ae6wtt9gpzue/ntyewts/n2o6xp24cxzu
  - Log entry 40496: process bash pid=25152 uid=46 src=177.200.200.30 args= 5o0u65csam 2dbr/hpii9wwu4x69p-be3 h7iomaojgd7tr
  - Log entry 68162: process perl pid=9087 uid=725 src=132.183.71.170 args=xgm3l/n2d1cxvbt7qm0kop1b7pqvx9u64dj vt0pfnzlg8gb
  - Log entry 91466: process python3 pid=7966 uid=90 src=93.101.208.180 args=mag8ji5b/5wmhlsulfsl 4irpiiz92n6gl9f t82ht//hc1 
  - Log entry 84715: process curl pid=18260 uid=171 src=8.167.4.32 args=5ddp1dxy26b-omabyqzfdb6ehhqcax59qtjidcc0ipnr38f9
  - Log entry 59295: process bash pid=12177 uid=518 src=112.209.169.212 args=4m15izmxk1-ghy04/1u9l m66f3s-p1uao1dt1u/o9ha0u2w
  - Log entry 61362: process socat pid=19428 uid=285 src=59.99.66.106 args=27 t350/bltrazn7j6vxxo6zhhsvj7dey7ue4cg1fud3nwhy
  - Log entry 14128: process nc pid=18595 uid=906 src=40.148.69.114 args=36sv-6-5rucx/ -jtstemy7927vgtdrcua0cdic787houe3e
  - Log entry 47456: process bash pid=6255 uid=804 src=57.108.214.172 args=8s3uvdtcqsppektdwjvc/m3vela6aq95ix71qot8fl6q9iwe
  - Log entry 94940: process sshd pid=15579 uid=970 src=129.211.107.204 args=fwzc3vn31e2tylnx9qv7-2cceyf2blul ocok-leo72bbtrt
  - Log entry 62143: process perl pid=8445 uid=370 src=87.151.165.208 args=j3zz5vtq0xh2sowmse3w3 n9ryeqgz7sr-zfuybvlsfmprf7
  - Log entry 41334: process perl pid=5922 uid=261 src=47.210.251.73 args=qv8szsh-v/p7075g11t0ddtoy8iygb23 xtxia/-ylpye3th
  - Log entry 80696: process python3 pid=29664 uid=784 src=126.12.13.242 args=zqra4gob8f2h6krh5sdlfw55t kk/z6mu730nn0-ble5881w
  - Log entry 44234: process python3 pid=26136 uid=968 src=58.251.212.111 args=brw-8qw3zu tssw5rwzasvzy0dkipc1f5vllnsxmd/plea-h
  - Log entry 69024: process sshd pid=17781 uid=897 src=72.107.243.147 args=i6t42a0hkd8j8rx-f3d9hrt-vt1f26ylz-/nv1y49u02u5o1
  - Log entry 68389: process nc pid=22974 uid=437 src=136.162.133.9 args=0nem8cvda5wi8zlvpikwrauiia1wz-q/v/m/3np4vki2jhh8
  - Log entry 85651: process socat pid=9880 uid=197 src=96.29.122.235 args=7bi4/7pkifixjc17iiukrtnya9j18czz-jcoz-76/ytgr- u
  - Log entry 72721: process curl pid=26478 uid=58 src=159.97.109.153 args=hloz528p1h227nyxsz2n2naiew1ru/124yozuyf1tf1 7ue/
  - Log entry 76477: process perl pid=1120 uid=692 src=57.158.217.154 args=za8k4wvenspqywr56z-4mbqo-uav/fb ri-t52pjj531ly07
  - Log entry 61785: process python3 pid=12635 uid=261 src=159.91.10.137 args=lhs /lb0wg44 64h-am9xsa2d/htnu73w/pzuduou6jovmwq
  - Log entry 53236: process python3 pid=20490 uid=620 src=99.141.218.76 args= u84n8efusvej2vxcw32e73fdi30r7-xdj0jr92w/ub5bn7/
  - Log entry 87466: process perl pid=7754 uid=433 src=172.82.111.173 args=45u6rak b5ht1y3-7-kgxbs57n hufxmd1rh4d8x636cmyty
  - Log entry 99228: process ruby pid=17766 uid=516 src=181.22.135.222 args=zx -uo3zwsrrtoopndvjq7pcuasqf6lk/25am0t53j4rglgv
  - Log entry 54071: process perl pid=16462 uid=189 src=217.0.67.37 args=2-tha2x2kafy-88vdzq7-84ziquxxk9mybxw2z kfhl7ws6v
  - Log entry 60860: process socat pid=13862 uid=334 src=21.154.192.117 args=ga// pgagkh2id7ui6jpqvb7st0/ z3ct9ijergr5/y1icnt
  - Log entry 28553: process curl pid=4902 uid=184 src=210.33.170.123 args=hi57uzqps70 5t pjn82-4g8a5jbydxkj0w4mxaomgql g--
  - Log entry 10139: process sshd pid=29061 uid=754 src=39.209.19.140 args=opf44acafx4d3xjigh5ydavm3je4m er4w bgnyn6x1dmorb
  - Log entry 22620: process python3 pid=14329 uid=280 src=152.37.56.28 args=5qcubj6 n4awv2gfc-dcl9yj52wnwopd3fx 8hk9205-z3e0
  - Log entry 81758: process bash pid=15452 uid=633 src=183.29.116.59 args=2k 9urjjxc83gfpyd1b3g/lxlu2j6hpu7mj22y3f/0kfhlb/
  - Log entry 17731: process ruby pid=10386 uid=630 src=14.4.14.185 args=3e im3m5sgbketk-wy5yn7knxl-z/vjbf1d69dc6hsebpyn-
  - Log entry 88800: process bash pid=27778 uid=956 src=174.226.66.142 args=2ovtwq4 e8qte2cysio/p61w84v7nrjbpn r/i8 nc271c6i
  - Log entry 87465: process bash pid=14686 uid=282 src=53.210.189.53 args=uckls/eyh/8k3qa9oaajs5ibr dfg8ze8ek831tf0amfin18
  - Log entry 73699: process sshd pid=21516 uid=442 src=62.88.219.83 args=ax4688w-fewvjmqub 6exkywpiim 7i8ceiuo8dj4379afrk
  - Log entry 26383: process bash pid=29857 uid=89 src=107.91.139.40 args=gmuqfmkmqx66178-75 xzm -tbyma30opgmhgt630zvsd e9
  - Log entry 42745: process sshd pid=22979 uid=333 src=103.87.52.12 args=/kw2 wld30p03q r 01gcw0feklk-py7gb58aau5oa1pj6on
  - Log entry 63446: process sshd pid=17323 uid=285 src=128.208.107.67 args=k8dcyblud8vx/in 93feugl7az/0z8687d-7pjagc0nzhgqm
  - Log entry 11339: process perl pid=16003 uid=251 src=150.245.26.139 args=k4-bzjmwtyyu1lrp73yr9jubgc1aq76k24t/lftf1rrdr/il
  - Log entry 43391: process sshd pid=15574 uid=991 src=195.125.117.109 args=xfupdo/apyh85wynliu7dun5j1mogsz4qz9ies1jzm3xkd7s
  - Log entry 75812: process socat pid=11749 uid=824 src=60.237.99.223 args=25pm9vv1mloj1sf5go/x2n65747vkhdi3ucj8sf5jpyfv2vl
  - Log entry 24749: process sshd pid=18664 uid=975 src=108.192.149.144 args=bbd86v32h092-m9smjz1xrzw5ihjn6bx5gvhwzqw0jjd6y3n
  - Log entry 36764: process curl pid=22244 uid=601 src=181.124.148.232 args=z7n3sz8y017hpivtn/hd93vobujxfhrc k48dm4nq1o2/e2p
  - Log entry 36389: process bash pid=16877 uid=902 src=62.153.24.43 args=g-p/hxrm9mfva9/teqhj57/ro20pefkdvj47rww66s95bd u
  - Log entry 97732: process python3 pid=16515 uid=443 src=58.5.41.248 args=tj-dhlpd/owtb imsizjwhy/27ftj 2afxdaz0aya8ieryq9
  - Log entry 16592: process sshd pid=5543 uid=937 src=43.95.242.187 args=hxkh2o7htct9vcw- kv52lxuikn4on9w1l45q4lf x7awk27
  - Log entry 58077: process sshd pid=8176 uid=184 src=17.51.84.62 args=u51m/ 9kd1vg5hzfiijaezpi8a025ew511l5llb61svtqd6j
  - Log entry 72548: process curl pid=19007 uid=326 src=152.102.224.100 args=4b rhdft45c7/7o1chu03j4h iv-h9eiif25u65fey04ea-y
  - Log entry 12234: process perl pid=6122 uid=462 src=137.97.150.100 args=grtkf1xbnri-rj9q8vzdn0zrterqku2jeopv6opxxln36/90
  - Log entry 78146: process ruby pid=14387 uid=96 src=110.159.179.178 args=0ui7cux0/wmpegt gl12ybp6a2x0xjd-txy-zj-s-f gpcap
  - Log entry 59972: process python3 pid=29071 uid=698 src=130.101.1.154 args=143g7cj14iygtghn3t07gomqeuzu7o-rea8or3dipb25mxec
  - Log entry 47900: process socat pid=21370 uid=102 src=63.142.74.234 args=8hu8atld0rxk3672eqx94p2ysizg5eti-d tjsaqna /nu55
  - Log entry 18946: process python3 pid=22249 uid=811 src=89.174.230.106 args=2flj7kl6srxlt9qoupfyay4aianpm0ol2jlvd8gdzhq3dsh9

## Supplementary Technical Detail — Section 31

Automated correlation engine identified 19 related events in the 6-hour window.
Baseline traffic on port 8033: 2 connections per hour.
Observed traffic on port 4444: 64 connections during the incident window.
Statistical anomaly score: 0.830 (threshold 0.750).
Related CVE: CVE-2026-48462 — not yet patched on 14 internal hosts.
Affected subnet: 10.9.2.0/24 — 5 hosts in scope.
EDR telemetry: 4 alerts suppressed; 2 false positives removed.
  - Log entry 52648: process sshd pid=10828 uid=836 src=220.150.86.129 args=0hbnpzu1i1-655u6 v4mt8t73wqaxvbv9mmbmcjtrq/2b9y5
  - Log entry 96854: process nc pid=8921 uid=810 src=38.88.229.117 args=c b954tdhcwsbir9ep99hre3 grb3esva34z3aqyfx7gzrx2
  - Log entry 96221: process python3 pid=22774 uid=698 src=57.3.223.165 args=o5vwkjmj7lbzhiknbu6t9o84q3b1dzi12kp2fkc2iuxdfysg
  - Log entry 15815: process nc pid=30788 uid=927 src=132.115.120.141 args=ef19v1haoh5 cee 6vlv5w1ysh68i -d01ob2crtzih78o32
  - Log entry 25420: process perl pid=19847 uid=1000 src=188.165.158.9 args=prt/81/onq1p5lqm gb46rqf0rr9sdyqkshghd1zowatki70
  - Log entry 11937: process curl pid=7202 uid=536 src=69.40.95.241 args=kixtsrw89n5be-vy-ua cbc6fhr306nm 5f3mwb9zp5p18jw
  - Log entry 20245: process socat pid=21985 uid=977 src=204.93.204.26 args=fhzc8h1s8be9lc0ssdxm h2b00f198qjm7j0sl2k4b3sfro5
  - Log entry 81297: process ruby pid=2587 uid=868 src=6.38.135.6 args=/4yvsg81ewfnqrghjcge7mj6efmk7k8wa1jcg 4rg3 qpsum
  - Log entry 96369: process perl pid=3869 uid=413 src=160.20.97.150 args=-t858mgz06 ynvqw6vmlyw1t737d16ltm va2jchjctemr07
  - Log entry 66989: process sshd pid=19251 uid=646 src=135.237.201.173 args=phy/hi8ovsu9ay0ic9- qzk6ogvu5sst0i4s3e0 ixspr265
  - Log entry 78790: process nc pid=10130 uid=1 src=45.208.200.184 args=-2738cdg-uawpdha8qso2h5yfms-wh58vn-oma67vbfu5m8x
  - Log entry 88650: process curl pid=26746 uid=906 src=105.21.96.54 args=1rx l egrvq9k3e6r7r04sl4t0ukes yx8leaeecj8vq ocb
  - Log entry 25995: process wget pid=7448 uid=71 src=78.186.147.113 args=maku2wommqazdcelpcso/5ydc65enldhtgw6tkxe0lwoc36n
  - Log entry 78065: process socat pid=16930 uid=464 src=143.155.194.62 args=g0hcm--mwdepwjwfw1uhntestpslkj3-hxrff944-/e4 r9o
  - Log entry 26434: process sshd pid=13735 uid=348 src=208.63.136.215 args=1owhfxup2x-ack/l8c 9ccjcm6b/vbeaivbie81s 1p6k-1v
  - Log entry 47052: process socat pid=28644 uid=805 src=34.201.232.238 args=onqp88q13xp3-rduxi8nc 7-4enjmapywz0-l- mu0t3kxk 
  - Log entry 35263: process perl pid=27929 uid=776 src=172.25.219.219 args=dzeyxx0acx15f5z2/129/eny/3547xjtw9b/-kp6m1bpgddl
  - Log entry 35905: process bash pid=22854 uid=101 src=63.153.43.30 args=18r0bb83qgtlgmf7m/hfutzxe1kajzmw9m-jdx0n81d4uhqd
  - Log entry 68937: process sshd pid=16788 uid=30 src=214.24.56.172 args=067q4matyg5ut5l3lutqyy834xxzs6pjhwvpvh1vk90ct7k9
  - Log entry 32240: process python3 pid=1603 uid=901 src=122.60.189.168 args=r54f10el03xsb/qjbc0bgacgff6yg1pgpx-io97hth4mzw1q
  - Log entry 30184: process nc pid=16394 uid=116 src=36.220.42.7 args=4wud0-pdly6oxe4q5/vx 4q/-xmy gj8nzzg7 koalwgymf8
  - Log entry 60603: process ruby pid=15708 uid=603 src=92.169.226.101 args=sobgbxh1vf3xjdkok1lyqkw4zyn56umcatbyn3r-zmmgl5m0
  - Log entry 93744: process sshd pid=11605 uid=509 src=30.157.150.246 args=24l9dr6-s2f5gcwkvc0tuwzplna97vk-ce24p2jh/jj1 l2s
  - Log entry 91420: process wget pid=28299 uid=571 src=201.22.100.233 args=-ltk2fc05 joww94kl6x7r8v52u8k2l9hzu8m78su4-8pfyt
  - Log entry 29547: process python3 pid=11308 uid=740 src=200.160.190.131 args=gy9/xqgr5eyhf5p47oadwnbi/-usboq6zka-lx9rdz2x-9zp
  - Log entry 91367: process wget pid=3694 uid=41 src=111.115.78.66 args=n7k1g7846kzx82 sdf9pia cut5h3y8wpma3l56bi4vu/b/e
  - Log entry 87835: process bash pid=3654 uid=704 src=174.67.188.13 args=bl/u1fpjp6kw54ok9a1hwezk4/1c/viuc8dwcajqzr x1ds6
  - Log entry 55591: process wget pid=22985 uid=842 src=37.234.126.153 args= 3/rl-mn2m6k14aqffvs/q7rh7elayozd3t5c/3ejugigr/c
  - Log entry 65967: process curl pid=17469 uid=67 src=191.9.193.251 args=ft79c9d6gc/v/idx 9lzehr0naewf 616zus/m-8c41a2wg3
  - Log entry 86542: process nc pid=28151 uid=939 src=14.56.155.214 args=2/ym4a9ah8/nwrtcq/dlqh7//kqx52htzsz785uboted3ku-
  - Log entry 10852: process python3 pid=23645 uid=929 src=97.90.172.52 args=916quk/fxajnp7jd-8j wiv-r1oe4nxwphi shx679d zsjv
  - Log entry 19360: process perl pid=6055 uid=504 src=104.153.1.179 args=-6 1ywdhf2mmkopq1a79u9-ivjlk2sonsm-pfnrwdwh6ne9q
  - Log entry 98131: process python3 pid=3286 uid=863 src=66.113.14.199 args=/w2h-3-9apzd0jlaw6ylit7b0vy0/zrx5375iv jl9wh7ak9
  - Log entry 95210: process wget pid=23367 uid=319 src=214.227.4.174 args=a00bxaxjbzx whaqc0yl3u o ze34a7kei-erq wj6jqfjbd
  - Log entry 32703: process socat pid=3797 uid=274 src=206.0.66.73 args=v4zj5q65u q82koag/dzjviant7/lam-g57xp-3rsitleznc
  - Log entry 57129: process curl pid=21215 uid=499 src=49.27.122.207 args=e8xpa/u1uj7wcm4dpuxp/-2hscm ndrnh40trgzh1o12lzj0
  - Log entry 65235: process bash pid=30596 uid=353 src=148.24.253.108 args=uxe0gyq06250x4uk6opkd23jwfizut48szkluuhi9i5rn4s2
  - Log entry 34838: process bash pid=22001 uid=499 src=29.212.37.58 args=xkguzamh17c h0r40n f1 83e ide6d/gwjnhxjfj -m /4h
  - Log entry 10059: process python3 pid=20915 uid=20 src=74.242.169.24 args=tvjs6wd nzazqrw1ghnuuqb14omtja5zef 30mr76zr1xour
  - Log entry 46541: process perl pid=23484 uid=170 src=59.128.189.48 args=vgbgt73b1upfs4k6eyf2a2izn9jbbu85bt e3i/34j/rqibu
  - Log entry 23843: process curl pid=23509 uid=338 src=153.176.47.234 args=dlyaivjy6/cqp9wblwu6kp6x441cx223/v 3cnqa3orwh/ne
  - Log entry 41170: process wget pid=3308 uid=664 src=79.142.16.67 args=wr-ihc7m9jfymqtesxr8/eh6hoee3omnewy262baax8jkkdu
  - Log entry 94460: process ruby pid=4831 uid=661 src=179.23.79.234 args=abwr5j53n 4k-qqlsi9ijo/e/-6-qvu84nyza41eut9z 7eo
  - Log entry 47443: process wget pid=1044 uid=374 src=171.44.131.160 args=lfsbyyif9i700 n2uphvy 8f-/6bkm4-jzn18n4llabeuzl-
  - Log entry 98672: process perl pid=19573 uid=820 src=129.27.100.55 args= nay5r68odfzp-f6qh4imp3/bzomz0mslras24nq/aq337gc
  - Log entry 27642: process nc pid=18165 uid=223 src=84.74.81.228 args=x34t3li//y7sc- qex862er27-rv3mqwjnrpru4sh944guy0
  - Log entry 69763: process wget pid=3193 uid=249 src=182.154.142.53 args=-y69yakhxnddwmrstx0b/1yx6tyvhl9qq8vg90q2  ppvfoe
  - Log entry 11948: process curl pid=4749 uid=99 src=17.22.245.153 args= 2przu6i-8f-ji4sea5ezr7d2xg04qnkq7 vt0f38dvt476m
  - Log entry 40435: process ruby pid=1163 uid=255 src=191.13.11.99 args=pm9l-d5p53jjpwntuqu1j88aqc1u hml2at0hq79 iu186pe
  - Log entry 17171: process bash pid=10315 uid=654 src=41.240.43.239 args=exmlc3hghvxjtgnxcqkdraujytixk1mkv0-se-l9uz30v1gq
  - Log entry 57528: process nc pid=28804 uid=632 src=138.52.174.155 args=wr1161o26h6j-7vhhdv5wjm23p45/dzbx78qp4lko-a368p2
  - Log entry 46115: process curl pid=31639 uid=122 src=85.23.33.109 args=er3z3sn2n067rg70gwfottux3it5gollkqd0ng63p0zefw16
  - Log entry 67696: process python3 pid=7106 uid=66 src=173.180.159.180 args=akc510ca1q9un1uxk 9va08y dxvmsbe7 3behft0 r5aw9d
  - Log entry 61883: process nc pid=5371 uid=363 src=49.124.114.218 args=zcrmbu5ijxtqmh2cmd44o0-n5srg6d3j7v9d/mjzk6/z2kyy
  - Log entry 99844: process curl pid=5452 uid=452 src=152.91.254.16 args=/1izyg cfqoa  mqjsrx750wyopt2flvs5sxr3tnkp4edxwm
  - Log entry 66977: process sshd pid=6716 uid=953 src=197.175.45.132 args=hso47i/m w4jcol5 vqkw7ltanqwht/8nvwpsyxzif9r88z4
  - Log entry 25082: process nc pid=17059 uid=959 src=57.163.67.104 args= jocajoyxou1tvo03r rf23i9-pp5/a2aegtlk7f73q1bvlc
  - Log entry 22068: process python3 pid=4119 uid=223 src=87.0.198.29 args=wmqy4k8xllbw0/qwktiilcmbwsfw1l-wrcfoh1owntj f7bq
  - Log entry 86374: process curl pid=16062 uid=820 src=17.127.145.37 args=/73ozo8743ent7x5pz/7n8-hhkg d-89-rjmbtt3pj444tlm
  - Log entry 60609: process perl pid=7829 uid=734 src=123.197.28.100 args=6qkh2tahzb 4k5dooyvc/af0535ruc/eilg28c7xcrktb2ii

## Supplementary Technical Detail — Section 32

Automated correlation engine identified 17 related events in the 6-hour window.
Baseline traffic on port 41929: 4 connections per hour.
Observed traffic on port 4444: 178 connections during the incident window.
Statistical anomaly score: 0.943 (threshold 0.750).
Related CVE: CVE-2026-27417 — not yet patched on 6 internal hosts.
Affected subnet: 10.6.2.0/24 — 5 hosts in scope.
EDR telemetry: 3 alerts suppressed; 0 false positives removed.
  - Log entry 90430: process wget pid=19764 uid=225 src=50.203.211.193 args=cnve7wccf9aufti3 3 4p22j6o2iw3dngg/3s8-eaudd4x01
  - Log entry 39674: process python3 pid=24329 uid=547 src=168.221.145.192 args=a1u/o05rh7 7cx7-diovz5a2 uy5jv1d1fkfp9r6-g0zw4ey
  - Log entry 17855: process wget pid=29419 uid=407 src=153.46.216.11 args=xt6o-ctaeoh6wnak1s1hcyzg3dbvq5r77acfnuq5n0/-9n/f
  - Log entry 36708: process bash pid=8682 uid=802 src=213.156.183.49 args=rp7je6 41z45kza3ke7zhpv 6d5fcddwsgs-82ftw--nh5i8
  - Log entry 64695: process wget pid=31250 uid=375 src=80.158.110.174 args=-ksncxo0hp2tmkvpl7urn1wdgb5aqmmrbal12mnwz9i5fc0q
  - Log entry 59662: process nc pid=16597 uid=725 src=17.18.220.212 args=vx-b6rlg6hj9rjlf0 i7nu1v6zuti71wvm 20nyf29acbw/8
  - Log entry 86906: process wget pid=4442 uid=859 src=86.208.245.228 args=hf-r2hu8nncul4fog3ak6lj3j -9rns/mro3589423e8g44l
  - Log entry 99428: process nc pid=4109 uid=324 src=152.25.171.83 args=4t9u2jmn2s8ilfvyqw6cns265tiugu28d7bx5h- f7fhi98u
  - Log entry 96096: process bash pid=30234 uid=461 src=23.19.229.77 args=occ7avn1dl1os/vgyd6i5k 2aijj-u9v/a3z-wf5-jxw9suo
  - Log entry 16002: process socat pid=31850 uid=358 src=29.6.96.184 args=1moqlhf/qswl1qrje22 a ji5o0osmu9-6067-psc8fel19o
  - Log entry 18617: process wget pid=24823 uid=564 src=40.154.45.62 args=p2bcwbk638-n0gpg d sgl8srj2mgtwfyqi2m2me3shaif7o
  - Log entry 35089: process bash pid=31184 uid=460 src=157.95.191.29 args=u36m8wssm/dw4t0pkrb12ifthcnc8l2xq9pjr0e10dyyvzs4
  - Log entry 74957: process socat pid=4849 uid=858 src=159.33.230.228 args=t38z3gg3i720293 9c g3elo/3621oif8bx0/fkxrkpo5d8l
  - Log entry 38005: process bash pid=28925 uid=43 src=102.83.135.167 args=gxx6hbu0fevqvlwy-r04ffqc4-mlg-c2ctnmgec4e-9o9ynf
  - Log entry 74375: process nc pid=8750 uid=951 src=160.157.7.57 args=wkzfo9p3772yt9s4btcyn9 1ipb20e85vx84vvl537uuc-7i
  - Log entry 23228: process bash pid=29369 uid=112 src=86.146.154.180 args=34 zd92gipygnb7fg 3z i5w7j08bz1-e wjfoq4 4ug9603
  - Log entry 84452: process nc pid=7229 uid=253 src=22.143.142.152 args=f744/4rnt8py808ca5i60/46v9972htv9wmdh-80/vjkdj8c
  - Log entry 65820: process sshd pid=11970 uid=264 src=71.49.98.4 args=ldgjvsx-sv12v9vxndvyahr-6mc/5cboyslmmk eubhtpko9
  - Log entry 97950: process perl pid=10354 uid=234 src=176.7.1.180 args=n21pnj5lnr9h2upg8f7pp3/9hivtrraxp48e ya7wygvqi 6
  - Log entry 31062: process python3 pid=1453 uid=268 src=166.133.20.72 args=fwajzpb2e35qgo9n 3f878g0w3ll8ex/04k/ d5/32fe1rnz
  - Log entry 37384: process curl pid=15774 uid=804 src=7.174.206.12 args=b35oq-rx49ldiejigi6xve4m2dyx67nq861-p0dz891ks1ya
  - Log entry 75258: process nc pid=24844 uid=206 src=167.55.188.98 args=io7au9vzzeotbg5bqvil-l-ja7-2cwq1anzg mpeyntxm8l1
  - Log entry 73790: process ruby pid=6912 uid=723 src=15.176.212.101 args=9x k51-vrlv5cv4 /2e6vtrhg4yrzm-f7cajns/ffr067tvg
  - Log entry 65615: process sshd pid=26657 uid=797 src=203.5.198.234 args=scjx7oafjr3973swcmhuxnualir0rl0wub69qzbggsm3jecr
  - Log entry 85657: process sshd pid=9131 uid=395 src=4.21.81.225 args=pxezn3kbo-xykfgz3nqcuyzeyk90clppkmmep0w5w//3n53g
  - Log entry 42517: process bash pid=9190 uid=994 src=140.137.34.99 args=zzfao15p21y6w1m5-lj148dc-o20tx/vl5jezfm2rsty2u/s
  - Log entry 94068: process ruby pid=30354 uid=358 src=191.160.138.72 args=36cvl2wkcd9eke b40qr1rbjv7rbhx96tnq/-wkku7 f1i2d
  - Log entry 97596: process nc pid=21094 uid=352 src=9.202.55.189 args=k6hufkk8b75gev73mvhvdp/onhy16ln2c40l lrq3cph139b
  - Log entry 83734: process ruby pid=14712 uid=545 src=192.211.240.73 args=1kat6mkhnv2m8wdxx7bpxob-cjmtpw ntxm/2 03dqu/xcur
  - Log entry 77972: process bash pid=22836 uid=229 src=223.60.66.154 args=p20dgfoow4pfyi7nfzbsllszyrdg8mg518zufle-dq03s/v5
  - Log entry 65694: process sshd pid=11278 uid=770 src=48.140.129.232 args=o-7u9s6axjstc7c9l-9g16zpr6rn7/3z0kk3t7xdielpd2m0
  - Log entry 99362: process ruby pid=16654 uid=951 src=49.244.191.109 args=er4dwo/q3x2urxjbl e-9dnu/gkut10k3qkpmh 3dnnp72te
  - Log entry 78755: process ruby pid=24938 uid=400 src=194.115.183.253 args=nds4d0ukzp5vwzp-um873vot3fypiy/jk064yisjvms7r0xe
  - Log entry 79739: process sshd pid=13751 uid=257 src=166.209.71.141 args=l9nrr5f4rgl6r7dln-v9rh18k/8g7q0halx5a14gj1socjfl
  - Log entry 28001: process wget pid=1967 uid=704 src=99.174.119.83 args=-wurxu/xok/4c1tez1xwtvj26f/0e8uae4crn-w1m6w2wzoy
  - Log entry 12521: process nc pid=18174 uid=998 src=145.111.139.35 args=lix6b7uesxb11n1qam7aht24t9n81amjg1xy55h5kp037p5p
  - Log entry 77871: process perl pid=9803 uid=207 src=168.217.204.98 args=ypg/fejp5y1/-7ep-fbhrkud9/oirmuhznne215f/-y4lufn
  - Log entry 16791: process ruby pid=29474 uid=419 src=175.162.12.189 args=fm-g28psh-kfx230ldc6esxzu05b1u312ms0r 3w1e-cq6q8
  - Log entry 31807: process nc pid=1878 uid=723 src=85.79.46.40 args=h5gdh254whok0jp5bi7b42kpsa9n7xcls0 ttfjayx6jb9cc
  - Log entry 32395: process socat pid=23113 uid=414 src=125.209.84.231 args=9b7u4fjknlpbolhhj4d9ozkbegf0mludiwp5hvw5zv1med9k
  - Log entry 26527: process nc pid=15265 uid=102 src=134.196.116.28 args=7j6f4/tw/zw4uiqgfmg6ywk2ak00i6s8j9f /pg6-mihd70f
  - Log entry 68645: process ruby pid=31519 uid=126 src=44.106.45.12 args=m36e7vrab1tljho6p8wemvfn1vm33xb4x8 ot2b s0td57ol
  - Log entry 71218: process nc pid=5596 uid=398 src=141.251.7.238 args=utb7ioq21b9fgtgkkh ift39cktchd/rzpvxx0sd7bnq29cv
  - Log entry 69371: process ruby pid=24634 uid=973 src=95.137.239.194 args=isyno 0gsb/yc15o7pvfm6a6fpj8gijm7fy8lc6e8gyyn//a
  - Log entry 37965: process ruby pid=16022 uid=560 src=76.237.153.155 args=nxq80 ynt/kiefxiq0fyv/ep5sfc71e6pc0fgv 8yq6xmk3-
  - Log entry 71117: process socat pid=6031 uid=417 src=183.146.97.83 args=bmfadz-j3 hoc1-aod24lvke2jd5yrlve4n4 lwm070w-bgu
  - Log entry 27562: process curl pid=9812 uid=103 src=110.68.146.240 args=7yo7rom-iv 9h-5i2fc0694gxu84pu7z32pqi0e-pwz8mkhs
  - Log entry 27095: process socat pid=3440 uid=517 src=129.230.22.246 args=ji3fh2fppg4w84fgx0kyhy/96whwcm1casc1uqfhtyvkphv0
  - Log entry 23997: process ruby pid=10159 uid=627 src=200.244.177.235 args=-iz2tm 7hf3s-/7wia-5onoqqrrm0bip r29 1ldgnrzkfjk
  - Log entry 31796: process python3 pid=16213 uid=246 src=122.103.233.84 args=05co2kh7d1cw61cx54xn21s0w8mx /30b/d20p2v 11ib8im
  - Log entry 96625: process sshd pid=5175 uid=409 src=112.188.37.195 args=41n4u4q59aam-e33x0pqhkjhqrjfdilx8v1m-w-4bgurjmyn
  - Log entry 45138: process socat pid=18686 uid=157 src=134.7.85.226 args=k9u4inj7o/6c8gxvlbekfdlxa24am1gtvl7fw3dbmp3gtzb3
  - Log entry 20144: process socat pid=22690 uid=912 src=182.233.215.33 args=m eziajuo sbe-3k-z-s9hw97bson5c0w-yxw/kqjv3thb6f
  - Log entry 30397: process python3 pid=23762 uid=103 src=77.82.4.64 args=2r69v6miiore9f111qaqdn9im1hfa/p/c8pmavxhg v5jrrk
  - Log entry 21487: process socat pid=29235 uid=179 src=64.63.89.213 args=w32p5j-9pou5ch7bjxf2t1fsg231w5ozrxsw-60rfjgn46h7
  - Log entry 29067: process sshd pid=29935 uid=638 src=149.97.191.232 args=s4mt65-ztt-i7h9bbzr4mg1wwjhnb6fpnt/ mymhtjvqr719
  - Log entry 19283: process python3 pid=4504 uid=342 src=41.251.45.141 args=0u9g1olk/jvj/31ua3vdbbihaw8-89gqgn4-slwmmczco/yv
  - Log entry 30973: process nc pid=31946 uid=480 src=188.175.90.45 args=yunoti3ekxsxw/9womy07fqlprmdets4byub2nr9f6ym/ibk
  - Log entry 83694: process ruby pid=2355 uid=249 src=153.97.199.190 args=1lzq6i7drwxlp9m-da5ca6s92ubq3w/knwlxlwnz08cfysj0
  - Log entry 29146: process perl pid=27840 uid=76 src=43.144.172.226 args=ctzcqzjg egzup6q3zp/xceaf/miseg9-08z5dt342oc6r6z

## Supplementary Technical Detail — Section 33

Automated correlation engine identified 23 related events in the 6-hour window.
Baseline traffic on port 45879: 2 connections per hour.
Observed traffic on port 4444: 53 connections during the incident window.
Statistical anomaly score: 0.900 (threshold 0.750).
Related CVE: CVE-2026-33616 — not yet patched on 20 internal hosts.
Affected subnet: 10.6.1.0/24 — 17 hosts in scope.
EDR telemetry: 2 alerts suppressed; 0 false positives removed.
  - Log entry 69940: process wget pid=14215 uid=277 src=124.120.207.144 args=08wosoa2-t9o2j-vyqt7le09tczt-6dj95r8q1-oxzish7a2
  - Log entry 69530: process nc pid=28088 uid=60 src=111.148.83.149 args= /5va oldqqla7fnemlktxocjgox3apvyda6gk1xt36cxfs4
  - Log entry 67299: process sshd pid=15367 uid=92 src=152.41.70.9 args=h/d-ck8hbhjg7i l-8a7e5ocskzdu89te7 e-bkz8rkn1r-y
  - Log entry 37966: process ruby pid=8924 uid=48 src=118.172.228.26 args=lsud 4peo5dr-td0u9cct5et6o4 7vfwoattpmud7bu3rg6a
  - Log entry 32192: process socat pid=6797 uid=643 src=103.212.104.38 args=wyuw-bsyj8a9i9ylgcn52t/3qmnmb1- goylkbam7-pvvpy3
  - Log entry 52872: process curl pid=9332 uid=17 src=83.85.194.228 args=4ugryi9q22a932v98ku-zklsh0stldn 06qqi3j9k6qctp/q
  - Log entry 29141: process ruby pid=13067 uid=713 src=95.190.216.196 args=sye1m1fgkc8a8p7u9-myel6k w02ghwqf7-x2riipfyo22-p
  - Log entry 20183: process nc pid=28014 uid=624 src=204.164.73.208 args=sim38gffpuyqbkt4d5k3 e8ws-ge31vumw4xlo1x60g53y h
  - Log entry 22852: process bash pid=15570 uid=403 src=142.24.130.200 args=v3ovc4zaek086p0r- n- i1db/h-nhk30yc/f-uhbkw1l/-t
  - Log entry 15766: process ruby pid=9605 uid=689 src=30.30.143.189 args=qkpjic83m7nudl1qbjs853698575js3j784me-l9a5zd0y8t
  - Log entry 65157: process perl pid=30472 uid=198 src=152.178.231.221 args=imkx/73n77ztfp4qcpj 79pqgopqoc6blxqllfmxir7n05s2
  - Log entry 69751: process curl pid=23979 uid=201 src=3.148.193.118 args=dhyjrsw7vt3 4ka1ok w9pkhde7re3p-vei95wp x4j o28q
  - Log entry 99657: process bash pid=31954 uid=493 src=210.180.15.160 args=uvi4brhyfq33d-3djnjth1jfbjuwh7hgt9nt8yxzsdxztcmq
  - Log entry 11234: process ruby pid=5736 uid=361 src=207.25.228.39 args= s9r72qk3kfsn 3npdwtbpr6s-2eweweq/ypyl3/vyq1 etf
  - Log entry 86470: process sshd pid=23518 uid=228 src=59.156.32.135 args=wg3sxzk7jck -z/1v193-ph1uic /nqeasomxbp0ygrv-q0q
  - Log entry 20605: process ruby pid=7862 uid=293 src=184.221.108.77 args=73-fqy0ypgbwp9ghyv655h9jlygmqnolh42hv-ki9zk2c-cr
  - Log entry 96077: process curl pid=31411 uid=889 src=59.224.249.171 args=/wbjal/o-z04drtxrod0kieg44n8zk7ws6hl8ylmfr09hojs
  - Log entry 51548: process curl pid=16482 uid=458 src=105.136.246.240 args=sqsa229plrn7onamubfkvz /3vp71lvrg/c8xtnh4-9n69je
  - Log entry 14091: process python3 pid=17690 uid=129 src=56.44.183.105 args=t n/4d n6y2q7pydygbpmfj-u8-/subs/2x1ndowimq/k 3x
  - Log entry 50539: process wget pid=12244 uid=589 src=110.191.187.147 args=adcxgyqmqu47t3gm5-zn9cwf47spem8nxh1eh7-ezi/pkqgs
  - Log entry 10403: process curl pid=1931 uid=987 src=3.229.94.172 args=n9tey5bfv2khq2/-k35l-rrue-3g/n2gp7fpznictzerbk-n
  - Log entry 86457: process bash pid=29186 uid=934 src=198.143.35.238 args=hch9/e37vm08o9y95ztwsiz-7aqzhz9g1tz/fbr8dwrg34pw
  - Log entry 46543: process python3 pid=28871 uid=872 src=124.93.27.83 args=lgnpu92/krpe w0sptn2b6afrmtwcd4juk12vo1le42-taqs
  - Log entry 21167: process curl pid=7146 uid=758 src=139.5.51.89 args=xn1vzdnzcb7ec7u5a3pc5r5-/e eb74rppyo9l6x9s8qv41q
  - Log entry 63414: process curl pid=16068 uid=700 src=154.60.228.97 args=b/8/l603 dp73so68w/sx7-ute2jmh9-1-tay61u9s7sg3m8
  - Log entry 50826: process perl pid=27835 uid=599 src=59.14.56.152 args=zsl07r67knadjgdok0ha14c- gv8fir2csmrwbx1q2/n3wrt
  - Log entry 94092: process sshd pid=10852 uid=149 src=98.94.255.127 args=8tm39tgh4oz ox7w4nzjwhjy0nqje3l3cm7zjgjtsqvpjtze
  - Log entry 93615: process curl pid=10278 uid=195 src=25.174.77.251 args=dd44x0ler k-izs45 jt-sm7rq4zuis93g3qbenyq5nxey4f
  - Log entry 37112: process bash pid=25819 uid=264 src=176.128.187.220 args=hnabdejvb q2hn2xer/pw96-1y1-2j4eow2ryqh87ggzgjcm
  - Log entry 76203: process bash pid=26785 uid=6 src=100.185.130.250 args= bgpgtsr11yy9b2es7yrkuzz0znttsbgxdd9ht3-theq y0c
  - Log entry 97483: process ruby pid=24290 uid=608 src=146.189.143.165 args=59-rn6hx z4u7od11xg4m0gngyo8l5u0q2qz785oy x-dj-o
  - Log entry 79423: process perl pid=26885 uid=199 src=114.207.249.17 args=v6nvgmt14q paj2yga5/z1op5udvr09vxtytcy5tih91kh6l
  - Log entry 66389: process socat pid=13242 uid=548 src=47.95.61.198 args=zmf y/fgo-  calsh0h19iqqw/6aqilc46ajq797at722mxd
  - Log entry 87483: process wget pid=28197 uid=887 src=180.138.20.214 args=yva9lljaeakfsgvvyg8idow/xpywvl  qscfs39rn8f4-rb9
  - Log entry 97796: process nc pid=16734 uid=583 src=218.44.108.24 args=ydh3kaz6e2emi4bs3unnu1y5sn2iozwqz3v0u4rym4/uqsrp
  - Log entry 78503: process python3 pid=19511 uid=875 src=120.28.30.2 args=k5oagj  h5yeg9tjlnkb1l98yameo1nf3m8wh6-164o7q08l
  - Log entry 86569: process sshd pid=7978 uid=542 src=69.40.105.25 args=9zy2 nnoap12wudbdgzi6l7nic6314w1s9s8x4oxkh4x59e-
  - Log entry 10374: process ruby pid=18803 uid=774 src=92.111.69.70 args=kcdy/n0md5bk1bqrup-jnk73dirltq6cq/3zmbzs/8hiklf 
  - Log entry 65841: process python3 pid=22629 uid=454 src=35.179.227.83 args=7y7ng y2ansyhjmz4l4hob5yznq73f3 jdq583/ro4a54wwa
  - Log entry 68123: process sshd pid=18510 uid=287 src=120.17.72.184 args=-46uzbjp9ag2npbbm-mhykcekrn4q0c8msnk186cew5o6qcg
  - Log entry 25987: process socat pid=22747 uid=427 src=56.67.11.178 args=g76552nzcxarupocbc9e6evc0e1xknjuk01p5roqcfofc fr
  - Log entry 16666: process ruby pid=14096 uid=657 src=130.129.9.250 args=2 xhp8aby/x 8hja63taflprcx/nekg6bg3h7y6c3uha2wyy
  - Log entry 85741: process python3 pid=18010 uid=479 src=202.62.67.40 args=415xkvy7e4-z3xv rywk500/-jvhkvnqibpwczsv9qtwep8f
  - Log entry 10095: process perl pid=12500 uid=356 src=94.65.59.18 args=5-7y-qtfmkca8mprwet178kjju4ehwu12dtxh/2mc22n491i
  - Log entry 88604: process python3 pid=8226 uid=189 src=45.163.145.64 args=g9il88b -uka1hex1p7iuq77sxht56b1dqqq6uxtb-szoeww
  - Log entry 21814: process bash pid=23707 uid=120 src=180.216.32.58 args=fe4pd1ux2d gd6b1zo0ug65ykrywqv8zu-ko173l-q5ht-vy
  - Log entry 64725: process wget pid=25330 uid=950 src=28.227.142.94 args=zqajpn5l1jm4h4cnnvflbyqjyy3ijhlc-3o/p 093gvkd-rv
  - Log entry 95709: process curl pid=15601 uid=783 src=210.170.230.28 args=j68r4t1j7nqy9c-azn68a gu1i19qc9rjc3x-afqw/4eybep
  - Log entry 12151: process bash pid=19492 uid=399 src=106.255.20.172 args=zcj17 37ds2rc7cau4k13nev/6zo3jznl2 u2pkdue02qo23
  - Log entry 48833: process ruby pid=16187 uid=353 src=33.97.20.79 args=4z1213ji4h419fgy2u041/5k745o7mxnij4xmy-lm6niy13q
  - Log entry 43145: process sshd pid=18635 uid=464 src=215.205.160.62 args=9-3p2yh 4lga1v8m0 o5vdc2mye7z1mabjmelaj26c0v8qqu
  - Log entry 36029: process sshd pid=5521 uid=109 src=202.26.79.116 args=2v qdhsobeb61z4u7xscf2qdh8g7/yqb0a4cj/q8i/ekgr9v
  - Log entry 76822: process wget pid=31234 uid=532 src=112.39.93.131 args=jza06dr1-v/ardntu7q82c/b5qe/k7f2 wed- 76kvw5o i3
  - Log entry 57487: process ruby pid=7342 uid=790 src=33.145.58.166 args=ggq84ic0tns8r-br2ql3i9x/amua814hfblcc01z4nozjf1g
  - Log entry 51252: process perl pid=17929 uid=51 src=89.8.73.201 args=6b-hhlx u635hvrciy6ur6ha6i05flmudz9hn0uevdftkm7x
  - Log entry 56848: process bash pid=2588 uid=562 src=156.155.70.148 args=u-0gaz58skgx0nuy0ba10nzex-jvp0xt4rp606 z/2e1z846
  - Log entry 76527: process perl pid=12839 uid=794 src=117.182.11.184 args=z0xo/t/kv-zv79ye8y8n0ybntxbr5uqakwtm5tg6 /9a2o0u
  - Log entry 51867: process perl pid=27278 uid=719 src=179.122.80.182 args=/64/yn9br4w-3wa0m-9tn1xojt/uhjz0iawfyx7jqpw3dt67
  - Log entry 69816: process ruby pid=20021 uid=338 src=199.84.77.144 args=ei83hqwo -ln6ypzeuyzl7/4bhe2jlnjr731-5ea2aajpja/
  - Log entry 13817: process perl pid=6123 uid=605 src=106.171.133.121 args=z0dzx1z6vvc62/kpwfszfd0k3wwgfrflfkl5smtdi77r/-ct

## Supplementary Technical Detail — Section 34

Automated correlation engine identified 45 related events in the 6-hour window.
Baseline traffic on port 46197: 5 connections per hour.
Observed traffic on port 4444: 189 connections during the incident window.
Statistical anomaly score: 0.885 (threshold 0.750).
Related CVE: CVE-2026-17240 — not yet patched on 10 internal hosts.
Affected subnet: 10.7.5.0/24 — 15 hosts in scope.
EDR telemetry: 3 alerts suppressed; 1 false positives removed.
  - Log entry 18942: process ruby pid=7738 uid=355 src=172.200.32.9 args=1zgh36uedot2y8do9scwobnn2eh1u2nfqy8aigkeh-a0bvl0
  - Log entry 78138: process ruby pid=12842 uid=35 src=222.102.66.166 args=c4t2bida9d9y1b//wbk5/ aurwjy2ly5p2bn2eb8qnge4zyn
  - Log entry 77136: process socat pid=23799 uid=621 src=105.220.231.198 args=/-wzm9j57mje270z97-guukq726hgb8tpyccc736z59i-qxq
  - Log entry 71839: process wget pid=18981 uid=686 src=163.199.88.106 args=5mu5fnua t8r4lbgeh6fj q4tv96o b/ppbpnc-0nk-hge6c
  - Log entry 86327: process python3 pid=25314 uid=512 src=82.16.164.59 args=-0wo n8ds7gxvsz2-1icgbbsisb7gz-wu3lr5q-zmkzubww3
  - Log entry 25457: process ruby pid=24151 uid=941 src=111.22.216.25 args=96/t8kiqzkxav06loh9pg8oiuiugth4k7hss3bt zt57hr2c
  - Log entry 77984: process sshd pid=28381 uid=299 src=64.35.31.243 args=61/qx-fsiaafyn/jd2ld2-/cys ccyhprsz4pi2d3pe0y-o 
  - Log entry 31430: process perl pid=18808 uid=885 src=94.163.169.94 args=o7kd3vviqbayfzjeq5-qzpqf guiocpo85-o75sbv0h4s6a6
  - Log entry 45128: process perl pid=6410 uid=189 src=56.60.137.177 args=nu8vi2va6lpkvadyhy1ficvf-vbj/6u5vwbn9knjzgds0y7o
  - Log entry 77996: process sshd pid=25033 uid=198 src=21.239.24.180 args=w2kds5iuu28yp0-tjs464wguuh1m3gpi44amnew77e9u53y2
  - Log entry 23605: process python3 pid=8599 uid=437 src=27.140.207.65 args=wgza8ji/x97gciw9o47f5rtb/xl3q35vzh-h5dfyy842cgwf
  - Log entry 39685: process socat pid=27578 uid=907 src=133.13.73.217 args=xnh6nep-q 3uuf ym0w4vhq5psqgc vc0ogeq 8gde72gim4
  - Log entry 19562: process sshd pid=24299 uid=716 src=217.153.224.30 args=v0zoemsv erz3k9ih0x3hc pvxzqxw3i3h6vzo02bh8uoitf
  - Log entry 32111: process nc pid=26290 uid=195 src=201.8.71.221 args=6z gxxw7xa9cgwukx2xpoec3yl3ktxmk29yya01l0cdf1v/p
  - Log entry 53500: process curl pid=23662 uid=218 src=47.87.254.162 args=ajrj19k/pswzu-cxsoibabr9528y73gy1wdc/5e9v5kg7bhg
  - Log entry 36282: process wget pid=21934 uid=301 src=49.66.160.5 args=orizsx//spkekqy z4sd5c4gr3zb7ydwjt14gmgdv/ixj5ee
  - Log entry 18193: process socat pid=20249 uid=858 src=175.39.81.125 args=y85cdg sav7o/e31xyi18knipl4ryqxud6 61/-cwdc65he1
  - Log entry 67430: process bash pid=12838 uid=802 src=44.120.163.131 args=bjf2m2m/pr70wpqxsizuo31v8j4j1elshz/adbtxt 2xxpq0
  - Log entry 84064: process socat pid=14268 uid=593 src=92.38.185.105 args=lc0gr4gzu7qn0kcraigt/ftepvz0002c ehw u6 c1vv/b b
  - Log entry 89561: process bash pid=1490 uid=36 src=162.239.24.154 args=5of9ch1uupbt9lsvaotjesaxp8e l 317kj8zbk-m /9h 2u
  - Log entry 46821: process socat pid=19093 uid=300 src=197.4.75.27 args=zgfhs 23ab0x7m5/jshq-4j/nuwr9ct89ug38ridz dh/d6q
  - Log entry 29133: process bash pid=17912 uid=392 src=205.140.175.87 args=9fwoacsnr 8r4hhhdm8akf3y6nerbyjrwvm0/oqi33wv3id4
  - Log entry 56676: process nc pid=31484 uid=723 src=83.21.67.61 args=v60o4s1ir4d71f61dldw p-1h14iar1tjy50wx3xoq3pxoby
  - Log entry 27938: process nc pid=8056 uid=752 src=178.181.34.96 args=yogx96mnz3fwq94j911delognm/njbudxxsrce3t9ouzg8 0
  - Log entry 17234: process curl pid=21483 uid=11 src=113.92.22.205 args=2m-nekedu0 2s hfptn0drdu9z0/nurr3nr/4ymkosw3-hpg
  - Log entry 51574: process ruby pid=25856 uid=39 src=140.253.230.167 args=im2obox6rlb8e1xs9 o/rj3qujauwo q1myds63zrkl fgoy
  - Log entry 68525: process sshd pid=8651 uid=232 src=111.16.104.173 args=4mbozxy6x mgcdowezq2pehsj74611infenq7klxwl09nv6y
  - Log entry 63209: process sshd pid=28249 uid=849 src=208.66.240.92 args=0/kisykhbfq1q3 gijfoa3pwitr87ir9u3thktbes1trhlkc
  - Log entry 18122: process ruby pid=29343 uid=768 src=218.0.102.185 args=dttk2230hxb/7gg1hd-65/184co7czeovtqr1ce0l2igpw7a
  - Log entry 43983: process socat pid=30319 uid=785 src=69.139.217.98 args=s0hh0p0ukb/vx9svcwylxa9hcxajsiciq8los-21krcs1w4m
  - Log entry 51469: process ruby pid=21537 uid=84 src=15.178.36.181 args=y-rdt5p5y329yar29xccn-z0/g5oxmylbwizwjsiaqz1  22
  - Log entry 54615: process bash pid=6166 uid=628 src=191.160.31.98 args=vu7/-s  81r4zl4jvy zo2h3zx-c nsw65b69x5y-n m5trl
  - Log entry 43044: process sshd pid=9205 uid=679 src=6.111.254.217 args=1l7dlezrevt5pjm3saumaca ci8-05d8s/zq3 i3h junkiu
  - Log entry 30835: process bash pid=26637 uid=18 src=44.42.170.243 args=l3x2vcp6-i411ucqhjfp bpb5lcmucw4zejcy164k0wl/qm 
  - Log entry 54845: process python3 pid=5266 uid=730 src=135.6.233.248 args=9lnakabumkkk7eigtiqo98onez zh0shcicpd/u5edgf473e
  - Log entry 64589: process wget pid=30455 uid=150 src=72.135.240.99 args=mxccw5kgwjotbxnf08gr8bbrt/-dig5rtd-c-2kcnrcs1ehf
  - Log entry 71914: process bash pid=3220 uid=771 src=61.128.42.251 args=uendww-i2/t/t9g0zcy-q0pc08ym zw5viiqv38p9zkzaug9
  - Log entry 65280: process python3 pid=10884 uid=868 src=35.116.83.30 args=a3t/ns4ty2q6dwtps0-z260xjdf-7aexdd3yzehcj7snzi4m
  - Log entry 88499: process socat pid=24228 uid=859 src=219.155.19.233 args= e89bi39t/uwz7d7zzftltmg9e66zmgwt2oxr4bcww/0054g
  - Log entry 30961: process socat pid=15483 uid=352 src=181.72.67.216 args=a2i8l/rp8kmwzgcvrxmfimc8qe20906vo6zse80bxkm1dq1 
  - Log entry 83397: process sshd pid=8570 uid=619 src=21.255.133.212 args=-obuuo3qp6bys dknqfb/6ds/pbbwsdzdtgruoebxc--per4
  - Log entry 74219: process perl pid=13918 uid=468 src=115.248.159.221 args=x-0 -6smc5scy3 s74onulvbqs8w9mponm/quk0-6xnrdiua
  - Log entry 99126: process perl pid=1347 uid=456 src=102.146.226.123 args= nhya6o zbh85gfdwffa30jddjk2jbmvwgvo4j892-a42rs2
  - Log entry 55713: process python3 pid=25036 uid=830 src=62.230.34.11 args=gnht5bq8mzg5pamgbga1z67u3rv5e382g84qaett0sfidpj2
  - Log entry 81512: process sshd pid=24492 uid=483 src=140.112.168.129 args=ri-6pl0q/27ee8mny53jxs8kq7yh6qhje k1mvlzda259-30
  - Log entry 84204: process socat pid=22755 uid=921 src=59.36.57.107 args=9n6y1zcokc0cb4b9nz7xybvulz6dxc8nvo/z90j3q6jh08o5
  - Log entry 29625: process ruby pid=28888 uid=965 src=186.134.227.208 args=8q9lsz7xqoins 410xtf6q/vzsm0xvjarff07ef4ef85eucu
  - Log entry 55511: process sshd pid=30376 uid=59 src=87.46.200.195 args=idvjbuczasqdpelda0-b703 yn6lmerx-5ri qeahccqpjee
  - Log entry 50262: process nc pid=10605 uid=968 src=174.24.11.12 args=sap43h-a69awpbfddtfblqkt1wwfwv2xkp1bl93fciqfb-h9
  - Log entry 85161: process python3 pid=9786 uid=329 src=85.68.81.38 args=rdqpyojk719zjnxr0n33m9sz-binh8/mqppzd17ybp93ul18
  - Log entry 57862: process bash pid=27044 uid=360 src=195.51.145.136 args=cuow2b7ug2shuocopib/sdd0ebflz-mmmauk-156t-g7tn89
  - Log entry 13578: process bash pid=10475 uid=390 src=136.237.96.87 args=el3rrwuau7wiy7bhm7tk4w5xuf0v633w vemdi9gz1d-aid5
  - Log entry 84842: process nc pid=28600 uid=199 src=127.223.77.28 args=ai2q6sqdu 3gug9lqsy2vk2uclipad39d7kguj59 iu0cers
  - Log entry 47629: process perl pid=24615 uid=920 src=173.194.55.176 args=qpgsk apr5 9jiq i83g9dsc6wx4bltmxj5-plo2hq93sn/s
  - Log entry 39882: process nc pid=27357 uid=453 src=131.181.10.230 args=cd/fqv-1pxe0uw5hctdbw/rzm/f  799b457vtn34bpfv5ow
  - Log entry 95462: process nc pid=25976 uid=25 src=178.110.239.54 args=2dm8fw2ajho7l9hs5gc7/svl/7o55twvru/36/owboj2qqo1
  - Log entry 13966: process wget pid=31479 uid=887 src=79.53.106.30 args=e-s56aiw2dv41n7ys-p2kezlkca-uvnn1v6um2q1t3yd0joj
  - Log entry 11469: process bash pid=29005 uid=660 src=109.92.201.211 args=3xrtw-3060p5p pnhsex 898wvvn0oyj0t9mjeu7 s0757ws
  - Log entry 60296: process perl pid=24443 uid=357 src=49.0.174.226 args=or59-mlohq3o8t8p2 6ra7s3/972fe-br8azc190gi0s1wm2
  - Log entry 48340: process perl pid=14491 uid=327 src=35.67.32.191 args=d4t0xu0hume8i3ly9yh0m88gw-hxqssypqskn1v-6p 3w/ki

## Supplementary Technical Detail — Section 35

Automated correlation engine identified 4 related events in the 6-hour window.
Baseline traffic on port 47535: 1 connections per hour.
Observed traffic on port 4444: 194 connections during the incident window.
Statistical anomaly score: 0.811 (threshold 0.750).
Related CVE: CVE-2026-24419 — not yet patched on 19 internal hosts.
Affected subnet: 10.6.4.0/24 — 12 hosts in scope.
EDR telemetry: 4 alerts suppressed; 0 false positives removed.
  - Log entry 29706: process ruby pid=18309 uid=328 src=18.83.211.157 args=liq9opfxf69lpz0s9b78katqc3k0nqxf0j9m4god6ud5lngm
  - Log entry 60051: process python3 pid=9051 uid=764 src=134.209.255.159 args=me1urps93doz  75/l5gzyg54nqgjy137g 4vr8td8z0vav0
  - Log entry 85475: process wget pid=29039 uid=215 src=50.107.71.4 args=zs1yq1myv2bz pwa/h0pqurphtg 1yzxt79htz4/8b1m//iz
  - Log entry 88757: process perl pid=30168 uid=139 src=26.226.115.138 args=cs4v2r1gi-kvh758ij3ytzdrm8frrh0uyg579-iw0g28w58v
  - Log entry 31862: process nc pid=4931 uid=333 src=193.111.199.164 args=bsdb4a8nvt2ucs7u8kausox3g42lps -361mw-kghmm5rsq5
  - Log entry 90846: process perl pid=25138 uid=312 src=140.252.176.222 args=b84-e4wgz2ijlszzrwh2d 44ug tc/t75a9bmxaotfzzvkun
  - Log entry 83742: process python3 pid=22305 uid=510 src=33.114.8.242 args=hfef3vd5qvk4q9b8u7e-puel 0ti125csyrlobbzllwxmsj/
  - Log entry 88108: process python3 pid=25801 uid=655 src=213.54.33.139 args= -0pxn7syw8ew097u2ub7kvzhd 3n799uakoujx wr64kor5
  - Log entry 86680: process bash pid=1176 uid=97 src=36.51.99.194 args=lhz5b7ka-icb-v92evarqymj2gvgzojy1r0q-yfx5l0r9jjx
  - Log entry 21669: process bash pid=24640 uid=692 src=170.172.180.136 args=ivpej3rq1uh/t82n283lw7k4bnm2auwk9w2ttj3y1ot sl0i
  - Log entry 23671: process python3 pid=10204 uid=531 src=215.122.154.190 args=zkirmcy7c q3h9k2/qtiepfxy2qx1sizn30zenzb0526ufcg
  - Log entry 72194: process curl pid=4656 uid=928 src=43.74.30.211 args=0gycsiy aile-4c2j7d-igww-94xf/nwgnjpahxhk92xjreb
  - Log entry 46402: process bash pid=6627 uid=509 src=46.104.55.69 args=c-136rly89oiz5ju4np7aklbaibeg71294khznlgvp57a359
  - Log entry 34885: process curl pid=21127 uid=352 src=31.208.212.245 args=q7xtow2q/-ucqzlup6ltv7mr/0paa5irzmc4pr0w4y0v/1q4
  - Log entry 16262: process wget pid=28739 uid=251 src=127.100.254.221 args=4t24e/f2lljrx2uuzeqvrxfxt-9j1vml/0gkfvkk/92q hh-
  - Log entry 30550: process nc pid=17248 uid=765 src=117.187.245.107 args=223e/3z7rwwkvwxo4co5fsgcnzv889x7r-ipplk37kd/kaxb
  - Log entry 15482: process perl pid=24298 uid=606 src=59.126.50.175 args=3wxftwi-cwokygegsvimd9h6qi1xhmo95iv7i1-cg pl0jlk
  - Log entry 29671: process curl pid=18670 uid=39 src=108.35.91.206 args=9fd2h9t7v3j8ux7qi-33mt71nj6gxzjwpsy52vv9pr9km5i8
  - Log entry 52187: process nc pid=30327 uid=113 src=191.0.245.28 args=xiryr21b/ba7vz2/r/z-3-o11f4dfc5//1ottw j5nhhqxo8
  - Log entry 20802: process curl pid=26318 uid=786 src=82.68.87.181 args=x2o l97d/vdc2mtnblrdhknpkfuxievqbyqrm0y54t1i5kn9
  - Log entry 19788: process bash pid=25528 uid=676 src=21.25.46.161 args=b52bwn8j9htg5riarweyz0kf7xxvphnri093bvo8h8nqi9u6
  - Log entry 91917: process socat pid=28701 uid=972 src=10.103.55.125 args=ppwgphibk6md83ur yw81xp421r0s6icoa5e//a4qxehx1/ 
  - Log entry 70877: process perl pid=17592 uid=803 src=198.1.83.181 args=f30 jf-sj2ay4d9tvcyqzo o6ev f d0j1014j8l0bbchhxx
  - Log entry 70267: process perl pid=24648 uid=944 src=173.249.160.148 args=d rqyogqza9m/mppea6feu04m dhe9uo1olhx0zxqjdt/b73
  - Log entry 39149: process nc pid=7446 uid=248 src=76.98.147.156 args=wf7a8j617sximyc1wimbb3txls1ywa/aao9gyena8v427z7f
  - Log entry 33704: process ruby pid=12620 uid=515 src=118.106.42.115 args=/py71e4-wq/nn1z3wiv224 7osx 42auo5uiuv5u80rr72q2
  - Log entry 31872: process sshd pid=8579 uid=676 src=164.132.184.222 args=rv-5ipadna/3d197ap3uhux6o0u/taiuvn6j-q 79l2971ep
  - Log entry 96608: process socat pid=15909 uid=430 src=73.28.195.92 args=sr61wed29/nr69axbf8 w2ltfw n2rcealbuzz--enm-xw-t
  - Log entry 96577: process python3 pid=20750 uid=575 src=95.172.10.147 args=739740fs4bavthq/1b8naq50vf d7r95x//hujo364lr5pfy
  - Log entry 70368: process nc pid=2157 uid=624 src=91.31.214.236 args=wd-4 t0j83d0 5yo/hkdnj-umfff/bau-iwtwjedizo6o87u
  - Log entry 88741: process wget pid=25822 uid=543 src=69.27.84.80 args=zswiwnnkvi-cz/7ocy7n5st7yx-vtewqthxstu0j1fv64ujh
  - Log entry 26536: process socat pid=16146 uid=404 src=208.130.111.219 args=5d-8if7vqmm9ogswgtc-gpvewe bi8xad6xns-49hesfzo10
  - Log entry 92027: process python3 pid=3981 uid=366 src=8.190.183.126 args=/2ozm5dvxvww1b95yj914jfzxna9pvs3sf0kf3ni2f1iu91p
  - Log entry 50875: process socat pid=22701 uid=996 src=139.229.134.227 args=69sn8kkww4ph92srrx0dcprsmxfdl5-n6zv66hgsioniqml3
  - Log entry 49170: process python3 pid=31600 uid=762 src=3.142.140.250 args=8advt upkw9j/zfoc18cagclaginhf7z9a4upynttg  hkis
  - Log entry 89033: process wget pid=1694 uid=971 src=116.29.238.223 args=efjrrx593k/rh0rf4642max5dypayv4in1v 2is/tpn9eyds
  - Log entry 61820: process curl pid=28181 uid=607 src=80.199.125.199 args=wus1q7ar6w4--4o4e-dq6qjupll4otm3pzco8eebftkgkuqd
  - Log entry 87379: process curl pid=10193 uid=26 src=56.93.167.229 args=331f3p6fdtvu5ui2h9d pfdupn8 vyq2yxr/zrw16smrc551
  - Log entry 97350: process bash pid=4517 uid=575 src=108.141.152.35 args= jgwqbtngbcxn540uvakn5678e279-uwhx3rzekjbjxlyik6
  - Log entry 29634: process bash pid=12764 uid=856 src=12.0.37.78 args=ifm10a/v26-wzspjfid6v4mb09upvjw5ut5w3n3bfahs--49
  - Log entry 28671: process curl pid=14168 uid=172 src=223.235.70.10 args=lt9 -0yb92z8zb/vsqh 59wg90y/ qvl5dc nielzch/bpdh
  - Log entry 91016: process wget pid=21719 uid=261 src=107.38.132.38 args=wy7dfsqj5b/f4bm/ ddrz2js0/abydyxd37hx2w205ztftx5
  - Log entry 88196: process socat pid=25451 uid=873 src=19.90.12.34 args=xtpaiurrsle4usm3zrv851zynj4ulwvi3us07c 5pdh-ryu3
  - Log entry 36285: process bash pid=24867 uid=754 src=94.242.205.224 args=oqmzp189q1abvfokq-blnaesvbt8k-thad r20g/im-zuc c
  - Log entry 55789: process ruby pid=13729 uid=201 src=95.250.231.204 args=p791dwz6sezt2redvcmxl7otbagi/cm93qd5q7zjcbjbo86y
  - Log entry 18973: process curl pid=11863 uid=987 src=39.78.79.196 args=3ef384a5ud7f0x--l25z5-v8gfs5/zxr6cv9oxbttbphuj0m
  - Log entry 82604: process curl pid=7005 uid=644 src=167.211.139.74 args=7qzytn4261ua2wiwjqmzcqfpbccsgyagvkjx4djhg7tjm/wi
  - Log entry 35866: process python3 pid=8512 uid=51 src=12.151.92.143 args=o/7 1tkqjvqge37eiiuitkb-nva95kwfq1zvamkz90d5euac
  - Log entry 44531: process socat pid=28929 uid=516 src=197.63.98.32 args=vwougo7r34adakl jp mu  qjcmyfh8n6sktg58ilnw2p61b
  - Log entry 61449: process nc pid=27845 uid=792 src=151.125.142.247 args=fw4240owtnly8i6/726gta2-9f/zv19n7uhfppowhpetmpoc
  - Log entry 61481: process socat pid=5291 uid=45 src=34.213.218.218 args=w2uwasgfycreww6jaa3f-4b/dsfz6yno19o9obnown6qw mf
  - Log entry 90168: process ruby pid=2723 uid=917 src=148.4.248.68 args=7uuit7fdsvajnveogfmzqsw6q-qr5/tb3w-xyl62hlvcrwyu
  - Log entry 38317: process socat pid=19179 uid=967 src=87.217.198.76 args=3pa0fiqbm4ptsyieth/is980/ wclms09 pnh02eupui/684
  - Log entry 97385: process curl pid=2918 uid=173 src=219.11.30.218 args=56uuyr6r-2k i4f71 anxgxipbluxmqco/pyjol5pgqc2hez
  - Log entry 42068: process wget pid=5132 uid=497 src=122.206.211.184 args=8o/j55ivt1h138um7bme/1r13h d8rd5tb7 k7- 8bq028ia
  - Log entry 40591: process bash pid=31406 uid=904 src=23.125.23.115 args=i77swr/b3zl7whfh ggxsvu3 c5/b0ap8uiymfjm7 qz3uu8
  - Log entry 70168: process perl pid=24233 uid=385 src=145.147.82.17 args=oy6u3mvpxei4c9r68o ymnte64k5oydai2ftljlconq-bhry
  - Log entry 63706: process nc pid=30810 uid=890 src=80.105.46.23 args=-2yrvl1iss1o8-77mrx6sd4hb a9cx0citnwx5wic07z jnr
  - Log entry 87505: process perl pid=21591 uid=947 src=78.122.170.172 args=xlwht4sqkiog18w4xkk0utoyvrjsl1prmxba4l3gc/s2c7c1
  - Log entry 72444: process bash pid=26580 uid=704 src=150.130.116.187 args=v4t- m1 ro9t6boly47g2wpiihrml-/cxs8066l7z94uhe7f

## Supplementary Technical Detail — Section 36

Automated correlation engine identified 4 related events in the 6-hour window.
Baseline traffic on port 62449: 3 connections per hour.
Observed traffic on port 4444: 91 connections during the incident window.
Statistical anomaly score: 0.981 (threshold 0.750).
Related CVE: CVE-2026-46175 — not yet patched on 14 internal hosts.
Affected subnet: 10.8.1.0/24 — 16 hosts in scope.
EDR telemetry: 4 alerts suppressed; 3 false positives removed.
  - Log entry 58349: process bash pid=25386 uid=944 src=117.130.235.125 args=bieug3tie2vqlq3k76i31/ra1no3mgc82annwfq16 s-4wv3
  - Log entry 92503: process bash pid=15181 uid=909 src=5.12.146.7 args=l6d36wsgjj82fu1vu-it7resn1yivycgtnm39ehv9ipgn1 1
  - Log entry 98460: process curl pid=15117 uid=447 src=71.8.42.145 args=yyre06sa8dg1zd01i2g24dvhp3a-c4wj6bi9vre/vr3bpbmp
  - Log entry 12376: process sshd pid=10890 uid=600 src=214.92.39.237 args=-6d7b5eyuaksnt58-ds mbu5q32v8fc77ffcfv0f1/yu3ro6
  - Log entry 83282: process bash pid=20837 uid=751 src=199.189.12.38 args=zj-basth08wrj5rs9o4wu7dbsn7-90umjw6-ncfflfurr/p8
  - Log entry 38223: process perl pid=23264 uid=822 src=193.9.24.200 args=ym54q4dp4u nnxvofjhf6c5tb3nv4641se82/pxx69d-hr0/
  - Log entry 42895: process curl pid=7874 uid=473 src=174.91.184.111 args=bozu5-u3w5o1d pqps6p2w-7v93lx4p9 prehc/k8/vtj2zr
  - Log entry 95346: process sshd pid=21949 uid=123 src=142.132.238.52 args=wbis2w6omq8oqeg dc5/a3senazd65/mz6ajzo2 esmvmcin
  - Log entry 20307: process sshd pid=5093 uid=166 src=64.125.117.251 args=g97jb032yvw9lqsr3fzmh7g-xeb 69khds1f3k2ny vn2soq
  - Log entry 76946: process perl pid=21347 uid=544 src=180.248.226.168 args=6pqpkplet9i/ k24d7zo1 0yvlsm7solxxhievtfsb38/jb2
  - Log entry 89019: process bash pid=16527 uid=407 src=80.133.140.102 args=58aua5ex6 coxyyw-d3horknia7--4wt/uo2u6l/golhnaho
  - Log entry 56347: process socat pid=2749 uid=385 src=208.178.178.253 args=xvujhfga5b-r6/y5ewxfpqdxibl3f51ar8ob8wjmv m8f6hd
  - Log entry 67232: process curl pid=16202 uid=687 src=104.21.254.192 args=egerqqbqje985ifxkk8oz 1tekr3 58ueytt983urhq0 ztr
  - Log entry 36305: process ruby pid=28920 uid=547 src=107.15.52.46 args=y5qwt9bl df-3e540rzltwrz0l js2d9v9qvubw-mu0/foq0
  - Log entry 83892: process perl pid=2891 uid=27 src=94.61.176.15 args=p5j25f4jjam072hl33lazhe2z80n846i82ky4lw- /jww 9l
  - Log entry 58687: process ruby pid=23391 uid=684 src=24.42.0.15 args=tg9roc/xi0otncp3m6qwqxt4zjv70/c-5cp40 4g- 264i3e
  - Log entry 55062: process sshd pid=25838 uid=848 src=199.157.209.211 args=s70wei1hbzcy25metyg6egu/uwd/koqcmyj5omkx7szp5nvm
  - Log entry 57311: process wget pid=9975 uid=955 src=98.41.245.228 args=wjx-0latb2khsrm7 6vgee994i6vtg6fj-b btnz29auxz6z
  - Log entry 96142: process wget pid=7984 uid=482 src=73.49.18.97 args=dpa/xmg9maxod/ccc919n3/aemno1zavr/hiq1x9/wyi3-1m
  - Log entry 39013: process python3 pid=7195 uid=807 src=185.1.11.191 args=1bbtuwh7mcw2ojztun78mfb6ta/rfdlg8ml2xu39evyr-h9l
  - Log entry 40749: process bash pid=10416 uid=628 src=24.250.173.140 args=w/vlz z6 6g14 rhoifuthjk6s du762ahew9-8c27fp2qg1
  - Log entry 31762: process python3 pid=11894 uid=40 src=9.19.226.237 args=j-bkm-5n4hmlsuv19tmuz0h13oxpafm8yxb61q6jlpmox3st
  - Log entry 78569: process bash pid=10589 uid=629 src=25.57.189.159 args=ushncmebzlxl15/5ckizozosj gdoi1 4vle/m2javqscwvi
  - Log entry 94129: process python3 pid=14331 uid=461 src=158.167.164.227 args=5xr0hnlyzoa46mwwr88g/xc94780nn3dcnv1j43r4oyq3epn
  - Log entry 11226: process perl pid=27092 uid=85 src=213.115.50.56 args=bk/9fmq/21srx9hyafo2xpiosuhyh79y1 2qytwp9lzwqi5i
  - Log entry 53544: process socat pid=18523 uid=997 src=24.242.240.167 args=eyylfw0/vo457z38x6lklnwi3-49bk9qdippr dbv65nxl/1
  - Log entry 40238: process socat pid=18160 uid=225 src=3.242.162.91 args=maczkv1mj3900ffb5k-b-lkg/o6lg0jf8afto0n0y8qq1-ki
  - Log entry 22104: process bash pid=3160 uid=807 src=57.163.207.242 args=n0f8qw/kvvjsxam6ba1uea6emjee/fvv3y2bpbcpflyi65kk
  - Log entry 90875: process perl pid=12599 uid=233 src=154.171.242.131 args=48-hj-coca/u34j8y3vvxr5o24z04eeux1blpap-u27xipa8
  - Log entry 91845: process nc pid=4617 uid=289 src=91.145.210.96 args=3i9kgrlcxyzyxjosw4x f88w0lquff8ou4215a5oc8olgfij
  - Log entry 58748: process ruby pid=7327 uid=250 src=141.135.69.224 args=1d7lp/z0/049hd99580sx1aa4clu3lcgra175vt77j/2ga-8
  - Log entry 55137: process socat pid=8948 uid=589 src=19.185.219.109 args=2/f gr5su-x rg5ttmfli3fxjjhrqkqmx5p7gnlvbrtdvrj2
  - Log entry 13363: process perl pid=24476 uid=507 src=197.19.123.212 args=x9oe-1l5o02gkrgn6x798yc9z4-i0730ih4y252z 4pzhmlf
  - Log entry 29819: process nc pid=16892 uid=187 src=40.132.43.34 args=99vxpfsz97bgrmrcdrsowwwa-1/c6hz6efzcf tqt6t67vgd
  - Log entry 60675: process ruby pid=7146 uid=500 src=5.30.110.140 args=ks19xe7yv el6z3kob/ardzsq70xpg-g4-z63ivjm0biod59
  - Log entry 73509: process ruby pid=1153 uid=567 src=194.229.91.140 args=54scw6zjypp2aoig9rc9c0d0ptol6oqpy/q/is4hx0fnp4d6
  - Log entry 24166: process socat pid=18764 uid=599 src=89.134.180.89 args=9-f 1f/b-bp4-ydxffqtai i35k35rjwttdet748czc--0hy
  - Log entry 54497: process wget pid=18059 uid=110 src=59.182.132.49 args=xio-j-ayqifljwg82k4htha/5o53dd9e6x2-w2 nmmk8kjtz
  - Log entry 81539: process ruby pid=25864 uid=263 src=97.181.131.98 args=y8pitfzlezwhazugpy 5xy9dj50bv8gcctebdop0due1cvxd
  - Log entry 85243: process python3 pid=24095 uid=558 src=175.178.216.64 args=3ead-fmoudzs8f1ufoz9u8/j7o81cu/s0eurqkqm/566kwmp
  - Log entry 18517: process socat pid=29665 uid=887 src=152.1.204.30 args=hqteq h-xf/0hm73hl efwbe6iichrusnxr7cht 40p92mwp
  - Log entry 27793: process wget pid=6522 uid=623 src=141.99.144.230 args=l6z-/dma hryyq9xppuua-0egr8/kq79iod3 eze05co3ruk
  - Log entry 11960: process perl pid=26508 uid=100 src=202.57.49.19 args=h93a/j5mq43qy/cu/846a hb jwy wfzsehw/fl5v/wubd76
  - Log entry 26923: process nc pid=26592 uid=92 src=96.45.144.136 args=37b5jfl5gwlwz3b9osa3bwrtit-6v3ujmslq4nfxiuq4pc/f
  - Log entry 17729: process ruby pid=2715 uid=233 src=95.142.65.71 args=og6t/k9nvm5e33emr/40rfc9 d99/hju5n-8xow-ml2xuv1z
  - Log entry 15299: process bash pid=9477 uid=952 src=83.46.56.101 args=3g7/hzrdux--7u1/szd-/-kgmyp9 b6/iy- ejc5wy93dl8b
  - Log entry 71110: process wget pid=18130 uid=828 src=195.42.119.38 args=c4fhgmygfzk6zncr zbq6 u1pe7fzmurreiw7xhccf40ehgp
  - Log entry 61752: process perl pid=18799 uid=753 src=164.154.51.202 args=lsx2j iqtigbo8-n/12ytar3iaakwbejb1vb-dlrox-4c5uz
  - Log entry 62727: process python3 pid=27328 uid=74 src=27.199.18.171 args=kq043ytoqqqd5peyoceipah/036qbgcezzq9/6fj9v1-ffwr
  - Log entry 35882: process python3 pid=11311 uid=835 src=205.2.62.29 args=lif-2aeh/4gtbems-z  alwspuiccyfj/ s7mvgz-dy01vqj
  - Log entry 91847: process nc pid=13928 uid=79 src=88.193.242.27 args=hnxokkjqr3-aozh8lwk920yez4x/tkzlbznc-6usq4q86rfc
  - Log entry 59687: process bash pid=26621 uid=501 src=81.74.212.143 args=gyz-mtcy9tuwmhmss-cvzdsbhc9g/a7dtq7t9xy2rt3b- 1z
  - Log entry 13137: process nc pid=28896 uid=505 src=1.62.29.159 args=/rd//rggav73942jj/9-qz5te26mi77enf8f/cn513vx-bbj
  - Log entry 43010: process sshd pid=4192 uid=320 src=112.157.210.15 args=sd/id-9xzyfdsz4trol/orp2n9r/gfmmay5 11bjkq9qtw-w
  - Log entry 40714: process socat pid=22673 uid=396 src=218.135.90.207 args=8acx46tfvmononl66gwg9c553lm2xz8frs-kmm5x0dadpyy9
  - Log entry 72899: process python3 pid=20408 uid=171 src=111.206.44.172 args=qgh6xj46ftpzfy6gwh7t mhn2n9 luuwgxl9il458ccirx6i
  - Log entry 19690: process socat pid=24822 uid=906 src=61.43.98.143 args=sa/z /fl9f0lypahq g6petjyhtiy86xalf2o0tusgsbdyd1
  - Log entry 82997: process wget pid=7289 uid=6 src=42.126.219.69 args=ixsawqkdosbxo8npw-j-ylionj1/8ickzgko9cnn7cnmbd8d
  - Log entry 39867: process wget pid=18993 uid=549 src=66.124.187.231 args=qv453pwjlmqpchqu-0m0ya-guxpem0ett7i7dhjikvrn36wa
  - Log entry 80430: process perl pid=30203 uid=703 src=179.51.55.157 args=ojruh ezgws31rw2li5/ agnt 4-vksttds84y3mrw-t19gb

## Supplementary Technical Detail — Section 37

Automated correlation engine identified 18 related events in the 6-hour window.
Baseline traffic on port 43742: 4 connections per hour.
Observed traffic on port 4444: 109 connections during the incident window.
Statistical anomaly score: 0.880 (threshold 0.750).
Related CVE: CVE-2026-48884 — not yet patched on 13 internal hosts.
Affected subnet: 10.7.0.0/24 — 19 hosts in scope.
EDR telemetry: 4 alerts suppressed; 1 false positives removed.
  - Log entry 77302: process perl pid=8401 uid=656 src=142.75.143.237 args=wnizbsz8njgici145hcp92czwaqd7c-p9 -8s xjt9nfkpbd
  - Log entry 44480: process wget pid=8273 uid=298 src=215.134.32.233 args=0kq6d/7sgfchf1th21x87mme  kl9 ravegn0h7rlkzxegpn
  - Log entry 29791: process nc pid=27833 uid=494 src=213.186.61.110 args=jobi2gqq- lz1npgoex-zolavx0zq601 7ac5l3ntmbs-v5u
  - Log entry 82710: process perl pid=12745 uid=223 src=65.59.123.113 args=khoretyt-r euur13--ngz5-bkg /yhqma-pfql/-4tq36ox
  - Log entry 96146: process ruby pid=29826 uid=219 src=72.4.95.95 args=z/gsnwezmhbv58jp esnh5f-0m9d2f-4du o48dhz yyqqfl
  - Log entry 79987: process bash pid=30660 uid=850 src=186.22.253.143 args=cit12i6ayn6vk/u60fpjx/vh0-u9ysgjxze6rolmslql-cem
  - Log entry 85650: process wget pid=21723 uid=133 src=211.65.245.64 args=wvu/rn073f7vnfspjftku789tt9k 65ghdcv1dmtt nz0nnf
  - Log entry 50921: process socat pid=1323 uid=444 src=118.157.148.168 args=lplxt2-hsscsbh8zyhf1bf0aj2a-t/hiuar9ijlc-oz8b-7 
  - Log entry 50962: process nc pid=22745 uid=29 src=178.18.101.51 args=oodb1gb9b3fokywr64cphtuy01g301-0kisa r5f2s6/i0hp
  - Log entry 45227: process socat pid=16814 uid=109 src=180.157.126.222 args=boq/smu2l9enp2px02i5ap-cxiecx2ioffan94u0sw2jy-94
  - Log entry 81159: process perl pid=15766 uid=662 src=41.240.41.250 args=khgamy59 8ljn3tts4oual4c-zw0ee2eb8yjc4l4-bjx2mm 
  - Log entry 27509: process perl pid=23394 uid=361 src=175.128.111.56 args=v7mkj8-mi6/55g5vpuxapfsz/4safox5qz03fajdndi31gsa
  - Log entry 67018: process wget pid=6923 uid=73 src=113.56.204.206 args=1nya5hy0k1f/xm5wow6te2lfiryaslgjj2xhdhx ykhj-5tl
  - Log entry 64608: process perl pid=7138 uid=3 src=67.37.196.148 args=avvv0kpo7ng- a 4srqtxp9-satkdpiz2w42 g4vede8asov
  - Log entry 45411: process perl pid=19117 uid=300 src=133.110.70.112 args=zhnf32fh4g0r3e1 1n7le1r03fc4s71 g27jz/hac2kr-4ms
  - Log entry 35050: process perl pid=11894 uid=170 src=174.245.4.176 args=5nwwu7nun69b9nl/ do7qq1et66ck77gil2l-z/vf6clxvw1
  - Log entry 43755: process perl pid=30186 uid=957 src=178.139.77.54 args=a98muxvhqg216hllsyr7fr8x/8iyc01hea3xgbmhtov22q4r
  - Log entry 46084: process bash pid=2785 uid=19 src=66.213.163.245 args=4oy-w0l1x3mrofjolfpul/918txgnfqh8ev3eijeb7 u059k
  - Log entry 57527: process wget pid=19677 uid=673 src=54.137.108.206 args=o64tx-3hd94zp5/fsocyd19-6b7q9eu/iwdw414nbk7ixowx
  - Log entry 55603: process perl pid=22455 uid=986 src=108.190.184.111 args=1qtoeobrct8vlffnan0ys8sgb0qvxyt-goo  8quvl wkcds
  - Log entry 14449: process curl pid=26359 uid=977 src=9.118.192.223 args=iepesjkhntbwdibed 28ws3pr4ce wdg18q/2 yz3d/y4l2d
  - Log entry 14744: process perl pid=18055 uid=54 src=146.69.159.22 args=aib85omiy/26x0925oeo/9r322up18fi17xghflgpa140ab5
  - Log entry 88939: process bash pid=10604 uid=342 src=60.107.44.19 args=c4jklilq07fa9aqx2g/st0 krnhawv403ddfwupu1j39s-3c
  - Log entry 77139: process sshd pid=25594 uid=179 src=159.208.225.48 args=9a7gy4410q5jyvjti-/l233p8/od9wklp2tjps/sgpk/prej
  - Log entry 85045: process ruby pid=30657 uid=389 src=19.108.72.222 args=abudh72zswbris5znal8p/363jsyvc6aj vaqhdr1le43ubg
  - Log entry 96557: process bash pid=16621 uid=206 src=146.187.136.86 args=pl6jtvcos7t0q3cl7bx 8oh35kidyurol1y5a11fe23q62d2
  - Log entry 86203: process wget pid=8348 uid=849 src=89.188.238.21 args=b2l9wvz9714q86pkql wtva0reb j3x2qdf/9vrjug 3c4ss
  - Log entry 75696: process sshd pid=19326 uid=266 src=123.79.139.175 args=tfjx3egr4iliu6ql5tlyde7r/8 6ke-241u8ps/qf8nfp/x7
  - Log entry 93201: process nc pid=4092 uid=208 src=16.69.193.186 args=cyqg6 fubro8f1y74nvjuh7npjerbv6d lv8i59xwb3t0y08
  - Log entry 60174: process socat pid=3535 uid=730 src=198.77.11.105 args=s3m12jebjr3un 34txbvi2xc1z2g49tp7sdmz4p9knl5n8mp
  - Log entry 40275: process nc pid=29216 uid=370 src=153.108.110.129 args=5zkvdp0b9donfzd8a7 4ef5vxzdlt42e10 8jtgrq5/-okx2
  - Log entry 99034: process python3 pid=27704 uid=763 src=10.234.147.31 args=jit9p4a02/ vv89ej/ky-jnrmqesl8zyaddbt9fqjvgn b/u
  - Log entry 88309: process socat pid=8391 uid=111 src=104.221.150.138 args=1p5mtp7v76j0 hgg6 1iarep-b/m5hl/h5p5rl7t-ai8ykc-
  - Log entry 87788: process bash pid=31844 uid=285 src=79.188.46.191 args=jijosqbesjdlwekfcg9a4y4wk2u-4s/8au qdlk4qfw-c3/x
  - Log entry 85407: process nc pid=8709 uid=340 src=50.89.116.59 args=h3kf6 0yho1pbvnwocdlw24wrnx6-1zgh jzpd2fe8kj/ciw
  - Log entry 45694: process python3 pid=28849 uid=572 src=69.128.146.207 args=w7kq010759nwkxuom0ls17ron4sbza-4rx7dtdotj3cz4vpu
  - Log entry 22698: process nc pid=5048 uid=651 src=134.155.239.212 args=0z5bmp74g/nhfn7blyvrmzq8zgkw0xzix4iksbpwbr2xc7ek
  - Log entry 71456: process curl pid=30565 uid=55 src=79.69.191.73 args=/w1vxobdyq30zl8 92g-3p8y5bc275/lt 9eckq3-ez/ul3w
  - Log entry 42700: process wget pid=4127 uid=708 src=117.231.5.154 args= if8krrknw345nge3w ye9x9ovcs8n9mc7xqiv0njwi26mvs
  - Log entry 15493: process nc pid=31728 uid=182 src=4.155.199.92 args=yi11sspzu7s0pvnogyop59hp6qeo47bjeyl-hovoi ey780i
  - Log entry 69663: process perl pid=8483 uid=407 src=112.24.148.204 args=i w/pw3m9vu8kp327bjkdn0dojqssd31b8nt/gsjz owkcxk
  - Log entry 52562: process bash pid=9180 uid=127 src=222.100.135.129 args=ugpqqgivsf7nm1jsckz2sblsmgrn8fwex4j0nkpapfx6enq7
  - Log entry 78813: process nc pid=15743 uid=31 src=140.192.244.203 args=/-se-7ph4lg3i81t833q8icvho9m5uxilan-5thsbt54d8um
  - Log entry 97412: process ruby pid=1242 uid=333 src=59.219.104.183 args=yvv57af/hbxmt0ng5zhmaj 04i72ckl27nsfy3//r059g9kt
  - Log entry 56710: process perl pid=22015 uid=988 src=154.217.54.135 args=52rnpjc o/mcrjf2/a9eivyaj/m5susyt7/4i3f/pt/x83dd
  - Log entry 68123: process socat pid=29601 uid=395 src=51.57.252.193 args=0736s0-8c6/zn2sxv8pcodl36sipu6/3vglkn2054mikpejo
  - Log entry 69885: process socat pid=1239 uid=903 src=99.180.200.70 args=v14vn7e2lleie4hklgmt/eh/-ok13qcd6ih34l560gkucn6f
  - Log entry 54665: process perl pid=25020 uid=922 src=197.106.86.11 args=6f7nb0w5in74ywh3lsu9k/7elor/-/-0qcy4j0our8p3100/
  - Log entry 58945: process perl pid=10039 uid=953 src=220.153.238.60 args=094h0tmv3kixvviwbxajhsijvfdu3o 5vz1nahgdv-v861i5
  - Log entry 24564: process curl pid=12803 uid=859 src=101.141.87.38 args=jznps85fjz6locu94kt0bref75nkp/nr8a/ fk1fl6jsougu
  - Log entry 94204: process perl pid=12696 uid=983 src=198.207.224.71 args=--i29xwbgzkn4/f68wvgswa0 vgjfst1sdb-chncnk-5024/
  - Log entry 73933: process curl pid=19337 uid=937 src=150.81.46.46 args=y7k22cjo8tpmnt81fpl72o7ioof3-feqeeky4oppcg/rymqr
  - Log entry 18791: process python3 pid=30786 uid=177 src=106.83.72.1 args=e6nguzsrvg8l491wbi221oo184-rwt1tb0civ3avmgjq9t5a
  - Log entry 63269: process python3 pid=4739 uid=143 src=30.65.135.162 args=yha8-pt4-/4 71dmo88-ljv0g5r-nmgmq-nlcuemgwmgwtfr
  - Log entry 90667: process bash pid=10555 uid=302 src=17.251.250.120 args=-3liey/5s4uzaor12fjj1qocile8z6gd1pjzsisbc9ams0sf
  - Log entry 45319: process socat pid=28070 uid=450 src=163.239.81.184 args=8 5k 9c-zy/pgoanf83i//yv5lqv- h/zix3g82v gw5cuf1
  - Log entry 23723: process wget pid=25493 uid=609 src=82.224.135.215 args=lgg8ayr299i7dojfik0nv4ua0m2l9vgzf-n/yd3p6w/oti2w
  - Log entry 34390: process python3 pid=7950 uid=177 src=42.124.27.80 args=o q4gentn2gzog diy40s4tlgkryjh6-r6uxra0-l8mwrbd2
  - Log entry 84139: process socat pid=18580 uid=645 src=62.253.164.71 args=epglk1h3jpr1hhns 5mm4qm5o89rjna2/8zsd1jg65r8bh-z
  - Log entry 10266: process perl pid=10689 uid=12 src=136.31.95.54 args=y0xrv7o0cduyunbl9z0e-h7gp/aoly6za74cjpm6b0n4  me

## Supplementary Technical Detail — Section 38

Automated correlation engine identified 8 related events in the 6-hour window.
Baseline traffic on port 10854: 5 connections per hour.
Observed traffic on port 4444: 130 connections during the incident window.
Statistical anomaly score: 0.954 (threshold 0.750).
Related CVE: CVE-2026-40907 — not yet patched on 8 internal hosts.
Affected subnet: 10.3.2.0/24 — 27 hosts in scope.
EDR telemetry: 4 alerts suppressed; 0 false positives removed.
  - Log entry 22536: process perl pid=15531 uid=479 src=61.117.164.143 args=b4iyl2w9s5hgtiy8hjcdym9rxx224/ ck5jsda5ttadsoo6g
  - Log entry 74718: process wget pid=9941 uid=284 src=151.166.7.57 args=9akz8tw0eqq0tppi tjcz5g2 n3xx0du/yw9c490l3go248d
  - Log entry 33146: process nc pid=11650 uid=152 src=124.193.252.11 args=cng/kuqv9wagyhq1wv-8mlvpqg337w4rh21t53fb2p9/-/2e
  - Log entry 22246: process bash pid=3504 uid=775 src=51.28.150.42 args=cr 7-2p1fv9f80vl ad/xxxwytgk477u6iiq6jy b9s46t4/
  - Log entry 98811: process nc pid=28848 uid=478 src=184.232.216.68 args=3goqwca0kko3o9bqdv6octh8h72kdtt95elidgbls2d066jq
  - Log entry 93131: process perl pid=12702 uid=380 src=61.221.175.194 args=dr51hbfdjjwon8of-bsapgo1w4wpq-mr93ta pa6sobj8-sh
  - Log entry 91192: process bash pid=11359 uid=756 src=153.147.71.2 args=lmkokqlrijit e 3tmoco074jvvqknd1svxvvfkmr r08zfh
  - Log entry 57004: process nc pid=2266 uid=295 src=133.115.239.165 args=ise0manlglikw 9ho2je5ueznt7/x5owrvf7fbos3az82jlg
  - Log entry 42528: process ruby pid=8985 uid=191 src=64.172.28.138 args=pmg1li7r6-ijuiq p0/7 0sffh9um0pbt9e1qo-jwzeolsk9
  - Log entry 87401: process sshd pid=29808 uid=244 src=63.154.140.241 args=wzp18gfwr834ph 0t00vr9/ 9v--n9dfd/tx9mxht56ave/q
  - Log entry 14393: process ruby pid=26126 uid=135 src=44.115.166.85 args=c f4 ti0p2k3pdv 10s3h3osbv/jn9sr//bj18 h3umwv0ev
  - Log entry 81210: process sshd pid=13338 uid=40 src=209.216.10.33 args=lunp00aqfhvn4sniix/d2f9-lggnnocdbyn-4cyr0hybvoau
  - Log entry 27708: process sshd pid=12619 uid=216 src=163.176.58.95 args=ycgxt-nys8lawvec8xzwg-sqp7aw54xul2mycw4g-d9db1k1
  - Log entry 94806: process socat pid=5262 uid=784 src=192.70.116.24 args=v7tbf14ug2/7cpoxxwaxevw9a5tpswgehs3jf1ub020/dswc
  - Log entry 64820: process sshd pid=21701 uid=391 src=43.85.44.216 args=wzyq-onz9u3bfk4js9089pwdyg-48agsnmz8gq8 qiocsofe
  - Log entry 72495: process python3 pid=10797 uid=931 src=58.13.183.174 args=7hmft/n3qb34uil e91twiqdd42x0c-qqgr88/ 97e6f0e6/
  - Log entry 23039: process python3 pid=16764 uid=503 src=217.220.221.71 args=e84pjg7wcshuhq7ynos6co ord9k2zfkefwi/erkbxyt28w5
  - Log entry 46295: process sshd pid=8837 uid=362 src=71.8.172.106 args=ctc81gj34 1b08snhf56-0r353i79gmymubwo0fouxknk7d/
  - Log entry 21209: process nc pid=29648 uid=554 src=140.64.72.22 args=r11g6jdo998b8eh pk3hr0h1t0eiuomt9-6 1zss9bn-cy53
  - Log entry 12771: process ruby pid=6768 uid=163 src=96.141.101.193 args=v68if/uc5pmvlbzxwzeiglwzp8dbl4v6mqap4mzf3xzhsgoq
  - Log entry 97367: process socat pid=2585 uid=752 src=194.135.107.253 args=kcpaskw6joj2m8zl  9hy/oh049r3ghp/zfu9wi9icl0ymcs
  - Log entry 83822: process bash pid=17094 uid=110 src=55.246.236.188 args=80n6-1lq/fxzq3x8i49nyiwc6o-p6u1jj-nnt/dn48-r8knl
  - Log entry 95645: process socat pid=21985 uid=897 src=108.135.94.155 args=d1-5rzx95ia1/l6g6bljb3-k0qbn eqb7pfa8jsugnvm7/ul
  - Log entry 57170: process ruby pid=22473 uid=255 src=62.6.92.22 args=2n3fhjb/7tz9zn4sep-9-txwd7skgaweu4ylywchg8qkderf
  - Log entry 63437: process nc pid=5012 uid=128 src=47.118.22.148 args=b/2/2dr-7owo3jrvac3z3zsu38xjexvpkhzjbdm//pni3f/ 
  - Log entry 38807: process curl pid=20191 uid=646 src=156.66.20.48 args=8mabc8iti06ads3tgisvm0s9dufr1gb2p6s9du-ksn533e2h
  - Log entry 84729: process ruby pid=20693 uid=665 src=157.93.125.37 args=b8vc6d2bpu4lm-3943pfc0/m6n7am/s1nftfxo6 yeb4hmiq
  - Log entry 99244: process wget pid=12105 uid=473 src=219.246.55.205 args=velecih4v4swn5cy yaa6kzfx70hffqyz2//uf9dwfhsnphj
  - Log entry 95410: process socat pid=24319 uid=829 src=201.126.107.167 args=q94i u9six2-shr/izjw4yg3z4hltogi/6u7z2b0np1gy8o4
  - Log entry 94601: process wget pid=8365 uid=982 src=194.166.188.154 args=rfjy8z4lurmto6fmfj8hnx9sur3juyy-5ruv 9dj tgpqmp7
  - Log entry 21245: process nc pid=23636 uid=500 src=172.58.88.232 args=-vsiaj7ssbbetxznjmjlue0iqrs57tg6ry-oun/n2nzk737e
  - Log entry 92193: process socat pid=8429 uid=396 src=52.81.77.208 args=6ia8veg2m59m/drl/6k6szdi5hj5m zw6qwu3b4m8arpi8r9
  - Log entry 68958: process sshd pid=10375 uid=248 src=208.217.205.98 args=67y8g4pe8h5gzqjurljxiu6-5tlxzxfta4ybouzx5kts36bp
  - Log entry 57991: process sshd pid=20532 uid=841 src=83.222.112.109 args=/ryhclgdhefo-5w7ka/79m4um5snf39px-9ya-55-9yote0l
  - Log entry 62813: process python3 pid=5715 uid=58 src=180.174.246.206 args=2h9855h34e4lnp5h2218zbcwzk9zhrga2 7 qqnx/8xg6ika
  - Log entry 67286: process sshd pid=8020 uid=433 src=20.65.150.213 args=m506jax2ajfg4vwv m1n/780kp0gq/r06x8kqcm3dj3eblvv
  - Log entry 16664: process sshd pid=25330 uid=111 src=200.192.42.206 args=939/lvyssw6hlaaq hxi1qfemncehree07l/71lw9b2np53u
  - Log entry 50818: process socat pid=20374 uid=53 src=152.105.1.144 args=dpg1suprp2 i0xydaozmyg7gbgv23lwr7/ih3aq1-0m9xn5y
  - Log entry 92566: process perl pid=28047 uid=506 src=96.36.160.13 args=o-dojng5zlcc1bnv8gd1wf5/ v3bd47pr4e1 jsh1qbkje-z
  - Log entry 76544: process sshd pid=29148 uid=662 src=35.134.68.75 args=txgeh/ ei2/tjk2sawh51gz-sr71abkg086m4cwe-y8a1fll
  - Log entry 84009: process wget pid=30958 uid=741 src=46.52.84.46 args=ij on1yqaupr0np2x1ssj-qevdo-hfc0x0aa-pf0br05olgj
  - Log entry 44525: process sshd pid=18402 uid=724 src=6.136.246.149 args=qow8z5/5s72xhb9opv11z8ukswj rzrnpycf38pwbmptaces
  - Log entry 66989: process curl pid=24768 uid=586 src=25.26.203.45 args=vjwe/wptjv0vqxzgmxguz0a8zxgqqnas427 ffcj47el8 7y
  - Log entry 16991: process sshd pid=11648 uid=236 src=99.17.231.247 args=oyjcgdz1kb-rzve1enpjkyqs z39x0q9d5hpytipie26f/1y
  - Log entry 28384: process python3 pid=30662 uid=950 src=115.186.195.8 args=ygyfclb- q0tdx10i3v/r-82sfcy3gbmf/w/ivflufqi- vq
  - Log entry 12315: process ruby pid=10183 uid=510 src=160.67.232.101 args=0bp 5-q1c9xs810bl8h7c0w7bbcy9r22g27hrmphm-x8hf79
  - Log entry 23791: process wget pid=1923 uid=476 src=30.33.55.36 args=0i xu8r8ulf6p7p3 27ke3583g12ijw75i-pyl/jmjw kx/g
  - Log entry 81193: process socat pid=30935 uid=789 src=80.170.73.66 args=v 0sz5 5/e9zlenoi/wq/iyeg/441ulv6fsm0yc-owra0 8/
  - Log entry 65812: process bash pid=8235 uid=464 src=213.221.31.202 args=lu/j7x7yv /de/h8i2nenrc0b5q1bb9y-d-/j 4grccyyl3w
  - Log entry 45985: process python3 pid=3578 uid=803 src=139.153.8.196 args=a6dhmco3yfsk43qdm 745pckq no-1z2ixba4g2g9c75k3hm
  - Log entry 16055: process nc pid=30301 uid=912 src=165.11.176.181 args=l 4gmcd- cb-6nbv1bqew3ho99-2q6apq5-/d i omzooa79
  - Log entry 28460: process bash pid=3964 uid=953 src=57.206.50.70 args=kj70zq6w3s7lnx-zc6wkiwy2-f1w6iauyu9uom/2tpw9d32d
  - Log entry 98538: process bash pid=28450 uid=850 src=99.81.235.119 args=yupaw0xd7q pooucpe9s u5b0p0y927z95gki18r2y9eb7/3
  - Log entry 20773: process perl pid=21194 uid=236 src=174.146.147.209 args=e1xky-2qq ed-ghm4jcyedkzhgsw6ibf2p0o-f7-0xh-ujn4
  - Log entry 87303: process socat pid=29339 uid=954 src=55.182.150.13 args=h5n9ma/76vi60b68cdgo1ctppm3u6qnsfsix8qgn tacwqy0
  - Log entry 31327: process wget pid=18125 uid=69 src=34.113.44.182 args=zb-gssnqwy3tsl5wn5zw8fex9azq mz/42ek0g0ia sargo9
  - Log entry 15959: process perl pid=15310 uid=822 src=157.174.205.17 args=o/u-0vmejpnyrhjrfza  0s5f6 s lf0hhv54rnogza3nc-g
  - Log entry 27946: process curl pid=14468 uid=876 src=158.109.142.122 args=yaogh wdgli9pzuirda/1yxx/mn07x9pgl0jx13jpiee r t
  - Log entry 48309: process wget pid=30534 uid=343 src=100.141.129.98 args=k759jt-td/zzs05ym2d0mj0neyeaih1jwduuggeot4yhtbhp
  - Log entry 95681: process curl pid=6245 uid=58 src=163.66.105.11 args=d1/g02mwhniqixc c91kn/ 3y1j0ay0p4/7bsrf8bago66is

## Supplementary Technical Detail — Section 39

Automated correlation engine identified 5 related events in the 6-hour window.
Baseline traffic on port 33526: 3 connections per hour.
Observed traffic on port 4444: 106 connections during the incident window.
Statistical anomaly score: 0.832 (threshold 0.750).
Related CVE: CVE-2026-46248 — not yet patched on 18 internal hosts.
Affected subnet: 10.3.2.0/24 — 12 hosts in scope.
EDR telemetry: 3 alerts suppressed; 2 false positives removed.
  - Log entry 14192: process ruby pid=4601 uid=862 src=180.193.2.134 args=pada0pkxf1tk1/ys/5ni8n6i5i1cbbse4qo4jkjv571q6j-8
  - Log entry 28522: process python3 pid=31884 uid=992 src=155.126.183.156 args=65 rrbr5-sd-ph f-lk6kxqegbqp/79h9k jpytclkd1z198
  - Log entry 19155: process nc pid=28732 uid=151 src=10.160.173.140 args=nep3-fz3kis sctgc2bta70gelp9ra4firbd30/mjp8ajpe1
  - Log entry 26062: process bash pid=18119 uid=914 src=133.33.69.8 args=soz4 m2brnr3d g2jl8jydj6asbekp6ey6wbputifvmdgf1h
  - Log entry 99081: process ruby pid=30090 uid=632 src=80.127.59.176 args=qgr6-d3mpmj pk4u od zxl7wt  up3356tqqqsxuw/d-0qg
  - Log entry 54285: process sshd pid=21763 uid=59 src=76.44.59.164 args=joc2rst6hxcml68rwkxd3oa5ffk7a0e89tlegkyqbwvgavzw
  - Log entry 31374: process perl pid=2649 uid=438 src=195.49.191.86 args=yg95qeyw3rp5ot07j0wi008u//15z/isc f5mdjd82avvv-r
  - Log entry 68761: process curl pid=25529 uid=964 src=81.209.145.156 args=n8iuyf3thqs vwio7iwsiwj7az-3-ohvur6-go003hikcv8c
  - Log entry 76310: process ruby pid=24474 uid=653 src=89.170.64.195 args=r2913kidb///l8dn86-83rinzgknnb5 p6be7pvp4lk6mq7p
  - Log entry 88817: process socat pid=20616 uid=49 src=74.43.38.19 args=- k8ibwmgt0kn8feetlt0ylbilp/vsoxvr8ow/cgqdn/qw00
  - Log entry 60570: process curl pid=24388 uid=779 src=204.48.230.45 args=xhj8x-04v00k6-g8atjjdae7w6pe8/2b81ndrv44aeolfgmq
  - Log entry 39578: process wget pid=8131 uid=632 src=41.100.53.43 args=lbdhex45e766ez8olk4m72xmdb0q6o7cwoprnwbaj6-h7tml
  - Log entry 10408: process wget pid=19613 uid=548 src=127.61.65.229 args=0bmpfutt 9 1m4687fj7owyhunsg/ymy16l1 3m77686k-1f
  - Log entry 33517: process sshd pid=2524 uid=435 src=23.114.243.245 args=r7e u8rnxjufw8d7qsvcqbmvs456yy17c5140 i z7fpywu4
  - Log entry 82946: process bash pid=20452 uid=931 src=150.64.179.49 args=wt3n3150vn1rq31j/ 6 wm375j-/20bs5husa ozl/eu7e t
  - Log entry 38888: process python3 pid=5384 uid=999 src=161.166.30.158 args=s/9jvbpx 1lx6pdvm1rosjmomxfvv5c-42 rqqdm02c6fet4
  - Log entry 72301: process sshd pid=17309 uid=286 src=154.102.101.194 args=gk5b4ywf6x3bkkkgmhhj9se-1hijo02/v 2k3q3 2pflnf c
  - Log entry 25428: process nc pid=8757 uid=873 src=217.133.85.108 args=lr vljp62b84i6 - 89asv/6cxno18d9zg  mxfnpwfgovs5
  - Log entry 88530: process python3 pid=19022 uid=853 src=29.187.37.208 args=zb06bd4gh0j66dqr//tab3fwloowux3khi4mraeyb8a4h57n
  - Log entry 37207: process socat pid=28815 uid=850 src=203.78.183.3 args=g7i j4gvaqig6-kzzzonytt axmtdyorl5gy/rbjw1hk n0u
  - Log entry 82031: process ruby pid=8583 uid=801 src=222.217.183.41 args=eyoxp2fp4ot1-470ru0c8kf64lsilvflk/3e8n28vdq1zhoc
  - Log entry 74062: process nc pid=22992 uid=616 src=47.104.235.126 args=6hu06l0o-e1u/9g0h 1wapwvmel1qd5dtowoe52jveoga3cg
  - Log entry 93000: process nc pid=30525 uid=721 src=159.51.178.53 args=-ogppe9hlr2o4tybewg a1ttx68cb6n-l8nq5doa7lvo6ldp
  - Log entry 82408: process nc pid=21718 uid=18 src=72.131.130.181 args=07do/3l -xi7jlybrolr6od9 mkb6hgtwcz9zfgy15f9al7e
  - Log entry 91280: process perl pid=13151 uid=669 src=128.81.81.227 args=2xa/seya iqk27w3gau-xki9i/h3hvov1otcx7hwy08oqh6t
  - Log entry 37624: process bash pid=29400 uid=631 src=134.1.84.2 args=nfcvholp38yaxvwuhb i2e ucj62wva rek/r4kss9fjhowj
  - Log entry 89147: process python3 pid=5169 uid=380 src=144.96.148.4 args=uztgzw/c0e31x-2mtd8 w9uo1q79k 22otrxl2c34fnzomi0
  - Log entry 42497: process bash pid=4804 uid=411 src=75.43.135.184 args=v6d/iszsjeii73ff1uepxant4cnoo8-xc90m3chz2mapmi1w
  - Log entry 31412: process python3 pid=2505 uid=204 src=206.185.250.89 args=7y2kw3snk4o sxis6jg14h7vhz9wculw7ztt2cp4zko78qoh
  - Log entry 50295: process bash pid=31976 uid=317 src=52.216.31.142 args=-u/sh1phh7bnchqvro2oman t1ypzbs1sw/ul oy7o hrsd9
  - Log entry 91103: process perl pid=13592 uid=500 src=197.103.101.6 args=jfj/ bqb5fzbm3m41t6wklt8ujy hluz21/z jq84g7lfgi2
  - Log entry 94008: process bash pid=16768 uid=153 src=175.232.179.38 args=z/t8qju3h 1v2tjyjxkpul7g--7emlcv/cq0wgdm rltmfd8
  - Log entry 76721: process sshd pid=4920 uid=435 src=201.72.227.107 args=wphfidj/hitlht/0pm3a- r rszv3oyxae351a98p2in9x5a
  - Log entry 76650: process nc pid=7510 uid=871 src=51.243.14.116 args=2ne2xwjl46 39mdouy2fv-8md7lfw9gmzwvm7gyyqs-inxrr
  - Log entry 60995: process nc pid=26254 uid=591 src=119.249.3.8 args=ndgx1f1-drrgkukxlmd 4k2fgw3pef9tobkobjk3qzkyqi92
  - Log entry 30624: process wget pid=8358 uid=446 src=214.238.17.237 args=mlk 3vq-8z8sglw39avk9dj248t29m3-s677-kt4hsnlmh-5
  - Log entry 69589: process nc pid=27692 uid=977 src=112.86.254.147 args=da3uz59r9shqjvbda1mafz7yet2fz7fqkgyh/nlkfrjvcnef
  - Log entry 54272: process perl pid=8322 uid=195 src=56.103.106.172 args=/m wyjhseasc5faoq84/gn9g8jr5okg43nepqmeck7ffi7di
  - Log entry 88488: process ruby pid=28135 uid=13 src=59.126.206.243 args=7gmbn4y7qwm9298go3th24231ectahx7lob-l1e4bxy3-e7p
  - Log entry 43395: process socat pid=7384 uid=310 src=130.249.244.195 args=1z6snkdb6ioh886w4l9mddl2ltjvfw/jv6h7qlzz4cn2l4uv
  - Log entry 61123: process nc pid=10670 uid=869 src=180.147.234.37 args=zh6l4b/v4hf8jzs 5ao2feb2 3h0oeg8h3emgwr8tl/h16ce
  - Log entry 13798: process ruby pid=24485 uid=48 src=4.145.73.126 args=a57hnqv1fk9x2uy2hop9vmgj5qsm8luyl1jhpd ievg3jh6b
  - Log entry 76993: process curl pid=19194 uid=86 src=61.142.16.39 args=q/1cqg /8ec kniovf8dnwjnrver4ws-lmb7bonqii79wdwi
  - Log entry 64341: process curl pid=10839 uid=924 src=101.51.168.222 args=4tpz68h2bu5dg7nnean7zsmku7r6owfpyl5zzs6segx0m-l6
  - Log entry 76342: process socat pid=9677 uid=688 src=127.121.148.118 args=glh0m3wz3d-ttsndsayhfgx rt6xkkho/2dluokvrq3x3hdn
  - Log entry 21200: process bash pid=15327 uid=370 src=119.12.195.180 args=rwqw oifbe3ril/k/z3 3nunzzrj0zfv45ke34fhlle3cose
  - Log entry 91138: process wget pid=20816 uid=851 src=62.173.240.14 args=okwf7jzjnwx0-wraoei2erlisgd2ivof3zylopjrhs-l1nt3
  - Log entry 56348: process sshd pid=28748 uid=901 src=180.81.61.69 args=vhzg-9rj60r 6q3v1knqfob451o3q6sit1fsuyyktdeqhueu
  - Log entry 58976: process perl pid=16545 uid=521 src=103.75.200.234 args=ry5x5uqr4f99x3d7tw1yfz d/-i9a02fkp8s9qmbckkypwk5
  - Log entry 69928: process nc pid=2281 uid=882 src=207.153.151.163 args=t8evr4ojp8zx34xb/e3o7eoo bsxb0r//4bj2xds7r1z9vne
  - Log entry 75540: process python3 pid=24948 uid=500 src=202.17.212.126 args=v5e7ybnx7fiyr1/k1k6 u6s51vp04uu1kmwy2jx2ab3ac836
  - Log entry 87070: process python3 pid=23382 uid=814 src=218.71.142.110 args=topbt3hioq40ev7qhoy6-ub6a7468jsl-poreyp60n 1k4q-
  - Log entry 35411: process ruby pid=8048 uid=145 src=24.6.6.79 args=4vlg-5we3b/mkpw7h79dho2r0vc-ne9jndi3hvx3j3su6dg4
  - Log entry 18583: process wget pid=12554 uid=986 src=168.195.212.11 args=ue2z9hzo8/salhu9aetwo i3jj 3t 0ilommb/6n00cy11qw
  - Log entry 27580: process nc pid=14563 uid=758 src=84.230.209.41 args=ly-8b147g foy-x6mc4rvv7xws1e3dkgny8/-a6 9i 1mcg-
  - Log entry 12469: process python3 pid=24207 uid=39 src=179.37.109.104 args=c08tv1 jlsyqs60e8xeild7inxw/1gvbott1ny1216qi1zrk
  - Log entry 65105: process nc pid=3991 uid=818 src=201.240.66.96 args=78zqzhsdq-t3c08c738xcmt2wu980abbd6zfcpfl/iffnqwe
  - Log entry 49335: process perl pid=8575 uid=301 src=138.151.33.217 args=ejnc1qjb0i/-k7f2pjpqm4c2gt3yswf3lq g50e89ojeue6c
  - Log entry 15038: process wget pid=4474 uid=140 src=142.212.169.206 args=7 d7il9bj5qqzwo8u6r9ucgv9c0k69/42xocdnxhkzpz/4 v
  - Log entry 65152: process socat pid=1440 uid=227 src=127.97.164.38 args=sjyuo4itqt3eh-j84m7k3tmphiu/gdsptor60xoa445gdsln

## Supplementary Technical Detail — Section 40

Automated correlation engine identified 17 related events in the 6-hour window.
Baseline traffic on port 41666: 2 connections per hour.
Observed traffic on port 4444: 97 connections during the incident window.
Statistical anomaly score: 0.951 (threshold 0.750).
Related CVE: CVE-2026-17166 — not yet patched on 4 internal hosts.
Affected subnet: 10.10.2.0/24 — 5 hosts in scope.
EDR telemetry: 1 alerts suppressed; 2 false positives removed.
  - Log entry 17845: process curl pid=3293 uid=956 src=143.146.127.173 args=r/7pzkv4jqewsyzjake1mznu7sfakqh1ll60nvm3dtr75/zm
  - Log entry 83978: process bash pid=9281 uid=325 src=198.219.231.46 args=8ck0y2lbnoh20 dngur15nrdfvht-j8a6vc1zfvi94w4x2ly
  - Log entry 15586: process socat pid=19313 uid=632 src=156.115.28.73 args=xbjeq9qfgcg93pcb24c/dqj0-u7hu yizsyvg1w3rsfwb9xh
  - Log entry 71276: process python3 pid=14669 uid=785 src=19.184.250.194 args=3 7t726k-5/bn/3yx2h78wal5ghunj33-07w/exyira7yew/
  - Log entry 87605: process sshd pid=30264 uid=137 src=60.164.232.170 args=fhaxor5uh ykdqilr0shqfvsbtwwqggy/wjma0rnvpp35tlf
  - Log entry 58515: process perl pid=6354 uid=270 src=59.48.86.160 args=mgogbo2688c7m7aufaqtk60df45-swj uz/s-fse5obflylf
  - Log entry 76230: process socat pid=27544 uid=502 src=88.18.154.234 args=harazdfp-ogvc523ilsv1ybg7jkx/kmfa8058eo4igie5kcg
  - Log entry 94464: process socat pid=23799 uid=635 src=116.217.3.202 args=mpsl14rf/4uaeejse ieakukj4wc/rumwuo0prjjcjm6rpna
  - Log entry 98468: process ruby pid=25345 uid=723 src=14.11.139.206 args=r9sbikxxtfhuhvekf2op 45fdz-5vz62pxvvsesvqwbqxf7j
  - Log entry 99990: process bash pid=31737 uid=858 src=35.240.143.249 args= d1m/lzr-9rbh-aos/wicb-l8z4t9aq77u5nggxm h73b6gs
  - Log entry 36458: process curl pid=25690 uid=734 src=57.85.21.63 args=jumr23v26xt--acg63c-wzc6cx59 xv/wklgb6p67609jd3y
  - Log entry 17067: process curl pid=15254 uid=211 src=184.42.52.48 args=g ta7miy8w8etvdcjk6xt4kcmx9l59q2p7s-frqc-9n-ab9c
  - Log entry 87040: process python3 pid=7486 uid=883 src=222.15.86.220 args=53 3a2jztpueoppxff2v41zdiul924ijua19q1acbcs6v1ct
  - Log entry 79482: process ruby pid=12788 uid=668 src=181.115.74.209 args=w6o 3o5jxpy10n6hib8io p8m2mf87qji66b824a9q873lho
  - Log entry 13327: process curl pid=23641 uid=146 src=106.218.250.132 args=2piz324jn8ng1uynoizund303q7-o0hyw7r3gkqzl5re7mwi
  - Log entry 32031: process curl pid=27081 uid=368 src=54.123.32.227 args=wah3ujn-idw/4/ui jahewlonfjjfgf8c3bvb4nmfn512z7q
  - Log entry 71029: process wget pid=5523 uid=545 src=157.155.162.40 args=yf55 50gcaigezu5lcx5vs6tzzyzri0l-3yj/f wardq2syr
  - Log entry 44451: process ruby pid=11117 uid=470 src=157.134.253.237 args=bm3bnsx e0ez4egzjuym9mp/8n25/5g6evnkts3usio2ksd2
  - Log entry 78218: process python3 pid=9213 uid=876 src=74.7.130.208 args=lo97--1r6phb/5tfhjerijp1ndrvenv nlec3meqv7rdotg3
  - Log entry 56199: process curl pid=31718 uid=311 src=129.153.161.45 args=jbrv/yo/kemjndshygczck8-iqk4efp34iwywb4aemvmocvm
  - Log entry 86109: process ruby pid=21862 uid=364 src=67.214.90.82 args=3cjitj9a74llzwmq81sutq/jyoky72hijx9xzirhvj1311mv
  - Log entry 13198: process curl pid=29699 uid=388 src=16.201.12.157 args=-hnkor2ntrqehfp9hqe23q7fa-on/zczkvtlepav96/lvi92
  - Log entry 46842: process python3 pid=25057 uid=199 src=106.181.76.232 args=g-3hks0ftnl1jporqjzynsydtbx8-/4s-595069v wv0l6uo
  - Log entry 89303: process python3 pid=12887 uid=833 src=6.255.141.203 args=5nirchy-igcc2i1/oquczk43ixju-hnloqc c1bdrssh5odf
  - Log entry 72414: process nc pid=8708 uid=826 src=167.219.203.92 args=u41dhjk5vux64zhaerimu6l41jspdafm1o3oka9nfot0-a6b
  - Log entry 75710: process curl pid=8662 uid=515 src=53.54.23.153 args=g8/665o07zk538givotvxrm m54owv5/u879fcrrgzs6bnch
  - Log entry 95355: process wget pid=29251 uid=472 src=80.7.126.166 args=/y/150e//9wrdj9e7nt6n1g0fgep-u5pe/4rv5paqv-busd3
  - Log entry 66180: process curl pid=22489 uid=685 src=25.165.139.74 args=mu0z 3mt3chls6axfd-5jismfbikjydqnwd7ceyq3ifi svf
  - Log entry 25471: process curl pid=31284 uid=388 src=12.52.230.117 args=t9syutsvvdok2no45bc-3cky49akgq6l4/4 9uuvwaheba1w
  - Log entry 32916: process sshd pid=14775 uid=622 src=90.109.69.203 args=80zpgwe/82ln2rooj4yq0h39quf/ge1y44nxvd4t0-ba7baz
  - Log entry 21649: process wget pid=31660 uid=629 src=179.175.64.139 args=ve-yuewu596xgktavz13j-n- lkfkkcezy0k0zjv/5vdxgab
  - Log entry 72161: process curl pid=18863 uid=853 src=156.47.116.214 args=svamp uebkq70//cb 7jimzojpnzy3i-b6ruj9pywkat6ngt
  - Log entry 43810: process sshd pid=16086 uid=621 src=89.243.183.97 args=vusellgv0pbyb//j94g1rnf/ej9y-1 s9mctki4x6-3km-km
  - Log entry 50475: process sshd pid=8943 uid=264 src=58.59.205.135 args=9di1mhv-eie60b3h8 27axlb wapn52z//jfb293xklsbs7u
  - Log entry 73750: process sshd pid=5768 uid=421 src=16.125.102.23 args=f14a/ z/ega3hhd8e5qarbounjarf8yk7coyt2v61p32eo/o
  - Log entry 87230: process perl pid=11370 uid=262 src=107.217.120.171 args=tmgv5if8h0m--euyksvfwxxqxeq/8-cg717xbe6nu5/3 /32
  - Log entry 30866: process curl pid=12940 uid=560 src=13.213.49.244 args=cothdcz6prhe7v7p2ifh01byvyqp57d-3x7yl su1q0th/qu
  - Log entry 92403: process bash pid=11088 uid=936 src=10.33.142.155 args=tw33uvr/9ep3pd3kfquaev7h1jzu6u902fucpfg8tqs9ezjg
  - Log entry 98738: process perl pid=29639 uid=827 src=75.224.153.236 args=sgrr1o2l8seofkh-1xzobps/wxvt0-6yqvaqr2n1g06ul5rt
  - Log entry 94403: process nc pid=23416 uid=466 src=24.144.162.150 args=4b 66j0aochhtq5ol/-cte/1ut3u/d64kew17ym9dbznw5hf
  - Log entry 61797: process ruby pid=14149 uid=336 src=33.117.43.198 args=znffexasmxp9t 8d7kivr6rskn5fej-7bdkxj-y9vl2l80gp
  - Log entry 32914: process ruby pid=22014 uid=317 src=31.171.49.139 args=qrp5tqwq oj/1rip8fn-j9exb n8hcdf1cnjhxs8-vgj1vv4
  - Log entry 51166: process sshd pid=29654 uid=615 src=104.247.154.57 args=wkahs2ctfvxtpoemwfrdxwn2j5x9lvxj9a4lj/dlinah3syq
  - Log entry 78110: process socat pid=27911 uid=948 src=184.16.81.75 args=urp67j24uqkr ervcwtd/6knajslk-q2o-dc6pwfx6ds68zt
  - Log entry 89320: process python3 pid=8038 uid=569 src=111.222.251.69 args=xf2kboc29whuveeo7qsk9goyx/6-p8uhp/6yxgmwrrrkjxm/
  - Log entry 54477: process sshd pid=15378 uid=472 src=192.155.23.76 args=b-re6g/hl6dm8gqbdh4-ue/5pm gqzwf294nq1fsfug4jri2
  - Log entry 94625: process socat pid=2583 uid=429 src=64.13.114.239 args=u653fhkgc47 y-vvw-b7ftyox v7p7a7d6mtg02w ws-6k6k
  - Log entry 10493: process sshd pid=7586 uid=375 src=44.120.70.96 args=/32kvb8kjy/76vnljcswjkx0fc10vij6azxskpsaongz-/op
  - Log entry 16358: process ruby pid=22716 uid=443 src=96.242.122.149 args=ff853mdrr us-lu/xymjv-kpvecnq2na5j37uqa1xb2zn4rl
  - Log entry 31083: process socat pid=1076 uid=236 src=62.160.253.84 args=wq7pp3gkfartean pnmttnzc9szgiz881l74mc8 bir/hh4-
  - Log entry 15028: process socat pid=10637 uid=38 src=117.59.109.192 args=7/g2r/nkmy3de0/k9mh5722i2-nau4cj9wf87kihcaiohdi1
  - Log entry 41031: process sshd pid=31827 uid=959 src=141.227.126.12 args=6us ij i3hmfs7b77u690v-elzd2ivsfy0oa8b-njnv/lbt1
  - Log entry 61861: process ruby pid=25403 uid=600 src=51.28.175.210 args=mllyq121rkuz6vn/s1x/nb-2k16f9sp/7pi55n-fo4ppj 1p
  - Log entry 72648: process curl pid=13810 uid=219 src=204.0.233.171 args=ahbvakhysx h6ez/jev6nhk-itu-8r-haz7ad21uhxn9ddrb
  - Log entry 76889: process perl pid=23799 uid=508 src=221.119.50.231 args=to79imvyxnb1ga343n4y5bfpb6tzv5mbwaes4v kju-9-1jl
  - Log entry 12639: process curl pid=24472 uid=826 src=126.7.9.144 args=1s-sco06kkpgc96jaugzuuj7nz8x1mf q4jsd7zjn3ntiasw
  - Log entry 76347: process socat pid=24767 uid=819 src=11.108.60.56 args=le-w0vj7n2k/py1z041kksajm3vcnxq59mnt5zw/ia5/zg/e
  - Log entry 80413: process python3 pid=23821 uid=275 src=131.24.36.26 args=3s9i761bmvvdlmumlec4q92wgqoas4jue6/r8uo8uk1krimm
  - Log entry 28006: process wget pid=30719 uid=813 src=119.71.9.205 args=ayax 2qvap/2k1andic/xg/khu5pkhb0uorgo2-6j iruq5x
  - Log entry 85590: process wget pid=2685 uid=858 src=78.124.69.55 args=vvvq-8zb9gehzk/-qef/e0bix3jzoyqo33s -2 3fjhmqmnb

## Supplementary Technical Detail — Section 41

Automated correlation engine identified 22 related events in the 6-hour window.
Baseline traffic on port 12576: 2 connections per hour.
Observed traffic on port 4444: 182 connections during the incident window.
Statistical anomaly score: 0.913 (threshold 0.750).
Related CVE: CVE-2026-20149 — not yet patched on 15 internal hosts.
Affected subnet: 10.9.3.0/24 — 17 hosts in scope.
EDR telemetry: 2 alerts suppressed; 2 false positives removed.
  - Log entry 51686: process socat pid=23851 uid=138 src=26.228.220.192 args=6ek9sl1w-em5ke9h0101i/qjr/vbm6ng9oc5kr52v8fib-l7
  - Log entry 53781: process sshd pid=5964 uid=362 src=103.177.174.104 args=w/qtvaxo6/p4g -we4n8r i00urn1 j/kgjwncrqw8ud00/4
  - Log entry 67493: process curl pid=24904 uid=58 src=196.53.89.66 args=y6bw20acydetb zowffqv9pqvidcohnhe6lcz3cv5s94sd82
  - Log entry 83444: process nc pid=20402 uid=622 src=46.122.159.93 args=jqcezmsw1by-/q8iv02/9z4oaxldyxowtky 74y14bz9a/-0
  - Log entry 79948: process python3 pid=11124 uid=434 src=45.80.76.229 args=nb 1ur2xym-7jipbf/eiu3cpa9iocyzmi9-km6p75ysc069y
  - Log entry 24978: process nc pid=15373 uid=321 src=221.147.211.107 args=fnyu-p0a4nb8ntvocja0zg60nofq/0avskeei9an09t35e0q
  - Log entry 34585: process ruby pid=10341 uid=219 src=200.23.38.42 args=z3-83o4b4 dwkg-jordvb-a3jve9d1/m9t/evd3d3vwow33e
  - Log entry 73284: process bash pid=29609 uid=77 src=150.33.78.172 args=u2roev12nmt0u0ceah9hjg6-f7aq0hq6gdis/l7kfxkxmn r
  - Log entry 64206: process python3 pid=18900 uid=104 src=4.227.128.178 args=xcpupm0ehtguh4js7ld55m/yjj--bljwywb506wg-3e2-ip6
  - Log entry 17353: process socat pid=30209 uid=196 src=189.254.55.23 args=151z0jkceum8isd6zfsibcwa6q8mt g7zs asgbdk-rd5xwq
  - Log entry 18913: process wget pid=13389 uid=877 src=88.165.35.70 args=-gq3t2cal7z96ukzwi3pbz3eskkew3d2k-bh/vqe68v2oqgt
  - Log entry 94622: process socat pid=22317 uid=890 src=185.17.117.247 args=o3s2f/u4ejv40hj5lsmdwsf8e0tn3ga08r7wfcolxfgj2c4n
  - Log entry 46776: process bash pid=30382 uid=591 src=152.141.61.224 args=-1fp9jrx6sithpy5bpxrd5fj0evd9m91z-d92vymsx5y90wg
  - Log entry 96896: process wget pid=23234 uid=517 src=43.218.211.11 args=c05n6z38tvp5z8ak1d/gdd16lf9hwx 4fi14nrj8k7uykjs6
  - Log entry 53214: process python3 pid=29340 uid=771 src=167.228.20.223 args=0q4mjavr3l4l-lf75ro/pwwqj1-w/j0l3yndvkef4rv2-wru
  - Log entry 52367: process python3 pid=30833 uid=782 src=90.220.33.113 args=fklcp94xhwm1t-ueh6pyneimibxc5q6x36o2x65korp7gz5t
  - Log entry 63912: process socat pid=30780 uid=498 src=126.215.29.216 args=-/nt-etg3myse y-b4ipd3ulf8h1dyquua6w79zwvbc 37gl
  - Log entry 46746: process nc pid=31820 uid=404 src=16.146.55.110 args=9w5s4l5edt952 -nlwgjox7ncy9kbfus967i-0qjn 9h bdb
  - Log entry 48874: process nc pid=7976 uid=403 src=169.84.29.205 args=xiu/6i-9sz5mzuk0pxs49jmqlyo1eo2btw81bq14w2lyu4-s
  - Log entry 37515: process nc pid=6801 uid=215 src=116.171.196.205 args=rsn2 ahjb5bgjozo4b/v9ceezz-9svs78w5ctkg0f0388bcj
  - Log entry 66163: process wget pid=2558 uid=699 src=46.26.49.55 args=mxybxy0ocoxs3jzzb9/f9hm7wgsdm477du18j2emx6qotdwa
  - Log entry 56534: process ruby pid=15753 uid=535 src=152.152.113.160 args=3d5sm54sitf4w0i5o/m6irjl a8mg-/ 6i3cqfafw 14/1eg
  - Log entry 37062: process socat pid=7788 uid=293 src=28.9.130.27 args=dwsa7/ kvas4dgzi4vq5zadfyt/fi1wc2v2u84oub29ga5o9
  - Log entry 55610: process sshd pid=17158 uid=350 src=204.44.57.151 args=5/80kqqb5v88rslqw9m-wd2e-g2yzs- 0uni3opov9erxkw7
  - Log entry 13555: process python3 pid=22058 uid=406 src=21.210.82.203 args=jbwkc3hmof22tf9an6rof7cbafwc1pm3q9wvle4p0hutug/1
  - Log entry 35383: process python3 pid=13338 uid=962 src=22.27.70.58 args=p0f7y7j 4-8v1zrmcgooe-6sqwk5g4-j5fi34h1tfp8pvltx
  - Log entry 10581: process socat pid=21511 uid=93 src=172.63.36.140 args=ajztj-ivtazqcuhz-d280j 2klhuvxoh3bz/4m5krd5teu/ 
  - Log entry 11467: process sshd pid=7798 uid=411 src=86.128.202.237 args=jop//evr/ 41qs8 al0/ l2b27gtete8mg3qgx0 3nn4ybfk
  - Log entry 93952: process sshd pid=6289 uid=929 src=122.223.70.3 args=m6oj795lyc8z-zyx0cbf fr0gbc-e/4zgnav7n7duhcy8ayo
  - Log entry 67404: process wget pid=10283 uid=97 src=51.147.94.177 args=/tq2gi-nuxdv7xyghrphy-tjqy6yn56ik6x7g/se2gn-nmjx
  - Log entry 49033: process ruby pid=14806 uid=932 src=169.23.39.188 args=dao 567dsmn1yp4ust7d-x23y-efe09r6pnv hv5eiiw1mng
  - Log entry 39481: process ruby pid=7695 uid=101 src=130.161.199.93 args=7xx8xfkp063-qpy8556a3i2gfawq7g1s7e 0u3b3/f-h8j8r
  - Log entry 79547: process wget pid=13769 uid=476 src=69.183.194.215 args=wyvi7nx40di/v6wmr1ctpqspc xunihyx plhbl09 wq-asq
  - Log entry 21522: process perl pid=16719 uid=615 src=24.221.65.100 args=e8 ql2qdcz2g/j3-sgb7tj3xgb3774rig93hw/qn3gh59j6/
  - Log entry 33524: process sshd pid=5735 uid=623 src=148.100.98.74 args=m9b--z-n2q3-7yplcbngca0fjdsc4gvq-g0 vdvkj1vqrpxh
  - Log entry 17603: process nc pid=19216 uid=500 src=32.163.139.242 args=xjzr70m7mkqzk7 h6ci64x6206 iwjtpyabhtc7lspen icv
  - Log entry 33471: process sshd pid=5344 uid=703 src=53.85.180.19 args=7kmy713tmkn34z5lmu2lj96w3bwhp61/5srhzcgi0dtao562
  - Log entry 50497: process bash pid=11373 uid=951 src=34.11.91.216 args=4uaxn6xvzb83d3ip cbdvugdfrvv 7bjkak81kc53grqyxz6
  - Log entry 21182: process socat pid=22436 uid=663 src=9.59.118.172 args=z0aapouhp4w6cwbpmr uwt-/ph29mdzief61lpwjl4uuo/ew
  - Log entry 45725: process curl pid=19349 uid=373 src=179.12.170.42 args=l3eyjbdzoe7s/069y 2c560zjb2usrxca29xqi2s51s20okm
  - Log entry 11639: process nc pid=19669 uid=159 src=43.153.104.153 args=k02 wewhwgs73x c2jynlfoh5e00unhw4ig8cm8ktc3e6nwt
  - Log entry 20915: process socat pid=6237 uid=243 src=157.47.204.44 args=-8kniz2n59b2e9gjmf6h /gs2pbdtxng2n6ty/te09hxed/r
  - Log entry 26284: process nc pid=31662 uid=437 src=14.152.105.63 args=/o8klebcku9w1t443tj0m7zp-61huz9qa9vb3cqv4r8bk20m
  - Log entry 87790: process perl pid=24642 uid=437 src=105.104.42.81 args= qt4bn4-w72t2pbgqqrrqjp176tv sof8q2f28ej0qbdf90x
  - Log entry 27618: process wget pid=16593 uid=892 src=135.28.187.39 args=ggrh/q12laszii/bos0sti w5tfagrb -ugjthlr01r3uijz
  - Log entry 78911: process python3 pid=19102 uid=434 src=17.249.19.37 args=lay0fw5a7u7k0604209jeq673m0ts1fr13c4qn22/8 63 8b
  - Log entry 18337: process socat pid=30735 uid=245 src=38.211.146.245 args=/uoxd4r6wncejyci3bob/k7t8ko jvcx68y/- 4itegftui-
  - Log entry 18131: process curl pid=29991 uid=768 src=41.102.181.183 args=jvehf3aw388r/840 x8uzqaa6xo1lskclmzop1w59rl1t0u7
  - Log entry 78139: process python3 pid=28705 uid=340 src=166.138.129.23 args=0a2s us mi7fgw-n881maay3o9 glaskg16b6r-r65vcpqsk
  - Log entry 58873: process socat pid=16014 uid=295 src=193.67.101.234 args=rpk1-1en5/armdgobjc-0uwt7sqvlra94waivxusn4z3dpfd
  - Log entry 34502: process bash pid=15789 uid=228 src=91.198.118.75 args=r31va2koe7j-sgmj0oip6mh/m3v32 xe1dx73bkqk-c7/g21
  - Log entry 97651: process python3 pid=15245 uid=245 src=43.89.199.234 args= gtynayig86vq5dcq/3/53vbvazvsuu7z5fml399ewb6nnbg
  - Log entry 82720: process ruby pid=18941 uid=330 src=195.152.112.248 args=/vbot-kkuyhnb6rfd/6t8dm7rl rujw e0a1tbezvky9gg2/
  - Log entry 33613: process sshd pid=7734 uid=147 src=83.74.66.95 args=mmn5v3/lf13eh55k23i3n 7/6tk11n0k1qzjbkqe r-we1gd
  - Log entry 81035: process sshd pid=13104 uid=934 src=47.243.67.183 args=8fsnutaoovez470fgiy7w1/eb6anhlm1umhks33fq-x46v4y
  - Log entry 13045: process bash pid=11896 uid=806 src=20.249.240.109 args= ru 7a80ngx57kg08b /9-txvvxuw17jwoy8yxbhgflefo-b
  - Log entry 49315: process python3 pid=27504 uid=406 src=89.101.122.212 args=az2h0vu4x7db3l681m9cbr 6--cn55 eupzw2-yru883l08l
  - Log entry 92730: process ruby pid=26967 uid=234 src=49.222.179.242 args=rs7mckaggzfgssu877x3lx0 7n8xcgijqxaud/w7rabr1tjy
  - Log entry 49100: process sshd pid=31838 uid=889 src=122.140.220.207 args=xtp7uysh gdkkxwr95wzvo3rc0cdok3yartargsb3ar2i9ff
  - Log entry 70470: process curl pid=29419 uid=589 src=52.81.253.73 args=cj2jvymrto j/fi/-x8dnp0duv s5g5o82hkc/o8y0w1f1q1

## Supplementary Technical Detail — Section 42

Automated correlation engine identified 41 related events in the 6-hour window.
Baseline traffic on port 32564: 4 connections per hour.
Observed traffic on port 4444: 174 connections during the incident window.
Statistical anomaly score: 0.802 (threshold 0.750).
Related CVE: CVE-2026-32630 — not yet patched on 18 internal hosts.
Affected subnet: 10.1.3.0/24 — 8 hosts in scope.
EDR telemetry: 0 alerts suppressed; 1 false positives removed.
  - Log entry 52539: process wget pid=9603 uid=180 src=101.243.8.4 args=0dt9di1wjrmxk0w1h90mobf1pltbnyotz0u7ke/g99q/tc47
  - Log entry 49659: process bash pid=8058 uid=702 src=125.16.124.226 args=1wsqrc6i 804h1-1g7v76n9158jj1lceyf0gow7zj37gecal
  - Log entry 22400: process nc pid=6260 uid=910 src=121.18.80.240 args=x4sesc 73t3kk8xf/oj r57-ld5h1g1-he5hdcvmhrwyl g6
  - Log entry 32755: process socat pid=17665 uid=425 src=129.2.139.194 args=06vxt-t3-9iw93drhb71mwmz5qxwex-dj4p-5cpr/g1wtt2u
  - Log entry 58707: process nc pid=17932 uid=554 src=75.156.240.116 args=uyi glixlhtiljm1lp lx2qmx9z54-win6ji/2f7zkg70mj4
  - Log entry 72938: process bash pid=1648 uid=168 src=174.100.147.50 args=qtqtds80ic naf 2g7wur3y/1m-hmjm-in77o6j51o45c877
  - Log entry 78769: process socat pid=25042 uid=272 src=172.131.19.180 args=zhgt1p-hzn0zztjmyzf27kn375e8/mrr42wjfhapef/6fxyq
  - Log entry 90402: process perl pid=20470 uid=749 src=33.62.68.250 args=p7kd x95zo4p/u h66edyhgrhcj1t4kidwodr-x66ca6xu0r
  - Log entry 99154: process python3 pid=9785 uid=744 src=54.0.12.150 args=1ih4/cf t0sd e5l556ftcoerpyno135pvq9opcyi0jqzlfs
  - Log entry 67647: process python3 pid=11360 uid=568 src=58.162.148.40 args=og2ml9gisovx js/t 7ak350-0r8w/dzvks5gduq3r33/j/3
  - Log entry 94689: process perl pid=3801 uid=468 src=90.72.144.126 args=grfd3ivz/oohniof83k6p32z906sztj wmt mg45a2bacuge
  - Log entry 39732: process bash pid=29705 uid=949 src=175.184.145.158 args=31fdonzaintv1fpi9nu5imkmgdgxo5evfg1czbqyj1jbfl 3
  - Log entry 66594: process nc pid=7145 uid=394 src=130.0.59.250 args=tu/bj c-lvfuntbog/mggmll wgmig  c694od xjmfxrsx2
  - Log entry 29697: process curl pid=15583 uid=368 src=157.9.190.157 args=wmpoqonlk7-bruscjrnxa4/yg49r0lcn88qf-hv0rcmr-zha
  - Log entry 71288: process nc pid=4693 uid=32 src=6.88.130.244 args=i3fms8jx8euosg0fgbfc46gu58p1f5b1kufvsrqu4wurxx74
  - Log entry 27344: process wget pid=17206 uid=524 src=147.74.215.183 args=044o/xliiuif-i/8p24x2n5gdp7l-bn8clcydng66js5blui
  - Log entry 37807: process socat pid=16978 uid=65 src=12.87.3.181 args=s70efhmodfb-8epccwznbc9pa39sx 34acg/ /6jjuyv9-x7
  - Log entry 71215: process perl pid=25428 uid=503 src=69.136.145.59 args=7brz/fgtppozm416rtzk8rt/xqv-gxpa3myh9gxbexfqo7/z
  - Log entry 89270: process wget pid=12045 uid=480 src=95.147.5.162 args=xuuv56zf 6pslgp8 vz9uj0g ch9m/uqe4yo9ouozvfjxa/9
  - Log entry 77274: process python3 pid=20403 uid=553 src=212.172.196.115 args=fgf9uc1qmno0lh5noc9a0ble8oht70u0ez41w9as/iu7od17
  - Log entry 46488: process sshd pid=11650 uid=577 src=223.35.211.172 args=j3f52jrf9bc5mrasm55unn o-htpq/z 8ncovjvxtp8rxgo4
  - Log entry 34903: process wget pid=21744 uid=911 src=120.27.23.234 args=8gwe6ncjoqtg4f-fnaz9brav7tx1n-mlra0s6oasc hxwzv3
  - Log entry 96159: process curl pid=30846 uid=386 src=25.110.77.86 args=quvue0x 4ac7/98s ok9 561qlp06tyk0pai4q/cocrlav-o
  - Log entry 34363: process python3 pid=5147 uid=732 src=68.165.30.209 args=ssyo/ zh/4yv2yqxzhpbomo0d yynw335t0/2yfss0y-tyrl
  - Log entry 21865: process python3 pid=22455 uid=46 src=151.232.110.58 args=d/-wf3btop-mnw q9cbvh8cc/dufh0tq0-2-kvy2anr-hi8k
  - Log entry 39743: process wget pid=20193 uid=955 src=73.22.151.252 args=vga7jywc6yb9xs-h-w/2mx6kx1znl r3v6c bhiazrctcpz6
  - Log entry 89431: process nc pid=8700 uid=121 src=98.131.190.23 args=skcftsozcqq857xn y9ua0iwz-hhlyiwh/chwnyyvl4xtvgm
  - Log entry 30725: process ruby pid=15191 uid=371 src=3.134.105.163 args=yjr0-k0hx4bmzaltwbcvzv-teshmacvt7xf2fc71dkb22uz/
  - Log entry 21635: process python3 pid=22544 uid=534 src=56.86.92.13 args=k6pshlz7xnq2jh3lf/hwp8o07ovkfs7g13be3r709w2wn674
  - Log entry 53996: process wget pid=6229 uid=353 src=34.212.113.144 args=w14x7fj2ck8qqe/qsq18b2 6nbpl6cj-rioblgqwlnccad7o
  - Log entry 75781: process bash pid=31973 uid=212 src=190.194.57.86 args=hmso2end7pg3bcxkoy5oldmdjfud38bm-lc9azo380fg4ijt
  - Log entry 63464: process wget pid=27205 uid=815 src=55.203.63.196 args=elgiuvw/- yyjj6e-olsib6 9c62ahsb-zuw0vqtxuktzab4
  - Log entry 30911: process perl pid=31341 uid=814 src=49.62.127.165 args=zo4obnbd8b6h7cf5c8 pdf0 bln3d1rump 4k6qbmx-da2i7
  - Log entry 38304: process perl pid=26498 uid=700 src=55.230.38.189 args=eeoi4o5ki7xleqsnjreeval2r44yhm/qucw7ek/m90oo6e17
  - Log entry 92252: process python3 pid=28887 uid=480 src=12.244.228.52 args=ge5cqj msrfeujiyy63/vgx4lgp12o mp9uo9px37j2khnl2
  - Log entry 59386: process sshd pid=4903 uid=327 src=129.105.65.172 args=k7apx 01tv23tnsupctc5u8s763uu0luv90dcke145kwdtq7
  - Log entry 65400: process curl pid=12083 uid=584 src=87.241.144.4 args=6z//8wm4uph/yfxydn4pirwgyfhtope6346p2cv274sa5fmq
  - Log entry 58360: process socat pid=1482 uid=600 src=104.36.157.64 args=1ndg5o  acb91px45oeg0 8kmbx55g2d6h0qsphltx7z- p5
  - Log entry 88548: process python3 pid=5562 uid=373 src=64.244.152.168 args=9o2yjzdw25-ak80z7r-mb3l4kez8-gj8a- 2- ibel8uzeub
  - Log entry 80790: process curl pid=17950 uid=58 src=221.120.120.144 args=3iqpbb-0pab0pf07lqg532qyo1y4m7kntjxf0-6-z082far0
  - Log entry 99684: process sshd pid=5393 uid=568 src=207.147.18.138 args=bto-b-902 h07sxnodnqv6f da20d45s-kx/4o/elvf10whr
  - Log entry 48128: process nc pid=16845 uid=803 src=93.58.196.140 args=tnmg v/6zvo yxfumk5hto89slyw6deb2i49spytsvi/c11i
  - Log entry 40073: process socat pid=23152 uid=455 src=91.196.170.131 args=bpfi254hango9daaku4lxkajun0iw1dqa1-72jdqmyr023q5
  - Log entry 29271: process socat pid=11137 uid=602 src=22.205.128.251 args=u8g6 nlqeipxt3g2hpk-13-j0znwmiz/9pg8k0a1l6upk ce
  - Log entry 83139: process nc pid=10799 uid=176 src=153.180.213.3 args=0gf27/ltu/yik8inkn7u0x08mxap9iit8z9xgty8o5kmszy/
  - Log entry 78406: process perl pid=11839 uid=60 src=53.12.227.102 args=oowgfhgjs6gr-kyrlqjx/ib-tcyeq6vqp 1bcuh82c-0 4jh
  - Log entry 37877: process perl pid=4434 uid=587 src=183.44.31.156 args=-bq8f-nw1fkw23uasphlqre6x psr5q9n2 03hv9sn18gdyc
  - Log entry 49973: process socat pid=8697 uid=819 src=115.250.214.8 args=30fe0qsf04pbq8wynej/0d88-04t/wxe6ee975onilxepka-
  - Log entry 59689: process nc pid=4419 uid=317 src=140.110.26.228 args=gp70cfb636pxs/s7yyoup4wbucvbvtt5ug 8xnj1pc7qvu3s
  - Log entry 48027: process ruby pid=7771 uid=313 src=91.132.185.241 args=ddqxup8960tq85276k 24gtz3c375s3wk3r-/4p3y-i6yd0u
  - Log entry 59702: process bash pid=3843 uid=879 src=124.43.35.118 args=ewd0i0v stjlre2/qoqnqvuw6acnm/un13k6-2sf81uu7ohj
  - Log entry 27734: process curl pid=1483 uid=704 src=94.151.129.25 args=le5/l/20 8hag1sdj9/c2wda8ydj2idzghj 0w0oi5-5aahx
  - Log entry 92637: process socat pid=20673 uid=836 src=88.86.202.118 args=ck9ut d717j9-w4d6mn4 m ny2a5eoguy/et/7ipm -5jjj2
  - Log entry 65426: process ruby pid=26457 uid=195 src=45.115.1.69 args=ifsp71wenidydaslfr4-sv94u 79qm8w h7a7mh -4/9ycow
  - Log entry 61854: process bash pid=18192 uid=486 src=222.145.74.234 args=zcchiim9xoh2eatw2 d0uy/qu3fnjqha9n5 xb p/4qf9psz
  - Log entry 54156: process wget pid=7107 uid=789 src=100.205.94.115 args=/hu1bcofx4qu9n8523u-rst5cuyng9v8vdig2as/roplyp/n
  - Log entry 81516: process ruby pid=13425 uid=43 src=19.202.125.207 args=mxuz99vdpp37p3x lq517cqg2amqoawgea2p4o175327 sin
  - Log entry 25931: process perl pid=12228 uid=937 src=70.144.198.227 args=po 4lsh8mu-1aydp0mg4-01i/e08 bgda-tiqq5kst7k  90
  - Log entry 39395: process wget pid=15359 uid=456 src=213.88.230.66 args=x5j8pfepmvyrxop5y6e-0t77n7jcfcdafdxjo0x26stmtd58
  - Log entry 89023: process ruby pid=27356 uid=76 src=109.112.10.105 args=l5xh87h wj/5pbz3n50k2 o txtjn8vq8i0a54lkgj08/se-

## Supplementary Technical Detail — Section 43

Automated correlation engine identified 12 related events in the 6-hour window.
Baseline traffic on port 21975: 3 connections per hour.
Observed traffic on port 4444: 171 connections during the incident window.
Statistical anomaly score: 0.953 (threshold 0.750).
Related CVE: CVE-2026-42282 — not yet patched on 13 internal hosts.
Affected subnet: 10.4.0.0/24 — 22 hosts in scope.
EDR telemetry: 0 alerts suppressed; 3 false positives removed.
  - Log entry 97436: process curl pid=4530 uid=884 src=58.17.39.89 args=barfb7ntrtpdc-sfu2d-/b-6cs0roezfv5v71mss2o9exba2
  - Log entry 66441: process ruby pid=17135 uid=812 src=93.219.99.16 args= rxdx6zjjujs390lbapicxsg09/eedm7v3k/4jswqk0gw0ds
  - Log entry 58018: process perl pid=3270 uid=891 src=30.237.133.107 args=i8eqwgjjyfn5gtrse8zhw403o3-9nk/2dnx483po/0x/c8t3
  - Log entry 18881: process ruby pid=7651 uid=594 src=93.108.89.160 args=2 4f6eqv2lxna0r6g 5z98c d 804l/923sq/z4e7x4uqnjq
  - Log entry 54196: process socat pid=26514 uid=94 src=136.74.31.111 args=8a2x4q3 9259f lq7sqgupldx 88kdr/3rvkirkajfsb5vd/
  - Log entry 86906: process curl pid=8571 uid=166 src=39.158.7.116 args=s2-sylpse0-nciaqwdezd06ejiwgq/i//6aowb4ub2p8jydk
  - Log entry 15435: process python3 pid=22700 uid=340 src=152.242.205.36 args=p44flv3y-nb53qecp8at0j45mrtwkh8hh2k9v//-c1mcj3eb
  - Log entry 14031: process python3 pid=14428 uid=687 src=76.33.91.120 args=6pmq51d7d-7b410ecrpm24idq-1176m/kea3xdo9j7lx 93b
  - Log entry 47466: process curl pid=8002 uid=398 src=164.137.34.127 args=kzwjjw1t /ctx8qm45woqp2dv5/h0wnb j/2ud esg/na6ua
  - Log entry 41574: process wget pid=24174 uid=7 src=4.193.114.11 args=ap/m87fc7xucqgggrhn77gmgs-e63kcf6kowb-m 0ybktbe7
  - Log entry 12255: process python3 pid=6104 uid=899 src=65.8.248.222 args=lh0kjb-dioal1hr 59rp 0nnft9mtl ds10696mkp3cy9mj0
  - Log entry 41038: process bash pid=1578 uid=265 src=90.35.11.86 args=1/giibquog4dfcu12c2ucu9gia5g2jzxf6whadu7vrl3mbs3
  - Log entry 18940: process perl pid=2191 uid=661 src=146.12.48.133 args=uckjj6gzr894ed48sqnrxg9nt33su6pd sowtbm8rw35xuq1
  - Log entry 74624: process sshd pid=13749 uid=893 src=152.239.250.10 args=7pqz5pc2epq4/2nvk3rr8hzhn1yobjbc/ksn9mvj/7vbvpvo
  - Log entry 80825: process perl pid=4498 uid=960 src=53.205.35.70 args=f ho-4pac5tc01r51nck1shevc0e0ykjskv8wdql40vlegyv
  - Log entry 44163: process nc pid=17839 uid=497 src=191.181.212.230 args= gj/q3h1zztttbimb-z60yq8qrls0bxn7mg0ce /wop/i0u/
  - Log entry 34587: process ruby pid=21259 uid=370 src=37.82.26.94 args=np538sli0d749ei/hy7oglv21qj3/0xclai07uynuts-hamq
  - Log entry 34302: process bash pid=16971 uid=494 src=198.210.150.241 args=5ah81tr0m1czshl5kr10cuo w 6j/ox0l 5jfv3174e2y95r
  - Log entry 11119: process socat pid=6551 uid=883 src=11.223.140.25 args=908wtlcspxyefbwx8k rmt7b3v7aglgo-rdlf95ta a jpgf
  - Log entry 49580: process bash pid=21758 uid=270 src=70.120.84.179 args=ahsltrbqfzhi2np636olrfoo169po00t ew0z 76dv13ktrx
  - Log entry 66685: process wget pid=30007 uid=656 src=157.166.168.58 args=7luxl5ke  4za3pso9nb0k7tq4be1e//5chq2v5s-oxriyqn
  - Log entry 13185: process nc pid=12333 uid=5 src=164.181.127.156 args=j0ps8iwiv85zv4g-rc261puoemo6dz-bwjeelm7teir7cjw8
  - Log entry 60012: process nc pid=16122 uid=637 src=81.115.30.81 args=i4363/gph70vv124cfwqkjk2ksu80l vdarxv4/hp8 6oo8q
  - Log entry 89396: process curl pid=8848 uid=188 src=183.189.122.205 args=s6ltsabtg n7 xcjlvqjj5j-85p1pk6rjbmict15/ ws-3wu
  - Log entry 97538: process nc pid=17889 uid=353 src=165.57.183.21 args=s50nnrzg8b2gym6ytt9yy7-exk/odm9v/-9z42f0w94i4n 1
  - Log entry 47516: process python3 pid=1987 uid=938 src=59.96.66.75 args=5abs22jh3jbe9kkad4e/58y9awlrwqpr52lvzkcpon0qcv l
  - Log entry 89248: process socat pid=6099 uid=527 src=203.24.137.50 args=o4 eif25cp7uc844ink0d7uovgirqiym10nck5g94hka64nj
  - Log entry 32731: process nc pid=16928 uid=62 src=25.110.227.108 args=qdl zd37/d95ty/3yedkxisla8ze6d5muci-tx1yfn7mg st
  - Log entry 55063: process wget pid=12814 uid=491 src=9.68.244.115 args=vhlh12efoqqu4yeyzq7wzvplebnk3i7gd11v2yf-igj4ad2k
  - Log entry 97296: process sshd pid=27083 uid=702 src=158.166.142.11 args=7zn71 3/ nyhpi4ldbdd849mbpndxn5adpncsfxej0w4heb 
  - Log entry 51965: process curl pid=29406 uid=58 src=80.125.126.137 args=4frbsww5qrdnec2ie780hziktqh ty5xjnz0la-ly 9/djkk
  - Log entry 88965: process bash pid=17924 uid=218 src=104.207.107.128 args=7oyhwc1io9fguvopd 7tgxnb3hnt/isr8ufisdp4-ecr-5er
  - Log entry 52478: process python3 pid=3816 uid=469 src=203.104.123.149 args=fawez2eygre2cu7/pro6kflpr89ys92rb01peydms9-u8a0n
  - Log entry 20617: process ruby pid=13680 uid=592 src=57.178.174.64 args=eyzln unpoyf57a--o1ijyki93piwhhbc7oohw9xg4vy16oi
  - Log entry 84013: process ruby pid=14319 uid=840 src=133.86.73.201 args=jj4geokgcx5prlr92d3pv3ij7xw7xpogx92r 3lfm cfker2
  - Log entry 34286: process bash pid=3542 uid=915 src=62.240.22.69 args=872xi7 0o3kujppz38b-x34wj8fpdwyb2-7vu0 61vbadybq
  - Log entry 67499: process socat pid=6440 uid=576 src=17.78.109.51 args=n5umvo4n1gesbmzdur/fw7hrlw4u9o4dm5ddgisca1qclj6v
  - Log entry 11875: process wget pid=31992 uid=535 src=179.148.4.136 args=fptiaikkmvh2/25vt7b9fwilpqoww3in12ilyz7-byu9e1cv
  - Log entry 89472: process ruby pid=12317 uid=276 src=40.225.157.109 args=-shxwv/vug lt-czejl1-ey toje9kwjfk38qdufmww9 ifz
  - Log entry 77002: process wget pid=20187 uid=975 src=48.241.126.36 args=bdx9-n gvxp5nx-mrkc/t-lj8m81kt15a7exd7otsfc-v5i1
  - Log entry 66281: process python3 pid=7400 uid=226 src=223.211.78.57 args=kd/6qr5z8nhor-71-n5mq41erots3met4bbyoe-sin6d76ay
  - Log entry 54817: process bash pid=3760 uid=441 src=183.74.206.4 args=1d23-n3nuot7g7xryk4nu 0fji5cnz7ifo5bbrxqfec8hu 4
  - Log entry 35882: process sshd pid=10256 uid=144 src=116.116.145.56 args=7hug79m4ytjf915-x-f43hrhj kr89dff71k/y4s41h0z7wa
  - Log entry 34646: process curl pid=24993 uid=513 src=162.92.210.13 args=/55mguk0d35q7xqvvnus236luz71yk3kfyaroysmr-g2virj
  - Log entry 69233: process bash pid=7393 uid=39 src=121.132.54.203 args=tn9 cgza5y/ky4w/6m-za33347q173w/-9yrvf4 unzcf-ry
  - Log entry 20933: process nc pid=2629 uid=801 src=180.249.88.22 args=dasw1xjsr eu5szkaeiy9leh 5926so03wi/tf/7z98mljcr
  - Log entry 10331: process python3 pid=27406 uid=722 src=14.131.202.115 args=14c3/3ovt9u9ly1e9rto0b2/yk93 /ue8wuhz5cj59lifzxh
  - Log entry 35763: process wget pid=10015 uid=590 src=178.57.252.179 args=-kgnbyi1dr35r10mblrwadgzgzw3i/w4-r9scgattdlqsjgq
  - Log entry 79026: process wget pid=4300 uid=176 src=101.13.27.228 args=be88ubfxn5s3dtl413zp z00lhr7gw93l/ 0z7bsay3h33q9
  - Log entry 62338: process wget pid=9148 uid=201 src=187.119.254.40 args=1vq xm2q/77gz4czle/6jolt7gqqtybs8lnlxy d0evcqzjs
  - Log entry 74084: process sshd pid=15431 uid=402 src=92.189.43.193 args=m1slpc4krsu5rvk9t8uzoitp5/y8qn4t23scdd96so3v98ie
  - Log entry 70036: process bash pid=2212 uid=658 src=67.246.216.22 args=/l86zt2gczs00rxzeukxxs897777ypkv5 84lyuiso53259v
  - Log entry 73097: process curl pid=8308 uid=330 src=205.247.155.26 args=d2 xz mmy9tvbjdzf36nlq1pte7yfcva84ymbebr zehinac
  - Log entry 64316: process python3 pid=31960 uid=922 src=162.133.163.55 args=pesb h-a2 t8p93itfwp0dj6211tonh88sbkdt dwt7eh8i-
  - Log entry 34266: process nc pid=9832 uid=481 src=183.213.39.152 args=9fumjzh 79qx6cutk4d1endz/5ctc49za7apr1lwhxjzd285
  - Log entry 87277: process bash pid=30284 uid=772 src=64.56.184.116 args=wia8ynndjb58w  gr0a3vjjf7aiwqxwp/6naannrhhj6jmez
  - Log entry 72162: process sshd pid=9573 uid=858 src=54.0.213.50 args=6gyiwmbv4d-o-d62iq/jokc1crgafse8//k/v/pt7n6umlpt
  - Log entry 77033: process nc pid=12324 uid=614 src=108.49.143.110 args=ijss0fr1su47lznl1ka6oge9227b6o9igxlap go8pf/46st
  - Log entry 23714: process wget pid=28981 uid=254 src=12.170.49.7 args=t-qwzdf3-opvxjpwwme-0phzedew9zozlq1r1xcq/5m7-2j6
  - Log entry 11625: process wget pid=30949 uid=250 src=117.160.248.121 args=667w4i27wfcbhub3197qd/rn75205zfp-ywudiku48gfg6q2

## Supplementary Technical Detail — Section 44

Automated correlation engine identified 14 related events in the 6-hour window.
Baseline traffic on port 37409: 3 connections per hour.
Observed traffic on port 4444: 107 connections during the incident window.
Statistical anomaly score: 0.985 (threshold 0.750).
Related CVE: CVE-2026-13105 — not yet patched on 2 internal hosts.
Affected subnet: 10.9.3.0/24 — 5 hosts in scope.
EDR telemetry: 2 alerts suppressed; 2 false positives removed.
  - Log entry 63762: process perl pid=15840 uid=957 src=83.95.224.155 args=oz-tj4w5ken0b4hwz5u45t4v9 /- r9e77jr6j477bt4hcv6
  - Log entry 92667: process socat pid=18515 uid=948 src=74.136.127.157 args=xb1rwke5of7sv3zs8ccseltz462adzlqns--46n-csh/gugh
  - Log entry 75885: process bash pid=5199 uid=74 src=167.228.199.158 args=egcyigyyc vwb-tml-ng2c fzgc6nf9c9lm6r0mmw2da7jsf
  - Log entry 42560: process nc pid=2689 uid=704 src=169.47.20.180 args=/m0x/osxhnm/ j myjdjnchu6jw8pnwcbfucho1p8-elgkyv
  - Log entry 44618: process wget pid=25423 uid=183 src=56.133.225.52 args=lprvgjzzhyhl83fktd-wbob6n-w7m/o9yf9 4h uv8 0pc2y
  - Log entry 34269: process curl pid=30655 uid=323 src=155.23.128.191 args=ddjichxa0z69 gb8b aciz8ji-/2p1dg7d0yetrcqs7gwp-n
  - Log entry 55487: process wget pid=5917 uid=689 src=3.34.196.173 args=ah1d0m x3w 91ts6nzk4x-xz/k7v1nbd6vcuwzf6d b plyr
  - Log entry 61046: process ruby pid=29492 uid=112 src=120.185.21.237 args=a8bqo40w5 44e4vygiblhync 3/y0/xbbybgr9/3ueylmz f
  - Log entry 64770: process nc pid=1507 uid=736 src=148.23.102.51 args=nn9qd7m8fk r-z7--0n//ngmezglbad-kh8a4t2nfgwf5dmi
  - Log entry 47455: process perl pid=18558 uid=623 src=192.202.17.79 args=vk3jyur86x6s-k q55nhx h/edeo5r79m2lqv-dz8go5e89i
  - Log entry 52285: process wget pid=23197 uid=433 src=59.93.173.92 args=bcryw/sgn0tiz8cypworv7rjlwrdoagx4lrpinaw9/b3-lvo
  - Log entry 81150: process sshd pid=16866 uid=576 src=95.227.137.191 args=c5rmuidyl-x5aobdl/tponqlgntrjprgvsfozm6m7d9jjcuq
  - Log entry 62294: process bash pid=27177 uid=158 src=44.80.88.60 args=aiz/ouwyamk8f5t/nmrkdt-m856o6-a//q4-92ej05mormzh
  - Log entry 44883: process ruby pid=24495 uid=156 src=190.40.210.6 args=0u/sszhk-fxpust5tjvmee6//m3sws9jtd8ss46vkb8vayyb
  - Log entry 49909: process bash pid=27975 uid=378 src=156.191.112.34 args=skq8n/jdz2oiuffu 301 omr/8vq90yu/myly-b41omhmirc
  - Log entry 42682: process nc pid=8511 uid=178 src=187.196.49.60 args=xx9/ 3z4kni20v5u0ib6xgnpde--3/oeqr1wzcju7d9l8wms
  - Log entry 42936: process python3 pid=6781 uid=769 src=175.108.119.191 args=gdi0xcfvej3oshf5f2aq/1om9udl1xumx9umrq65o4/6-h p
  - Log entry 95154: process nc pid=31638 uid=532 src=162.201.172.151 args=/evpft0rrty4unvj1j9 jcvt4y2u1pav7w0w9g wwj3j7 i/
  - Log entry 39966: process perl pid=12194 uid=214 src=116.212.35.215 args=v1m7pmom83/alzl2zwmjh-1wwsy0av-mm52p03ne /kibi1v
  - Log entry 50109: process socat pid=21912 uid=916 src=156.54.17.241 args=y0cu76wbjjszddhl7zwn1rcp-ytyt  qj-s2wvbeqefl0y6e
  - Log entry 33265: process ruby pid=19781 uid=870 src=148.160.60.213 args=x31v9hpglqiw2za65m1yrd-a9kgoad3a2yp5v 0ofa03lwtb
  - Log entry 30661: process nc pid=4671 uid=647 src=144.250.72.162 args=32 v57yt1v4r54u07/0foxaotikxryqtacucl- of4l01r94
  - Log entry 45073: process wget pid=25791 uid=467 src=1.61.154.153 args=oesi80x tq87racs9nzwthyqzbu3upglr4/ i191v5wsi4vp
  - Log entry 96036: process perl pid=19657 uid=499 src=32.83.77.204 args=h6nod3c4zvn0fi2colttf-2zc2f41emct/ugc5eumo1rnebm
  - Log entry 63201: process nc pid=29350 uid=913 src=18.70.28.25 args=8iqp67yk1natvm/9ush n29a4cezk31yz-2 zib0vrka/sej
  - Log entry 17217: process socat pid=10516 uid=194 src=150.204.40.73 args=ybpzk0e6bt gdmczxeobp4dcumbdhmi7gf/ema62vyyh7q c
  - Log entry 86151: process socat pid=13013 uid=861 src=167.98.212.252 args=xzg  -fyov3dj0ladf2yq70lq zxvswov7etfw5yt mi9lkp
  - Log entry 86943: process curl pid=27188 uid=336 src=211.44.5.211 args=1w-x7zcpatz2xl5oadpt5n/k9nhx/z 9tiyjox5n01dbptrd
  - Log entry 78192: process bash pid=23553 uid=974 src=132.138.214.8 args=zf-mtt2i2gnrjwic0tkrsemh0w2qheebqxvoztj9cpch8vdj
  - Log entry 71358: process curl pid=28774 uid=915 src=72.207.91.225 args=65bqa 1pvm45ezpx wtn 2jourq8/mba  fqgq q5s25 nod
  - Log entry 52501: process sshd pid=11690 uid=504 src=109.168.221.210 args=yjqykzi4ebbd3x51ba82iwz-cij0dgwhgyqxmz-9xwtp97rg
  - Log entry 49092: process ruby pid=30659 uid=944 src=89.27.165.220 args=11 zxdqq/hrcyq76zo1qt6-q6m0om 9sfvtkoi2zpo8lapw9
  - Log entry 16688: process curl pid=29922 uid=405 src=129.99.187.89 args=4xknyocuqwj4jayl m 1ugjthy43pi0lh6nv3mq1hf7vwbgn
  - Log entry 27031: process perl pid=3673 uid=173 src=3.195.18.60 args=dt0u6ke99yp26/vvfh3-st3wikukk64ev ux0/5 x2fz293n
  - Log entry 30533: process wget pid=11457 uid=986 src=103.151.164.113 args=z85nxbjedm45jmned7da85pjcw/t-  ct-vkhu569-uccr2e
  - Log entry 22182: process python3 pid=5472 uid=363 src=104.217.196.251 args=2u0ue/j2u5216s56z3uk6izi5qv9kdi8gffr5h636/qt1/j3
  - Log entry 17550: process perl pid=3179 uid=52 src=21.222.103.32 args=8h2fi16x-dhyjw-l5y7u6-wtn4s3/c4l7io6sx18a94k-2jz
  - Log entry 99819: process bash pid=25972 uid=658 src=106.53.6.140 args=wzyrxnb1u1r7bwk2yta/-302ykt22jit u cpq6ir5rap/dd
  - Log entry 68123: process sshd pid=2632 uid=976 src=139.171.204.213 args=8y2xp18y/llufhcw/1ayu1s 83j9o1po9mxh e9orlg8tzy1
  - Log entry 37766: process curl pid=13755 uid=6 src=44.215.216.209 args=s2x95r6j yydgss07z00wqbxtr-vcf16iiw1lwg050ct/-x-
  - Log entry 18804: process perl pid=9186 uid=641 src=167.160.3.20 args=-p-sr6fu15m46758a0zsoyijwlrfdtz-0115gq619z1yhfy6
  - Log entry 80828: process bash pid=15876 uid=121 src=160.157.98.170 args=pl5br 1otypzm6k04qs4g5c9vm1bx1zl 236o7blgvney-d1
  - Log entry 33639: process ruby pid=22881 uid=487 src=186.204.130.81 args=8zdwwigsi5/z2cbumkhvohov5/bedptn/w-8aedl520njflt
  - Log entry 60422: process ruby pid=28197 uid=406 src=197.170.200.129 args=1hd1 zjmi06nibwtmlb/n3-7oww374rl3lt5u5xn0xx08u3k
  - Log entry 88979: process wget pid=17165 uid=930 src=168.242.113.108 args=it5pmj/zdu/shva8zzlnrp v7wlglflt485rqhiq/8cvhvz8
  - Log entry 16215: process wget pid=21010 uid=363 src=151.166.92.61 args=mnxufxgyjp3hu4t1g tb9pb-f2qqgw-ljd7pb567xh38x96a
  - Log entry 17698: process nc pid=25084 uid=724 src=193.101.3.109 args=-natg2hpd1/rth// ate brd1zo7-rguj7auvlrcgs567g-w
  - Log entry 53496: process ruby pid=27720 uid=615 src=214.179.215.46 args=nl-u7cgmmr pe7 ngsmtp/o86951xikakctuu02cwfx/ a2z
  - Log entry 21712: process bash pid=8079 uid=577 src=169.131.112.92 args=a34gor5waw055rnfgg kor-d5zq9xbdawhmhc/t4 949eo97
  - Log entry 53066: process socat pid=4393 uid=57 src=154.114.34.248 args=w95 1n14bp034f0oj gmtlsta87cmv6szprdlsrhilt-4pcz
  - Log entry 32702: process perl pid=5880 uid=776 src=42.101.49.67 args=2u7pip9z 6c4vgma9hei9989lkj8ozmkrkfp8wv40zk7an9i
  - Log entry 44267: process perl pid=5811 uid=860 src=34.173.133.90 args=msgds/5vy71o u16jpro5izx1wssc oosqg9b-5igi-snxco
  - Log entry 84014: process sshd pid=1335 uid=997 src=164.26.175.97 args=bj5xbkg9w av56xkx- nvu66mxx/yxgu33x78/skuvhfqu-0
  - Log entry 94189: process bash pid=31557 uid=455 src=43.232.182.230 args= eogt8115iiza6514/drv3ydn- 621uzve4ql483ctyhq7i6
  - Log entry 53802: process socat pid=11753 uid=302 src=112.183.16.38 args=7nhye xl-0sqaxq7x/lh5ml4ih207pp36yp-sr744unju9dm
  - Log entry 35419: process python3 pid=4380 uid=614 src=176.96.220.3 args=-zyn39w08cwnxazzn-/75-g0oz9zyjz99bznmg57dzt5wnjl
  - Log entry 13078: process ruby pid=4805 uid=385 src=14.8.146.172 args=apf7pr6xell7pq3yin305-g5gc677d7ml1f3fp2wgjfp70fg
  - Log entry 85380: process ruby pid=23409 uid=860 src=113.203.126.157 args=zu8xfersy6s5m-qqdqgn1c 0024cdhz3t2md50cfm3c4hnyx
  - Log entry 81925: process python3 pid=15446 uid=816 src=84.79.43.91 args=xq7r89 gfxe2rsd72 j8-xpoxnuoo8c749ti42la2akngze1
  - Log entry 89466: process sshd pid=2895 uid=826 src=70.173.175.236 args=7jsnl8yr/9uz2/y/e/r4n6i kv5rrltk366ef evehntq kb

## Supplementary Technical Detail — Section 45

Automated correlation engine identified 33 related events in the 6-hour window.
Baseline traffic on port 20002: 2 connections per hour.
Observed traffic on port 4444: 198 connections during the incident window.
Statistical anomaly score: 0.874 (threshold 0.750).
Related CVE: CVE-2026-40962 — not yet patched on 18 internal hosts.
Affected subnet: 10.1.5.0/24 — 29 hosts in scope.
EDR telemetry: 4 alerts suppressed; 3 false positives removed.
  - Log entry 14403: process sshd pid=29190 uid=858 src=157.60.174.203 args=5i0aszyc4v6mt7mng7f7i60iqwa/mcjs2u3yrahocsop-zbs
  - Log entry 74733: process nc pid=13158 uid=789 src=184.135.247.252 args=2e0i braj9gqv/g4a75f-8k769ysartnwfg0do7cy 4jueug
  - Log entry 19136: process perl pid=10485 uid=757 src=90.79.56.53 args=y9z08 g9cok0r3m66sjhr6ze69usfu//co2b47ls0-78w5mc
  - Log entry 11990: process bash pid=13270 uid=158 src=34.73.19.99 args=y-lbh98vt rm6lnhzlutcd/owcnxf8saf11naj kcdq y 6-
  - Log entry 50091: process socat pid=7368 uid=360 src=176.86.176.220 args=vkpytx6ps7t3rxkp6372/457ptf-5 xffsfmpc61neq6ss2a
  - Log entry 51579: process ruby pid=30718 uid=350 src=93.199.187.151 args=acbalcn/6k-52pr2/b4ylfctoapd/vwcwknoyt0d70obdhjp
  - Log entry 10304: process wget pid=6480 uid=36 src=51.130.107.7 args=zbno4tuc6q44xpr5255/77ixgbznfryn2bdr740xwsj5yflg
  - Log entry 51176: process ruby pid=25331 uid=663 src=40.174.239.194 args=2v1fckydmpflnf kccdgozjnupobcs7sn/9cq7q64qwbs - 
  - Log entry 92472: process curl pid=7807 uid=47 src=108.254.241.138 args=yqzcdcecwik4en61zvu-b62vhyemxi35gp09m/5/w01rvl/m
  - Log entry 24913: process nc pid=27815 uid=256 src=152.94.106.227 args=k3coh8490rycju07i5jytahfsar o0l6/l33w-t8lfnrsj3e
  - Log entry 15977: process perl pid=18610 uid=448 src=164.232.143.76 args=2b3pg2hdaxqamtcemdt 22vi6ncy1yx28981 xbydnympmj-
  - Log entry 39993: process perl pid=17457 uid=45 src=34.83.48.253 args=4lqol2 18matgvrx2xrp0vsaipv7q7-ux lnpafnvddkhtu2
  - Log entry 13545: process wget pid=9144 uid=491 src=214.14.86.120 args=u9d0lqeoblivb-o88rfsj47ja4kzia0650t4v-b0r9jnyu3u
  - Log entry 94792: process curl pid=2622 uid=942 src=88.31.46.173 args=-vdie47k6a-n3/uhglnx/gm5if6vc11tpkg0qqpp-jceg/b9
  - Log entry 51430: process perl pid=29414 uid=961 src=104.50.82.157 args=752t-enqm2/l0pbx7nzv06o1ukv73twnu8ikwkl w8-iqa96
  - Log entry 74763: process sshd pid=28056 uid=781 src=18.32.25.162 args=3i xji8kf/jjh3wjwexg3 jtraxe9twrj1/pgrq8pvpch02o
  - Log entry 47079: process bash pid=7823 uid=394 src=149.224.115.177 args=-250lyyy1567n-otbor-itmpy6h0t3eppx-mwv vntnvdzbc
  - Log entry 65811: process sshd pid=1983 uid=620 src=63.116.23.194 args=/9 ig2b7hh94o0vh-arkvm914haxb5/-z-dp7p6u/xialcis
  - Log entry 96897: process socat pid=20471 uid=656 src=212.144.164.113 args=al2tcsv lh1s0xmc-/ruhy2henah-j27 j6-5ld06gn56/tj
  - Log entry 40046: process python3 pid=1761 uid=831 src=50.217.217.215 args=vn9xrqc-u/gi-qqm5s11s9i72qs2a48qdhvocxerh5ywgd2a
  - Log entry 31307: process curl pid=27430 uid=720 src=65.116.186.33 args=mobro5wfu 4d1-dyuo6wycw3ijo1 1s4u-a4kh5a8xn3cuiq
  - Log entry 83449: process nc pid=17835 uid=708 src=191.64.68.3 args=/4fr9/bocvp2xv 192jwf5jlg38y m9s9aegrjna9-s/il89
  - Log entry 20486: process wget pid=9292 uid=607 src=18.245.78.231 args= e-/zdezhshz7 1/3qlcksi4norytg29h0ve8e3rryr2w6tm
  - Log entry 71335: process ruby pid=11769 uid=99 src=84.162.212.85 args=b7r3v-5w62l1i0rbwoufujoc-m01mte0fyfgl7korlj7jyke
  - Log entry 61753: process ruby pid=25055 uid=285 src=37.61.20.176 args=vhnnw2ca75x26vqekfrija/j10niemp7 v-oq63wwc27u7tz
  - Log entry 90439: process perl pid=1509 uid=822 src=223.1.253.165 args=m43xkksl8ix-g4vsf03lsujycdxvlpgrknors y33yc4m5x8
  - Log entry 65469: process python3 pid=31463 uid=999 src=208.216.162.175 args=hpqsd2-1wa1sfxyf5f2z1lu mv4tiyozgsv88o4ngdcw9829
  - Log entry 99423: process perl pid=8975 uid=268 src=49.161.120.131 args=q49soz8mf9k6rm70ru2v4ma5qaqg31c3w9b-etus43ym-zc/
  - Log entry 51951: process python3 pid=17821 uid=445 src=25.133.72.150 args=nfj9e g1dl2t6y6k9sd-5j63hh/cfiohl4cy/06nxc/74jx4
  - Log entry 55860: process python3 pid=18398 uid=320 src=13.23.92.88 args=qe 0uolnf x91fq/npem0d66p7i3 dfmdjgmhfvnpm8x8smt
  - Log entry 42023: process sshd pid=11194 uid=123 src=121.238.112.96 args=we394kq2bq2k5cyl2w15/4b8bbncl4kj4wpz/1k2rxw4rpjw
  - Log entry 97239: process perl pid=22740 uid=142 src=62.210.35.211 args=lc7tcb-o/nsj19jehv/mp72wkrm6pm/clxfs56z bumupg6e
  - Log entry 75645: process bash pid=8349 uid=492 src=211.101.123.217 args=jl4yimtd/bpd5/o5-6tg6zb8y3137xqu0-zaay1-0w8425k1
  - Log entry 98263: process bash pid=12398 uid=477 src=151.3.237.63 args=hroslb47ihrlk-/u5lo1avj7cy4kcsorudwldw9m34bonr k
  - Log entry 36142: process perl pid=14542 uid=274 src=22.25.159.87 args=c7hlyne9n5/5b 6yk7tuaefiv7837 wpwclfb47tkec18hlg
  - Log entry 26186: process socat pid=20079 uid=848 src=33.107.123.5 args=648svphuqpghkjet4tg6kb7/nmu68lu517dk5ys8xeo-2eal
  - Log entry 94832: process perl pid=30310 uid=105 src=114.78.249.130 args=4pnf4t3311hd6hmvww98wun-/bb2en7qt7nqzmu-y1pc46qv
  - Log entry 61736: process ruby pid=31348 uid=705 src=95.109.38.84 args=63ky7hz6s2cs0/xa4b8 3519sckiq79oq5hi12- kiycu08k
  - Log entry 57363: process perl pid=29420 uid=437 src=38.183.226.250 args=n31q0qh5ur0d/u5ehvbhxmnwt-fj0g12ntius3bpo5jsbu2b
  - Log entry 56843: process python3 pid=2668 uid=243 src=169.173.54.203 args=r qqzxex/vb5qhflfqgsj0x6 gu9l1evgxrz/ nk-f4rvro3
  - Log entry 38615: process socat pid=30937 uid=506 src=223.124.14.129 args=lrs-vp7j0uji6-kc0za01ml1kt5-qk36x3w5snf6y1qhgzsk
  - Log entry 51452: process bash pid=22881 uid=431 src=148.205.50.177 args=ogmrm6dsut4rjs6g34y8nfy9jyj9cw1o857mp-661u58wggu
  - Log entry 35016: process ruby pid=21476 uid=161 src=56.153.189.235 args=l0u9bcq6-j48-ascfhu/s4arq/lr6l5l88ful0/4itfmhf/6
  - Log entry 82115: process bash pid=12331 uid=917 src=66.174.143.99 args=wmxamkmocxkqrlen06lkb1mz22slwgpob21outy8rfuhaaty
  - Log entry 98320: process nc pid=12825 uid=637 src=178.101.173.135 args=mj0blsw8th3fog 9rajcez0j6abv2 x2e t 0xwtd3zhap6c
  - Log entry 93717: process perl pid=22464 uid=156 src=200.89.32.30 args=zhicve h96uv3mr 4h56nx/064v4wa-ou/fqqgvvb h6lov4
  - Log entry 48102: process bash pid=25971 uid=955 src=74.178.128.120 args=uwns q//7x7 jy lochvjo 14xyes 8fbeenranj4-0sx7p8
  - Log entry 59817: process socat pid=23562 uid=958 src=196.215.195.128 args=0mjsh6oh37mg-r7/y5tgu u/nlub380qts-1q-yrih60dsii
  - Log entry 38694: process sshd pid=5716 uid=630 src=139.82.252.55 args=km/1m1tl78thoglfoxm/cua2 mir9i/6qa675wk8l/x/bf0k
  - Log entry 59063: process socat pid=12751 uid=297 src=160.52.212.143 args=/swe1iq ebyj kduhbq/847f5ow1p-7p9x7tzlb8c1po7dx6
  - Log entry 84081: process ruby pid=21131 uid=421 src=49.177.132.187 args=i7h1trp3 qs/xencxikdtbs36guwgk9jyscsz3uamck80xgj
  - Log entry 35198: process ruby pid=5446 uid=144 src=176.39.14.159 args=4eobpc3p8917kfdz-g30gr3 u z3uj0im8v2za9hswuevd9x
  - Log entry 57891: process perl pid=1026 uid=849 src=177.152.130.57 args=h4i32bv23vdiooojej3l/6fo08d012dayye05 rnirxcp9k0
  - Log entry 66514: process wget pid=5139 uid=909 src=16.153.99.37 args=h6nrpdwfd2vr y5cxskm0pb-9qg4r3wbm7dictu 7ivnysve
  - Log entry 55526: process bash pid=25874 uid=206 src=108.45.81.31 args=oe1i05qtgf6nr7uymv-2e8pzqrk6tyil2rmat-6w7hnq5a/d
  - Log entry 56759: process socat pid=2953 uid=490 src=113.186.17.29 args=o1ynflxfeun27402nnl6v6sb4hst21ewb6w-op/y/fk-c5c1
  - Log entry 38129: process sshd pid=9598 uid=810 src=41.136.238.82 args=0v 6t0n4a-9w6lhoe6aqd6fr5nwv8r82apv/0hxtqi31powr
  - Log entry 91971: process nc pid=7330 uid=992 src=161.162.106.154 args=k/vsydjb27hier0-9ff9lyx0b53al8ybgua04/vgxvbsjh95
  - Log entry 15777: process nc pid=23359 uid=41 src=183.112.155.151 args=fedobx5p2cto3bwkq046w367htch4uw9vis6el0s99ac41ct
  - Log entry 99798: process socat pid=23109 uid=128 src=83.238.197.182 args=by/p91294dl7zjxdweaje2mpie8lr4/nbwk0mc9qi1h3xc9h

## Supplementary Technical Detail — Section 46

Automated correlation engine identified 19 related events in the 6-hour window.
Baseline traffic on port 11374: 2 connections per hour.
Observed traffic on port 4444: 63 connections during the incident window.
Statistical anomaly score: 0.870 (threshold 0.750).
Related CVE: CVE-2026-24151 — not yet patched on 12 internal hosts.
Affected subnet: 10.7.3.0/24 — 27 hosts in scope.
EDR telemetry: 5 alerts suppressed; 3 false positives removed.
  - Log entry 50894: process python3 pid=30038 uid=944 src=197.8.116.145 args=0hljp1gz0y1z-4n5k1kdmia1iyva t8o6etrbu24tuvlyg7y
  - Log entry 18089: process bash pid=23863 uid=33 src=223.73.204.49 args=pv50m0mn7x03m tq/be/m1i6pf7ye23kyeztvj5rmcyziuy7
  - Log entry 50058: process perl pid=7602 uid=462 src=43.9.33.231 args=dr7byva52ebt99siagghrsyjqif7xlot01h/8sy56gdnv64/
  - Log entry 29596: process sshd pid=24115 uid=656 src=28.190.0.87 args=n knuav-olv7ox3nt0fv/ha4bdvcuyemnhrvstvqh/86mqle
  - Log entry 49888: process nc pid=14952 uid=960 src=164.51.98.90 args=g8mo0qh vmf52nuee-68w7eegn5-3tc5n13miqd6mk4/8mcz
  - Log entry 15155: process bash pid=3411 uid=762 src=105.53.96.240 args=w8d-7/9dhvab3rplxrrdsa f59oqa6zpmpj6 q-9 y8i8zj0
  - Log entry 10286: process nc pid=20330 uid=780 src=183.250.212.95 args=r6j8foqkl10 9gtvzwxbtn29ywvm1lah5t4me5mmogy19101
  - Log entry 38232: process python3 pid=27605 uid=669 src=57.3.209.99 args=f1wdtgr1/4y76ab0vfyb9xnh /w5/ixgkzaywm3g4mtfy5n4
  - Log entry 52649: process sshd pid=3729 uid=441 src=96.203.232.53 args= n-i3pnh29eqy10n89y ofum0ianvbghc1dkie/cbav-k/r-
  - Log entry 44572: process wget pid=12220 uid=239 src=126.1.12.69 args=tvm62qzgy9h69 ch7mv60i681p-tc47kpu41xtxwpmabcf6z
  - Log entry 32823: process perl pid=13098 uid=830 src=108.184.34.158 args=tzkv87tmq34rfba507xn5862v/gexohz6pslxn16buc3cxca
  - Log entry 63002: process bash pid=14668 uid=43 src=12.214.27.143 args=24f  9fk0-r 4zc/24-5n98drvudrpqrobxg/6fbd lswk k
  - Log entry 80868: process wget pid=27401 uid=718 src=11.175.79.1 args=ejx45oka7pxa05moo63qzprdtg i6ze1e2qevr fsh41e pw
  - Log entry 85750: process nc pid=25634 uid=493 src=45.5.19.142 args=ni8vmx6/biut21ellzd48zr2g22/ /jbnvefbvi1rzw/wfw7
  - Log entry 46120: process curl pid=7869 uid=977 src=51.152.24.217 args=--qzchm5sha-j--mf 6d3jv3j5u17-tgg6or-ukxpblan jk
  - Log entry 26792: process sshd pid=7387 uid=56 src=11.112.76.75 args=h2c6pzugvd3kbhska7dxzxjac9mad b0ra3k3q3qnlq5g5ht
  - Log entry 12582: process ruby pid=4008 uid=67 src=16.198.58.121 args=kno ioswlbxuh/rw7g3j-k709l-7nd6mu6rmj0kx 3-y-bnq
  - Log entry 85802: process ruby pid=5380 uid=151 src=144.43.93.183 args=6ads84ubzlrjirbvew2ym618acrd7ymqv-uqgqmiu1zom1mh
  - Log entry 92577: process socat pid=6646 uid=301 src=182.77.80.71 args=w5p0h6jdzmvp5brwp/s-jjd3te42atrms-xbnt-9eyr vq v
  - Log entry 24521: process ruby pid=22943 uid=696 src=113.123.153.87 args=rx/74zrobr16 6zbcvxu6nj//wtqwk5/w-xu0t2n4j3v7oum
  - Log entry 60061: process curl pid=13113 uid=580 src=86.158.22.78 args= 0-78-clu-vtjml6diga ex5se00j8o75ualdl o5u03cz84
  - Log entry 51670: process perl pid=16454 uid=146 src=206.134.172.228 args=qwada0 wx1urqso188sol56gek/zw6zfsheye2dz2o9//jgu
  - Log entry 72416: process sshd pid=20545 uid=221 src=151.108.236.29 args=r2uvl/ratb2y98q2rfqqafui3z5sqz3rh1o3-h01ngztw7o4
  - Log entry 89224: process bash pid=10354 uid=61 src=77.143.23.20 args=ndo6j57k7z3bojhrunk4rmu4icefulxpkwf6m1qy7pusafeq
  - Log entry 78538: process nc pid=4192 uid=463 src=152.243.75.56 args=b8p366i8h/jcngjsc5jt6dsezon8ohoz696syy-ymb2h1e 1
  - Log entry 30589: process nc pid=6983 uid=53 src=26.216.113.171 args=byji8titsqie30tbwngx2ldfk5kgmexmbzr43a4oikvbni9x
  - Log entry 81688: process perl pid=10654 uid=42 src=137.55.233.199 args=142mpx5l tuc1v-l4wjhxkui5t4oi89nuwy8kv0ia ls01-2
  - Log entry 80860: process python3 pid=9725 uid=773 src=202.29.56.104 args=9ychawoj4o41/vb7rep w/cn53fnh0mfd0dk86-fm4beqhug
  - Log entry 98113: process python3 pid=29162 uid=437 src=126.80.65.8 args=bechh5efw2brl3v33/ vjvh-3--ljxt5c0cjlb4pz5v327q8
  - Log entry 37504: process sshd pid=25828 uid=325 src=36.246.187.9 args=/44qd1-n394njnvse0o12us8adwwr21x9hiopxou7dz9/jy-
  - Log entry 14298: process ruby pid=24998 uid=743 src=107.151.74.173 args=rw3oq-p4t3pozolmpxnouajj9hdmjt0af57onc3rcmn79mct
  - Log entry 37068: process socat pid=14551 uid=14 src=112.201.103.138 args=6/y93zsgdnsif7opq5y9cny840y/ioq6/5-1ynnl9zo8id/g
  - Log entry 58593: process curl pid=25402 uid=47 src=159.54.169.124 args=ikjvlngf4a1nhdeyd4-wirz721bs/1mnmw7h-bt6 qsk15ce
  - Log entry 89841: process perl pid=21455 uid=165 src=187.2.3.168 args=3f4y7qk83ouumw7-svznij nwf768wl5mh-zmzpuczs5t5w8
  - Log entry 44342: process curl pid=2767 uid=10 src=55.62.147.134 args=45m1al--74z1sm6w415eby9g6gk51efv/0je9jw wnl1d00q
  - Log entry 16212: process nc pid=7518 uid=376 src=209.253.25.65 args=xq76l3hb9ovxbdelaoq68tw8k0ei78jt7cszyb2sprrjrqb9
  - Log entry 37629: process nc pid=27069 uid=264 src=53.13.99.162 args=kwp8w5/soxwpc6qxgeivsltviepz6xaz-jzx1lw6yrrg0lrr
  - Log entry 73387: process bash pid=23990 uid=550 src=9.109.82.103 args=5g-kpn4odtp1 hd9dpo46mq-8e3fj1cnt4qfu15y-5qr46sk
  - Log entry 13750: process curl pid=11928 uid=186 src=94.170.59.37 args=pqalycs-du732xt5yj9goa-qmkxg2b86qabeqquyqk5wqxsk
  - Log entry 90639: process python3 pid=13107 uid=718 src=18.249.250.215 args=zhjs2dz8fwgli1ovjyl-9c/4tq7bhg4qd-hqdctc72-xnuav
  - Log entry 88898: process ruby pid=28973 uid=214 src=152.123.86.111 args=iwik8t6qpucr/gpj2z/3ibwf14q2od2qe73-y4zvurk2gkoi
  - Log entry 72488: process nc pid=10264 uid=934 src=96.112.182.229 args=rr2-41rh8e3u9ov9qo 4vh3yd0eub1157t7g6ieo/jl0 p86
  - Log entry 50351: process sshd pid=23992 uid=637 src=185.37.59.147 args=v4wc//sr /ylr5 2w3wwjmk2g 104x0ew gl8jv-ch2 cgmj
  - Log entry 30412: process sshd pid=14832 uid=197 src=174.50.148.202 args=ug3glw4teia7gg/eadpuxtw384t5milarn/altdl x9u7c14
  - Log entry 78768: process python3 pid=27172 uid=627 src=49.89.75.68 args=w-p-q-5lbq-q0ji1p3n3ybr48adiya635r7gvvjw6j35e4 n
  - Log entry 59834: process nc pid=1435 uid=324 src=145.163.156.57 args=j6gpodqlomsk-hpknnm7yk8m7qybowai/l-5oskecg03cjo2
  - Log entry 39459: process wget pid=2112 uid=879 src=169.189.7.223 args=c1z88j23djpbu3kj09 bnlgi4zoxt79r4ep-u62cv1dtl09c
  - Log entry 30210: process python3 pid=10656 uid=742 src=66.114.59.76 args= //8hjqaywman14q3919caornhpbky8m6ks8gyifbnqq blq
  - Log entry 82319: process sshd pid=17131 uid=445 src=82.41.179.235 args=pdh0zcjkbxw7j8agd9wvloc-/tihvm7pa2iyv3jllye84i84
  - Log entry 14301: process ruby pid=28465 uid=160 src=150.247.206.194 args=l872d0nt27z8zox/ca71oamcwcwj6l5r3sbposeytm ztrmf
  - Log entry 61697: process nc pid=5063 uid=543 src=219.128.45.72 args=ws6ywqnhn8pth2q63aj7ji 0eym4hlsnnb8f12uwp9 0r/e/
  - Log entry 94358: process wget pid=3571 uid=162 src=144.101.172.94 args=u/4r9fxkxtu8u4iol9u04rcqmh4q/ly6a5qjd5zek5jkkkn8
  - Log entry 23414: process sshd pid=6133 uid=770 src=181.32.143.203 args=13lbia6qwotch2s755ce4l4 61zxriu5aio51v9m2oiojy43
  - Log entry 76806: process nc pid=25299 uid=686 src=165.56.36.236 args=v3y3zjat595loglpy74i091asik1 0hwxegheuxl-rf/gb-b
  - Log entry 51288: process wget pid=8105 uid=986 src=152.134.94.176 args=mc4pv2b-7zunaqv9ecar8l18938fyr1e8uf2k6oeb0bot30i
  - Log entry 97749: process python3 pid=4012 uid=751 src=76.35.249.72 args=6 jk3mwma09275891qbxi4pcg6w3pa8dxjiaqcuz 2xlq3i1
  - Log entry 61724: process ruby pid=15900 uid=266 src=19.30.72.222 args=sbgy80ncm-n7-jiiy-a1muugu455htxbabf14xylslk r6t7
  - Log entry 63636: process sshd pid=4686 uid=17 src=131.214.75.81 args=s0l6tx k hd6r/28z6n/6yd4bh4iq-s0w7rr4z21fqsbntr8
  - Log entry 65329: process socat pid=25447 uid=555 src=87.100.28.23 args=1jyl0/zpbc8shlfvtl0o21sahz1azxwxkw5n-gn -nu0bye-
  - Log entry 94838: process bash pid=29521 uid=626 src=50.177.122.154 args=t3x4vg519-glw5x2/7w/4nnne8uzpthn6wt6f8dhni/bcpnd

## Supplementary Technical Detail — Section 47

Automated correlation engine identified 19 related events in the 6-hour window.
Baseline traffic on port 61457: 0 connections per hour.
Observed traffic on port 4444: 176 connections during the incident window.
Statistical anomaly score: 0.932 (threshold 0.750).
Related CVE: CVE-2026-44994 — not yet patched on 5 internal hosts.
Affected subnet: 10.0.4.0/24 — 17 hosts in scope.
EDR telemetry: 1 alerts suppressed; 1 false positives removed.
  - Log entry 29585: process socat pid=5025 uid=997 src=23.216.220.68 args=r 0q7ncmgnh3cwmpz28zjrz79ufmvwosv96dskemucwzxzs9
  - Log entry 36805: process socat pid=10315 uid=23 src=187.30.173.232 args=4lyila83njrzbcoa7zfp9t1h izav6bz8cz6ercg9023/5cu
  - Log entry 77833: process ruby pid=23635 uid=26 src=31.119.114.70 args=9j3b-nzqp4wbqe5ia44eje54x06l7e365tpbqclvjy0y0 k5
  - Log entry 15815: process perl pid=3634 uid=145 src=58.99.121.64 args=k9bf7daiv v62hkucwuxfi7i m858-kk3le9w26s1svr5esu
  - Log entry 47810: process curl pid=6205 uid=850 src=213.13.113.109 args=dcwswfmspyh3nyop38qrdmqz5t3z 3t kc-1qsls56mn/wnh
  - Log entry 69724: process python3 pid=20288 uid=490 src=38.159.109.208 args=xwq9tfxfrmu9br74fd0e-ok0l0sy60sywf4v-an0m45v4rt3
  - Log entry 75977: process sshd pid=22694 uid=220 src=144.202.50.48 args=n 0e2uspsvmnsht7std7yi5is1ba087srdxikgzvqd6lki6p
  - Log entry 13803: process curl pid=24787 uid=512 src=102.165.212.31 args=x9i t57m-lrw7i1i4263cw3 m30524xj1uj7osk3 o2ycqhx
  - Log entry 25026: process socat pid=31236 uid=648 src=108.120.168.233 args=iw6l93jlpk-/ 2xs3a7jvrlza3znmmbrum6/-6su7fm2-2lw
  - Log entry 72391: process nc pid=12604 uid=216 src=204.132.206.144 args=2fw4txfeb5v5k3961pe09wwyx97kuw f7kxve c 9cf7em g
  - Log entry 83667: process socat pid=22814 uid=753 src=84.110.162.104 args=m950e2cfzih1lykoukqrcm/7p5s65id6oli0d9aqanajrno6
  - Log entry 69276: process sshd pid=1015 uid=876 src=37.97.81.69 args=/5kfw7ygjl3naz -p3rwm05vgq-q2jv3aos8cb7tyrw0mtei
  - Log entry 94636: process wget pid=28151 uid=872 src=216.164.171.158 args=cb/h1p-i91pacmni6gcmju941ix/utg pzshcr3u09ozlzcd
  - Log entry 59606: process perl pid=27152 uid=532 src=2.75.126.5 args=bnqc-bn8t7p1ps4amevtyv-agvme2pqt2j0b8vd-belk1clx
  - Log entry 18376: process socat pid=3133 uid=748 src=39.74.22.117 args=sw5f9rrfcwby4o326 tf02ltgm79vv89vzdx2mzc/r-20jzz
  - Log entry 73009: process ruby pid=17309 uid=818 src=199.99.163.89 args=ku-1tyi7jt081a7x6u1ofwkjw/w6tc95lwhwnixe5gzfjpbm
  - Log entry 47531: process sshd pid=11886 uid=703 src=42.16.127.105 args=w0fti39fg3aioha60h119sjnh1q00nau41in61cyi-nt/qff
  - Log entry 95484: process ruby pid=19450 uid=786 src=54.235.141.197 args=b/8x4x1x2l062y8o1o29q5tr54aeb168fbbd-p3ico8meu63
  - Log entry 68922: process ruby pid=16691 uid=218 src=23.88.15.195 args=/1iep6kfdo5071kcyvmnhwn-xd8iwv32ymsb3jqqtg/4r4m1
  - Log entry 30184: process bash pid=26146 uid=213 src=223.23.47.182 args=58vdpok/xxwvjt4/j7ahgdekznk-  7jgcpjy 52-ufhcpm4
  - Log entry 58081: process bash pid=15958 uid=817 src=218.253.170.135 args=iod iori5h4ud ccvixp2jhmrxofy4lz4j1k2mo3hmh-iykn
  - Log entry 87004: process perl pid=26100 uid=2 src=61.198.100.46 args=nsegxtie4ro8cf6draf5mgb4icldmuzds7cvpj12y /suykw
  - Log entry 92262: process ruby pid=22135 uid=123 src=41.177.135.108 args=khg0olr-kp/x2l5jt43eh64euu89e88khy5u69-5hu92pv/y
  - Log entry 48492: process sshd pid=19396 uid=705 src=173.128.68.174 args=/1jq5ml7rfwm91462j19drpvzejy4p-hm04zmw3xmy00wf4i
  - Log entry 84029: process perl pid=25756 uid=243 src=156.209.186.165 args=roqktruyvem8f0 8bl59cxb81j51r0/n99h06y/0rbjtvnm3
  - Log entry 28239: process wget pid=10887 uid=476 src=104.253.125.236 args=j26jz5au03jus3x1f40nf2yn92g/fgg8lhi47g6glanhkvhp
  - Log entry 40714: process python3 pid=31385 uid=534 src=101.53.172.71 args=aot8ifux7h050c0 k57-a2/uk3ctnl4ydng6bwsy7oqow2kj
  - Log entry 38597: process ruby pid=7765 uid=742 src=17.160.158.220 args=qb2826rqwchak76ig3bzrpnna6pq9ufu0wysg696fkf4wh 0
  - Log entry 29608: process sshd pid=7489 uid=325 src=200.44.159.147 args=sip8syly2mz4uv473agkf/ps08gy7om/ gg4ofrtex-9tnki
  - Log entry 50132: process bash pid=6013 uid=840 src=153.151.225.56 args=11dlgk8o49h3zpco2jm/i0zkum42q/lmxyyeskly9zx7 ruz
  - Log entry 40976: process curl pid=1235 uid=17 src=11.189.106.63 args=5awmi8umh2o3ucfn2t9ykzhlrmw/8zmik9n48086q0sfkb53
  - Log entry 72666: process wget pid=21656 uid=498 src=6.189.102.199 args=ke9waoj2il6jt18mqx2pkvye/xeg-p014o5m-9 lo7i0ybyy
  - Log entry 96765: process perl pid=31609 uid=957 src=6.211.159.132 args=c3gm-xybl/si5xl-lbtx6xgjsgwhor1sqwzox5jz-8/qr2ow
  - Log entry 49804: process bash pid=3385 uid=56 src=132.29.119.254 args=c7a9svv/7ui0wpq1yqyd55c8og1aoz2bsstpp/32hdxtyo81
  - Log entry 79718: process bash pid=7177 uid=152 src=64.249.4.195 args=tyk14zq2jevgdt6pusi9kyzhxh/qt5xxbjmqup363mnb6xg7
  - Log entry 96295: process socat pid=19938 uid=0 src=217.40.24.227 args=m9gjqg30fq3g3hx3gjz9haf90/n m45mbpeaw yngyjwufrl
  - Log entry 19666: process bash pid=25620 uid=822 src=85.237.99.130 args=cqdt42qu dzyz1lv02nmawkn5ycg6otgb5-vejqa4 wlss-4
  - Log entry 26844: process nc pid=3658 uid=947 src=198.132.93.27 args=35kbbcr/481e-qcp0bqh/m bpkkefrp29gph2n7iepuoy57/
  - Log entry 26735: process wget pid=9480 uid=182 src=123.177.241.196 args=va5riy tsqq8o2qq2pdghy33x-cu 99w7qn4x5u7wc5v8fuh
  - Log entry 24081: process perl pid=14350 uid=317 src=49.22.158.146 args=u9j/vo80jn1 txbawt6x/ijxd85kl7c0gf9p7grg4jh9nxse
  - Log entry 20143: process perl pid=21790 uid=665 src=13.249.168.129 args=z2a-qddt2ete kguwl cjrpohw0tc0r/p1rf7 q/9ri3869-
  - Log entry 70984: process python3 pid=3564 uid=871 src=211.233.60.134 args=-wy3r-qpslgn949o-lmm2igsl2wi4-2ybjwayh5b5-jnfiny
  - Log entry 17756: process sshd pid=1016 uid=323 src=114.75.244.100 args=aty5wnwrcu8ucqudppnatb-ivp2s99hey/pt/zgc8-m0  zp
  - Log entry 75659: process wget pid=30220 uid=445 src=107.155.239.31 args=f-9redgs2 ff3a2vf1qm62879b 4ir6tow0tepemd182iuga
  - Log entry 48104: process sshd pid=18484 uid=0 src=31.81.10.213 args=7-2elylo2n9 6d4 y/flu7yslh060nge4lv0ft7uonos5mca
  - Log entry 32994: process perl pid=24911 uid=7 src=28.99.211.210 args=pwle73gu4zydll1di7di/a uiuff0itnwoz6deqn43nb16oo
  - Log entry 69869: process nc pid=19037 uid=690 src=42.20.175.157 args=52ohc4n7q3vmuskyoa1wj/lofgtemcnbv3d8g9c5/1bda1lx
  - Log entry 35326: process bash pid=2509 uid=33 src=35.138.159.194 args=2nwn5vi9dlvpn j1f8/9m0dnjosud/yqmy3yhx2rwigt4yj/
  - Log entry 50826: process perl pid=19466 uid=349 src=186.43.181.197 args=g6f/qip7m2e68yhiohakyyjpu42h7gp4l0rp7mezkx80whrv
  - Log entry 45232: process wget pid=24749 uid=28 src=44.39.249.58 args=1vycpb8fq0r8/gqd7265qj-24 lncu8/rf59eds/gwsc1aa1
  - Log entry 80466: process perl pid=30369 uid=618 src=79.81.249.180 args=ex/utblb1gtxxsi2mhtewa7ktec8qjqy4is4kfjm0qqo04gz
  - Log entry 14341: process curl pid=2550 uid=554 src=26.219.64.154 args=0d32d-4aedkbbm86ydp2nk/-h1szfwdxym7l3lfszyqzrsnl
  - Log entry 65947: process nc pid=18905 uid=892 src=164.104.3.139 args=eyl7rtuihpptke2z6gjjbma11d5amn9rvuftfn nlua -b2u
  - Log entry 86595: process curl pid=9588 uid=512 src=35.151.62.237 args=-cionxfcol436yw2im2cux4pcmtd/z66-5hku untx72t60a
  - Log entry 62028: process wget pid=14179 uid=603 src=197.215.115.146 args=k4iq3 y-w86edqby72 83j6g39//gox-vkd3wjqpg0hpp5in
  - Log entry 60051: process wget pid=2595 uid=210 src=123.17.45.127 args=i er0xwwkucxub/lgav 65q6nc ymf/oy173pk29yyuw12i5
  - Log entry 17546: process perl pid=6024 uid=2 src=82.82.166.221 args=c1rk20nub2vmv469wvrdti mdnrh03u5av42/-12ni7dork7
  - Log entry 95341: process socat pid=16684 uid=286 src=46.245.190.25 args=uo2rrln7k32jfjdex13im7skp-5h01d11c0l8mhvjkahnjh3
  - Log entry 77919: process perl pid=29453 uid=912 src=32.158.4.95 args=nk2q 2zqamj5p-5dqd51xzxnr88buen6ug4qjfq2pmou/ -h
  - Log entry 72298: process ruby pid=24615 uid=741 src=121.176.12.215 args=gjyrxfu2c0/40ytkxytzh-gk4f09q0mgbfk6m0-- kfwnzox

## Supplementary Technical Detail — Section 48

Automated correlation engine identified 42 related events in the 6-hour window.
Baseline traffic on port 56147: 0 connections per hour.
Observed traffic on port 4444: 109 connections during the incident window.
Statistical anomaly score: 0.975 (threshold 0.750).
Related CVE: CVE-2026-34822 — not yet patched on 19 internal hosts.
Affected subnet: 10.6.4.0/24 — 22 hosts in scope.
EDR telemetry: 3 alerts suppressed; 1 false positives removed.
  - Log entry 29496: process socat pid=29409 uid=301 src=197.44.201.16 args=hxjur3rtjgeopkoz4u690pfwifjfzgwp27pu9rd5obvnpjqs
  - Log entry 39659: process bash pid=13479 uid=349 src=114.183.240.221 args=drbs1//8- -vw6u7ldf2lxuognd-6nnx3zpzrf20v3jnfdqr
  - Log entry 38011: process nc pid=17929 uid=463 src=196.249.165.54 args=s09p5-kwdihp82kmxxbb4khcv /btrhpgeozgegbjpn5lhx8
  - Log entry 77045: process python3 pid=14143 uid=977 src=84.241.174.75 args=v/ 3h01d999xw2-0ih0ld84r-816zbhr6wre4fsu3boizz6f
  - Log entry 14308: process python3 pid=13373 uid=828 src=173.190.135.161 args=8dleqvz0ivnx2-d56hsp5vzpiedfn7nn8qo6t1a6z81a o8t
  - Log entry 53496: process socat pid=15498 uid=705 src=114.193.183.47 args=2sr8uhos28m6k112v0u3cnhc-46w8flgth-a5xtj64k3btoh
  - Log entry 79720: process bash pid=21515 uid=451 src=118.12.62.168 args=4e3ch6vp3z0rgbabjv63-2otyddbzgw5pef7u8r5wc sjtaf
  - Log entry 48726: process socat pid=30125 uid=762 src=155.75.231.24 args=nqjofosd8t8fq9nm v2ocwf5-066x5hnlgku z2-t7h65ssm
  - Log entry 81849: process socat pid=21187 uid=733 src=184.192.108.71 args=-0y8a -6hfun srqitokt6 2gp1becws38gxj40gvpz7fmws
  - Log entry 20749: process wget pid=22099 uid=228 src=35.23.202.182 args=2y88l 7poagvm225o19lts2u4mgvcbfidkbr43ybsc1m7zjh
  - Log entry 36363: process python3 pid=25551 uid=659 src=207.246.13.6 args=4k9-ui1zwft2lc9--xgw3i-w31-e/17u56m3c7rur1eg3ejq
  - Log entry 73830: process bash pid=13358 uid=595 src=155.49.154.113 args=szw875 0pgs3p 6jjm0za3ida959qfs0evjtui8w 5fa48x1
  - Log entry 55635: process nc pid=23937 uid=555 src=1.239.228.147 args=agrdalr-8xez//qa2buqg5yf kh-cg6pmgoavp nfe2ce0gr
  - Log entry 15313: process nc pid=7352 uid=416 src=128.30.201.181 args=5om8ecetsvhgcc9aoo16jb/4vopfubocukb/1a8ghu1h9hy3
  - Log entry 90705: process perl pid=18832 uid=607 src=103.65.19.20 args=89xliu4sliin9erplyotgspvtg0avu7x8zcow-29cay-k4yd
  - Log entry 12796: process curl pid=14691 uid=377 src=73.57.116.32 args=/ 8yf6kwsnazmyu2a9v8cg4cjd74kj 7av2kuw77v1564nmq
  - Log entry 32940: process curl pid=13959 uid=858 src=27.235.32.241 args=s36-d  xr/56ahc9gt2nhjlx7b8b7y xc8o9-xsa8irsj98f
  - Log entry 66125: process sshd pid=13641 uid=474 src=28.172.239.237 args=fdud8ie6s4iklx 6i7bf4455ejhanoj/wxnpgq8b6d  e1e-
  - Log entry 23679: process socat pid=20897 uid=857 src=32.192.190.225 args=9dun78hjao un16qn/h7u e4m1bzk6va m2xs0kel80zyhx1
  - Log entry 30300: process wget pid=27707 uid=487 src=60.129.227.80 args=s-pq6u31 il vkezpx6 uqzggkkn4 hgq-m4q7 vqu-b/zwk
  - Log entry 71260: process wget pid=10948 uid=310 src=130.177.33.189 args=8eciyfw0xsjezlacpiaztqau9ofyzl/xqucxcqnnuq4tcg0m
  - Log entry 48357: process ruby pid=25784 uid=404 src=79.85.227.26 args=cti6s0oyw6xzta94cjdbhgmho3a82w-67k/qtvok-il0tvw2
  - Log entry 17025: process perl pid=29943 uid=136 src=77.29.126.120 args=utj0-43o sspmosae-k332of//-kixvgz3iyyxsj8ugvk7rg
  - Log entry 63028: process perl pid=30989 uid=908 src=138.24.221.52 args=3yol 8mp1v-1qipxcxe1ct7t7ovb28oor0ht597o78f1f9r-
  - Log entry 89470: process bash pid=18699 uid=328 src=138.57.254.72 args=pzp6w0sesb0qzswred3t18 babrtjyylgs1yl92i634okyh6
  - Log entry 40901: process python3 pid=20004 uid=54 src=199.244.35.102 args=99s8nfjq1ts so0xaoshqqekyc8kol0f7piq65/9qbj25c5h
  - Log entry 44988: process sshd pid=15888 uid=426 src=152.233.185.98 args=lbfgw g9sla 43ih1ho 7347l6mk2lm95rblut4a53j/jp6u
  - Log entry 96260: process bash pid=5703 uid=703 src=67.228.20.34 args=i-ytdbrxfjsx1toj5kemzy4mwclrkasu1q3o3dzwil3uc04r
  - Log entry 41761: process ruby pid=24887 uid=986 src=75.81.24.154 args=2q1tjpl0dn6y78ykn8-umc 913ld5ffkxl/7okv0b6donwrs
  - Log entry 42055: process nc pid=17009 uid=647 src=21.39.210.137 args=d/3htbklcvpge6hgtldtgmgfw2zd7-n564v4uee7zzpbttre
  - Log entry 33647: process socat pid=14349 uid=686 src=74.65.149.111 args=t5o5kqa7 dyoce0 y7t/0dzbhw5u40o3fqduvumbky8bl99v
  - Log entry 32354: process curl pid=3701 uid=498 src=27.234.23.143 args=fonr6evejv6c/11azdys-0 d4-fo1hkt166wdcq r84-n9a5
  - Log entry 71128: process ruby pid=28142 uid=574 src=14.132.140.77 args=a5r46zilselrc-6uvtjps/puq8lz56o5si7bsxypcpra-kmd
  - Log entry 60408: process curl pid=11461 uid=970 src=194.181.126.134 args=7e1lf1l6xk5te/5run51ei/wwzs/jz/z9/xmjko1jmkb-s0k
  - Log entry 19575: process bash pid=24165 uid=250 src=37.222.213.129 args=ln-3ppk03qbb m-zgp8bnkrsx9jv1g0dypmj955p/v q7k6z
  - Log entry 56482: process curl pid=25669 uid=404 src=69.104.187.63 args=x668lkrbi6phi/jyzw9tdlsj135e2e40p/qg3foezc0asqdl
  - Log entry 20360: process perl pid=18750 uid=315 src=211.28.130.162 args=u69h-y h-v7nv1r0wgvlgb5cwc-2o61loeci-ksqhj0wkhuw
  - Log entry 19269: process socat pid=22783 uid=737 src=198.161.126.64 args=8q0tz6y/5vug/-jah67bv9wxgvmf1v7vwiojzr8u1u2wfw01
  - Log entry 59560: process wget pid=30814 uid=801 src=193.4.172.144 args=vkutf0v8e88brmar55ndu88rg3vde66mel8cly 5i m3zls1
  - Log entry 37040: process perl pid=27883 uid=247 src=133.132.60.92 args=wvu6v7vx-me15l9p4gr8wtx2zc08u5xgtw nu49wbgoe-93y
  - Log entry 36565: process nc pid=25243 uid=450 src=145.16.180.122 args=q2aoh8f26tcshfu871s76e5uw273yq46oujcz/5s5f6pu-6y
  - Log entry 78202: process nc pid=9463 uid=565 src=102.117.146.104 args=k3c02x5nnxbkkzt 1j3kxzczrm lom4npfgcz0o78mg8wjrb
  - Log entry 75494: process sshd pid=26136 uid=886 src=108.110.79.153 args=hju-itno2uqqlci95l450c19mq6h4mrno3d-da3mld412529
  - Log entry 58411: process nc pid=19512 uid=703 src=212.97.85.125 args=f1x4910-bv3kqnm33y/e7pp2vqrd1h1-u8hwn0-b 9f6vf3-
  - Log entry 90277: process curl pid=10740 uid=105 src=200.111.64.28 args=kkbpz68nue5lbqeri/38a403bvka9me2fkpplzqju3hzkeih
  - Log entry 50944: process nc pid=25456 uid=904 src=33.138.168.201 args=76nxok0ig6caavlw639fw87sn-vxr/i76v0fu139unrfi88q
  - Log entry 33974: process python3 pid=3741 uid=499 src=164.176.255.44 args=4vkh -3wn3e-j1eeud1g/owzv0lhqktryi6jtvlksixwc6/9
  - Log entry 99055: process socat pid=31391 uid=26 src=164.130.216.114 args=ienqj3-j4an8 cod3qzin56hb4u6ubi58kad2/bl3hfqo/xh
  - Log entry 17887: process wget pid=3209 uid=345 src=66.58.111.253 args=eg42wctifv2c9bx1y9nsvxrm75i 514nkykywm 57vspfq5o
  - Log entry 54941: process ruby pid=13332 uid=66 src=103.16.108.99 args=no/lpb3i1ab0j80sccdrn/4h1u85-d4qnszttyvratubbc6q
  - Log entry 87289: process sshd pid=29285 uid=63 src=201.52.81.212 args=69fn4wo/xzynu0/67wxf pbxlxkqdkfhjlqb7xvj662uipcv
  - Log entry 52422: process bash pid=17320 uid=80 src=86.242.173.75 args=79 eh/l/cvff4z//6670hrhwjyp e5x0c9qbaz9y1dcbyx94
  - Log entry 91476: process perl pid=25575 uid=985 src=138.43.60.156 args=h1517w9aseix4c7woqb9roptsijxi7/cx9tezx4gmtdymbfn
  - Log entry 13669: process bash pid=17565 uid=147 src=172.198.73.194 args=xjto/ytugmmfcy9cr4jcai-lp38pfmg my5udh6airw38urb
  - Log entry 63688: process sshd pid=18338 uid=298 src=125.242.46.157 args=0d45zi0sulfdcy/pqlq-hbgsh8gl9v7h12ghyva3d-/rc3bv
  - Log entry 22478: process nc pid=13971 uid=684 src=175.159.162.87 args=s25at9he2r3mt090ncynx0nk2ethmi38/ztut-yrwjw3zk3d
  - Log entry 74219: process curl pid=9925 uid=613 src=43.146.86.205 args=48i4fqxsjzyuzhuu2bp2fdi5e h-62ec8p/u44uwn 6jrl /
  - Log entry 26388: process python3 pid=3791 uid=310 src=167.159.194.156 args=6raxk1k88n0-69awx09oprvi7ijzriydb6twrc7rb--rk1dr
  - Log entry 36329: process bash pid=31796 uid=848 src=67.237.222.18 args=5vgg66ft-yycrnlm-nd4ao79zcchb-az3rewul85a/9y-krk
  - Log entry 13684: process bash pid=25013 uid=364 src=193.250.238.165 args=n4z0768-g3y okepygzsl7a8rx/ou33srjrjwy/x2p9nlu-w

## Supplementary Technical Detail — Section 49

Automated correlation engine identified 11 related events in the 6-hour window.
Baseline traffic on port 17685: 1 connections per hour.
Observed traffic on port 4444: 96 connections during the incident window.
Statistical anomaly score: 0.971 (threshold 0.750).
Related CVE: CVE-2026-31325 — not yet patched on 12 internal hosts.
Affected subnet: 10.3.1.0/24 — 16 hosts in scope.
EDR telemetry: 1 alerts suppressed; 2 false positives removed.
  - Log entry 52588: process bash pid=27567 uid=543 src=187.98.2.8 args=6tczw3qzzej0xfiaaejwl 1i6ptc6xeq8ozd-m0f 01hur5y
  - Log entry 24596: process python3 pid=23617 uid=2 src=47.242.19.138 args=mi7sgwwf5qv1zdcplayb24samfvh0q6ql3tdrkez3el1la54
  - Log entry 80372: process ruby pid=10592 uid=1000 src=130.44.176.18 args=a07b-gzn68laqvpmmlinpflecfuifqdaggakr65n asq/vn4
  - Log entry 10769: process socat pid=11205 uid=947 src=84.231.40.159 args=jnhone4ht3l3l30j pxk2897zkqq/oit5 suv8u4ds51d8l4
  - Log entry 91517: process curl pid=2327 uid=935 src=90.30.148.19 args=9io4gipdd57-kg9p4jmfmfwih09su-y arn7llw5gwyljlk4
  - Log entry 24197: process python3 pid=18884 uid=315 src=145.97.200.132 args=hz9bzlafhcs68ni/n2gkaoyzqnn97ns8u4l6l6/wxt6hydb7
  - Log entry 11276: process perl pid=31269 uid=295 src=76.53.53.128 args=dnehv1vy1hjo -k94f5 pbsuewpetxus3wp5 l2pzw7gilxc
  - Log entry 33677: process nc pid=27188 uid=120 src=67.15.26.249 args=/8l9gymjdt- i24rz43joohx9l237/76pw3ki2y pfe4 tnf
  - Log entry 69275: process ruby pid=15219 uid=27 src=51.119.3.97 args=xdxmunlc37-avp-obj/p0d vx235rahnqqmwy5n2gkiowct7
  - Log entry 77421: process nc pid=22219 uid=291 src=6.112.55.90 args= 5os-vkmr4a9jpg qjc23p9jts18zztetw3cxi1-2iep0ytj
  - Log entry 58637: process socat pid=12497 uid=316 src=94.230.157.250 args=5s1y32ferrvgr3cpsbayaukb5-jhfmy9t5t/6liih/v0lgdk
  - Log entry 73268: process perl pid=18535 uid=118 src=140.28.40.98 args=c5po6ux30hr6aebdg2u/4x9uveaci2o290gscxn3ypg-rnea
  - Log entry 60806: process sshd pid=24948 uid=181 src=179.243.191.224 args=z152j9gr9pfugm7j3au uor31969u-n5u1ezwlq3ekgpk7n8
  - Log entry 56274: process nc pid=19186 uid=392 src=172.127.12.158 args=ix 9ny/5u6g3o333b89a6buexejii 271wu4rivuqdywsh w
  - Log entry 26309: process sshd pid=22134 uid=195 src=95.49.157.77 args=vyt/zkq92qdstc58oif12a8i7i60fqu/xflh38ucs-u53krp
  - Log entry 50045: process bash pid=14316 uid=326 src=50.92.67.113 args=h5jzhf8fglaacbyqn790 1ezei/i7gdo9a8u9ljxui1/0vyk
  - Log entry 66635: process sshd pid=30437 uid=55 src=82.63.135.137 args=e5084xd2x7rr/8ql9edlgw1e27z3u-vxda7tveao14qei79o
  - Log entry 18330: process curl pid=28093 uid=347 src=163.4.104.193 args=gdvr spj23xjkloecktz6xf1e0fdlt/1jkfz5-x25if/1cy3
  - Log entry 25462: process wget pid=10013 uid=795 src=1.53.226.111 args=w-p2gabb jrjjnitn2mbuhadkz4of1w0-81tbqw0pik6054j
  - Log entry 64837: process wget pid=28857 uid=845 src=70.23.4.22 args=gwce7e6eed/smft/wj-asgw7tseo4vw1nh5bw6qf8kme4z/i
  - Log entry 86203: process socat pid=26477 uid=924 src=92.33.210.123 args=1slgdo5lnd t3u7dytht7e104flikccs53j-hz25nlqr8egk
  - Log entry 87295: process curl pid=18656 uid=498 src=168.159.229.154 args=z1t34/v68u hqsqp6gtev831covjr59wxabex2/h73yzu76m
  - Log entry 11290: process nc pid=16705 uid=193 src=200.214.172.220 args=z0e7sez90nqbdf zjnhftlfnw3dtpoasg4p2qyka/f osnmj
  - Log entry 34923: process ruby pid=20129 uid=889 src=172.203.254.237 args=wzktqb6wvr3gy/b2-ify uj9iqutaek2h7gw8rlq5akap2nl
  - Log entry 95369: process curl pid=4192 uid=419 src=209.65.130.74 args=yzdkw2 ycc3thhrnrvolkuqhx80yv7czpl/w7y-2nkth35au
  - Log entry 63217: process bash pid=10722 uid=990 src=113.126.180.111 args=an74c6ppqj0y /n0bratnjuuyi97yq4/j393kgmq63ib5f88
  - Log entry 17501: process bash pid=10127 uid=427 src=178.250.189.84 args=pgz3u-b  ch /60e336bdqiksmeer5it/1u8ub9d2sheid5-
  - Log entry 90505: process bash pid=22019 uid=358 src=84.169.22.112 args=slnggw0d0a/lnb083y17x-qr0623uf6 khgrq-g54z107b8k
  - Log entry 42077: process nc pid=11299 uid=175 src=130.3.182.252 args=mvm7jm25zy4ebe3153cubbc1i7a-w62 31hyx58rixsl4eg 
  - Log entry 66871: process ruby pid=28207 uid=488 src=186.15.212.155 args=cwuk hrt9znfryu58u t zk3xh8i/oy6iq72my1bi5v-bnb6
  - Log entry 98919: process python3 pid=26885 uid=638 src=5.174.109.50 args=b9vin4xzfuusrpflak9--1ed4ik7mhqvcy/r4t3syvom4pte
  - Log entry 14658: process python3 pid=21219 uid=472 src=198.244.207.2 args=uosdtu rxikg1dhj/cgxd522zk qko7/kw1zwomb0-z52qmv
  - Log entry 49381: process python3 pid=8166 uid=476 src=64.33.173.34 args=xkvx01azazeu1s6/v-b9mu8s64380fa 6odao9jp7dqgft4-
  - Log entry 58231: process wget pid=29506 uid=647 src=67.179.72.21 args=1tm7f5b0cmatuzbvvd3phe ki5ls//8wm4 fem0vzrjfuj v
  - Log entry 98264: process python3 pid=31711 uid=739 src=182.252.105.156 args=doiiaa5ok2rboln08zs9wctz2d/du-99kspmamfoe42huswm
  - Log entry 92668: process bash pid=7111 uid=693 src=70.32.237.113 args=8ka4o8ytmnzk50x0sjdi8vmfci09vv0aksps57isr/9112bk
  - Log entry 13041: process bash pid=30478 uid=6 src=49.142.11.159 args=0kwv3ojjgdbf5h yv9gj xt0el6lasy03nwwku8ekonr5hhf
  - Log entry 74652: process python3 pid=1241 uid=898 src=150.218.134.217 args=mpi98j546/ayw2j1nhou3s6ygszf6/ff7i6-t3pno-p-e3ar
  - Log entry 13659: process nc pid=29702 uid=491 src=124.167.77.43 args=h81y1oi4 n0w-do0dmwep355whyn99phix3hvb-qwl0mm/-3
  - Log entry 83919: process curl pid=19296 uid=105 src=86.125.0.90 args=1x cqzqti4-t1uhihv4gfcsu2xlxg1sta5y5b is4jltsboy
  - Log entry 77804: process sshd pid=1847 uid=759 src=213.181.229.136 args=3thcivkn2hgh n/nq3shrmeqq0s8t3/s4k/ohoz1rxeku3z1
  - Log entry 34268: process sshd pid=7339 uid=568 src=15.70.107.150 args=3k7virdmq4oecjtvq8dqc0yb-ylijc2zvjxdx3un6eokqmeg
  - Log entry 69573: process python3 pid=16320 uid=574 src=118.224.16.157 args=r70cjbme/is5bzu1fqlfp4rrf4l/0ivqk07kc/kab1vagfqx
  - Log entry 47889: process bash pid=16979 uid=640 src=48.72.23.122 args=u9gkn4f ooqjzfcj1mqdrpyhixdhhg-kfpaqyxeg1a/1eccw
  - Log entry 28916: process socat pid=7573 uid=27 src=84.6.199.236 args=qxkmzg46llwaot 5w9ike81vw5fuc70bcnvo-gb-1v39hyli
  - Log entry 79360: process curl pid=4765 uid=19 src=33.43.249.183 args=2nzvh0o5b430xspbrwus-0192gp74h0qdl3ge67x5apo-ebi
  - Log entry 16826: process bash pid=24157 uid=97 src=44.203.148.86 args=-n6qrawo2c37xea2rplazjrq8ia5-gtk6n0/yr5o5dpq7lu3
  - Log entry 49430: process wget pid=29310 uid=647 src=213.13.169.88 args=wxa8wfnrcy05opetry/5kyscd110r7sv9/-qxh5322qt37d-
  - Log entry 98066: process perl pid=22770 uid=832 src=185.96.172.87 args=s/44vtf1nf yo/31er4918ip6yx-6xivlewhmk4g nyh/aqb
  - Log entry 92664: process wget pid=16875 uid=510 src=74.106.66.30 args=3cyyl20vj6h7demp/0dvhdk5y1fg75w/pkp0z-qmiq0mdl0w
  - Log entry 47795: process ruby pid=14150 uid=585 src=13.182.149.77 args=k/cqk3g4qrugdc/ak41miizy2i0nfefdm/pj07bt9yvyh1op
  - Log entry 77043: process nc pid=9206 uid=762 src=75.10.215.239 args=fxbz20ogz-9tn3m8jrg7y1r6jc2gcpl7e8k 1ljl4f14gp8t
  - Log entry 83857: process socat pid=4178 uid=948 src=200.184.13.80 args=chue78-k5cvyl/g3zo49gi4/8ornnpluxvn 3ln3196t4684
  - Log entry 78779: process socat pid=17675 uid=547 src=167.184.193.150 args=sf8hfopdqa-3l3i7n-ok8pzt/dpvji5w9k--pr1w4qb463av
  - Log entry 87951: process ruby pid=11613 uid=452 src=145.128.123.192 args=rt94k1-f/ndjywrv66pmzo4ebhhgax-gh3j8d5p496x-07u 
  - Log entry 62586: process ruby pid=27677 uid=86 src=6.28.26.71 args=jol99qswss2zly8k38s-fogq -ptlc4/1q1 sz7lz8zir893
  - Log entry 82180: process wget pid=6636 uid=789 src=204.149.101.88 args=-ao6fv-6m8o5ju b5qmgba8peuz9ve9781psnnbbh9/dap63
  - Log entry 23041: process python3 pid=24537 uid=361 src=131.22.241.36 args=1oinlt-froaycrp2u/nfm17sohw0gbuuild 6uv76jqvucr-
  - Log entry 63455: process sshd pid=25900 uid=569 src=102.133.6.178 args=6jr3sr99d/lhhu98fhfnhgpvlbo0xwt33ei8gk/1lb-5pdw8
  - Log entry 22532: process python3 pid=5895 uid=919 src=191.243.112.192 args=5-/refnjrzwz7b 66k6kk24d1t0l-y5-lhr806q60l6raopl

## Supplementary Technical Detail — Section 50

Automated correlation engine identified 31 related events in the 6-hour window.
Baseline traffic on port 22829: 3 connections per hour.
Observed traffic on port 4444: 119 connections during the incident window.
Statistical anomaly score: 0.890 (threshold 0.750).
Related CVE: CVE-2026-22000 — not yet patched on 10 internal hosts.
Affected subnet: 10.4.4.0/24 — 19 hosts in scope.
EDR telemetry: 2 alerts suppressed; 0 false positives removed.
  - Log entry 67224: process python3 pid=5010 uid=368 src=97.23.124.64 args=1klc/2r8vhik4nfh9c9hu50fg5w5apwxj3jjsr-gny2q6ef8
  - Log entry 26980: process nc pid=30884 uid=853 src=207.65.216.209 args=dhqax-amls5fjuabx0fbo03 kgfibto8th84ptw6tladg5tl
  - Log entry 84867: process wget pid=26303 uid=304 src=183.238.119.155 args=rebr8vks/fbm4f lk0ssb-mj4gaugb7gcjjlgu3e3mkrw90s
  - Log entry 88510: process sshd pid=28359 uid=851 src=177.222.84.88 args=9b5u 69-rzlwplonedb93ykj6n3/hvkmkfq0froorebgl8ls
  - Log entry 53369: process socat pid=14983 uid=764 src=197.69.118.228 args=bljiebdnbwwg2- jrmnevofcfef3rmgj81-mvmylq2ut1-yc
  - Log entry 94685: process socat pid=13282 uid=30 src=198.164.64.70 args=fi6kmt2yeeyl139gvrbin70si2f2374ttuk2azc6pl8cpdp 
  - Log entry 65893: process socat pid=15413 uid=221 src=31.162.184.58 args=ipd27denosgy- 3w/d53/7m4f6kaul6h5uxnt4-a vk4bfdt
  - Log entry 69360: process sshd pid=6061 uid=205 src=23.4.49.83 args=m0r562r/b/68bqz32ncb08c3u5/bvjq7i86tjf5egkbel3hz
  - Log entry 64994: process ruby pid=1171 uid=301 src=207.18.251.95 args=s3l-o7t7e8wbvojshq9kmhi9y1dc 2alifv9mi2qjxrytf29
  - Log entry 97424: process python3 pid=12622 uid=179 src=173.11.227.238 args=mty15/5xqw24v4l49x7nha8m44y7q0msi-sfn-p90m-sfs6b
  - Log entry 78914: process bash pid=25096 uid=396 src=147.217.63.152 args=iyrkhdradbvj at/ki27c7t1wt mbwkbj4xci9tevel 0r/c
  - Log entry 80321: process wget pid=29079 uid=8 src=95.24.104.145 args=x4 eny9c8n8s7z7tb71gbf-pxb8ay6qzhy4eysem8ixcdoyj
  - Log entry 49557: process nc pid=24735 uid=27 src=145.221.183.139 args=7 7a7i8qloh6de67pcqxe-lg5rg93fc5aon2khiykzc0mfuh
  - Log entry 72958: process sshd pid=30856 uid=200 src=85.242.88.156 args= 5kfiyn4egrjcxzvwla-ie5odsm ulxwprgvtp0dekuzeth5
  - Log entry 39054: process nc pid=20222 uid=657 src=159.186.53.86 args=eyf5ws-/1py4iwdx/b-1r7k7w27fjbt7b59x1pmg-nbtdcmp
  - Log entry 37682: process socat pid=25480 uid=281 src=151.102.23.24 args=drs/nyzhlvhwlqdgbv16p1/lgtgkwlc7ax0ga01yxf0e8qgo
  - Log entry 74591: process curl pid=6603 uid=988 src=212.200.152.124 args=h1zg504yuj0x-6 eouvjjjdgp087ostgq/e3fx qs0 n-t4h
  - Log entry 52070: process socat pid=25002 uid=759 src=49.11.137.112 args=yapwar9-z lal7df4iqbr828s/r9dw/rp66spvrousur4oz-
  - Log entry 69566: process python3 pid=12456 uid=858 src=8.97.84.190 args=dcqa6v451aajfynr/use o-/565omqo-o hqz1cr4nmprdx0
  - Log entry 95564: process bash pid=24488 uid=751 src=218.185.206.160 args=42la4u8i2g/guac9dmdu95qfef-32yrz7f0sj7w 69lwa01f
  - Log entry 53435: process nc pid=19991 uid=831 src=189.236.118.205 args=d57yd8zwkq315uz6edv5357tmwrp59ct2ld0423igm36cabi
  - Log entry 92683: process perl pid=27479 uid=692 src=49.58.227.229 args=gav15is6rwyzp2op/ce8fpg4rvo1pj-vbdd/1ryhu s9iiel
  - Log entry 57080: process nc pid=7365 uid=423 src=211.67.27.201 args=g3 65rla11mkp06a2969p-8vj9-8yv1l3bg90b4ou3a2wfdi
  - Log entry 40233: process bash pid=10847 uid=432 src=155.186.29.104 args=o47legiuhjwxz7vqbzhxas5k1efzwwt40/k6/rxzsnbf3khp
  - Log entry 40576: process curl pid=29027 uid=103 src=158.4.192.216 args=ghk7n44appwwmf648ul9ht54tiu9gzb8pyb0l8u1pirfzy2x
  - Log entry 40533: process ruby pid=12405 uid=391 src=4.229.199.49 args=2fska091rlj2bfnmcqhcrt2pfywip-d/ 4c3cujcf/a6psif
  - Log entry 34887: process wget pid=18415 uid=271 src=127.154.216.209 args=q0hwhwio sinp5xzjaehsqmd0f7offth6f fiqev37m1hxh3
  - Log entry 96624: process nc pid=19617 uid=337 src=1.55.190.236 args=m/h5gaoudytbrrvn zh3c8u2i5j/lcux-gebjwahv7/nvl/s
  - Log entry 18023: process perl pid=1398 uid=901 src=141.229.227.20 args=r omojnyf8isph-ut7ma1fued5ngkn kkbb71o16wg7w9sfj
  - Log entry 66646: process curl pid=25496 uid=775 src=214.157.176.131 args=a3x8iq6wzr69-v7y0f717r47o1eqs/1sp4c8iq-uq f/57u 
  - Log entry 59807: process nc pid=9784 uid=182 src=83.98.114.204 args= 5z1zo4j089q/rhnz/wfk--uk06jz0xb3pbvm9f0r 28bc4g
  - Log entry 46653: process perl pid=15435 uid=495 src=26.105.49.50 args=d8byae9cuog-r0vkcjhrwgy4mr3wddq3uqm-t9mdt/7hgheg
  - Log entry 81091: process python3 pid=13926 uid=415 src=162.68.63.133 args=cill4p09y//r0myqw4fuk76ye569qwzu798oiw-qpe33l522
  - Log entry 13627: process sshd pid=19873 uid=429 src=2.126.222.128 args=y51bai4t/c76eiw/tk0fz8dci6yft8f/auf2ac7cxteb 4oi
  - Log entry 96746: process sshd pid=4010 uid=158 src=75.47.18.115 args=6u2b  uts3x5m-ogzqqeuz0ho5w-ayza5kk1-r4c1/zscuwc
  - Log entry 87119: process wget pid=16252 uid=666 src=25.184.245.132 args=lrhf-lgdhpkz04kv rthiw zb31g/o7hw-z6ri91uvv8jvft
  - Log entry 30845: process perl pid=17015 uid=940 src=161.65.88.103 args=izr21ql88m0cskrg9m33bagnsznhwx/ 6e4kjhxg9m2txker
  - Log entry 35499: process python3 pid=4319 uid=375 src=197.202.166.97 args=aqvns0k5evlf1wtuktcjy0 tiedd6x6bv3nckmib6qof5f6p
  - Log entry 61934: process nc pid=12862 uid=916 src=104.71.37.43 args=/yn1 ldwitbdifie 0u54ecxer7ub285a58acy8y1y410n72
  - Log entry 51253: process bash pid=2970 uid=739 src=67.149.245.117 args=tkja9o59r1dpwyldt3vse2h45s6-ju887jn-k57/0f6b5jph
  - Log entry 18996: process sshd pid=11155 uid=830 src=147.17.221.9 args=2spj7oe6j2nd pj7 hl 5q/fipkhek8phhptourjte06cr9d
  - Log entry 50988: process sshd pid=14145 uid=744 src=198.99.204.235 args=-uvsmpy67hfw2fm9ov c7h-/u-twncllnk2x0dub-p6gy1bv
  - Log entry 62970: process bash pid=10563 uid=392 src=102.19.89.179 args=wprgfulpveubhzsv226op81dnr0m0p086f62/rdcp10or96n
  - Log entry 64028: process perl pid=24944 uid=99 src=150.60.127.70 args=dhvr0lhzaxi59iek1pma6a05ored2q/yux mf2z8jhfbwq3g
  - Log entry 48410: process perl pid=12599 uid=427 src=179.94.201.78 args=acpvx4raj-xo nbn bfyl8u6m24d16dywho3k1yt/e1csnay
  - Log entry 40984: process perl pid=15070 uid=921 src=116.147.200.154 args=bdyutwcj79tdtd941haozzbkmth46-ptpczvgrto26/3ay i
  - Log entry 54862: process bash pid=21854 uid=440 src=140.43.64.130 args=r56li87mvwp/i5uijqfnqmwzqrk4x1qn0r5fndxpb5apqr5 
  - Log entry 28816: process perl pid=29688 uid=687 src=144.193.178.89 args=sry rkq41ibl1sqybzoklpq93kvx57ygzsxfw9b/2-kr8q0w
  - Log entry 72825: process sshd pid=2230 uid=116 src=40.16.81.177 args=uf9n4ae 635ncd8fum1f  nqf mmv3lv2/0d1-1tnt6loa8o
  - Log entry 26679: process perl pid=25537 uid=50 src=203.204.159.236 args=cojmrgi/qowo/j33c4u97z9oeu69hofh186j7np5st-v5dje
  - Log entry 34686: process socat pid=24581 uid=368 src=197.191.27.214 args=m2g449vxqje0unmspht8ac-mud8q57fsjevsyab4cto1nj-b
  - Log entry 58234: process wget pid=18907 uid=841 src=131.154.124.44 args=-9f0zxxxv4gxb0cp850unyu8ff1- 75p6gv1t4e64l2fe-72
  - Log entry 84874: process bash pid=20580 uid=966 src=110.18.149.199 args=n12t/74pa6fr5d83zfc-zsmi82 7lymhdifn-k1klnos10 y
  - Log entry 12032: process socat pid=15057 uid=314 src=61.107.233.154 args=8993fac85jzs9tq7t0x7k-arq9-jrt 3wyw6tgjz/qf/f08b
  - Log entry 99311: process perl pid=31818 uid=375 src=144.7.180.240 args=y9/04fypg29gzbd8dp0ymmdt799p -0d u x0yraum/15vfi
  - Log entry 97364: process bash pid=15414 uid=763 src=208.98.112.93 args=8h33u46xufpbvqtjhu2da1ykuf5pd68k2q0t2199j7tjto4h
  - Log entry 57479: process bash pid=21480 uid=259 src=142.217.182.229 args=ehg8ocsddqm-7dc3get30yjnxe4vln-qvj51qa25zs88upyp
  - Log entry 82508: process bash pid=27082 uid=147 src=120.90.52.55 args=2ucezytkot7hvv62j wlsj4vtevizq2-dnma74wb/vr1sq5f
  - Log entry 65594: process nc pid=2394 uid=105 src=17.11.119.119 args=c60ijeyk0whfpryx-7d1jumexpw-5jp0irmczm6utslvm6oz
  - Log entry 23333: process sshd pid=21103 uid=657 src=102.64.216.92 args=ke7kod9pcgg4io5tqp6zc-iv4ds8y-i-d2e6uyts6e7x9fxu

## Supplementary Technical Detail — Section 51

Automated correlation engine identified 44 related events in the 6-hour window.
Baseline traffic on port 54994: 4 connections per hour.
Observed traffic on port 4444: 163 connections during the incident window.
Statistical anomaly score: 0.943 (threshold 0.750).
Related CVE: CVE-2026-40833 — not yet patched on 14 internal hosts.
Affected subnet: 10.3.5.0/24 — 20 hosts in scope.
EDR telemetry: 5 alerts suppressed; 0 false positives removed.
  - Log entry 10533: process python3 pid=5257 uid=242 src=73.87.232.173 args=oe/wo-s66t2f9-einnrhl0x3xf1eu136u01am8sdjhtmxoj 
  - Log entry 52970: process sshd pid=21810 uid=430 src=22.188.75.61 args= dgt859t-f82bs-vsr-y vsrrcrtg318dp 5x-d1-0e520ii
  - Log entry 10930: process bash pid=14133 uid=155 src=72.164.177.108 args=8bo4e-92flsezp9zxl47w/0svk6p-0/veyuyblaowed2 49g
  - Log entry 91899: process ruby pid=3711 uid=61 src=120.137.144.143 args=gzg ve8rz8k5k8d-000c84m5 nhd6f27xz6hd-uno00xw71k
  - Log entry 75909: process perl pid=9225 uid=565 src=124.229.182.224 args=3k8ks2j0gi-qy4fo//vfhdoqjv31roi11/ 8y3h0ckm m68k
  - Log entry 24799: process ruby pid=13167 uid=833 src=166.202.106.6 args=6tsf/18n49klqnadinp-4ouyosp-mmpewd3yrzsxemne77n/
  - Log entry 14847: process curl pid=11825 uid=962 src=163.230.99.224 args=ayhen4df0ohwq2o5wcxdd8iw otrxd9do---w/9ghn9 ay2m
  - Log entry 40797: process ruby pid=3116 uid=688 src=181.3.249.217 args=0bdiypt/fx3rwb4vx5x0d0sm6lqw-n qnxg948wsnzajoo2i
  - Log entry 48135: process ruby pid=5382 uid=124 src=160.73.19.135 args=yv03q2/b1t/eaou5e35pt7oqcv-k-v3pzllqfwbk/dzilkrj
  - Log entry 28188: process ruby pid=24533 uid=128 src=142.189.97.249 args=hbgadu6l9g38e0rpzkt328fz7 yms0-egt6omsklbkqyaoot
  - Log entry 79397: process socat pid=17648 uid=244 src=24.143.218.217 args=ku-7eeflg g jv0woujrkltq/bv0 ufx y5atxab6e77neue
  - Log entry 88315: process python3 pid=21427 uid=149 src=133.160.135.170 args=zhn5/0 660pqw67it4y rtdbs0 5i-140bdr -/babcdj-wk
  - Log entry 38310: process ruby pid=20912 uid=808 src=217.236.227.252 args=q6552ln4v-u272n4t0uoi6m k/4q8kob17csh-z8u9m5m3/n
  - Log entry 29424: process wget pid=20464 uid=237 src=199.220.195.248 args=ttdimetywlyta87mujs81/47bvft-ez5xwere zjxklrhvuc
  - Log entry 59881: process wget pid=28977 uid=636 src=81.121.255.195 args=7fyyp0w3vcxp6u7ga4dvrtvqem5ms93sq8cj4/y-1sl1t4os
  - Log entry 97200: process wget pid=2948 uid=590 src=97.64.70.19 args=iwmc1bekgkp/7zw7oddt9xn 9x1zjkw0fikoqzweoo8u59 4
  - Log entry 90773: process nc pid=13939 uid=965 src=108.127.156.41 args=oh312o6jm b8zw6yxi7r0lxh3q1clbczq nx9-k7efy0d14 
  - Log entry 19123: process nc pid=17432 uid=764 src=29.89.39.148 args=bqozwc5mah4oiq9ssxt0uf3qndag1ltudj--c9ws8softho1
  - Log entry 40727: process perl pid=14332 uid=679 src=55.244.79.30 args=/iqev1biv xjpvut1drjb/h3o6-xs46sifwtg56gizkf-/yv
  - Log entry 56720: process nc pid=5218 uid=744 src=46.208.4.216 args=eyp/s/-uzrom9lv5-xxdc34m13czfivnj7t5f 1q60z2-ldp
  - Log entry 71962: process nc pid=24638 uid=369 src=167.98.94.90 args=5fqlc8ix99dt/u4bm2-l8yz6-08uj5u0/190u3a p5 cf9vm
  - Log entry 36029: process sshd pid=2264 uid=891 src=143.21.192.173 args=v89phxd7ogeb72hv2pyi0-ded3vx3s-d36ulnfi/egos272r
  - Log entry 80014: process wget pid=3879 uid=859 src=20.86.59.27 args=z9uo53284-ehl5uw/bdrenv9-6ktc3q22an o9huv9-a4g46
  - Log entry 72418: process ruby pid=17721 uid=514 src=210.41.157.74 args=g/j5hrlvo59fqzjbnn-zv5wvccprjsgjerbjz/iabq1f xa5
  - Log entry 25440: process nc pid=10141 uid=705 src=79.21.124.66 args=ckhy/ ucnaiwpd7k59vz-a3suaz74b9ubzul637b6ok0jzbp
  - Log entry 81812: process python3 pid=8962 uid=794 src=175.56.178.211 args=dws20bhr8w3k5mz5o7quy-7hjg-pb2pczmcrqsjca/z6jioc
  - Log entry 24693: process curl pid=28994 uid=582 src=9.219.3.9 args=l57mwsjy13-85spwmk  -wpqqstiq6b5lgtsdyyjdi/frw3 
  - Log entry 72905: process bash pid=16240 uid=345 src=122.10.51.107 args=qynuzzhta7g-8qn4x-ri7bxx0676bk5kk0uq8icv rg88-9-
  - Log entry 16242: process python3 pid=19190 uid=503 src=214.158.79.108 args=mdj zo5nvt-wh0p2nvdt-cawkcktjxlyaspyoebdpslfee3i
  - Log entry 67915: process sshd pid=4261 uid=138 src=193.118.229.55 args=r-t2w3qd1l6toiid/n6jq6z6 7eqgqsd9oibfkumm-f3fk5q
  - Log entry 84324: process socat pid=4720 uid=224 src=136.177.160.163 args=yv8jo4q4f9debtht1ae 7xr-uwvtfs7hs46inramnw0vs5me
  - Log entry 40552: process wget pid=2230 uid=12 src=153.60.135.197 args=-rqarv6iptw80 3 kv5fm5bemjyqbj1qj8s9ll1dxg9jnf57
  - Log entry 80077: process socat pid=24200 uid=794 src=173.232.182.11 args=r1w5yk3 4udsee8/n6ummu6dub1qs1f0 qgoik4fcigp7 l8
  - Log entry 49388: process nc pid=10474 uid=963 src=78.89.140.107 args=/hu0dg1u/pw/yrt/3c7qtl/4/6ue6ixq g6 zj0e3fujsvwz
  - Log entry 94699: process nc pid=1251 uid=69 src=215.95.209.78 args=3q22tg3v6r1y7lstxaxfmh7j7ws2426/-ystrrew9ie0wvca
  - Log entry 20088: process socat pid=13020 uid=43 src=147.133.248.149 args=2b0a sewcl7n06uue6sag/26m1b1jqzumv5097shraq5byqr
  - Log entry 50814: process sshd pid=19794 uid=480 src=215.4.246.113 args=p7sdzua lne51ahr720l8w/7wvvwgi0a60c fzidgu3fs0r7
  - Log entry 29836: process ruby pid=19872 uid=183 src=46.156.25.184 args=qzm0fntcs5u8s8lo3lvipy3q8psarw0p16t15lt2kz7hkigo
  - Log entry 44189: process sshd pid=22243 uid=586 src=129.19.250.248 args=jvpfjg0o/m8 znm719nvcc76wdgi73chje vgectxdboqf9/
  - Log entry 91614: process ruby pid=31882 uid=572 src=180.161.70.66 args=rxxwazn5rgmlx xp/7avxi8ml4u 1l8c1adz54/i20c081d8
  - Log entry 24715: process socat pid=12467 uid=428 src=70.112.221.191 args=1ntvc 049flm5f/48k/65a8a60q3fr257/etqx-otm7klw 9
  - Log entry 47340: process socat pid=31825 uid=465 src=25.90.226.1 args=2nm/a70ik9g ag 6-oeu3g7hmxkscfm14i715c-cnwubw6ly
  - Log entry 56870: process curl pid=3112 uid=258 src=162.154.205.155 args=d02-amgpv qooelonkzcx7qfezgb0efnd8cn6e1cbnsklozr
  - Log entry 70256: process python3 pid=22915 uid=732 src=213.238.238.118 args=pp5k42n686oafql4of64grhg2s1yzk8e1fm6 s5n0n8n7ybp
  - Log entry 13589: process socat pid=30658 uid=395 src=148.80.194.79 args=daac0c88--rwgvyyjsd8eikutvmyuy3/6wo2bmn/r0lpnz/n
  - Log entry 73829: process bash pid=22833 uid=653 src=186.223.60.79 args=h3p7xyd1z0ec96m25v4e2/9hidpc5uj2aid pk48airllaeh
  - Log entry 45977: process sshd pid=9561 uid=617 src=45.168.224.208 args=g1tz4q7-o366srailoelouqqitxalxjhs9agqnls0rswj 5l
  - Log entry 84425: process curl pid=30865 uid=254 src=157.164.105.199 args=vt905i9ppbpv/8q48wpyf2fgj2yjstuorjuwk7p5xkhf82wa
  - Log entry 49417: process curl pid=2599 uid=169 src=57.70.64.29 args=3s0bbowl8faicth5btfi5o2 5wodykd9r-d4r5bbjspifklb
  - Log entry 47791: process nc pid=9198 uid=430 src=36.28.29.95 args=dhfbx-58qnmsvheiimookoup-cnw3xe4jz48kx2-x9jjoq8l
  - Log entry 63710: process wget pid=7627 uid=60 src=160.228.30.174 args=s-zg8 cu782kw9/sll33zx64wb8sdfuwp5hptxiftk95vo-p
  - Log entry 29327: process bash pid=22248 uid=240 src=199.95.161.160 args=3vu91icfbeamt45-771du4pp0/w3bal0-oi16t4urepfw242
  - Log entry 84766: process ruby pid=23790 uid=244 src=42.14.183.187 args=szc170k8ezcuplv6u5pt7bys18/nz7ejhlku0rxwslagjpv2
  - Log entry 65672: process perl pid=6368 uid=474 src=182.222.80.24 args=1-30hbcognekjpt-gkzxa5oqwcj66/wlyc8dirrxvd mwmwv
  - Log entry 29997: process sshd pid=15782 uid=670 src=116.230.196.234 args= 89-cw1endmbotls6b881r5k0fen9w0-6s8vjl/53gw3p7kz
  - Log entry 26726: process bash pid=7500 uid=537 src=170.155.37.92 args=ncx oc9wan2txsg111ksgi9bv8c9usgjnkv3mnpuxu9g9nfq
  - Log entry 61620: process wget pid=13992 uid=903 src=140.30.207.100 args=9ge237y 1pbaqbg9yt6564gpdwhu5jsgb5h dz8tqyqxr7u/
  - Log entry 20232: process ruby pid=13081 uid=271 src=86.117.67.48 args=chi4vnxnb c/ifi94bvrojmvwwpkb2ry9kv/t f530mg8ytk
  - Log entry 55048: process nc pid=8682 uid=806 src=72.134.77.90 args=11t7v-4d5q-lyr1fyklqejt49rj-x30xa5-f6swow2xcdsw1
  - Log entry 90944: process socat pid=24656 uid=511 src=127.243.207.41 args=d2tmymt82kjhwc/8/nyydtwg8va6exm9/hs73rsdmsmywsxz

## Supplementary Technical Detail — Section 52

Automated correlation engine identified 32 related events in the 6-hour window.
Baseline traffic on port 9584: 0 connections per hour.
Observed traffic on port 4444: 133 connections during the incident window.
Statistical anomaly score: 0.963 (threshold 0.750).
Related CVE: CVE-2026-24501 — not yet patched on 3 internal hosts.
Affected subnet: 10.6.1.0/24 — 29 hosts in scope.
EDR telemetry: 0 alerts suppressed; 3 false positives removed.
  - Log entry 93043: process wget pid=30017 uid=430 src=182.158.80.175 args=ph/r8u2s n180zbg-zm6szb-c/yvqm9k9wx55gbic7-/8-5u
  - Log entry 26896: process ruby pid=25922 uid=983 src=148.107.14.167 args=4dryemvwyh1iq/upz7ur-d04y5nk-c6e0pkz-0cyk77etuzj
  - Log entry 95743: process ruby pid=15430 uid=348 src=155.217.155.34 args=qkvgl0w4b4-yvcd5-f426 2bmlqmt9t-4jbha0icatv-ndz2
  - Log entry 52373: process socat pid=9945 uid=221 src=73.185.87.243 args=tyohfj9k9rwjv4ymyk6d-f1hfpwgel81g8053u j47g74r0g
  - Log entry 79395: process wget pid=12925 uid=389 src=112.110.39.178 args= 5696kk4sgp/py goo1 se 0xwcxhxklzfms8ia/gcu-7m-o
  - Log entry 13589: process nc pid=27688 uid=590 src=101.82.100.172 args= 4-py5buxrelxu250tzcg5z73irrmz0v8eupcdmpc95b rq6
  - Log entry 19519: process wget pid=26906 uid=96 src=66.9.48.39 args=njvvbyg0tm0pjqm3g-/wt9s2ade8169stt tk21348k7q5pt
  - Log entry 56104: process sshd pid=28737 uid=961 src=58.104.250.31 args=j4uro7s0-2ew-x3i vx9h4/qml bts6m2u42h0f195211yem
  - Log entry 56110: process nc pid=21226 uid=718 src=189.36.7.160 args=onux5-oiehoj40nsy/-zos/ouktvd6zo- yq2x5q9jmlanzt
  - Log entry 61838: process sshd pid=4392 uid=643 src=181.226.128.136 args=jwt3wdier4y532045jp2/xo1c-h05262i8qwophyh2hivjmo
  - Log entry 85819: process bash pid=28167 uid=169 src=57.142.157.8 args=-jwt3cczi0jsg-sbo3h351xgsrmtwao7sm54pmaal4 b5ue1
  - Log entry 92813: process perl pid=10244 uid=543 src=130.210.74.129 args=7ppqg iiluhvlvzcrcdw5 n28b0gw646f46u0v037tx7-sbj
  - Log entry 46139: process bash pid=17066 uid=352 src=33.215.205.227 args=x pm6au6jrd-flrbs49j4p5um3mpcv90nchn wsa1jgpxvj5
  - Log entry 92700: process socat pid=24857 uid=568 src=69.125.136.111 args=51n6cd4i3w7sw4 kurp2qflgpp1b3dnor6il59b226bu7tbj
  - Log entry 48901: process wget pid=10697 uid=898 src=45.188.103.221 args=zn1z4eshpqa0t7f8a9qrkdzdoh r8feri7jys-/j6lhw7z q
  - Log entry 51782: process bash pid=8976 uid=848 src=59.216.75.248 args=85gzqhxkwhbmub-eo9ikx/9iqtowfvd37rca44k/a/jri0up
  - Log entry 78478: process python3 pid=29948 uid=452 src=156.114.104.87 args=8z79flb6hjp1oae13ytc4fqeo5bq1/39ln/1vu3jfe1r t8o
  - Log entry 94011: process python3 pid=9707 uid=739 src=87.49.185.161 args=cm2tc5f7oo/f0b17xza4oku/pf  da7xr-bkefmteobjzqet
  - Log entry 62236: process sshd pid=7251 uid=24 src=117.227.236.151 args=c0qdhvtw2io5assj1ehloyhe8pi5/xrsz n/bvvgzmoyn2j 
  - Log entry 33328: process ruby pid=15960 uid=556 src=49.78.164.97 args=3611xbax koixyel49m8wom0gly9tsa rj9ptjc47r1w2liq
  - Log entry 16700: process socat pid=6665 uid=0 src=64.250.27.182 args=xhml otog4b7l-bfgquxjnuhn2a/ d bj1b0jnh0e53nm0qk
  - Log entry 83139: process curl pid=20599 uid=625 src=188.18.173.173 args= 9yna18yf65hvuc1xzj4-rjm3u-ooxnkf1on 3z/6fj0ymkn
  - Log entry 38591: process sshd pid=16070 uid=618 src=67.60.244.172 args=nnxo4wy3rw6qljg1504a0-m8giusn6-mbr-x sl5/uy0oi2j
  - Log entry 41047: process sshd pid=14315 uid=405 src=88.217.107.138 args=74n/v 1yh28qfnb0hnm8/vz/063mdefr8mzht ypvb5ofpr/
  - Log entry 59411: process ruby pid=11612 uid=237 src=58.246.57.143 args=e8wlidyjwwua97mkexd8rc706v866-5j-eiv46al/pnkebk 
  - Log entry 23277: process python3 pid=5725 uid=647 src=159.137.199.248 args=a9n6zvczbkt elvha-o3vq/t2me3m9m/vp-vee2i2ucjp5k4
  - Log entry 94698: process python3 pid=21609 uid=932 src=141.241.126.136 args=d0p95imety3pnr40ngrhmrq2tyir9gnjua/ exng3254aq2i
  - Log entry 45638: process nc pid=2747 uid=705 src=89.52.85.96 args=t5pw/baei9lqkfdqv2ww1n-m1j32hiaom96tqlos-a 969yl
  - Log entry 57762: process python3 pid=27012 uid=230 src=158.68.189.129 args=falyxrdhoq2 inp/8vlg biyp4-qrqg64dolwk/it4oclt5p
  - Log entry 44155: process python3 pid=9910 uid=691 src=206.94.126.130 args=tmkfk9btxzwyfjx4v4-r0elhxfybsrib-tp3n9e n el1nyt
  - Log entry 98640: process ruby pid=2091 uid=672 src=89.226.60.233 args=r0y-fjle4racgo0uh6o4itu2hhjcto7 i5sx7v90u4uc5-ru
  - Log entry 24745: process nc pid=6447 uid=466 src=142.151.21.193 args=0pmt y7/agg1n6hvgkxu8l ew5f1-5edqnjokigd 0i4khg0
  - Log entry 40564: process python3 pid=9583 uid=719 src=183.31.119.209 args=vozuohoot/g1onc9v0qk7esblnqraqk9u9cmoyu3axwp4dwc
  - Log entry 36485: process perl pid=6423 uid=477 src=2.56.229.108 args=wtobnnhb3c0m/6i4pa2tuwxwspld6j6ru84w60bg8te5i0l1
  - Log entry 60675: process python3 pid=17075 uid=406 src=13.123.46.16 args=2lza0lxyz8jfpwxtx/8ua3lrjgigpd54zypcvwtt9jx-5smn
  - Log entry 91952: process curl pid=18846 uid=863 src=50.93.75.128 args=z0t6ixgiqkq9601-cx/1foodgra0haw pbzd0u1etrb53pgm
  - Log entry 82012: process wget pid=1841 uid=582 src=23.172.196.129 args=44z8xertma2kqbn1lrvtj2f8apbcwmcn9bn9qo7g6mb6-hp5
  - Log entry 16671: process curl pid=16419 uid=522 src=222.172.185.164 args=uzfgwuyyj/5duc8/ro/wlujc-0yrdb369pztvrfzx68s27hw
  - Log entry 18643: process sshd pid=7277 uid=990 src=145.250.225.76 args=1x43ujdbqv67amc22lpykbfd7hajv5lzh7k1i01h6p-pts45
  - Log entry 58257: process nc pid=31648 uid=48 src=72.11.189.249 args=ga2wb079 pd59mj3 -s3 du3vfz1sydc73wh9u0yswcmn-ep
  - Log entry 96564: process ruby pid=30246 uid=473 src=23.42.50.127 args=9p-zn3hitj mg3uqvq/h8oqyaszq9axq76042cki/3s y2cq
  - Log entry 57596: process socat pid=5619 uid=96 src=169.20.77.97 args=kzzljju1/dvpq4p5rj3pdeil-uvgw  zoaf-d8ddc12wadwt
  - Log entry 66777: process socat pid=25475 uid=82 src=90.35.135.40 args=d9 283bnr6j/qmvm4d8mce 5u5w2jql unroktq5e wzy8gs
  - Log entry 97259: process curl pid=9766 uid=158 src=92.127.170.24 args=r2c9x7ndtuq7w-dpds6s/ai6idjeew367n-g17n/u0hqkbof
  - Log entry 75919: process ruby pid=19830 uid=138 src=15.115.85.218 args=taid vlosf7dttx5vnaq8serjbf21g927bi3flv q5l62icz
  - Log entry 17438: process sshd pid=13715 uid=883 src=66.141.1.104 args=my6ow015kxtcysatdq1whyawvf 1t-7qe2mwzqz3 9jcn2dt
  - Log entry 49447: process sshd pid=28643 uid=462 src=212.118.186.139 args=5tkjiudpug1-hzwzh5mied4vm6z1pv9sg82g vf4e6v7ung6
  - Log entry 34430: process nc pid=16732 uid=472 src=92.4.227.151 args=nq-rtddg70hxj56fs839ec96dbubua72t1///v36tnqoffc6
  - Log entry 26458: process nc pid=17923 uid=600 src=12.214.158.206 args=fkca/uby/ dxf1tfqtqpdrax755 uxlqeyx3dc394zf4pmda
  - Log entry 58258: process bash pid=6431 uid=774 src=63.250.97.131 args=goi 5a436qqt8ad1z0afkx55nyj/ssqp7a23-v-6qjjw8w-u
  - Log entry 43163: process sshd pid=15383 uid=812 src=197.191.185.167 args=1p7apsdnkm2e44fcur26g4-s1w70o-uupa4x/ijs7s hd6vm
  - Log entry 28649: process sshd pid=12645 uid=488 src=37.44.249.128 args=wacm3/6uvl3g3y2ksvwl2z2g8l6-rw6toyqqs7kzki1x/2h0
  - Log entry 10864: process sshd pid=10170 uid=811 src=136.97.28.94 args=po24o0xusigf85o5x2paplzjqra5y99f-nwpu538i8gj-zys
  - Log entry 54362: process sshd pid=1897 uid=634 src=19.145.37.62 args=znt/oytzctb1l-ers9gz3373asr0ohh0vxd7l7t66j3ww8r/
  - Log entry 76867: process curl pid=25919 uid=655 src=207.134.93.15 args=kg3jg/duv3kvzsi7z2w6xi8top56yepos0dilmtvzz7p7cnt
  - Log entry 35291: process python3 pid=13855 uid=921 src=81.172.67.118 args=dbwfz1-ak/jjyapkz-j98ckb2x1ndj1yhb1dvho49qabei4 
  - Log entry 51916: process perl pid=17572 uid=555 src=9.7.94.231 args=evrhplcs6r/mv9dq2per6urh1n/hqskcqevfn1v7dqk pvx8
  - Log entry 69715: process curl pid=15622 uid=36 src=128.146.136.164 args=5jwsuireelsg8r01690hf m8rskh6bs78k7rba1lbjl 8ik 
  - Log entry 95290: process nc pid=26563 uid=126 src=220.152.254.6 args=iyvgh21pdnpuq/utn0fiqcild4ku/8yl7iqcd61hixnvlekb
  - Log entry 28583: process sshd pid=16581 uid=842 src=97.20.120.83 args=201ywcwqkxgwwlvngbb86hq9c5j17 d2z7j-bspr40n0eqy6

## Supplementary Technical Detail — Section 53

Automated correlation engine identified 33 related events in the 6-hour window.
Baseline traffic on port 51045: 4 connections per hour.
Observed traffic on port 4444: 118 connections during the incident window.
Statistical anomaly score: 0.942 (threshold 0.750).
Related CVE: CVE-2026-38993 — not yet patched on 3 internal hosts.
Affected subnet: 10.0.5.0/24 — 19 hosts in scope.
EDR telemetry: 3 alerts suppressed; 1 false positives removed.
  - Log entry 10928: process sshd pid=2688 uid=155 src=156.5.64.228 args=f-0z7nh3lqs7ze/h2u1p0u3ifx i5ch6zq0r3gx8miwhb21d
  - Log entry 62151: process perl pid=25775 uid=960 src=120.121.242.192 args=1hb-87/0f3t27ch4-nh0xoedt47whjan 6f9y50/kvpgvjf8
  - Log entry 44986: process perl pid=31126 uid=778 src=133.135.64.2 args=u64jzd5zw1dr3hra3a8xdkjugreb igjmkidzggv2pj/a4cl
  - Log entry 80643: process python3 pid=26683 uid=438 src=139.76.58.230 args=uytfvvumo8t7w7jx3v nvbg3jcb1nnk2w0am3j-ic4ln2-5g
  - Log entry 87287: process python3 pid=6353 uid=845 src=91.69.156.23 args=08glplnumezkebs7qmoh xbm7ilp-av-4x7xs5vcprmaf1ia
  - Log entry 67096: process bash pid=11387 uid=487 src=59.75.185.184 args=z3tr73qrxva2xwtsoq/km0s9/lk8cg0qljprn2rqiqxmr/-l
  - Log entry 85665: process ruby pid=8920 uid=977 src=44.81.61.37 args=g31yc2qyat/ap-uyt8l4fwobcp82op8m4omwmvxn76xjpftf
  - Log entry 63221: process wget pid=15631 uid=61 src=90.235.176.159 args=zk4p4dm5qb2l5cu26t8c4qd s/rs97tjr1/2rgktpncz8 2h
  - Log entry 31240: process sshd pid=14295 uid=477 src=217.185.192.182 args=i1dbu ghd8-3l6inv575xl09945dk3au1n0fo8haumi1m3h-
  - Log entry 60769: process wget pid=31262 uid=379 src=101.69.81.159 args=wyugpy1taq4fbqy 6xcithf u1s7s0v7g8tdscq6uuxutu8k
  - Log entry 28959: process perl pid=27337 uid=983 src=51.139.227.180 args=jbin5lhl a/omtiyz-3qril55p9oclqj7wm/32hxfj-um/1e
  - Log entry 25693: process socat pid=24109 uid=974 src=201.27.79.71 args=61/3it41mnchqkv2hzghznfqktajrcjw/xi24cujqi3upqgx
  - Log entry 19810: process ruby pid=30142 uid=890 src=26.81.162.129 args=1nbidj9ajm/dm2yxnqoj9/2y5x3omxoa9at/hgjy74ggi8o7
  - Log entry 13901: process perl pid=29129 uid=918 src=84.169.204.88 args=numi-bifz 6cgpmsupscz40w3tqznr2j6cc1bw1/q6am3q-1
  - Log entry 39714: process sshd pid=26118 uid=790 src=112.115.250.4 args=15p-eo6z5jxpwr7nqgqp-3i-ahuozeqrzq-gfmjiv0shf47j
  - Log entry 80477: process sshd pid=25030 uid=200 src=173.25.41.185 args=4e4n8yq6-c5/0xcxt5fi8vl88ivuc8gvnpo4-uqejj7cvh 4
  - Log entry 51306: process wget pid=10526 uid=497 src=166.37.37.55 args=21dy1tou-aldgf21bxw-08j4mjwwv6/h12tp5b322yikyfa 
  - Log entry 44708: process python3 pid=4504 uid=431 src=32.63.250.187 args=4u-/tdg5hfvqxfe1m3n8vks1qf/et 68joz15kg-k355atm0
  - Log entry 93438: process curl pid=26654 uid=755 src=153.18.115.225 args=e280qfhgyi5vc9t7udcrloqbcqmbmvway8ulxlwkj-i8-njx
  - Log entry 47147: process sshd pid=16755 uid=569 src=14.154.193.203 args=0wjr-ujr9wcdlrd1gmsw/i/46fsqni2em8r32smwonbhf6zp
  - Log entry 62343: process ruby pid=30463 uid=363 src=4.179.93.43 args=-7fxgkif6wav451 rtg5sfm76c1y-dn1-7a9wk4wqx3na/ni
  - Log entry 71891: process curl pid=6621 uid=993 src=41.210.212.229 args=2sf1qbfkht530-l1sptnmarc2-wfzld1bt -tbz4it3d2tiq
  - Log entry 42320: process bash pid=4103 uid=351 src=66.20.202.124 args=ouycadg/5/ia-mih587jjs/dkrcfol/2p0i03h 90   8tya
  - Log entry 21000: process curl pid=13200 uid=900 src=100.229.61.192 args=bk886x33 trttonih5e/4lqcgiqw09/z6fglx8a2udu-ereg
  - Log entry 64601: process curl pid=6754 uid=918 src=72.12.192.149 args=px/hwdt58fd 9/fe-66ke-zsz605oi7-9o2mlzsxvwu7ov4x
  - Log entry 35958: process wget pid=1735 uid=517 src=169.222.91.159 args=zcxz2-/ ffrcd3x-dfo3x4k8lx3-fbnfwrgl//cak/o42us5
  - Log entry 33316: process python3 pid=5608 uid=417 src=107.8.103.167 args=7sc3bmehqdrn366bnyuia53nca/znbjwf/j-an926wh2yhd-
  - Log entry 49970: process curl pid=16914 uid=779 src=133.190.61.183 args=wvc/rhev gr4sgy06qoxoc4-zn vcb 908/h/w062 3l qfj
  - Log entry 78782: process python3 pid=2326 uid=595 src=110.46.219.85 args=wnd7gtb15 dl7v-h1crz8iez6-jx3gvphdfh8hm0h1zei8jn
  - Log entry 68457: process ruby pid=17564 uid=747 src=86.205.50.22 args=wn1bbp9np/nnnepwbs wj 0ba0f6lyiqii-q-bl/4u6hy17n
  - Log entry 66527: process python3 pid=13261 uid=30 src=204.2.198.115 args=c57u-8mq/8509v98r90z1c28s-dizy- 0ppz ly6th di31p
  - Log entry 39352: process wget pid=21961 uid=798 src=133.94.26.45 args=cbphfq/j556-3g04toq6 001811etapdosv9wp62ox gchaz
  - Log entry 69053: process wget pid=13443 uid=898 src=112.139.130.204 args=nr2r2n liywrdva/bgtwo-nfmpt4c04wzjrx3jhvdy-li1-1
  - Log entry 70055: process ruby pid=22019 uid=260 src=40.9.26.92 args=g55f8tpncrju8wq8t3-j8jge4w e-/oifb1hjsc976jr/-ke
  - Log entry 66033: process curl pid=18647 uid=583 src=189.43.25.88 args=8klzbpyqwpt-1e1ps7vnrx43epzcj0utpjk26v7z54bd039l
  - Log entry 63790: process wget pid=27892 uid=987 src=53.112.167.54 args=x2xc5whf-27/bag80b523cykc wf49qb8e6qvgylzi1ubitn
  - Log entry 70030: process python3 pid=12169 uid=555 src=21.121.4.38 args=m97ughskyfejz-qhro4upj00jzzamjb8u6dkpxxuyv7qsp15
  - Log entry 52115: process curl pid=14138 uid=121 src=160.115.199.218 args=o4bl/hc25a7r7rs 96mrwqhgi7ssrz8trt546u/p46i82-vo
  - Log entry 14195: process sshd pid=9984 uid=979 src=216.34.222.156 args=mv--cm5009puzh1b mbqiiya0m8lnu-kzmhsz0f8b02f6jpx
  - Log entry 51560: process wget pid=17593 uid=338 src=106.82.61.225 args=hsnmgnuas7qhk6b2wgl23 ufsfwmyb-952qen/9jco4nyo50
  - Log entry 94591: process python3 pid=27915 uid=661 src=158.96.14.228 args=4lue5ggyg0mpom2kcxz/nrhrx/65uzvb6p88e5wbnz3aioc-
  - Log entry 94750: process ruby pid=17190 uid=896 src=181.154.19.146 args=ft7o8z7d5pzwcml7yxv/ecaowymm7uk5h7wmb1wtmgerx58p
  - Log entry 69909: process ruby pid=31071 uid=876 src=51.223.45.115 args=16eg9a85aa/ct679xbki2rzbz/019qulhkb/1vfb6dq9viqv
  - Log entry 97063: process bash pid=11995 uid=182 src=187.234.63.215 args=hd36zl90joz0ee14otck s3gqrdholz/c1tlhifoq-6owvhz
  - Log entry 90714: process perl pid=8817 uid=66 src=78.73.187.107 args=o-3cyg0/5toccb99stym lke986qf242i4787nn3cm756lbu
  - Log entry 97583: process nc pid=4682 uid=426 src=185.98.168.125 args=mlxoywa -a0om/utve8fqcei8x7vrada lmr5l59-q8g8jls
  - Log entry 18802: process perl pid=22077 uid=318 src=132.29.220.226 args=2brv2qy2m2itwire/-u317ak98enls5yx4ss-5q31g0pq9w0
  - Log entry 95120: process perl pid=3470 uid=110 src=76.178.170.47 args=j7fmwgc2jwxsnk8vym31hqj0qdj698om6mnqzelycptp0v/5
  - Log entry 18803: process sshd pid=7021 uid=210 src=223.41.1.3 args=tre1unspx/og5vbfss7cjwhh s/2cy3modbpcrqayhmb9ev6
  - Log entry 86420: process perl pid=21655 uid=962 src=106.60.232.209 args=uesuuwai9o cg/-p8u-m3uq4ahgdh4sgmzygxwik6x/zwfkn
  - Log entry 19598: process curl pid=10715 uid=649 src=212.200.212.172 args=024kkowtlokn4w0piasyn3pohiwb//1ll-dsfdvx2fq0o/14
  - Log entry 78520: process wget pid=6386 uid=115 src=57.16.236.12 args=h 9aio830l3pw4tg138lhim5cgc h-vrw8nd4wpj0ceuqbey
  - Log entry 22931: process socat pid=20492 uid=350 src=19.181.32.94 args=2pvbrb d44li r2ruhr0nb xkqdal85adiset7km/l3frjzw
  - Log entry 40828: process curl pid=17469 uid=690 src=3.124.106.174 args=imutyl1/s3/hbecd/933v u9ynn76nw00twbsoob4u24w-i2
  - Log entry 34027: process perl pid=13743 uid=819 src=80.179.181.107 args=n7x25j1sbb4ejuh2hamtvy4nx1knqq171jsobizfxa5ttpne
  - Log entry 41267: process nc pid=16486 uid=869 src=132.160.3.76 args=aupz/-k838pvk0z4fatpkt1bq-vly62ncs3n020zh-fvdzlc
  - Log entry 40124: process python3 pid=4903 uid=597 src=190.48.236.71 args=nm9iji8y18w2p7oaw6-wxo8x7attkf0frr1vtsiwtgl2oto-
  - Log entry 24407: process wget pid=2784 uid=956 src=56.241.222.117 args=g77bynk6pizoch6j1fsenc656reai1vtcx3fn00 25mdd ir
  - Log entry 89091: process ruby pid=31673 uid=574 src=51.151.88.239 args=3qmz/d2uviswi052p0v15x-q4s9ic93pnywl4rwdr64s -0k
  - Log entry 30331: process perl pid=4993 uid=571 src=21.184.99.72 args=6rs4e5rjpr9mga89p24hb7z9/syv78m6lkc0veef-doqy6wk

## Supplementary Technical Detail — Section 54

Automated correlation engine identified 16 related events in the 6-hour window.
Baseline traffic on port 50798: 5 connections per hour.
Observed traffic on port 4444: 179 connections during the incident window.
Statistical anomaly score: 0.864 (threshold 0.750).
Related CVE: CVE-2026-16975 — not yet patched on 20 internal hosts.
Affected subnet: 10.10.1.0/24 — 11 hosts in scope.
EDR telemetry: 3 alerts suppressed; 0 false positives removed.
  - Log entry 73389: process curl pid=16096 uid=158 src=178.154.134.114 args=m71b5ur1-8vm23hhdifdg3946 2ugpql6bq3s3ssbbfs8e33
  - Log entry 40478: process ruby pid=9238 uid=625 src=14.232.137.191 args=m-v8f0j6euf99wknj043okmltj4mojb2jwz-3-u kmtmrj0i
  - Log entry 85343: process sshd pid=14081 uid=974 src=98.234.72.220 args=2fgtbfh87icn6tg0gh364fkoed/wozi1vspjfg5l97bqv5jh
  - Log entry 85807: process ruby pid=23324 uid=449 src=107.201.43.97 args=c9temmzl47y 3 a79eqcox749on5xm3-r/lzi93s1r0m1rkf
  - Log entry 57941: process perl pid=21903 uid=622 src=155.173.84.234 args=-7hky4css6f8265edyxl2uznb7uf6f8g15gu8 /qto/ya/gz
  - Log entry 28782: process perl pid=1442 uid=696 src=42.76.52.29 args=wtbd5e9t38e727pc7hq 6i1pugknxwq6c 3csb/b2wd0wmt-
  - Log entry 49529: process bash pid=25688 uid=567 src=18.8.88.181 args=lsn5jy5yp8unj//7yq56oo8difgbqm8gn8anzshxt74o6wo-
  - Log entry 82195: process curl pid=25553 uid=323 src=65.214.110.91 args=r-fft5f686a3b5grr8uqa y5fhw34m/p5sic03f0e/bwmi9m
  - Log entry 46089: process wget pid=21537 uid=480 src=63.247.212.157 args=5j2brjf-ko-fmm05na/6u0x9eo2 1y3m/1rw53a55xsw  ne
  - Log entry 37410: process ruby pid=11987 uid=59 src=113.3.36.188 args=0wcqm4ajj5lenblyceb99ofunxkhx4m-gqbci0m498f2gpsq
  - Log entry 11551: process python3 pid=25346 uid=434 src=71.171.142.125 args=txdv-p3xw2teg5ygvykiazg9sk9l 4s7b-acqf3o2bcxv4n/
  - Log entry 50654: process perl pid=1171 uid=680 src=177.163.185.185 args=vt45gb4ml89x5eiey6dnp5umzq4lqphp4r9ck1e2-87agdsk
  - Log entry 88795: process perl pid=30287 uid=935 src=195.200.144.252 args=3f5ory1slmd9i0vdajpoby02f6kyzp32o8qcqhau732 stpf
  - Log entry 38675: process nc pid=25829 uid=943 src=44.169.151.24 args=3i7w9v/m/wj3pbkz2m2abktvlvvn7ao8nxjatz ppwqtko-x
  - Log entry 29014: process ruby pid=19920 uid=735 src=17.186.64.92 args=kx1d2bcl na8he8cecmslt qdo78-8t3szu2i6/e2u8j7vme
  - Log entry 46784: process wget pid=13977 uid=276 src=88.0.52.209 args=khd2ptqi9yd09w h/5eujyeudq0urpjje9w6dtrdl1lg3w 0
  - Log entry 60411: process wget pid=10821 uid=641 src=130.199.208.224 args=ogpuyj4i0kamo08x6qa3llu93gpanhjz73ivy3tp4ow1cmbz
  - Log entry 11180: process sshd pid=14111 uid=570 src=217.229.234.54 args=g/0syszy9o9ackj41miola8n45ma574ds/qmzjaltr5uqmno
  - Log entry 31983: process wget pid=8526 uid=295 src=116.51.254.201 args=v617/ifu9o1flisrdll0pclobbljylk7lm8j0g2-lm9o0553
  - Log entry 17877: process sshd pid=6195 uid=110 src=168.142.16.66 args=6hw t87hndm0-828h  0yu/ tu6cx6citejuksrev7g8q0vu
  - Log entry 48464: process socat pid=7288 uid=231 src=12.66.243.151 args=40-dlsrqypw67ybxxdv69lbs/fxlz0  cnwh1anh/x0ahipi
  - Log entry 59249: process socat pid=14240 uid=913 src=100.169.245.186 args=9/dl62ejelh9yq7s4w7dgem1gu5 im4qwuplsfpcfg-2sffq
  - Log entry 20942: process curl pid=24342 uid=877 src=82.13.86.206 args=3q qvhmayuf6zuecg8oqrm2h-/chxgsow4ckd1-vx9d41hgl
  - Log entry 46013: process nc pid=16660 uid=691 src=83.181.71.135 args=2jwyqpct9t/dr6icrve6wuyc-e5wi 18a1smj5-3jqn-864x
  - Log entry 25332: process sshd pid=28800 uid=50 src=160.73.225.85 args=b-jyvsrwj-t8zy8pv6tu3dh83oyw26mbe102bvpoynk-5 v5
  - Log entry 29524: process bash pid=1918 uid=581 src=150.224.73.44 args=7uaxlbhcm79-xmygbmoailfiu886x7mf5 xr-7qe6b5jeu20
  - Log entry 50467: process sshd pid=26307 uid=191 src=22.55.35.243 args=7-u5t3hf91bz f3xu7lj woex8vr/gmanl/l0cdrfj3i6 tt
  - Log entry 14722: process python3 pid=3005 uid=310 src=205.222.106.138 args=cxkyy-vcv p18y13cgnyyyblyljtm/3domb05ni9nzhhpmam
  - Log entry 25993: process nc pid=22309 uid=224 src=175.6.180.78 args=trnu-3thrcul75w53qvky5v1iev-w-r76d7l11b66l37 3lt
  - Log entry 18392: process wget pid=1499 uid=937 src=64.105.48.41 args=uep1h-yn-s8j5fith1x-t71wvi 2gqut2/56bdjqhe54hmsy
  - Log entry 72709: process wget pid=28482 uid=121 src=184.178.53.155 args=cq 2dpcs6khu19pix1sf0ho9ce-yf8xs-fu0qqee3 hi546k
  - Log entry 18166: process wget pid=30445 uid=193 src=78.140.139.220 args=m9/ykay1wwf3zyn3u87-01x2ujd2z9 slb4fyijt-ynnxyju
  - Log entry 38166: process perl pid=22325 uid=293 src=180.84.66.46 args=8vkuyzgmr14ywba-qcby y61b58xhs20c7l8fncsvxhz9vq/
  - Log entry 61743: process sshd pid=26874 uid=924 src=74.232.147.164 args=2lu/hhxcu6u55oqwf6tt7z1xwr-i0h5hs9npg-ar1t/-b5ou
  - Log entry 27846: process socat pid=26675 uid=721 src=26.178.196.58 args=uqzo133by4xj6ys9hlg9v7r85vqz9w5hlshuq36f02tdatsw
  - Log entry 80642: process socat pid=2324 uid=308 src=100.111.95.224 args=jkdl78gut9q3/137h5y c1ta838zrczfi8avfhl-d73zjrpi
  - Log entry 19473: process nc pid=4003 uid=466 src=182.59.141.52 args=46sl9fk6hxmml/s4ygj7pfstmt/mdqf5cwcxh8c7y d6nx41
  - Log entry 59676: process curl pid=24541 uid=167 src=60.14.109.157 args=zyo1htybtsbbs43i5yl3kobp y2z-nzye1w0s6w4qr-zg-13
  - Log entry 25952: process ruby pid=21135 uid=721 src=104.124.145.222 args=1xzesaw3ap3i1/7b-e/acjyx0vu3q9gt 6826b eszl9v2c1
  - Log entry 91792: process python3 pid=21488 uid=318 src=182.157.23.137 args=07sogxmefrk6h75f-ps kw5sfli88yh8fjnegtrf l0ll/5x
  - Log entry 94367: process sshd pid=7792 uid=60 src=56.8.44.30 args=ba b6q2t ubi6x57ehqvcmrw8ot7s6/19xppflcu-iudlfxq
  - Log entry 38464: process nc pid=7933 uid=120 src=189.122.169.21 args=/i ze8d8sx dn5cpv- w05ec9pb3ujloo- 8pwlipgcmjsmj
  - Log entry 46466: process ruby pid=19998 uid=783 src=166.49.121.63 args=t69aj1ivznp6izvgbacw5r/op/dz a4e 8ap1g1im55wk9n 
  - Log entry 13305: process bash pid=17958 uid=868 src=71.178.184.197 args=aipjpv5it8pyw-78/d0 k/fptt r6ppeujp5jf 5fhw6krri
  - Log entry 80631: process python3 pid=27502 uid=794 src=148.10.17.106 args=cstf hfx8odw3buxhgvrtfihrpqre25t7vi0re6d3qtk6-g1
  - Log entry 83302: process nc pid=17858 uid=713 src=222.183.55.56 args=5ndttiyrljnkd6sdj9-o3m l8wyw ylyye3hjshbik8y7ksp
  - Log entry 50509: process wget pid=28187 uid=810 src=72.195.91.139 args=chgtlrnsn4a0rj1wr rtzvrqoga-5bfrimv1iqurxd27cb43
  - Log entry 14836: process perl pid=10328 uid=584 src=2.67.98.217 args=ysi/t/4sf/s3a2e kf-4587b456z6e2ae2xua1wrrunmgdge
  - Log entry 30376: process wget pid=13567 uid=482 src=82.65.105.181 args=qtrdmo8ocbcv4205dj6 r25vipskt4-ixhj08j/08y/jzilf
  - Log entry 19679: process sshd pid=25736 uid=736 src=52.255.124.121 args=jpvtc/x/p7og8wno6jsiddfylagnrq ui5r16xgfiy1q/n w
  - Log entry 95451: process nc pid=17444 uid=562 src=204.181.125.46 args=z1i20nh p5gvu fjvv112j22a7 rw14zxwgzx497i4srxuqq
  - Log entry 40370: process ruby pid=25688 uid=228 src=120.62.103.59 args=8buch2gwv9hcup6/rywfglukpmykwv657ez047-wo2nlwwf 
  - Log entry 18983: process ruby pid=3704 uid=870 src=148.232.8.209 args=bkl/bqgf1447l7g97zkn8ukrmwpd-pxpryd1tmxpwn6inj6q
  - Log entry 91197: process socat pid=17143 uid=950 src=134.236.217.191 args=i8nmjxhwqeq/vo2sor7-a-nxnbj4/us/v/wr8n7e1n9iu7at
  - Log entry 19300: process python3 pid=5775 uid=577 src=4.239.122.26 args=ipocyvjj-2ye5996y9b koaa8enmmr-1/ppy6m0o5sy-tukc
  - Log entry 91057: process sshd pid=19286 uid=507 src=119.167.21.24 args=q/kky36dfrzudb r0oxswqcck3fgx7ngqgac70rh-t99c9g9
  - Log entry 88878: process python3 pid=29182 uid=763 src=118.96.155.191 args=5 0fcuv425dq zq2we8/em/klyt isw2/nmxisd21rxu554c
  - Log entry 92417: process curl pid=28407 uid=927 src=209.134.218.211 args=d pu7lzf0gi6gd0c32aj8mol6z1 bj9enoyc6b7nl7kc6rt9
  - Log entry 28305: process nc pid=14285 uid=261 src=88.219.180.24 args=ib064gfuhf20p 6-4mec7-blokd4b3dk4cxl5kqifi1-xw05
  - Log entry 44509: process bash pid=12621 uid=420 src=39.0.78.19 args=zg5luqfgcauh/6skzt62t pb9eo6v9bxn41yvrx /8mo oij

## Supplementary Technical Detail — Section 55

Automated correlation engine identified 40 related events in the 6-hour window.
Baseline traffic on port 40752: 0 connections per hour.
Observed traffic on port 4444: 101 connections during the incident window.
Statistical anomaly score: 0.988 (threshold 0.750).
Related CVE: CVE-2026-30017 — not yet patched on 13 internal hosts.
Affected subnet: 10.0.5.0/24 — 15 hosts in scope.
EDR telemetry: 2 alerts suppressed; 1 false positives removed.
  - Log entry 71787: process python3 pid=4887 uid=368 src=117.165.214.97 args=s3pqmas4cu5dxxxlpndmv6qnzghh2w89easg0palzjsokiua
  - Log entry 58322: process bash pid=7017 uid=935 src=212.156.72.229 args=kkryzr6iw3hdo7awi7dj5sbzaqg0phno h92yu6l-ec lcu3
  - Log entry 32784: process python3 pid=13407 uid=946 src=219.232.9.246 args=fwlg55gin4g5s/be/1isy75e2bhpm2ypp1swoo7jw1a-hmm/
  - Log entry 11160: process nc pid=2871 uid=853 src=187.241.163.61 args=hi6nlp0lkjsxq3u6e5qeu 5cu-7vjatrtkngjlc0- 0 v8/ 
  - Log entry 55756: process nc pid=13182 uid=183 src=206.107.105.99 args=ssr844ublkdx 745 17c-px1ecjufifh6bwyi3s-fjy16tne
  - Log entry 23697: process socat pid=5507 uid=830 src=14.96.193.173 args=5 gpkg-3hi2/6ghk-5ilo99lknvwlujoyic9jm08q/77vks3
  - Log entry 49779: process curl pid=4575 uid=663 src=137.53.90.24 args=uc30deo8s24j4/mtj4dr-2unix1um1af4/m6cu1uwc/rs0f2
  - Log entry 54429: process curl pid=6529 uid=362 src=71.232.101.115 args=8urstn9unqig-byvskjzszz3 8dvi9jvrbdzrjdx//z7501l
  - Log entry 34498: process socat pid=29025 uid=944 src=125.62.99.126 args=34rn6h2v4y6m8btd96qirql2rxpwxhro9c-weg0pd4patich
  - Log entry 37645: process sshd pid=14857 uid=925 src=50.26.147.79 args=yvzgbx4-wjskt0/v5czw 3aya0bz-jjyp989uuikwtyr8t18
  - Log entry 57818: process nc pid=16742 uid=455 src=199.224.203.230 args=ud3nwf5cv2km5bf/1wsurps-fl7oh4ge x36-1qvjp5gh7co
  - Log entry 18830: process nc pid=5511 uid=725 src=141.128.160.2 args=nep6fw663h7nodw52im1midy01ls7z8tv a2uneoqf u9k37
  - Log entry 79711: process perl pid=23850 uid=998 src=142.142.138.200 args=g49ww1mer/6uidcw8bz915hn920w w8djwm5bmaak99i3r1 
  - Log entry 52993: process python3 pid=12011 uid=273 src=4.120.63.34 args=szr6k-nqkbcehr3bvmoft6ey3tzy4m vkicyvqv42egwek0/
  - Log entry 18248: process curl pid=16491 uid=799 src=24.28.7.165 args=kud44pr93/m83mmvey-ej9/behldyuzfk0crte3orzbkrpr4
  - Log entry 18619: process socat pid=24714 uid=684 src=37.106.255.160 args=ci26oe96td2-9t7-hahyveqg hlw/prd329rqop5htk4k7b4
  - Log entry 79179: process curl pid=26125 uid=240 src=125.137.86.180 args=0phxfo7i7tto7/h735a7ex6arsq2-3vi-xjhg7sqvqt4gjna
  - Log entry 11829: process ruby pid=30885 uid=743 src=133.108.211.219 args=cdbjxuc52od12dgmudpn16ujf5u-5/b063nw9kisjntkg/d 
  - Log entry 25791: process nc pid=6785 uid=423 src=215.12.39.178 args=bz078xhki7-uxt3atez162 leb7q6pb4im1484nl7yce1p27
  - Log entry 61206: process curl pid=10728 uid=47 src=104.2.179.120 args=iu0982za43gbcj o4v77k/yucq5yzi06b5 sg wqt2qsedxx
  - Log entry 64211: process curl pid=1680 uid=799 src=109.218.74.165 args=o1n443bmlbjhxnxh/w7q/8-5 d iy6vl7jc88hpzm93h64yt
  - Log entry 20993: process bash pid=8370 uid=546 src=54.233.214.109 args=itako3aqnivrmmvso3ho13vv3pfn366/uwt0zcauam wxev4
  - Log entry 34157: process perl pid=17099 uid=18 src=33.163.245.17 args=4p5oiqvvpzoentnxg-7eykjt9kxogirco99b2wp7viuo2uis
  - Log entry 55843: process sshd pid=21517 uid=898 src=97.170.190.122 args=ncloa89ekasepjfndhdzfnfy45mk6cy753gl5/1e5ry4elit
  - Log entry 95940: process sshd pid=13719 uid=491 src=201.162.5.184 args=3ugv0ctzi/u/mw9tf-9bhvyo9yk-mz8/g717c-1zu7hd53oc
  - Log entry 99808: process wget pid=24815 uid=745 src=133.193.230.144 args=2r2p-6h0gi3 dj1c2ocw02ws2gfpyuw/23bwu5/9rhz vmqb
  - Log entry 75723: process nc pid=23447 uid=622 src=210.6.144.46 args=gls ps/6i2vjj93h48hs fr18iuieo52-g61r69hh/f9m92v
  - Log entry 32131: process sshd pid=10604 uid=91 src=111.230.102.126 args=5p8f5zn8c61b-/qu-r/png37avrl0vzd8wrsbj z-qtxsqn7
  - Log entry 32374: process curl pid=23955 uid=98 src=140.66.126.67 args= skf3y-5t-w9w ikmm49ca2w4hi8n-p3y8ujkd-2o6vj45zn
  - Log entry 46034: process nc pid=14470 uid=435 src=87.54.112.81 args=tj1yp2/q/edkut15 qctoa9p7h42n5yda1zdc33d0ojkqoh/
  - Log entry 13204: process ruby pid=9864 uid=744 src=68.140.62.47 args=yu4ogl6hniqqtj8c38-tvs9hec/6kue/eraxd3-5uu zqu-z
  - Log entry 56667: process curl pid=9390 uid=119 src=204.19.174.39 args=kpo 5rsndj35i247v5mbt0cay7p4p9ya5tqchb/wtgmqm69l
  - Log entry 46780: process socat pid=5548 uid=875 src=41.9.218.34 args=u/lwh09bxhw2sb0ph3lco5mlsd9bb5i7d6r8hgy86i44f--g
  - Log entry 11054: process wget pid=23658 uid=849 src=182.198.135.208 args=j1pn25k652kw852-2/21vrysfatabco3fp47o h4g-x076m1
  - Log entry 86827: process bash pid=28731 uid=217 src=8.90.94.98 args= q99n5 -qc95g61-tgbsyj6k0anqzpk64 r4gqm44uwztiis
  - Log entry 76567: process nc pid=22927 uid=821 src=91.83.65.48 args=ie39gbxdey39z6xo3cjqcsk-kvgvv5 1c841vhp8tnpz9uqf
  - Log entry 93536: process curl pid=29613 uid=341 src=94.193.180.22 args=g/hznx6mpcf m2qdwyt34hyrd4cpo6zfyd/jg8-ggfp284gn
  - Log entry 93646: process perl pid=3179 uid=39 src=78.161.210.148 args=uxwjhu-6pm9a40kyel30 xksll446c2ovdt1boz44ciljj5h
  - Log entry 96080: process bash pid=20991 uid=471 src=94.203.244.248 args=wft6t9vco7pxft9e7xt/l-lticxfocylv0qfe 6j9h/a86ov
  - Log entry 18757: process bash pid=1483 uid=170 src=2.122.176.167 args= 0s551e4t uxteynq0t3/u57201n46-j3mc7ocz/v0x05 bx
  - Log entry 76790: process nc pid=9682 uid=127 src=182.133.235.122 args=ks0f0n14yhgq5/bzlxafdrlbobsykl2itkzwphe he9wx2oh
  - Log entry 80245: process perl pid=4033 uid=631 src=141.236.251.142 args=/axmxyglxr5/j8vvwx88is3pxke89b4nban25us59by6lct2
  - Log entry 19988: process bash pid=21021 uid=847 src=162.67.242.130 args=h-3-u2bejtwi1hc-yazounvxa/f2nqo73vrdbxyvgtzt1e6s
  - Log entry 17612: process perl pid=23182 uid=901 src=70.133.146.96 args=nk5yniut5kj9txi-tsz3sby5depovlls0l/6-ltuji1ua9em
  - Log entry 81297: process perl pid=10814 uid=809 src=56.127.123.33 args=9 l5 gky9dmb0vriz9rx4m4bvh26885acr49v8tx9160y5sk
  - Log entry 25517: process sshd pid=13034 uid=472 src=62.62.88.140 args=3px1drv3golizvu/5 27qh5h4ko-u89m5stoqkmgb0nvg440
  - Log entry 16190: process python3 pid=13030 uid=493 src=127.72.30.94 args=--9 wla 2 3b3/zwz7hh6l9d5q4vakb/fenaddup8mj4gv8b
  - Log entry 36439: process python3 pid=20382 uid=838 src=11.178.205.245 args=zjjsw7os9n/rkao2y-ijsy3vys32jlnyj6qs4-5/flx00ro3
  - Log entry 54454: process socat pid=21878 uid=643 src=189.190.35.234 args=-xl1mvrcdzp0970vxhlpg-vcc8jywfdephygx/1jtk 9aan/
  - Log entry 21742: process socat pid=13880 uid=599 src=15.214.154.118 args=3y/566/76x95cl7t1fm4dzjhqb//3sfccepq5q6ubl4aiz1s
  - Log entry 76868: process curl pid=17105 uid=289 src=36.109.57.165 args=trsnchuikwr9rk538/bvcgmdi1tfbfe06ta4nj8hn4twvprv
  - Log entry 15785: process ruby pid=7783 uid=648 src=51.162.13.98 args=-9vwkxczbbggb-dqgzld5khfarrmklgn162y3w0o04 2zo95
  - Log entry 17899: process nc pid=25950 uid=384 src=125.246.220.71 args=4iacwo3pfzvnhdr31nnq24a7lu3zu2yvh56-qj35rmet b6/
  - Log entry 29233: process sshd pid=15278 uid=623 src=207.24.18.89 args=i h/ez4ufqk29syh ec6icmxv3tkacb9kfmmkl1/0pwvp2y5
  - Log entry 70957: process socat pid=24217 uid=636 src=92.174.121.109 args=naw7kz1/hjkw4u5hef6afnhwe5i 7nq imeg3lqthi0err l
  - Log entry 72601: process perl pid=4221 uid=513 src=113.65.120.154 args=x 3uwxz5 z  35ig2klzy7wkljzmm62 61cf/k0i0u3h rsm
  - Log entry 55506: process curl pid=3045 uid=369 src=200.166.246.206 args=iyo5wy4gvsie7-9/pi yr1v8 7l1 5hh-phtw4l3say8y2as
  - Log entry 40435: process ruby pid=26979 uid=786 src=213.156.186.10 args=criombxvx2x117nzfi9fyk1zmmiyh26q9rflsgjpeohmjolu
  - Log entry 24623: process perl pid=31890 uid=288 src=139.73.222.165 args=e9fshwoj0xapw5e24p50y/33kgf0sxb8x7 rsyh7iz63is0w
  - Log entry 37717: process ruby pid=25992 uid=30 src=155.196.109.70 args=zhlhgyw81lba6p51aq7p8 buewsxs3igubs9vgnp 2o0dnfs

## Supplementary Technical Detail — Section 56

Automated correlation engine identified 34 related events in the 6-hour window.
Baseline traffic on port 48335: 3 connections per hour.
Observed traffic on port 4444: 165 connections during the incident window.
Statistical anomaly score: 0.980 (threshold 0.750).
Related CVE: CVE-2026-33711 — not yet patched on 7 internal hosts.
Affected subnet: 10.6.2.0/24 — 6 hosts in scope.
EDR telemetry: 4 alerts suppressed; 1 false positives removed.
  - Log entry 35544: process nc pid=9208 uid=260 src=22.23.70.36 args=8hwosko8t8bg8tyitsqtz-6vt2jzaenh/zqqf8xzj90 rl31
  - Log entry 74348: process python3 pid=23917 uid=355 src=223.249.177.186 args=vfhoj15-w5u99ojf 1/9lbemc36wefopk477sg7u01ke40pe
  - Log entry 72469: process sshd pid=23143 uid=912 src=115.213.177.134 args=ehmjo7vxhf62 yaetdj0w-y21z8ffstgm137nb3oaa fiobp
  - Log entry 37896: process perl pid=31976 uid=666 src=216.129.203.13 args=6vo4 o3xj0w4grs6dimxtl-yz1u3a620vw7q9bjh6jv1gsdh
  - Log entry 37703: process ruby pid=21378 uid=534 src=199.182.171.216 args=in9t-0150xbs6e/5z078jt90s21ilaomkh1a89cfruly0ukm
  - Log entry 23878: process sshd pid=4589 uid=816 src=167.45.150.111 args=3xwt sdfwladbnv digbanpwid ksyxdp6wfmbky6u0x1-3m
  - Log entry 35469: process sshd pid=23368 uid=543 src=171.216.207.123 args=miskv5gigcqm 6l-k/9r h i33jof00h/9613cdn76nmx55j
  - Log entry 94387: process curl pid=9993 uid=220 src=37.43.52.103 args=mg0nond2b7/r zyja9ibw1537 lje7gp9xwe7yys94nrkccp
  - Log entry 83839: process python3 pid=31742 uid=362 src=187.156.159.89 args=clscufrdu4nes6axisgur-s9gof2-oaxszifm4rcuziqsx9f
  - Log entry 24386: process socat pid=30300 uid=491 src=198.120.111.233 args=isb8ge1okr112-sb7hjk58-i91p7ksaei8w2koclim/j177o
  - Log entry 12421: process ruby pid=8558 uid=498 src=14.208.43.114 args=ud/mp/tzwpxqmb/syf3m0awfys/hbpkr07wmryco1ng3mb47
  - Log entry 38781: process sshd pid=22113 uid=617 src=118.160.103.165 args=ijbmqj2t6zy4y6e bvehv79ydb-xd/ m6vu9us0gu1r oiur
  - Log entry 62156: process bash pid=2133 uid=841 src=90.163.53.123 args=o472d8tx-1s6tz101hgul2oe-i7c5i jg0gb/vid/odoteal
  - Log entry 68896: process wget pid=21515 uid=673 src=12.172.232.20 args=--bbdaoo1oymax6ktm5ek3qkp0jh0oifj-px5/hr4ynbx6ez
  - Log entry 37242: process bash pid=30683 uid=211 src=10.130.193.72 args=hkul3jesu9hwol5cpz/wu83myw4pfz986496owbecjoblg j
  - Log entry 26858: process nc pid=16155 uid=494 src=160.117.86.137 args=k/ois0c-qyjxd0i1 zgjg0yg8enrdhl9rpsuj8w7umfpcmxx
  - Log entry 31168: process perl pid=26457 uid=122 src=186.135.132.175 args=kbpxdoqj/b5kc1a/j6/dpwco7w-6i0/il5 bkoxqv-tay0dm
  - Log entry 69268: process python3 pid=7574 uid=506 src=3.143.210.41 args=365vyidqwha2pcnxu8200teh3f 5wxuz9qk9/5d1je/p l4y
  - Log entry 18590: process ruby pid=28056 uid=272 src=29.149.71.5 args=a65nlvnq4lxg1ma071o/6 ai vjoi2m7flfde 62 7fw0k64
  - Log entry 71729: process sshd pid=27478 uid=215 src=130.194.82.80 args=w8w3h7rn5dzt-fuevyahatlx3rw58zwr3o6 cd5x fhx3e f
  - Log entry 64737: process ruby pid=29160 uid=523 src=203.130.170.177 args=-m5edjfs39iy6r3chzkluzjbd b11jyw4f6ibzjtw3bldl0x
  - Log entry 50361: process wget pid=17795 uid=349 src=100.21.136.137 args=y/sgtj3xrqm9/3rr5qql9cmu33ymou4hu4g60-jaqm7 4bd8
  - Log entry 73750: process bash pid=17016 uid=890 src=6.46.39.155 args=z8yx0vcn/v/kjr9ccnmx-5vamq /32fh-itthc3h260d96k9
  - Log entry 74737: process python3 pid=15048 uid=131 src=44.173.213.251 args=3qdqy3qk8anywsdgygxax-hcgxdgh3v0ohy13pv4j2d-aolv
  - Log entry 25673: process socat pid=20561 uid=947 src=222.111.117.248 args=-0c6cx/2-7aesb6m6ku3pbddi z9xwphmacgwmf/b-ajpmkc
  - Log entry 73216: process ruby pid=4533 uid=368 src=129.74.61.179 args=72aeomnlq8zdd x26utw63yel5nndwq99at-5milyjnld4tb
  - Log entry 23412: process bash pid=3015 uid=820 src=176.2.92.230 args=joxrev6wibs3dfn8bn182xz- f5eq850q771kh /f7nsphga
  - Log entry 77659: process perl pid=23985 uid=712 src=53.108.161.163 args=n9alxv5usn6zqzne1r46 vc4/c454rrp7i1sticeqo2d7kh6
  - Log entry 90076: process wget pid=15701 uid=644 src=3.29.206.152 args=uykugm8a7hg5p4h g12wb9r6hj7zdx/2wvg6hz3tl ywj5i7
  - Log entry 13211: process sshd pid=20754 uid=826 src=41.199.71.107 args=bmm4oil3emcr0px7hfr4oo-5mwfrco57bxv7rgsfz81h3-0p
  - Log entry 21093: process curl pid=23075 uid=767 src=89.119.133.91 args=h2scesf8nooa41cbsz gz3er- r mq3bo9y52 j5ithducun
  - Log entry 59000: process curl pid=7411 uid=825 src=63.45.171.136 args=fgd18pphgnvg4b925q8z9fb/53bz 77ygvga7w-os8onjrqa
  - Log entry 88261: process nc pid=19423 uid=929 src=1.100.159.40 args=o2zwsm55b4v/yy/0/3fsnsku50qmz1xfolfzy-ynb094d2 4
  - Log entry 11393: process sshd pid=15139 uid=582 src=182.159.90.225 args=klanj1 ccxeakghqla2116kgnetfh/869 y0xz2jmkkik/vu
  - Log entry 14084: process bash pid=22581 uid=676 src=66.64.230.134 args=7frzd6vr0s3co0dsjwyzne9no1d8nwmpw22c9iladozj-lhw
  - Log entry 63438: process nc pid=20749 uid=124 src=77.76.228.76 args=hdn eh07wmav3 -oear82fnjm/n6eo/g3mxk c183vqt-jsh
  - Log entry 81012: process ruby pid=14710 uid=132 src=133.71.15.144 args=rd3nx17smw/hzc--/aoorpmjehrctio0nhya2c2oxlc/nbx0
  - Log entry 52310: process python3 pid=31760 uid=208 src=203.21.86.229 args=5nupl046bn2 7t lozyl/veq6w72iu07m5ec32smvgt/-/in
  - Log entry 72112: process ruby pid=28541 uid=705 src=166.215.153.62 args=664eq100nr ov hmtgi ld3khkrwy7 w47xdim/hvc1/1-rm
  - Log entry 53084: process bash pid=12386 uid=195 src=60.68.197.175 args=kwitroweai7gtukowlq093wrarzclppxi5siv13v5iuf/oqa
  - Log entry 44628: process ruby pid=1162 uid=269 src=22.81.194.1 args=pn7aelpb0e1cathoqhox0zdtarncz510u-xs1l8-k2x036-w
  - Log entry 14705: process wget pid=23463 uid=769 src=73.32.90.22 args=-6zsxnl4zyg76uky4fkf-qtqo/gk9xmh-fgvu661nx30xdtu
  - Log entry 91601: process socat pid=8541 uid=691 src=46.187.66.50 args=gu4mn06aqzdgqg-9j6tbl w-49sb zfd4uwox/ksihh7ovwm
  - Log entry 80992: process bash pid=2230 uid=857 src=121.34.50.146 args=vnpj1equh0-tc280r2/u7pu1-2emhlcmemufncieykpeal/j
  - Log entry 33025: process ruby pid=22251 uid=220 src=53.145.98.74 args=phnbs-g 44oea/mi2n55zcw72k36aiwsxiwefpim298comcr
  - Log entry 78308: process nc pid=9820 uid=201 src=155.168.2.12 args=ywz5fr0 v8tjskvoq75gq/kyxqxsf517utp00fr6lop4co4v
  - Log entry 68839: process python3 pid=21026 uid=145 src=187.147.242.73 args=pd84pq/x2u2cmy3c zzi156v8ha3ckc- 5uoasdu4oy8xf-s
  - Log entry 10516: process perl pid=7396 uid=894 src=145.234.98.245 args=ot8y83rvvx7x/9rh9z0f/ 8tab18py70kes4qkgd-8lbc5vg
  - Log entry 44212: process perl pid=30269 uid=888 src=93.165.66.128 args=f4woe4zjut7h4 fg-fga1sau8btzbu1yssl7qj92i7spp9kb
  - Log entry 44797: process perl pid=8224 uid=853 src=164.76.40.225 args=b325oq-kpuppp/sr5zpl /oaiuy9ayt 49c9c9 393s6ofzd
  - Log entry 98379: process python3 pid=26885 uid=513 src=37.7.53.147 args=4 9vx1l6clnfvw7p-akw26kfh6pktm42lh2y3hivrxl fwo 
  - Log entry 54454: process socat pid=26877 uid=94 src=19.65.222.118 args=wv7n9jkx48lmkc0h-0y/zinfuzrfgv45zq2 1pxi0vopo0 z
  - Log entry 21233: process python3 pid=17751 uid=259 src=164.186.114.252 args=aamfjnk6wcj4su7t1vg-qjhptbs3byhzynp8dzkjf4jtvjap
  - Log entry 68056: process curl pid=16041 uid=614 src=45.230.0.183 args=eqgd64wn4je3/0wii3k1gvbkm04pb7e/j5/x/nk398 s56tx
  - Log entry 39006: process socat pid=6828 uid=44 src=183.121.206.44 args=169/obokj2 kr zroxm/t1ydnx6k5qvlk8u8mfw1kxqrr/b 
  - Log entry 40438: process ruby pid=6544 uid=241 src=121.220.174.194 args=9/x6a-q3v3ctmrhqmubppcd3dw9rb 8by72enmju/931a7b4
  - Log entry 83149: process python3 pid=18932 uid=286 src=36.1.166.117 args=r720qrjlx287yiw/wjfdr/9u0-y45vta/xtqacs/a71izg3 
  - Log entry 50248: process sshd pid=22092 uid=994 src=124.185.243.242 args=rebdhmifsnx04kvk7k4p0 2bhvc-dpemqy6nza8z60n7ok6w
  - Log entry 26310: process wget pid=26622 uid=26 src=172.190.135.40 args=c74/6lkd-q dbraxonij4efg yflwyi9ojmaoi364y 1i ho
  - Log entry 23078: process sshd pid=29192 uid=825 src=65.110.104.4 args=8dzoaisp ecxt8e09vj146i2v9ff/5blp5h85wamsh5 ye5t

## Supplementary Technical Detail — Section 57

Automated correlation engine identified 29 related events in the 6-hour window.
Baseline traffic on port 57086: 4 connections per hour.
Observed traffic on port 4444: 130 connections during the incident window.
Statistical anomaly score: 0.920 (threshold 0.750).
Related CVE: CVE-2026-38995 — not yet patched on 20 internal hosts.
Affected subnet: 10.5.4.0/24 — 6 hosts in scope.
EDR telemetry: 1 alerts suppressed; 1 false positives removed.
  - Log entry 95765: process python3 pid=6567 uid=228 src=66.208.12.225 args=ctt7c3wpkbdg zop0cg6vh4-g8hwvokuecq6sc5ee0p9imzg
  - Log entry 58804: process curl pid=12273 uid=383 src=55.90.138.91 args=5pwkdxxbz1zzgc/o-3m/a1i9idxjfpn6mdnzc0ljm g47ir0
  - Log entry 45439: process perl pid=24138 uid=451 src=120.11.62.7 args=ojbqhhqip6n3uqz/6ysl4qg18h1pv-w/jjkfcidmlwvtq /x
  - Log entry 28875: process curl pid=20011 uid=265 src=183.168.41.52 args=zd1q2iqv7s-6k0lb16khai9u8uqs/2w0gw7egrncml n0rmq
  - Log entry 33939: process ruby pid=21751 uid=435 src=114.160.178.226 args=b5nfkv4szigpohnvczs4dwjm7a0q/hz1n9573ax640i/ s7 
  - Log entry 53402: process perl pid=2497 uid=117 src=29.56.233.183 args=lrneuanmhcm/f6izaw0zffhykpsiq7k0y43bephr508e1jvy
  - Log entry 19912: process python3 pid=24421 uid=473 src=89.115.8.28 args=g 056tyh5jprfla7cg-cui468gwiuriv3sjmblew34fl8oc5
  - Log entry 34741: process ruby pid=3832 uid=623 src=110.40.184.92 args=yltd 42i0q8pt5h190627ahsrcmw3iisey294pi3gf9-g5mc
  - Log entry 36485: process perl pid=30074 uid=870 src=158.62.228.184 args=v19vjr /z6ikndeo 5yvgkpfxgwi4py77 75f5wllo65t0/u
  - Log entry 96696: process wget pid=31266 uid=864 src=181.18.94.83 args=au/rb9a7i 3ozy4hryt-386h8/begaodn/3acjddrtkku45p
  - Log entry 72973: process socat pid=26576 uid=224 src=193.111.104.145 args=hay03kzc4 ioh1lf059-4brjhnmtcp0bguvm01r-6/82-opy
  - Log entry 61375: process wget pid=20344 uid=362 src=17.178.114.143 args=ljbeqgry72s7rv2cz  gpa 1ylepo1lq5iafa/agna36ke3d
  - Log entry 13558: process sshd pid=13635 uid=554 src=39.185.9.219 args=ef6-hodvyvuj17/h0qbd49vv6q6csldu8aju dtva5xbvdrk
  - Log entry 62918: process python3 pid=29054 uid=434 src=189.54.126.135 args=nzjy2x gaa3cc6/y1y3r2tl wexmg2h5s6s1xa9swzk1p3u-
  - Log entry 24417: process sshd pid=31498 uid=934 src=85.0.207.239 args=oak -zxo4r05n pqbxxa8 455pbkjhfeoog-wfrce2n0lh80
  - Log entry 89432: process perl pid=11854 uid=676 src=205.224.107.192 args=x/xf6u0zu18di2lh2-5gi17w8/b98sswh7ay4/1m6gt4f/2d
  - Log entry 82059: process python3 pid=15901 uid=38 src=50.105.62.67 args=thl-67lq1z0/96tqawwjiam24m7 bw41zi6bv4v v3am4irw
  - Log entry 34619: process bash pid=27102 uid=102 src=14.241.223.161 args=x5xa pn76hpt/jno4biqhmpd7kgznikf9ywjgbhbhs/hd0zg
  - Log entry 19782: process curl pid=3339 uid=583 src=9.161.195.41 args=1qejmcd/wo0e 3h/28zh3bl9lxa3s/x rpossn20m6s9t1lx
  - Log entry 45647: process bash pid=28324 uid=267 src=68.28.234.116 args=i crs6t07o1xl701hfwz-bqt89xw9bn42bneej7xu872f6uy
  - Log entry 49915: process wget pid=28879 uid=230 src=167.47.216.188 args=vvozrn6m0ngp7okh6ixxps0hmq1rj38hzi0t38i/989t16qa
  - Log entry 53466: process perl pid=25299 uid=265 src=47.115.177.126 args=h1-oq57wwb3jslo3o89q4bvdwzzyt7iwda-psr4rh13x/ajw
  - Log entry 23563: process ruby pid=10234 uid=995 src=26.251.59.66 args=rrpdcw-ya55fxzw6dh4o 0dmy8391ymgxyso9co/3 g6fqk6
  - Log entry 23356: process nc pid=7406 uid=990 src=53.137.142.195 args=x5wlczjxui2em74cqt137fur jlbvsbfh50s8mc5 hs5jvb1
  - Log entry 33632: process nc pid=6153 uid=756 src=135.74.26.124 args=fps871gros dv5fpn30el- rkre49byx-8z/4cxtdbrjd9kp
  - Log entry 92152: process python3 pid=14241 uid=8 src=8.247.124.247 args=mg5bu6uq/ve0d9-ihnle7xr5241 to37c jvvu3o6vgmzf5h
  - Log entry 97973: process wget pid=15517 uid=82 src=97.132.60.190 args=jg0p9o7w6tgb7cepxn/xehti9cs9sw3d7mnvsjn19huii0md
  - Log entry 79717: process python3 pid=16841 uid=944 src=85.230.207.219 args=yxjp2br4mxgvl5wdw76/vxbkzcyuhssnaott4z8ar8qg-4mg
  - Log entry 63761: process wget pid=4124 uid=170 src=133.38.13.17 args=shmm 0toafxo 1o/2nzqr3aaaqt2ye/2ao54nvm qxjcebpe
  - Log entry 52219: process ruby pid=19302 uid=228 src=41.60.97.119 args=pk6clymw-4-djoc4rdp lf5zyp0grmmt0b98h/9j9gc5okzm
  - Log entry 51313: process bash pid=3451 uid=405 src=173.212.65.80 args=q3su37a8ta3zws2iti20if p8vrpd/3-bds-1apuz8qu5qby
  - Log entry 92827: process bash pid=18539 uid=780 src=188.63.51.73 args=gzrx6hez-r30a63t5bulw3m4mnlncseu7jpk2u8/vwzdw-jv
  - Log entry 84912: process curl pid=13637 uid=95 src=160.55.160.163 args=m4ie0xx3cpqd2v0d59-w0orpjvl4143/ccn451tv2qv83cqi
  - Log entry 20563: process bash pid=25686 uid=268 src=205.52.195.153 args= 6esnkoo374/xw13ch5-2nwp2t7z-lcrudu6gbl gp4qny9u
  - Log entry 57189: process wget pid=21924 uid=187 src=108.82.21.138 args=bpz7407kc2-bj55ii-kd0fxj9h1ki8w8t7hrqwrwc77uxlxy
  - Log entry 69359: process wget pid=9897 uid=683 src=142.248.215.71 args=nerrk1s5p9axf0siy91ygcw9apx o87s0ctiti1w5lcpr2yh
  - Log entry 79409: process ruby pid=4415 uid=64 src=39.31.56.222 args=w11q6yl1sqyp 5ndhiydkij p6a6va5iv-82xmtjwpc9ocef
  - Log entry 57868: process bash pid=19803 uid=693 src=111.8.74.196 args=c0 jz0rk82bxdinmm510nzsc9p9qb/ugmf9z3gdwizo8/x/o
  - Log entry 29351: process bash pid=31186 uid=617 src=34.211.44.101 args=4m626oxep1ux0/73w37-x-ua3zwtq uafyu4a2q-swlhnazs
  - Log entry 70832: process wget pid=19581 uid=81 src=194.74.65.40 args=7m8zk4/5zb2w4q/h tpjbgst6ebl-nsa0fixfgogz/5i7n01
  - Log entry 55782: process python3 pid=15618 uid=183 src=53.11.213.38 args=qq/mu8i9y83uk66d00-jqi/dc05n5q0p0i8lmh4g6 z7/z-v
  - Log entry 54624: process python3 pid=7173 uid=11 src=74.43.170.124 args=qhdxsn7/bn3r 1fs4eq6/9lk0rqnj2hnnkzlq6nk88h vont
  - Log entry 51243: process wget pid=15714 uid=554 src=59.173.157.89 args= zt9fmi7s9f11a7kidr10/ca2/xo3w1q52jjyfeds7ad6awl
  - Log entry 56223: process python3 pid=19431 uid=668 src=75.95.218.149 args=u5i/wcldfs-pdwygp2-4p66pcvi8 fz0nd6ysknxjor95eg6
  - Log entry 56121: process socat pid=22541 uid=254 src=207.179.110.227 args=yddhpbz41gg10ph6khji g0s4ded78hf9uv97 jz3s sy-fw
  - Log entry 15013: process ruby pid=8295 uid=447 src=138.21.14.137 args=e0g162xx4/xvmyovd3yr85 ldp2c0vztmcrthnbrkjwwqhws
  - Log entry 23929: process curl pid=23755 uid=316 src=36.39.165.253 args=2 opc fmi7p7i0kc532efxmguznyqbjxfrq9498vigh9cezh
  - Log entry 37086: process wget pid=17649 uid=204 src=3.194.135.205 args=y/4o9ly4i tmzqzkos d3x0-caa/jkdjk9-tvk103vkkzm62
  - Log entry 13018: process bash pid=15861 uid=474 src=189.1.213.74 args=/ dkcoadkgh6y/3- 9ug6/2j0xs4yqu8dg/ojdmyk/p0 bbw
  - Log entry 38377: process ruby pid=6234 uid=553 src=145.221.193.122 args=7co92-bu7a3xjth m1x2ncdlk0xrsed6 wpogq1zzgv ns8w
  - Log entry 43047: process wget pid=23199 uid=584 src=130.234.198.201 args=0hr5siak-ozkz 23fpoxm3vjtfhxkpaw34ouqw0f2-kflelb
  - Log entry 72521: process wget pid=13317 uid=548 src=99.162.235.79 args=wcy70xcrk3oewpj19h1nkxgor9wvpbmv009duj3zmm51od3c
  - Log entry 31569: process python3 pid=4952 uid=780 src=172.10.23.158 args=xkhyhuy0kafhr nrdy1bkjpd2k 2wt64wv3wf-/sx-lltzvw
  - Log entry 18098: process nc pid=10149 uid=635 src=63.163.123.153 args=ggm//5817khkw-kvlfjfojg v6zqja36ri vwew3m2jdniht
  - Log entry 97430: process wget pid=12759 uid=323 src=203.64.222.42 args= wsf18wyp7-triie5s6n/9od2okwq/v0hbg5cyvr4br85ed2
  - Log entry 52929: process bash pid=21123 uid=84 src=218.228.116.103 args=k-yxv9yr32zzyvp2d-hrndttw-o8ygawi8p1y9gnz137f84-
  - Log entry 48280: process curl pid=12336 uid=798 src=164.51.90.210 args=r0kfqf-gx3qgs 789fstlvkyrr5sopk7gccpo iib-2m52vi
  - Log entry 58213: process perl pid=9617 uid=299 src=213.151.80.138 args=b5bhs43v49nm9wwm4om31az/k7xetvx1m93ujox50cvgh3lh
  - Log entry 12129: process wget pid=30405 uid=698 src=39.85.114.8 args=hafrljs8jo9x zi7x3w9klq/n4g2ykg/5mjpc8gphtj69vz4
  - Log entry 77188: process nc pid=3907 uid=593 src=44.186.247.16 args=oa969kc2xasuiyzl u0 v5bvl95ox-fy 38b7xnp1k h2x0c

## Supplementary Technical Detail — Section 58

Automated correlation engine identified 29 related events in the 6-hour window.
Baseline traffic on port 44743: 2 connections per hour.
Observed traffic on port 4444: 107 connections during the incident window.
Statistical anomaly score: 0.915 (threshold 0.750).
Related CVE: CVE-2026-37387 — not yet patched on 14 internal hosts.
Affected subnet: 10.2.2.0/24 — 12 hosts in scope.
EDR telemetry: 5 alerts suppressed; 1 false positives removed.
  - Log entry 22312: process python3 pid=9381 uid=749 src=75.156.163.57 args=cqgqdae5rxvjq7dzwul1rsygdw4np//8jrmdypp8q 9drrne
  - Log entry 46394: process socat pid=13341 uid=296 src=110.121.75.181 args=51wth/b-k5 f/gljp7n3gm1xm47oawjb1e9yb9bixq7chz-n
  - Log entry 56918: process perl pid=18072 uid=314 src=216.195.127.35 args=8 lfwq9c pad/ j5j5/z/2oy600t86m5 0xaa35yo8sbdcfb
  - Log entry 91894: process socat pid=9118 uid=409 src=34.132.222.53 args=86xf2b3slj-j4zd6d0ftu2dux169fhchdi6pztzo07f2v3//
  - Log entry 92652: process perl pid=21215 uid=134 src=73.163.144.38 args=q/pzf6p9dq6twsalos9lt3n-0a9f8id ekudtrfj99zg-8ks
  - Log entry 29250: process bash pid=18847 uid=914 src=130.90.68.243 args=-bgg93ikg2ld029whk ayet-g15amfjmlg2xmc59qw4iaped
  - Log entry 45145: process python3 pid=10635 uid=70 src=71.228.7.83 args=f/0ff0egxij9ckxr8ia4/zm5difu5txrplurvmyy4is45vdc
  - Log entry 56578: process socat pid=8665 uid=199 src=223.74.97.115 args=xtu698kleb8h8-uoxqjrit40t21mo5ti/pwjf2eft7hwjcv9
  - Log entry 65391: process ruby pid=18167 uid=700 src=6.155.204.109 args=cwolojx31-tasx-rl2279l31z4yvp hd0lqdxq elyexiopi
  - Log entry 98197: process wget pid=14609 uid=285 src=107.56.239.80 args=88u -gex-rlu79lph1ywxxf1vgzuexn-lszhh5 3k6ancsee
  - Log entry 73807: process python3 pid=31219 uid=370 src=215.171.37.156 args=eo189o/3 e1r37sy5eyl9tv7yzscko49inxosscfkfmqpg-d
  - Log entry 76660: process sshd pid=28372 uid=393 src=207.90.15.135 args=km ukrfm6lu/rwe//syo4o21jq5wma1q/7v29w5ym pn4iwj
  - Log entry 96885: process ruby pid=25580 uid=241 src=174.39.54.83 args=j5q9ouf3a/nfcaoflclj81zo olpzo7th-k1kreiewuuunpa
  - Log entry 54008: process wget pid=18628 uid=761 src=65.43.150.11 args=zpcul7cbr2gqgl4fspa /ei 280qw0gjju7qmb36vytnaoj3
  - Log entry 61258: process wget pid=8906 uid=331 src=213.52.205.129 args=/tcysz50pxexry84x9jg78802ivcjrc3qx1zoot-d-1/dg7v
  - Log entry 23928: process curl pid=22515 uid=20 src=148.19.33.170 args=vtss7cohu0/6qelx73pbigkjustfjj3m2on-h7g5n50jnjfa
  - Log entry 18217: process wget pid=11894 uid=983 src=208.65.142.117 args=7vtudzgwbk0c5yt0mo8nf2051ilqx1rfmjzohz8vt0ne9h94
  - Log entry 38312: process nc pid=20549 uid=706 src=217.243.249.178 args=6kvgg5wrp9lz8a jkax sx jfp8o437bt59idzcgimk6-762
  - Log entry 15635: process socat pid=2262 uid=890 src=222.234.13.77 args=jdh13h6bktqk oqymzhqtkugon8uc7gl45396l02maj/ht r
  - Log entry 99148: process sshd pid=1134 uid=459 src=95.167.93.247 args=j69fi542uln3itd/gtax aw/s/5qephtr5dqxtx84u2eakwf
  - Log entry 70364: process python3 pid=2377 uid=683 src=142.110.228.116 args=y2orwob-xepn -2ii39g680zvfeejzu d2pjjdfjjyv8dmul
  - Log entry 73241: process perl pid=25829 uid=508 src=114.162.132.35 args=j6tfwzknvo4brqaavg8 q86u0xzcnh0blrf7rz4 3v1xpgez
  - Log entry 66941: process nc pid=9085 uid=275 src=43.94.240.196 args=d0jujsf1/1t /mj4a4lmz4/s23wm7gh9pjc5iytpt6/2/mq3
  - Log entry 28905: process bash pid=12738 uid=98 src=197.191.37.23 args=0ur1u2hr/6  1-d5u khs a0l-5q915fp e6oro8 tyl6ihi
  - Log entry 95548: process bash pid=14960 uid=836 src=220.231.47.105 args=er2ulrau-tia-yup5othjityjhigjc8z-4c9v85e6q//box9
  - Log entry 46713: process perl pid=29604 uid=697 src=206.8.191.111 args=9ihvyrkxsxo5rqrx7/0aurl3uyg6g0/re-it1irnny5uemix
  - Log entry 32754: process python3 pid=4107 uid=646 src=75.235.192.24 args=497stcy2f71y/xefd7whry 6-rbrpx9sk7c8kj-ngfcd/qhn
  - Log entry 81559: process perl pid=17884 uid=269 src=113.44.192.127 args=i0mfzji8pqfboam9-govsglp 9pcot9h2wfaqerrfodrbmdb
  - Log entry 67833: process sshd pid=20202 uid=903 src=167.27.228.22 args=y2ydb7eeq/k49c285zzku7b66txf0pen/p yh3fcot6tw1ip
  - Log entry 81042: process python3 pid=10813 uid=73 src=72.58.190.20 args=neyqecdhnflbpyu1yv39j-n/ gwk751d6t/1-rml7hr3zxjh
  - Log entry 50547: process nc pid=21795 uid=354 src=104.49.2.195 args=3r4qnu6q/upk3m5r5010atrowafle/38vlgn2fnn338e6276
  - Log entry 57088: process curl pid=31733 uid=902 src=144.179.218.98 args=uut-st3c7zrw4nh8gafwl8pbqtaj4jb/j/71smffjo/83ce/
  - Log entry 54368: process ruby pid=9128 uid=408 src=81.213.57.171 args=q-gr73lvygqmdm-b2hdjb45 j mydjco -570d3uqu0g y4n
  - Log entry 84046: process socat pid=2362 uid=229 src=182.47.212.205 args=e68qxlubf2o754n/ n0fvv7hi7yrjn zx/nz5s05ndluneae
  - Log entry 97828: process nc pid=8651 uid=727 src=7.121.7.185 args=pswmkzfye8v-mktz5llum  r0a6q/g9hlj6jh9xgcerw5zl 
  - Log entry 26005: process bash pid=8426 uid=289 src=27.39.130.199 args=fakva7s -gkz0d/bl55wosz8n947md4 xcutqadevj4jrd5t
  - Log entry 45766: process perl pid=12715 uid=527 src=16.134.106.105 args=83crlzpgzhc/ka3oe-5yruqrh79g2u5a79o35axq08 n4bt4
  - Log entry 51212: process socat pid=7150 uid=268 src=13.155.234.245 args=/7yvve7165tk9ju42spt bm5n/ixx4f-1p0lupversskrlkf
  - Log entry 31911: process sshd pid=8579 uid=116 src=101.130.241.78 args=irz8h2/vvfvk705x7c-m0ls91wxz1yq4jfqf66gihk14o/j7
  - Log entry 27470: process wget pid=22600 uid=873 src=133.148.189.46 args=v-27ll04ho2wca/hj16-8pnwsuhcy4pajzx kbj9u 4v5rbs
  - Log entry 69730: process sshd pid=26264 uid=551 src=146.192.25.103 args=/my3vxyah5bvhlvhi9 us-k/z/q-nj-skoglih854v7e zix
  - Log entry 40107: process ruby pid=9395 uid=422 src=20.116.52.163 args=t6bgtps0dxy5wgvvvvhj00lko2s9e0mvz5-mhs/8c/vmyy3n
  - Log entry 70775: process nc pid=11367 uid=238 src=152.61.185.119 args=sbm2f0ysn-ubzn kiaar-in9yia4mbdnoxyp9-gerg2h7d77
  - Log entry 84644: process perl pid=14887 uid=966 src=15.177.213.173 args=8f-12epj65u ev7tlgqcw7k53/roe5tlbk-teehc171dhqu0
  - Log entry 15362: process wget pid=21774 uid=121 src=97.56.117.96 args=k-fkhrpyypk8nh2j8/jd9bkbzj2prgyt3yovnbhu7/u9nziz
  - Log entry 67707: process nc pid=5383 uid=514 src=25.128.115.142 args=i75a/v-tu3gev7y/y1-r/t8slmjmbc0jculailtp/96s5vlj
  - Log entry 78194: process ruby pid=4728 uid=840 src=34.61.37.53 args=ckwvluhqx0a7lyyhfbf-214i9l9i2rga//uawc//1wlhoykc
  - Log entry 45028: process ruby pid=18886 uid=541 src=98.176.3.13 args=lk10cv1xnc3uydwo2paeq8v1qtm7s9x/to3yrc-24s3x/9rs
  - Log entry 82967: process perl pid=26530 uid=139 src=42.45.31.58 args=5565dq/zsz2k/vr4xdjomjdvj//qkr/ae0yy2nen0ze-xysz
  - Log entry 81334: process curl pid=4498 uid=430 src=73.39.89.189 args=ieyatnbqjq/39e1ha2st90qaqmkk2vkycr8vjjx5u2igzc65
  - Log entry 41692: process nc pid=4525 uid=779 src=62.34.199.156 args=ho4khzzp54z3cm2oz5hfce1f5xb5vuaier2gwq8em9uwp8ec
  - Log entry 81014: process python3 pid=30315 uid=463 src=68.84.46.231 args=iqchg912rnapmfo68v1ehi0 sng yjsz9y818mtt-mrc76qt
  - Log entry 62313: process ruby pid=17188 uid=959 src=60.187.223.25 args=1etihg0c7fmp1n im3s6edgpv/xebryuecrc8zngz 88vghy
  - Log entry 14712: process sshd pid=21783 uid=160 src=86.34.111.210 args=49otlsyxjosxo9vwf9tx4u5wsq4yu37 xqi  7/zsy0sv9oj
  - Log entry 17415: process curl pid=18154 uid=647 src=124.137.43.86 args=zfk0v75wzpl98d/njv88wwbaprvsfo4mu1n77y1a2s7ydrdg
  - Log entry 44012: process sshd pid=17944 uid=316 src=176.36.150.216 args=kff c5n1glhmg4w939sk3i7i8enjhx7/zqmylkr1-mv08hh/
  - Log entry 93042: process sshd pid=25998 uid=315 src=28.5.79.69 args=5s6 qg0fn1na-ytqmoht-j9dju-cg/sq8dff383wo5o5oa/z
  - Log entry 68978: process bash pid=1185 uid=757 src=50.183.139.212 args=8rigpo65twh4qk-/36nw-i-cgu67/ti0bh-ldcc8qg2-3/2d
  - Log entry 41976: process wget pid=10873 uid=321 src=107.36.197.200 args=s--rrsgmebe1z4xbvog4rf1-6344nell 65mq0y ou/-4/cb
  - Log entry 78541: process socat pid=26948 uid=203 src=99.194.98.38 args=5qhnobkejs29bd8zy7gfxpalsh 9uy5v2s/bq-rbkzfxtbqi

## Supplementary Technical Detail — Section 59

Automated correlation engine identified 36 related events in the 6-hour window.
Baseline traffic on port 47333: 0 connections per hour.
Observed traffic on port 4444: 165 connections during the incident window.
Statistical anomaly score: 0.906 (threshold 0.750).
Related CVE: CVE-2026-28775 — not yet patched on 19 internal hosts.
Affected subnet: 10.2.0.0/24 — 11 hosts in scope.
EDR telemetry: 0 alerts suppressed; 0 false positives removed.
  - Log entry 75712: process sshd pid=1748 uid=808 src=176.129.241.234 args=plj87da0q zim3snozrqy2h dh8mx4099-kz0-9oot4k2w4z
  - Log entry 60969: process bash pid=30654 uid=675 src=200.221.46.33 args=vq36q-qty36p3f/77jexwq3m du16l/g1zgn3sf1cmpamzyu
  - Log entry 70370: process bash pid=2824 uid=877 src=29.186.79.64 args=1ru8-enykdzjhhf554pj4kzi26c0i5d6179421q0es4i-2og
  - Log entry 86289: process curl pid=20099 uid=727 src=95.55.22.213 args=na3-l gbdcp7zgzrha7zahtmya4gzjeb1jgd feey/5caquc
  - Log entry 93208: process perl pid=31608 uid=320 src=50.77.164.34 args=eenpgue56fkrdv87aydtw 8e18za/2 al7q/bpzegdf0qadh
  - Log entry 17740: process bash pid=1074 uid=420 src=212.128.32.206 args=-u875nfhf8ss6jf0kektdv/8 1n gfygb9rw-wkruo5nvr9y
  - Log entry 22547: process bash pid=9591 uid=591 src=211.144.117.249 args=7pfowgfy7ysmrvwqduc9b75594fdl-kf7z61h9nb ac7sluy
  - Log entry 24803: process ruby pid=27084 uid=263 src=97.36.159.60 args=/4278otij6bi-j3j99k6tfz5k2 8e4kib/d-0y2apkwv0myn
  - Log entry 62683: process wget pid=12501 uid=951 src=148.4.89.168 args=f3pzta769s0d9z7fgh5z14oimyzvmmxu0jmqla1k5buj6mom
  - Log entry 91035: process nc pid=2841 uid=698 src=213.240.63.59 args=1-o03 qhdls7hxg 3lxnf7j-o6i   9rymtbu0dcmwd8n1z4
  - Log entry 91156: process perl pid=17997 uid=614 src=223.9.107.102 args=cdpzm/b7az85ussxuoav2npe5oefd rnix1w6l/qdalcjus1
  - Log entry 23647: process bash pid=7742 uid=936 src=92.222.164.101 args=mwe3i88iqgv4xy/pzgzdoai9xql3i4lz1so0qyyccxm6gi4j
  - Log entry 99196: process perl pid=9240 uid=868 src=64.25.176.171 args=c-r6axacyc2chkxnpn vddrm8-yjz-nngpzsdfg9jv5g2ke1
  - Log entry 51146: process perl pid=13122 uid=392 src=47.127.133.177 args=vjl2hni2d7gsbi68apuubz2sb8zhkamaqxbcxg4-e4tt41/r
  - Log entry 82335: process nc pid=8386 uid=335 src=142.145.2.1 args=9v7/b e23srzl1eowrn5sl45gbmc7bpaeaxrzrh1jk 35p6d
  - Log entry 38478: process nc pid=12883 uid=334 src=142.125.151.111 args=2i3p0aswtjj f-/36d-9pl8lok7vww gf77os87no2--9nx4
  - Log entry 17009: process nc pid=11860 uid=858 src=128.34.4.94 args=-1caj/89jxo53pw36h36sf7s-95 cfoes9kzchohuoks9s03
  - Log entry 74499: process curl pid=28047 uid=380 src=159.179.33.164 args=w1w3wk/p0-- idm5fmw8jn2fp6lll07w1pgj5wj9qk7ormkt
  - Log entry 81484: process wget pid=20541 uid=17 src=135.93.10.59 args=xngoi6j1nvn3/tzvwl3cvs2itqdb9dlnp/vyas3h6nkm48l 
  - Log entry 70301: process socat pid=2230 uid=73 src=114.141.113.83 args=tt-angxl4el w5u13h9w/ /lw6/zajw-pc 8y4ct950ripp0
  - Log entry 18063: process python3 pid=2795 uid=200 src=163.227.140.28 args=7wijidbnu0k5d543d61o12uv7d6qogysupt3b 4-8d8d4soj
  - Log entry 39877: process wget pid=18679 uid=292 src=148.63.199.144 args=3fcbvb-2cxuuy5sckpgkenuamjq7b6qw0m3xe/ ifvdse971
  - Log entry 80831: process bash pid=13255 uid=378 src=104.217.232.167 args=nmpd7lxhhebdbiatr9vwqpn6m7jo3as5c7h9 jd lsg89v55
  - Log entry 54459: process python3 pid=2757 uid=328 src=168.175.218.77 args=uiwjxq4h04/xbgdpb6yap3yc/e4v-zvj31lpe5-takj2k6qv
  - Log entry 48594: process perl pid=27738 uid=464 src=139.173.157.48 args=xo14mem dwlmr c8g2v2z20p2xno7het2be24ry2j1e6y86i
  - Log entry 57517: process ruby pid=4848 uid=796 src=168.219.202.12 args=pwq6s70z2wmkbnwpoju6l5j4p9s4abyexg8183nlr/32w8n 
  - Log entry 30666: process ruby pid=28072 uid=222 src=165.209.90.214 args=owmdu1sjnwvgzm9g-00imba/0ey3v/bm1kcy4/q50i8x03eu
  - Log entry 78777: process perl pid=28819 uid=464 src=45.233.200.166 args=3v kzb1cx-35/g2yassi01v42ryfv7hu9lirgq4-na/6jgsj
  - Log entry 34682: process ruby pid=5251 uid=448 src=1.73.212.109 args=wk2r09ef0o 777iz1dbq8vzjezng 66t-wutl9yeufazvds5
  - Log entry 83348: process nc pid=27489 uid=994 src=33.12.77.202 args=i9ukizkt563y/7vd68/v zao1 m48zhkti/ro7a4mpkcxp5t
  - Log entry 38781: process perl pid=17469 uid=546 src=140.169.174.172 args=zacz/fjnuqhxbxy5/cqeov1dxpejelhxg9504j4ayoukqz4w
  - Log entry 34919: process socat pid=5016 uid=208 src=137.138.143.66 args=yim yfcgy6wcrz5eh6wvbj7vwm9k6xpkg1 iosdb0 b51n6i
  - Log entry 62529: process sshd pid=5208 uid=76 src=215.87.82.253 args=/h1se//jnjig8i1ou9z9w1nm j/gbxt08f26mysip 8z5nim
  - Log entry 60553: process curl pid=20296 uid=872 src=140.68.21.101 args=ab7v29rnbqjviacf3z65w9u5n7v/a-zlmh6mo9djmq9hejr6
  - Log entry 88461: process curl pid=23725 uid=664 src=211.76.56.47 args=ferzjagat2k7gcmwb64l42f2tj/hixsh/uewuz8m5aq31fh7
  - Log entry 11953: process sshd pid=15793 uid=340 src=207.253.177.225 args=b76j4un-v q5wu1z6za95q5zmhm048uk4aw129jcg  -5mhx
  - Log entry 98204: process bash pid=31566 uid=209 src=130.174.146.130 args=qq0zsejj8xw3jdk-9xg3z5zvs06oazi-s6p8l/myeby3m0xc
  - Log entry 58617: process python3 pid=3123 uid=729 src=199.197.173.200 args=jwwar65q065pry8bt7yt1r-hs34h3-5gq-i--gtmyfjy1usu
  - Log entry 13835: process wget pid=10279 uid=452 src=135.61.170.215 args=dvt5u0w00bhuahrda42l-do2zcvvaimgv-c2l5uf/iwe88 n
  - Log entry 77768: process curl pid=4886 uid=296 src=98.186.20.84 args=pq2n j2trw8frdo0 yr1 6qby8-yt4290cacpeadonfbtjui
  - Log entry 31388: process nc pid=11978 uid=601 src=33.26.13.79 args=2pj50n759ldp/ kjba8b9x30sewfn7inlx6akau3ccnd0cof
  - Log entry 33822: process python3 pid=24689 uid=858 src=223.219.47.200 args=4yh6lpws/45ss3b4176iy00w0u3ao9c5ti0domvzob5dvdm4
  - Log entry 21978: process perl pid=5967 uid=740 src=30.139.221.242 args=-txdpjbkaliv4r1nw1ftur8v7j7cifwof34/p6ail8f1an92
  - Log entry 86002: process wget pid=19844 uid=22 src=191.94.249.181 args= hcos0g9h/sj7twuaiylop6-2jrxmok4o1lyajv4ctewr8i 
  - Log entry 95624: process wget pid=6206 uid=707 src=198.55.94.177 args=-qstuk2lekuue aizv3-nc7h5bq-mcdg3xjx1vukt 6 a6u7
  - Log entry 25473: process socat pid=30105 uid=52 src=6.239.234.205 args=uv9l9i lz-i7o4nyfhaoe4c6xarfkrcw8ojmaffiu/8ejgyx
  - Log entry 14184: process perl pid=11209 uid=89 src=113.68.229.31 args=nz-tejrz016u7npdkrxrd5ufj /le0yvqip5jg-72gw/6xxv
  - Log entry 69401: process curl pid=22067 uid=523 src=141.3.124.51 args=5bsr1h5zu-objutm6cotdnvu vetju 49yzppspc4w-sa5dd
  - Log entry 45451: process wget pid=5199 uid=781 src=221.125.34.31 args=qmqbhw6vqwq w49ap143wmqsw1ad5prlowbzl2fdsafs5s59
  - Log entry 15742: process socat pid=7169 uid=821 src=217.219.117.14 args=uk7pb-dt4j2lhf32ymunlfrviu3i-5gffhauxw5vbykchndv
  - Log entry 88314: process python3 pid=14034 uid=676 src=57.240.191.211 args=p/5hh7-7-dye1zy/tjxcd6qy-2t nr1c7vtidt37i9 vhhle
  - Log entry 80969: process wget pid=20511 uid=960 src=215.24.36.238 args=2v1oo04ubx17 sw vlcp6ufcscaqnfum4-2sjbye3vvnjh/p
  - Log entry 49456: process sshd pid=10080 uid=209 src=91.194.201.171 args=oof8djf2s1hdkwqjej9/bv6ha2sb-q1b96gu81ohzd6gk  i
  - Log entry 61296: process bash pid=17607 uid=717 src=29.43.178.101 args=jrh9d63ej42x68hf/spev5j3ahsitp66ggj43ebnqr2qvhvy
  - Log entry 95066: process curl pid=20130 uid=559 src=177.72.177.207 args=zaz55hrrk3rzde8d0hj6vjbmsjh4/eft7el6yvbsy90ljrng
  - Log entry 25550: process nc pid=12651 uid=995 src=145.202.146.233 args=p83h4z/k5lscobess a oy7e/g9/anqx/u-p/bsvkyy5u-e2
  - Log entry 10716: process socat pid=29081 uid=646 src=66.119.175.207 args=yfg3aekh774iy4-mijl-m99nmyb8 7vzhxh4d6mluh2t9qgh
  - Log entry 93375: process socat pid=28698 uid=451 src=196.234.243.51 args= j1bo9-0ik5pafffxd-me5wqtqli5ozdg6l77x2avz4kjl1e
  - Log entry 59367: process nc pid=4660 uid=827 src=208.54.168.124 args=-vri9uuc8m5wp9mw1ru58e6eolmqq5b 95/ix/3kaa2p0sbl
  - Log entry 63116: process sshd pid=2303 uid=42 src=22.206.140.86 args=3g5ycm2tci387j9ae/-4w1ekr0li0-56zwvxnsjx33u wne7

## Supplementary Technical Detail — Section 60

Automated correlation engine identified 7 related events in the 6-hour window.
Baseline traffic on port 25178: 4 connections per hour.
Observed traffic on port 4444: 163 connections during the incident window.
Statistical anomaly score: 0.826 (threshold 0.750).
Related CVE: CVE-2026-39296 — not yet patched on 13 internal hosts.
Affected subnet: 10.10.3.0/24 — 9 hosts in scope.
EDR telemetry: 3 alerts suppressed; 3 false positives removed.
  - Log entry 56269: process python3 pid=8578 uid=832 src=190.194.91.132 args=7d2r niu8ym04fc54sw7k7edbhzs9t4xwuqzo82get6uzl-z
  - Log entry 27994: process socat pid=5798 uid=525 src=58.143.8.213 args=7dxyq7w/7/hq3 fwy0mapjjbr -ekgxb7nyje06cj32v-wf/
  - Log entry 10376: process python3 pid=31394 uid=829 src=113.100.177.225 args=jt02p2hvopswdsxlenej0hqlb9 ggln5cvcj5yw ec jfn h
  - Log entry 10393: process ruby pid=25353 uid=189 src=201.147.225.166 args=epp3pf1n73bcoi80j9u7d/tt9sx8iw bqtqqwnwo15k oath
  - Log entry 63353: process sshd pid=9792 uid=928 src=36.35.167.93 args=itmk4vrqziotim9pv6mn47sq9qb60rsgvqamyhj1mi-bee 5
  - Log entry 76605: process ruby pid=14961 uid=437 src=161.22.221.202 args=aza-aicpxuzzmeccjx68 dgkf470r90xtcbqbd/bqavc xme
  - Log entry 22572: process bash pid=7387 uid=278 src=104.91.98.198 args=8a8aixhpjb6vl42gh81vi25b/s6guj0zzztgmay8g-eze/y1
  - Log entry 71694: process python3 pid=31212 uid=585 src=43.23.181.127 args=r76lza -72/bhinmxssjw4zj9-p f 1iehq6/7mx63ecagk1
  - Log entry 30033: process curl pid=27471 uid=849 src=61.47.241.29 args=39i36bkeabjycu-qqd-52c 4mdpmnzvefejtxp7/yi0v3ecg
  - Log entry 71353: process sshd pid=17082 uid=49 src=118.87.150.1 args=u7p4j/xb1of77  /3c1nh-h49 7fkpixsvfbtf4dtkl2fua0
  - Log entry 14483: process socat pid=17237 uid=638 src=215.2.242.93 args=mdc9w-3 02/9v0mw7asga43dvkl1npwcaznnfa0je8kvkyas
  - Log entry 44121: process socat pid=27312 uid=582 src=214.151.74.91 args=3q6uwttvfsli6cra515eq5t4vn11zgp17hf5uust8hrn0xz2
  - Log entry 51840: process sshd pid=22073 uid=543 src=223.104.79.89 args=xk074biqg/ry493xvoq3g9vmu25wwq-7kawmr6ln1zzel-jk
  - Log entry 63945: process socat pid=28099 uid=218 src=100.18.255.70 args=z rg/gciieaxn8k0jdsqzg46wtauwf z/7f0sx74 1-9//ua
  - Log entry 38454: process sshd pid=5904 uid=752 src=113.179.17.213 args=o6scxpza32tngi7cqvjmpzvq7521/fr -jxfbgtrwvnpzgye
  - Log entry 70553: process ruby pid=14351 uid=557 src=114.147.9.226 args=d3sr6qs5o8qswq h-rdye4z3qx0jox5c3jxdqhtwfw1c8d2a
  - Log entry 13893: process python3 pid=7681 uid=269 src=7.225.79.128 args=0 8tuaih3na0zgc4fcy16hkr5l/--f h9rukl1j4gkg7okof
  - Log entry 99011: process bash pid=9626 uid=499 src=46.172.244.63 args=htoetqelapgwjwlu60ou n5b95dj2w86wjqbf2z1llydg7/v
  - Log entry 33750: process curl pid=5476 uid=765 src=66.12.241.34 args=to 2wpm706sgemzdw92yo1h6r-al3nw4k1jm3bctu-6/htah
  - Log entry 82989: process wget pid=9483 uid=850 src=124.249.8.42 args=g3whgfpox9bb vnkoeqr-vx91t f4j9bw-ze 96ln2ya9av6
  - Log entry 97828: process nc pid=4299 uid=286 src=151.157.95.103 args=huc7x34p3owww2orab8hc/bza7zca--6lotqi1fzwqf9aqg-
  - Log entry 99551: process ruby pid=12591 uid=698 src=54.157.184.132 args=5yzl10f0zyhbgvg3oz4w0-un-a66/q/he1xeul/48hzue0lu
  - Log entry 65231: process ruby pid=13458 uid=784 src=65.98.247.31 args=xo23 gz2nr bv5hls-tn2seowy0cqszpj0qvvds0x n2hqv1
  - Log entry 89280: process nc pid=31410 uid=177 src=72.76.225.212 args=x19-otbzs6mym-alohe2rqq6a58eg60gkvdg/uu72vlmwt/w
  - Log entry 97707: process socat pid=5157 uid=343 src=35.62.33.233 args=eal656nioyktff5vv8a3mg3dfqzfzh4r4zuj87xxr69t 9iv
  - Log entry 76073: process wget pid=10880 uid=144 src=78.22.82.176 args=39rlporlpxzg44l-ckis1ddjmvi8nam8f3dhpc2kpzszmmer
  - Log entry 23399: process socat pid=2684 uid=852 src=192.125.162.146 args=ytsci-a1khblrayagtp28-1l5nip7g6o42lr3 -y/fpf w5 
  - Log entry 83284: process ruby pid=18153 uid=457 src=209.225.253.224 args=2zgpx14b5wbvm xb0 l/6ylleq38ift 2do5hflpda0 o 5d
  - Log entry 70894: process nc pid=7514 uid=908 src=66.84.90.190 args=es8-5kv-k03ulbr13z kfy2hi7s 9lbc9rr7zfhkeg7 hnsb
  - Log entry 55482: process socat pid=10953 uid=302 src=99.248.254.61 args=ll04vvc/yk3jieuo4s7 knp52i66fgy4m3xhm2lzi-jh ghs
  - Log entry 82056: process wget pid=27277 uid=185 src=213.66.152.76 args=mmq4jx3vhos6 6eurk mwb-tbeakpjpn9b5o02-gy947iqa0
  - Log entry 79379: process sshd pid=1164 uid=869 src=194.120.134.244 args=3 uuvdcjyqc-ofau9najuq91njk 7c57md5sx vorefoejrp
  - Log entry 93662: process bash pid=15491 uid=786 src=6.236.115.39 args=rih1321q 1/89j73x  55sqv-ix0d0eh9j4aqb -om-nt0od
  - Log entry 72956: process perl pid=9610 uid=215 src=75.152.64.93 args=200g0v8e6qgj66cpxwsdk0ofdj0xcusu1kfi0ljosg1vfg7x
  - Log entry 10731: process curl pid=27171 uid=130 src=9.135.100.186 args=m88q1k06-oj8360nagxp8m0sfolpc9nolx706-g8w6aunk/2
  - Log entry 97725: process curl pid=5214 uid=513 src=81.46.228.126 args=ylxnd1/k19zs bzey4-mz3 6s870muz29irrnbb4ceyym1ju
  - Log entry 58042: process bash pid=15602 uid=22 src=145.32.64.57 args=73j0l1gsgzqev qqkt4dnwbkmcr/r9zvmqpa 6vop9tttogu
  - Log entry 20434: process socat pid=13008 uid=85 src=83.179.131.82 args= rgfs4c7s/ 8xnybo416vd2 9kdgok4o8yyq528nux8kyrs/
  - Log entry 47019: process ruby pid=7756 uid=78 src=2.211.53.87 args=ord8eae71uiv3rtlj2x6/it1nhjlduwzzk/30hu16/ytwxki
  - Log entry 93553: process python3 pid=1333 uid=977 src=43.132.196.122 args=0qi-beb qe4r89csfe4 2dy32lj3dm700vh7rgyt3zuuv8nx
  - Log entry 93144: process sshd pid=2209 uid=579 src=182.37.3.252 args=qz1iplw3 xme/e9ekhvvy4z-gn2xck03zv8-6dvsbc6s9-9o
  - Log entry 68741: process ruby pid=22004 uid=305 src=176.161.87.91 args=5fp2w4tp5ldivh2rore6httmc191p8ypa57y72st-hcflemn
  - Log entry 32940: process socat pid=26515 uid=292 src=152.199.176.217 args=1wv48snxp2b3o5ztlptsm-ns8ksz/ct-fcr8i2po1zq-fahs
  - Log entry 62704: process curl pid=6127 uid=636 src=36.231.39.116 args=/7iuti-cka/69vrr8whlqwi9-dsne-9pcj93/jy-k2ecei3y
  - Log entry 67082: process bash pid=21305 uid=891 src=59.36.55.61 args=d4jqzfv/7ttfot/a/tti7c481az/3f fg51o1j8y61oxxqpj
  - Log entry 64527: process ruby pid=21648 uid=768 src=209.203.16.209 args=ukt ttwhu1wq0hca3bqc-sxkj7v28avja3h nb0p9alell/1
  - Log entry 57189: process python3 pid=7365 uid=381 src=42.28.12.49 args=5t7jhphr8oisi7qgkr5fqmtcda8uy3ukvqi5syib 1py z71
  - Log entry 66721: process socat pid=2263 uid=865 src=132.101.9.130 args=3b5at6wao8x91tro6byiyex1ztz9xpdxekvbhk0ikxjj6u7p
  - Log entry 58189: process socat pid=19318 uid=252 src=102.209.189.243 args=c-8ixe/6o/duz24oq4zki9v/gy-mvm2025pg85d3pihb/kuc
  - Log entry 66977: process curl pid=19087 uid=110 src=203.254.161.99 args=jkiu8cyegnv1l9b39s7w2lam61u4b60moqq/vses/zlaxd/v
  - Log entry 59888: process sshd pid=16691 uid=43 src=172.103.105.113 args=9jv8ua2rqw0bheg1o0s2qg33bkk8qs81sb01-sy3mll7wxrr
  - Log entry 10324: process ruby pid=11189 uid=151 src=66.159.244.117 args=6ps79-1r969zub512cj8t5plmm d7e/1lasuqulkdvkl bzq
  - Log entry 81513: process ruby pid=6758 uid=197 src=202.252.199.66 args=btx068vmojjoo/59-vmetg36ztpk/j8av0 /w0 l -jff bj
  - Log entry 76845: process curl pid=11882 uid=296 src=192.246.39.250 args=dwnklw8-pld3lk-hf4zqlkpu4d7ry0tx5vqqm-r0tjxc4s/w
  - Log entry 36975: process python3 pid=10946 uid=308 src=188.252.141.151 args=9yb2dfchkubdud42ps2cgvqn3m2c4twltdttvdtw8-o6aeyq
  - Log entry 89352: process wget pid=3692 uid=684 src=13.212.149.61 args=3571699ag1txzyrk4nc317ekgk-jotv2eo9h8314z9u4dw0t
  - Log entry 92661: process perl pid=27952 uid=425 src=154.141.184.40 args=dbj-bn42vrz l4808fgprys4f-cj3p9u0zmoce906vqz5z4u
  - Log entry 78128: process nc pid=26980 uid=342 src=119.214.162.175 args=99f-t8d2vn86j3o//g7 xpub3rihc6nm0xe3drnihjxvbe-3
  - Log entry 81167: process perl pid=11224 uid=941 src=155.236.133.165 args=41o75mjk1e9uyf560ms7rddsbc0tor1hv5l-tdlhqjw0u/du
  - Log entry 88500: process wget pid=21280 uid=266 src=145.2.55.149 args=vxxtow2lk/zvhm1rhkqw68m9lyzxoqj2ivme8zfxktk1spu3

## Supplementary Technical Detail — Section 61

Automated correlation engine identified 44 related events in the 6-hour window.
Baseline traffic on port 54409: 2 connections per hour.
Observed traffic on port 4444: 87 connections during the incident window.
Statistical anomaly score: 0.853 (threshold 0.750).
Related CVE: CVE-2026-22614 — not yet patched on 18 internal hosts.
Affected subnet: 10.0.5.0/24 — 7 hosts in scope.
EDR telemetry: 4 alerts suppressed; 2 false positives removed.
  - Log entry 99917: process wget pid=1106 uid=268 src=135.141.0.80 args=rdqazn5 sdeh53y vzeuufoxg 0/f3dlzjcafijck652ob6-
  - Log entry 41315: process perl pid=14302 uid=948 src=219.32.187.44 args=e61vev9fbqlngwate3 w1t2w3vmn9/89fskblcqdaki/8yjc
  - Log entry 19170: process wget pid=1230 uid=107 src=222.238.168.144 args=kdkk8ibcy75xwziv-liv-nwixs2naz88-v/w0g jgqtpts27
  - Log entry 10886: process ruby pid=7406 uid=432 src=212.222.88.140 args=oc58wjyfyssuvvqu/k- ou6y03jrkrz7412kbqbzn33ew6a6
  - Log entry 31180: process wget pid=3408 uid=713 src=39.46.153.215 args=n202dz3dnxrw-0/ydeqv4jv6ilo/fiwpxpcp2z7xjdsllbgm
  - Log entry 39791: process curl pid=16903 uid=535 src=176.108.210.184 args=iofhtvsd04vt3rhojxogbr81obba-zu2hdgsg0i g7pd6j-q
  - Log entry 68275: process socat pid=19950 uid=81 src=61.21.127.197 args=21 011ir02gyypi-fw6n68e tu/mfc5klcw a/7p8b1fdn5v
  - Log entry 74247: process nc pid=3094 uid=19 src=46.107.43.193 args=hzc9yinl6rfah8sesws3ramnc-aw-f2lyiof8wp3-yrot0j5
  - Log entry 72498: process sshd pid=24825 uid=204 src=81.72.40.93 args=9hrg2jfcco4 8u6avg/ie6s36ooe9wsqw 1m937un-f vpol
  - Log entry 68566: process socat pid=16257 uid=474 src=135.164.31.240 args=c/jpump5knx91-g42l/x-5-wd33hos9hven-/7r2d/0j75cu
  - Log entry 46949: process sshd pid=27740 uid=442 src=75.115.238.144 args=t104bpy7yg18rd fneo36t9kik2tpvb avf9r1h69nxyjn7s
  - Log entry 64339: process sshd pid=17620 uid=653 src=72.220.115.34 args=53q gqpj-l5vwopp3y8feyxo9wg-9bouwi-5qwjf uh8ayqm
  - Log entry 42581: process curl pid=12143 uid=228 src=37.110.191.84 args= g-q-r3vx2-cc6-9a v7a1-qst65 kgd8yqwjoxa9obyn7zm
  - Log entry 53233: process perl pid=27598 uid=601 src=38.7.6.125 args=ex0e4-hmpcvo7j3vxpkn-/nkltiy/ av3zaz6vr85767qx-v
  - Log entry 75128: process ruby pid=24835 uid=218 src=176.78.205.85 args=2jdvxjhzwqcqe0w2iny4uhbsws1ka353-3tc4hhy4bvqd4kv
  - Log entry 30490: process perl pid=17468 uid=218 src=122.182.8.178 args=t9gp2wgciwdcvgvss9ymb06btfil45z-g0cw279l9di5h n5
  - Log entry 26085: process socat pid=21236 uid=444 src=41.88.254.12 args=pz7/hvx dzr3k5zoeilrymbfu08z6rm//z-3nuzi1h9ufoa1
  - Log entry 51138: process python3 pid=13768 uid=980 src=108.226.239.208 args=ni2gb36vjgxaan884btwyjak4c/41rp/8j27pd5b0h8d2r e
  - Log entry 85416: process nc pid=26243 uid=847 src=176.95.150.119 args=a61egne/j8pnwx 21k4z9qdmoriin5lifdo0zgev 39fuo4e
  - Log entry 94322: process sshd pid=29155 uid=196 src=104.197.79.114 args=f dq6/l20uy6z95 nrtxp3ck81mkhwlugu3v-v13jp57 l6w
  - Log entry 15327: process perl pid=5216 uid=262 src=156.175.140.205 args=9yv408eihudgo1p1n2 ghtoi4 ylcg83vfc-rjqm8hfeq73n
  - Log entry 74436: process curl pid=12480 uid=765 src=89.84.217.7 args=s4s8pvmt4pa046ka7firkes 0we/j1  o364ch61nkxckkn 
  - Log entry 63150: process curl pid=21344 uid=852 src=19.217.213.3 args=9iil3w0c1t-elp84x40nytn0dkmyxqogiulx7-549ijcgued
  - Log entry 32914: process sshd pid=6073 uid=393 src=170.165.61.126 args=m7j7ey08jjtwa1rcsojc3xc98xfeoli9-ex 7nt/gepk7j14
  - Log entry 67502: process bash pid=30937 uid=714 src=187.33.92.245 args=i/gqr x0s1yiqg/14ou34qi0cxprkci0 m5s91w-198cqblf
  - Log entry 91378: process wget pid=16637 uid=712 src=11.195.24.234 args=t45uylhuc5bt4mlsxt9o zpl-1l8x1xg3/qwcc -647rwlly
  - Log entry 65842: process bash pid=3033 uid=109 src=181.10.171.84 args=iuff70iam6onbw i8p4l2ejjt99m8br9vdm3tgp1eh30u4fv
  - Log entry 21404: process python3 pid=31861 uid=835 src=146.105.167.209 args=/jntyqjagwhy8e921yg0kztps48c8ozcm6vv9k2z5j66pnrb
  - Log entry 87835: process nc pid=27159 uid=255 src=118.79.160.93 args=rk9k 0ot58ru14h2cvy ncnnir p/65m7cwwks35pbm9er67
  - Log entry 32701: process sshd pid=29316 uid=662 src=49.218.29.147 args=-jm1vtmzxaq0b8/mjm8kow/mlbyw/0fsaan4 7p 3t5u62ha
  - Log entry 34094: process nc pid=26908 uid=888 src=34.81.205.24 args=g7ewu205g7b65as4w--edzctu8984vi1amrj52296lp5-tp 
  - Log entry 43795: process curl pid=22141 uid=998 src=44.140.239.214 args=dgoi2s2jizxrc3tzqifvws4- ezf/6l4n/gef19kw/d/y5ws
  - Log entry 66377: process python3 pid=8960 uid=307 src=11.151.224.234 args=g-160otp7dehrxusgdd4x685xv5gm adwyiad a7/zbkd/hj
  - Log entry 90467: process perl pid=1683 uid=712 src=43.241.18.111 args=/2sp0kfc8mcbaezrw  yr6nh7to/i45dc/s-uohnqa8wgmwy
  - Log entry 99263: process bash pid=4867 uid=881 src=9.40.57.65 args=kf4x4xa72nm4bktfiwbmqsyfh7rf3sem3lpd1eu7fgyi1pfd
  - Log entry 64639: process python3 pid=8374 uid=817 src=212.191.225.138 args=jko2ixud1a/b-xuf1aesjlu3x45c8axq7l3zk 1i2g6q26-r
  - Log entry 67628: process nc pid=25158 uid=960 src=132.192.154.52 args=x18qzjc9yy9sx4he eqt-e/tlib 6eradr3m6n95cvlh9vjn
  - Log entry 43932: process wget pid=26573 uid=163 src=53.198.139.71 args=us8gxtr-ao2hkuu8skfrdp6hxw/u8r6f rvxv5tt376pi9a-
  - Log entry 64348: process socat pid=4095 uid=923 src=61.127.20.126 args=j-fhjp6vff0indqblko7xtkrf731b8av9wqgf /fip/ a3tc
  - Log entry 14874: process socat pid=20901 uid=438 src=137.79.116.100 args= gckdynmldtkoelhunx14klbwm2rmdm8w-qhiyq7e-vg4/46
  - Log entry 90560: process sshd pid=29998 uid=188 src=220.122.0.30 args=33 ze/oz89xbbskx dq-5ddv2o-pfgh4xap59qqp7ltfw42w
  - Log entry 55890: process bash pid=10389 uid=931 src=35.112.153.242 args=46hsxd7g7m4v4kfejtno3lx/ny-hweh96arga6blwcpls3 c
  - Log entry 80984: process curl pid=2465 uid=192 src=180.3.201.99 args=2p 87mxpin 6yj5me0xfefdz4/3k1rxnsczkdq6p9tmj 9u7
  - Log entry 28153: process perl pid=16104 uid=231 src=212.170.5.173 args=brh6j66l9olsnlwpejrpmnmkn-cv4/k52nzby2483zgsajl-
  - Log entry 10520: process python3 pid=24444 uid=654 src=179.139.202.2 args=edgmoemfx8z1v9959g3jwbb0ab010fs62827/-qtaoz8-i15
  - Log entry 47266: process socat pid=10108 uid=607 src=210.244.55.143 args=utqezab-xwoi-b3zp6utcjvr-i 97nh235/m6b1udhhva2h-
  - Log entry 18906: process wget pid=10105 uid=402 src=75.70.154.200 args=nf-4-ttl8 /i2qq7wz7gkhi4axqqc4x4dv8vh1txjvuiqlos
  - Log entry 37733: process nc pid=16234 uid=543 src=5.229.130.76 args=a8e48yvi46xobo5pgcjl10n-7d2capz8dymq-ppha64y7hmd
  - Log entry 30230: process curl pid=7899 uid=77 src=201.145.190.44 args=htu5cwum6lh4475ou3xfo3mjig/s6tz6c30zir6udd4duuom
  - Log entry 28919: process perl pid=9513 uid=206 src=129.216.142.77 args=umx3lbvbwhyq6ktrdcsq-or2a6edj3 tk0f75gmege0o-9p-
  - Log entry 32151: process socat pid=28038 uid=443 src=99.29.95.129 args=8-7yavk0s3h2unztq9eem/tg0v05kwhai0qzeu25b3zwr40m
  - Log entry 53804: process python3 pid=20983 uid=481 src=149.193.159.204 args=036vx6/cpryne69bw/kmcbwu6wd9zuyl06y15714ld-r89r5
  - Log entry 73956: process bash pid=10675 uid=89 src=25.221.88.22 args=6in9bardwyju6 n1d5y6w3/7clfinvg3wz1syf0w20tu-9ky
  - Log entry 66836: process socat pid=14640 uid=655 src=147.3.193.18 args=35tdhs9y18n64mplvaaysfq9l78l1rurcpqkl-f5r-3jmueu
  - Log entry 52388: process curl pid=18573 uid=51 src=152.15.125.204 args=ex/vckc/bq4r778tvxjz8vi69o-aitl0l-sbhzf9id39cm83
  - Log entry 63154: process ruby pid=5511 uid=279 src=40.165.83.14 args=2nflo4bjfhr1mp4jvkulv79 25-8htre4ndo/-e5/taf9x6l
  - Log entry 78182: process nc pid=6084 uid=604 src=189.95.52.107 args=9yhbriw oxa-w2pp6uohnepd869kejw-jjy5ej1v9j8w5/xu
  - Log entry 47708: process wget pid=2216 uid=707 src=186.85.4.6 args=2m5094u1fve6 rh7acm6zz5ko15wu841nss2d8kqxssuu0if
  - Log entry 17896: process python3 pid=20544 uid=735 src=214.181.77.186 args=b  gnq426jgdvvatjfanztf/h6u5u-hakvou9rqq0qbs55jw
  - Log entry 25537: process wget pid=18788 uid=815 src=53.185.88.21 args=70q-xervz3uy7/exqgvwiv23k8j7sy1r/7pjrkhn8db07b/5

## Supplementary Technical Detail — Section 62

Automated correlation engine identified 28 related events in the 6-hour window.
Baseline traffic on port 29681: 0 connections per hour.
Observed traffic on port 4444: 185 connections during the incident window.
Statistical anomaly score: 0.807 (threshold 0.750).
Related CVE: CVE-2026-11303 — not yet patched on 5 internal hosts.
Affected subnet: 10.8.3.0/24 — 20 hosts in scope.
EDR telemetry: 4 alerts suppressed; 0 false positives removed.
  - Log entry 34120: process perl pid=9654 uid=708 src=80.194.243.45 args=cg/v/2w0v39j89kpk0b2agjgmbyksib5qtb3z3gpx-e6o/vr
  - Log entry 92046: process perl pid=24871 uid=757 src=125.225.33.250 args=dy nufh cudryrx972z-4bo/pfw/j/5ed0tzpzbtocety52k
  - Log entry 87699: process sshd pid=12008 uid=279 src=113.119.131.177 args=88x me 9y29s/aoeh5vl3s6 tbt  5my11w38v7gyl 4c735
  - Log entry 44490: process bash pid=25295 uid=565 src=187.223.120.133 args=vqqgv19zumzvva5yy0j-pq3ucc1 f7pfsv0tevmaiosggn4b
  - Log entry 54882: process bash pid=2803 uid=961 src=111.125.204.208 args=k70h64vycg8dmslcq0/ei39w1xsm1c71opst2hwtwgj9n5e0
  - Log entry 46093: process python3 pid=13694 uid=722 src=98.130.199.42 args=41-65653zi7w6swktrabqcs0n1c8 8gojdbj2 x41sur7zou
  - Log entry 19900: process sshd pid=21812 uid=639 src=221.114.17.83 args=r/43 ov333-nm7vpy9w72t3e21t cmdjfbdvid45p73s/wt1
  - Log entry 65903: process bash pid=1621 uid=676 src=130.218.13.206 args=ev0tnnzs3tcg-n7bulds7jzt9i4kl655kg9rk0zm0mfys5d5
  - Log entry 92934: process nc pid=3016 uid=442 src=86.189.33.63 args=m-vjqinz 9oq/umik6co02z9nr3 y8v-3 ywvf17hr2exb1e
  - Log entry 28727: process ruby pid=7259 uid=855 src=60.40.190.97 args=-6y5gj2/ 03b2jxw9rj3fht7vzzd243u r0kkvtgo8t/c de
  - Log entry 19779: process ruby pid=31491 uid=237 src=180.57.192.221 args=-rpik-xvvg-c8ewmy/iehud4e1jqrnb7v/260 n5j8p11wp-
  - Log entry 78809: process nc pid=11236 uid=894 src=212.201.101.126 args=azzf2x9cba5/ppk aoksi4-lhmdsp27tt2qrfv2b9a/v9cxx
  - Log entry 93936: process bash pid=18960 uid=863 src=219.249.182.125 args=6pi-bkbc/44c81v3js2pd7ys3rn0tmhnf tnyzvilf6 7-qx
  - Log entry 75023: process sshd pid=30430 uid=627 src=220.221.166.153 args=91iao-cgl9w2mtn7810upb7mc3glp5o69877bbknb2cwjxp1
  - Log entry 72783: process socat pid=2981 uid=451 src=143.231.189.126 args=38zm1ird 0kl7/mktfe4dugul r8ecoxwqx0 t0u2w182mes
  - Log entry 14004: process ruby pid=4671 uid=985 src=150.128.148.153 args=pdqapu ul6cmjsggdhcvf4qir1z594txl/jx6r06vsiathes
  - Log entry 42046: process socat pid=16809 uid=346 src=182.102.111.1 args=cysgvjd-pie8suq4a33osz1kcvnslvdn0p83z r0/i1f1n2k
  - Log entry 98036: process nc pid=3690 uid=281 src=194.199.45.13 args=qarlrt6zgy20dhrc2nymvfbdqoyp1iz-219fh7cg3/ri/eg3
  - Log entry 16602: process ruby pid=23998 uid=479 src=90.143.102.134 args=tyr2mlcq  khi5g40 rs9bfvq1qces0v53/-tt1bxtxjqoxx
  - Log entry 51044: process bash pid=19811 uid=326 src=9.80.177.29 args=f33n368nh61n2mwpeuwckodu/rossz-r0s7kyfmb52--zkn 
  - Log entry 25029: process nc pid=13187 uid=680 src=2.10.58.40 args=kfcj4-bpzkoxhxks1heuf4ai/cj82jgyx83t-5 gfqkbtwtr
  - Log entry 43977: process ruby pid=6887 uid=289 src=141.65.57.211 args=wczw8 oseidrqv3x24d5o5e5jawgzs9u88xj2qjr7dsvyjy2
  - Log entry 19905: process ruby pid=20056 uid=451 src=128.83.217.137 args=wjwinz4qqno6qmdrlp/011485a8gr10k4x3q 05uoptsznxw
  - Log entry 13245: process curl pid=6646 uid=600 src=144.23.75.135 args=elquw4-bdsuvlqrx98ucqm5/9ellhhnapacgxeims-go2hsf
  - Log entry 11560: process curl pid=25732 uid=535 src=194.248.23.141 args=ql46k5c3gs82kfs jvepf2pq39s7 i7f5uqh-mztfa9d21gs
  - Log entry 80958: process nc pid=29666 uid=852 src=68.163.199.105 args=/njdlges3z0a22o0dmauh73z3mq6527mbydlbcv-55-7 04e
  - Log entry 73281: process sshd pid=19309 uid=267 src=123.206.44.160 args=a8rmll4eh /jpku1vms69 4ivj-02olv6pocb12/2kdbufcz
  - Log entry 76873: process ruby pid=29705 uid=345 src=27.148.15.28 args=j4y1h31u9do o9v4rzfjps/mqxnh5 1wvqniraryk2-7y17p
  - Log entry 61982: process bash pid=19135 uid=632 src=186.58.79.68 args=-slp3yjx89a/dwmg4a/-ya3no2pos5u3i/-ukhj-yjxftz0d
  - Log entry 97512: process curl pid=15354 uid=505 src=221.11.203.249 args=ok1zdns- 0qfzpulku2pat0ss4uhpuvx2w/zost1297jlnq-
  - Log entry 38873: process sshd pid=23409 uid=430 src=14.95.198.235 args=4gb-y7nri099mhfco1eubximbowj1738w12hsyrejyl60esg
  - Log entry 93675: process sshd pid=20723 uid=371 src=180.150.27.63 args=9vb1gaj22lvbeys0pg2psgw fxskj8pjb8-imafyhh9e-0jr
  - Log entry 95761: process bash pid=23161 uid=809 src=139.69.23.114 args=ns09fsm y3joj7kmfp4jr9xewekad7ujwh0c0mh9/b-yl1cr
  - Log entry 97109: process bash pid=20413 uid=932 src=176.186.105.115 args=56-klaa8c/mbog0wi2j98ucr95qywcglpn8olut-6x/lkq5z
  - Log entry 77074: process nc pid=13853 uid=973 src=37.239.186.29 args=bbdqtleq/crl9kaeiublnt/260gy8vz/cnt8 lq45a  jc0k
  - Log entry 50759: process wget pid=28267 uid=431 src=201.212.96.145 args=1i/72a/wua9c3lo2s-5sv459oqfhl3n48w0l9mr/upgmw hh
  - Log entry 96432: process nc pid=1893 uid=186 src=90.184.87.39 args=ervv01xnr5djlu wm1d7/3kokweiqwx1-65l8ukq2ujna8eq
  - Log entry 17726: process socat pid=7828 uid=660 src=31.214.158.100 args=88j7r6k8ny/1booalin upl3s/1k4lgw0 npy5c6o lxqr2q
  - Log entry 35743: process socat pid=24847 uid=275 src=181.161.140.30 args=1rct5z8cb43sxh3urox55bugqv0aii4w1bs-wvos1s/um3xx
  - Log entry 57214: process sshd pid=23921 uid=170 src=120.226.155.185 args=qs0816o47 kzm4jpt bx8qa02d nmt0ueq3z4-2 v01i2pg/
  - Log entry 69819: process curl pid=1324 uid=526 src=27.195.157.138 args=rygki899i-0ah9 ai5p3 k56fkrctge53k0814lguoextpe7
  - Log entry 65963: process python3 pid=30387 uid=84 src=112.188.254.116 args= c734ogchnkr2iij5n5bi/3w84myhmxsrai8fir5aanatsmf
  - Log entry 10067: process nc pid=8434 uid=340 src=141.43.11.80 args=4l7/6tt7ja/18sn4pdrwnzqeh31kie900mprt73myekcmpc8
  - Log entry 19381: process perl pid=19924 uid=744 src=122.149.39.102 args=u7iiu/wpm0arlecgk/md/xpdz3lp4h/6kfi44er1ex/yiszy
  - Log entry 12290: process python3 pid=5566 uid=689 src=206.145.230.137 args=24esza06o2jaziwyzyvdk7nwlz5huww5vei6/n25askd06rb
  - Log entry 15358: process wget pid=20023 uid=440 src=112.147.78.191 args=cc9451j2g mu1yjfwygrtrmys6p ft4xxdn s945mnh5/e72
  - Log entry 55070: process wget pid=28206 uid=745 src=149.41.84.120 args=smi8vrx8w3imp6kfixc3pfdv9b7o446m0 /8cpm657aluuvr
  - Log entry 75392: process wget pid=25713 uid=415 src=161.64.51.185 args=h0zxyahftdju pys0dav31v3tapv49li6q1/3naq-7t16d/4
  - Log entry 85661: process nc pid=24230 uid=549 src=5.193.200.198 args=h/mwzgt4u9672ggh5ewqngold9ciu4t1gu 54d by3q/wlhh
  - Log entry 98916: process bash pid=19952 uid=660 src=135.140.63.210 args=cpvp3bexo53fwun0 ahnw8un762wr6qqd7-klfkas9z6bvnh
  - Log entry 81514: process ruby pid=22640 uid=255 src=79.67.4.137 args=ay85drpx8x1bb6snmccms5yk3t2sm onhmgq0cqj9-s1b45q
  - Log entry 83901: process nc pid=17440 uid=660 src=160.97.102.71 args=3lj6z7lq5easpy/w-33  uw13mw298vygo4g 17qd6umlt-m
  - Log entry 16648: process wget pid=11558 uid=821 src=200.115.65.153 args=-v/1 z/8x5uas6wzp53vq od4etes6//wy82qtuam 0es3ez
  - Log entry 18711: process wget pid=26217 uid=372 src=13.219.180.227 args=a eh3u2qgydl6sf 8k1woib5  4 fhvz7hefor06jse45k6e
  - Log entry 25596: process sshd pid=6028 uid=679 src=216.34.9.174 args=xkkb8yhflgwljq/76spsf9/yx4y6i3qm1a13b6dur2keau3a
  - Log entry 66377: process socat pid=12152 uid=946 src=159.59.208.42 args=o7qi5x34mwjajvw41loqc/pdvmphlaod8y4rvh-4496wf-av
  - Log entry 24273: process curl pid=31198 uid=190 src=151.181.205.32 args=4r20mt5no2khxi8p3zcwwveg4/ds3m lxvvw0amt 9k s/x3
  - Log entry 37160: process python3 pid=21610 uid=552 src=103.166.249.67 args=uh0ou94u8opyo/fcnb4mhvvsu4rjgj7ted35-my/7twx4e7h
  - Log entry 31646: process sshd pid=4860 uid=797 src=196.168.188.163 args=n3y2-u5kn767ib8e6s75fz oz-i/-2i0v2ndz3ncglfkzohx
  - Log entry 55032: process bash pid=16141 uid=682 src=119.5.79.223 args=3zmh5fvis w-/cy0e9 1tjksmc3mfpuylkch/-913dpf0ii/

## Supplementary Technical Detail — Section 63

Automated correlation engine identified 47 related events in the 6-hour window.
Baseline traffic on port 17563: 1 connections per hour.
Observed traffic on port 4444: 110 connections during the incident window.
Statistical anomaly score: 0.802 (threshold 0.750).
Related CVE: CVE-2026-11381 — not yet patched on 9 internal hosts.
Affected subnet: 10.4.0.0/24 — 4 hosts in scope.
EDR telemetry: 3 alerts suppressed; 0 false positives removed.
  - Log entry 93428: process wget pid=26270 uid=438 src=170.45.40.93 args=iwy9bx3s6unfubqm1f3o/30n4amn-dbz0/v3d479795nz7yd
  - Log entry 63077: process perl pid=31880 uid=1 src=109.172.239.227 args=rf8ihcg wjja rhvkayp643owma3q5tu04jwpz0f6hq5xhnj
  - Log entry 54021: process socat pid=3439 uid=881 src=139.43.65.153 args=hv29d hi/0sj70nbn2i13arj2 zxwynxglj8ilxbhzp7-nft
  - Log entry 23780: process wget pid=24892 uid=941 src=54.235.199.20 args=bc1peznx33t39l7k4udsdne2wfx8zp23d634km-nhpohw5w 
  - Log entry 20320: process sshd pid=31025 uid=510 src=8.241.110.58 args=q5hb05ftpiioar8y13h 34slj6yoxbqww-bq9sm2tvd-nv-x
  - Log entry 62539: process perl pid=14673 uid=393 src=40.239.228.31 args=4d0c67ixuvhi6l-8hpaeuz9xozc6c3hjamaoxixxh15b63 a
  - Log entry 47580: process ruby pid=6462 uid=454 src=198.90.104.232 args=ivten69k/y0y32q1k-l2j4f04q4hub5jj2n7tri1vualnobe
  - Log entry 33037: process sshd pid=30867 uid=599 src=214.105.73.172 args=cq-phb6tci5sgtnecugy-42s77n-eneuy09kx5am5t6pdpuu
  - Log entry 40244: process perl pid=19455 uid=14 src=175.220.241.138 args=86kutpektxjvhwn5hu82f c6szjc4ckj1djtyz/wxw3mh8jy
  - Log entry 22550: process bash pid=2814 uid=386 src=98.249.234.73 args=ava30r-6xeqgu1q4akx1my/6npjs6agi 9zlh1e0z7wa0udw
  - Log entry 23571: process curl pid=29076 uid=698 src=60.178.73.61 args=5wq af1 yng-binhwg9e18y tql7rlk63fauos9zu2k5/ sr
  - Log entry 83361: process bash pid=4646 uid=299 src=106.156.73.152 args=qs3hw4j00cpthzqzlygh/ruhpx-06pjwitcurj9hh922xkxi
  - Log entry 36428: process wget pid=20435 uid=160 src=23.220.80.128 args=9sb ctg97uuejg-fg jma9j2bcv1v24a8k4tnobdkbsqi58v
  - Log entry 98398: process socat pid=8833 uid=792 src=14.170.21.238 args=k5l/ 6940pgyum0u6xi178c8e3w5ljaponig0wdh-pjonq19
  - Log entry 61279: process ruby pid=4491 uid=184 src=203.186.5.231 args=ogui7iybxrwk953dotiu89ekb0smulsjw25hus3k y8fhv24
  - Log entry 56628: process bash pid=14917 uid=493 src=117.84.11.211 args=1ruqe89zb5kr e8iiquukc6dcy/mvo3sipfeom21k3pexapz
  - Log entry 51902: process socat pid=28381 uid=171 src=141.146.28.80 args=8fz2imj0d1pntthfg2v2xdddwds2ioj7grchp-7krz2eckfi
  - Log entry 71615: process ruby pid=18840 uid=171 src=119.51.88.129 args=-h/ou206zs4zgtiws /h khzed6xd3wqwgsol5q58hqkk-qu
  - Log entry 26759: process curl pid=18321 uid=869 src=221.214.70.60 args=34q uxp-9/qki6hilm8znh xh g xu79j2wjwebe5ddz/n h
  - Log entry 64961: process python3 pid=21733 uid=559 src=83.234.81.60 args=5/oyxlyxnyk-xgxe5v093mp16rk0qk41lfxfk2-9t7xvqy41
  - Log entry 98378: process sshd pid=26335 uid=768 src=141.197.117.72 args=j6ojmdcft0zdlwqzfyo2vunpb///b63zt3u9t3ncylsaycz1
  - Log entry 29587: process perl pid=8414 uid=109 src=161.221.66.186 args=vlpikx481cqpke9g19rmk0lr-v79 u39cy1ai h4x3ml7cxi
  - Log entry 84589: process wget pid=15865 uid=302 src=30.25.160.209 args=r4ray1/u6x4-vwm152j35isw1qe7yqppm9d0 4dwpdtiu006
  - Log entry 88322: process socat pid=13687 uid=392 src=159.174.173.204 args=5yewcj6aw71q81bg1-oyl2qr/qztn9e49a1aw/5431/l5h6s
  - Log entry 78229: process wget pid=18539 uid=789 src=60.194.32.151 args=d9ak6hwb3jf93rbugcgh1kak7fue6-drshzpe5g6f-4higmf
  - Log entry 73462: process nc pid=15611 uid=839 src=135.166.94.205 args=j64-q3opectbtdx59irywt98dg75chjbqbfaswzdbeur1g4a
  - Log entry 93176: process nc pid=20330 uid=136 src=63.60.161.10 args=fb2ipi814wxzs85sewdtl1sp2k0yybzjg8j65y-89-uh9pl0
  - Log entry 39507: process socat pid=1072 uid=888 src=152.58.206.157 args=4xaej2gcpjiewjnxf78t42fj reky6 0z9pnvkc3mwo9mp-o
  - Log entry 57466: process nc pid=10462 uid=904 src=140.169.238.136 args=2sd7-lca9r cu-qp2v2r4vhz4f8-lr0e5wkbyy0f--ggaqtb
  - Log entry 39708: process nc pid=7067 uid=594 src=71.17.224.84 args=8s6augsk-/-i0wsq8/7-io0-eixc4uc4snde4k2lw4dmc46v
  - Log entry 24024: process curl pid=10379 uid=591 src=136.17.230.242 args=edfk7f-myo6f3gijq1bh0cu5c3tshqey27n3 flofa3iq-t/
  - Log entry 52004: process socat pid=23557 uid=244 src=1.27.70.74 args=n6j7q4r5pt1ssj8 houtzusn4urcs kq t2kzw1n5pze9q94
  - Log entry 11441: process sshd pid=6731 uid=439 src=80.6.32.154 args=1jedu8/pel1s581g31ikk8xw56sunanb8/b-jwz64 wu06bu
  - Log entry 88222: process ruby pid=29851 uid=132 src=196.222.6.231 args=n cxnjd2ff/d2vjuy wlq1ti54qvcjzka02eok7d81a/5jcy
  - Log entry 86740: process nc pid=19446 uid=409 src=92.118.233.76 args=sz3s8gskrtob5kd9xqfueck0qkl-fpbv1d8ek2m9idoxn2em
  - Log entry 18553: process nc pid=2975 uid=119 src=181.29.141.105 args=hx1ba9/qo6k1pyn--fk6g0m24gc3lerzr5t-8ohmllzydwqy
  - Log entry 17814: process perl pid=31711 uid=70 src=52.75.77.249 args=9m5/1imsslx2yoc7z52/d106e jqzoy/dxahh62jg30udw8-
  - Log entry 55311: process curl pid=15081 uid=879 src=87.76.197.25 args=k4185lgxs/liha-cz83gtux87xm-9h bktei254et5so/y7g
  - Log entry 56330: process ruby pid=23539 uid=241 src=73.76.49.234 args=4j1i/29119bcwxft vnqgsmyoqv1y0jydx5ee74ser7m6p5a
  - Log entry 66795: process curl pid=7696 uid=539 src=166.218.70.24 args=gal6ki2u9m495e3rq/-mc-v0n7z d-n4q-nphfc8s3tr59v-
  - Log entry 70120: process socat pid=20956 uid=117 src=172.228.213.152 args=6/1l48d438qukbe75207 tdvl39xm/a3zomxiu5oe /2pc1y
  - Log entry 66265: process ruby pid=3605 uid=139 src=94.135.239.186 args=q1qcdns3iatqnbsvdlc7n 0/ju4h-a/584lfm906bnsnt30o
  - Log entry 34354: process ruby pid=12156 uid=626 src=3.178.206.186 args=-rjt/u3c id83ykubtp9j7v1gu219pfd/kqoofhqf6qvijuj
  - Log entry 51384: process nc pid=20263 uid=895 src=99.8.235.209 args=y24ca0fp9y6t2g-3oscqn2rosn08n01yd4znoy7/7y lczu5
  - Log entry 36438: process curl pid=22296 uid=979 src=29.191.160.142 args=f1ur0vxpvd/ggks 6094efkaw68hw0ivyjtozarairkf2d3x
  - Log entry 98822: process curl pid=26277 uid=430 src=135.10.43.88 args=obv/vcahm/m9r4c8-zyh57a ton9xjia9r3//wf2eac79x74
  - Log entry 53809: process curl pid=31616 uid=606 src=213.136.103.21 args=2bnxb84oi -ctzmdp em6ppkaalr-dkpcvrkjk-6 d8roqq/
  - Log entry 72404: process python3 pid=27843 uid=739 src=139.148.238.84 args=f/rj/-ecq8/846bv0zgw0snxc-ob9o8n14l0dd 82s213w3w
  - Log entry 54351: process wget pid=19644 uid=928 src=125.48.191.72 args=l3sphtk108lijlp7pu6cvsf8v3rbywi-6haphzi/-jrh7z/-
  - Log entry 99057: process sshd pid=9701 uid=79 src=26.9.36.191 args=8m330q8jz 120p81daxmvnxosoib7447xkv/ez4djra0uqcc
  - Log entry 26606: process sshd pid=26559 uid=550 src=189.222.227.218 args= 03ykgximo94/rcurd5zwo4en5k60uobv3wj849u5nplcsa9
  - Log entry 93234: process python3 pid=24575 uid=825 src=85.47.52.53 args=7ih2v2bs1tdm7ype90ni-43kd763myd/eahz1noomvty00a0
  - Log entry 81833: process sshd pid=8909 uid=182 src=14.46.26.205 args=ze5ku1gjlg/lbganbkqm4lea43/0g4bh5bjj-mmv1laww5os
  - Log entry 29474: process perl pid=7325 uid=702 src=103.246.131.92 args=/ 046wss4cqplm0djfwes-un0logxgggzsitspb4h3vdgh23
  - Log entry 55189: process nc pid=2512 uid=72 src=2.111.222.232 args=vt/gcdbx4t4xs07m18-u0q9/p1f/tx-b0 vjxx36aqg5ledl
  - Log entry 27860: process bash pid=14967 uid=102 src=158.44.174.177 args=br9/egta6enkm2oydy9og0e6y3dc0 9cw2j67lig60rd0ei4
  - Log entry 18051: process nc pid=3992 uid=565 src=135.255.47.112 args=f71-kzewafol3535mverwvoqlfxh75hrr4e2umyt-3akizot
  - Log entry 15533: process curl pid=11908 uid=912 src=115.247.25.246 args=n9p2-xkv2ib0ydnzi5q2kgpb8u y48z72cn4m2j4hy -l7x/
  - Log entry 40231: process socat pid=29427 uid=488 src=14.98.13.213 args=-a5/zqa0bgqgq282v73x-biipkiq4hi8alpml049bdaasnbq
  - Log entry 61268: process perl pid=27069 uid=616 src=145.206.82.42 args=7sygpzdmnko67i-milbw7kxmgivitdtp8rtza7-dmaqe4v42

## Supplementary Technical Detail — Section 64

Automated correlation engine identified 34 related events in the 6-hour window.
Baseline traffic on port 28357: 3 connections per hour.
Observed traffic on port 4444: 177 connections during the incident window.
Statistical anomaly score: 0.938 (threshold 0.750).
Related CVE: CVE-2026-24268 — not yet patched on 5 internal hosts.
Affected subnet: 10.9.1.0/24 — 17 hosts in scope.
EDR telemetry: 5 alerts suppressed; 0 false positives removed.
  - Log entry 89881: process ruby pid=15319 uid=20 src=200.80.167.150 args=ezx7pe-da/t3n9azh9h-fjqv/3-v3qfet75qbg207jbsg o-
  - Log entry 36118: process socat pid=4973 uid=289 src=92.79.248.75 args=xxo9n4d72vlp/-x/5topsbba5gu1g5/qgx596l5b1oy3 y1w
  - Log entry 80340: process curl pid=24439 uid=424 src=58.82.247.164 args=qoq/wfije10pbqz7 u18uhv1hepjfmhow73hwzvu95zgj4jk
  - Log entry 54909: process curl pid=21412 uid=133 src=178.198.231.211 args=kea4dx2fkresqjj/80kx5u3zi-h/olzp0sng5 xmoybsim/5
  - Log entry 32445: process curl pid=31926 uid=417 src=79.5.224.239 args=w0i4yyxxxk9uvcsc30oey8hq7-nl/k7kxvmctoqcd74i-znx
  - Log entry 74908: process ruby pid=20297 uid=657 src=142.116.203.27 args=t nh0em7tle5j3-mvg-x2-dkwr 59jeg0n tpz1n9kcg9fpp
  - Log entry 87244: process sshd pid=1206 uid=968 src=11.63.196.124 args=3wkcrt-/ mf33zsah62 5zakhn9lgkt7t2pnibo/ob3w1dz9
  - Log entry 39223: process python3 pid=22404 uid=773 src=95.39.73.160 args=2p5gukrp2wf6zvydmq7p8y9jymu9og0spiy4iki7nb 13i07
  - Log entry 97169: process socat pid=22894 uid=804 src=77.43.178.73 args=yetq00dw8zrumfdmm lik3 an1t3qe/85epau2dh/lz1mcr/
  - Log entry 77601: process curl pid=20364 uid=979 src=48.31.183.171 args=hum7w4ks4bs6utx6o// 190ai3aolqvl3/5x2lzhr8oz80mb
  - Log entry 78331: process nc pid=15738 uid=147 src=9.210.40.149 args=7424lxwkld52jgxh-i5get5bdeqkh-m-1/x7t19r/5g 4b1v
  - Log entry 46780: process bash pid=8443 uid=716 src=1.59.166.141 args=h-/hc90jrlgf6b7 ey8-qz5porcn9cspoexof333ycrseb7u
  - Log entry 52609: process ruby pid=7622 uid=423 src=180.253.48.4 args=9pzzw8h3ev46zbooyqigx uuqxi3rviaxhika2wo/yigr2l4
  - Log entry 18221: process bash pid=3110 uid=907 src=72.232.76.162 args=h7kk7ax9ky04b-gp44pblfhngnenlgqwsd5ervsa4rj8u8e0
  - Log entry 82876: process ruby pid=13674 uid=761 src=25.214.204.230 args=2dvk1wf8b2/ekkc9nq13ofdhk4qml70nl/g7jelp/6c8ug1l
  - Log entry 22901: process socat pid=21174 uid=764 src=146.238.65.190 args=7dq7z1 6yuy6rag/2oimo-xcw1 cslvjbn3eh1lz5 gy6n9q
  - Log entry 25541: process nc pid=5429 uid=543 src=41.179.59.7 args=3jw4evnw09ykl u9se2ik4faitl6791zm2fsc3ome0daov/9
  - Log entry 97928: process sshd pid=26121 uid=6 src=171.87.101.41 args=/d80c8i8ppr0x1w/xrd-35 t6qyvib179y3kpg6v2ttursnd
  - Log entry 70482: process wget pid=3631 uid=597 src=43.172.20.198 args=oc9ghdu7j8skn34-tujddia35wuxcegho47yibaw1agsiofd
  - Log entry 93682: process perl pid=15119 uid=379 src=92.8.60.18 args=ftma c847m-hemw45wf58u-yk4rf928l-irggm5t-b 7/b-5
  - Log entry 46293: process socat pid=1533 uid=651 src=209.181.250.162 args=e-85gaxy3p3v36inh6bfnos7iddqreoxejd8pr 16wo7y gt
  - Log entry 66462: process python3 pid=14080 uid=966 src=48.240.100.123 args=-ppg3f1t/ft6qiyk776qx wj47 peyn7k/2fm78uw3c-cv6i
  - Log entry 47018: process ruby pid=1200 uid=35 src=36.245.106.126 args= nbtjq6f4a2ea8g57y795otmh18risbrkqvj77-4nwswoz4m
  - Log entry 49323: process python3 pid=2570 uid=619 src=191.57.186.232 args=p4bsra4u6z/hwzylohg7/dazqmd8ciai3ppxp8-etbc11u/d
  - Log entry 67285: process perl pid=24130 uid=153 src=133.151.152.183 args=6rw996vz4m--bm06pzih02frexv-f ucrnov0kagf4gmqq6e
  - Log entry 73828: process nc pid=15310 uid=854 src=31.151.254.217 args=jk0kn0cxw-elb2m-hwk9goa0iydhom-016e7ozojyd-1x9-t
  - Log entry 46201: process wget pid=16910 uid=492 src=149.186.49.85 args=hbs u26ps1dtmmeny9f-g9bxm-5xbyt2io2y482 xe-lpnx9
  - Log entry 59628: process wget pid=1574 uid=25 src=32.106.232.60 args=8pimwl3h8cenm5nnnxxq6lp/njc97rzyhpc0jzfgcnd95net
  - Log entry 95878: process curl pid=30554 uid=371 src=48.208.83.212 args=69o5/ks9pptwousq9kcd-q0h9vp77v-s 0nkgyxj0s8d79t7
  - Log entry 88312: process sshd pid=10202 uid=204 src=220.150.244.222 args=hxe7471l 20lu-9j20bppu4qabzlguuhecv3po/r6witg2v8
  - Log entry 45338: process bash pid=15368 uid=997 src=12.180.156.151 args=9/n6mp8cm 32f/j9xx zr2/x/70 83ib8awx-xm1lkrxsc u
  - Log entry 11091: process socat pid=27217 uid=474 src=9.116.113.16 args=7 qm/ax1398vlmfe96u-tmpca86o5iouw1kvvquv389dgdcf
  - Log entry 31929: process ruby pid=2947 uid=432 src=206.103.190.140 args=q-bxgv6-d25jalv5pmkrkiotjo51mtlqn habz/jczuy-0rm
  - Log entry 92281: process bash pid=20891 uid=886 src=175.152.111.172 args=t7russpwu hdy8k h/gptdrakxa b06-1cqyqi8b4qzo-3d5
  - Log entry 33837: process nc pid=27179 uid=405 src=216.20.170.184 args=15d77cv4lt7-5ec61s -/4dxkdsgvwwrp0xuj19iy4wba-ed
  - Log entry 75319: process wget pid=31296 uid=355 src=167.68.174.162 args=8wzq-ig8aekek7zkh/7ymui8856 6u1zn8gis5c5yc nh26/
  - Log entry 81046: process perl pid=6213 uid=949 src=127.50.246.202 args=h 9o-84l0smp 86l5z6p4erh7xz24zj69t2x0e2z hg58-jd
  - Log entry 15080: process bash pid=9885 uid=756 src=134.147.117.230 args=ykjv29bpz38qa4crm17klof17vbvel5h-0k3wn/q1ykjlykx
  - Log entry 83925: process ruby pid=1428 uid=918 src=141.26.183.182 args=tfcd7x 7i8v5ai9qy9tn92a336swxl/ugdfda2rijktckko9
  - Log entry 73867: process python3 pid=29671 uid=987 src=33.218.231.2 args=5fbzgtumrjo9sa2swmejdje/52nkmjhr3iw/z5qy lz8s qa
  - Log entry 95850: process python3 pid=16316 uid=53 src=97.222.185.63 args=vcxrm j112by3yv39tfpu9ac730fk 9e whfy05lqudxqkha
  - Log entry 17190: process nc pid=8117 uid=359 src=31.177.215.19 args=hqbqge4umm307kgjx/7-1-d1btw72/okqb/7u21c0hf4q/5k
  - Log entry 16967: process bash pid=29189 uid=206 src=201.136.142.213 args=by3t-n5qc4um4pp5nceeyua-i4muledmbo8 ho -i/cuehux
  - Log entry 23692: process python3 pid=14817 uid=284 src=193.22.70.127 args=wbvt6dy1vsn7lk299a3punh6v7qpmv1o1py9x2u9v8tfmcx9
  - Log entry 90744: process nc pid=13660 uid=400 src=176.60.235.143 args=3bsanzfk/2a  tj2dfzwi-7q 0n83twy/3xlibfkwkq-cufv
  - Log entry 39974: process socat pid=13476 uid=380 src=43.234.100.75 args=/co1wbl rhz97 c-9lb3-pxrir8j5n7v372yf-6oehdavfsc
  - Log entry 12650: process nc pid=8899 uid=37 src=64.144.130.11 args=/wtu425ikrem6thjm 5l5tl1o bacl6a17nih9xcttq v2 d
  - Log entry 47095: process curl pid=15787 uid=479 src=183.159.133.156 args=j8s8aytsgwrkkcwy2cv/mjbeeg53izpqg3yys cbq887ymbm
  - Log entry 54025: process curl pid=1991 uid=888 src=136.124.34.13 args=7xdb1d29gdg0a 3515btjpr5z5ga ist17lzkf6mufac/ae9
  - Log entry 78719: process sshd pid=13926 uid=391 src=214.227.19.108 args=ve tjo85436p0fo5dtgmze-7saacjwxdc5mgv502pit8ic78
  - Log entry 96127: process sshd pid=15372 uid=618 src=169.83.132.179 args=r8mn c06/rw2eusrzyhwex4kp9vf15qrts0rt18ne9uw4-y2
  - Log entry 26038: process perl pid=31559 uid=685 src=120.70.245.138 args=4ybe75or6zfxogvu8uor6-powfy5yqhm0pbszed-54hq0fs4
  - Log entry 73014: process python3 pid=28280 uid=240 src=66.3.69.214 args=jf-bhl-nfaf1 tecbyvxrff3nwfkwxnr/c-rcd6-l2j-jofw
  - Log entry 79849: process sshd pid=21551 uid=531 src=28.254.4.197 args=t5eo1334gsvadtym8tpkxbq1rqe0iwgpgj/jymh0y1n3d4gc
  - Log entry 33335: process bash pid=30793 uid=183 src=216.4.100.203 args=q31tyvxoffo-g mvv-qz2vh6k4/mtcxkdmww2a3b00pdcdxz
  - Log entry 22480: process sshd pid=14440 uid=356 src=140.112.215.218 args=rz8oiu6rom0ktixslym6l-fstdctt8ygwzo77un 4zeg7r03
  - Log entry 54849: process nc pid=7463 uid=963 src=22.116.160.252 args=s9v pvh3b3wf/c-gg-/oikbwbzz9mw3x21pjo0mlh6moi7dq
  - Log entry 88517: process ruby pid=7107 uid=884 src=200.249.222.75 args=xmg6zavyvw6w0v3vxjgxuin1 j6o706wy1vzalrlk0mykcau
  - Log entry 66625: process perl pid=18974 uid=735 src=159.241.112.141 args=94v/zb3agv/lrd1rj-1p-35bexgsjuvwma6zas7lhscpm 73
  - Log entry 74720: process socat pid=24142 uid=851 src=139.243.122.40 args=6an2ix54esazrrf9wtvh-2u/bi8g5xbmig1/axj85s4bw64e

## Supplementary Technical Detail — Section 65

Automated correlation engine identified 21 related events in the 6-hour window.
Baseline traffic on port 48147: 3 connections per hour.
Observed traffic on port 4444: 102 connections during the incident window.
Statistical anomaly score: 0.854 (threshold 0.750).
Related CVE: CVE-2026-13935 — not yet patched on 7 internal hosts.
Affected subnet: 10.1.4.0/24 — 2 hosts in scope.
EDR telemetry: 0 alerts suppressed; 3 false positives removed.
  - Log entry 66237: process socat pid=9798 uid=824 src=198.101.253.163 args=tm8vdd81fwoqjm1t3u98rl2o6llciu2yo3es lvmwhi7act6
  - Log entry 98829: process sshd pid=13606 uid=666 src=52.165.170.120 args=4ju2k1-6u7gvrb5b7jvqc6jux1hlgwc5-vzmo5x/8ybkshbd
  - Log entry 29633: process sshd pid=3728 uid=693 src=206.125.207.128 args=s0p3vritjjheo4e/ytq1hrf9875shudv6xv65 vumncoj9wa
  - Log entry 42352: process sshd pid=8666 uid=896 src=46.110.179.172 args=i9g1ezkak4t w y3zxh-8waze245d2h6hw0/2/-nd070a6zn
  - Log entry 50194: process socat pid=18649 uid=256 src=155.50.77.21 args=gmuah0onbux5zlg2byrn8hln09 he5kks8ydjh0chtm08b4m
  - Log entry 21772: process wget pid=5115 uid=507 src=78.64.64.7 args=2993jt0wr968j/kf4n/rru8 6rh820u9n4/k68uj-xnjr2yi
  - Log entry 97854: process socat pid=9497 uid=470 src=175.198.113.128 args=ksbx  bjma5t1arnwqcoojcvf-4ogkhlw32tddrt/38ase7j
  - Log entry 24866: process python3 pid=4104 uid=994 src=5.251.179.197 args=08qi56v8sr4/5w4cintg2ganrfvhha826uml0f/yuiohspi3
  - Log entry 28590: process wget pid=8232 uid=247 src=61.138.112.245 args=jrg57qvuaky4ce/6hl-m2kcj7leke2anyl1a16 ni6had0xp
  - Log entry 48271: process nc pid=27624 uid=600 src=222.137.181.117 args=yuljuc8t3p1hkmu5expf-0w/r35b/orya904gmapalrbjs07
  - Log entry 29690: process python3 pid=1395 uid=882 src=70.183.213.125 args=/adu8hxl8gls/u7ahtmb5cx2316n9k0z7gxwap476m6g0cg9
  - Log entry 59303: process bash pid=2850 uid=790 src=48.9.216.247 args=tckzbt3kwu7vyrha3cirgpmh/gf0cczem6co/fzae1kf6 ju
  - Log entry 59752: process perl pid=4819 uid=206 src=115.134.165.155 args= zhftwm 02erb7jn8-fa a9duqibk7xudhsf-dq1dq5el9ed
  - Log entry 74893: process curl pid=31342 uid=896 src=75.113.9.177 args=1ifrkh- xox-p4gp78ofaq 3drm 2jgo3m k3-h7nfpwc43v
  - Log entry 45005: process python3 pid=8224 uid=589 src=86.101.104.34 args=c2icg8uiw ppn03192pfjwurl ypst7qe9ma85xclrk/tpy2
  - Log entry 28663: process perl pid=16333 uid=320 src=60.139.131.177 args=x fmb9tj83a7nxxudtew-3q2 m3k9/lonb6hppnmnjvluqih
  - Log entry 73144: process ruby pid=11102 uid=95 src=16.242.236.157 args=uosl0tyxj4comzqiv0hp/4b79gi12qnlpqw/lulkvnh14sm8
  - Log entry 88156: process sshd pid=21131 uid=712 src=148.128.126.46 args=seyjbn6u2j4aw2av9xndmtjbtl2z5/ws2okn7tcob98br877
  - Log entry 17196: process python3 pid=7110 uid=859 src=69.234.114.79 args=5-- ckmwbn9-4ter4c3zhek4c54ynpb9atgvbkjqhfbi/w g
  - Log entry 59753: process nc pid=3680 uid=237 src=195.176.48.122 args=e0it4q8ghwhzca-g9lz-8b33ky1tu6r3/del4b4j6rca4k2h
  - Log entry 36257: process curl pid=26781 uid=227 src=129.9.106.29 args=i4/4fart 6h-wn jrq-3cbffh/0dvsn3408- ih95o57rfll
  - Log entry 82681: process curl pid=4958 uid=679 src=159.243.189.80 args=/29llni77w8ysx069uwxojrfwp1aj0c3if57-/gmdpq05rym
  - Log entry 58788: process sshd pid=20899 uid=893 src=181.129.167.83 args=gvfnt35vl3h5bu2sp1-s72q3/04 5 1kc 1wzn6m7sulhurr
  - Log entry 81344: process curl pid=2393 uid=528 src=60.125.234.156 args=2oobv0rv82srl5l0698h7c9bmof2qnt20789o-aynmjn3dde
  - Log entry 73934: process perl pid=13507 uid=125 src=127.84.72.86 args=n4 sxl6y4ma944k4yeqwfh8ac 0/3pxb-gu6nlv13m1lmx31
  - Log entry 98995: process python3 pid=13816 uid=138 src=99.248.222.71 args=1noxp5ob5b2h2aff4q4qgwvba5asfmgkx72nt13i2oq4hcm8
  - Log entry 74194: process nc pid=16244 uid=134 src=40.252.146.229 args=0482a1gabygvr03boa 9ypu9j10bsiep62kxap4vwnpvzlhg
  - Log entry 24580: process sshd pid=13274 uid=479 src=16.213.145.26 args=73pg91q4/i/o0/adn1yqzposc/3rcjx27 ix/gba5-34qiyf
  - Log entry 43873: process curl pid=9994 uid=805 src=50.94.156.145 args=vnchv974g8m30kv5odjwucalxmzzf2l 9uob8g8si4ycmf0y
  - Log entry 89815: process nc pid=29553 uid=11 src=184.73.176.65 args=/w4v-rz47d6qu /91fajawpisuf-5/6wc10v971u9ejrlwpb
  - Log entry 24662: process nc pid=3066 uid=721 src=151.219.30.206 args=j9kdd243y8dwuji29ef1pl3jp62g6c9pk9oi20dzv8q8hr43
  - Log entry 38334: process perl pid=22532 uid=735 src=220.232.93.196 args=au0gvpu9wekr j9djp1zd/f50qhgdrekzjhk0anuid-ql6--
  - Log entry 61447: process curl pid=5054 uid=619 src=150.107.161.40 args=9 y /er4g /9h/f-2v-hdlrlbgmumm12lb0hh49grn9-nagz
  - Log entry 51924: process ruby pid=27255 uid=340 src=51.21.84.111 args=8bboo9r9lye qzz4k2sthdbk-bdgkasjjvtc0mlkkq7ufzzn
  - Log entry 15321: process nc pid=18804 uid=904 src=76.54.61.48 args=i12ax8bjqa431veiw680o-5ng6w7ls2bv dhpf9s0753otbe
  - Log entry 97028: process perl pid=29732 uid=750 src=172.26.203.198 args=imlv 0ms4ua6d3m2tbay011rt3c/2mxco41jn n7eum2iwwv
  - Log entry 99531: process curl pid=4646 uid=894 src=23.99.206.35 args=47q2v/s9lm2pj-67ija2kqabk2/8f1samahwx5ep843h2w9v
  - Log entry 38973: process bash pid=7218 uid=245 src=35.113.36.38 args= 40ylbo5exd494771hfczdkgnm zv15j4dms ycbhgoj6afi
  - Log entry 24887: process perl pid=17902 uid=856 src=117.238.153.223 args=iiytav7llajph3uc /tlgr54qlon4jz8m09 em6sjaafd861
  - Log entry 73006: process curl pid=9904 uid=787 src=180.27.241.21 args=aev0oajpep c/91iv2nf5q3lbkdjudfw3vq48t9i3oj450k3
  - Log entry 15706: process python3 pid=13426 uid=296 src=88.208.251.60 args= 1muzb1416o19t- hparu7acv7t-9/k6-nxqtm0lsh3zf/cm
  - Log entry 47968: process wget pid=21029 uid=489 src=104.253.131.175 args=tm3k8zsdiginj2l1/9og9rdy 6/ll1fefswla-jq13031ubb
  - Log entry 91823: process wget pid=23305 uid=954 src=12.106.88.56 args=xaldpmdxvmbayetapn2-en 069hgp1cl6er1k2/0u23tjph6
  - Log entry 54094: process ruby pid=10950 uid=592 src=126.30.238.70 args=um3v9g9t1dyh9ft4a01vs4ldig3 he3b-3t3cosaexwqhec0
  - Log entry 76283: process nc pid=24648 uid=944 src=213.166.129.182 args=y7/1u7-aju1nztig8ue674svhe4j8gvv si/yhqh/4no5wah
  - Log entry 37435: process perl pid=9147 uid=497 src=82.33.11.11 args=bbt2s0bditigucy7h 5yo2p-gm/bbhmg/99jjq2noyzm-0yt
  - Log entry 77206: process ruby pid=20747 uid=694 src=178.227.68.132 args=f0i2zfuz4r8b6mrmcytlojoubmvl9pmn8-/5o3u0q2 hx cm
  - Log entry 17258: process nc pid=9501 uid=517 src=32.151.237.43 args=m2g-ebgpt4p34e46 1tgjt6cyovxzq/lsgchym0f3z hnmpf
  - Log entry 35608: process socat pid=4733 uid=545 src=168.99.25.52 args=ls779/4/rccxdg67gx4pmfj7/937z7db/ypd2ilz00udug11
  - Log entry 10621: process socat pid=1934 uid=910 src=27.71.179.230 args=tel14ljdh1fl0xoeadu48-e2aprrsanfr96m7qhhlvnrr78 
  - Log entry 31082: process bash pid=29132 uid=549 src=202.0.140.100 args=a8keyjj0dz/5vp8zqwprr7ma035ylzzhr126qk69gonutu9c
  - Log entry 82969: process nc pid=6391 uid=269 src=101.162.193.250 args=7 1 0/0bmelkmh7exvfhm0bt461k3te0a/-b61-4z8/2luf3
  - Log entry 81295: process python3 pid=4454 uid=692 src=64.29.119.22 args=8/9pypzhe3vzuv q q/vt80tk6wac89tgi05uj4btxyhl1al
  - Log entry 34634: process socat pid=22658 uid=302 src=118.54.10.141 args=48y9oemdv4bh1avjby2y0jda00q9sm1m-cgpjn4kj2guqqfw
  - Log entry 66751: process sshd pid=10574 uid=799 src=99.252.84.246 args=z74n48u 1fjruwzkax7tf2q3phy2co49mihzo2ow7eul 9cc
  - Log entry 85011: process socat pid=5212 uid=506 src=199.111.214.71 args=vctc5z3n7w99dbhi/u3/uprgsvhoae -h3ek/s29qwhclma1
  - Log entry 43967: process nc pid=13591 uid=618 src=140.20.54.69 args=3j6ys127etffy58o7tm0f39191z59y5akgcl4b8istx0o3w9
  - Log entry 61358: process sshd pid=20619 uid=456 src=33.246.58.135 args=8uh83odtnwzuw rnuf5d1bjdgtc8sc5i--ptlj39ntxwk  q
  - Log entry 64166: process python3 pid=16363 uid=367 src=13.31.38.100 args=e1-07ku9je lp-6x2froqc6jdoes9rx4ewu77kz0/weal2fx
  - Log entry 32702: process bash pid=19982 uid=120 src=20.110.135.220 args=dm4e/v62y7/jiv7ub7096cavn ewszf0nrgeugk/6chhl ma

## Supplementary Technical Detail — Section 66

Automated correlation engine identified 19 related events in the 6-hour window.
Baseline traffic on port 10311: 2 connections per hour.
Observed traffic on port 4444: 148 connections during the incident window.
Statistical anomaly score: 0.948 (threshold 0.750).
Related CVE: CVE-2026-17172 — not yet patched on 13 internal hosts.
Affected subnet: 10.0.3.0/24 — 10 hosts in scope.
EDR telemetry: 1 alerts suppressed; 1 false positives removed.
  - Log entry 38888: process nc pid=9223 uid=261 src=27.151.113.116 args=mkz95t-6plvswoc26i50kg4escm8ve7mz d6a89c9ch-6y4n
  - Log entry 87284: process bash pid=31917 uid=989 src=164.39.65.226 args=8zn6gpabtbgg8dkge/ t8n plxs so8l wbrvm 9iql8/6h2
  - Log entry 11431: process socat pid=3886 uid=329 src=81.244.17.154 args=f7ui8d1a4/1nc4n5ckz0y357ouu07c-653ak 76719t h9on
  - Log entry 63739: process sshd pid=28348 uid=676 src=46.173.205.107 args=-96mu2uuglh09xnpu3jhwinfy3-bt1fhgbedkcrf8v-bxx-b
  - Log entry 84003: process perl pid=10077 uid=579 src=149.111.104.153 args=4/-zos46 pep9zzx4ehpkwxd ci1cz1z/85x3nsj6xy9v5jr
  - Log entry 21787: process nc pid=25839 uid=724 src=168.248.117.106 args=4302nxz1xj33xhvuq342syvuo yupsgue0oqm12b7ele7j60
  - Log entry 72904: process sshd pid=10730 uid=874 src=10.128.30.58 args=o/w0hri1g2ut/ysm1jz5fik2qp1i04i85l tox6w-w2ouoyv
  - Log entry 14247: process python3 pid=11250 uid=133 src=49.55.24.102 args=4sk015kbnd6nsx0h-9b5bf/0t/rwm0efk2z3h0rjbfv-8kn/
  - Log entry 73309: process perl pid=5358 uid=610 src=115.127.248.81 args=hv-3sma7/1kywi5mxp9ud5sya87/e/1 gat506tafa2iudp2
  - Log entry 67803: process sshd pid=14241 uid=918 src=118.206.186.243 args=epq5tt2f1vv6g0w6oi-uf/nga2asj00 rqk8v0975uc4pn54
  - Log entry 49022: process socat pid=21678 uid=152 src=86.15.12.167 args=hhr7fa m0ark03amm738zovjg-m59eaos3v7k3fglkkzbdkw
  - Log entry 18764: process bash pid=11225 uid=188 src=138.143.190.167 args=-tuwygu5f9wr94m5lr4 oie7gjnjd42-ov-fam51-2xoyto 
  - Log entry 72085: process sshd pid=6490 uid=594 src=43.207.83.22 args=6jfc7y/5p0qm crepmkje8g 7ezwzzdalv914n5dcikt/zx/
  - Log entry 95347: process wget pid=5776 uid=317 src=163.114.13.196 args=9alzjfspejek1a2unmhoozkettj1-14kux2t0gckp45o1/w5
  - Log entry 30987: process python3 pid=13450 uid=923 src=83.153.120.239 args=v lz3npk3x7opd/p4ilvtxcxt2w16ttmvm8td1eqp tya/w8
  - Log entry 65524: process sshd pid=3633 uid=698 src=117.204.170.88 args=q55//z2pk6wdl9mt09n/fxcy/-48e1h84h q5du05 u6e3pc
  - Log entry 57513: process perl pid=2680 uid=339 src=189.195.40.64 args=9o-9a71qct7mvow 4hz5kogli7d579ta1g-50b12gud1ntss
  - Log entry 67163: process python3 pid=22842 uid=832 src=125.42.70.205 args=st2hx92j-zy-br31jta/4m64ubhjb5r5114roeyqxo1gfp3q
  - Log entry 83257: process nc pid=8947 uid=357 src=104.104.93.233 args=cxvj3e2kwxagu4s3l3o4r69vfsoviucl 7lhl0ozt5ipzsrx
  - Log entry 48977: process ruby pid=5631 uid=868 src=17.93.37.79 args=3-x4-q7799y91wa7gm3c3v2nwiw4vbv0m5r/0trbyhvw9cwr
  - Log entry 50990: process bash pid=22010 uid=364 src=115.17.77.133 args=bxaur2ol9djx4u1-d85pfj6 oqiahxrqs69mr x8cpdkkbo5
  - Log entry 56106: process sshd pid=4269 uid=744 src=97.174.204.29 args=3naugj4dttm450a-8/dy/f6nya8ns20m vr5-c00ij8-hlmx
  - Log entry 50659: process perl pid=18624 uid=928 src=38.145.139.128 args=w/lbk3c4zh9h4m62j827s2/u-4sk-dbwzdcm6b6hk/ 9fupb
  - Log entry 33132: process perl pid=6886 uid=561 src=36.60.84.212 args=1mb36qmz66n7bw 3np7emdgx-k20ruo0vb mygze9bm4micw
  - Log entry 67102: process wget pid=19485 uid=439 src=128.133.179.226 args=cx0lem4ryln4h9hblofn//d08bsxw1ujd6rgipa-w4-ui8ox
  - Log entry 94491: process wget pid=3439 uid=70 src=148.53.1.84 args=2m11tcvl4gjf7/viri-cs28va45lp-vu17/48qzd oqa035v
  - Log entry 95161: process ruby pid=3399 uid=751 src=214.179.142.87 args=ycek8vw6f jj6v658e580fu3xbeh4rb1m7d14i8n9032h35w
  - Log entry 89194: process sshd pid=30951 uid=937 src=67.156.161.119 args=zw1yy-t4v/39fs4si0d4okxx-ddtku0snu939afq9fcez-rp
  - Log entry 34022: process curl pid=9445 uid=492 src=54.125.49.110 args=ygne7k9vjuayptv9-ukcohedxb8x0ng/6/0boa5zub2r4tah
  - Log entry 33206: process bash pid=6427 uid=706 src=129.111.207.48 args=ngzg3acfaaykd5zvl2q0wwi 5tto0p//mcx6t02my1bd5jyw
  - Log entry 64510: process python3 pid=14573 uid=517 src=61.245.140.111 args=hp-5q9px i8jcs0twtth0frr8j262h  28vx-crwdirdj7p-
  - Log entry 33145: process nc pid=26861 uid=346 src=45.90.65.209 args=8kn4fd-7c2ty9ped th3f61j0116-cx71nxloy skzegn6p-
  - Log entry 27257: process curl pid=8973 uid=423 src=106.92.134.61 args=osnl56z/cl4wbs1wig oywxno1r9gx3j14vyrwetlz3dyk98
  - Log entry 19652: process nc pid=12632 uid=26 src=81.9.6.34 args=nr7jzm1mfj7czdi6i8- bei8-k7jf2bwy8xxz77gc7f0o6-z
  - Log entry 56136: process socat pid=17937 uid=665 src=187.255.155.32 args=b/86kvk5-pgdfqfd3vua0mkcbdqu4-6z/h1s9bhzg/sodu e
  - Log entry 52716: process python3 pid=11971 uid=233 src=114.135.11.39 args=axruu270 47l5bah2vd4e27bbmniwb0rg9gl8cql8vlloz08
  - Log entry 82964: process python3 pid=17725 uid=519 src=4.39.243.39 args=/17x xucyxbqu3hxuxlxdw20n1m4np4v69uehs2doglkv43w
  - Log entry 88515: process perl pid=5602 uid=739 src=99.94.13.94 args=mdqvlw3y0v6ryse0ee3pzpsc1v6qg/eskyrirtmqlpeom83z
  - Log entry 82332: process sshd pid=25466 uid=781 src=6.84.163.183 args=cehnkw8l7j-x 09prun8ro ojr44mfr//zkls7fgjj-bc0ac
  - Log entry 91010: process nc pid=3165 uid=61 src=151.87.193.241 args=xke8iy7vim2//xm53x2k5bc6p14l4qynzy/af0g-vhzdz2w-
  - Log entry 84295: process nc pid=22435 uid=440 src=57.0.160.95 args=e-wxvfjd32z54ft5zh9efm0iio5mtccho6 /c3toywgf0dj8
  - Log entry 26511: process curl pid=8736 uid=653 src=10.72.234.23 args=vhi6/o7kyj735-2ll3ff3875b16tlcxjafattu75z8461t6d
  - Log entry 68105: process nc pid=30148 uid=525 src=210.249.134.204 args=zdav0uhk2z/hm1cxs9n7gc/2s7v03q422 v8os62ny8l3g89
  - Log entry 89945: process socat pid=2613 uid=14 src=218.114.241.246 args=dmhfsw8gz48q6mlds77l59c31h9hd5hcilqvhdy2psvu -on
  - Log entry 45304: process wget pid=23186 uid=993 src=180.172.137.197 args=t7p7y9bka00c69bxpn-wacqpnluchimkyk ew9lpawdzbfmr
  - Log entry 95719: process python3 pid=20664 uid=932 src=119.162.223.42 args=/mngc89lrzneqp5d9pqqgjtozfocesgooo368c8r0jzrfeni
  - Log entry 68586: process nc pid=4857 uid=470 src=63.155.92.129 args=p 2bf431vn1u7d 74ip9dd43/72oaon0bol03-301ak0u 09
  - Log entry 80574: process ruby pid=19791 uid=362 src=78.55.195.91 args=o011in-7t3ct5ovk9nthfzc7 -/-xl771ekipmg3hzr0qo7y
  - Log entry 37620: process curl pid=25871 uid=641 src=74.147.187.181 args=jhtgwphsi56go5d lzypdaptis2vy1t5m4pth44my50h -yz
  - Log entry 88765: process python3 pid=4985 uid=903 src=57.141.237.9 args=eyn9uqb4bz 5sjwuus1ohhp4yeiu6zvppmxab60ky4m-ib6c
  - Log entry 82213: process ruby pid=9927 uid=616 src=141.26.69.183 args=fi4k5jxu77gv8razp9g5xep9awufqlyd e44dne7w9qj0a5o
  - Log entry 86437: process socat pid=8106 uid=353 src=138.102.64.87 args=4tplad mguezowd40jzm2gurnjd4jfdnrmopo8xtoejf3fbv
  - Log entry 23703: process nc pid=9265 uid=193 src=154.177.55.231 args=0h-g2wtd/pi/g1gh54hxrm0bgguure4uc4izbz973vpdaqut
  - Log entry 66310: process ruby pid=10750 uid=255 src=223.110.12.55 args=6fm0eoj6h3oc6wmzkhnkkdsf4t2u1q2mnd30y3j6v50axe8v
  - Log entry 32751: process bash pid=25874 uid=629 src=38.164.166.172 args=uvspd8o pao3 yw3adjg4 8k-lq3mw2juxe6-g-lm2 7milv
  - Log entry 54752: process sshd pid=1034 uid=905 src=42.235.222.85 args=p1a4f-9dz6z88wy/aetutv0f1-ephaqw7xkd0x59-yqv0zn6
  - Log entry 27982: process python3 pid=13894 uid=635 src=140.49.50.203 args=74mfjpmhziu2lh29wg3bwzf5zy-dnq26jtzxnb/ftqudrbzr
  - Log entry 97980: process sshd pid=29092 uid=839 src=18.109.31.224 args=sv7xgg394z tdc9/md8ail0d-mu7ufn1846p2/pg tujwbbp
  - Log entry 44102: process sshd pid=16079 uid=799 src=144.136.118.179 args= dpoih5ybf/5bk1bknihz9na2ougamgvm9timg9o cvsux9z
  - Log entry 23205: process bash pid=20085 uid=969 src=119.182.87.155 args=3s8 j/apujc17pv6ojwdscbjsql396e7xrjg7f9i7lmq1fna

## Supplementary Technical Detail — Section 67

Automated correlation engine identified 15 related events in the 6-hour window.
Baseline traffic on port 38471: 4 connections per hour.
Observed traffic on port 4444: 58 connections during the incident window.
Statistical anomaly score: 0.890 (threshold 0.750).
Related CVE: CVE-2026-31099 — not yet patched on 7 internal hosts.
Affected subnet: 10.0.2.0/24 — 21 hosts in scope.
EDR telemetry: 0 alerts suppressed; 0 false positives removed.
  - Log entry 88347: process nc pid=12900 uid=79 src=159.200.135.161 args=s6y1br95749kzba3lmehs6vrvrua9u2qi/6z2v2t06mp30bg
  - Log entry 92598: process sshd pid=17432 uid=584 src=26.200.222.121 args=riux4xl3zbc5e5w38 xmhm73/r1 rykdmzt/baqdvjngv xt
  - Log entry 27548: process sshd pid=21450 uid=108 src=10.253.59.184 args= 06gl1x7evrv6sr/1kdr9k26bhf9jxx6-9ey-jxrlc1qe5ie
  - Log entry 54286: process sshd pid=13607 uid=384 src=72.29.105.254 args=8 0lsqiqj3iwce o8tqhto6ux7pnv5j-lniyy1fh8umqwz3v
  - Log entry 60096: process ruby pid=31035 uid=52 src=197.162.186.122 args=rk9dexge613e/0-1p51 yl3p-/wbrusb0owrdno16i-72v7i
  - Log entry 58944: process sshd pid=26962 uid=613 src=121.145.204.210 args=5ep60q9ay627i6k6m1llkiui3-lnow7mw32xw/f03-t8rqur
  - Log entry 20299: process perl pid=29640 uid=963 src=121.10.35.172 args=9bhjj9o csixl2k/39x2ntp752lw1tcae7bc0rm-nsx64n 2
  - Log entry 63358: process socat pid=7562 uid=826 src=94.93.69.204 args=em8okevwj4pni73m/17s//ui582whl xeg6se2forh/natzb
  - Log entry 84059: process python3 pid=25958 uid=690 src=43.69.201.39 args=0j4xvbvemh3ypy8renqb3dv1if98tkwl79imxqw5cw81r/v-
  - Log entry 44269: process nc pid=9678 uid=899 src=133.207.138.198 args=2q2gpy8epuss/vf9oj5wcigilyer  we6r3cjpev pj5gdch
  - Log entry 45982: process ruby pid=8117 uid=146 src=16.60.89.168 args=xlg/e52 ij45odi6hhte1/ej9eqjztpj un84lkifx9f965/
  - Log entry 84094: process nc pid=4252 uid=673 src=208.114.48.80 args=yb7glruj5ud7-i2gxhbgp-fzv8h6b2x5vx3yy0/ltz3khi 1
  - Log entry 35046: process bash pid=5645 uid=394 src=56.6.240.49 args=kw0efgmmeqzmor/vlz8sycpfkppntobj5wty gc8a6eil7 1
  - Log entry 87763: process python3 pid=18673 uid=129 src=217.89.18.187 args=n0fy2hc6hiofw6swzkw3zpq16lw t2xvdbp27oj8e9qrthtw
  - Log entry 65474: process curl pid=18562 uid=480 src=86.83.244.161 args=3c1x7mj7s8sl0a-r2 u6jpi7730sikutq3n1ghfoc 5leywj
  - Log entry 81304: process sshd pid=5928 uid=377 src=12.196.139.179 args=t4ybfhq6 i6r t11-qb r6idi6ghvbk9iy4bep6tk9/nmj3m
  - Log entry 59146: process sshd pid=26261 uid=384 src=14.80.62.1 args=av2u2h 0-trvsk-7-/9lj-z7c63 tdsjt1ho688kr38dnhq8
  - Log entry 33845: process perl pid=27625 uid=229 src=175.195.242.20 args=pf7f8xzerat4yos9mx29hkzj-mlb9mpbr7fvfrw4ms51i6u4
  - Log entry 73755: process python3 pid=4706 uid=268 src=17.101.251.174 args=t 5785cuy-gjt32-1vja xrqfcqn3 98189/8lt8c2 6ipg5
  - Log entry 57082: process nc pid=31568 uid=550 src=56.17.60.80 args=kgsjijix1lv-gok 67 n2wms m7uuc5ek99l3pg036 s657o
  - Log entry 21030: process python3 pid=10506 uid=535 src=15.15.249.150 args=1k8o1r zgaaa1/f 5is63v6ha oe9os- -9fcxm3 v- 5myg
  - Log entry 79823: process socat pid=1330 uid=795 src=171.134.254.233 args=-sm5ob82qrpq30yn6qles-9u77xrvlkg299hegbqu9yymv2b
  - Log entry 34388: process bash pid=3773 uid=298 src=59.122.50.57 args=ccgx/jgl6y0t75itpg3o8wyvd7x0j4g2utoct9go rn/qu7v
  - Log entry 81961: process nc pid=10239 uid=150 src=212.255.136.4 args=86-x1u7otybm -z6ggqsy-hldf6zw4wp hjexnbcsft9lneu
  - Log entry 65770: process socat pid=3110 uid=461 src=76.173.142.117 args=6a5f sa81r1ucgxcnqhtm7rjyvb9iwh2iyehfv-357wmkk i
  - Log entry 56795: process perl pid=14103 uid=282 src=111.253.204.230 args=rj8wi bc5lsn8a6 b46e qodwft1x82yu6heaknkote-obnv
  - Log entry 75837: process wget pid=24968 uid=727 src=19.191.113.106 args=rz72za86mr50 a3byt-ixdo2raj3j1a74xg7ijgkrli24ro-
  - Log entry 65651: process bash pid=29559 uid=89 src=92.26.138.93 args=pdvnljywtg4a3b0l7daow-8eatoobypwkaa4h3f841817mm1
  - Log entry 73590: process sshd pid=14030 uid=780 src=124.27.31.14 args=30kr0/f- 8w109rkr3lww9-3iavufcdiiu4lxz-9wrkna0ca
  - Log entry 83022: process ruby pid=24776 uid=218 src=183.111.137.68 args=vqyoep7pnkyjicfgh7/va4g2vvjlqeq8w9-l5sg0vf1m/v1b
  - Log entry 59290: process python3 pid=1247 uid=431 src=63.246.82.69 args=7khprwbrd40/x0i5de7dhkuo/mxbl2lze- vvp23y6ba4z /
  - Log entry 24013: process curl pid=23101 uid=11 src=20.177.16.74 args=uvwgzt4w2rjr70k5yrnoszbdc6bf444ksix4/abc7eir-jfn
  - Log entry 61594: process python3 pid=27680 uid=45 src=10.240.220.228 args=qqphvv7a/91tyglaqflmz4ytuo0qi34ew h1qye4ta2ya1y7
  - Log entry 38936: process perl pid=20437 uid=139 src=10.60.189.221 args=-7fheeab9jx55kmtd2zltwoma1rl 6lehq6rtdv5bfir-u8b
  - Log entry 68789: process socat pid=27372 uid=74 src=106.150.34.77 args=jb671r0yjypwc3lo4y4r008-cbcvfywdm54-x 02x-7wn/85
  - Log entry 40345: process perl pid=17794 uid=675 src=56.15.66.114 args=041p5l98/qo7iecl67gxciqp9nf-t0zl/w/klyf1x6j-3gcb
  - Log entry 91997: process perl pid=10971 uid=848 src=56.169.216.10 args=xteylqhj8ylwhfnq1sybkpm0bu 34p7qjrdcna9znd5nox3u
  - Log entry 90020: process nc pid=8609 uid=231 src=16.177.216.26 args=1axtwhp0v8v3t49yf9i1hln8odbd599d-1bp7i9s109ik4ur
  - Log entry 83046: process nc pid=14377 uid=502 src=189.76.47.159 args=7e8yx73smduf8klajrl4or7/bo/tgde6euvrn 1xd2nej5gy
  - Log entry 16702: process nc pid=23532 uid=57 src=126.108.244.200 args=afcrvwymj-zmu3g22i1aqqpx7odcjql9gr7l/v36y x2 -d6
  - Log entry 45299: process sshd pid=29624 uid=92 src=173.168.1.153 args=frkz1-o523p48ulvxlw/f0sypmzfo2fzwaf-a2/t1j0nx43b
  - Log entry 46313: process socat pid=23216 uid=18 src=193.92.160.100 args=oo0pf61dn295l4zlaoaaankduw1e1x-8o09-ksf70a 64tmc
  - Log entry 42022: process socat pid=12098 uid=448 src=42.158.184.62 args=3vb5mb5gmml-2pgquh d0igrc1l-fxdy3aoths9k016xs1ir
  - Log entry 46634: process wget pid=16536 uid=410 src=185.231.52.176 args=gwoh0tip3nypwfxt8dm29/78lsn3h80mf uc0gtue82g4i7r
  - Log entry 57116: process ruby pid=21906 uid=241 src=204.220.120.228 args=c9x wnxm1celmsy0 s91tc8hjsf-gpmqt/8-9o xs173coux
  - Log entry 88112: process python3 pid=4750 uid=704 src=102.226.155.193 args=d75i2-yg72d-orl4-zp/9pbprt -jr9 l9/nzmscu34yggz6
  - Log entry 76363: process nc pid=15064 uid=967 src=122.110.253.39 args=tv314spzuc9 ow875ll211ew9cqo5rztjvglsw2v/x4p49vc
  - Log entry 43307: process python3 pid=28395 uid=412 src=193.135.230.192 args=s8vlv9jxdxj10-tb8pofugsq6baq zephhsuphuaak6pywlf
  - Log entry 59344: process ruby pid=10799 uid=755 src=158.47.130.188 args=daiiof5sc4pcmbh76ye0z6tv54zt787ewdmpxmpdf nkzxgc
  - Log entry 65448: process nc pid=13567 uid=194 src=179.23.235.174 args=-cheaj a/zadlcu2 54lpxygiuz8v-u9w15l08q277dsof2m
  - Log entry 25441: process wget pid=30539 uid=263 src=137.139.169.60 args=9s/8ka27eymp-ct9ips8g/po3yy3nkbm-noet2flj93/xdkx
  - Log entry 69869: process nc pid=23330 uid=343 src=142.55.217.92 args=u-s-z9xa8k3s97or9/fpe-i4ghm651wpb4-4himkgfq47omn
  - Log entry 66871: process perl pid=25049 uid=239 src=185.221.77.153 args=k-4ru9ehrs8z0bwan-mkiph15atz55egk645tmwxwr-otm/o
  - Log entry 68376: process bash pid=20554 uid=260 src=57.121.48.167 args=xoh5g29 t7j70k4mz-/f07jms9ne/8uc/w4ng3vhq-pj/loi
  - Log entry 99347: process curl pid=19210 uid=624 src=200.113.91.44 args=rcwe4xqu0koluvj-2a-iih81zo7vwxmgv8z2znf6khpr0-jt
  - Log entry 59580: process bash pid=14366 uid=960 src=172.1.192.93 args=s7pq0fb3udeefau6emmf8tsbqx3h2lk-1m7ri7x8s-zte-xm
  - Log entry 64571: process sshd pid=30241 uid=850 src=158.253.106.123 args=3woo/rpq1t9eqdm8mpurplosg0/23djnlq6ck-h-zkqw78rt
  - Log entry 23506: process nc pid=9803 uid=69 src=184.9.209.232 args=k6yqbiug zl rvn6-10cz k-iz5rot50n4de/pihvyqw2enp
  - Log entry 16345: process nc pid=16803 uid=447 src=187.191.101.200 args=luc4ellxqgbhnb6vgssef31q54x0-jbmn/dqyswlv1/965cc
  - Log entry 86023: process sshd pid=22058 uid=108 src=190.209.220.148 args=b5dlq lxld68oxv/t nblxptp/7x0c/7kz34csxl7- -hi3m

## Supplementary Technical Detail — Section 68

Automated correlation engine identified 3 related events in the 6-hour window.
Baseline traffic on port 38726: 3 connections per hour.
Observed traffic on port 4444: 185 connections during the incident window.
Statistical anomaly score: 0.849 (threshold 0.750).
Related CVE: CVE-2026-18271 — not yet patched on 14 internal hosts.
Affected subnet: 10.9.5.0/24 — 26 hosts in scope.
EDR telemetry: 1 alerts suppressed; 2 false positives removed.
  - Log entry 47308: process python3 pid=3193 uid=78 src=48.230.88.147 args=h06vf5snb1vvcdo5uaf59pc-umyztcn7-7t9nx sdf6gjtk9
  - Log entry 28783: process wget pid=10801 uid=897 src=64.37.222.245 args=e3ax672frj-dsd i8pq1na-dka9a43--oj v9ro47htfag1q
  - Log entry 41830: process bash pid=1873 uid=192 src=49.95.13.106 args=-x9laps6jovjlth ylzx3pjh0pp-r8ef7 p0e df7q-7s12p
  - Log entry 35184: process sshd pid=28218 uid=122 src=199.109.31.156 args=j i8dw5syqqjdl0r7/gj9vr4xrcunwubfqwo2n03rhsp7n n
  - Log entry 35371: process wget pid=8207 uid=762 src=24.48.52.135 args=h/wihsbwi/oter/w83yperqd8 up/hw-wim/m4c585wt824z
  - Log entry 60768: process perl pid=13810 uid=849 src=85.215.121.214 args=nm0m4392tsdpz9w y1bolnl3chh323oq-kjvi-flndi b3/a
  - Log entry 74632: process sshd pid=22443 uid=155 src=15.104.13.199 args=zuj2 ec7mpc-pe99s2g6snkwbhylyaubbrlkb0b3oxhx026z
  - Log entry 43195: process curl pid=22955 uid=55 src=38.88.133.236 args=21g91kqzm30080q-9 9rz17rm/2lkgpgrfmxk-i0zs 7duvh
  - Log entry 15759: process python3 pid=12438 uid=913 src=31.90.61.221 args=n7xdckbd0qyp/6nwq5/8fe6bvkcn8 c441iw-m3au5wald i
  - Log entry 72321: process python3 pid=30347 uid=239 src=14.56.133.189 args=sfpfbm5emgus2liguzlpti84 / 11w/-cdwed/stior-k1sj
  - Log entry 51467: process nc pid=8300 uid=924 src=45.97.167.33 args=m41lcs3wbsf5-3597qormnk/ras5ko0c7ws4usztv pkbu d
  - Log entry 77065: process sshd pid=3856 uid=809 src=153.140.174.97 args=h5-81cmbw65w/t8e1cdp twggjfgibc1kwo1rq04nyad7x4u
  - Log entry 36948: process sshd pid=17455 uid=191 src=71.91.108.222 args=rend-cyxxftnl5/0isgmrdwcf--8mp3ukgc-6ur7bk2ylqfl
  - Log entry 28007: process curl pid=14378 uid=43 src=20.141.122.97 args=kvs 2y1 l-tk8b/oze8gwmp5alng/q5g3jd8l hlbv/pjo-g
  - Log entry 21864: process ruby pid=9539 uid=638 src=210.224.12.138 args=6 /duezo0gjbduu66t--/utw8v4 hv/nl92vjlc8dz-8-tfa
  - Log entry 17478: process ruby pid=28139 uid=324 src=143.173.160.139 args=95 2bkup91lzq4-i0pisyh-ixg2qk6nvnwkhuhq-rmp709xu
  - Log entry 72287: process python3 pid=2891 uid=135 src=190.132.119.138 args=7y/sp1rc5g2mo6ae046msdx2tev-tvdnrrzral2/ks7hsek4
  - Log entry 87283: process socat pid=20195 uid=954 src=215.243.109.68 args=rz7q28b67e24f1pyj5wy//3/4q4w6ph u/k6vdo65vurf0y7
  - Log entry 48130: process curl pid=22381 uid=531 src=116.156.38.171 args=1 6v0i55avoa78/ eezwb8vsp0go6p9qbynfhxvprchx7pdn
  - Log entry 40505: process socat pid=4770 uid=138 src=71.154.219.131 args=b398zm5y1g2wt87w0wfkl35eo- ojloe/tpj-aj30fqzkkuq
  - Log entry 96234: process wget pid=15654 uid=947 src=119.61.24.102 args=b126mwbm0ug/gckuyr2ypvcjjf9s8obh8cbf9zrd5nw yjg7
  - Log entry 21662: process ruby pid=10950 uid=89 src=23.11.62.130 args=ax1tm lcx d5gmt8y0nnv3yztajy-1t75k fdiuf8phpvv1d
  - Log entry 10967: process nc pid=26363 uid=285 src=56.64.217.15 args=u8t7ebvaustwwhdhenaojglf6 isbwrtmkvlu67t2y2 5 q0
  - Log entry 65518: process ruby pid=1115 uid=29 src=113.49.112.103 args=/x5npv553mf3u0y/pfu54svzw7//yslutd4jy9l7wyefe6xe
  - Log entry 61293: process ruby pid=18523 uid=873 src=215.153.227.84 args=snj0bm25idv21llohfumutstyoddt7vi/xak809dzubn8isp
  - Log entry 56899: process ruby pid=11725 uid=98 src=158.57.67.172 args=vty0cpgroyxkzl9v7m01lueh-sp/zs 2ribv9v-7hxtofblt
  - Log entry 72275: process curl pid=2663 uid=437 src=136.233.199.180 args=zb9t36bj5xp9i8kzcy6mtr7ij09uzo7i74x8o6ion/b3n7m4
  - Log entry 49405: process sshd pid=27575 uid=173 src=101.248.44.156 args=nfg922ikm-uytr9pa4ku5ob 24soed4c vy6h7pcdsme0hrd
  - Log entry 34662: process nc pid=7403 uid=205 src=165.216.241.135 args=2d0ws/s1xhf8rtyfky1bq95g07te0j0c/va74nn9gqdi8kz9
  - Log entry 69703: process perl pid=11462 uid=486 src=39.195.159.92 args=b5-5s0 a3wq/gxtfnjgo57tp05xwe743ae/-onu7ob-7m406
  - Log entry 42244: process perl pid=15396 uid=145 src=27.38.7.115 args=e4oxig5m izoto42ytpfxqyjcox5 gr/vfe2yjjxqp52hrhv
  - Log entry 83175: process sshd pid=14831 uid=963 src=205.136.101.94 args=bdl9mwu56o3gcyy8ah/vclbdnh3ubjc7ru2gxxrr h/1mm-n
  - Log entry 19379: process bash pid=24563 uid=97 src=60.233.124.73 args=kyia87soyc-pk3agod fouhucf5dc3u-d7mybg69wljyeeff
  - Log entry 52358: process bash pid=14206 uid=287 src=167.55.235.120 args=jt14rz 24axh70k96pc8aw27x6/-q/c-xoch8mi93nq1ziwr
  - Log entry 19946: process ruby pid=6848 uid=859 src=10.161.73.51 args=uf-anxaz-9fu9p3h83/8jisthqz5iuyve7ue-1bkp7mbp 95
  - Log entry 83821: process perl pid=28913 uid=851 src=114.110.177.56 args=nom-/8k2ecya5yseyol0ju6xiccy clwmaxy1t1noeps3-7-
  - Log entry 90081: process bash pid=28139 uid=671 src=114.190.5.82 args= dlmsx6kb-91jt/qtlt 4dlt33l85ipml0/t8s7s35 323fw
  - Log entry 62135: process socat pid=20719 uid=538 src=11.1.189.239 args=r-biru 3-jp47izjnas7ppyqdeuwyi/9q0sz4dw 11z1fe-m
  - Log entry 93889: process socat pid=14216 uid=152 src=203.193.193.28 args=6d5mp01r/uqekklblh00keh558hnhnd0/bekumg6un 23elq
  - Log entry 87062: process bash pid=13286 uid=925 src=122.38.128.100 args=kuecgoci7k6xpbd-kg5o-asw5k4sbkytfv1ivvh8tcjim8qm
  - Log entry 67529: process perl pid=3812 uid=912 src=215.69.76.215 args=j na-xccop6jw3ewo4maocz8dlzkr3t5iku5toby7yjzvhxv
  - Log entry 12438: process socat pid=27746 uid=887 src=186.76.80.87 args=pzxz7ukutc4es5am7s30p9/gqlid0lzw8xz3jfz1l25qc1il
  - Log entry 50970: process sshd pid=28295 uid=844 src=3.205.1.38 args=pzkq1iqqmoevs57qlkweq0gcs wtbo 7-w-d15bvl4eth4sj
  - Log entry 11103: process perl pid=2323 uid=658 src=151.133.126.103 args=ijy/w-2j7x6c3f5kjhq1bj1gi4ps/t//5gux/2bm7fkzkn2k
  - Log entry 99403: process sshd pid=25703 uid=157 src=158.107.214.197 args=5r85b-lg8whuba2f98rcuj62et37cy/m0qyq/86vuh72exzr
  - Log entry 96657: process sshd pid=12680 uid=788 src=153.173.4.203 args=jyuyxk1/48ko4a6kw16lu5xrjylh829sn/xzrtna5r62nem9
  - Log entry 73778: process ruby pid=25326 uid=474 src=195.217.199.249 args=jhpc5j2k8l3hphjjeblgdogdl13bhh5x8paeyyht1rcsv3pt
  - Log entry 41948: process socat pid=19249 uid=662 src=153.213.135.166 args=ghog7 x4hsup6bf99w-jev7jtq-hevh /tg8rsgb9wpb5omg
  - Log entry 80450: process socat pid=16271 uid=949 src=92.93.42.140 args=9ea3i3 zp2-k3mza7caxl  i6im4eu5n21-1jf00ol5syg/4
  - Log entry 91152: process ruby pid=7966 uid=796 src=187.54.118.254 args=f5xas5fk0l6epprytn6b9ef1if/o7xr3hjqzbqz dv5gg3xi
  - Log entry 19272: process ruby pid=25184 uid=784 src=65.128.157.243 args=h9y0af13x9itge489n53ii hjcut3kjfqt-iz7u2t0ut3nfc
  - Log entry 23505: process perl pid=17867 uid=130 src=83.38.2.234 args=hvwu46-32qsace5rhq007vfrfxhc1udiqk7by77 bhw81c87
  - Log entry 14230: process sshd pid=25196 uid=588 src=178.9.248.35 args=9cq41/4xr-rrl/1jwo-c7s-yz5o4ncec4a1wo1xbipyaat-7
  - Log entry 52752: process wget pid=12621 uid=466 src=132.169.70.119 args=qckfd425i3vn nxxox71w3x4n4wu/x5283-1dmdzlofn80n5
  - Log entry 53689: process wget pid=2086 uid=272 src=50.192.86.62 args=ugw7 yj 46a0 g er8adlus3a0g-bhccs 6603 i96e-y61p
  - Log entry 89895: process bash pid=19083 uid=478 src=75.13.113.24 args=vdm2t0z  u/42hgmuh73c3ng hvgqh8qru1at8k/1d96lp/q
  - Log entry 76241: process sshd pid=9257 uid=425 src=94.136.139.47 args=/4ouk0hw7he-4f4bh64evvdggnm3e-1 6ag8bhp8muqe fv6
  - Log entry 32770: process socat pid=15925 uid=787 src=59.127.129.79 args=cc3h8tm2j/0/rtnex7yoj/34thqg4k3ya0jg0rgod64 5wdk
  - Log entry 37225: process wget pid=16325 uid=791 src=111.71.145.130 args=m7mgq23h-xm9rjwimz70b2-9bfuf n6b3muj gjlvtwfean6
  - Log entry 38968: process python3 pid=17177 uid=784 src=17.163.182.226 args=ncx8 v3u6fvg5- i8zgyggd642ehs/u7wh0x89a0mblc0a4z

## Supplementary Technical Detail — Section 69

Automated correlation engine identified 25 related events in the 6-hour window.
Baseline traffic on port 57728: 1 connections per hour.
Observed traffic on port 4444: 178 connections during the incident window.
Statistical anomaly score: 0.856 (threshold 0.750).
Related CVE: CVE-2026-34088 — not yet patched on 10 internal hosts.
Affected subnet: 10.6.3.0/24 — 9 hosts in scope.
EDR telemetry: 0 alerts suppressed; 2 false positives removed.
  - Log entry 97841: process sshd pid=20973 uid=254 src=78.189.51.63 args=hrq4mwtt v1ndetxkls6vjipct2r83a2jzfofva6ipi9dw0w
  - Log entry 61395: process nc pid=16594 uid=491 src=66.201.230.218 args=8qw69dhclqssmsliwk6/l91u9-mje1zkc5zxf hx//h1l/rr
  - Log entry 54231: process nc pid=14941 uid=817 src=119.28.107.174 args=-vlhjtsy/nq3eyup3x/qczc9n/ 0c2wo5wy5goa9lyn9nz5g
  - Log entry 13227: process bash pid=27311 uid=674 src=200.87.164.66 args=5sw6whyvyftj8w31u8-1-/4y5ltwlxd5y99/fkl-6ilh swc
  - Log entry 94333: process python3 pid=8839 uid=430 src=20.5.15.44 args=neilnbxxw5mzstngc24dv3qtbh8n 83/ujgfmgrob8h2j36m
  - Log entry 28981: process ruby pid=17238 uid=912 src=144.151.170.224 args=ditakbhrcioo6j0nuu8j067zrcpavcnobiw2uf sxjw4ate1
  - Log entry 59902: process nc pid=9686 uid=6 src=67.169.239.215 args=4d1clpboovey8j429g9weivgp/byt4s4p4ioyorfyejnnlbl
  - Log entry 40065: process bash pid=12347 uid=461 src=140.233.118.40 args=31tic06 ncor6-kac/jkw8hpa7ia7grf7/oh//vq6urjl115
  - Log entry 73723: process curl pid=26865 uid=979 src=22.147.111.168 args=-sg0wf-yh4ptbg81vbvyzfxhy6ng7faw 7jti3on1xx8cxg1
  - Log entry 90996: process python3 pid=15881 uid=594 src=128.221.29.60 args=yn1q/qju/4cojas6p7fws5wl0yb-ruqg5z2ub3iav96z1xqy
  - Log entry 52236: process nc pid=9444 uid=535 src=129.245.157.87 args=z63r97vjpoftjen-t//im 5qjo02u/9mx00pespta v5i4n-
  - Log entry 42084: process nc pid=27885 uid=672 src=2.172.122.168 args=vq6x-mhou6pe4qh4a0hhhdk vbh pjzip23lwz4hwhzvfoo0
  - Log entry 56982: process bash pid=1683 uid=460 src=36.178.110.238 args=31mi3ag8olf 9m q8jbhr2tvb7c7p3/j0j86aurlpkyzeego
  - Log entry 99200: process wget pid=20483 uid=713 src=216.194.135.186 args=wcs-x5 8cohh0w4w/2mx8xd045kt1l/e4m13/x7c835voerp
  - Log entry 41470: process ruby pid=27934 uid=190 src=150.1.81.231 args=07lkg0c3d7hrdw4k1/eb2t1agf9jlny9t2v3sdm6hao lhmd
  - Log entry 15196: process curl pid=12240 uid=347 src=40.241.88.213 args=v7746pvyjbigcglt41ar00p/wjozxwuo308njtvv0dak9/mu
  - Log entry 59018: process python3 pid=4954 uid=94 src=77.153.123.36 args=mvl8w8/qfo9thj1n4pvzp5l4k5afna9195ykfybdu1csitnf
  - Log entry 25766: process python3 pid=29593 uid=888 src=22.109.142.174 args=842q2y/ug  7ss77/2tw5saz9kb9o8opx5jl8nezhww8kznd
  - Log entry 66590: process perl pid=3968 uid=459 src=112.30.15.169 args=nv/i9bn 6hv454rtftuxp5j0- s3dju24oodc470p7pkj0x5
  - Log entry 77413: process curl pid=8433 uid=757 src=47.1.221.84 args=os7t5b0witfnvf728jen7lmcg/y8x3pkm847k8vyivka68ft
  - Log entry 86215: process wget pid=26026 uid=31 src=29.237.245.58 args=1drc-a23q57xrg7bim2-6iwq6s9kws/0ekg72fj6to0qodg8
  - Log entry 32072: process ruby pid=1346 uid=132 src=103.173.255.135 args=bgllbg42ljp/qp/468mvi79q297g g82g4-6h 4d/kl9ccpd
  - Log entry 97318: process python3 pid=31296 uid=750 src=37.111.223.141 args=raoqoxbeedn0u277ctmkcew/re6zr9hn5pukz luptqk1amz
  - Log entry 48806: process socat pid=3523 uid=226 src=169.206.87.93 args=hhhk9951v4ux9u4qvnvvdqjl5b0fp5j7m3tn eyx7q92tdsm
  - Log entry 90685: process bash pid=13727 uid=944 src=160.240.148.117 args=c1iswmrv60v920beyzzwwcyp3jvsh9ltsjdq27r60 h-b75r
  - Log entry 91491: process bash pid=12514 uid=997 src=67.144.81.88 args=-4ehr50f02ue8huorbt/-730uh68t6jugu3kmmy4h2tf6-ad
  - Log entry 57729: process ruby pid=5377 uid=468 src=175.46.188.51 args=w11 sv3lc9s3pwene5imve8mufrwb lzfx1hrk0i46 cgdx9
  - Log entry 45354: process nc pid=20593 uid=934 src=174.126.228.215 args=19dtqbbh1f78g434m7nito1h0uagsk ekreeyuu2qd759i8n
  - Log entry 64449: process bash pid=18527 uid=719 src=206.138.23.116 args=va1j0bdus9ocwe34zqwty r8r5bin egtbgbom  zp1l5x5t
  - Log entry 61859: process curl pid=29400 uid=555 src=60.130.45.191 args=m64029ib-ory4gbeqk4v3eydh3slj5ikhslcjzyub5lce12c
  - Log entry 97378: process python3 pid=25890 uid=995 src=180.170.6.14 args=3ghhg093x0xv/0v820dvtynt byclkixy/e--hbchosp-r9v
  - Log entry 76471: process nc pid=5691 uid=436 src=213.215.5.181 args=tylxn 15z2hsv66s33bt26tefu/y-46phze-qh-np5ro- 7j
  - Log entry 21564: process perl pid=7315 uid=799 src=70.98.160.218 args=fdtts6h0m1h11qw8iq 3vz51yhk77j-smedaxbeegzfxzylt
  - Log entry 53524: process python3 pid=12223 uid=582 src=5.106.227.150 args=29rre8zmrgne-y/jud6v m8p7c0giksbg5ollipasewu5b86
  - Log entry 66285: process wget pid=4089 uid=548 src=118.177.46.166 args= uvrp48p7l1xaq0-m2001cwjgg37v0ozp0as8 o25qow8cy0
  - Log entry 71537: process curl pid=29254 uid=560 src=220.62.93.40 args=rvd6q7z914ahp6mq-9u8i2pc2exfm/w0maug gera-u7pz8k
  - Log entry 63478: process socat pid=15704 uid=489 src=147.204.133.168 args=v-ycq0udv3zgnajhq-t977rdiy3e8s-t hzh qtsn1w-w6ox
  - Log entry 44104: process curl pid=2551 uid=179 src=28.224.224.165 args=56 7/kdv70qu-a0pcma glngyjyn2w77 pljrtogt5 6srn1
  - Log entry 57503: process perl pid=14377 uid=815 src=135.221.74.21 args=2x93savx0auc6ab4 b9o  p591chh5-u24sjfaeyzpo-g/8n
  - Log entry 71871: process sshd pid=2300 uid=144 src=91.240.109.194 args=-g/zgqt3lq1pnm0aysp661nop126z1gskyth3 lb92i2sor3
  - Log entry 12393: process curl pid=8914 uid=988 src=212.51.217.202 args=xt41e6snxe0mcipxhcr/vjl7x3 h7w163slkgkzm1d5sph/-
  - Log entry 38499: process nc pid=12743 uid=473 src=223.70.17.95 args=ho miwzixzbk6fwtcl4latp0nyww4hq/ too6s2bb01ynka7
  - Log entry 50574: process bash pid=18702 uid=367 src=58.147.79.182 args=ry g9pl3o3z/u9yi/cvhgcta5lg3ds4p-buuej45waf9/-8i
  - Log entry 39225: process bash pid=8065 uid=288 src=87.199.105.32 args=nithrkn24nxdzu2ec0p8df1 zq8m du8zhurmksdsfl6 2uq
  - Log entry 62687: process socat pid=23077 uid=399 src=143.140.166.123 args=ohkepc94x3-wd9mv9k05zufu kk6f2fciw-qb6japdyjeiid
  - Log entry 88319: process sshd pid=10491 uid=477 src=28.129.27.164 args=6m5j24jq3oqvxu1cbyo ycne63vlg2bkt 22ey1b995wqklk
  - Log entry 90138: process sshd pid=3626 uid=741 src=98.205.111.6 args=sm/3aznr2b7u377ht4g/-tt5e96dmt-xed2yeb/cd3m3z14p
  - Log entry 13982: process curl pid=15329 uid=638 src=11.10.175.138 args=ril2vb/vnf-ep3ki6vzvd2nsn2d9rmgiaayvg4pwdt4obn2n
  - Log entry 57242: process nc pid=11717 uid=838 src=201.214.52.165 args=lsn2-h7czgdqcfpd2kxfi2x/o3urlh2zl-qzcgfedz000/cl
  - Log entry 24896: process python3 pid=16845 uid=812 src=63.255.197.34 args=dpx519atyjeqoi-c-7qs2ecp7nesfsrq1s4 he4ed omz2ol
  - Log entry 74614: process wget pid=15162 uid=618 src=116.142.195.244 args=ncl3 h7iw2m5u1s-60wnkza3 slr63uvg7w9ii/ 37tklrqg
  - Log entry 67303: process perl pid=13415 uid=65 src=101.74.64.139 args=542opkaw-5ex2d3tae1f4 1oduylwin6zbznsq7ihwnt6hbz
  - Log entry 63105: process python3 pid=10679 uid=80 src=88.63.47.93 args=zgdh/5xnbkd6/uk0si9c3as6-qknkou7051 4gt0lc0bkc2j
  - Log entry 29272: process sshd pid=16614 uid=226 src=121.240.146.206 args=q0ora/geic- udz-1p99w6o/w7wd1835ke2opnc5ralo1xrl
  - Log entry 43157: process bash pid=31928 uid=145 src=176.218.8.158 args=s/9rstyobs0vc/4/kzin2ugj04nj26zbabvr0utmr5jv6zs 
  - Log entry 11179: process python3 pid=4269 uid=910 src=161.107.161.55 args=zknugop2s8wkke4 iqd375d6bfh1oty2lnwjeulsrukgm6u0
  - Log entry 59117: process perl pid=20917 uid=460 src=127.47.85.149 args=r0j160zd44pmxtb2ry6ndqw2a704361ln9d9tsqfpjwlytkn
  - Log entry 66626: process nc pid=16791 uid=780 src=32.199.206.50 args=y5qq3n89rsjkwf86cfpdwypnqhoapwdopjmw89 8n-yd0/7z
  - Log entry 58998: process bash pid=17622 uid=562 src=223.178.169.63 args=uodyga3evmgrgtcjdwhjuzt1w07slbldjkkozr83kh7q1bin
  - Log entry 19512: process sshd pid=16801 uid=942 src=67.73.9.96 args=ptyahe2 /4r q3ovcm3w l3757wn2-pkh/89 vwb1b1gb1xv

## Supplementary Technical Detail — Section 70

Automated correlation engine identified 11 related events in the 6-hour window.
Baseline traffic on port 13243: 0 connections per hour.
Observed traffic on port 4444: 83 connections during the incident window.
Statistical anomaly score: 0.960 (threshold 0.750).
Related CVE: CVE-2026-27168 — not yet patched on 10 internal hosts.
Affected subnet: 10.6.1.0/24 — 5 hosts in scope.
EDR telemetry: 0 alerts suppressed; 3 false positives removed.
  - Log entry 31992: process wget pid=12661 uid=794 src=100.53.48.179 args=i9kzywp8c12tb9k6ckzu1ticq6qfqk/fc8rc6v2cvfpazh33
  - Log entry 54558: process ruby pid=1213 uid=645 src=14.155.88.98 args=00tx/fchij s-4hv0jsox8lr/22bnjc9mhcve du53kh--ju
  - Log entry 56717: process wget pid=29695 uid=561 src=60.101.0.60 args=/56fnzh5/z3k /am9ky4df5nz70oivwxtbcupojnomjkksdh
  - Log entry 67489: process wget pid=30473 uid=584 src=128.89.118.30 args=t9q3gs0f-26cquq91z-lc5icxe0a508i8gpyik0/1g6 hs1t
  - Log entry 63738: process perl pid=13495 uid=659 src=110.232.11.101 args=2470jvvgj7kx3ppj2/nl3nwhi6g42qqsgo9lj-zqelpdx6f8
  - Log entry 47396: process nc pid=17697 uid=321 src=31.139.159.183 args=mc-4cg4jtjfe23aw 6ml12k /rwl752ocszu8rhjyn5paz3j
  - Log entry 33854: process bash pid=8085 uid=152 src=108.229.208.49 args=gc5vvzuyklb/yguatbrrz0la/xraldh3w/tg57pa2i1m8elx
  - Log entry 40375: process wget pid=4284 uid=904 src=142.38.157.232 args=bggmmfxr316l e05/-xk69594fnui-ky6461c8fvpjd9oqk3
  - Log entry 25428: process ruby pid=7385 uid=808 src=86.170.146.166 args=21tst4w60dk7-16j/t275is0nz5c2z5b1wsdlp2s3dzmtibg
  - Log entry 81040: process perl pid=11036 uid=611 src=222.1.86.4 args=j8pabfbtsfy gxv91mi-soiv41kc2e7botiznfftjc xny56
  - Log entry 80500: process nc pid=15358 uid=194 src=168.89.16.204 args=z9q/o0zgj5a403vcbzjqtfhw8lt8v/qz-8 65hm/a4zijfb9
  - Log entry 69252: process wget pid=2513 uid=141 src=182.186.201.112 args=-3m8r1tyr1wg122y-8ytd n722jxu7rv6f8z3csit s4d2jn
  - Log entry 48132: process bash pid=17959 uid=568 src=41.36.185.187 args=kvhfnm3s139nf bzxw/hnfhv54bf7ske8jnxo8apijr222wb
  - Log entry 88903: process sshd pid=3342 uid=929 src=168.181.242.75 args=9/7jy-h4zwtcc70e1i8 /8cdpfm7nsuffab--5uyl1wi2733
  - Log entry 18230: process wget pid=6093 uid=483 src=175.161.48.164 args=gn31ub9zyxjpqyfhi55cv3uxncpvq56 gbrji1aarv18tge5
  - Log entry 22047: process sshd pid=4090 uid=392 src=41.140.106.182 args=7r3k3xpy0uy ihzwdvhjp3nw5fh4ckxipwahv- i1g6ml07r
  - Log entry 80212: process wget pid=18225 uid=461 src=102.4.146.43 args=uhkmz4jefaq5y1b3onnfcex-iuo3n8bkmsn900x49vlux jx
  - Log entry 68188: process socat pid=8692 uid=223 src=80.24.59.7 args=q54p7k/s7hvncljk y/cw 75ev6gw5hx50r5ut01txh5m nu
  - Log entry 56594: process wget pid=17466 uid=345 src=111.94.66.157 args=0 0dw3jsyuwjd4jfw2zvk2i1c8q70ggpuancl14r6rptgwz0
  - Log entry 30277: process perl pid=4077 uid=547 src=178.231.125.201 args=i7n419-tj9vbx-vm-snjnb46f9w2h7op5y0uezvw7u -twwz
  - Log entry 81881: process nc pid=17842 uid=880 src=215.13.141.20 args=4h 9fjzd/7g liurqjz49buz4tmy conkyc4nrazy5/aq1mr
  - Log entry 96268: process wget pid=9504 uid=69 src=177.125.39.179 args=5toma9pkgz0vnh11y39i/sp6e n9t6dksk796/viia18z9lw
  - Log entry 75335: process sshd pid=5837 uid=700 src=52.159.234.87 args=-turgr6bxpwg2r57ygzlg50ljpw 3hae/sypv9pfot75b6ic
  - Log entry 74488: process socat pid=8273 uid=331 src=53.98.224.138 args=rmc7r24f4/66p9xdzutk65utfachst0ez8wf9vyz3- 0gpu1
  - Log entry 78782: process bash pid=2933 uid=910 src=24.143.61.42 args=9ozd3dya53dyhwidljcp0-9i4/2jh-oh32jbamhx4ucs-u5e
  - Log entry 80328: process wget pid=12854 uid=369 src=205.66.49.82 args=zu3-5hs45z3t z2oqmhztrq1u14f6r2dqnp5td8pvnw8 1gi
  - Log entry 79851: process curl pid=25987 uid=796 src=21.20.61.187 args=4q90jy3ssf5jqhj3a3lql5v/vcyy96-ys85c8njzhx7a/whl
  - Log entry 84513: process python3 pid=26850 uid=282 src=218.162.165.97 args=0kfxp0ka10b4ff7h7y/z4n0m6p7ng2lu3vyugw4tk0cclb0n
  - Log entry 36469: process ruby pid=29243 uid=136 src=206.53.109.82 args=7gbi1dmqawm0gqfceakv3e/l 23ayxhhqgwc9th7trm/3dc7
  - Log entry 31609: process bash pid=11841 uid=620 src=82.172.8.105 args=q3ervquvl1mwts6r844n4jthaw0cj4vq8e0ykt8q97rvxh/i
  - Log entry 34476: process curl pid=27348 uid=257 src=43.146.230.58 args=/4hc6ve vftp92-vti5mhpswvz8swy4 eo6ev838pga5yz6u
  - Log entry 44998: process nc pid=4510 uid=775 src=49.120.115.36 args=37 /g9woghuxw9c18-czcr77or 7rlzsxzg k1n4plgcwgxr
  - Log entry 83686: process perl pid=22365 uid=869 src=58.255.0.207 args=5390527ls6m5v7zlxoy/9gr/o21gte2ma3yjbwr83o9awaht
  - Log entry 36559: process nc pid=13281 uid=111 src=114.153.171.17 args=jmpm9yej/-/9trulbfxmf-76jrk vszdmfz22jbxwp/a3pcr
  - Log entry 57239: process nc pid=9111 uid=777 src=222.60.248.29 args=g4mql2cw 0rylpulz9/-9si54pd9qdmxakb/mgo377434eji
  - Log entry 38823: process ruby pid=17425 uid=98 src=88.99.73.148 args=oz6klk-yuedpcbm2r7py/1o9mfk1gdk4mt2f53c8 38u4eoc
  - Log entry 99092: process perl pid=13125 uid=635 src=177.59.205.146 args=p37f07u611v 30cr7w3k1gh0xhrras17df1qljiugbhcqvww
  - Log entry 66628: process nc pid=13975 uid=773 src=26.57.184.53 args=greynhpyk8xe75bkwfigpl9bdj2g83c/zg21-z7x2qhi vl0
  - Log entry 73302: process python3 pid=14500 uid=203 src=59.62.64.133 args=5ovv7g0c2sd9yo74 yhp46htgjqrabruw6o092vm/28t/6/o
  - Log entry 60822: process python3 pid=4033 uid=381 src=39.5.239.86 args=9n0db7y-gsl54kx/5z9s 9ocowgb/wiwpaq9ji6/q-/2n2nd
  - Log entry 31121: process sshd pid=18215 uid=464 src=200.38.6.96 args=hpy7vwz4/w8mpcfsp/wcem 3e/n/vrfh1xij7wxvm8h3mjr-
  - Log entry 73438: process wget pid=21188 uid=346 src=24.107.236.98 args=25jqq0r 3pcesxm6 i9siorjrpsa8ktnxjun2w37u/phvhjn
  - Log entry 19707: process perl pid=29828 uid=815 src=79.198.196.120 args=8oj--z2 o3yp0/5z 5in1/sfi0wi62g1o64 17a0f5e99kxt
  - Log entry 21690: process python3 pid=9911 uid=969 src=43.32.153.22 args=wfuq9sr8-1d564/ld3haglyntntjwf fbckit88woyawe/fq
  - Log entry 47418: process bash pid=12706 uid=223 src=81.204.65.247 args=odw-1pvheblrpo8ne6mtz971liw3xw2a0/uxm7ibzd/37pfl
  - Log entry 67780: process perl pid=30895 uid=853 src=210.216.179.219 args=krua6 y4 8cr5xykoywnic80gazbj9jo4qg3ax7-u3qzlwin
  - Log entry 76406: process wget pid=17278 uid=467 src=195.244.177.60 args=-pvhp8zns1w 3y kl5jo-ij3ocuzmqe6 -n-0wmj2 g/g ru
  - Log entry 68774: process socat pid=20003 uid=523 src=63.227.45.194 args=0qcgzbftsawqyua5u4xplaq4cwvsw6 btko06 kc2tw4kqcg
  - Log entry 41284: process curl pid=14919 uid=514 src=151.61.231.44 args=e5xkcvswk5bff8s55yc/x4z5nlj31yl5pinn00aij0yo-2qf
  - Log entry 51712: process ruby pid=11017 uid=299 src=122.254.207.189 args=wztkyhrpqlao/3bf hzztsz7owrwwa5kxxbyixe 2bfsmqlb
  - Log entry 65266: process curl pid=3241 uid=229 src=159.24.230.236 args=83gltjex9lc/-88s3cux4dczy2z miv/p3c/jn ewh991jca
  - Log entry 85870: process nc pid=3410 uid=867 src=120.253.2.40 args=wf8w61/54m7f3d92zoa8aej 0knirgjtm6g872l6yny4cbsk
  - Log entry 46970: process ruby pid=18296 uid=609 src=170.152.200.38 args=aj8u6llxl15hg56uzgwhpq231n1giej3b6tg 9hc0c c5p/n
  - Log entry 90498: process socat pid=21442 uid=904 src=8.76.200.142 args=lq cmd8qffvwe65bvs5cy5a9dohxl4 kecjt/aj8xs120b8 
  - Log entry 82663: process nc pid=8144 uid=450 src=203.220.154.104 args=xz-casn ilu/-w5k0plaj0m8ksff317/vt37832e9jp/2u/h
  - Log entry 13701: process wget pid=27778 uid=449 src=50.62.139.36 args=mj8tifljdh3qqd4ivu-k q85e4 xnng89xxov3kp5-2hankt
  - Log entry 82691: process nc pid=29483 uid=603 src=91.169.112.163 args=e142cz3xt/2w4ucgijrlfzcl62k5i2 w-nf2tryl6gejafg/
  - Log entry 84539: process perl pid=30200 uid=540 src=71.223.130.141 args=okua7 x7g/7d7fkq56jeuwy8ip9y5dsbo9-pbf9hhswmnrer
  - Log entry 57719: process curl pid=13635 uid=563 src=103.142.225.180 args=qx80t43ptb/d62k9hn7h9a-2u6mcb/6vw87xlo6pnlh9m346
  - Log entry 33194: process ruby pid=21803 uid=242 src=166.97.90.137 args=narclobfziyfgppkqhkb8whtp25-k3rn7 ni9axazzcbh78z

## Supplementary Technical Detail — Section 71

Automated correlation engine identified 19 related events in the 6-hour window.
Baseline traffic on port 45068: 2 connections per hour.
Observed traffic on port 4444: 103 connections during the incident window.
Statistical anomaly score: 0.916 (threshold 0.750).
Related CVE: CVE-2026-44085 — not yet patched on 14 internal hosts.
Affected subnet: 10.7.2.0/24 — 10 hosts in scope.
EDR telemetry: 0 alerts suppressed; 2 false positives removed.
  - Log entry 78139: process bash pid=8243 uid=520 src=88.72.51.91 args=/zw4/wy910vvm4-1lmbz-hpzbiw-j0cu8zoo0621iwcbfye0
  - Log entry 57915: process ruby pid=6517 uid=309 src=220.254.247.154 args=ljp0vg1uho67liln2n0i08r28r4 ph5t1sni8-awg6xyud3m
  - Log entry 65660: process python3 pid=26291 uid=746 src=72.12.41.67 args=75pp18un4ud22qf 7bwr-gm7hy/vmyjrq3yy8tk2qd/rul1x
  - Log entry 41496: process ruby pid=2560 uid=746 src=167.145.127.164 args=1esvm1cxxz4m95mh6q/5324g-tdcj87offhcpqgt7baampba
  - Log entry 67072: process sshd pid=27201 uid=547 src=178.223.51.66 args=rc9pjsnoj36/p3x-vgw/u8c75z2g3k1k2hljsoisi-/4fqcf
  - Log entry 96876: process python3 pid=8701 uid=908 src=171.240.183.242 args=k9ueqelhk ssp743f /31hz3luj5-xjr50s0jeze8fu8ex-b
  - Log entry 54869: process nc pid=28195 uid=763 src=155.46.230.70 args=80nfn8abh2i5qxqo87gks2107wlnoygpuxqj5u f 12a41qt
  - Log entry 24686: process nc pid=6092 uid=681 src=151.243.70.251 args=qbp506plih--s4s0j/e7ulbowm38pl 8mmajv1xy2x5uk35b
  - Log entry 98566: process nc pid=9730 uid=236 src=93.151.179.160 args=l6ia4t-4smw940/2gjywupqvi4i86xd0jfqm20-ca  8cq t
  - Log entry 49009: process curl pid=5542 uid=768 src=216.215.112.4 args=r3ujoz0rn e9ak/lzac8ojw 76zi51490d 6y6fhye5sj1rz
  - Log entry 64697: process bash pid=20024 uid=635 src=35.101.115.66 args=vjg n--id90rcorzjfcxqgy1ejg5gtp iboprr9q13iqy68w
  - Log entry 51550: process curl pid=28635 uid=560 src=52.7.55.41 args=srt6k2oskfc4k1uqq41pez/81l-zlpctdv0vev7yz5ps6pcx
  - Log entry 99810: process nc pid=10239 uid=456 src=43.196.155.248 args=4chpegileud9yhc1z66f9hypw02okkcf0ogw3nwd-9/5rn3z
  - Log entry 19866: process sshd pid=12194 uid=105 src=220.124.235.16 args=rjzfji5zcrizejooq 04x-l e/ xda-y j7q5mymsl10/d -
  - Log entry 50008: process wget pid=16155 uid=110 src=30.140.218.171 args=g/v3n/3yy-7ci/2 1quzulqbw3hb72unj84lyblwqc-vn8mc
  - Log entry 41372: process curl pid=20568 uid=20 src=180.33.172.39 args=-5td8/xv iml3cjejbhbbd1/l-5he28jk58g/5r5/um-js5m
  - Log entry 55039: process nc pid=7016 uid=617 src=22.204.233.50 args=3g8l23 x5i580q9uamqsep78c rki1wj7fybv4tpgqun5zm7
  - Log entry 42921: process bash pid=22315 uid=917 src=86.201.227.150 args=79x9 at56/tj-9ijc0 649zhktis274606juo3afh gyny8e
  - Log entry 75373: process ruby pid=22043 uid=658 src=117.57.170.73 args=tkk-ptvuos0ogdp8gzgru2eh1 kcw0 zul71pq30/ x3cd7l
  - Log entry 64262: process perl pid=12237 uid=742 src=214.227.139.177 args=0bmtyq7wqgwv5ni539kp0g23r338aauu3q0clzf/8c5kt6ti
  - Log entry 79942: process nc pid=5381 uid=189 src=143.67.180.180 args=4ng muiqu6fdz/4 9fxrw5n4i1s5i0-cvlra9fqju0d-sxt9
  - Log entry 28831: process python3 pid=20942 uid=748 src=84.209.67.225 args=zr840y2qiu6855m/lsp8nedw0pid44sv 7d92gvtd0l4vbyf
  - Log entry 31191: process ruby pid=3893 uid=152 src=152.47.70.248 args=x0qp0cl88hr2wxzk450ac1ul/thm-jyirhp3z-tgtzr8xav4
  - Log entry 25899: process sshd pid=14663 uid=943 src=19.69.133.39 args= 23shn85j66h32cql1c9yppayih2kmzi19b8v-lgq-ug4zme
  - Log entry 53455: process wget pid=30479 uid=123 src=218.92.208.242 args=gqahuam5e7n72765u2arom4wjs/3wfio5wzf3lyvvf7lm/at
  - Log entry 16310: process wget pid=13760 uid=168 src=147.103.195.169 args=x/hzo wd70ov4 7cv4kkeafg1pzl8 3f028c6nmhdlozejvu
  - Log entry 86762: process bash pid=16097 uid=129 src=178.111.218.98 args=84-m7746wp8spcedq7dxgyzwc8p-qsn974nesy rwu7ov2t-
  - Log entry 72999: process perl pid=19825 uid=418 src=54.202.71.218 args=x8d/u1 1cdci2kitbmc-vm96m2-p74fejuhe2/hq/t25jz88
  - Log entry 70051: process socat pid=21296 uid=688 src=180.127.46.111 args=k9krjk0z5a owtyrn/kd7xwex73xgw9ola766gnd8s50ud7s
  - Log entry 61253: process socat pid=26121 uid=314 src=196.29.60.125 args=evk4qplhneniqlm0m8sxntjh4qzsu4yw-29ljws ueg8ng5v
  - Log entry 70850: process socat pid=15210 uid=58 src=219.183.159.232 args=5gsbklc/vih1rr5 hpd/brm0tkdbkneymhsflf96z1n 7e-v
  - Log entry 82792: process socat pid=8139 uid=907 src=93.7.149.6 args=dqp2kck6y/l a1a 21j/3au6t9p//rs8-giek2zu0zk2eizc
  - Log entry 74732: process perl pid=30745 uid=44 src=129.248.149.196 args=2g5whu 0mms q9vmow4ig/ 3/b rpwo36bimymsxif7uwxnm
  - Log entry 98102: process bash pid=2320 uid=742 src=105.177.171.32 args=wgm29ybuld-ujwncnxf7o5poav84fwn448iw78/6kvyahnro
  - Log entry 64570: process perl pid=8694 uid=753 src=154.51.104.231 args=824nqz6uvmud7/cr0fzccghv-2364sisku0iiyyuqd5gl6ui
  - Log entry 76640: process perl pid=1277 uid=552 src=120.173.148.185 args=wxg/mrjb9ny-e9w7sem1v9bl qj93b0ae5ic0sni3r22ntkv
  - Log entry 65858: process socat pid=10972 uid=166 src=53.184.15.8 args=i2ia-prs3mmhnac/9ffqwhtj6co7h4ozypbqazln5cgpvu m
  - Log entry 15483: process curl pid=10268 uid=785 src=169.85.184.91 args=vhx-twdy8vvkwqms3jf07 x2p/bjd7bzetamp9fp17ah/r5m
  - Log entry 52924: process ruby pid=11681 uid=966 src=156.158.1.157 args=lltbtwzrcwml/keickvma6kswmoa5tce45qt50 9w t85ep-
  - Log entry 60984: process nc pid=6436 uid=452 src=20.130.27.76 args=s0qhhzzp5z/mnbsbbha2woo9rwllp1fboqi8omy3u/rvfubl
  - Log entry 76517: process sshd pid=8031 uid=997 src=111.64.219.165 args=4y5cht1764b9yygngmx5mqecrfgay6rb hd9po1f959rvhnf
  - Log entry 55826: process curl pid=20318 uid=853 src=169.3.206.33 args=bv atug/26-wxnlbxkv83-ahqp5l5bukc-p5kqkrys1j5x-0
  - Log entry 97764: process curl pid=30570 uid=808 src=166.136.231.185 args=5 r8d1pb/vs28t6y3-6xey-0ikk/64k21775ti/3pppe/nhs
  - Log entry 83175: process curl pid=5431 uid=394 src=150.175.237.13 args=ptfu 5a--gxvx7mztw2yyfq2z2vsz o q6ts jqb5dwnv6k7
  - Log entry 98290: process nc pid=4981 uid=634 src=60.92.47.129 args=16yjrd/cufffszp/nnalrjbxn3ci-dc4kw/h1u6nf-r/w 97
  - Log entry 55654: process sshd pid=17686 uid=310 src=27.201.250.105 args=d2n62wv8wh08v/qj5kwvwuak/3uln/9fily58daljvvu/a63
  - Log entry 25574: process sshd pid=2193 uid=833 src=142.28.170.102 args=aalbuncnrovt ggoiggkofx/gvlw7skc/6luxp8sz d366p3
  - Log entry 98038: process nc pid=21376 uid=639 src=177.64.113.206 args=y8pmwkj8sq2uujcu0lxpiiwgpgn0vh5xrniux0ctux4y9sve
  - Log entry 89685: process sshd pid=19657 uid=196 src=188.15.97.32 args=nhohmk6f31t/js62d9 8jy0/328/u8akp8ve/qcun9nkzthm
  - Log entry 24857: process nc pid=1637 uid=944 src=150.24.243.241 args=o2i4h4/q14yqmak0dafl5lro9oxmfp v99ye e1kc8pmxuxh
  - Log entry 69073: process nc pid=11365 uid=362 src=66.199.136.252 args=qyyv9jt-/xdorg0q6k2v5-a63t6h dperx38gsttb4lydpww
  - Log entry 29743: process sshd pid=3755 uid=66 src=121.229.217.235 args=khxwr-y//3  o4g3lw51zh0a umezalj8lp8l6n62-mdxgbg
  - Log entry 14742: process socat pid=15317 uid=468 src=192.217.100.154 args=xjjgw03iycdib x-c1r-2i y35qa4ydhe s23958i27usojj
  - Log entry 26917: process ruby pid=26441 uid=677 src=179.105.9.78 args=stryyp91vg 07l/lau8ttm0hm3ag2h15cnsz58xz5ps2y7 c
  - Log entry 57975: process python3 pid=19090 uid=713 src=58.115.198.140 args=judsz9narvqotyj/t uwpyd7ozkz-zu6w9oki-0v0hrgrdml
  - Log entry 10460: process socat pid=17406 uid=919 src=172.249.17.118 args=e/zp8yz9vjk6hghcb6jtq9ndxss95mfoaa6o8/utr2lygf4j
  - Log entry 20010: process perl pid=15825 uid=71 src=209.94.247.148 args=c36ergsvsvk36caj9v/ljc-i/upwt01k4 z5hj64/4pwtevb
  - Log entry 25142: process bash pid=29535 uid=176 src=1.233.113.186 args=uc05-n4/220dc5d1vz/vgel34qoodjjhxvcjihcojp irmu5
  - Log entry 21444: process nc pid=10950 uid=704 src=113.243.94.64 args=jvdqfh6cwpfn-1y9254y/s3o6-0mkl9hqib6n8rmjbba4nm/
  - Log entry 32571: process curl pid=13534 uid=627 src=53.126.62.111 args=cssoeb1w4zfv-kfl9v5-o9z37o43 y/tj4ltp4q/6el0m3vd

## Supplementary Technical Detail — Section 72

Automated correlation engine identified 32 related events in the 6-hour window.
Baseline traffic on port 54653: 2 connections per hour.
Observed traffic on port 4444: 79 connections during the incident window.
Statistical anomaly score: 0.967 (threshold 0.750).
Related CVE: CVE-2026-31537 — not yet patched on 14 internal hosts.
Affected subnet: 10.4.1.0/24 — 16 hosts in scope.
EDR telemetry: 2 alerts suppressed; 3 false positives removed.
  - Log entry 52612: process perl pid=12655 uid=886 src=123.146.32.26 args=g g11p0xj3-  y39e7vqou4xmykzsfagpk6lhjv/7ah1uc1 
  - Log entry 54409: process perl pid=3663 uid=108 src=55.252.94.16 args=czsjn2od8ve9ts7qghc5rgmnlfh5whxy/acswb8whusiy563
  - Log entry 19955: process wget pid=31451 uid=224 src=108.92.126.121 args=3urwi6hx48aqeysy0esd86b4z3u2m4npj07ja75tk-19x4tl
  - Log entry 86390: process python3 pid=21297 uid=593 src=133.175.74.167 args=mr1be36slreblvdh8oy25b01gr-trcrtgk/iiwjzq7sstq6e
  - Log entry 11843: process ruby pid=19278 uid=700 src=104.216.86.224 args=7je/a52xqi3o/ng/oixd-km e9684f lrekfvu6ryyh u nz
  - Log entry 43479: process nc pid=29080 uid=946 src=9.142.78.180 args=c/26a d34z2d8aar605 c2-msszq2832yrzdmkpgcwaiefkr
  - Log entry 64306: process sshd pid=19049 uid=296 src=212.73.41.74 args=bjor4/mqzpraxhvxxfe5zjxaim5h dl/28x fk0wdu--ojh1
  - Log entry 76205: process curl pid=12100 uid=215 src=214.246.201.141 args=cppv0dru-92gx/37m 2hpucmlvsk8z-vkopi0q7u7bll-9jo
  - Log entry 53060: process socat pid=28660 uid=573 src=170.189.61.182 args=gz/1jim1i/jgu3tog9w6bev5wv4dc6/pn7ipki5vtdbkg/6i
  - Log entry 41252: process perl pid=29915 uid=941 src=142.214.247.165 args=pgo33f8whkj4-bdf/t8qpk3pngplyzdtlxdfbh/tmz3ld11-
  - Log entry 60187: process bash pid=23039 uid=177 src=116.85.129.233 args=vu/zyvalf3f2skhcbtyi9xro25iwy7zoi-vwxx3kzqzg/qt6
  - Log entry 70859: process bash pid=10786 uid=323 src=119.165.8.95 args=rud-7js/ui8waqh0ky5suw knp56u5eb1bzpq0v-ges6g6ls
  - Log entry 12374: process curl pid=25600 uid=524 src=136.150.169.235 args=ufe86/-nkiedj9wjdpjz-ur55tqyb0r-bvt10h40u4q9p1rk
  - Log entry 19744: process perl pid=3320 uid=689 src=135.30.75.205 args=0kii5o9tdgz1dbzo tpr-at2wcnwya3hr0sxhavikb8fts98
  - Log entry 73036: process bash pid=31085 uid=96 src=82.96.125.137 args=n2ytcccs9tsh52zra-wo2zhkk4bt/m160ik3x04ujfrdn z4
  - Log entry 58453: process ruby pid=7204 uid=25 src=107.85.231.51 args=nl8xodlk6fqkj97 wwriguej47-0ub7kzh4fj4reuia/ergc
  - Log entry 29919: process bash pid=22919 uid=767 src=14.115.147.34 args=mneh/zi0-mp7hqy 4cxr1aqurlqqh75cgoooc79en sm64a 
  - Log entry 72708: process sshd pid=2846 uid=481 src=30.35.31.62 args=l99a68xo7gcwk1hm0ufvtwfuxnj0ceyrpxb6um4mm9h/85c1
  - Log entry 19852: process sshd pid=25482 uid=967 src=11.71.110.19 args=7rcno8h-u84/bz6-99a2dphqp0/qzgt0am6y79ac1vzjjkl2
  - Log entry 76319: process bash pid=26080 uid=154 src=158.78.85.36 args=e7xvb1fpu9d/81xk8m-zizc7wmsaync1ir-xekunf jjw280
  - Log entry 76797: process curl pid=5784 uid=898 src=28.218.41.78 args=o rzqxtzrokkmzzqqyi953a7sa5/l/rudd5dl-ztodjc0 2y
  - Log entry 91289: process nc pid=4541 uid=624 src=61.238.177.112 args=mygmobsm30kse61ut0ya2hho3cwu03gna92-90k8fwm2ys9s
  - Log entry 56869: process sshd pid=1794 uid=9 src=217.129.88.82 args=gljxi7qo/bp7iouspsdtotgge6t9bbnmd5/1t0/-di3vj ep
  - Log entry 89862: process ruby pid=30647 uid=958 src=38.65.251.138 args=r0af/4snhk6 tgfk0pbh-1xphgmjykuvzszge3d4x-nytxg1
  - Log entry 96955: process perl pid=4291 uid=432 src=90.123.117.171 args=1ajb8xl8yenfmfvs 9ovxwpuxmh0x5ztnf7 a5p-2llii51z
  - Log entry 96194: process wget pid=30868 uid=120 src=40.113.127.79 args=dm9ce35nadk/sko9m3r/97qg8e/si86/o5462o0d3cuo5m2a
  - Log entry 80756: process nc pid=15575 uid=941 src=189.71.80.159 args=r vy5t kb7rdv1g42am4nxgigmzg9-x/fgdr7occoxwlzh0x
  - Log entry 45444: process ruby pid=14534 uid=205 src=77.71.43.140 args=nh5tp-s7k 2f0//znuereguuilqgslha9z2d5e-lsq1n5lws
  - Log entry 75234: process bash pid=19312 uid=264 src=101.22.209.53 args=pbh4099j4vqui4h37/b9-h0-i6ez-hsczbiie2ye86zigl21
  - Log entry 99694: process socat pid=16734 uid=252 src=37.122.37.207 args=l6ikn4g/vu25g8u24-2wkena0orl4c74qq7knsb-uw-u54g7
  - Log entry 68977: process python3 pid=11966 uid=970 src=156.221.9.138 args=v3lsc4cths8tu6vj h3pzkw2dojyo9abvw/ba78dqwmh/g-b
  - Log entry 79903: process ruby pid=4254 uid=458 src=113.110.205.238 args=fanb5zmafy8/f1/6oxvkposh8evcrbj37k53tl0py4c0/0no
  - Log entry 19296: process curl pid=16516 uid=558 src=191.68.164.137 args=9kxteuk6tl63pq2xn5w vgsqr/ 6-nqbs-8iuc-d0noae42-
  - Log entry 89585: process socat pid=24871 uid=892 src=52.187.91.21 args=g-qprxo81/y-joh65-9/j-e4/r/qffi5fxtoa9xekymi -np
  - Log entry 26699: process wget pid=27496 uid=31 src=34.24.77.92 args=3g-si/681rl2cp1-g9ify7c5/pqiwc2pwx6y-ffsbx3fu2k7
  - Log entry 98968: process ruby pid=16407 uid=196 src=68.205.124.204 args=6im/xahvamzonowvu-ikad4ptpku-7qsy4rrvqyd3/apjrvb
  - Log entry 44167: process sshd pid=5479 uid=737 src=143.15.121.168 args=hfhsz9mvr76jci32ea/ais6gt2po3rpwrpv98elagp7e3p73
  - Log entry 35958: process sshd pid=13156 uid=64 src=184.43.54.167 args=fkl865ddayclqrr4vi137 4g2ff3c2unzly/4itvjxs1je0l
  - Log entry 28223: process socat pid=2649 uid=756 src=31.237.216.227 args=tu81j1x8xzztf1o be42z9a63b47-6-km1 y3q-z rizknaq
  - Log entry 51057: process ruby pid=23443 uid=408 src=15.222.166.44 args=2q9pm-es1 2gnz0yf4f2/o5c2k08/oapbvp-/dnl/s qtxs4
  - Log entry 74003: process socat pid=8478 uid=955 src=174.200.157.66 args=a88q7/eb-q3fcqnm8m3cvamrhp-hqvkx8rnwk3/n7rzzkux-
  - Log entry 26346: process sshd pid=16123 uid=459 src=34.120.196.136 args=3-7x/f1odmv 3bu4h9pssu1fvrm0pz 7bvvd46lc07qf06yp
  - Log entry 84755: process perl pid=20276 uid=250 src=151.215.47.80 args=8k//d12hlv9u k34f/sv5ptssm 1s-ltw3-na6ilvkijuapy
  - Log entry 85599: process python3 pid=6869 uid=911 src=26.71.138.11 args=f av 7gl0tw8o/9/lxz6ih8fgvmojo11 50ugpegzoueky6 
  - Log entry 15490: process curl pid=17720 uid=235 src=33.62.209.4 args=p6 5w7a/9bns3s ozggnc-1tl1sjg75xx6ypj9uh6b0oc5ts
  - Log entry 25942: process python3 pid=25283 uid=899 src=134.101.161.104 args=/gki2pcxhxdh9sygk/0khbfg4i1ux2ouipwmptwm se2qzsh
  - Log entry 27761: process bash pid=15917 uid=51 src=92.70.170.171 args=lgk3ste6/r5nx5dmb/q3i/81p4f0m90/-gy66rnzpbhk3ghm
  - Log entry 66218: process wget pid=23434 uid=853 src=95.27.52.107 args=7xd3xrz0la9j47r s-10iz/68-eq487yz5pv5clo/jvi-2x7
  - Log entry 41567: process sshd pid=25544 uid=316 src=167.181.181.231 args=48amq2c9y4jgh3xzsox17nbhg3ncw37294s9acgwsohc9v4f
  - Log entry 53436: process wget pid=25965 uid=39 src=139.24.236.247 args=3iqw1oosdrga0qb sy8r4y4 a1odl5qo hftyfgnt in /js
  - Log entry 51814: process ruby pid=23631 uid=802 src=88.86.46.1 args=/6kpy71/ecc6uw  b tph8z1y-mnz5rrkh-/pkf9gxahdgd8
  - Log entry 19746: process socat pid=7916 uid=404 src=25.148.91.126 args=f17tndl5ubmvzojx65fe en8draedryvfbylrnfphhxnl42-
  - Log entry 22071: process curl pid=1463 uid=413 src=80.55.190.108 args=kbua8e9r/mr4xt0w3ft1e-dv/w4wy9mug830p/qiu0h7av65
  - Log entry 36260: process curl pid=28419 uid=212 src=50.13.157.107 args=2zxqepqc5 hy9q5w89l58/ncz5owvcm5n7psjwnsac0djlux
  - Log entry 39837: process perl pid=14874 uid=5 src=10.125.208.15 args=jf1aho90wo c 3i0qn/c4q5jwspyc02ro7jd9d5i6zm-0p-u
  - Log entry 60942: process perl pid=30073 uid=96 src=215.235.9.133 args=0i8ar12htuh902dy ipgtj5yrl fljaucaccrb9ahita qrj
  - Log entry 80315: process python3 pid=2027 uid=10 src=192.126.147.158 args=wmyp0x1f6ezzb15t9f 6y67xmsxgzed7 aqqtp/wh5g7/kiq
  - Log entry 33127: process nc pid=8582 uid=221 src=102.205.165.81 args=08yrnm31ueghmsfh0ss4-d7ov/rx9zlv4khnm9kyzehl5r1h
  - Log entry 64077: process nc pid=5863 uid=322 src=150.53.32.128 args=ycx0bk1k-mcoajwr203xircm-6 u9fpsba/ig3gp8kl70n-0
  - Log entry 72492: process nc pid=14718 uid=635 src=104.241.113.8 args=gq6pikyvqtyolrwgihesqwy1qg bfxrbnh2z0q0/h9sbjcyx

## Supplementary Technical Detail — Section 73

Automated correlation engine identified 29 related events in the 6-hour window.
Baseline traffic on port 27204: 4 connections per hour.
Observed traffic on port 4444: 64 connections during the incident window.
Statistical anomaly score: 0.850 (threshold 0.750).
Related CVE: CVE-2026-22952 — not yet patched on 5 internal hosts.
Affected subnet: 10.6.1.0/24 — 6 hosts in scope.
EDR telemetry: 2 alerts suppressed; 1 false positives removed.
  - Log entry 80140: process curl pid=5063 uid=776 src=164.137.101.130 args=jpmjcus tugo8klba6k6q-fld-c381 80zcnmv3f7clag am
  - Log entry 76651: process ruby pid=6446 uid=755 src=19.50.88.177 args=41vtfvkrpbdd4h63al42ps6fzou3k3xorg395/lfb4shn/-4
  - Log entry 31431: process sshd pid=23821 uid=298 src=62.85.203.72 args=l1j5e mnf8gj0e2bzj bl583ragmgenifjbsvi/m/cm1m3rh
  - Log entry 69511: process wget pid=16318 uid=500 src=184.51.184.128 args=xyobt9p461ips2vwm 0l1p3npasado///-gpg6yxzow 9w/g
  - Log entry 98832: process python3 pid=15966 uid=148 src=16.99.190.156 args=gy3t2t3iq8fox-xua7uh0t8lpyov8q56 4a6ei0jefp-5ymg
  - Log entry 86526: process bash pid=30647 uid=626 src=16.255.209.174 args=w8nmd1kc6s6f-gr6ks6rhj8wkshtkmyytki8-j3immnt-fuu
  - Log entry 24622: process bash pid=20969 uid=673 src=184.46.188.128 args= 6rf8ipbb2po541u27w7yrvqtn0pxqtmbtz6/co7v/3s q 7
  - Log entry 48141: process wget pid=26582 uid=173 src=56.228.201.234 args=ln-dad/s9inissef4tt6rw2-tc9 13 jzy2tg-  jcjwdklk
  - Log entry 73852: process ruby pid=17577 uid=257 src=12.27.160.8 args=3sncnzrcjho curs0pr7/g-j// wkcnlcw1rrjd7zt7uz4-p
  - Log entry 86055: process sshd pid=6423 uid=821 src=29.81.180.173 args=zrt7/asawwlr-o0zj48/txz8yxvdrgzbs6ziqswen40/1l63
  - Log entry 94212: process nc pid=30290 uid=472 src=96.11.103.191 args=lp-2y4/gzro7ajw2veyei455f1h5375qe/ft-l5ukszdof 6
  - Log entry 86986: process socat pid=9321 uid=889 src=44.45.190.46 args=g7lhyj7g/1zi37mav/j/pd62e5o5flwxxj09p4s qn 0hcnn
  - Log entry 84651: process ruby pid=21380 uid=933 src=144.18.59.164 args=o2k-ec96ney7gzwnhq6n9261ek5/i8822dxv7t6r  09r1b1
  - Log entry 59732: process socat pid=13122 uid=92 src=153.109.88.105 args=n3ljvhsgx86k5z6qzhbb2hpwvsey4upo2zh/47 wooszeise
  - Log entry 67204: process bash pid=16520 uid=490 src=168.147.131.14 args=78/p/3m 7eckymkt60frijtx73d22y6ip4pjzafcxhga4nv/
  - Log entry 82006: process bash pid=27459 uid=355 src=183.102.151.14 args=rg26p-4jj0gvx2/ aupmf5ns uc77-83gwb3l8qo8ur2v21l
  - Log entry 79928: process curl pid=19274 uid=259 src=159.51.132.7 args=e7lh-alt81a8zl4-u wgzcj-klzbisqtsgl69w6srtpnzgss
  - Log entry 72892: process sshd pid=24569 uid=821 src=171.35.137.227 args=lb3t-ryf1nnzr1frwaeitngtzz11zo1bqjhq-i2bwfpewi5e
  - Log entry 61179: process ruby pid=8121 uid=908 src=175.176.10.88 args=j/vssae28a0 arx1ao/b64g4o4 7-9q568rv91zmmib62fgu
  - Log entry 40426: process sshd pid=20500 uid=580 src=173.31.54.206 args=32i88/uqnjm2vv06iqt tfvmlp8w0nakig0rms1wex6qdiyk
  - Log entry 58328: process ruby pid=18396 uid=488 src=182.235.3.163 args=rjl4xal9us06bw1/3zhbpq1jvbg v25ov2tqr3ad0 151qp/
  - Log entry 71911: process curl pid=8296 uid=889 src=193.29.154.134 args=boudrzz9yogmjb2jaqrlgtblvas8u0aj24wcyd76rtagrd4c
  - Log entry 54614: process sshd pid=21749 uid=951 src=213.131.8.213 args=huq n/sl2wqfgl-enhviggy8y3bqviwivg9hcmz0dvcu9ph1
  - Log entry 37487: process socat pid=22364 uid=55 src=57.19.175.157 args=fgcqrkrq5rvv7avo4r3vd/4c-yx29725iun9edcll90ghupc
  - Log entry 83046: process sshd pid=2769 uid=577 src=174.87.21.169 args=svujd30aovj-aenfkbjtft/6h9eurzcec8/nmzqocj3e3gpc
  - Log entry 79338: process curl pid=17624 uid=514 src=104.125.110.36 args=eagfzpxk/kby/-hrx3fxgy/qanf6fb0tnuqdd 3xdoz0ehnl
  - Log entry 52663: process curl pid=25153 uid=578 src=215.134.107.63 args=-137 q0zgmhg9vel2e8abdx7bbbzc5jjuvd6r8qjap/rgfwa
  - Log entry 84602: process perl pid=26338 uid=610 src=66.63.181.20 args=sfuxcjp08gzhtd80dkel409p0atktihj23-o073nl9i3bafz
  - Log entry 33065: process ruby pid=16232 uid=170 src=144.114.153.21 args=4oktfs/hncmc9ilng6hr1qyoa8pvfm 354lqz3utigb2owtn
  - Log entry 96185: process sshd pid=23312 uid=629 src=180.90.199.64 args=63rzmmznztj2zgykx/dvsok5h3020 fmxx64fowa38fxx2o 
  - Log entry 57809: process ruby pid=12578 uid=308 src=7.221.243.195 args=v39ry72rrdtwlni3ubt2xhcku9ng/w1stqhjbl8lrlfuno9u
  - Log entry 16779: process wget pid=5824 uid=859 src=122.96.20.114 args=ctx/682pfzzds5z1m/nn0y4wo2hi35lp6/1qfonavxnl18kt
  - Log entry 32523: process nc pid=21241 uid=829 src=14.201.120.238 args=2x5zn9gur15sumnnly6 -s6md9wa-wxtcixv--l qwzb4o h
  - Log entry 74868: process socat pid=21129 uid=538 src=100.3.234.91 args=nt/gnxah8dy/rq3s7kot3vv7bj75i8yrxn53h2qkfulnrz8 
  - Log entry 97826: process ruby pid=15902 uid=370 src=38.248.250.2 args= 7jsq25low6ad62hxxoz/3xad 09p5ne9pors9uugufghy73
  - Log entry 94211: process sshd pid=12421 uid=323 src=2.123.241.153 args=x2g3h37dbvjzghh6e3anzijde1-6nqcd/hyffz7mhmlvuyiv
  - Log entry 57751: process bash pid=17875 uid=495 src=137.226.105.73 args=54pezxzkylgpjnzbuo82femp0mgy04gon6s/vax27udy/0yd
  - Log entry 20820: process perl pid=27933 uid=215 src=149.31.140.117 args=az/ix qo22tyiyu/c0jnbkmfi2jq8w3-60hfe8x-rhh8ytta
  - Log entry 17316: process nc pid=26596 uid=458 src=194.129.23.126 args=vs-mivqc2m ia3eiu1wd4-s587rap268tzy3e8705udf1m5q
  - Log entry 84537: process wget pid=2878 uid=411 src=81.211.143.242 args=tz58do38hfap7itcpwbw/ue/y9/fl0dcj93jk4mu0j3f-h8j
  - Log entry 85979: process ruby pid=22402 uid=928 src=23.5.206.94 args=63t5mvhuopjrm0dnw88  ni4wv7ngjsuuj6v5gggm2/1fvab
  - Log entry 41537: process sshd pid=3597 uid=755 src=8.160.81.184 args=k0ddpzcmo6yuf5lr414klrfqz0xerxj6yzsbeejoul6ir0t 
  - Log entry 64636: process wget pid=5763 uid=875 src=174.10.243.112 args=6c du0d2idh8l-koe6a8j/l-0kkn0k2gl2c1wwjyterxnga-
  - Log entry 11967: process sshd pid=20179 uid=253 src=182.253.252.234 args=mko90gul9r6e3sna5eaki9ez/b9rf-d95 efr-b7pypbpd3b
  - Log entry 77280: process bash pid=26469 uid=908 src=45.200.146.177 args=xqjq jo8mszdx9sexibsg09974ihmilvy9wtkxwh/csqjomg
  - Log entry 95609: process perl pid=4907 uid=550 src=130.97.0.22 args=pi4tus2miwk79euhhce7--u5jw111zg2gp9ww0ajva6hshe3
  - Log entry 69233: process sshd pid=2502 uid=913 src=136.153.61.131 args=i25g8y/fmel93mlezesfpi7a0 bp93hqvjwr6p66t uxppxa
  - Log entry 89055: process bash pid=21191 uid=301 src=185.182.13.38 args=cx3oj2t5d9fkga17iv18 cok2h-6/9o05fz26od3uliat hq
  - Log entry 28139: process bash pid=30347 uid=848 src=127.101.213.134 args=c3n/b4y1b7g-ejzm44b29 e0spx65n3dxdgztqbxr8efsyyb
  - Log entry 89472: process wget pid=12326 uid=125 src=56.110.249.236 args=- 38oidzi400w8cebdb5/jpe40k-ugv6jv awks ay677d3u
  - Log entry 75012: process curl pid=9693 uid=75 src=190.145.115.97 args=y7fbm4a81 xg zg9luexts2yr0yl9//r5v3uxpu2mn jzg98
  - Log entry 31582: process sshd pid=5720 uid=324 src=1.245.104.171 args=ugj1bf /2o6orfziyhlrz3snb5xbsbdtaacv9e4-ax9s4- k
  - Log entry 13439: process bash pid=4223 uid=295 src=26.213.196.90 args=rtu9gf-lnwug1zqfnsskkxr795npy2wcpf4m-6ewvqy3yh3y
  - Log entry 76946: process sshd pid=22347 uid=863 src=98.171.233.245 args=cjzrajwkixbzq14416x0gwr4gajkos3f222r5r2nj1wenwyp
  - Log entry 63663: process nc pid=10295 uid=561 src=107.192.46.9 args=a3n2hrmg-vbog8h39 ik96 4mrgw1b61f/ayv/u3 667tue1
  - Log entry 78076: process wget pid=4151 uid=449 src=21.243.111.57 args=gl89otfwnrpq493mj71o2gueh/h04x3fqxuq5teusj9mut7a
  - Log entry 58440: process curl pid=30172 uid=272 src=134.104.95.242 args=bw--cooptzzv16t0pqrqlbyk4p/kvm2uuzydvu7pd/o8dchm
  - Log entry 77021: process socat pid=8351 uid=479 src=145.28.1.99 args=zxire3624h9bcz9aqhlebshk73qhh93lbdcom fgvrw cqr9
  - Log entry 33939: process nc pid=13580 uid=704 src=4.221.46.49 args=a- rar/c6/ogvoj4hlbzaiylgzqeatlx1 gy ky5xl4ql4w0
  - Log entry 37104: process socat pid=31106 uid=135 src=137.27.214.195 args=omtq3w6r3sqp8axog91b91rnftdayh4sgcg2-9zvqcv07 bb

## Supplementary Technical Detail — Section 74

Automated correlation engine identified 19 related events in the 6-hour window.
Baseline traffic on port 28438: 1 connections per hour.
Observed traffic on port 4444: 137 connections during the incident window.
Statistical anomaly score: 0.868 (threshold 0.750).
Related CVE: CVE-2026-13580 — not yet patched on 5 internal hosts.
Affected subnet: 10.6.4.0/24 — 19 hosts in scope.
EDR telemetry: 5 alerts suppressed; 2 false positives removed.
  - Log entry 66629: process ruby pid=18718 uid=764 src=91.153.242.228 args=iwd 00wd18wtegpe06/ym7r/umpz/7f-3b 72ccxzkwopfhj
  - Log entry 29048: process socat pid=17615 uid=20 src=143.188.192.10 args=1usd8e 4vq0/2ron443ggj47yee/5umveynd1iwuy0ied8yx
  - Log entry 96406: process bash pid=13467 uid=390 src=137.124.149.108 args=79q7-hzesxwopuvgg1phv0 khvn345aoi-yqqzrqox/dhsg6
  - Log entry 55474: process perl pid=27927 uid=844 src=49.238.138.183 args=lqxr6pz3yd0 mgjh4qlhq3w8tgx2ofh/62/o05jks1dd7zy/
  - Log entry 42937: process nc pid=12978 uid=763 src=8.171.235.205 args=26smvteos qxrhff1n1g- --ph8v c/mkk0nsozl63667atd
  - Log entry 55949: process socat pid=24062 uid=130 src=66.69.135.87 args=0xedvahl4pw yagn42/r832m4d/11/ub4o12v119/f8v5y5v
  - Log entry 54472: process perl pid=27396 uid=171 src=53.106.233.11 args=4vkvh27j/oyii ozz37icoxit08w hic11- wulrvtchua c
  - Log entry 92140: process curl pid=20811 uid=144 src=51.22.104.199 args=szq-37j2i8t4zxd4j69juitfi0jkpy7-y1chaqwr/v2jvrrt
  - Log entry 85146: process python3 pid=12066 uid=743 src=184.26.236.242 args=/0josmxv154yd-g/otzf0nhggnxcfk-dqiy1oumb/z7vtpim
  - Log entry 78967: process sshd pid=3590 uid=812 src=45.234.154.237 args=h5a8c-/q9hfziifzfebf51y34w2twpihvzurk9q/b7kt9vx1
  - Log entry 37177: process perl pid=6403 uid=268 src=149.2.41.249 args=oqrjipgzv/w80/kh77sml7efmo/2caokc11bfm28/c58dqtd
  - Log entry 60745: process nc pid=24210 uid=433 src=126.51.40.126 args=fvlu15dgqnw2k/4 r711 ntv/p-u88jplui9lvbrcg9k6x3p
  - Log entry 98618: process python3 pid=5494 uid=866 src=84.140.197.133 args=7rcjlg0aa-2kz0jbhmvxaezjbki08/9t712q2igcyunof4qy
  - Log entry 43078: process sshd pid=2553 uid=654 src=62.55.208.21 args=rimw0xpv5ipkq09fjqb17c apqd1b-34v2 u96 057l1t2f-
  - Log entry 75835: process wget pid=26585 uid=547 src=213.181.218.164 args=hytovpnvvh2skhu491qfvg3f2ls8s92uhzic7wu-o2/p7yos
  - Log entry 73412: process bash pid=29606 uid=830 src=1.132.235.27 args=laeaj8/ebkn8qbiwlq c1sm75zpbtihpo8h7nxqnkyf9zq7c
  - Log entry 37027: process bash pid=27720 uid=137 src=199.222.24.227 args=- tk3rj fqj3zm1417278k awjeddsg/vd7693z5g6sb1/wp
  - Log entry 47181: process bash pid=26589 uid=446 src=206.88.86.236 args=/8gesu53hpttey1t 1jei983 njv5y7kbu8/geqcmg0ussgm
  - Log entry 80395: process socat pid=16975 uid=989 src=50.127.178.4 args=8uolhwbzl87jp/apk12v63f9 o71l3vd7e3emhdk2zo/jwq 
  - Log entry 93189: process sshd pid=2427 uid=896 src=151.140.232.155 args=e3s06cb8pkz23e6x1/os7gwnev8c v-vkuvl-3ts/12f8al4
  - Log entry 71252: process ruby pid=18209 uid=440 src=131.63.49.64 args=/mubf5i-ecg1cs245v5c13688npt t-2y srka/wxvp--v9c
  - Log entry 89314: process wget pid=12776 uid=302 src=57.186.79.150 args=nvxqf9xnykakwfefy4nlppm26ldoi/7f4w2py9p6u6xrb2da
  - Log entry 39059: process socat pid=22096 uid=949 src=120.18.31.60 args=6 q9mcxxjo-myzvgl2jutvjnzi9xmm-31r5rbee3v-io kh9
  - Log entry 23380: process bash pid=4610 uid=39 src=163.56.181.219 args=w3iuzvn/3fw41vmmnhl5tlsv42bziz/vh33 6ts8bhm3w-d4
  - Log entry 13609: process perl pid=1635 uid=308 src=53.90.52.238 args=smeok9h5/dt6q0xaid-gp0bserb//-2fxnwq mgx-83zx8uj
  - Log entry 66304: process python3 pid=3796 uid=611 src=154.215.131.61 args=6sk zaasu8e69svrge2rk9yed8qu97/c247e7ws-y3 tke8d
  - Log entry 32981: process curl pid=7213 uid=958 src=83.43.119.149 args=nur/0t2r89oq k8at7h2ctxelyr06uz8bwg 93vfo7gmhrz9
  - Log entry 96001: process wget pid=3019 uid=493 src=44.185.179.41 args=ok877cei/6vbw91pp4cp8asi62dkb0thc8/89/15yzll9atf
  - Log entry 73873: process curl pid=10077 uid=816 src=76.225.142.194 args=3cu89kxk//uxo0034sy7banpvh6c1ghx7 qdr5nsbs0wb080
  - Log entry 61146: process nc pid=11898 uid=78 src=105.214.218.55 args=2cur23 xcylha3wataz5j28ciag9up5mgkweix2a55l3q1yp
  - Log entry 31978: process socat pid=25996 uid=529 src=87.203.21.142 args=hmjppim8q7dxn39g9vk2e2gdhcy17lfmy-2o7qrv9d3jrgoj
  - Log entry 31069: process socat pid=8676 uid=691 src=168.204.70.178 args=8/p71gkt74cszut7wla5yuz-r9rfo0232iui-rpnufhs7k-b
  - Log entry 77308: process wget pid=23959 uid=673 src=13.28.173.105 args=y699mb9zirdex7w511k8v6mepv7w859wv3d6qr3drm7t-e4c
  - Log entry 13042: process wget pid=30242 uid=633 src=118.174.112.232 args= zm0i4-bc50sdl5rcj wc/i82z5v0oll5dotjnmv tun/bp2
  - Log entry 82731: process wget pid=6298 uid=310 src=108.149.166.160 args=08t7178p/ma6xbr0-gsbbij53w7qf- p6l6nojd2q9-jqeoh
  - Log entry 31357: process bash pid=20693 uid=238 src=96.62.36.26 args= 9loiovk2w42j3x0c3s-p5cc0tdo9ugy3pexpuq4byt-uogu
  - Log entry 88925: process bash pid=18854 uid=809 src=186.152.109.139 args=t8/z57ljiussrd2dzu5ojm/c1z008/ook20 z8 f abgt728
  - Log entry 90742: process sshd pid=14530 uid=16 src=95.229.160.82 args=e8i9plytsez57ba4x2dlh5m6cx0typpg31u-lx3twbbubnky
  - Log entry 81440: process ruby pid=20213 uid=831 src=208.142.115.21 args=j2wpg5aejd/ce3m5trqcwhgvbo1ohj g//sde/ud6e8kuovm
  - Log entry 30338: process perl pid=27229 uid=233 src=117.46.114.20 args=khdr6nlh ld9g27jww43qn zs-e83 vbb8cdqgi3u4blzxzz
  - Log entry 30011: process socat pid=10227 uid=209 src=212.61.254.27 args=nc-lvnm em5d72tzcb-6-osbi oht2vxdic5lfpn-zfeocsq
  - Log entry 81206: process socat pid=28568 uid=903 src=154.107.77.152 args=u4m78sg028bpsex0e1kd6ghadm99lwwx8a4dpbtptwve  h 
  - Log entry 24625: process curl pid=6559 uid=952 src=178.67.38.230 args=git3mrhjyn6 81uqqpk01xn0hmosb eu6ovm7486f2g3300p
  - Log entry 86862: process curl pid=19433 uid=930 src=92.55.204.207 args=5nh1amv czh6p2/ccm86daqiot3c9a/guup/iva3v6i0yzok
  - Log entry 13465: process nc pid=11457 uid=812 src=82.114.4.36 args=x6oxsuf6pf8bv84pzykg851csizfliys5u59mw2amluit34r
  - Log entry 33571: process socat pid=31282 uid=49 src=159.230.105.151 args=hfh4l83swb9l16-g/u/4kxj877cljbnt6c3mejnz miue-0w
  - Log entry 15883: process bash pid=7924 uid=31 src=51.218.207.167 args=x7zohagj05esehcib0y udom8dyucz1-v7szdlb8hrvx/p1w
  - Log entry 34168: process perl pid=8980 uid=991 src=70.16.13.16 args=5 gr3ksputbtvbm0s-e73bs9-sed26x87d73h81xy1ffe94m
  - Log entry 85727: process perl pid=3072 uid=974 src=2.95.83.12 args=p y66pvg2bmr43wc55zub7mkq1-6lned7pmf4i4u1hql243k
  - Log entry 57631: process python3 pid=23482 uid=196 src=145.40.70.198 args=qu8dgoe67urb7xk6-o-clz3p9ft7ru16z0rbk0u/vf8hzjin
  - Log entry 48501: process bash pid=10069 uid=188 src=140.195.108.39 args=3zpy 2lp uoa24ef0y3ssanj-gpoxmdqi6qac/i-19k6l/ l
  - Log entry 78973: process perl pid=30666 uid=474 src=193.22.144.85 args=wsyu3lop-yfzhd/461ysllkqxxvc/j8m9mk/wu1800a0tn0e
  - Log entry 51790: process sshd pid=7544 uid=3 src=96.34.23.170 args=3lrj1om7igcd5nax7e6x-qd0i diz0/qrj7uijy0088ie8lj
  - Log entry 68796: process ruby pid=5138 uid=70 src=94.174.199.73 args=kfpppol02mi88m96- yh0pkv93jikedg-4ams79hkp6cz7ef
  - Log entry 36454: process curl pid=17619 uid=26 src=126.136.77.183 args=r2q1x-6rkpdn8-dmdd51lpr73 cdfhcwwt7v3elq62dsf8ac
  - Log entry 90034: process ruby pid=10059 uid=258 src=159.133.176.72 args=p3ao3k0u 07wikijgpyk75qe-sivhm23ajw9guwee-ao4/7w
  - Log entry 90605: process socat pid=7278 uid=860 src=178.106.68.100 args=o/0c/44rzxydrreksey073d7w2l4 rv74q6edwttto3it/8c
  - Log entry 93604: process ruby pid=1920 uid=159 src=6.46.48.43 args=9xogrxs1d40byhhq-82- -6a6qzerehc-/-zmi2e6r6it-x-
  - Log entry 73095: process sshd pid=5554 uid=46 src=56.161.9.164 args=ufiuu-x9qp1ktb24p3aqrt1rlkab/mkibj7q0erc8xr-0drc
  - Log entry 85522: process nc pid=5118 uid=529 src=57.100.229.71 args=bx-gd30lmlc1stve1ge5la-bl-hml9mcfw7ay72e3gib nsh

## Supplementary Technical Detail — Section 75

Automated correlation engine identified 46 related events in the 6-hour window.
Baseline traffic on port 42990: 1 connections per hour.
Observed traffic on port 4444: 53 connections during the incident window.
Statistical anomaly score: 0.908 (threshold 0.750).
Related CVE: CVE-2026-38782 — not yet patched on 11 internal hosts.
Affected subnet: 10.8.3.0/24 — 27 hosts in scope.
EDR telemetry: 5 alerts suppressed; 3 false positives removed.
  - Log entry 61882: process python3 pid=30746 uid=511 src=178.107.54.30 args=wlc0tay2awbfs0 u613j-ro7rnh-8/eqszv9hqj9ax3li3 e
  - Log entry 72356: process bash pid=17046 uid=43 src=143.71.16.95 args=s-fs-jtlkp-aon5sfgdysmak2picplkukc/-gzx0r2fzcde0
  - Log entry 40468: process sshd pid=25036 uid=355 src=169.77.55.193 args=wolb3fmey5fz7pgy5qc mzgtjp7th9bh5y308/5i9bmr0tlz
  - Log entry 26629: process curl pid=15737 uid=166 src=173.235.208.123 args=e3657byerwtbfi89b2lv0137u39kr4qvdmdh50ny r-y fj1
  - Log entry 53409: process sshd pid=18433 uid=404 src=209.59.238.250 args=cteecyu4imvbickl750zd9g37sws0ux5angre/c/fid3t d/
  - Log entry 57291: process bash pid=13868 uid=436 src=84.89.229.126 args=ypqtw38bfcv1n7z9qa0ke-hh7xwcpu5i-6up3urm0vcslbb2
  - Log entry 84121: process ruby pid=17414 uid=340 src=217.105.103.194 args=8j5saleg/8 o3-jtlkc9-5pl57bnnsv9q3m0n//sfhse 9ie
  - Log entry 29801: process perl pid=11887 uid=398 src=93.75.88.80 args=y52x9jv91h4e1o/h-8q62dp6g pr-y7snm7b2nafkn3 0f7 
  - Log entry 82517: process ruby pid=7514 uid=775 src=75.1.11.151 args=zedkzck 55/i1arcqmkdl1qy7rtw6af54-5en5wsrr3y049q
  - Log entry 59631: process curl pid=12032 uid=197 src=112.210.231.199 args=3kk49s6nc7 mzhl/822syr-9xigjuf5jt5beodyu1rjgjmsv
  - Log entry 69096: process curl pid=13284 uid=199 src=163.234.45.121 args=xz1kany -/gdfi-u e1j5mapcne ess0ia0pr0e94zk62 gg
  - Log entry 93872: process curl pid=27355 uid=125 src=110.142.108.51 args=1pk97e8haxfkt/q3btdw-obgf78qgymuboqxo2ej5dsqrnq-
  - Log entry 59441: process bash pid=22497 uid=879 src=220.237.237.193 args=g0br211p7qu 9l4xri1t2elg5mtcounfb e g71lzgefe2mm
  - Log entry 14094: process wget pid=14490 uid=651 src=218.32.4.35 args=eu-0osm69q-8xye8pm/ oqau47/o9ow6-7g2r8gpegbijvg7
  - Log entry 47305: process perl pid=1908 uid=177 src=58.151.8.121 args=66b4ykp1-h-y4wtk1vuze/wfhz50yedanml7342 mu35eiru
  - Log entry 46087: process socat pid=6618 uid=317 src=193.232.187.203 args=ziklhhyqv2-x131606e /4co7ien49 5zjdxa hh bxsuio3
  - Log entry 71379: process sshd pid=17566 uid=954 src=124.95.224.105 args=k2dedzpobapzzdnz7 tm9qognetoi-/tkt40kxaqtcvjux60
  - Log entry 24355: process perl pid=1489 uid=615 src=160.66.206.252 args=ube/j91hp/a 8l5rdh0v0irz3ixrk3-11n8g1g1cmlc8jly3
  - Log entry 35843: process bash pid=29884 uid=963 src=40.33.225.236 args=5n 3gv9366l2pbmjz/380p2nacvqroy8ufgs7oe59976kh  
  - Log entry 40227: process ruby pid=21721 uid=615 src=111.182.110.202 args=iwu7kwg3am0e9g8ds43atmvfe/r-pta0fz-5s/ z6qkag4nf
  - Log entry 40482: process perl pid=12275 uid=455 src=116.219.176.222 args=s59m841b8owkn98g/39 fq/r0rwq-slm6ny47g3l5c84urx6
  - Log entry 26689: process curl pid=9348 uid=963 src=51.76.247.252 args=hn0qk/rh52dmh908q1tqj8weq3lwzqd8-/hl7q6elh24vg y
  - Log entry 12768: process wget pid=16766 uid=380 src=197.117.30.191 args=3ixrfzyx8ymg9v2bgnd8n6s a1eo607f76wqp  61 craii0
  - Log entry 28355: process sshd pid=19936 uid=884 src=21.222.150.152 args=2k25wzy/98oxvokmnfz38gfhh 0ge-0063/m2yr8cj7z4rvx
  - Log entry 54432: process nc pid=27924 uid=862 src=172.11.40.160 args=dk96sj2chmxa4iwvvr9x4-8x798dq/kvnlfgv0t8nbj/iekn
  - Log entry 37588: process perl pid=14875 uid=155 src=167.204.209.232 args=g3wskjgr391f3y8uzmgw8-btnhyp1miknahlqiqeyqm39/pf
  - Log entry 48788: process curl pid=30585 uid=455 src=204.208.212.154 args=vh9t7jpme1ptpjaoiwg342f6n/ul60hl78zhyo/b8en9tuy4
  - Log entry 18350: process sshd pid=9444 uid=993 src=59.28.25.251 args=061kkaef1apigbnqdj43lt2eggkk rd 8o3i36k933g/mzjg
  - Log entry 49404: process nc pid=18500 uid=494 src=71.165.77.17 args=y-0m465fzjfkppjtvc-8vspxkzfwd172irc214mxol gi2/o
  - Log entry 83465: process wget pid=8172 uid=861 src=99.132.11.102 args=4dwytd9rgrw-942tz8qmd85hohfgi01dwkf2yqvjhvpq4th2
  - Log entry 60576: process nc pid=22625 uid=109 src=164.190.5.109 args=y99yzffpw2omsmgeixc9qtqxrcm408y1smf34x4b18mdrj-b
  - Log entry 43178: process sshd pid=2266 uid=426 src=52.87.29.156 args=m2zjtnkdos048irfd6jthkfzcv l2/sydxcmjkccw2lamp53
  - Log entry 48743: process ruby pid=24111 uid=126 src=167.151.155.114 args=2-x4ct089sjbkhf/u2y1tve2lpxzu4c-jvn1y4oop700nn e
  - Log entry 75194: process curl pid=31587 uid=548 src=219.4.160.225 args=r4mqfivon2m0ehvwpuxorsm0br/0fm1jfbl l6ty1/ upj5k
  - Log entry 55550: process wget pid=24754 uid=724 src=188.175.82.8 args=r3f/9xycbdv6f 6w-wv-d8-j6mp-f101vj5fgy/pkb0x2s33
  - Log entry 72070: process wget pid=17121 uid=546 src=187.135.237.175 args=3gvu574mp90ycuds44041yf/kk6-ydzvn fe4uzi1/l195kt
  - Log entry 99640: process socat pid=11722 uid=633 src=200.122.160.224 args=s5/eko1uv 84lmwpobzhqkd6zxzeb-319f7w0v994zjltkve
  - Log entry 28517: process perl pid=29652 uid=559 src=204.208.175.2 args=j-y9hr9b1i16qjseypltr1z2vih/uwt39vfh7nw3r68dbxk6
  - Log entry 65784: process perl pid=16587 uid=952 src=82.158.225.37 args=utfx43 pjc/bzunb38m8-tjhq2hufqdud7jeskc61xzoomxs
  - Log entry 82373: process ruby pid=6515 uid=908 src=133.90.72.8 args=aetzvdqd25taujuq8ji2z9tdf41-nevd1it2njz0lrv8svpf
  - Log entry 64873: process wget pid=9460 uid=347 src=29.183.110.239 args=5gunclvlh7hf/nz-sint e8iu9a/slkgv9egsqmdv95rvhzb
  - Log entry 50428: process ruby pid=26995 uid=401 src=193.169.180.78 args=dfj8gfqj8r6taf3aplg/0yyovkj4q-ullaw4pq-2igqoqa26
  - Log entry 60567: process nc pid=28362 uid=555 src=93.208.130.48 args=dkpoxzt7 t3p/flm-v3sn i4/t3q496ssnooylsog-zftm3 
  - Log entry 31314: process sshd pid=21333 uid=635 src=208.0.87.244 args=c1eeis7q9y5 qp9-/r0rugtr12vig w5vo082u/ q9be/nbo
  - Log entry 61398: process nc pid=22962 uid=377 src=167.162.122.52 args=m7cpo5f16zl8d5-kp4cog fqnqcnhicypj-jy7ykbmr4594t
  - Log entry 19285: process sshd pid=9623 uid=436 src=100.250.122.19 args=exob /vz9jd/cer8/kzg18yg1s34n7fp-fvpgai169j9zesv
  - Log entry 72055: process python3 pid=1295 uid=602 src=135.175.204.138 args=xy4vyt81ju/xda /h-u7tmky4b7/cc-v en7 ywjfiz4b8do
  - Log entry 86862: process bash pid=17014 uid=905 src=110.20.189.172 args= 1nxd q/0jpd3cy52gc tjvktsv84big g8ewbzn33r54wk0
  - Log entry 11024: process sshd pid=12819 uid=487 src=174.249.8.183 args=gpnx5l50lvjwl9s46aq3tk43569ns9c6/m49vo1-9lyyy5mj
  - Log entry 62413: process wget pid=2831 uid=898 src=175.115.182.17 args=qh74tm-/88b7gh wlj42o15vvuyujgqpyo8e-v1caehl37 c
  - Log entry 23588: process perl pid=23153 uid=513 src=218.17.1.68 args=/5rdx/qov/zuyrte4mc9 29f6exdyyelfejsm611f1cl bis
  - Log entry 73767: process socat pid=25317 uid=432 src=75.48.215.130 args=ga-zy6mr-x5oktiq5s2p-05ciz5yjhlv5rdoa0cms9rvcwa4
  - Log entry 50684: process ruby pid=10791 uid=724 src=56.172.249.112 args=ninv3rv15m3hg24blyxjj1q3l8 mmho9w68tdvq1 -mi3whl
  - Log entry 78628: process curl pid=9985 uid=916 src=100.9.243.1 args=rssy7mec1s11q3958s7dry0ypdcd-sxg --czgl8vq3mhqqf
  - Log entry 81873: process python3 pid=1218 uid=374 src=15.184.108.22 args=yy2hh7wu9n/um i8bt9re4f b1rfxzjjnygmpfem20b0pun4
  - Log entry 61626: process python3 pid=13583 uid=930 src=49.94.112.112 args=8rw6y-/lktqx81iaycq7c4e8m8a40u zl0xf0lfgl6lpws x
  - Log entry 78113: process sshd pid=24962 uid=989 src=89.45.47.12 args=p9vskiu33hrygifcx svsqyp8f9/lpvgays5/n4pbc7ezjjh
  - Log entry 24721: process socat pid=26583 uid=323 src=6.82.200.141 args=pj 17nr3mbegq9m842v9/-aatcwthgt5pkyzs zzl0bw7jxw
  - Log entry 95203: process bash pid=4479 uid=891 src=12.155.0.79 args=gkl2ocng7/yszxr5ew1hq0fjknqr3wv30hf8h5 vkntmrrv9
  - Log entry 54183: process socat pid=28834 uid=27 src=62.189.232.84 args=/3ja8kuez6gblses8d ya8n3/r1m9-iszb70qudc27z/s53n

## Supplementary Technical Detail — Section 76

Automated correlation engine identified 5 related events in the 6-hour window.
Baseline traffic on port 16422: 1 connections per hour.
Observed traffic on port 4444: 188 connections during the incident window.
Statistical anomaly score: 0.866 (threshold 0.750).
Related CVE: CVE-2026-48475 — not yet patched on 10 internal hosts.
Affected subnet: 10.1.0.0/24 — 10 hosts in scope.
EDR telemetry: 4 alerts suppressed; 2 false positives removed.
  - Log entry 66876: process wget pid=11920 uid=799 src=15.97.234.253 args=-w1tewokut4-/swwzfshwuvbifbj7hfx2/s6sjko61c/g-7a
  - Log entry 38339: process python3 pid=12359 uid=162 src=68.69.33.236 args= fz7b m8b1 gx7ex0u67bjtnj cql2plt1lz ji4/rzns7yy
  - Log entry 26453: process wget pid=5454 uid=358 src=89.160.50.141 args= k1mx2i56yo5yekt1lt9vvsx5tfnz/on5mq-3egn05n6hd 4
  - Log entry 81667: process python3 pid=5261 uid=13 src=108.21.169.251 args=n89atke16ac8lpe1xjxu3u4r110 o/b7-ow1d6mppjfim6-i
  - Log entry 68046: process bash pid=5015 uid=601 src=66.129.216.36 args=14glzu79iucx 2gxz7qhdkoy61dr5u/gd5ny-21ipqvj5ci 
  - Log entry 22130: process socat pid=18621 uid=83 src=166.113.210.233 args=ot18w8ixw4q w8qstkr57ztobl8yeuctbg0beu9r55efgu5o
  - Log entry 11012: process sshd pid=1315 uid=895 src=193.91.41.227 args=0 8jgtv5eubs0g-b2x5hcbj6ckh11vl2rnkpo/ecmya9x3q3
  - Log entry 80743: process socat pid=1475 uid=115 src=183.189.0.231 args=95ymwl- gkm2b637rlg5cpa5-llcl2ck25cx32qe4d9pj81m
  - Log entry 87614: process nc pid=14247 uid=889 src=16.248.168.38 args=/522arah/uniyb/k7b70tp10/k5shvg1w8g3jebt66g75i97
  - Log entry 11050: process socat pid=29412 uid=103 src=82.58.161.109 args=fytczq6jqxw/408rv3ewi4oxl0m-zf8y3k7ckrjyu5tvw o4
  - Log entry 73818: process sshd pid=16440 uid=382 src=90.54.82.246 args=r4uz4nakztd5im7odb1nxfmn-0xl3fuaeubq0kl0jol5-yy4
  - Log entry 27812: process sshd pid=17380 uid=140 src=47.74.37.123 args=dj5271-7up-sgraxk2o4az/q1vl/dzuw21/efqhpt2kpua0f
  - Log entry 80986: process python3 pid=5519 uid=456 src=149.100.192.98 args=gn-r9w8hsmruanelhmsy0 dr-l9o5g6c9//90689xlta/jus
  - Log entry 46396: process bash pid=21110 uid=54 src=75.148.75.81 args=o38cyqspgviliqgaia9qhfbyggwbq1k/uihhoal tkwqjt-8
  - Log entry 35212: process ruby pid=20693 uid=566 src=83.245.252.80 args=ewhwnn104ul3t y7f2tcfzv9v5296g7b4zcf/s4weg259fq1
  - Log entry 87935: process curl pid=18799 uid=530 src=95.16.249.12 args=ghcdosx/3daad8/09cs4zgcmf-1f/n3razuigqxt7ibee/80
  - Log entry 66308: process curl pid=30772 uid=381 src=171.205.209.24 args=dnb8ky20-aqfa0wcoyn6k-j2s1 /myw0xq q/urc-7mrg0o3
  - Log entry 78082: process python3 pid=9372 uid=393 src=182.93.152.156 args=4o3cfuq 0zhzdjpp67y 68u3uq4kv6-k9mdoziy3mdpuftrr
  - Log entry 54763: process wget pid=24352 uid=805 src=206.155.74.90 args=loovp5s2vm0sot/7x56nrn2b/5ctk j4/w4yarkvp5e4m9wv
  - Log entry 36546: process socat pid=5562 uid=491 src=34.64.184.212 args=o 7nfpngh8427944-d5acpvwgo2iyp8iwd58 zsyp2ddoeag
  - Log entry 56747: process python3 pid=25466 uid=668 src=8.125.182.146 args=6k4umslcd-8uomu gu 0sw/87kott0tr//e/lobkrn4fvrpp
  - Log entry 69961: process socat pid=6082 uid=450 src=211.99.197.78 args=-de0ws0mumnmhz766mtn-kz/ff51k/r bac66ju1bmqd7bzp
  - Log entry 28162: process nc pid=21440 uid=742 src=199.250.11.40 args=ceog02jyfzl8cdhrmzizau5mgr9lf1-96egh5utyvp8kez z
  - Log entry 19226: process perl pid=13429 uid=287 src=1.246.110.86 args=9h9awgzc9twguu40tumwjgo- wvdn008ogom-mkulnmwmidj
  - Log entry 74283: process wget pid=2942 uid=345 src=38.4.6.199 args=24nqbhe-3qrxxtswp54q0pe-t6ztivl0hx9u3fwawusr8n7 
  - Log entry 95730: process curl pid=19689 uid=196 src=217.19.6.123 args=jk/vsh988b10z66xlosj10zmxvvmsfu2-q96hkmt0/jf/ da
  - Log entry 38926: process curl pid=11117 uid=222 src=133.147.69.152 args=kaw9h7bc2bv2427wvp7117mw5oncbr4eqm-qs-jk1g1avx57
  - Log entry 23979: process ruby pid=18896 uid=919 src=147.202.245.209 args=lei0timoduejmy9poamnpm/h3yf46ymomb33719y5hmjc454
  - Log entry 37743: process curl pid=29727 uid=269 src=82.35.55.103 args=1mow--h-76ez 2ixem 5pp v/0rhh/5lgn8ms0yr2akro0z 
  - Log entry 54242: process socat pid=7213 uid=307 src=163.169.172.119 args=xf0ksnot3-/pwb15mgtfv7cfojx833zizi6f2zszpkqhpvsk
  - Log entry 88866: process nc pid=7077 uid=638 src=19.223.254.240 args=5kd3ofb91npxq  cajzxyz0a5r4zmy0fn3wc9bq52z7srgws
  - Log entry 92285: process sshd pid=4615 uid=628 src=82.73.148.250 args=/sgc8zv06odwuwvw2heckhenf78e8a8k9b4nvjtrqfgxn 4p
  - Log entry 28656: process ruby pid=15332 uid=77 src=98.14.16.49 args=y 2u9u-q6 jjmah6zsmag 6xlknfyvk1dgacdb56ihza3ifm
  - Log entry 17967: process curl pid=22650 uid=792 src=157.102.130.59 args=rjoufo580zz- cnxkzd jka8j39-8d/cbwnxu4j236 dt01d
  - Log entry 74348: process nc pid=27339 uid=903 src=164.236.135.204 args=cazaf3 9kkqmtj6/s3993f67ql6xfmyt3/dmysu60a7y/b9e
  - Log entry 20876: process socat pid=23307 uid=856 src=84.169.166.73 args=ee-xotjpyqktpn2mrdv/muwc18a -fy18dgh2dzz0ny8i70y
  - Log entry 74630: process sshd pid=14268 uid=788 src=198.164.26.239 args=7x4ouatavya92i xam3fda32xzoe er1f0y0xth/gm080gpx
  - Log entry 61310: process curl pid=14364 uid=189 src=162.170.18.208 args=pqygbbirn-s1a03330zf - bwvgxtmdv4qyh99cs4u8lp44k
  - Log entry 99217: process nc pid=3589 uid=987 src=191.204.198.52 args=r1z3mt68p51l7tckym/kcump60-3tmnhj71o5a7hzj0tt8zh
  - Log entry 73902: process bash pid=23234 uid=977 src=62.125.148.48 args=lng7nh7gdib/gz0wlysu-l3lox0yd k-7lm5c3s06by1fddo
  - Log entry 68115: process sshd pid=8271 uid=608 src=171.26.19.71 args=4y6ybktf9npq2lg4u/igdpp/q0llby/h71txrq2e70lp4snb
  - Log entry 79405: process curl pid=7585 uid=888 src=14.84.155.113 args=qcal1jo59k9ttkfs4qed/b/b-cm6dc1ucuk2eaa733mfrmi4
  - Log entry 90285: process wget pid=29934 uid=147 src=56.249.81.223 args=l16g8mm4b-ga2asi4qyxc9ut9x47xc4apt2ycmx27a2/ -u1
  - Log entry 90216: process bash pid=19543 uid=883 src=29.243.139.240 args=ulvn-5nrai/17wsvxd5a0tmj52yg6wq2ny6mjswalw/0qpth
  - Log entry 79071: process ruby pid=14406 uid=894 src=67.158.223.177 args=dyo0nu/kkfq07x1sqafivtk626p4vjnzkr oxzpgloqbzf7v
  - Log entry 93397: process socat pid=22329 uid=136 src=81.53.32.47 args=7sk4fbejzog5/9vviwkgvtmpio5z 3f-/hyva5 2k2hrohzi
  - Log entry 17671: process bash pid=13251 uid=159 src=60.249.106.107 args=erf xuguy4a1f/lilox-x8ekm4rs9b-aeumcq/t-f97vim0u
  - Log entry 47680: process ruby pid=6890 uid=515 src=188.65.162.108 args=hhj44ef11qcetjx/1h0eo67ic zx9/z2o01pb4/7o/ipho5f
  - Log entry 73903: process wget pid=4259 uid=180 src=149.85.207.208 args=3r2c8b5amlqh08c u7eqt02ywued 7when 8h2 g8xcfo3g0
  - Log entry 29242: process perl pid=2982 uid=422 src=147.52.15.125 args=s6xb9tj1dz-iiirbrzrui1e 7vzg9r/nm -  zk5qtxlgyra
  - Log entry 12522: process perl pid=25050 uid=499 src=189.135.61.64 args=sq6c46rcfpzc419-yed-0jqdg2egvp246rxf-3lyyp17lass
  - Log entry 52767: process wget pid=10276 uid=523 src=213.114.139.224 args=qu3y0xcdefyn979vkp6jk0/3utzkc7s4q8z0l206vd7-tf3j
  - Log entry 51094: process sshd pid=17388 uid=629 src=64.170.43.224 args=enztea9xqt6p935fn1-e77rcikijoa5h-g397pvj6exfe3gh
  - Log entry 70180: process python3 pid=13225 uid=830 src=19.231.75.185 args=5u6xaz6ccrl4huc-gy2b0d mld1--9isvg1os-4e7i82vasy
  - Log entry 25382: process nc pid=14884 uid=165 src=102.183.38.174 args=sq/en16/vt4/ r1nzu-mq9x0es r5r6i6/bzd5miz1a/p6yq
  - Log entry 95727: process bash pid=29021 uid=210 src=85.207.16.83 args=u2szl3s2vkv-n bqykfo pxtdnrlrhz/2gi4wxwsc7khb-ol
  - Log entry 57276: process sshd pid=11338 uid=185 src=154.4.13.29 args=iq7gwbu7rj4d469e13om8xjeymtkxmqmuy4akrrgncznikoi
  - Log entry 89945: process bash pid=26341 uid=819 src=173.165.99.15 args=h4uppit919ed435r7ehdrhvbd5pbrx/7ht2i59lr mnkcdvb
  - Log entry 31847: process sshd pid=4931 uid=648 src=42.132.230.248 args=/cf389wzmesju0btvby74h9f21dvaszlyp33zbn4oyr05dnw
  - Log entry 84293: process ruby pid=2756 uid=462 src=28.41.182.141 args=33uylsot-f6jr sllq8z37hygncmtv9 6l8v9df9/bw453m 

## Supplementary Technical Detail — Section 77

Automated correlation engine identified 45 related events in the 6-hour window.
Baseline traffic on port 6572: 1 connections per hour.
Observed traffic on port 4444: 80 connections during the incident window.
Statistical anomaly score: 0.873 (threshold 0.750).
Related CVE: CVE-2026-47270 — not yet patched on 3 internal hosts.
Affected subnet: 10.8.0.0/24 — 8 hosts in scope.
EDR telemetry: 1 alerts suppressed; 2 false positives removed.
  - Log entry 37731: process wget pid=26250 uid=49 src=118.136.195.94 args=scrcp7h5fuxrjj5r16l8j0p/vyy1syi1na 55g350ve01dnu
  - Log entry 86108: process sshd pid=13585 uid=723 src=11.232.105.154 args=63qkudomrpfx-lnzkqf/o7mzv93j 2/4gkg6rn0dpcyjcpnn
  - Log entry 74796: process socat pid=30375 uid=774 src=40.251.105.67 args=4/laygn2i4j ifuwtaou2x5-pdgrjp4qqxbj9t9lrk-lw9 q
  - Log entry 99915: process perl pid=19390 uid=710 src=152.202.58.106 args=o 5jby5nblr2z//xv-xy5zl6mms72z76/djjd-f1qfm/pow5
  - Log entry 88198: process wget pid=15758 uid=88 src=108.12.5.236 args=f/0mc/knkr4wii5qwhuokadawuaaznta2lfjg3g6k/-58vik
  - Log entry 55914: process sshd pid=5037 uid=85 src=88.179.155.60 args=g5so14ra/puznffhn5g/zvd/5yodnxz5pxo-ck1e4wl5ua03
  - Log entry 36088: process socat pid=2099 uid=998 src=205.162.127.197 args=j7snqb2a2k1/tb6z2-k7xfbgf204e86efy0502menc2v/w0t
  - Log entry 23995: process bash pid=22812 uid=461 src=194.208.67.59 args=igxk1xb8bh/uvc4 bbf2vuwgkzqlytw38-93-qr0ogu04rtr
  - Log entry 34657: process python3 pid=9097 uid=942 src=138.20.124.200 args=monzdeyjtqw-r0rq1xl-0v9dp433zcsk9lktc83kdn7lqzs4
  - Log entry 91984: process sshd pid=6876 uid=82 src=164.97.43.135 args=u8zyojajycj/d5t0ri3d3mzxj-eynbj0tpobe9/8j8luhvxq
  - Log entry 23372: process curl pid=9518 uid=592 src=202.199.142.70 args=1odg0i7s6-hfneyyaclpgng5i8/rq251 raby 0ifrzi6 e6
  - Log entry 56912: process python3 pid=6553 uid=965 src=114.106.57.92 args=8r57v1-c1 0hi9cif2q/zhdv3yo 6nzit9wu5i m/venxrq0
  - Log entry 82900: process sshd pid=22854 uid=756 src=175.252.31.92 args=oe0lh/ouo 51v2to0ymtc-v14nlhgod4ieex2gpsbgija6an
  - Log entry 66463: process nc pid=31900 uid=910 src=144.126.6.139 args=fd5h41zp3quzayznl86qp7w4dfqy8azmzu o8l79mwgk183v
  - Log entry 35480: process python3 pid=13580 uid=613 src=71.23.35.170 args=8ctsvsgv3lfea33cnf0iygf/iiuv4-zxceg0809h4w252ubq
  - Log entry 89866: process wget pid=23619 uid=504 src=49.245.241.198 args=2h zlk4zf51/8t/mquui628mc/ksnw815odt0tk5c3x6-7ws
  - Log entry 87701: process curl pid=8599 uid=303 src=4.161.246.166 args=lxqkjtuxfjy11/ef51bgfyyisx7nliag53mnx0z8qvfbpl8v
  - Log entry 67079: process socat pid=18755 uid=773 src=171.224.209.242 args=z352mc-yikcje8 p-2i0-8tkg/1xe5ncbc70aur/blo748zi
  - Log entry 10153: process nc pid=24378 uid=226 src=64.43.230.245 args=lha6puuibbi7fhq1fu2 z32/zajwg2cprpjvvj9nzqzzg8x4
  - Log entry 62680: process curl pid=7074 uid=661 src=4.175.32.250 args=dw2ig54dpclddzinqxbpgpkr38m4-zl1p4khj9rmqcyv6587
  - Log entry 48127: process wget pid=6650 uid=318 src=53.110.20.219 args=yprgxcvc8b8xetm279rrjoepvz4xn2z8afn3rd 830z- y-4
  - Log entry 24878: process bash pid=15662 uid=396 src=131.121.97.7 args=e6on5basjhyiyne6tn64huqztwvl8zr5shm7kfc4eg1zxq7l
  - Log entry 98443: process curl pid=1529 uid=625 src=92.112.193.199 args=faqu/yak33pj-wjbq3hi2e8oj1ijgdhbo2-45wftj12-cqca
  - Log entry 58931: process nc pid=8800 uid=278 src=47.202.221.48 args=2v7 lwlcj4rzmirb5694c4f-5jpamt60ud-xilhr1zh48prw
  - Log entry 94632: process ruby pid=7057 uid=445 src=27.205.93.39 args=ue6cni0ks7hx1my2-ny6ser7j6wwr70vjc2wb8ou581dhd87
  - Log entry 96599: process sshd pid=5962 uid=915 src=170.193.219.30 args=9n/77zo927c23mkv96c26v4q957m27sln-tf61soxjy/jld/
  - Log entry 79346: process curl pid=13952 uid=300 src=131.70.246.130 args=5djton 0yk5 o3/cegxu58/l58kdrp3vv3h8h4-t829a81pt
  - Log entry 40730: process wget pid=25982 uid=5 src=70.35.14.212 args=-i9uh58bv/islz924sw8uv-pq0ir903on-e u6uloq5-h8ro
  - Log entry 15668: process bash pid=2090 uid=481 src=167.41.38.220 args=7c1h3iiktz02kuz kfq-1/hlk9-lteemyyyn9248f9ou3 ij
  - Log entry 85786: process sshd pid=15078 uid=63 src=159.160.153.69 args=-u-wnscing xych4/qx1urysr09-d no5a4a173j7kkgvwrq
  - Log entry 89687: process ruby pid=3286 uid=995 src=220.117.133.15 args=mx1hse4ccey99dq6yb4hvzhmxtpvlgdpyxsyhv x7/uq90-y
  - Log entry 21456: process socat pid=31630 uid=935 src=117.57.16.107 args=3abrhuliv7twrf/1q6f9-sgdrqp0vg6oox5ossvudk d unv
  - Log entry 96454: process bash pid=1505 uid=745 src=162.170.220.167 args=cdwafpfu1jc3iiqu1-in yoh440-vuhrfanv7mpz/mr7nmf2
  - Log entry 84541: process wget pid=15211 uid=457 src=93.97.36.252 args=a-muy7 d8cl7vmozzrqosixi0m37assaisy58rn1waejcnmd
  - Log entry 68049: process wget pid=5399 uid=756 src=7.24.139.168 args=ism8gkulg38cd1wp-/oi6di8qpei0s/3-0c2gd6wcvm092l0
  - Log entry 26120: process socat pid=19817 uid=734 src=175.231.84.208 args=y0tmkk4cj38njk- z rzpi2rwaov0zi4agluq1ka jx2w66/
  - Log entry 18289: process wget pid=22232 uid=989 src=148.156.173.72 args=-bk4yrpcs 0f27hh3stmjocmrdhx20dvpyn-2dynzsdxf611
  - Log entry 15113: process ruby pid=15817 uid=702 src=14.155.162.128 args=x//l0cw900baow-nh1 ucwi/bx17f/6wehsud 089952px z
  - Log entry 44874: process nc pid=1007 uid=586 src=104.50.161.40 args=iwk7zuyps74bn8d4-5phbn27wxcqj4gvnpcwnq35yvl95pj7
  - Log entry 59962: process socat pid=7481 uid=735 src=78.87.172.55 args=j6dy- u6len/3qaoyrlr814sq5aqcp c88l-6q53/n8y0p7c
  - Log entry 11270: process python3 pid=28365 uid=325 src=95.192.15.223 args=3t68-nfbqggdou1o w /8ttxoiq3quu58w x8b5n8ge2g3pw
  - Log entry 90555: process perl pid=5008 uid=532 src=80.99.219.79 args=2brabz qwx9ap2zel14t--1t5zgc/ql9x90jcxas-8hy9msd
  - Log entry 31832: process sshd pid=30573 uid=633 src=202.105.50.19 args=z/i6 yin1c3lyji68vj9ycha-84ak y0rt41a-1-a33 rc -
  - Log entry 61022: process perl pid=8707 uid=272 src=75.226.52.9 args=7d1dmoimgpaojfw/5wbts0twju7urjxn3u2gi7knjbbn6zof
  - Log entry 27257: process wget pid=9544 uid=208 src=137.195.183.41 args=26m6tpuc7o4kjt1nc/4ind1vgf a46bk9kag4i24uztdbtzx
  - Log entry 65808: process sshd pid=19689 uid=963 src=164.123.131.181 args=rfd/94v/5ir/x/r4v4so9r-pzy4al1p/3ptofxrn7irw58hl
  - Log entry 36376: process ruby pid=3693 uid=811 src=43.129.162.126 args=si/as1-c8l8xib51/rqis1aqqfls6hrh 4 6h j/1i- dew7
  - Log entry 87025: process socat pid=11075 uid=48 src=81.92.136.76 args=hka3jhg5lg5eu6b3t2f-id4wxqng8egqkwerq-cwkqc9z pp
  - Log entry 69050: process nc pid=10064 uid=91 src=123.147.65.96 args=36n9dol/pz- tru7nmv8-/uhags m-w3l zj uq3 ggfhu-/
  - Log entry 20902: process nc pid=20861 uid=300 src=122.120.59.132 args=ullmpa381d6vlng1ybtm gmwwt2saw1w62o-hveru7cr0kiu
  - Log entry 68767: process bash pid=6894 uid=888 src=18.255.31.165 args=rqdi51j6ruv5dhg02zem1kvw6h2ud/qq/8/q-/rtg7epsbdc
  - Log entry 65862: process ruby pid=5440 uid=416 src=125.18.96.18 args=z1q5ha5pltzci3rx-vgeih2s2s75xkn22//8q1d2zit9yn-w
  - Log entry 97096: process nc pid=15550 uid=95 src=64.10.166.33 args=sn0cb7aekz8xhw bc493yjai a8jzhbsgmyqj-kvig66de35
  - Log entry 45302: process wget pid=22373 uid=316 src=4.254.66.120 args=mxiesc9a2mea5oixlr8qfenf1tordj6si60hr /kxv2999uj
  - Log entry 13859: process sshd pid=25024 uid=363 src=50.50.167.129 args=rrcfq-1 bkr5h78ccdvb1/cjc03gm37vk0hd0-48dx0y9f82
  - Log entry 61865: process ruby pid=18792 uid=244 src=191.26.108.58 args=h4g/c1q wwrp5j gbpjwjc0-qxrw3thxfqszjyhm h2 0xp4
  - Log entry 53106: process sshd pid=15897 uid=33 src=100.251.9.5 args=3rdjxsdcgf-i82hm0x456kdwdmwd4na753vdez5elrpof8py
  - Log entry 92560: process curl pid=11119 uid=361 src=29.6.249.81 args=5m9q2-xvwt-kqfulmj2yhd0umi2axzbm25/yxdqt3orn2ibc
  - Log entry 86642: process perl pid=16002 uid=684 src=30.230.53.5 args=w6vg79lok70rn-yh3p833oe5skonzq-vv1bizf6rcid2/x0i
  - Log entry 98469: process ruby pid=15543 uid=633 src=196.208.139.218 args=/ntmqhkqgpk1rnet4j46oh3d1ybf7f7kwhgz4jjo7ey2v10c

## Supplementary Technical Detail — Section 78

Automated correlation engine identified 33 related events in the 6-hour window.
Baseline traffic on port 64292: 1 connections per hour.
Observed traffic on port 4444: 109 connections during the incident window.
Statistical anomaly score: 0.914 (threshold 0.750).
Related CVE: CVE-2026-22674 — not yet patched on 15 internal hosts.
Affected subnet: 10.0.1.0/24 — 8 hosts in scope.
EDR telemetry: 3 alerts suppressed; 1 false positives removed.
  - Log entry 46380: process socat pid=3883 uid=175 src=31.116.82.52 args=yxtqswx6407h-d7vh0jvddzi0s6e/q7r032wf8atbcqh7v/b
  - Log entry 23418: process bash pid=13792 uid=991 src=177.11.100.234 args=jk9qepflhkq6zshnv3gc4fg7gihcdrdlhx/6vo7yaj3wq8j 
  - Log entry 12674: process ruby pid=13738 uid=632 src=33.205.191.96 args=0u3t0pcrzp14xr34gndj0myni kdtpn/69o8-rk0 ezb24cn
  - Log entry 92613: process bash pid=5317 uid=466 src=76.245.156.239 args=oehbuvt 86wn6ypooen79khv8bw6jiaeem0zj6z4iaok-me4
  - Log entry 33316: process socat pid=31432 uid=803 src=162.91.11.33 args=t3m6q/bbhs-e2 mkerfyasp n6gvgi1b4u6 kbwzstu1xz3y
  - Log entry 55152: process bash pid=1027 uid=867 src=196.180.228.4 args=pt0-d64u jc-ufhi5vasp6/ d0d0 4s8xnm3gh8rxjtf8-so
  - Log entry 85883: process wget pid=10398 uid=892 src=141.129.96.179 args=ipuf6jk9m3yv2yxpk4geqhdo2w/k30 0vsh3oxalr45g7bw6
  - Log entry 55960: process ruby pid=8089 uid=238 src=59.45.15.18 args=w0ijno9ql0mrj7e/z3btsgqohw8q60u2f0wnmx2bd/urvsb9
  - Log entry 32411: process curl pid=10012 uid=111 src=27.53.117.116 args=vu/ya--d 79g9 48swp3aeacqr/411jwqek6ogmjelcp/fdp
  - Log entry 62786: process ruby pid=31424 uid=611 src=176.215.240.141 args=k8gpb5eb2o a9n8lrbdzuxy5/ks-/swyzu12f17u /8ll2v0
  - Log entry 51268: process sshd pid=12481 uid=57 src=63.10.248.103 args=jl2tdg2ybee6fix3tweh1n eoz5k8c6e27pn/28advvcl/yx
  - Log entry 21949: process wget pid=21458 uid=189 src=148.48.58.167 args=aht5g/hu3ukaodea57/y32la4pu3sh8gnx31p0hezny263c-
  - Log entry 79439: process python3 pid=24100 uid=987 src=213.253.211.145 args=ds6q4rzw1xxcjmfedqyjwu d94kfpxftb5z1c902- pqthzp
  - Log entry 19646: process nc pid=18707 uid=772 src=74.174.184.254 args=9522bu/4481slf/2i3ov-414y-7eyqolbg8k mjmwtju794i
  - Log entry 16722: process bash pid=25621 uid=158 src=70.65.84.46 args=8mqfwbv203aez-05a yyo16b1f5jg2vp 55dtc2skty653lm
  - Log entry 56436: process bash pid=25594 uid=277 src=214.167.27.152 args=n0zh2qv  ar5v2xl/m5u-ywipnj6ybeyrcluzvigdhkfzlxz
  - Log entry 42867: process perl pid=7961 uid=239 src=209.118.18.142 args=g76usz1y mol04h5y99t0s1 lhhnih08c59y9yv81xj8eb6g
  - Log entry 43576: process sshd pid=10446 uid=60 src=40.211.68.161 args= y0m89tiq 7yacga656k1ykg49old4a7lyj47h25jwtmeagk
  - Log entry 79867: process nc pid=26033 uid=686 src=166.86.239.176 args=6g2q/yr/z m4bl icvdm-86i8j/yz18biq5291qi6etpgnu/
  - Log entry 12845: process bash pid=17232 uid=340 src=65.39.79.107 args=bxr kpp44hg/4vnbi0kufry1xbok8/kvq17445ca/b5uiogm
  - Log entry 31233: process ruby pid=23509 uid=706 src=80.74.230.150 args=orophwp-exvpk3yr2-z787tkec3g4hgz6cvdtcurhxora31g
  - Log entry 86118: process nc pid=8780 uid=406 src=144.112.130.119 args=uq2/3o8rof/24e4lqx5asvbrw1p6kx/z 7jhkn4tvqbpq1tr
  - Log entry 91395: process nc pid=8360 uid=379 src=65.108.104.170 args=ea55 gigt sux5lf-zf4t da30zoxn5/bi is/puwsi98fdd
  - Log entry 65378: process perl pid=1378 uid=238 src=49.212.139.142 args=70jruql4ru1-4up2rmq9tz148kbmc-3gbg49/hzdt3y6njsp
  - Log entry 92685: process curl pid=12714 uid=553 src=14.119.254.52 args=p57 oswry7jj0lw3y1r1 6z29m2ou04j4me8glrmyje6mrd 
  - Log entry 96003: process nc pid=18547 uid=363 src=148.161.48.109 args=q4it4e-o tlq q7x5m0 0 t4x16kfj99ka 6smkyv/vzzlae
  - Log entry 48884: process socat pid=11319 uid=425 src=151.182.243.172 args=oiyl651jnh9hpun-8u/0hngcxamu-1 xvlc/kunbsq4b kn 
  - Log entry 55848: process ruby pid=23934 uid=708 src=69.145.66.66 args=-x90qmhfb6ljx35tx3 db72m5b7tuligufn9 4gcia-/nu89
  - Log entry 69472: process python3 pid=15271 uid=165 src=59.23.103.2 args=-dqrpcw901cg93s14ia76w-061j-/lolsamyf5qagziouk9 
  - Log entry 19996: process nc pid=22114 uid=309 src=98.121.112.81 args=6jvcrpu//h9vp8g5c0tvrbw00545krygu7t27psq3vx c94i
  - Log entry 33628: process nc pid=26977 uid=143 src=214.28.93.23 args= objf3uaqnbc7k8-tuvdw7djrxcsc3upecwlgymxm5qmlcwn
  - Log entry 19911: process sshd pid=17850 uid=150 src=126.152.81.166 args=lh53vwe1ruwgipfahbfkpp2mwf9gr/vjyf je09930/mvsrf
  - Log entry 34026: process curl pid=5116 uid=354 src=49.253.191.104 args=9wna67f92fmhlohs0uzs/8anuycvupxjofk0vq/ rowm 26e
  - Log entry 20807: process ruby pid=17932 uid=852 src=138.225.196.240 args=rsr6d150hbnbhem3nr2j3zw4nra50xl61f9liq2kz5thbf57
  - Log entry 92640: process perl pid=31568 uid=715 src=69.114.157.179 args=m-07r1iyz1fwlnoj-m8uv0ru-cojao2-t9ljxva2nv1il188
  - Log entry 40545: process ruby pid=22098 uid=939 src=165.73.134.236 args=nuznfjtkhg10q w67rkgo8qavyuh3tf6veyl9fkf8eb5gv3i
  - Log entry 57214: process ruby pid=3028 uid=146 src=75.37.194.147 args=m/5er3erkekwegipic92 89p-4/4lhupdosqo7r54h1wh2of
  - Log entry 90153: process wget pid=15759 uid=444 src=88.19.205.107 args=9s7y/kk9vj5zf90swl78kapkst zb vmnpuf1uqy0qmu-2xb
  - Log entry 25211: process perl pid=9137 uid=177 src=37.167.137.123 args=4r-064y0dejo0vzu2987wir-h52 pg8ssgx/wl8fwr/yxkjk
  - Log entry 58303: process socat pid=21968 uid=139 src=182.88.164.120 args=j6p0ha6rroau382gv95m064oe74ue0o9wjpmhmkeo88d332m
  - Log entry 13473: process perl pid=28995 uid=543 src=76.138.42.117 args=92 56x14dhdaz6y1677nibqmq8cy  yj7f2diial -h5v46k
  - Log entry 80065: process ruby pid=19014 uid=866 src=149.16.26.81 args= b9mhoo00intvm6bzkqcfun0v7rbmyt1n5sbzp4ppjkkem0q
  - Log entry 43510: process bash pid=1403 uid=596 src=38.5.99.233 args=1wpun2bfhqpx4btp81k/dl68dek7iaa4wnagxzpfeg6n8ta 
  - Log entry 25356: process ruby pid=23708 uid=193 src=44.242.22.19 args=fi-rzn0ld51rcyr2olwrm51x dw2288hfztxx8v2yi4qc3qf
  - Log entry 14601: process curl pid=26759 uid=992 src=151.146.46.46 args=tj8nkrmxr52jpr3l730or3v9m702-qfjlcjp-j5w6x5vgl36
  - Log entry 32859: process perl pid=25574 uid=792 src=175.197.52.17 args=w-fphrtq/qgfg1dy3d7fskk3e0stsuw3g2pbfiau4bufi2vw
  - Log entry 64093: process ruby pid=25218 uid=436 src=82.186.183.19 args=d9n8rww2mrv7v/k68p8u 970suzn3nalt955qu c9t6/rb1o
  - Log entry 45343: process perl pid=7812 uid=301 src=196.220.169.203 args=o4hs2mx4ts53f8y1y2-krb9oqvg8kua4myfd-chqzhsel7yr
  - Log entry 85757: process python3 pid=27664 uid=294 src=151.231.155.97 args=1y19ryx3n5k9w067adm5w893-tclzcq8k/vp7heag6lrhbkg
  - Log entry 50475: process bash pid=17940 uid=404 src=42.165.27.52 args=w2o60duxquwyl9a8qzf3qe1af65yt if/myanalwj-4pbhnz
  - Log entry 24919: process wget pid=12441 uid=207 src=20.54.98.232 args=atx8/itmn/p0u67i029n7gzrkf9xhxovzq58pu25gvqho954
  - Log entry 44713: process perl pid=4690 uid=614 src=97.109.219.154 args=v6f9p98d/pqpuc05foi7568nvz911xxoql f6v9i5a73wu0u
  - Log entry 58209: process bash pid=8128 uid=292 src=6.5.41.135 args=blfjjzbhw7fm36zh6jqnya0pabzpp5duys6-mo2s8qdhcynm
  - Log entry 97124: process ruby pid=5047 uid=282 src=8.21.181.148 args=9en1xai7om5a13uv3tv52x/2zd19zgf61ce-3qe3wdma9qbj
  - Log entry 51093: process perl pid=4764 uid=299 src=133.253.245.140 args=zd4t90j16h98b9yhsizfm u4f--u7scuiiz79a/v5n55l6 /
  - Log entry 22255: process wget pid=7013 uid=928 src=70.183.141.48 args=pfrm25w6sf-ulj1y308h2jy13z7/5uggnlnuc1o63j2i7 gj
  - Log entry 70475: process nc pid=6200 uid=178 src=209.206.210.169 args=z6iexd/uf3ahex873i2ahs70i1tc1c31qse2z9pgzot1xuza
  - Log entry 62258: process wget pid=13839 uid=93 src=11.173.73.181 args=5n5qcu43ls9 6/9dywg8qepad0nknnk62ro h81wcijxukq3
  - Log entry 55741: process ruby pid=9005 uid=163 src=166.135.9.68 args=gstfjr30735r1jv584k7dxeckbnd02y9y044yua-p3ly16dz
  - Log entry 32167: process perl pid=15980 uid=191 src=185.67.143.1 args=0s-jhu07fv/oxo34cpqe7s lahpxi2tm00gx1404-yu21eoy

## Supplementary Technical Detail — Section 79

Automated correlation engine identified 12 related events in the 6-hour window.
Baseline traffic on port 35071: 0 connections per hour.
Observed traffic on port 4444: 197 connections during the incident window.
Statistical anomaly score: 0.965 (threshold 0.750).
Related CVE: CVE-2026-28022 — not yet patched on 15 internal hosts.
Affected subnet: 10.5.5.0/24 — 25 hosts in scope.
EDR telemetry: 2 alerts suppressed; 2 false positives removed.
  - Log entry 47855: process python3 pid=24713 uid=138 src=82.80.144.44 args= ma2hvtwnkd7s-pv0e8pefcprmgw9c4j88l9mguiu05hmde5
  - Log entry 50282: process curl pid=23295 uid=5 src=174.56.205.15 args=z8xeyx-tlvjaz0ic/ivhm7/4ci-xj/-sr5uvz1bfvhxak/7/
  - Log entry 45543: process nc pid=27059 uid=895 src=58.51.135.41 args=tg-7gq92bc/bf6ep hqhxhnytwrhlqgcw-6qjhq0m82sf 04
  - Log entry 70824: process ruby pid=31963 uid=549 src=177.132.231.118 args=1ug0aumou9ym-65-mnwqi44-0przigz9hxdvpt-g557cwg0j
  - Log entry 48449: process sshd pid=13651 uid=347 src=81.97.30.184 args=t5qipp6zgv/-y2i1dzkkfpj0o37w/izt5eobui61sbbp65n6
  - Log entry 65136: process curl pid=1634 uid=832 src=144.130.227.127 args=8z4  /n7vu-6iiobksjgp516nk54/xge-rkbfwah5u sr6dj
  - Log entry 37996: process ruby pid=28982 uid=890 src=145.84.169.181 args=mffkvcef-oxr3/uz hqci7a2cxj04lyztev/8k2thm5dkwuo
  - Log entry 50100: process perl pid=26433 uid=583 src=97.253.42.232 args=5r7y65cfdwnk71s/b4hy9aszc/g6sq5f8 lv/2wtbn55n 5x
  - Log entry 70037: process python3 pid=14287 uid=538 src=16.141.147.67 args=ed21s510t6wzcmpkmy5/ubvpn05p7gd95-ij6v8-6hac9x h
  - Log entry 32946: process python3 pid=29278 uid=404 src=46.179.125.62 args=9wb u3-cjap2d3k6eno-kzhvwmkg k/j55wt4ue113xeqpsy
  - Log entry 12341: process nc pid=26357 uid=368 src=220.202.223.183 args=t ly643vktbw7n6f2lmcjuk1u7rh/dz0p6ca6mv/sox-uguz
  - Log entry 87934: process bash pid=30865 uid=759 src=196.141.28.165 args=kj5bbpsqz  54ce5d7zxvl5uvjc8jjep83gtb4cfhli476ri
  - Log entry 61261: process socat pid=30275 uid=618 src=112.140.17.203 args=kogbw2y2k5lsyi4kn -5jdjp0-mfed02zoq/pw7bawk1f21d
  - Log entry 87871: process socat pid=2352 uid=225 src=54.71.123.78 args=kv8re33pcmenks6oi9rzj3hjjwoswugjzpuwmciyc33/8off
  - Log entry 87712: process sshd pid=26554 uid=748 src=156.145.114.172 args=hd2soikny/x88d8emoc47b1q37o90jz2mu44 mww58 vr-hl
  - Log entry 53105: process sshd pid=23876 uid=531 src=122.140.141.181 args=3azplb9bf9y38d7dtqwfw44g8bly3bz8q vakvu -868v2hs
  - Log entry 21015: process sshd pid=17958 uid=837 src=106.180.124.76 args=tlx8yf c2kapfwhyjxfskjbmq8 o1verg/ cvyw2/ap9qk e
  - Log entry 77322: process socat pid=5255 uid=789 src=50.11.219.134 args=b80kawxbbwic55cs bfoi3//e6lmb6ewi1wz8pk4189pjmpm
  - Log entry 34064: process bash pid=17604 uid=910 src=147.70.54.28 args=foh wq1-1n1-q2ujx- m6yxgjx5scfj3 g0q/v9wnswiy3/i
  - Log entry 51436: process wget pid=31988 uid=322 src=70.111.229.215 args=90rq08c9twc07vmcc6bflzuv1g5h0u2map48e68pgi-f31ye
  - Log entry 20813: process perl pid=17409 uid=945 src=156.115.34.231 args=q vanew3jyhfblbdi6q5trq3g-uk6of/8kc9ffp22gq3ctap
  - Log entry 32488: process sshd pid=26870 uid=210 src=58.150.65.66 args=-ke95uomt m8uyv6a yv3ofazvm-6wm65c3-ek0j-3f 870w
  - Log entry 38136: process nc pid=23949 uid=561 src=216.87.67.211 args=nqb960ip/fzryq 4ux2mc99n36jk8vpt5k0e9v0prv0b yhd
  - Log entry 82156: process sshd pid=18052 uid=582 src=27.194.78.232 args=gq0fuqvfb5x 1vc6k153kwc7vu178exjyhthz9pj-hwg8i7z
  - Log entry 70598: process nc pid=1317 uid=893 src=56.20.238.238 args=6oc-7gy3nf7ll 1fwiavq7msdz -gh62cziohsc771qhm1xo
  - Log entry 71130: process bash pid=30942 uid=296 src=120.102.166.161 args=p-ei-t1ckti6h55pavso0ocpyyh6-pwot2rrkfsigqyc6282
  - Log entry 82662: process sshd pid=7630 uid=336 src=105.91.20.143 args=ao0llmuslr3g1f 27qyqnys44o2bna4f10o8zu8ooere8tkr
  - Log entry 78698: process wget pid=15277 uid=451 src=97.175.254.97 args=ga jtz5xdcwtvadzffa2iae3vw-xvk1o0t491hcgv1t4srv9
  - Log entry 85234: process python3 pid=6341 uid=288 src=105.251.170.203 args=co61tpg bavq-yt9r/d61pwyf5-un22fby1/w 2k2/53yakr
  - Log entry 34644: process ruby pid=6025 uid=385 src=174.54.187.135 args=ic4w43ys5kbli6oglc6tdr6qgzfod9mazu8sp4gvtt1fi0bn
  - Log entry 20591: process nc pid=22141 uid=386 src=201.135.132.9 args=ogvq nmt3uzj0e5lq59v4ra26j0bpr3q7072/a2d6dz4zw f
  - Log entry 67637: process bash pid=15632 uid=105 src=185.86.118.25 args=i3r/kp5 7mp3 jzylr2sd4boj4xpc8l/-1mbi6m3xx0tmd-5
  - Log entry 26541: process nc pid=12551 uid=266 src=178.173.167.209 args=rvquz2djtem1m4icslpqq 9na7dp7j/ml18lw0e4xril84g 
  - Log entry 19662: process socat pid=28846 uid=294 src=7.72.33.155 args=3g0oziealdd97qiyn52pf4mst1iybmf/ig5245xml1oq1e/z
  - Log entry 33804: process bash pid=5324 uid=86 src=32.106.137.172 args=n1wfxid nqvy5/kxlr7jdd5c2w5w08/eqq6dsmhb-5aluzmh
  - Log entry 93713: process ruby pid=6107 uid=23 src=175.151.13.28 args=m7/str-4axo qa/x132fk02adrrds-8us4h85ml9re2gy8qq
  - Log entry 93740: process ruby pid=12128 uid=61 src=159.65.65.113 args=/3mvqr7kkzilm /o2rwf7p/gs9jgfg 65ee a8 25ku/6z-v
  - Log entry 76003: process ruby pid=14343 uid=20 src=39.79.3.84 args=cy8ix2ooi u7pyeti-ax0nvt/kfhmouip6ao-3k6ebhpabsa
  - Log entry 90860: process bash pid=15065 uid=328 src=151.51.251.246 args=1hhoydy jzh/0tsb35th-zkbvkicsmpr5ko0q57ozq3mhny5
  - Log entry 74026: process curl pid=19882 uid=659 src=172.220.174.41 args=96ios0n-1vjc/m-s8lzf3/n11wiceiscqza6da5x4wt937i3
  - Log entry 51873: process ruby pid=25853 uid=949 src=194.83.126.19 args=zjw2ib3xfla96f2yeqdy1x6y3 /v-/1ldnrxa0-oramuvvtc
  - Log entry 54464: process sshd pid=17390 uid=189 src=103.77.212.96 args=titdnmcnevvvt1q63 a 49iewn1ululef9ymm 0 k8i//l9f
  - Log entry 83802: process curl pid=2323 uid=270 src=181.82.93.17 args=tkae-0sapn8y5z3na9f0n3/y3z5h0bsqf-akpdzvau ftpd2
  - Log entry 25902: process socat pid=8372 uid=961 src=40.85.118.184 args=x4/vi hizbq  pp0j15s0s4hf6jcfg6y3u0pmxq1vgss59ns
  - Log entry 13760: process curl pid=12685 uid=434 src=212.41.219.167 args=ap2pmiseew35kj1oq72nuifpqg 1-4n9fl cghvt9us 32-j
  - Log entry 28454: process socat pid=3640 uid=506 src=185.45.20.163 args=5b-337 djl7thtgl5ea5-h31n/e421oxb7i7sftm/8df21zl
  - Log entry 20820: process nc pid=9880 uid=305 src=218.177.165.63 args=08v-9 dfp6om/ g5gi-xvnzg/aawwdn00b/vp-5l llq8c5 
  - Log entry 38814: process python3 pid=10190 uid=304 src=71.242.44.30 args=v2jsjx6dxmkozr53bm1ds/b33c5ht9eyxo/aa-gquos-3eoc
  - Log entry 79755: process sshd pid=12505 uid=795 src=29.249.115.223 args=a1t5u-gmc0mbtsfya67wbl6sxzgwb7ou17mepdj48tmri/yt
  - Log entry 10932: process ruby pid=20127 uid=643 src=25.214.181.108 args=2qvipo2fbbdy1so1t31u41amb3qn8lu16z94oodv95qgtb58
  - Log entry 59883: process perl pid=21027 uid=991 src=122.22.4.99 args=nfaz7ir5a1iht 29mmagq6bp1i29tc4acxfdtkci 15tx9zt
  - Log entry 28957: process nc pid=8354 uid=529 src=99.163.21.151 args=cwldavev8wipfpt/6r389/ epbq2bq1h-vculq-mon0c-qt9
  - Log entry 97044: process curl pid=24411 uid=63 src=146.191.220.170 args=qiys3hhh-50z -iv6wtukp/j a3mpj1utxv3tvjz5rrv90vp
  - Log entry 68072: process curl pid=16904 uid=135 src=161.122.137.192 args=81iea7i392vkprcgeftbo45c4j/zp0w0qxiifsznqjrxtvct
  - Log entry 33438: process python3 pid=17690 uid=600 src=92.249.116.157 args=tahz4xsg6a0zgwtuf/5-xi8pqwiusifskzahvdn 4wh03pip
  - Log entry 16282: process perl pid=29561 uid=855 src=47.79.167.182 args=td53662od6u9b9cxkkqfq5e/001qlr1th4lhlk00vsbz45s9
  - Log entry 47435: process nc pid=28701 uid=340 src=174.140.20.123 args=gwnpdjrczsrbuyn1q0xvkkdvxotn0lhww0uw61e6bl0ju-gf
  - Log entry 48583: process wget pid=3744 uid=738 src=67.163.54.237 args=xu8jh2kojjy6spp5e69keukfkifgm5i/z30rj0bebmtol 6u
  - Log entry 21726: process wget pid=5332 uid=526 src=90.47.255.179 args=wpbf93zo82ldghz/8dwutdod80hrtmnt7nfrd5n/308a0zz7
  - Log entry 57457: process curl pid=26279 uid=548 src=36.167.197.213 args=rqal-cboz3cyzje62gq3 uq4-1rfxm4pgsmuanppmrysz/jr

## Supplementary Technical Detail — Section 80

Automated correlation engine identified 47 related events in the 6-hour window.
Baseline traffic on port 37025: 2 connections per hour.
Observed traffic on port 4444: 190 connections during the incident window.
Statistical anomaly score: 0.835 (threshold 0.750).
Related CVE: CVE-2026-17921 — not yet patched on 19 internal hosts.
Affected subnet: 10.8.0.0/24 — 22 hosts in scope.
EDR telemetry: 5 alerts suppressed; 1 false positives removed.
  - Log entry 82762: process ruby pid=26747 uid=487 src=104.251.199.184 args=n1jv3gtg-0-4e/aiq8v1g/s/5xvwkdpzwclp1spohbarwf8g
  - Log entry 68362: process curl pid=4911 uid=994 src=215.244.171.159 args=r8zjz-ir1jkb52b9w2nl61/mk5ydkn1miwmr2cxtm2aa0loh
  - Log entry 36460: process ruby pid=4900 uid=719 src=218.103.245.138 args=85x/njt/4ohbb/wael8sbyhaqhu3wm x5vvqd0-rp79nsa3g
  - Log entry 81202: process python3 pid=7439 uid=86 src=195.214.252.22 args=a6tib-iwrm4dc5afb4a i72 3vov8iw/er5x1zpld h7qugf
  - Log entry 49008: process python3 pid=19830 uid=779 src=103.131.161.34 args=ssp2j0rf8p35spbf5xn9rp hu0b77refx44pu v-gx2c8had
  - Log entry 36524: process nc pid=11117 uid=310 src=13.126.89.130 args=cz-d5scupn7o7l4thfiae3l81of4g7c3hah c4m-8ntw5j41
  - Log entry 60232: process sshd pid=17802 uid=615 src=119.87.127.80 args=t6f/a9 4qolnp5wayz0 bj0pfotf9ot4cq33qu0xqswhopvs
  - Log entry 69955: process bash pid=25502 uid=760 src=93.251.155.254 args=3rle kcw3j163flx73i89v9hbvr0b7gnfzh-n-am7qkp-e2k
  - Log entry 84778: process bash pid=16810 uid=580 src=26.18.39.206 args=r43xqx7e1q8bgu57wbjiv/wy1-2bixqyiab5-h/2o2yc02ll
  - Log entry 87089: process wget pid=3386 uid=356 src=11.181.130.206 args=oo1pwx9n7p8dvq999ding3nmrie8u lvns/p67q946b1k5zl
  - Log entry 32325: process perl pid=3805 uid=644 src=104.137.158.244 args= 11laks6/ 56ox3nsbgkr45tbm8tjnxq0dn3c37dw7y5irat
  - Log entry 27855: process bash pid=11912 uid=214 src=40.240.88.48 args=1q63pkji0d983u/dxqt02n3zu78nxj22f6ybp0iy/ouhrk6-
  - Log entry 36540: process ruby pid=11900 uid=269 src=103.204.125.120 args=dirup-rlovcymza jbmczyb3lle5mersncalqvvgj0vwdz-e
  - Log entry 77676: process bash pid=9592 uid=310 src=146.59.49.135 args=6d2o0hr9gxnuioa03v3rc md5m9l6n4946mm1us1ih1hid-c
  - Log entry 89467: process ruby pid=16722 uid=456 src=54.226.240.97 args=ydf s 2v8mtlt5r3rzn1o-gzagzmqcr7q9ex6x5qvcl88tde
  - Log entry 34685: process sshd pid=2062 uid=214 src=3.106.72.74 args= c4n-brh0kuk e235ncu5ug9lw1ruyif2mfyv-rppwl0-bss
  - Log entry 36149: process sshd pid=31577 uid=913 src=29.255.172.114 args=8u6-q2/ww-dqhvezbgmhrlxq85gw5uv8s /azdx7s3j4sp 2
  - Log entry 68155: process sshd pid=18926 uid=824 src=12.52.105.233 args=4sa6yriqrydv-k-b2bsxt8wqhazj64-8hp9h762ap9lv8o1y
  - Log entry 23227: process bash pid=22617 uid=864 src=81.79.109.112 args=h7tb1lrnb1 9qves4e0ylw3-9fggd1e36-tjduqg7u85 lr8
  - Log entry 98016: process bash pid=6982 uid=666 src=26.207.80.157 args=pbgk2ashelzq9l77o2zq9s90ziu7lijnzl5o 0vz4ad5ivx 
  - Log entry 12581: process socat pid=27992 uid=537 src=173.238.3.234 args=9h/pc soq0t1pat0x/3i9ib w4c/53k1wzatuam04i7nyyvg
  - Log entry 93631: process curl pid=10363 uid=443 src=134.175.0.130 args=b29fxq7eva9mly28f/3jg041h-f2q14soiggfshgpx65lbpx
  - Log entry 38208: process ruby pid=2191 uid=330 src=123.186.208.217 args=r/e6vunyl e6iaurtooms/4oelejpex1j569j7b-a534uy0r
  - Log entry 50934: process wget pid=23477 uid=863 src=77.51.246.223 args=7hb/uw7rfg4uyhakr9 tg nwn3on-xdluz70kw5l3gb699xe
  - Log entry 50794: process bash pid=4816 uid=104 src=172.76.14.138 args=zoj1aspaxzdj85qq31rc- 0b6sr9pt9hj-je/02a wurna7n
  - Log entry 73690: process wget pid=22859 uid=397 src=40.248.112.70 args= i1yo45t1lo/ijjbjk4xnsjavtcu/cmf1599pxyvbbljns9l
  - Log entry 54628: process socat pid=18626 uid=515 src=22.137.245.102 args=3klk/0p4c6nx9haxnztproem2-2xzkc8/s2eflc9z/02gqa2
  - Log entry 73092: process bash pid=12566 uid=881 src=87.211.36.70 args=3r8-nl2y9l02fnns/7gmuynhjh8cjuobzq8oefr-/go5v/6v
  - Log entry 56295: process python3 pid=22926 uid=308 src=116.81.244.67 args=9wl- a6neq3j2pca 4i41 7xp15g0yt 3zofry/-04-cgcje
  - Log entry 72570: process python3 pid=16890 uid=360 src=3.244.138.228 args=urp1657 mfh3-29/5w4ge0h1euz-bj/hdxnf0t cj-xhladx
  - Log entry 51315: process wget pid=20549 uid=807 src=206.168.171.30 args=9qt39/9qxe8a8go 64o9jiw5rnqiicztuge52kyigg6lme9o
  - Log entry 44542: process socat pid=22389 uid=663 src=172.44.178.21 args=q7 q4r4hp4oh1mdotj3 id-s0ykk4x2gd2cuvgent1-x00tb
  - Log entry 23089: process perl pid=8396 uid=38 src=126.56.217.254 args=piaqacyavug16nj7z82v22s5rz/76lla/m-f/6sqio/u699l
  - Log entry 38919: process ruby pid=25546 uid=887 src=104.206.98.89 args=vlyxarq32ii87l1n32un0c/-pjxy1-0r/wjpd6h0pfag6xyj
  - Log entry 30061: process python3 pid=29367 uid=297 src=66.18.171.84 args=um58hbhzqafapltg9kg5v0ucy7cxh6br7vsn6h7jcn4sng z
  - Log entry 29688: process wget pid=5437 uid=20 src=207.215.230.189 args=s3ie1rqn2e-8pru42y8aoot014ez650oerkumd 1/ft/48yt
  - Log entry 73957: process bash pid=5053 uid=275 src=116.222.27.68 args=4yql ct6s0v2wdkawq31p/l1ecqqlkmi5jllvgwdsc61vl3m
  - Log entry 99545: process bash pid=23404 uid=564 src=222.143.183.140 args=4ecrq3kd184itlcoqscchqowqipp9d5 s-e7640/6s68g9wt
  - Log entry 45778: process ruby pid=6104 uid=341 src=6.33.187.34 args=jc0/i1-lzb9k717janezo/e0/j2wjz1iani50zk0agf43zh9
  - Log entry 98676: process nc pid=5425 uid=857 src=34.64.43.230 args=q6326f65wzo/r4w7lgu2vnee/ /v09ox5if/302be0sneui/
  - Log entry 69682: process nc pid=20879 uid=427 src=120.39.166.211 args=hjv daii-bsrxhanc4h1g-8d5r8i8y7kj7fj7/fwpla 0v4e
  - Log entry 96096: process socat pid=30412 uid=162 src=183.78.212.246 args=wjni8ceiy7 9zr0i7levqv5 0vwrunx7zctst0mzjs173pf8
  - Log entry 92920: process curl pid=1712 uid=459 src=206.98.136.118 args=tqw-6po16a6ynzg7- 6uwd-3dh-okbi3g09aio0wj7pzw7co
  - Log entry 50876: process perl pid=24675 uid=635 src=7.193.224.67 args=hjszh8lropjk3bwconbql0r0w3kk6brqzd48g2o7dnqy1thg
  - Log entry 84066: process python3 pid=24003 uid=249 src=206.137.192.220 args=a4-dos78c5030u/6omgbi2wztby64lj8/ kb1mcieyr4frye
  - Log entry 56823: process socat pid=31807 uid=678 src=55.151.172.127 args=d 0hxz7k13hd07417j64urvd exhrnqzklu7xa1-lg6pf7va
  - Log entry 97394: process curl pid=26740 uid=224 src=95.143.103.175 args=gf6zpsooba79f07yp076sqjputycm6ca7qzr 5th-s05/y2d
  - Log entry 44158: process bash pid=3587 uid=847 src=5.137.104.162 args=ua/19x3e4p-r9 lvk00pm9uvch6cjio5o/sbs f9/rwa53yx
  - Log entry 69244: process nc pid=1906 uid=27 src=164.209.118.8 args=b1auovo/qo0062gw8l1rm53/n48a/rtrklh11hzi3y7kybv7
  - Log entry 28652: process curl pid=8919 uid=243 src=140.131.12.192 args=hfwx72kjmb95dji-q8zbi5abr93h292fevwns85 c08jbzn4
  - Log entry 60843: process nc pid=8561 uid=47 src=218.153.232.125 args=tl7ol41ola9i5ocvpccrpk0s5mbrw54 -06i9h bvf85js1/
  - Log entry 69645: process perl pid=11985 uid=809 src=221.212.179.7 args=hm3v2s0/c/al01skma701ddwzw9l2 3ggm8 e1sbb8xp571k
  - Log entry 56159: process python3 pid=13855 uid=661 src=63.70.201.234 args=w-xk3djhd5230jlkadu6qosaez4rgq37zkkiv7ldcb9qa zi
  - Log entry 89218: process bash pid=13643 uid=71 src=71.224.134.122 args=vzesmeunqv5p2/f257ak6t5eip89jy82c4nq18ov9sb15rm7
  - Log entry 89344: process python3 pid=25703 uid=27 src=8.203.220.78 args=9m2au1ukq9wz74ecifxdcqo5ikodh a 05a-o2/tie nsjlk
  - Log entry 56112: process wget pid=2946 uid=931 src=118.108.246.206 args=xm3qoohp1scb/jth5-sg8i9w3uvz3giisrafzrylfdouzdxl
  - Log entry 15998: process nc pid=8297 uid=816 src=17.45.17.11 args=imw-96mgnksrizxct7 wiznvhq-f1t7mxpcj  umspew8cfe
  - Log entry 84702: process bash pid=3537 uid=695 src=61.134.32.120 args=d3446dwwt/0pxzj-7gcyd3qsobci/6cnx69g y6wm0cdm00f
  - Log entry 75508: process nc pid=25152 uid=163 src=205.18.133.128 args=48 uv-v44w6ttz5-c360d3nk8lmb0cjdpe7bjatfg6r5z2ae
  - Log entry 74088: process socat pid=12270 uid=450 src=137.5.179.144 args=yoykbt13/yorm3ld57bo8nu k3da82mg kl akkrafzr13r7