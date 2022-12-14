import os

def execute_cmd(key, value, cmd):
    if "port" in value.keys():
        cmd_to_execute = f"ssh -p{value['port']} -o ConnectTimeout=5 {value['user']}@{key} {cmd}"
    else:
        cmd_to_execute = f"ssh -o ConnectTimeout=5 {value['user']}@{key} {cmd}"

    print("CMD to execute:", cmd_to_execute)
    res = os.popen(cmd_to_execute).read()
    return res


def print_logs(message, sys_level=1, cur_level=1):
    """

    :param message: logs to be printed.
    :param cur_level: level of this message, 0: common message that will always be printed, 1: optional to be printed, 2: to be printed only when necessary (i.e., debug logs).
    :param sys_level: level of current running system, 0: strictly print only necessary message; 1: optionally print; 2: debugging mode.
    :return:
    """
    if cur_level <= sys_level:
        print(message)
