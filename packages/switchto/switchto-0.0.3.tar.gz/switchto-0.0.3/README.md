# switchto

switch between dev and prod environments from command line.

# Installation

`pip install switchto`

# How it works

It edits your hosts file locally on Windows, Linux and Mac.

# Usage

## Add entry

`switchto -s my.website.com dev:127.0.0.1 team:192.168.1.100 prod:`

This will create 3 entries for your website domain, named "dev", "team" and "prod".
An empty string indicates to remove the entry from the hosts file once you run switchto that rule.

## Switching from production to dev environment and back

`switchto dev`

Will add the following entry to your hosts:

`127.0.0.1 my.website.com`

Once you want to go back to production, you can:

`switchto prod`

## Remove entries

You cannot remove entires from the config file, you can however set the rule to an empty string:

`switchto -s my.website.com team:`

Note: settings are saved in .s2.json on HOME or HOMEPATH directory.

## Listing config

`switchto -l`

To list everything, or:

`switchto -l regex`

Which will list all rules matching that regex.

## CNAMEs

Currently, switchto works only via hosts, which do not support redirecting domains to other domains, but only by IP address.
You can create a rule with a target domain, but it will be resolved once you create the rule, and also you would have to pass "-y" to confirm this:

`switchto -y -s my.website.com dev:my.website.local dev`

Note the "dev" at the end, which specifies to make the switch instantly, rather than running "switchto dev" afterwards.
