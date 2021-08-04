class NFA:

    def __init__(self, accepting):
        self.accepting = accepting
        self.actions = {}        

    def add_action(self, char, from_s, to_s):
        if char in self.actions:
            self.actions[char].append((from_s, to_s))
        else:
            self.actions[char] = [(from_s, to_s)]

    def run(self, string):
        cur_states = set()
        cur_states.add(0)
        res = ''
        for c in string:
            if not c in self.actions:
                break

            new_states = [ns for (os, ns) in self.actions[c] if os in cur_states]
            cur_states = set(new_states)
            cur_acc = cur_states.intersection(self.accepting)
            res += 'Y' if len(cur_acc) > 0 else 'N'

        res += 'N' * (len(string) - len(res))
        return res

def main():
    string = input()
    n = int(input().split()[0])
    accepting = set([int(c) for c in input().split()])
    nfa = NFA(accepting)

    for i in range(n):
        inp = input().split()
        num = int(inp[0])
        for j in range(1, 2*num, 2):
            char = inp[j]
            to = int(inp[j+1])
            nfa.add_action(char, i, to)

    res = nfa.run(string)
    print(res)


if __name__ == "__main__":
    main()