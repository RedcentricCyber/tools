# Bingip

Uses the bing.com ip search capability to return a list of domains hosted on that IP address.

Takes a number of arguments:
<pre>

  --ip/-i						single IP address
  --file/-f					file containing IP addresses, each on new line
  --nmap_file/-n		nmap xml output. Searches for tcp/80 or tcp/443 and uses this as target
  --ports/-p				override port 80 and 443 above. Separate ports by comma

</pre>

## Example Usage

### Single IP Address

Here we use lb.wordpress.com's IP as there'll be loads of virtual hosts on that.

<pre>
bingip.py -i 72.233.2.58
72.233.2.58
-----------
blog-imfdirect.imf.org
blog.gcflearnfree.org
businessbuilderclub.co.uk
sarahockler.com
centertheatre.org
thesewingdivas.wordpress.com
hollywoodlife.com
...continues...
</pre>

### Specify a file of IPs

lb.wordpress.com has a number of IP addresses so specify them in a file like this:

<pre>
74.200.243.251
76.74.254.123
74.200.244.59
</pre>

Then process it with:

<pre>
bingip.py -f /tmp/ips
74.200.243.251
--------------
blackberry.wordpress.org
satyamshot.wordpress.com
businessbuilderclub.co.uk
74.200.244.59
-------------
monaghanmotorclub.net
wessexcancer.org
www.standrewswatford.org.uk
76.74.254.123
-------------
brightonmtb.org
deborahdunleavy.org
pinkacademy.co.uk
coventryhalf.com
</pre>

### Doing it Raw

If you just want a list without the headings use -r

<pre>
bingip.py -f /tmp/ips -rckberry.wordpress.org
satyamshot.wordpress.com
businessbuilderclub.co.uk
physicsmadeeasy.wordpress.com
charlestownprimary.wordpress.com
jannettesrareyarns.wordpress.com
gamechef.wordpress.com

</pre>

### Parsing an Nmap XML file

<pre>
nmap -p 80 -oX bingip_example.xml scanme.nmap.org
</pre>

Now pass the file generated as an argument and bingip will automatically
extract hosts with web server ports (it's pretty basic at this point)
<pre>
bingip.py --nmap_file bingip_example.xml 
74.207.244.221
--------------
scanme.nmap.org 
</pre>


