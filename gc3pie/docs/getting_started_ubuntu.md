# Getting started with gc3pie on ubuntu 14.04

Install development packages:
```
sudo apt-get update

sudo apt-get install gcc g++ git python-dev libffi-dev libssl-dev
```    

Download gc3pie installer:
```
wget https://raw.githubusercontent.com/uzh/gc3pie/master/install.py
```

Install gc3pie:
```
python install.py
```

Activate gc3pie:
```
. /home/username/gc3pie/bin/activate
```

Install python-novaclient library:
```
pip install --upgrade pbr (optional)

pip install python-novaclient
```

If you get AttributeError: 'SessionClient' object has no attribute 'auth_token' then downgrade python-novaclient to version 6.0.0 if you get 
```
pip install 'python-novaclient==6.0.0'
```

Create directory
```
mkdir ~/.gc3/
```

Download configuration file:
``` 
wget https://github.com/bascomptelab/sciencecloud/raw/master/gc3pie/docs/gc3pie.conf

mv gc3pie.conf ~/.gc3/
```

Edit configuration file
```
nano ~/.gc3/gc3pie.conf
```

Modify image_id parameter in resource [sciencecloud] section in gc3pie.conf file:
```
# - image_id of Ubuntu 14.04.04 (2017-05-19)
image_id=820738e3-0ef5-49d2-ab01-f780fa57d3d5
```
Save configuration file and exit:
```
^O
^X
```

Create a key pair (follow instructions of ScienceCloud Web interface >> Access & y Security >> Import Key Pairs
```
Description:

Key Pairs are how you login to your instance after it is launched.

Choose a key pair name you will recognise and paste your SSH public key into the space provided.

SSH key pairs can be generated with the ssh-keygen command:

ssh-keygen -t rsa -f cloud.key

This generates a pair of keys: a key you keep private (cloud.key) and a public key (cloud.key.pub). Paste the contents of the public key file here.

After launching an instance, you login using the private key (the username might be different depending on the image you launched):

ssh -i cloud.key <username>@<instance_ip>
```
Example of how to create a key pair and adding it to the ssh agent:
```
cd ~/.ssh

ssh-keygen -t rsa -f tutorial.key

chmod +400 ~/.ssh/tutorial.key.pub

ssh-add ~/.ssh/tutorial.key.pub
```
If you need to start the ssh agent try:
```
eval $(ssh-agent -s)
```

Edit user and key pair in [sciencecloud] section in gc3pie.conf file:
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

add new line

        from gc3libs.quantity import GB

Change last line

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

Give execution permission:
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

Show results:
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
    
