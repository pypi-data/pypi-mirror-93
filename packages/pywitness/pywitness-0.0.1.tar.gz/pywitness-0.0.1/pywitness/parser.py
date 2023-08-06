from datetime import datetime, timedelta
import re

from pywitness.channels import Channel

from pytz import timezone


class TextParser:
    def __init__(self, cfg, single_match=True, timestamp=datetime.now):
        if 'start' not in cfg:
            raise SyntaxError('Parser requires start state "start"')
        elif 'end' not in cfg:
            raise SyntaxError('Parser requires end state "end"')
        elif 'eof' not in cfg:
            raise SyntaxError('Parser requires early EOF state "eof"')

        self.channels = []
        # regexes with their actions
        self.transitions = {}
        # actions for special states
        self.actions = {}
        self._state = 'start'
        self.reachable = set()
        self.single_match = single_match
        self._mark = datetime.utcnow()
        if timestamp is None:
            self.timestamp = lambda: None
        else:
            self.timestamp = timestamp

        for state_str, transitions in cfg.items():
            if state_str in ['end', 'eof', 'start']:
                self.actions[state_str] = [ac for acs in [
                    [self.create_action(action, value)] if not isinstance(value, list)
                    else [self.create_action(action, v) for v in value]
                    for action, value in transitions.items()
                ] for ac in acs]
            else:
                self.transitions[state_str] = {
                    re.compile(rgx): [ac for acs in [
                        [self.create_action(action, value)] if not isinstance(value, list)
                        else [self.create_action(action, v) for v in value]
                        for action, value in actions.items()
                    ] for ac in acs] for rgx, actions in transitions.items()
                }

        for state in self.transitions:
            if state not in self.reachable:
                raise SyntaxError(f'Unreachable state in text parser configuration: {state}')
        for state in self.reachable:
            if state not in self.transitions and state != 'end':
                raise SyntaxError(f'Transition to missing state in text parser configuration: {state}')

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if self._state in ['end', 'eof']:
            return
        self._state = value
        if value in ['end', 'eof']:
            for action in self.actions[self._state]:
                action(None)

    def add_channel(self, channel):
        assert isinstance(channel, Channel)
        self.channels.append(channel)

    @staticmethod
    def _process(v, groups):
        if v is None or isinstance(v, int):
            return v
        elif isinstance(v, str):
            return v.format(*groups)
        elif '_timedelta' in v:
            return timedelta(**{dk: float(dv.format(*groups)) if isinstance(dv, str) else dv
                             for dk, dv in v['_timedelta'].items()})
        elif '_time' in v:
            if len(v['_time']) == 2:
                return datetime.strptime(v['_time'][0].format(*groups), v['_time'][1])
            else:
                return timezone(v['_time'][2]).localize(
                    datetime.strptime(v['_time'][0].format(*groups), v['_time'][1]))

    def create_action(self, action, value):
        def set_state(_):  # closure for value
            self.state = value

        def emit(re_match):  # closure for value
            # collect groups as a tuple for format, with the entire match @ 0 and the groups following
            groups = (re_match.group(0), *re_match.groups()) if re_match is not None else []
            _value = dict(value)
            # if a timestamp is specified, resolve and then remove it
            if '_timestamp' in _value:
                ts = self._process(_value['_timestamp'], groups)
                # timestamp timedelta is relative to the most recent mark (defaults to utcnow at creation of parser)
                if isinstance(ts, timedelta):
                    ts = self._mark + ts
                del(_value['_timestamp'])
                # if the timestamp is indicated as a new mark, save and remove it
                if '_mark' in _value:
                    self._mark = ts
                    del (_value['_mark'])
            else:
                ts = self.timestamp()
            # emit remaining content of value to channels
            for k, v in _value.items():
                for ch in self.channels:
                    ch.emit(k, self._process(v, groups), ts)

        if action == 'state':
            self.reachable.add(value)
            return set_state

        if action == 'emit':
            return emit

    def parse(self, line):
        if self.state in ['end', 'eof']:
            return
        if line is None and self.state != -1:
            self.state = 'eof'
            return
        if self.state == 'start':
            for action in self.actions['start']:
                action(None)
        # remember state (may change due to actions)
        state = self.state
        for rgx, actions in self.transitions[state].items():
            if (match := rgx.match(line)):
                for action in actions:
                    action(match)
                if self.single_match:
                    return
