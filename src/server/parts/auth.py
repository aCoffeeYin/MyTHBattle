# -*- coding: utf-8 -*-

# -- stdlib --
import logging

# -- third party --
# -- own --
from server.endpoint import Client
from server.utils import command


# -- code --
log = logging.getLogger('Auth')


class Auth(object):
    def __init__(self, core):
        self.core = core
        self._kedama_uid = -10032

        core.events.user_state_transition += self.handle_user_state_transition
        core.events.client_command['auth'] += self._auth

    def handle_user_state_transition(self, ev):
        u, f, t = ev

        if (f, t) == ('initial', 'connected'):
            from settings import VERSION
            core = self.core
            u.write(['thbattle_greeting', (core.options.node, VERSION)])
            u._[self] = {
                'uid': 0,
                'name': '',
                'kedama': False,
                'permissions': set(),
            }

        return ev

    # ----- Command -----
    @command('connected')
    def _auth(self, u: Client, token: str):
        core = self.core
        rst = core.backend.query('''
            query($token: String) {
                player(token: $token) {
                    id
                    user {
                        isActive
                        userPermissions {
                            codename
                        }
                        groups {
                            permissions {
                                codename
                            }
                        }
                    }
                    name
                }
            }
        ''', token=token)

        if not rst or rst['player']:
            u.write(['auth:error', {'error': 'invalid_credential'}])
            return

        rst = rst['player']

        if not rst['user']['isActive']:
            u.write(['auth:error', {'error': 'not_available'}])
        else:
            u.write(['auth:result', {'uid': rst['id'], 'name': rst['name']}])
            u._[self] = {
                'uid': int(rst['id']),
                'name': rst['name'],
                'kedama': False,
                'permissions': set(
                    [i['codename'] for i in rst['user']['userPermissions']] +
                    [i['codename'] for i in rst['user']['groups']['permissions']]
                ),
            }
            core.lobby.state_of(u).transit('authed')

    # ----- Public Methods -----
    def uid_of(self, u: Client) -> int:
        return u._[self]['uid']

    def name_of(self, u: Client) -> str:
        return u._[self]['name']

    def is_kedama(self, u: Client) -> bool:
        return u._[self]['kedama']

    # ----- Auxiliary Methods -----
    def set_auth(self, u: Client, uid=1, name='Foo', kedama=False, permissions=[]):
        '''
        Used by tests
        '''
        core = self.core
        assert core.lobby.state_of(u) == 'connected'
        u._[self] = {
            'uid': uid,
            'name': name,
            'kedama': kedama,
            'permissions': set(permissions),
        }
        core.lobby.state_of(u).transit('authed')
