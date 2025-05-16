# run.py
import argparse
from shared.allocator import allocate
from monitoring.cli_dashboard import dashboard

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--json', action='store_true')
    ...
    args = p.parse_args()
    metrics = allocate()          # selects & runs strategies
    dashboard(metrics, json=args.json)

if __name__ == '__main__':
    main()
