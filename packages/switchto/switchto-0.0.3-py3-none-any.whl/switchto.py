import os
import re
import sys
import json
import socket
import argparse
import platform

home_path = os.environ.get('HOME') or os.environ.get('HOMEPATH')
config_path = os.path.join(home_path, '.s2.json')

if not os.path.exists(config_path):
    config = {}
else:
    with open(config_path, 'r') as f:
        config = json.load(f)

def get_hosts_path():
    if platform.system() == 'Windows':
        return r'C:\Windows\system32\drivers\etc\hosts'

    return '/etc/hosts'

class HostsEditor:
    def __init__(self):
        self.fh = None
        self.lines = []
        self.skip_lines = []
        self.map = {}
        
    def load(self):
        with open(get_hosts_path(), 'r') as f:
            data = f.read()
            
        self.lines = data.split('\n')
        lineno = -1
        for line in self.lines:
            lineno += 1
            pre_cmnt = line.split('#')[0].strip()
            parts = pre_cmnt.split(' ')
            if len(parts) < 2:
                continue

            # ignore spaces in between (spaces around already stripped)
            ip, domain = parts[0], parts[-1]
            domain = domain.lower()
            if domain in self.map:
                print('WARNING: duplicate entry for %s @ lines %d and %d' % (domain, self.map[domain][0], lineno), file=sys.stderr)

            self.map[domain] = (lineno, ip, domain)
        
    def save(self):
        new_lines = []
        for i in range(len(self.lines)):
            if i not in self.skip_lines:
                new_lines.append(self.lines[i])

        with open(get_hosts_path(), 'w') as f:
            # NOTE: open with 'r' and 'w' on Windows will handle '\r' before '\n'
            f.write('\n'.join(new_lines))
        
    def set(self, domain, ip):
        domain = domain.lower()
        line = '%s %s' % (ip, domain)
        entry = self.map.get(domain)
        if entry:
            lineno, old_ip, domain = entry
            self.lines[lineno] = line
        else:
            self.lines.append(line)

    def remove(self, domain):
        if domain not in self.map:
            return

        lineno = self.map[domain][0]
        self.skip_lines.append(lineno)

def set_rules(domain, rules_dests, resolve):
    if domain not in config:
        config[domain] = {}

    for rule_dest in rules_dests:
        # TODO: check ':' exists
        if ':' not in rule_dest:
            print('expecting format rule:dest, got: "%s"' % rule_dest, file=sys.stderr)
            return

        rule, dest = rule_dest.split(':')
        # super simple IP regex
        # (empty destinations means delete entry)
        if dest and not re.match('^[\d\.:]+$', dest):
            if resolve:
                original_host = dest
                # TODO: it might be a good idea to keep "CNAME" in s2.json and
                # resolve it only before writing to hosts
                dest = socket.gethostbyname(original_host)
                print('resolved "%s" to %s' % (original_host, dest))
            else:
                # this is because I'm using hosts file, not a DNS which would allow CNAMEs
                # maybe next time... ;)
                print('cannot set domain to resolve to another domain. pass -y to resolve "%s" now' % dest, file=sys.stderr)
                return

        config[domain][rule] = dest

    save_config()

def save_config():
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

def list_rules(filters):
    if not filters:
        return config

    # so I can use ^$ in multiline regex
    filters = '\n'.join(filters)
    output = {}
    for domain, rules in config.items():
        for rule in rules:
            if re.match('^%s$' % domain, filters) or re.match('^%s$' % rule, filters, re.MULTILINE):
                if domain not in output:
                    output[domain] = {}

                output[domain][rule] = config[domain][rule]

    return output

def print_rules(rules):
    print(json.dumps(rules, indent=2))

def switchto(rule):
    hosts = HostsEditor()
    hosts.load()

    insert_rules = []
    remove_domains = []
    for domain, rules in config.items():
        # TODO: consider adding "-f" so if and only if specified, when rule is
        # undefined (as opposed to empty string) it will remove the entry from hosts
        if rule not in rules or not config[domain][rule]:
            remove_domains.append(domain)
        else:
            dest = config[domain][rule]
            insert_rules.append((domain, dest))

    for domain in remove_domains:
        hosts.remove(domain)
    
    for domain, dest in insert_rules:
        hosts.set(domain, dest)

    hosts.save()

def main():
    parser = argparse.ArgumentParser(description='redirect domains to dev servers and back to production')
    parser.add_argument('-l', '-list', dest='list', nargs='*',
                        help='list [rule|domain [...]]')
    # TODO: verbosity is always a good idea
    #parser.add_argument('-v', '-verbose', dest='verbose', action='store_true',
    #                    help='verbose')
    parser.add_argument('-s', '-set', dest='set', nargs='+',
                        help='set domain rule:dest [rule:dest [...]]')
    parser.add_argument('-y', '-yes', dest='yes', action='store_true',
                        help='whether or not to convert target hosts to IP')
    parser.add_argument('to', nargs='?',
                        help='rule')

    args = parser.parse_args()

    if args.set:
        set_rules(args.set[0], args.set[1:], args.yes)

    if args.list is not None:
        rules = list_rules(args.list)
        print_rules(rules)

    if args.to:
        switchto(args.to)

if __name__ == '__main__':
    main()
