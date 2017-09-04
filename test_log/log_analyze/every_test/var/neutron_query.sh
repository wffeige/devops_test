> /root/devops/scripts/log_analyze/every_test/var/neutron_result.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:59:59"   && $4 =="ERROR" ) print $0}' /var/log/neutron/server.log >>/root/devops/scripts/log_analyze/every_test/var/neutron_result.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:59:59"   && $4 =="ERROR" ) print $0}' /var/log/neutron/tmp/server.log >>/root/devops/scripts/log_analyze/every_test/var/neutron_result.txt
