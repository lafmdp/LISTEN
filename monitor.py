import re, time, json, datetime, numpy as np
from tensorboardX import SummaryWriter
from utils import execute_cmd, parser, print_logs

if __name__ == '__main__':
    cur_time = f"{datetime.datetime.now().strftime('%m-%d%H:%M:%S')}"
    logger = SummaryWriter(f"./log/MachineMonitor_{cur_time}")
    args = parser()

    global_steps = 0
    while True:
        # load current config files
        with open("./config/monitor_config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)

        with open("./config/cmd_libiary.json", 'r', encoding='utf-8') as f:
            cmd_libiary = json.load(f)


        print_logs(f"\n----------------------------------", args.verbose, cur_level=0)
        cur_time = f"{datetime.datetime.now().strftime('%m-%d%H:%M:%S')}"
        print_logs(f"Current Time:{cur_time}", args.verbose, cur_level=0)
        # eval every machine
        for key, value in config.items():
            # record each cmd
            print_logs(f"Start monitor machine {key}!", args.verbose, 0)

            for cmd_key, cmd_value in cmd_libiary.items():
                print_logs(f"Monitor machine {key} with cmd {cmd_key}!", args.verbose, 1)
                data_to_record = []
                if "cpu_utils" in cmd_key:
                    repeat_times = 5
                else:
                    repeat_times = 1
                for i in range(repeat_times):
                    sentence = execute_cmd(key, value, cmd_value)
                    s = [float(s) for s in re.findall(r'-?\d+\.?\d*', sentence)]
                    print_logs(f"\n----, {cmd_key}, RES from ssh:, {sentence}, RES parse:, {s}", args.verbose, 2)
                    data_to_record.append(s)
                    time.sleep(1)
                data_to_record = np.array(data_to_record).mean(0).tolist()

                if len(data_to_record) == 1:
                    logger.add_scalar(f"{key}/{cmd_key}", data_to_record[0], global_step=global_steps)
                else:
                    for i, v in enumerate(list(data_to_record)):
                        logger.add_scalar(f"{key}/{cmd_key}_{i}", v, global_step=global_steps)

        print_logs(f"\n----------------------------------", args.verbose, cur_level=0)
        global_steps += 1
        time.sleep(3600 * args.monitor_interval)
