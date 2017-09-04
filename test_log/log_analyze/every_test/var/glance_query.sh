> /root/devops/scripts/log_analyze/every_test/var/glance_result.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:59:59"   && $4 =="ERROR" ) print $0}' /var/log/glance/registry.log >>/root/devops/scripts/log_analyze/every_test/var/glance_result.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:59:59"   && $4 =="ERROR" ) print $0}' /var/log/glance/api.log >>/root/devops/scripts/log_analyze/every_test/var/glance_result.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:59:59"   && $4 =="ERROR" ) print $0}' /var/log/glance/tmp/api.log >>/root/devops/scripts/log_analyze/every_test/var/glance_result.txt
