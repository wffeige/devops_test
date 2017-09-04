#同步/root/devops/log_analyze脚本到每个节点

scp -r /root/devops/scripts/log_analyze 172.16.1.134:/root/devops/scripts/
scp -r /root/devops/scripts/log_analyze 172.16.1.135:/root/devops/scripts/
scp -r /root/devops/scripts/log_analyze 172.16.1.138:/root/devops/scripts/
echo "sync 172.16.1.134 is ok"
echo "sync 172.16.1.135 is ok"
echo "sync 172.16.1.138 is ok"
