#!/usr/bin/env python
import sys, os
from docker import Client
import argparse
from requests.exceptions import ConnectionError

CGROUP_DIR = "/sys/fs/cgroup/memory/docker/"
CGROUP_FILES = {
    "memory.usage_in_bytes":"Usage In Bytes",
    "memory.max_usage_in_bytes":"Max Usage In Bytes",
    "memory.limit_in_bytes": "Limit In Bytes",
}

def print_info(args, container_id):
    container_dir = os.path.join(CGROUP_DIR, container_id)
    if args.cgroup_name:
        print_by_name(container_dir, args.cgroup_name)
    else:
        print_many(args, container_dir)

def print_by_name(container_dir, cgroup_name, message=None):
    file_name = os.path.join(container_dir, cgroup_name)
    if os.path.isfile(file_name):
        try:
            file = open(file_name, 'r')
            contents = file.read()
            file.close()
            print "%s: %s" % (cgroup_name if not message else message, contents.replace("\n", "\t").strip())
        except IOError as e:
            print "Could not open the cgroup file %s because of error %s" % (file_name, e)
    else:
        print "%s is not a file in the docker cgroup."

def print_many(args, container_dir):
    if args.verbose or args.list:
        files = os.listdir(container_dir)
        for file in files:
            if not args.list:
                print_by_name(container_dir, file)
            else:
                print file
    else:
        for cgroup_file, message in CGROUP_FILES.items():
            print_by_name(container_dir, cgroup_file, message)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Grab information about your docker containers.')
    parser.add_argument('--cgroup_name', help='Specify a particular information file you want to display')
    parser.add_argument('--verbose', action='store_true', help='Print all information available about a docker')
    parser.add_argument('--list', '-l', action='store_true', help='Only list all available cgroup options')
    parser.add_argument('--url', '-u', help='Specify how to connect to your docker', default='unix://var/run/docker.sock')
    args = parser.parse_args()

    try:
        c = Client(base_url=args.url)
        for container in c.containers():
            container_name = container['Names'][0]
            container_id = container['Id']
            print "\n\nContainer Name: %s\tContainer ID: %s" % (container_name, container_id[:6])
            print_info(args, container_id)
    except ConnectionError:
        print "You could not connect to your docker install via the specified url, or the default(unix://var/run/docker.sock)"
