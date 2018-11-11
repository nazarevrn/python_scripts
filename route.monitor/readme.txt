This script is check route table on cisco device, then compare values, and send results to host "route.monitor" on zabbix, 
and hosts using zabbix_sender.
To run route check on new host, add host to group "Route_check" and add Template_Cisco_Route.
Script starting by cron.
If you don't want see message "Route changed" in zabbix, run send_ok.py
2018 Roman Nazarev
