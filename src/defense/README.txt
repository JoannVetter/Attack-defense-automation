Everything you need to install DVWA on a remote machine is here.

Make sure to edit the inventory file before you try to run the playbook, also make sure you have an SSH key to connect to your host (or a password).

You will have to slightly modifiy the ansible script to change the path of the copied files.

When you are ready you can use this :

ansible-playbook -i inventory.yml dvwa_install.yml  --ask-become-pass
