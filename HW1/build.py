class NFA:

    def __init__(self, string):
        self.accepting = set([len(string)])
        self.N = len(string) + 1
        self.actions = {}

        for i, s in enumerate(string):
            self.add_action(s, i, i+1)


    def add_action(self, char, from_s, to_s):
        if from_s in self.actions:
            if (char, to_s) not in self.actions[from_s]:
                self.actions[from_s].append((char, to_s))
        else:
            self.actions[from_s] = [(char, to_s)]


    def concat(self, nfa2):
        N2, accepting2, actions2 = nfa2.getNFA()

        for from_s in actions2:
            for char, to_s in actions2[from_s]:
                if from_s == 0:
                    for acc in self.accepting:
                        self.add_action(char, acc, to_s + self.N - 1)
                else:
                    self.add_action(char, from_s + self.N - 1, to_s + self.N - 1)

        if 0 not in accepting2:
            self.accepting = set()

        for acc in accepting2:
            new_acc = acc + self.N - 1
            self.accepting.add(new_acc)

        self.N += N2 - 1
    

    def star(self):        
        if self.N == 1: return # epsilon

        for acc in self.accepting:
            for char, to_s in self.actions[0]:
                self.add_action(char, acc, to_s)

        self.accepting.add(0)


    def union(self, nfa2):
        N2, accepting2, actions2 = nfa2.getNFA()

        for from_s in actions2:
            for char, to_s in actions2[from_s]:
                new_from = from_s + self.N - 1 if from_s > 0 else 0
                self.add_action(char, new_from, to_s + self.N - 1)

        for acc in accepting2:
            new_acc = acc + self.N - 1 if acc > 0 else 0
            self.accepting.add(new_acc)

        self.N += N2 - 1


    def __str__(self):
        a = len(self.accepting)
        t = sum([len(self.actions[key]) for key in self.actions])

        s = ' '.join([str(self.N), str(a), str(t)]) + '\n'
        s += ' '.join([str(acc) for acc in sorted(self.accepting)])

        for key in range(self.N):
            if key not in self.actions:
                s += '\n0'
                continue

            line = [len(self.actions[key])]
            for char, to_s in self.actions[key]:
                line.append(char)
                line.append(to_s)
            s += '\n' + ' '.join([str(l) for l in line])
        
        return s

    
    def getNFA(self):
        return self.N, self.accepting, self.actions


def regex2NFA(regex):
    i = len(regex) - 1
    if i == 0:
        return NFA(regex)

    balance = 0
    for idx in range(len(regex)):
        if regex[idx] == '(':
            balance += 1
        elif regex[idx] == ')':
            balance -= 1
        elif regex[idx] == '|' and balance == 0:
            left = regex2NFA(regex[:idx])
            right = regex2NFA(regex[idx+1:])
            left.union(right)
            return left

    cur_str = ''
    while i >= 0:
        if regex[i] == '*':
            if regex[i-1] == ')':
                j = i - 2
                count = 1
                while j >= 0:
                    if regex[j] == ')': count += 1
                    if regex[j] == '(': count -= 1
                    if count == 0: break
                    j -= 1
                mid = regex2NFA(regex[j+1: i-1])
                right = regex2NFA(cur_str)
                mid.star()
                mid.concat(right)
                if j > 0:
                    left = regex2NFA(regex[:j-1])
                    left.concat(mid)
                    mid = left
                return mid  
            else:
                right = NFA(regex[i-1])
                right.star()
                if i > 1:
                    left = regex2NFA(regex[:i-1])
                    left.concat(right)
                    return left
                else:
                    return right
        elif regex[i] == ')':
            j = i - 1
            count = 1
            while j >= 0:
                if regex[j] == ')': count += 1
                if regex[j] == '(': count -= 1
                if count == 0: break
                j -= 1
            mid = regex2NFA(regex[j+1: i])
            right = regex2NFA(regex[i+1:])            
            mid.concat(right)
            if j > 0:
                left = regex2NFA(regex[:j])
                left.concat(mid)
                mid = left
            return mid   
        else:
            cur_str = regex[i] + cur_str

        i -= 1

    return NFA(cur_str)


def main():
    regex = input()
    nfa = regex2NFA(regex)
    print(nfa)    

if __name__ == "__main__":
    main()