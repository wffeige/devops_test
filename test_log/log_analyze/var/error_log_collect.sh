> /root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/ceph/ceph.audit.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/ceph/ceph-mon.ztx-controller-136.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/ceph/ceph.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/ceph/tmp/ceph.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/ceph/tmp/ceph-mon.ztx-controller-136.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/neutron/server.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/neutron/tmp/server.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/cinder/cinder-manage.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/cinder/volume.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/cinder/api.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/cinder/scheduler.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/nova/nova-scheduler.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/nova/nova-conductor.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/nova/nova-api.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/nova/nova-cert.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/nova/nova-consoleauth.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/nova/nova-novncproxy.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
awk -F " " '{if ($1=="2017-08-26" &&   $2>="00:00:00" && $2<="23:01:00" &&$4=="ERROR") print $0}' /var/log/nova/tmp/nova-api.log >>/root/devops/scripts/log_analyze/var/result_com_err.txt
cat /root/devops/scripts/log_analyze/var/result_com_err.txt |sort -t " " -k2 > /root/devops/scripts/log_analyze/var/sort_result.txt