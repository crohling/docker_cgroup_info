#!/usr/bin/env python
import sys, os
from docker import Client
import argparse

CGROUP_DIR = "/sys/fs/cgroup/memory/docker/"
CGROUP_FILES = {
    "memory.usage_in_bytes":"Usage In Bytes: ",
    "memory.max_usage_in_bytes":"Max Usage In Bytes: ",
    "memory.limit_in_bytes": "Limit In Bytes: ",
}

def print_info(args, container_id):
    container_dir = os.path.join(CGROUP_DIR, container_id)
    if args.cgroup_name:
        print_by_name(container_dir, args.cgroup_name)
    else:
        print_many(args, container_dir)

def print_by_name(container_dir, cgroup_name):    
    file = open(os.path.join(container_dir,cgroup_name), 'r')
    contents = file.read()
    file.close()
    print "%s: %s" % (cgroup_name, contents.replace("\n", "\t").strip())

def print_many(args, container_dir):
    if args.verbose:
        files = os.listdir(container_dir)
        for file in files:
            print_by_name(container_dir, file)
    else:
        for cgroup_file, message in CGROUP_FILES.items():
            file = open(os.path.join(container_dir, cgroup_file), 'r')
            contents = file.read()
            file.close()
            print message, contents.replace("\n", "\t").strip()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Grab information about your docker containers.')
    parser.add_argument('--cgroup_name', help='Specify a particular information file you want to display')
    parser.add_argument('--verbose', type=bool, help='Print all information available about a docker', default=False)
    args = parser.parse_args()

    c = Client(base_url='unix://var/run/docker.sock')
    for container in c.containers():
        container_name = container['Names'][0]
        container_id = container['Id']
        print "\n\nContainer Name: %s\tContainer ID: %s" % (container_name, container_id[:6])
        print_info(args, container_id)
