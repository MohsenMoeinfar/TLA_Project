import json
class State:
    __counter = 0
    def __init__(self, id: None) -> None:
        if id is None:
            self.id = State._get_next_id()
        else:
            self.id = id
        self.transitions: dict[str, 'State'] = {}
    def add_transition(self, ch: str, state: 'State') -> None:
        self.transitions[ch] = state
        
    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls.__counter
        cls.__counter += 1
        return current_id
    @staticmethod
    def reset() -> None:
        State.__counter = 0
class DFA:
    def __init__(self) -> None:
        self.init_state = None
        self.states: list['State'] = []
        self.alphabet: list['str'] = []
        self.final_states: list['State'] = []
    @staticmethod
    def deserialize_json(json_str: str) -> 'DFA':
        fa = DFA()
        json_fa = json.loads(json_str)

        fa.alphabet = json_fa["alphabet"]

        for state_str in json_fa["states"]:
            fa.add_state(int(state_str[2:]))
        fa.init_state = fa.get_state_by_id((int)(json_fa["initial_state"][2:]))
        
        for final_str in json_fa["final_states"]:
            fa.add_final_state(fa.get_state_by_id((int)(final_str[2:])))
        for state_str in json_fa["states"]:
            for ch in fa.alphabet:
                fa.add_transition(fa.get_state_by_id((int)(state_str[2:])), fa.get_state_by_id((int)(json_fa[state_str][ch][2:])),
                                  ch)
        return fa
    def serialize_json(self) -> str:
        fa = {
            "states": list(map(lambda s: f"q_{s.id}", self.states)),
            "initial_state": f"q_{self.init_state.id}",
            "final_states": list(map(lambda s: f"q_{s.id}", self.final_states)),
            "alphabet": self.alphabet
        }
        for state in self.states:
            fa[f"q_{state.id}"] = {}
            for ch in self.alphabet:
                if ch in state.transitions:
                    fa[f"q_{state.id}"][ch] = f"q_{state.transitions[ch].id}"
                # else:
                #     fa[f"q_{state.id}"][ch] = ""
        return json.dumps(fa)
    def add_state(self, id: int | None = None) -> State:
        state = State(id)
        self.states.append(state)
        return state
    def add_transition(self, from_state: State, to_state: State, input_symbol: str) -> None:
        from_state.add_transition(input_symbol, to_state)
    def assign_initial_state(self, state: State) -> None:
        self.init_state = state
    def add_final_state(self, state: State) -> None:
        self.final_states.append(state)
    def get_state_by_id(self, id) -> State | None:
        for state in self.states:
            if state.id == id:
                return state
    def is_final(self, state: State) -> bool:
        return state in self.final_states
class NFAState:
    __counter = 0
    def __init__(self, id: None) -> None:
        if id is None:
            self.id = NFAState._get_next_id()
        else:
            self.id = id
        self.transitions: dict[str, set['NFAState']] = {}
    def add_transition(self, ch: str, state: 'NFAState') -> None:
        if ch in self.transitions:
            self.transitions[ch].add(state)
        else:
            self.transitions[ch] = {state}
    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls.__counter
        cls.__counter += 1
        return current_id
    @staticmethod
    def reset() -> None:
        NFAState.__counter = 0
class NFA:
    def __init__(self) -> None:
        self.init_state = None
        self.states: list['NFAState'] = []
        self.alphabet: list['str'] = []
        self.final_states: list['NFAState'] = []
    @staticmethod
    def convert_DFA_instance_to_NFA_instance(dfa_machine: 'DFA') -> 'NFA':
        nfa = NFA()
        nfa.alphabet = dfa_machine.alphabet
        for state in dfa_machine.states:
            nfastate = nfa.add_state(state.id)
            if state == dfa_machine.init_state:
                nfa.assign_initial_state(nfastate)
            if dfa_machine.is_final(state):
                nfa.add_final_state(nfastate)
        for state in dfa_machine.states:
            for ch in dfa_machine.alphabet:
                nxt = state.transitions.get(ch)
                if nxt:
                    fromstate = nfa.get_state_by_id(state.id)
                    to = nfa.get_state_by_id(nxt.id)
                    nfa.add_transition(fromstate, to, ch)
        return nfa
    @staticmethod
    def union(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        nfa = NFA()
        countofM1 = 0
        nfa.alphabet = machine1.alphabet + ['$']
        for state in machine1.states:
            state.id +=1
            countofM1 +=1
        startstate = nfa.add_state()
        nfa.assign_initial_state(startstate)
        nfa.add_transition(startstate, machine1.init_state, '$')
        nfa.add_transition(startstate, machine2.init_state, '$')
        for state in machine1.states:
            newst = nfa.add_state()
            for ch, nextstates in state.transitions.items():
                for nextstate in nextstates:
                    nfa.add_transition(newst, nextstate, ch)
            if machine1.is_final(state):
                nfa.add_final_state(newst)
        for state in machine2.states:
            state.id  = state.id+ 1+ countofM1
        for state in machine2.states:
            newst = nfa.add_state()
            for ch, nextstates in state.transitions.items():
                for nextstate in nextstates:
                    nfa.add_transition(newst, nextstate, ch)
            if machine2.is_final(state):
                nfa.add_final_state(newst)
        return nfa
    @staticmethod
    def concat(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        nfa = NFA()
        nfa.init_state = machine1.init_state
        count = 0
        for state in machine1.states:
            count+=1
        for state in machine2.states:
            state.id  = state.id + count
        nfa.alphabet =  machine1.alphabet + ['$']
        for state in machine1.states:
            newst = nfa.add_state()
            for ch, nextstates in state.transitions.items():
                for nextstate in nextstates:
                    nfa.add_transition(newst, nextstate, ch)
            if machine1.is_final(state):
                        nfa.add_transition(newst, machine2.init_state, '$')
        for state in machine2.states:
            newst = nfa.add_state()
            for ch, nextstates in state.transitions.items():
                for nextstate in nextstates:
                    nfa.add_transition(newst, nextstate, ch)
            if machine2.is_final(state):
                nfa.add_final_state(newst)
        return nfa
    @staticmethod
    def star(machine: 'NFA') -> 'NFA':
        nfa = NFA()
        for state in machine.states:
            state.id +=1
        nfa.alphabet = machine.alphabet + ['$']
        newstart = nfa.add_state()
        nfa.assign_initial_state(newstart)
        nfa.add_transition(newstart, machine.init_state, '$')
        for state in machine.states:
            newst = nfa.add_state()
            for ch, nextstates in state.transitions.items():
                for nextstate in nextstates:
                    nfa.add_transition(newst, nextstate, ch)
        newfinish = nfa.add_state()
        nfa.add_transition(newstart , newfinish , '$')
        nfa.add_transition(newfinish, newstart, '$')
        for finalstate in machine.final_states:
            for state in nfa.states:
                if(finalstate.id == state.id):
                     nfa.add_transition(state, newfinish, '$')
        nfa.add_final_state(newfinish)
        return nfa
    def serialize_to_json(self) -> str:
        fa = {
            "states": list(map(lambda s: f"q_{s.id}", self.states)),
            "initial_state": f"q_{self.init_state.id}",
            "final_states": list(map(lambda s: f"q_{s.id}", self.final_states)),
            "alphabet": self.alphabet
        }
        for state in self.states:
            fa[f"q_{state.id}"] = {}
            for ch in self.alphabet:
                if ch in state.transitions:
                    transitions = [f"q_{s.id}" for s in state.transitions[ch]]
                    fa[f"q_{state.id}"][ch] = transitions
                else:
                    fa[f"q_{state.id}"][ch] = []
        return json.dumps(fa)
    def add_state(self, id: int | None = None) -> NFAState:
        state = NFAState(id)
        self.states.append(state)
        return state
    def add_transition(self, from_state: NFAState, to_state: NFAState, input_symbol: str) -> None:
        from_state.add_transition(input_symbol, to_state)
    def assign_initial_state(self, state: NFAState) -> None:
        self.init_state = state
    def add_final_state(self, state: NFAState) -> None:
        self.final_states.append(state)
    def get_state_by_id(self, id) -> NFAState | None:
        for state in self.states:
            if state.id == id:
                return state
    def is_final(self, state: NFAState) -> bool:
        return state in self.final_states
    def refresh(self): 
        count = 0 
        for st in self.states :
             st.id = count
             count+=1
        NFAState.reset()
def main():
    State.reset()
    NFAState.reset()
    dfa = DFA()
    dfa.alphabet = ['a', 'b']
    q0 = dfa.add_state()
    q1 = dfa.add_state()
    q2 = dfa.add_state()
    dfa.assign_initial_state(q0)
    dfa.add_final_state(q2)
    dfa.add_transition(q0, q1, 'a')
    dfa.add_transition(q0, q0, 'b')
    dfa.add_transition(q1, q2, 'b')
    dfa.add_transition(q1, q1, 'a')
    dfa.add_transition(q2, q2, 'a')
    dfa.add_transition(q2, q2, 'b')
    dfa_json = dfa.serialize_json()
    print("DFA:")
    print(dfa_json)
    print("**\n")
    nfa = NFA.convert_DFA_instance_to_NFA_instance(dfa)
    nfa.add_transition(nfa.get_state_by_id(2), nfa.get_state_by_id(0), 'a')
    nfa_json = nfa.serialize_to_json()
    print("NFA:")
    print(nfa_json)
    print("**\n")
    anothetnfa = NFA.convert_DFA_instance_to_NFA_instance(dfa)
    union_nfa = NFA.union(nfa, anothetnfa)
    union_json = union_nfa.serialize_to_json()
    print("union:")
    print(union_json)
    print("**\n")
    NFA.refresh(nfa)
    NFA.refresh(anothetnfa)
    concatjson  = NFA.concat(nfa , anothetnfa).serialize_to_json()
    print("concat:")
    print(concatjson)
    print("**\n")
    NFA.refresh(nfa)
    starstar = NFA.star(nfa).serialize_to_json()
    print("star:")
    print(starstar)
    print("**\n")
if __name__ == '__main__':
    main()
