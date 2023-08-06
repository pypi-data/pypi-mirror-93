import yaml
from pathlib import Path
from .util import join_nonempty

################################################################################
# Config system base classes

class ConfigError(Exception):
    pass


class ClassdataStrMixin:
    def __str__(self):
        return '\n'.join(self._get_str_lines())

    def _get_dict_for_str(self):
        return {k:v for k,v in self.__dict__.items() if not k.startswith('_')}

    def _get_str_lines(self, indent=0):
        for k, v in self._get_dict_for_str().items():
            get_child = getattr(v, '_get_str_lines', None)
            if get_child:
                yield '{}{}:'.format(' '*indent, k)
                yield from get_child(indent+2)
            else:
                yield '{}{}: {!r}'.format(' '*indent, k, v)


NODEFAULT = object()

class CfgBase(ClassdataStrMixin):
    def __init__(self, data):
        self._data = data
        self._populate()

    def _populate(self):
        pass

    def subkeyname(self, name):
        return join_nonempty('.', self.keyname, name)

    def cfg_get(self, key, default=NODEFAULT, cls=None):
        """Get an entry from the config data

        Parameters:
        key     name of the entry to get
        cls     optional class
        """
        try:
            value = self._data[key]
        except KeyError:
            if default is NODEFAULT:
                raise ConfigError("Missing key: {!r}".format(self.subkeyname(key)))
            value = default

        if cls and value is not None:
            # Ensure data is a dict unless the cls desires otherwise
            if not isinstance(value, getattr(cls, 'data_type', dict)):
                self.invalid_type(key, value)
            value = cls(data=value, name=key, parentnode=self)

        return value

    def cfg_get_path(self, key, default=NODEFAULT):
        """Get a path entry from the config data

        Parameters:
        key     name of the entry to get
        """
        val = self.cfg_get(key, default=default)
        if val is None:
            return None

        p = Path(val)

        if not p.is_absolute():
            # If the path is relative, it is taken relative to the
            # directory containing the config file
            p = self.cfgpath.parent / p

        return p.resolve()

    def raise_for_key(self, key, message):
        """Raise a ConfigError for the given sub-key"""
        raise ConfigError("{}: {}".format(self.subkeyname(key), message))

    def invalid_type(self, key, value):
        self.raise_for_key(key, "Invalid type: {}".format(type(value).__name__))


class CfgRoot(CfgBase):
    def __init__(self, data, cfgpath):
        self._cfgpath = cfgpath
        super().__init__(data)

    @property
    def cfgpath(self):
        return self._cfgpath

    @property
    def keyname(self):
        return ''


class CfgNode(CfgBase):
    def __init__(self, data, name, parentnode):
        assert name != None
        self._name = name
        assert parentnode != None
        self._parentnode = parentnode

        super().__init__(data)

    @property
    def cfgpath(self):
        return self._parentnode.cfgpath

    @property
    def keyname(self):
        return join_nonempty('.', self._parentnode.keyname, self._name)


class CfgDict(CfgNode, dict):
    def _get_dict_for_str(self):
        return self


class CfgList(CfgNode, list):
    data_type = list

    def _get_str_lines(self, indent=0):
        for i, v in enumerate(self):
            k = '[{}]'.format(i)
            get_child = getattr(v, '_get_str_lines', None)
            if get_child:
                yield '{}{}:'.format(' '*indent, k)
                yield from get_child(indent+2)
            else:
                yield '{}{}: {!r}'.format(' '*indent, k, v)



################################################################################
# adman config

class HasScope:
    default_scope = 'subtree'

    def check_scope(self):
        if not self.scope in ('subtree', 'one'):
            self.raise_for_key('scope', "Invalid scope: {}".format(self.scope))


class LdapAuthConfigFactory(type):
    def __call__(cls, data, name, parentnode, **kwargs):
        if cls is not LdapAuthConfig:
            return type.__call__(cls, data=data, name=name, parentnode=parentnode, **kwargs)

        # Factory mode

        # Kind of overkill to construct this object just to access one key...
        o = CfgNode(data=data, name=name, parentnode=parentnode)

        mode = o.cfg_get('mode')
        subcls = {
            'gssapi': GssapiLdapAuthConfig,
        }.get(mode)

        if not subcls:
            o.raise_for_key('mode', "Unrecognized mode: {}".format(mode))
        return subcls(data=data, name=name, parentnode=parentnode, mode=mode)


class LdapAuthConfig(CfgNode, metaclass=LdapAuthConfigFactory):
    def __init__(self, data, name, parentnode, mode):
        self.mode = mode
        super().__init__(data=data, name=name, parentnode=parentnode)


class GssapiLdapAuthConfig(LdapAuthConfig):
    def _populate(self):
        self.username = self.cfg_get('krb_username')
        self.keytab   = self.cfg_get_path('krb_keytab')
        self.cache    = self.cfg_get_path('krb_cache')


class UpnSuffixesConfig(CfgDict):
    def _populate(self):
        for container, d in self._data.items():
            self[container] = UpnSuffixConfig(data=d, name=container, parentnode=self)


class UpnSuffixConfig(CfgNode, HasScope):
    def __init__(self, data, name, parentnode):
        self.scope = self.default_scope
        if isinstance(data, str):
            self.suffix = data
        elif isinstance(data, dict):
            super().__init__(data=data, name=name, parentnode=parentnode)
            self.suffix = self.cfg_get('suffix')
            self.scope = self.cfg_get('scope', default=self.scope)
        else:
            parentnode.invalid_type(name, data)

        self.check_scope()


class PasswordExpConfig(CfgNode):
    def _populate(self):
        # days
        days = self.cfg_get('days')
        if isinstance(days, int):
            self.days = [days]
        elif isinstance(days, list):
            self.days = days
        else:
            self.invalid_type('days', days)
        self.days.sort(reverse=True)

        # template
        path = self.cfg_get_path('template_file')
        try:
            f = open(path, 'r')
        except OSError as e:
            self.raise_for_key('template_file', "Error reading template: {}".format(e))

        with f:
            self.template = f.read()


class SmtpConfig(CfgNode):
    def _populate(self):
        self.email_from = self.cfg_get('email_from')

        # Default to sending mail via SMTP server running on this host
        self.host = self.cfg_get('host', default='localhost')
        self.port = self.cfg_get('port', default=0)

        self.username = self.cfg_get('username', default=None)
        self.password = self.cfg_get('password', default=None)
        g = (self.username, self.password)
        if sum(bool(x) for x in g) not in (0, len(g)):
            self.raise_for_key(None, "If username or password are set, both must be set")

        self.encryption = self.cfg_get('encryption', default="").lower()
        if not self.encryption in ("", "ssl", "starttls"):
            self.raise_for_key('encryption', 'Invalid value: {}'.format(self.encryption))


def RangeConfig(data, name, parentnode):
    o = CfgNode(data=data, name=name, parentnode=parentnode)
    return range(o.cfg_get('min'), o.cfg_get('max'))


class ContainerConfigDict(CfgDict):
    def _populate(self):
        for container, d in self._data.items():
            self[container] = Container(data=d, name=container, parentnode=self)

    def iterate_containers(self):
        if len(self) == 0:
            # Not configured => search everything
            yield (None, 'subtree')
        else:
            for container, d in self.items():
                yield (container, d.scope)


class Container(CfgNode, HasScope):
    def __init__(self, data, name, parentnode):
        self.scope = self.default_scope
        if data is None:
            pass
        elif isinstance(data, dict):
            super().__init__(data=data, name=name, parentnode=parentnode)
            self.scope = self.cfg_get('scope', default=self.scope)
        else:
            parentnode.invalid_type(name, data)

        self.check_scope()


class IdAssignConfig(CfgNode):
    def _populate(self):
        self.uid_range = self.cfg_get('uid_range', cls=RangeConfig)
        self.gid_range = self.cfg_get('gid_range', cls=RangeConfig)
        self.computers = self.cfg_get('computers', default=True)
        self.only = self.cfg_get('only', default={}, cls=ContainerConfigDict)


class UserdirConfig(CfgNode):
    def _populate(self):
        self.basepath = self.cfg_get('basepath')
        self.only = self.cfg_get('only', default={}, cls=ContainerConfigDict)
        self.owner = self.cfg_get('owner', default=None)
        self.group = self.cfg_get('group', default=None)
        self.acl = self.cfg_get('acl', default=[])
        self.subdirs = self.cfg_get('subdirs', default=[], cls=UsersubdirConfig)


class UserdirsConfig(CfgList):
    def _populate(self):
        for i, ud in enumerate(self._data):
            self.append(UserdirConfig(data=ud, name=str(i), parentnode=self))

class UserSubdirConfig(CfgNode):
    def _populate(self):
        self.name = self.cfg_get('name')
        self.acl = self.cfg_get('acl', default=[])

class UsersubdirConfig(CfgList):
    def _populate(self):
        for i, d in enumerate(self._data):
            self.append(UserSubdirConfig(data=d, name=str(i), parentnode=self))


class Config(CfgRoot):
    def __init__(self, data, path):
        cfgpath = Path(path).resolve(strict=True)
        super().__init__(data=data, cfgpath=cfgpath)

    def _populate(self):
        self.domain = self.cfg_get('domain')

        self.changelog_path = self.cfg_get_path('changelog', default=None)

        self.id_assign = self.cfg_get('id_assign', cls=IdAssignConfig, default=None)

        self.ldap_auth = self.cfg_get('ldap_auth', cls=LdapAuthConfig)

        self.userdirs = self.cfg_get('userdirs', default=[], cls=UserdirsConfig)

        self.upn_suffixes = self.cfg_get('upn_suffixes', default={}, cls=UpnSuffixesConfig)

        self.pwexp = self.cfg_get('password_expiry_notification',
                default=None, cls=PasswordExpConfig)
        
        self.smtp = self.cfg_get('smtp', default=None, cls=SmtpConfig)

        if self.pwexp and not self.smtp:
            raise ConfigError("smtp required if password_expiry_notification is used")


    @classmethod
    def load(cls, path):
        try:
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
        except (IOError, yaml.YAMLError) as e:
            raise ConfigError(e)

        return cls(data, path)


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('config')
    args = ap.parse_args()

    try:
        cfg = Config.load(args.config)
    except ConfigError as e:
        raise SystemExit("Config error: {}".format(e))

    print(cfg)
