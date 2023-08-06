docopt_top= """Console monitor

Usage:
    monitor [options] <module> [<args>,...]
    monitor [--grep=<string> --grep=<string>] <module> [<args>...]
    monitor (-h | --help)
    monitor (-v | --version)

Global options:
    -h, --help  Show this screen
    -v, --version  Show version

    -g <string> --grep=<string> Grep the output
    -b, --batch Batch mode (output only once, don't iterate)

Commands:
    ip          External IP
    sensors     Sensors
    leases      DNSMasq leases
    resolve     DNS Resolve
    route       IP Route
    interfaces  Interfaces

See 'monitor help <module>' for more information on a specific module.
"""

docopt_ip="""
Usage: ip [options] [--output=<field>,...]

Options:
    -o <field>,... --output=<field>,...     Specify output fields [default: ip city country]
    -a --all  Display all fields
    -h, --help  Show this screen
    -v, --version  Show version
"""

docopt_sensors="""
Usage: 
    sensors [options]
    sensors [--chip=<string> --chip=<string>] [options]

Options:
    -c <string> --chip=<string>     Specify sensor chip
    -f --fans   Show only fan outputs
    -t --temp   Show only temperature outputs
    -h, --help  Show this screen
    -v, --version  Show version
"""

docopt_leases="""
Usage:
    leases [options]

Options:
    -s, --short  Skip HW address and show only ip address and hostname 
    -h, --help  Show this screen
    -v, --version  Show version
"""

docopt_resolve="""
Usage:
    resolve [options]

Options:
    -s, --systemd Use systemd-resolved (default)
    -r, --resolvconf  use resolvconf
    -h, --help  Show this screen
    -v, --version  Show version
"""

docopt_route="""
Usage:
    route [options] [--column=<number>,...]

Options:
    -c <number>,..., --column=<number>,...     Column numbers to include
    -h, --help  Show this screen
    -v, --version  Show version
"""

docopt_interfaces="""
Usage:
    interfaces
    interfaces [options]
Options:
    -h, --help  Show this screen
    -v, --version  Show version
"""

class OldMonitor:
    def __init__(self, argv=None):
        # If args is empty, show help
        if argv == None or len(argv) == 0:
            argv = ['-h']

        # Parse args
        args = docopt(docopt_top, argv=argv, version=__version__, options_first=True)

        # Get module
        module = args['<module>']
        opts = args['<args>']

        # Shift args if module is 'help'
        if module == 'help' and len(args['<args>']) > 0:
            module = args['<args>'][0]
            opts = args['<module>']

        # Run the module
        try:
            func = getattr(self, module)
        except AttributeError:
            print('Error: module not found "%s"' % (module))
        else:
            out = func(opts)
            # Grep the output and print
            out = subprocess.Popen(['grep', '\|'.join(args['--grep'])], stdin=out)
            out.communicate()

        return
    
    def show_usage(self):
        docopt(docopt_top, argv=['-h'], version=__version__, options_first=True)

    # Ip address
    def ip(self,argv):
        args = docopt(docopt_ip, argv=argv, version=__version__)
        if len(args['--output']) == 1:
            args['--output'] = args['--output'][0].split(',')
        if args['--all'] == True:
            args['--output'] = 'a'
        jsonData = json.loads( urllib.request.urlopen('https://ipinfo.io?token=3796117b2f73cb').read().decode() )
        out = TemporaryFile('w')
        for field in jsonData.keys():
            if field in args['--output'] or args['--output'] == 'a':
                out.write(field + ':\t' + str(jsonData.get(field)) + '\n')
        out.seek(0)
        return(out)

    # Sensors
    def sensors(self,argv):
        args = docopt(docopt_sensors, argv=argv, version=__version__)
        if len(args['--chip']) == 1:
            args['--chip'] = args['--chip'][0].split(',')
        if len(args['--chip']) > 0:
            sensors = subprocess.Popen(['sensors'] + args['--chip'], stdout=subprocess.PIPE)
        else:
            sensors = subprocess.Popen(['sensors'], stdout=subprocess.PIPE)
        if args['--fans'] ==  True:
            sensors = subprocess.Popen(['grep', '-i', '^fan'], stdin=sensors.stdout, stdout=subprocess.PIPE)
        if args['--temp'] ==  True:
            sensors = subprocess.Popen(['grep', '-i', '^temp'], stdin=sensors.stdout, stdout=subprocess.PIPE)
        return(sensors.stdout)

    # Leases
    def leases(self,argv):
        args = docopt(docopt_leases, argv=argv, version=__version__)
        leases = subprocess.Popen(['cat','/var/lib/misc/dnsmasq.leases'], stdout=subprocess.PIPE)
        if args['--short'] == True:
            leases = subprocess.Popen(['cut', '-d', ' ', '-f', '3,4'], stdin=leases.stdout, stdout=subprocess.PIPE)
        else:
            leases = subprocess.Popen(['cut', '-d', ' ', '-f', '2-4'], stdin=leases.stdout, stdout=subprocess.PIPE)

        return(leases.stdout)

    # Resolve
    def resolve(self,argv):
        args = docopt(docopt_resolve, argv=argv, version=__version__)
        if args['--resolvconf'] == True:
            resolve = subprocess.Popen(['cat', '/etc/resolv.conf'], stdout=subprocess.PIPE)
        else:
            resolve = subprocess.Popen(['systemd-resolve', '--status'], stdout=subprocess.PIPE)
            resolve = subprocess.Popen(['grep', 'DNS Server\|Link\|Global'], stdin=resolve.stdout, stdout=subprocess.PIPE)
        return(resolve.stdout)

    # Route
    def route(self, argv):
        args = docopt(docopt_route, argv=argv, version=__version__)
        if len(args['--column']) == 1:
            args['--column'] = args['--column'][0].split(',')
        awk_str = '{print $' + ',"\t",$'.join(args['--column']) + '}'
        routes = subprocess.Popen(['netstat', '-r', '-n'], stdout=subprocess.PIPE)
        if len(args['--column']) > 0:
            routes = subprocess.Popen(['awk', awk_str], stdin=routes.stdout, stdout=subprocess.PIPE)
        routes = subprocess.Popen(['tail', '-n+2'], stdin=routes.stdout, stdout=subprocess.PIPE)
        return(routes.stdout)

    # Interfaces
    def interfaces(self, argv):
        args = docopt(docopt_interfaces, argv=argv, version=__version__)
        ints = subprocess.Popen(['ip', '-4', '-h', '-o', '-c', '-br', 'a'], stdout=subprocess.PIPE)
        ints = subprocess.Popen(['awk', '{print $1,$2,$3}'], stdin=ints.stdout, stdout=subprocess.PIPE)
        return(ints.stdout)
