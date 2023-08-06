import typing

from transitions import Machine

from ...interfaces import IStateMachine


class StateMachine(IStateMachine):

    readonly_states: list = []

    def __init__(self, context, **kwargs):
        self._context = context
        self._request = context.request
        self._app = context.request.app
        initial = self.state or self.states[0]
        kwargs.update(
            {
                "model": self,
                "transitions": self.transitions,
                "states": self.states,
                "initial": initial,
            }
        )
        self._machine = Machine(**kwargs)

    def _get_state(self) -> typing.Optional[str]:
        try:
            return self._context.data["state"]
        except KeyError:
            return None

    def _set_state(self, val):
        self._context.data["state"] = val

    state = property(_get_state, _set_state)

    def get_triggers(self):
        return [
            i for i in self._machine.get_triggers(self.state) if not i.startswith("to_")
        ]

    def is_readonly(self):
        if self.state in self.readonly_states:
            return True
        return False
