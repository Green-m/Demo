sudo cp /etc/bashrc /etc/bashrc.bak
sudo tee -a /etc/bashrc <<EOF
#history  
USER_IP=\`who -u am i 2>/dev/null| awk '{print $NF}'|sed -e 's/[()]//g'\`   
HISTFILESIZE=4000  
HISTSIZE=4000  
HISTTIMEFORMAT="%F %T ${USER_IP} \`whoami\` "  
export HISTTIMEFORMAT  
EOF
source /etc/bashrc
