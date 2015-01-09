# Docker cgroup info
## A minimal tool for inspecting docker containers

## Boot2docker install
```
boot2docker ssh
git clone <this repo> docker_cgroup_info
wget http://www.tinycorelinux.net/5.x/x86/tcz/python.tcz && tce-load -i python.tcz && rm -f python.tcz
curl -LO https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py && sudo /usr/local/bin/python2.7 ez_setup.py && rm ez_setup.py
sudo easy_install pip
cd docker_cgroup_info
sudo pip install -r requirements.txt
./docker_cgroup_info
```
