The command to launch the playbook is the following : 

ansible-playbook -i inventory.yml attack_install.yml  --ask-become-pass

However, in order for this command to work, you need to edit inventory.yml properly by setting the IP of the
attacker machine you want to setup with the right port. Also, since there is no parameter for the attack script
so far, you will need to change manually the target IP there.

Make sure you have a SSH key configured to access the machine you are trying to reach. 

The sudo password will be asked, if you do not need one just type whatever, Ansible needs one to work.
