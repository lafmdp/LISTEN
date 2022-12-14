import argparse

def parser():
    parser = argparse.ArgumentParser(description="Running time configurations")
    parser.add_argument('--verbose', default=1, type=int, help="levels of verbose logs. 0: only basic message; 1: print parts of necessary messages; 2: debug mode for verbosing printing.")
    parser.add_argument('--monitor_interval', default=0.5, type=float, help="interval for monitoring the machines, by hours")

    args = parser.parse_args()

    return args