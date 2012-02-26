import ldap
from pyramid.settings import asbool

def scope_converter(v):
    if 'subtree' in v.lower():
        return ldap.SCOPE_SUBTREE
    if 'onelevel' in v.lower():
        return ldap.SCOPE_ONELEVEL
    if 'base' in v.lower():
        return ldap.SCOPE_BASE
    raise ValueError('Unknown scope %s' % v)

def search_args_from_settings(settings, prefix, default_scope):
    def get_setting(name):
        return settings.get(prefix + name)

    search_args = []

    for key, converter, default in (
        ('%sbase_dn' % prefix, None, None), 
        ('%sfilter_tmpl' % prefix, None, None),
        ('%sscope' % prefix, scope_converter, default_scope),
        ):
            setting = get_setting(key)
            if setting is None:
                setting = default
            if setting is None:
                raise ValueError('Must specify %s for an LDAP search' % key)
            if converter is not None:
                setting = converter(setting)
            search_args.append(setting)
    return search_args

def setup_from_settings(config, settings, prefix='pyramid_ldap.'):

    def get_setting(name):
        return settings.get(prefix + name)

    pool_args = {}
    uri = get_setting('uri')
    pool_args['uri'] = uri
    if uri is None:
        raise ValueError('If you include pyramid_ldap, you must set a '
                         '%suri configuration key' % prefix)
    for name, converter in (
        ('bind', None), ('passwd', None), ('size', int), 
        ('retry_max', int), ('retry_delay', float), ('use_tls', asbool),
        ('timeout', int), ('use_pool', asbool),
        ):
        setting = get_setting(name)
        if setting is not None:
            if converter is not None:
                setting = converter(setting)
            pool_args[name] = setting

    config.ldap_setup_pool(**pool_args)
    login_search_args = search_args_from_settings(
        settings,
        prefix + 'login_search.',
        ldap.SCOPE_BASE
        )
    config.ldap_set_login_search(*login_search_args)
    groups_search_args = search_args_from_settings(
        settings,
        prefix + 'groups_search.',
        ldap.SCOPE_SUBTREE
        )
    config.ldap_set_groups_search(*groups_search_args)

def includeme(config):
    config.add_directive('setup_ldap_from_settings', setup_from_settings)
