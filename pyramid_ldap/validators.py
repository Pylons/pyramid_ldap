import colander

import logging

try:
    import ldap
except ImportError:  # pragma: no cover
    # this is for benefit of being able to build the docs on rtd.org
    # copied from __init__.py
    class ldap(object):
        LDAPError = Exception
        SCOPE_ONELEVEL = None
        SCOPE_BASE = None
        SCOPE_SUBTREE = None


logger = logging.getLogger(__name__)

null = colander.null
Invalid = colander.Invalid

class LdapScope(colander.GlobalObject):
    _ldapScopes = {'base': 'ldap.SCOPE_BASE',
                   'one': 'ldap.SCOPE_ONELEVEL',
                   'onelevel': 'ldap.SCOPE_ONELEVEL',
                   'sub': 'ldap.SCOPE_SUBTREE',
                   'subtree': 'ldap.SCOPE_SUBTREE',
                   'SCOPE_BASE': 'ldap.SCOPE_BASE',
                   'SCOPE_ONELEVEL': 'ldap.SCOPE_ONELEVEL',
                   'SCOPE_SUBTREE': 'ldap.SCOPE_SUBTREE'}

    def __init__(self):
        super(LdapScope, self).__init__(ldap)

    def deserialize(self, node, cstruct):
        cstr2 = self._ldapScopes.get(cstruct, cstruct)
        return super(LdapScope, self).deserialize(node, cstr2)

class PrintingString(colander.String):
    """ A non blank string """
    def deserialize(self, node, cstruct):
        if isinstance(cstruct, colander.string_types):
            cstruct = cstruct.strip()
        if not cstruct:
            return null
        return colander.String.deserialize(self, node, cstruct)


class Boolean(colander.SchemaType):
    """ A type representing a boolean object.

    During deserialization, a value in the set (``false``, ``0``) will
    be considered ``False``.  Anything else is considered
    ``True``. Case is ignored.

    Serialization will produce ``true`` or ``false`` based on the
    value.

    If the :attr:`colander.null` value is passed to the serialize
    method of this class, the :attr:`colander.null` value will be
    returned.

    The subnodes of the :class:`colander.SchemaNode` that wraps
    this type are ignored.
    """

    false_reprs = frozenset(('false', 'f', 'no', 'n', '0'))

    def serialize(self, node, appstruct):
        if appstruct is null:
            return null

        return appstruct and 'true' or 'false'

    def deserialize(self, node, cstruct):
        if cstruct is null or cstruct is None:
            return null
        try:
            result = str(cstruct)
        except:
            raise Invalid(node,
                          _('${val} is not a string', mapping={'val':cstruct})
                          )

        result = result.lower()

        if result in self.false_reprs:
            return False

        return True


class ForgivingMapping(colander.Mapping):
    """A forgiving mapping, modeled along the lines suggested
    by chrism in https://lists.repoze.org/pipermail/repoze-dev/2010-October/003599.html
    """
    def __init__(self, unknown='ignore', empty='skip'):
        self.unknown = unknown
        self.empty = empty

    def _set_empty(self, value):
        if not value in ('skip', 'preserve'):
            raise ValueError(
                'empty attribute must be one of "skip" or "preserve"')
        self._empty = value

    def _get_empty(self):
        return self._empty

    empty = property(_get_empty, _set_empty)

    def _set_unknown(self, value):
        if not value in ('ignore', 'raise', 'preserve'):
            raise ValueError(
                'unknown attribute must be one of "ignore", "raise", '
                'or "preserve"')
        self._unknown = value

    def _get_unknown(self):
        return self._unknown

    unknown = property(_get_unknown, _set_unknown)

    def _impl(self, node, value, callback):
        value = self._validate(node, value)

        error = None
        result = {}

        for num, subnode in enumerate(node.children):
            name = subnode.name
            subval = value.pop(name, null)

            try:
                _val = callback(subnode, subval)
                if _val is not null or self.empty == 'preserve':
                    result[name] = _val
            except Invalid as e:
                if error is None:
                    error = Invalid(node)
                error.add(e, num)

        if self.unknown == 'raise':
            if value:
                raise Invalid(
                    node,
                    _('Unrecognized keys in mapping: "${val}"',
                      mapping={'val':value})
                    )

        elif self.unknown == 'preserve':
            result.update(value)

        if error is not None:
            raise error

        return result

class Schema(colander.Schema):
    schema_type = ForgivingMapping

class ConnectionData(Schema):
    """ Connection parameters schema """
    uri = colander.SchemaNode(colander.String())
    bind = colander.SchemaNode(PrintingString(), missing=null)
    passwd = colander.SchemaNode(PrintingString(), missing=null)
    pool_size = colander.SchemaNode(colander.Int(), missing=null)
    retry_max = colander.SchemaNode(colander.Int(), missing=null)
    retry_delay = colander.SchemaNode(colander.Float(), missing=null)
    use_tls = colander.SchemaNode(Boolean(), missing=null)
    timeout = colander.SchemaNode(colander.Float(), missing=null)
    use_pool = colander.SchemaNode(Boolean(), missing=null)

class QueryData(Schema):
    """ Query parameters schema """
    filter_tmpl = colander.SchemaNode(PrintingString(), missing=null)
    scope = colander.SchemaNode(LdapScope(), missing=null)
    cache_period = colander.SchemaNode(colander.Float(), missing=null)
    search_after_bind = colander.SchemaNode(Boolean(), missing=null)

    def validator(self, node, cstruct):
        if not ('filter_tmpl' in cstruct or 'entry_tmpl' in cstruct):
            raise colander.Invalid("At least one of filter_tmpl "
                                   "or entry_tmpl must be present")
