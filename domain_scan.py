import sys, os, platform

import conf
from conf import *
from queue import *
import asyncio
import aiodns
import asyncio
from async_dns.core import types
from async_dns.resolver import ProxyResolver

import asyncio
import ipaddress
import socket
import sys
import time


try:
    if sys.platform == "win32":
        import winloop as uvloop
        skip_uvloop = False
    else:
        import uvloop
        skip_uvloop = False
except ModuleNotFoundError:
    skip_uvloop = True


if sys.platform == 'win32':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

loop = asyncio.get_event_loop()
resolver = aiodns.DNSResolver(loop=loop)

"""
class DNSQueryLoop:
    def setUp(self):
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        self.loop = asyncio.new_event_loop()
        self.addCleanup(self.loop.close)
        self.resolver = aiodns.DNSResolver(loop=self.loop, timeout=5.0)
        self.resolver.nameservers = ['8.8.8.8']

    def tearDown(self):
        self.resolver = None

    def discovery_query_a(self):
        f = self.resolver.query('google.com', 'A')
        result = self.loop.run_until_complete(f)

    def discovery_query_async_await(self):
        async def f():
            return await self.resolver.query('google.com', 'A')
        result = self.loop.run_until_complete(f())
        self.assertTrue(result)

    def discovery_query_a_bad(self):
        f = self.resolver.query('hgf8g2od29hdohid.com', 'A')
        try:
            self.loop.run_until_complete(f)
        except aiodns.error.DNSError as e:
            self.assertEqual(e.args[0], aiodns.error.ARES_ENOTFOUND)

    def discovery_query_aaaa(self):
        f = self.resolver.query('ipv6.google.com', 'AAAA')
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)

    def discovery_query_cname(self):
        f = self.resolver.query('www.amazon.com', 'CNAME')
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)

    def discovery_query_mx(self):
        f = self.resolver.query('google.com', 'MX')
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)

    def discovery_query_ns(self):
        f = self.resolver.query('google.com', 'NS')
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)

    def discovery_query_txt(self):
        f = self.resolver.query('google.com', 'TXT')
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)

    def discovery_query_soa(self):
        f = self.resolver.query('google.com', 'SOA')
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)

    def discovery_query_srv(self):
        f = self.resolver.query('_xmpp-server._tcp.jabber.org', 'SRV')
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)

    def discovery_query_naptr(self):
        f = self.resolver.query('sip2sip.info', 'NAPTR')
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)

    def discovery_query_ptr(self):
        ip = '172.253.122.26'
        f = self.resolver.query(ipaddress.ip_address(ip).reverse_pointer, 'PTR')
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)

    def discovery_query_bad_type(self):
        self.assertRaises(ValueError, self.resolver.query, 'google.com', 'XXX')

    def discovery_query_txt_chaos(self):
        self.resolver = aiodns.DNSResolver(loop=self.loop)
        self.resolver.nameservers = ['1.1.1.1']
        f = self.resolver.query('id.server', 'TXT', 'CHAOS')
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)

    def discovery_query_bad_class(self):
        self.assertRaises(ValueError, self.resolver.query, 'google.com', 'A', "INVALIDCLASS")

    def discovery_query_timeout(self):
        self.resolver = aiodns.DNSResolver(timeout=0.1, tries=1, loop=self.loop)
        self.resolver.nameservers = ['1.2.3.4']
        f = self.resolver.query('google.com', 'A')
        started = time.monotonic()
        try:
            self.loop.run_until_complete(f)
        except aiodns.error.DNSError as e:
            self.assertEqual(e.args[0], aiodns.error.ARES_ETIMEOUT)
        # Ensure timeout really cuts time deadline. Limit duration to one second
        self.assertLess(time.monotonic() - started, 1)

    def discovery_query_cancel(self):
        f = self.resolver.query('google.com', 'A')
        self.resolver.cancel()
        try:
            self.loop.run_until_complete(f)
        except aiodns.error.DNSError as e:
            self.assertEqual(e.args[0], aiodns.error.ARES_ECANCELLED)

    def discovery_future_cancel(self):
        f = self.resolver.query('google.com', 'A')
        f.cancel()
        async def coro():
            await asyncio.sleep(0.1)
            await f
        try:
            self.loop.run_until_complete(coro())
        except asyncio.CancelledError as e:
            self.assertTrue(e)

    def discovery_query_twice(self):
        async def coro(self, host, qtype, n=2):
            for i in range(n):
                result = await self.resolver.query(host, qtype)
                self.assertTrue(result)
        self.loop.run_until_complete(coro(self, 'gmail.com', 'MX'))

    def discovery_gethostbyname(self):
        f = self.resolver.gethostbyname('google.com', socket.AF_INET)
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)

    def discovery_getaddrinfo_address_family_0(self):
        f = self.resolver.getaddrinfo('google.com')
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)
        self.assertTrue(len(result.nodes) > 1)

    def discovery_getaddrinfo_address_family_af_inet(self):
        f = self.resolver.getaddrinfo('google.com', socket.AF_INET)
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)
        self.assertTrue(all(node.family == socket.AF_INET for node in result.nodes))

    def discovery_getaddrinfo_address_family_af_inet6(self):
        f = self.resolver.getaddrinfo('google.com', socket.AF_INET6)
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)
        self.assertTrue(all(node.family == socket.AF_INET6 for node in result.nodes))

    def discovery_getnameinfo_ipv4(self):
        f = self.resolver.getnameinfo(('127.0.0.1', 0))
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)
        self.assertTrue(result.node)

    def discovery_getnameinfo_ipv6(self):
        f = self.resolver.getnameinfo(('::1', 0, 0, 0))
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)
        self.assertTrue(result.node)


    def discovery_gethostbyaddr(self):
        f = self.resolver.gethostbyaddr('127.0.0.1')
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)

    def discovery_gethostbyname_ipv6(self):
        f = self.resolver.gethostbyname('ipv6.google.com', socket.AF_INET6)
        result = self.loop.run_until_complete(f)
        self.assertTrue(result)

    def discovery_gethostbyname_bad_family(self):
        f = self.resolver.gethostbyname('ipv6.google.com', -1)
        with self.assertRaises(aiodns.error.DNSError):
            self.loop.run_until_complete(f)

#    def discovery_query_bad_chars(self):
#        f = self.resolver.query('xn--cardeosapeluqueros-r0b.com', 'MX')
#        result = self.loop.run_until_complete(f)
#        self.assertTrue(result)

"""
class DNSLoopStartup:
    """
    @brief      This Class is to Dns Loop Callback
    @param      name (name of the domain)
                nameservers (nameservers of the domain)
                loop (asyncio event loop)
                resolver (aiodns resolver object)
                tasks (list of tasks)
                future (list of future)
                records (list of records)
                domain (domain name)
                domain_name (domain name)
                domain_to_brute (domain to brute)
                result (result of the query)
                exc (exception)
                errno (error number)
    """


    def __init__(self):
        self.name = ""
        self.nameservers = ['127.0.0.1','1.1.1.1','8.8.8.8']
        self.loop = None
        self.resolver = None
        self.tasks = list()
        self.future = list()
        self.records = list()
        self.domain = "jennylab.me"
        self.domain_name = "jennylab.me"
        self.domain_to_brute = "jennylab.me"
        self.result = None
        self.exc = None
        self.errno = None

    def setUp(self):
        self.resolver = aiodns.DNSResolver()
        self.loop = asyncio.get_event_loop()
        #self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        self.loop = asyncio.new_event_loop()
        if conf.DEBUG:
            self.loop.set_debug(True)

        self.timeout =  int(os.environ.get('ASYNC_TIMEOUT', '5'))



        #(self.loop.close)
        self.resolver = aiodns.DNSResolver(loop=self.loop, timeout=5.0)
        self.resolver.nameservers = ['127.0.0.1','1.1.1.1','8.8.8.8']

    async def resolve(name, record_type):
        records = []
        name = await resolver.query(name, record_type)
        for n in name:
            records.append(n.host)
        return(records)

    def run(self):
        future = []
        #self.tasks.append(self.loop.create_task(self.resolve(self.domain_to_brute, 'NS')))
        #self.tasks.append(self.loop.create_task(self.resolve(self.domain_to_brute, 'MX')))
        self.tasks.append(self.loop.create_task(self.resolve("jennylab.me",'A')))
        #self.tasks.append(self.loop.create_task(self.resolve(self.domain_to_brute, 'CNAME')))
        self.loop.run_until_complete(asyncio.wait(self.tasks))

        for t in self.tasks:
            for self.domain_name in t.result():
                self.name = resolver.query(self.domain_name, 'A')
                self.name.add_done_callback(DNSLoopStartup.error_checker_callback)
                self.name.data = self.domain_name
            self.future.append(self.name)
        self.loop.run_until_complete(asyncio.wait(future))


    @staticmethod
    def error_checker_callback(future):
        if future.exception():
            exc = future.exception()
            errno = exc.args[0]

            if errno != 4:
                print("#{}, {}".format(errno, exc.args[1]))
        else:
            result = list(map(lambda x: (future.data, x.host), future._result))
            print(result)



if __name__ == '__main__':
    dns_scan = DNSLoopStartup()
    dns_scan.setUp()

    dns_scan.run()




"""
class DomainScan:
    def __init__(self,domains):
        if type(domains) == type(str()):
            domains = list(domains)
            self.domains = domains
            self.name = ""
        else:
            self.domains = domains

    async def query(self, query_type):
        return await resolver.query(self.name, query_type)

    def dns_query(self):
        asm_nop=0x90
        #coro = query('google.com', 'A')
"""


