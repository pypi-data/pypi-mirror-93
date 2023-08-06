# MIT LICENSE
#
# Copyright 1997 - 2020 by IXIA Keysight
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE. 
from uhd_restpy.base import Base
from uhd_restpy.files import Files


class RsvpEroSubObjectsList(Base):
    """Rsvp ERO Sub-Objects
    The RsvpEroSubObjectsList class encapsulates a list of rsvpEroSubObjectsList resources that are managed by the system.
    A list of resources can be retrieved from the server using the RsvpEroSubObjectsList.find() method.
    """

    __slots__ = ()
    _SDM_NAME = 'rsvpEroSubObjectsList'
    _SDM_ATT_MAP = {
        'AsNumber': 'asNumber',
        'Count': 'count',
        'DescriptiveName': 'descriptiveName',
        'Ip': 'ip',
        'LeafIp': 'leafIp',
        'LocalIp': 'localIp',
        'LooseFlag': 'looseFlag',
        'Name': 'name',
        'P2mpIdAsIp': 'p2mpIdAsIp',
        'P2mpIdAsNum': 'p2mpIdAsNum',
        'PrefixLength': 'prefixLength',
        'Type': 'type',
    }

    def __init__(self, parent):
        super(RsvpEroSubObjectsList, self).__init__(parent)

    @property
    def AsNumber(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): AS
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['AsNumber']))

    @property
    def Count(self):
        """
        Returns
        -------
        - number: Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Count'])

    @property
    def DescriptiveName(self):
        """
        Returns
        -------
        - str: Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offer more context.
        """
        return self._get_attribute(self._SDM_ATT_MAP['DescriptiveName'])

    @property
    def Ip(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): IP
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['Ip']))

    @property
    def LeafIp(self):
        """
        Returns
        -------
        - list(str): Leaf IP
        """
        return self._get_attribute(self._SDM_ATT_MAP['LeafIp'])

    @property
    def LocalIp(self):
        """
        Returns
        -------
        - list(str): Local IP
        """
        return self._get_attribute(self._SDM_ATT_MAP['LocalIp'])

    @property
    def LooseFlag(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Loose Flag
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['LooseFlag']))

    @property
    def Name(self):
        """
        Returns
        -------
        - str: Name of NGPF element, guaranteed to be unique in Scenario
        """
        return self._get_attribute(self._SDM_ATT_MAP['Name'])
    @Name.setter
    def Name(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Name'], value)

    @property
    def P2mpIdAsIp(self):
        """
        Returns
        -------
        - list(str): P2MP ID As IP
        """
        return self._get_attribute(self._SDM_ATT_MAP['P2mpIdAsIp'])

    @property
    def P2mpIdAsNum(self):
        """
        Returns
        -------
        - list(str): P2MP ID displayed in Integer format
        """
        return self._get_attribute(self._SDM_ATT_MAP['P2mpIdAsNum'])

    @property
    def PrefixLength(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Prefix Length
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['PrefixLength']))

    @property
    def Type(self):
        """
        Returns
        -------
        - obj(uhd_restpy.multivalue.Multivalue): Type: IP or AS
        """
        from uhd_restpy.multivalue import Multivalue
        return Multivalue(self, self._get_attribute(self._SDM_ATT_MAP['Type']))

    def update(self, Name=None):
        """Updates rsvpEroSubObjectsList resource on the server.

        This method has some named parameters with a type: obj (Multivalue).
        The Multivalue class has documentation that details the possible values for those named parameters.

        Args
        ----
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))

    def find(self, Count=None, DescriptiveName=None, LeafIp=None, LocalIp=None, Name=None, P2mpIdAsIp=None, P2mpIdAsNum=None):
        """Finds and retrieves rsvpEroSubObjectsList resources from the server.

        All named parameters are evaluated on the server using regex. The named parameters can be used to selectively retrieve rsvpEroSubObjectsList resources from the server.
        To retrieve an exact match ensure the parameter value starts with ^ and ends with $
        By default the find method takes no parameters and will retrieve all rsvpEroSubObjectsList resources from the server.

        Args
        ----
        - Count (number): Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
        - DescriptiveName (str): Longer, more descriptive name for element. It's not guaranteed to be unique like -name-, but may offer more context.
        - LeafIp (list(str)): Leaf IP
        - LocalIp (list(str)): Local IP
        - Name (str): Name of NGPF element, guaranteed to be unique in Scenario
        - P2mpIdAsIp (list(str)): P2MP ID As IP
        - P2mpIdAsNum (list(str)): P2MP ID displayed in Integer format

        Returns
        -------
        - self: This instance with matching rsvpEroSubObjectsList resources retrieved from the server available through an iterator or index

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._select(self._map_locals(self._SDM_ATT_MAP, locals()))

    def read(self, href):
        """Retrieves a single instance of rsvpEroSubObjectsList data from the server.

        Args
        ----
        - href (str): An href to the instance to be retrieved

        Returns
        -------
        - self: This instance with the rsvpEroSubObjectsList resources from the server available through an iterator or index

        Raises
        ------
        - NotFoundError: The requested resource does not exist on the server
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._read(href)

    def get_device_ids(self, PortNames=None, AsNumber=None, Ip=None, LooseFlag=None, PrefixLength=None, Type=None):
        """Base class infrastructure that gets a list of rsvpEroSubObjectsList device ids encapsulated by this object.

        Use the optional regex parameters in the method to refine the list of device ids encapsulated by this object.

        Args
        ----
        - PortNames (str): optional regex of port names
        - AsNumber (str): optional regex of asNumber
        - Ip (str): optional regex of ip
        - LooseFlag (str): optional regex of looseFlag
        - PrefixLength (str): optional regex of prefixLength
        - Type (str): optional regex of type

        Returns
        -------
        - list(int): A list of device ids that meets the regex criteria provided in the method parameters

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._get_ngpf_device_ids(locals())
