import netaddr


class RobotFrameworkNetAddr():
    ''' Wrapper functions to access a selection of the python netaddr library from robot framework.

    Most of the functionality from the netaddr IPNetwork, IPAddress and EUI classes are implemented
    along with a couple of extra functions to provide more ease of use in robot framework.
    '''

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    # netaddr.IPNetwork class
    @staticmethod
    def ipnetwork_broadcast(addr, **kwargs):
        '''Returns the broadcast address of the given subnet.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs).broadcast

    @staticmethod
    def ipnetwork_cidr(addr, **kwargs):
        '''Returns the network in cidr format.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask) |  10.0.0.0/255.255.255.0   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs).cidr

    @staticmethod
    def ipnetwork_hostmask(addr, **kwargs):
        '''Returns the hostmask.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs).hostmask

    @staticmethod
    def ipnetwork_info(addr, **kwargs):
        '''Returns a dict with info about the network.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs).info

    @staticmethod
    def ipnetwork_ip(addr, **kwargs):
        '''Returns the ip part the IPNetwork object.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs).ip

    @staticmethod
    def ipnetwork_is_link_local(addr, **kwargs):
        '''Check if the address is a link local address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs).is_link_local()

    @staticmethod
    def ipnetwork_is_loopback(addr, **kwargs):
        '''Check if the address is a loopback address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs).is_loopback()

    @staticmethod
    def ipnetwork_is_multicast(addr, **kwargs):
        '''Check if the address is a multicast address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs).is_multicast()

    @staticmethod
    def ipnetwork_is_private(addr, **kwargs):
        '''Check if the address is a private address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs).is_private()

    @staticmethod
    def ipnetwork_is_reserved(addr, **kwargs):
        '''Check if the address is a reserved address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs).is_reserved()

    @staticmethod
    def ipnetwork_is_unicast(addr, **kwargs):
        '''Check if the address is a unicast address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs).is_unicast()

    @staticmethod
    def ipnetwork_netmask(addr, **kwargs):
        '''Returns the subnetmask of the subnet.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs).netmask

    @staticmethod
    def ipnetwork_network(addr, **kwargs):
        '''Returns the network address of the subnet.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs).network

    @staticmethod
    def ipnetwork_prefixlen(addr, **kwargs):
        '''Returns the prefix length of the subnet.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs).prefixlen

    @staticmethod
    def ipnetwork_size(addr, **kwargs):
        '''Returns the number of addresses in the subnet.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs).size

    @staticmethod
    def ipnetwork_version(addr, **kwargs):
        '''Returns the IP version of the network (4 or 6).

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs).version

    @staticmethod
    def ipnetwork_is_network_addr(addr, **kwargs):
        '''Returns if the provided addr is the network address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        net = netaddr.IPNetwork(addr, **kwargs)
        return net.ip == net.network

    @staticmethod
    def ipnetwork_is_valid_ipv4(addr, **kwargs):
        '''Returns if the provided addr is valid for IPv4.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options, should not contain the version keyword  |  - |  -   |
        '''
        try:
            netaddr.IPNetwork(addr, version=4, **kwargs)
        except:
            return False
        else:
            return True

    @staticmethod
    def ipnetwork_is_valid_ipv6(addr, **kwargs):
        '''Returns if the provided addr is valid for IPv6.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  fe80::1/48   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options, should not contain the version keyword  |  - |  -   |
        '''
        try:
            netaddr.IPNetwork(addr, version=6)
        except:
            return False
        else:
            return True

    @staticmethod
    def ipnetwork_previous(addr, **kwargs):
        '''Returns subnet one lower than the one provided with addr.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        try:
            prev_net = netaddr.IPNetwork(addr, **kwargs).previous()
        except:
            return False
        else:
            return prev_net

    @staticmethod
    def ipnetwork_next(addr, **kwargs):
        '''Returns subnet one higher than the one provided with addr.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs | passed to IPNetwork constructor, see netaddr docs for options  |  - |  -   |
        '''
        try:
            next_net = netaddr.IPNetwork(addr, **kwargs).next()
        except:
            return False
        else:
            return next_net

    @staticmethod
    def ipnetwork_in_network(addr, addr2, kwargs_addr1={}, kwargs_addr2={}):
        '''Checks if network addr2 overlaps with in addr.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | addr2 | address (ip/mask or prefixlen) |  10.0.0.0/24   |  -   |
        | kwargs_addr1 | passed to IPNetwork constructor for addr1, see netaddr docs for options  |  - |  -   |
        | kwargs_addr2 | passed to IPNetwork constructor for addr2, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPNetwork(addr, **kwargs_addr1) in netaddr.IPNetwork(addr2, **kwargs_addr2)

    # netaddr.IPAddress class
    @staticmethod
    def ipaddress_bin(addr, **kwargs):
        '''Returns ip in binary.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.0   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPAddress(addr, **kwargs).bin

    @staticmethod
    def ipaddress_bits(addr, **kwargs):
        '''Returns ip series of bits grouped together in octets (ipv4) or hextets (ipv6).

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.0   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPAddress(addr, **kwargs).bits()

    @staticmethod
    def ipaddress_info(addr, **kwargs):
        '''Returns a dict with info about the IP address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.0   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPAddress(addr, **kwargs).info

    @staticmethod
    def ipaddress_is_hostmask(addr, **kwargs):
        '''Checks if the IP address is a hostmask.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.0   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPAddress(addr, **kwargs).is_hostmask()

    @staticmethod
    def ipaddress_is_link_local(addr, **kwargs):
        '''Checks if the IP address is a link local address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.0   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPAddress(addr, **kwargs).is_link_local()

    @staticmethod
    def ipaddress_is_loopback(addr, **kwargs):
        '''Checks if the IP address is a loopback address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.0   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPAddress(addr, **kwargs).is_loopback()

    @staticmethod
    def ipaddress_is_multicast(addr, **kwargs):
        '''Checks if the IP address is a multicast address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.0   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPAddress(addr, **kwargs).is_multicast()

    @staticmethod
    def ipaddress_is_netmask(addr, **kwargs):
        '''Checks if the IP address is a netmask.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.0   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPAddress(addr, **kwargs).is_netmask()

    @staticmethod
    def ipaddress_is_private(addr, **kwargs):
        '''Checks if the IP address is a private address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.0   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPAddress(addr, **kwargs).is_private()

    @staticmethod
    def ipaddress_is_reserved(addr, **kwargs):
        '''Checks if the IP address is a reserved address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.0   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPAddress(addr, **kwargs).is_reserved()

    @staticmethod
    def ipaddress_is_unicast(addr, **kwargs):
        '''Checks if the IP address is a unicast address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.0   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPAddress(addr, **kwargs).is_unicast()

    @staticmethod
    def ipaddress_reverse_dns(addr, **kwargs):
        '''Returns a reverse dns notation of the IP address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.0   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPAddress(addr, **kwargs).reverse_dns

    @staticmethod
    def ipaddress_version(addr, **kwargs):
        '''Returns the IP version of the IP address (4 or 6).

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.0   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPAddress(addr, **kwargs).version

    @staticmethod
    def ipaddress_words(addr, **kwargs):
        '''Returns a octets (IPv4) or hextets (IPv6) set of decimal values.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.0   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPAddress(addr, **kwargs).words

    @staticmethod
    def ipaddress_add(addr, amount, **kwargs):
        '''Add a number to an IP address to get a higher or lower (if provided with a negative amount) IP.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.0   |  -   |
        | amount | the amount to add |  10   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.IPAddress(addr, **kwargs) + int(amount)

    @staticmethod
    def ipaddress_is_valid_ipv4(addr):
        '''Checks if addr is a valid IPv4 address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.0   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.valid_ipv4(addr)

    @staticmethod
    def ipaddress_is_valid_ipv6(addr):
        '''Checks if addr is a valid IPv6 address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  fe80::1   |  -   |
        | kwargs | passed to IPAddress constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.valid_ipv6(addr)

    @staticmethod
    def ipaddress_in_network(addr, netw):
        '''Checks if addr is in subnet netw.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the IP address |  10.0.0.200   |  -   |
        | netw | the network |  10.0.0.0/24   |  -   |
        '''
        return netaddr.IPAddress(addr) in netaddr.IPNetwork(netw)

    # netaddr.EUI class
    @staticmethod
    def eui_bin(addr, **kwargs):
        '''Returns addr in binary.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the mac address |  00-01-02-AA-BB-CC   |  -   |
        | kwargs | passed to EUI constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.EUI(addr, **kwargs).bin

    @staticmethod
    def eui_bits(addr, **kwargs):
        '''Returns addr in grouped bits.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the mac address |  00-01-02-AA-BB-CC   |  -   |
        | kwargs | passed to EUI constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.EUI(addr, **kwargs).bits()

    @staticmethod
    def eui_ei(addr, **kwargs):
        '''Returns the addr's EI part.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the mac address |  00-01-02-AA-BB-CC   |  -   |
        | kwargs | passed to EUI constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.EUI(addr, **kwargs).ei

    @staticmethod
    def eui_eui64(addr, **kwargs):
        '''Returns the addr's EUI64.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the mac address |  00-01-02-AA-BB-CC   |  -   |
        | kwargs | passed to EUI constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.EUI(addr, **kwargs).eui64()

    @staticmethod
    def eui_iab(addr, **kwargs):
        '''Returns the addr's IAB (if available).

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the mac address |  00-01-02-AA-BB-CC   |  -   |
        | kwargs | passed to EUI constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.EUI(addr, **kwargs).iab

    @staticmethod
    def eui_info(addr, **kwargs):
        '''Returns a dict with info on the addr.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the mac address |  00-01-02-AA-BB-CC   |  -   |
        | kwargs | passed to EUI constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.EUI(addr, **kwargs).info

    @staticmethod
    def eui_ipv6(addr, prefix, **kwargs):
        '''Returns an IPv6 address by combining a provided IPv6 prefix with this addr.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the mac address |  00-01-02-AA-BB-CC   |  -   |
        | prefix | ipv6 prefix in hex |  0xfc000000000000000000000000000000  |  -   |
        | kwargs | passed to EUI constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.EUI(addr, **kwargs).ipv6(prefix)

    @staticmethod
    def eui_ipv6_link_local(addr, **kwargs):
        '''Returns an IPv6 link local address based on this addr.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the mac address |  00-01-02-AA-BB-CC   |  -   |
        | kwargs | passed to EUI constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.EUI(addr, **kwargs).ipv6_link_local()

    @staticmethod
    def eui_is_iab(addr, **kwargs):
        '''Check if the addr is IAB.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the mac address |  00-01-02-AA-BB-CC   |  -   |
        | kwargs | passed to EUI constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.EUI(addr, **kwargs).is_iab()

    @staticmethod
    def eui_modified_eui64(addr, **kwargs):
        '''Returns modified eui64 of this addr.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the mac address |  00-01-02-AA-BB-CC   |  -   |
        | kwargs | passed to EUI constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.EUI(addr, **kwargs).modified_eui64()

    @staticmethod
    def eui_oui(addr, **kwargs):
        '''Returns the OUI of this addr.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the mac address |  00-01-02-AA-BB-CC   |  -   |
        | kwargs | passed to EUI constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.EUI(addr, **kwargs).oui

    @staticmethod
    def eui_packed(addr, **kwargs):
        '''Returns the addr in packed format.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the mac address |  00-01-02-AA-BB-CC   |  -   |
        | kwargs | passed to EUI constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.EUI(addr, **kwargs).packed

    @staticmethod
    def eui_value(addr, **kwargs):
        '''Returns the value of the addr in decimal.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the mac address |  00-01-02-AA-BB-CC   |  -   |
        | kwargs | passed to EUI constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.EUI(addr, **kwargs).value

    @staticmethod
    def eui_version(addr, **kwargs):
        '''Returns the version of the addr.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the mac address |  00-01-02-AA-BB-CC   |  -   |
        | kwargs | passed to EUI constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.EUI(addr, **kwargs).version

    @staticmethod
    def eui_words(addr, **kwargs):
        '''Returns addr in a set of decimal values.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the mac address |  00-01-02-AA-BB-CC   |  -   |
        | kwargs | passed to EUI constructor, see netaddr docs for options  |  - |  -   |
        '''
        return netaddr.EUI(addr, **kwargs).words

    @staticmethod
    def eui_is_valid(addr):
        '''Returns if addr is a valid MAC address.

        *Arguments*
        | argument | Description |  Example  |  Default value
        | addr | the mac address |  00-01-02-AA-BB-CC   |  -   |
        '''
        return netaddr.valid_mac(addr)
