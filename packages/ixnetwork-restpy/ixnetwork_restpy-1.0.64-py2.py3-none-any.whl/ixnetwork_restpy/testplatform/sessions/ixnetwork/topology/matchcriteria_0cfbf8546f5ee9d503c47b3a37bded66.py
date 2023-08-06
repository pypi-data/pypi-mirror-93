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
from ixnetwork_restpy.base import Base
from ixnetwork_restpy.files import Files


class MatchCriteria(Base):
    """Match
    The MatchCriteria class encapsulates a required matchCriteria resource which will be retrieved from the server every time the property is accessed.
    """

    __slots__ = ()
    _SDM_NAME = 'matchCriteria'
    _SDM_ATT_MAP = {
        'Count': 'count',
        'Description': 'description',
        'DisplayName': 'displayName',
        'IsEditable': 'isEditable',
        'IsEnabled': 'isEnabled',
        'IsRequired': 'isRequired',
        'Name': 'name',
    }

    def __init__(self, parent):
        super(MatchCriteria, self).__init__(parent)

    @property
    def Field(self):
        """
        Returns
        -------
        - obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.field_f65a45047b747ab6446cd586626ccd2d.Field): An instance of the Field class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.field_f65a45047b747ab6446cd586626ccd2d import Field
        return Field(self)

    @property
    def MatchCriteria(self):
        """
        Returns
        -------
        - obj(ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.matchcriteria_0cfbf8546f5ee9d503c47b3a37bded66.MatchCriteria): An instance of the MatchCriteria class

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        from ixnetwork_restpy.testplatform.sessions.ixnetwork.topology.matchcriteria_0cfbf8546f5ee9d503c47b3a37bded66 import MatchCriteria
        return MatchCriteria(self)._select()

    @property
    def Count(self):
        """
        Returns
        -------
        - number: Number of elements inside associated multiplier-scaled container object, e.g. number of devices inside a Device Group.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Count'])

    @property
    def Description(self):
        """
        Returns
        -------
        - str: Description of the field.
        """
        return self._get_attribute(self._SDM_ATT_MAP['Description'])
    @Description.setter
    def Description(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Description'], value)

    @property
    def DisplayName(self):
        """
        Returns
        -------
        - str: Display name used by GUI.
        """
        return self._get_attribute(self._SDM_ATT_MAP['DisplayName'])

    @property
    def IsEditable(self):
        """
        Returns
        -------
        - bool: Information on the requirement of the field.
        """
        return self._get_attribute(self._SDM_ATT_MAP['IsEditable'])
    @IsEditable.setter
    def IsEditable(self, value):
        self._set_attribute(self._SDM_ATT_MAP['IsEditable'], value)

    @property
    def IsEnabled(self):
        """
        Returns
        -------
        - bool: Enables disables the field.
        """
        return self._get_attribute(self._SDM_ATT_MAP['IsEnabled'])
    @IsEnabled.setter
    def IsEnabled(self, value):
        self._set_attribute(self._SDM_ATT_MAP['IsEnabled'], value)

    @property
    def IsRequired(self):
        """
        Returns
        -------
        - bool: Information on the requirement of the field.
        """
        return self._get_attribute(self._SDM_ATT_MAP['IsRequired'])
    @IsRequired.setter
    def IsRequired(self, value):
        self._set_attribute(self._SDM_ATT_MAP['IsRequired'], value)

    @property
    def Name(self):
        """
        Returns
        -------
        - str: Name of packet field
        """
        return self._get_attribute(self._SDM_ATT_MAP['Name'])
    @Name.setter
    def Name(self, value):
        self._set_attribute(self._SDM_ATT_MAP['Name'], value)

    def update(self, Description=None, IsEditable=None, IsEnabled=None, IsRequired=None, Name=None):
        """Updates matchCriteria resource on the server.

        Args
        ----
        - Description (str): Description of the field.
        - IsEditable (bool): Information on the requirement of the field.
        - IsEnabled (bool): Enables disables the field.
        - IsRequired (bool): Information on the requirement of the field.
        - Name (str): Name of packet field

        Raises
        ------
        - ServerError: The server has encountered an uncategorized error condition
        """
        return self._update(self._map_locals(self._SDM_ATT_MAP, locals()))
