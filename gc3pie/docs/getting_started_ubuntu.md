# Getting started with gc3pie on ubuntu 14.04/16.04

Install development packages:
```
sudo apt-get update

sudo apt-get install gcc g++ git python-dev libffi-dev libssl-dev
```    

Install gc3pie:
```
cd ~/

wget https://raw.githubusercontent.com/uzh/gc3pie/master/install.py

python install.py
```

Activate gc3pie: 
```
. ~/gc3pie/bin/activate
```

Check installation:
```
gc3utils --help
```

Install python-novaclient library:
```
pip install python-novaclient
```
***Note :** Latest version of python-novaclient library generates AttributeError: 'SessionClient' object has no attribute 'auth_token' when submittin jobs. In that case is needed to downgrade python-novaclient to version 6.0.0 as follows:*
```
pip install 'python-novaclient==6.0.0'
```

Create configuration file:
```
mkdir ~/.gc3/

wget https://github.com/bascomptelab/sciencecloud/raw/master/gc3pie/docs/gc3pie.conf -O ~/.gc3/gc3pie.conf

```

Edit configuration file
```
nano ~/.gc3/gc3pie.conf
```

Modify image_id parameter in resource [sciencecloud] section:
```
# - image_id of Ubuntu 14.04.04 (2017-05-19)
image_id=820738e3-0ef5-49d2-ab01-f780fa57d3d5
```
Save configuration file and exit:
```
^O
^X
```

Create a Key Pair and add it to the SSH Agent:
```
cd ~/.ssh

ssh-keygen -t rsa -f tutorial.key

chmod +400 ~/.ssh/tutorial.key.pub

ssh-add ~/.ssh/tutorial.key.pub

cat ~/.ssh/tutorial.key.pub
```
***Note:** If you need to start the ssh agent try:*
```
eval $(ssh-agent -s)
```

Import the key pair:
```
Log in to ScienceCloud web interface: https://cloud.s3it.uzh.ch

Browse to 'Access & y Security' -> 'Import Key Pairs':

Copy & paste the public Key:
```

Change authentication parameters in [sciencecloud] section in gc3pie.conf file:
```
vm_auth=ssh_user_ubuntu
keypair_name=your_key_pair_name
public_key=~/.ssh/your_key_pair_name.pub
```

Create/Copy basic-example files from repository:
```
mkdir ~/basic-example

cd ~/basic-example

wget https://github.com/bascomptelab/sciencecloud/raw/master/gc3pie/examples/bash/basic-example/do_multiple_sums.py

wget https://github.com/bascomptelab/sciencecloud/raw/master/gc3pie/examples/bash/basic-example/sum.sh
```    

Edit do_multiple_sums.py python script:
```
After line

        existing_file, positive_int

add this new line

        from gc3libs.quantity import GB

Change the last line

        stderr="stderr.txt")

by

        stderr="stderr.txt",
        requested_memory=1*GB)
```

Create exports.sh:
```
    nano exports.sh
```
Copy & paste this lines and replace your_user_name with yours:
```
export OS_AUTH_URL=https://cloud.s3it.uzh.ch:5000/v2.0
export OS_USERNAME=your_user_name
export OS_TENANT_NAME=bascompte.ieu.mnf.uzh
export OS_PROJECT_NAME=bascompte.ieu.mnf.uzh
read -p "Password: " -s mypassword
export OS_PASSWORD=$mypassword
unset OS_REGION_NAME
export PYTHONPATH=$PWD
```

Save and exit
```
^O
^X
```

Give execution permission (optional):
```
chmod +x exports.sh
```

Run export.sh and enter password:
```
. exports.sh
```

Launch python script resource sciencecloud:
```
python do_multiple_sums.py sum.sh 10 -r sciencecloud -C 5
```

Dump results:
```
cat sum.d*/stdout.txt
```

You should see something like this:
```   
67+9=76
93+66=159
80+16=96
14+62=76
15+26=41
43+73=116
7+64=71
25+3=28
69+88=157
7+73=80
```
    
