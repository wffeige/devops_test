

from collect_log import Controller_Node

con = Controller_Node()

con.generate_script_rel()
con.message_src_rel()
con.httpd_src_rel()
con.rabbitmq_src_rel()
