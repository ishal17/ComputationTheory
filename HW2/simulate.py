class TM:

    def __init__(self, n_states):
        self.accepting = n_states - 1
        self.actions = {}               # {(state, r) : (next_state, w, mv)}

    def add_action(self, state, r, next_state, w, mv):
        self.actions[(state, r)] = tuple([next_state, w, mv])

    def run(self, string):
        tape = string
        state = 0
        pointer = 0
        result = ''

        while True:
            r = tape[pointer]
            next_state, w, mv = self.actions.get((state, r), (-1, '', ''))

            result += '\n' + str(next_state)
            if next_state == -1 or next_state == self.accepting:
                break

            state = next_state
            tape = tape[:pointer] + w + tape[pointer+1:]
            if mv == 'R':
                pointer += 1
                if pointer == len(tape):
                    tape += '_'
            if mv == 'L':
                if pointer > 0:
                    pointer -= 1
                else:
                    tape = '_' + tape

        return result[1:]  # remove first \n



def fix_symbol(c):
    return '_' if c == '' or c == ' ' else c    

def main():
    n_states = int(input())
    tm = TM(n_states)

    for i in range(n_states - 1):
        actions = input().split(' ')
        n_actions = int(actions[0])
        actions = actions[1:]
        for _ in range(n_actions):
            r = fix_symbol(actions[0])
            next_state = int(actions[1])
            w = fix_symbol(actions[2])
            mv = actions[3]
            tm.add_action(i, r, next_state, w, mv)
            actions = actions[4:]


    string = input()
    res = tm.run(string)
    print(res)


if __name__ == "__main__":
    main()