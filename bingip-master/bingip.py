#!/usr/bin/env python
#
# Queries an IP address on Bing and returns all the domains associated - currently limited to 50
#
import sys
from BeautifulSoup import BeautifulSoup
import urllib2
import urlparse
import argparse
import xml.dom.minidom

# function to identify parent host node in nmap xml
def get_parent_object_node(node):
    while node.parentNode:
        node = node.parentNode
        if node.nodeName == "host":
            return node

# function to perform the bing request - needs converting to the API really
def bing_request(ipaddr):
    # Perform the HTTP request to Bing
    url = 'http://www.bing.com/search?q=ip%3A'+ipaddr+'&go=&qs=n&sk=&sc=8-26&form=QBRE&filt=all'
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', cookie))
    response = opener.open(url)
    html = response.read()

    # Parse it with BeautifulSoup....mmm, beautiful
    soup = BeautifulSoup(html)
    divs = soup.findAll('div', attrs={'class':'sb_tlst'})

    # Loop through all the divs with class="sb_tlst" and find links
    for div in divs:
        url = BeautifulSoup(str(div)).find('a')['href']
        hostname = urlparse.urlparse(url).hostname
        domains.add(hostname) # add the domain to the set

# Process command arguments
parser = argparse.ArgumentParser(description='Queries an IP address on Bing and returns all the domains associated')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-i', '--ip', metavar='IP', default=False, help='The IP address to query')
group.add_argument('-f', '--file', metavar='filename', default=False, help='File containing IP addresses on new lines')
group.add_argument('-n', '--nmap_file', metavar='filename', default=False, help='Nmap XML file to parse for HTTP hosts')
parser.add_argument('-p', '--ports', metavar='p', default='80,443', help='Ports to recognise as a web server')
parser.add_argument('-r', '--raw', action='store_true', default=False, help='Print raw output')
args = parser.parse_args()

if args.file:
    try:
        f = open(args.file, 'r')
        targets = f.readlines()
        f.close()
    except Exception as e:
        print "couldn't process file %s:" % e
        sys.exit(1)
elif args.nmap_file:
    try:
        targets = []
        xml = xml.dom.minidom.parse(args.nmap_file)
        for port in xml.getElementsByTagName("port"):
            for portid in args.ports.split(','):
                if port.getAttribute("portid") == portid:
                    host_object = get_parent_object_node(port)
                    address_object = host_object.getElementsByTagName("address")
                    targets.append(address_object[0].getAttribute("addr"))
    except Exception as e:
        print "couldn't process nmap file %s" % e
        sys.exit(1)
else:
    targets = args.ip.split()

# Set some variables
cookie = "SRCHHPGUSR=NEWWND=0&NRSLT=50&SRCHLANG=&AS=1&ADLT=DEMOTE" # We set this so we get up to 50 results per page

# Where we store the results
domains = set()

# Our list of targets in a set to de-dupe
targets = set(targets)

# loop through our ip addresses
for ip in targets:
    ipaddr = ip.strip() 
    if args.raw is not True:
        print "%s" % ipaddr
        print "%s" % "-" * len(ipaddr)
    bing_request(ipaddr)

    # Print out our list of domains
    for i in domains:
        print i

    # reset domains
    domains.clear()
