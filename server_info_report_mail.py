import smtplib
from email.header import Header
from email.mime.text import MIMEText
 
import paramiko as paramiko
import multiprocessing.dummy as mp
 
 
class ServerMonitor(object):
 
    def distribute_task_to_host(self, server_dict):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(server_dict['ip'], server_dict['port'], server_dict['user'], server_dict['pwd'])
        exec_command = "top -b -i -n 1"
        stdin, stdout, stderr = ssh.exec_command(exec_command)
        string_list = stdout.readlines()
        string_str_0 = string_list[0]
        str_0_list = string_str_0.split('average:')
        load_average_str = ''.join(str_0_list[1].split()).replace('\n', '')
        load_average_list = load_average_str.split(',')
        load_average_list = [float(load_average_list[0]), float(load_average_list[1]), float(load_average_list[2])]
        string_str_3 = string_list[3]
        str_3_list = string_str_3.split()
 
        exec_hostname = "hostname"
        stdin, stdout, stderr = ssh.exec_command(exec_hostname)
        string_hostname_list = stdout.readlines()
        string_hostname_0 = string_hostname_list[0]
        string_hostname = string_hostname_0.strip().replace('\n', '')
 
        exec_ss_tcp_count = "ss -t -a | wc -l"
        stdin, stdout, stderr = ssh.exec_command(exec_ss_tcp_count)
        ss_tcp_count_list = stdout.readlines()
        ss_tcp_count_string = ss_tcp_count_list[0]
        ss_tcp_count = ss_tcp_count_string.strip().replace('\n', '')
 
        mem_dict = {
            "total": round(int(str_3_list[3]) / 1024, 2),
            "free": round(int(str_3_list[5]) / 1024, 2),
            "used": round(int(str_3_list[7]) / 1024, 2),
            "buffers": round(int(str_3_list[9]) / 1024, 2),
            "mem_used_percent": round(int(str_3_list[7]) / int(str_3_list[3]), 2),
        }
        final_dict = {
            "memory_info": mem_dict,
            "load_info": load_average_list,
            "hostname": string_hostname,
            "tcp_conn_total": ss_tcp_count,
        }
        return final_dict
 
 
    def get_mul_ssh_host_info(self, server_dict_list):
        p = mp.Pool(4)
        result_list = p.map(self.distribute_task_to_host, server_dict_list)
        p.close()
        p.join()
        return result_list
 
    def send_mail(self, msg):
        mail_host = "smtp.exmail.qq.com"
        mail_user = "xxx@xxx.cn"
        mail_pass = "xxx"
 
        sender = 'xxx@xxx.cn'
        receivers = ['xxx@xxx.cn']
 
        message = MIMEText(msg, 'plain', 'utf-8')
        message['From'] = Header("xxx@xxx.cn", 'utf-8')
        message['To'] = Header("test", 'utf-8')
 
        subject = 'ServerMonitor'
        message['Subject'] = Header(subject, 'utf-8')
 
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("email send successed")
        except smtplib.SMTPException:
            print("Error: can not send email!")
 
 
    def send_html_mail(self, msg):
        mail_host = "smtp.exmail.qq.com"
        mail_user = "xxx@xxx.cn"
        mail_pass = "xxx"
 
        sender = 'xxx@xxx.cn'
        receivers = ['xxx@xxx.cn']
 
        if type(msg) is not str:
            msg = str(msg)
        context = msg
        message = MIMEText(_text=context, _subtype="html", _charset="utf-8")
        message["Subject"] = Header(s="system info", charset="utf-8")
        message['From'] = Header("xxx@xxx.cn", 'utf-8')
        message['To'] = Header(";", 'utf-8')
 
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("email send successed")
        except smtplib.SMTPException:
            print("Error: can not send email!")
 
 
    def make_system_info_html(self, data_list):
        tr_list = []
        for item in data_list:
            string_tr = "<tr><td style='border: 1px solid; border-color: black; cellspacing:0;'>" + str(item['hostname']) + "</td><td style='border: 1px solid; border-color: black; cellspacing:0;'>" + str(item['tcp_conn_total']) + "</td><td style='border: 1px solid; border-color: black; cellspacing:0;'>" + str(item['memory_info']) + "</td><td style='border: 1px solid; border-color: black; cellspacing:0;'>" + str(item['load_info']) + "</td></tr>"
            tr_list.append(string_tr)
        final_tr_str = "".join(tr_list)
 
        html_str = """
            <html>
                <head>
                    <meta charset="UTF-8" name="viewport" content="width=device-width,initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no"/>
                </head>
                <body>
                    <h1 align="center">服务器信息</h1>
                    <table style="border:1px solid; align:center; weigth: 100%; border-collapse:collapse; margin: 0px auto;">
                    <tr>
                        <td style='border: 1px solid; border-color: black; cellspacing:0;'>主机名</td>
                        <td style='border: 1px solid; border-color: black; cellspacing:0;'>总tcp连接数</td>
                        <td style='border: 1px solid; border-color: black; cellspacing:0;'>内存信息</td>
                        <td style='border: 1px solid; border-color: black; cellspacing:0;'>负载信息</td>
                    </tr>
                    """ + final_tr_str + """
                    </table>
                </body>
            </html>
        """
        return html_str
 
 
 
 
if __name__ == '__main__':
    dict_list = [
        {'ip': "192.168.1.215", 'port': 22, 'user': 'xxx', 'pwd': 'xxx'},
        {'ip': "192.168.1.213", 'port': 22, 'user': 'xxx', 'pwd': 'xxx'},
    ]
    sm = ServerMonitor()
    result_list = sm.get_mul_ssh_host_info(dict_list)
    html_str = sm.make_system_info_html(result_list)
    sm.send_html_mail(html_str)
