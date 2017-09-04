> /root/devops/scripts/log_analyze/every_test/var/nova_result.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:59:59"   && $4 =="ERROR" ) print $0}' /var/log/nova/nova-scheduler.log >>/root/devops/scripts/log_analyze/every_test/var/nova_result.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:59:59"   && $4 =="ERROR" ) print $0}' /var/log/nova/nova-conductor.log >>/root/devops/scripts/log_analyze/every_test/var/nova_result.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:59:59"   && $4 =="ERROR" ) print $0}' /var/log/nova/nova-api.log >>/root/devops/scripts/log_analyze/every_test/var/nova_result.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:59:59"   && $4 =="ERROR" ) print $0}' /var/log/nova/nova-cert.log >>/root/devops/scripts/log_analyze/every_test/var/nova_result.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:59:59"   && $4 =="ERROR" ) print $0}' /var/log/nova/nova-consoleauth.log >>/root/devops/scripts/log_analyze/every_test/var/nova_result.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:59:59"   && $4 =="ERROR" ) print $0}' /var/log/nova/nova-novncproxy.log >>/root/devops/scripts/log_analyze/every_test/var/nova_result.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:59:59"   && $4 =="ERROR" ) print $0}' /var/log/nova/tmp/nova-api.log >>/root/devops/scripts/log_analyze/every_test/var/nova_result.txt
