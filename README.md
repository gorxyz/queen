# Queen
## 𝙱𝚛𝚞𝚝𝚎𝚏𝚘𝚛𝚌𝚎 𝚊𝚝𝚝𝚊𝚌𝚔 𝚝𝚘 𝚒𝚗𝚜𝚝𝚊𝚐𝚛𝚊𝚖 𝚞𝚜𝚎𝚛𝚗𝚊𝚖𝚎 𝚠𝚒𝚝𝚑 𝙿𝚢𝚝𝚑𝚘𝚗
!TODO: improve tor server integration and spam undetection
## Dependencies
```sh
herbe(not required), python3-pip, tor(if u want tor server)
```
### systemd
```sh
sudo systemctl enable tor
```
### runit
```sh
sudo ln -s /etc/sv/tor /var/service/ && sudo sv up tor
```
## INSTALLATION
```sh
git clone https://github.com/sudurraaa/queen.git
```
```sh
cd queen/
```
```sh
pip3 install -r requirements.txt
```
## Launch
```sh
python3 queen.py --tor enable
```
```sh
python3 queen.py --tor disable
```
for help
```sh
python3 queen.py -h
```
