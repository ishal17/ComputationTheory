class TM:

    @staticmethod
    def get_state_pad():
        return 11

    def __init__(self, n_states_2tape):
        self.actions = {}               # {(state, r) : (next_state, w, movement)}
        self.state_reads = {}           # {state : [r1, r2, ..., rn]}
        self.dotted = {'0' : 'A', '1' : 'B', '_' : 'C'}
        self.lst = 11 + n_states_2tape - 2

    def next(self):
        self.lst += 1
        return self.lst

    def last(self):
        return self.lst

    def add_action(self, state, r, next_state, w, mv):
        self.actions[(state, r)] = tuple([next_state, w, mv])

        if state in self.state_reads:
            self.state_reads[state].append(r)
        else:
            self.state_reads[state] = [r]

    def add_plain_actions(self, state, next_state, mv):
        for s in self.dotted:
            self.add_action(state, s, next_state, s, mv)

    def add_dotted_actions(self, state, next_state, mv):
        for _, s in self.dotted.items():
            self.add_action(state, s, next_state, s, mv)

    def add_plain2dotted_actions(self, state, next_state, mv):
        for s1, s2 in self.dotted.items():
            self.add_action(state, s1, next_state, s2, mv)


    def add_head_chain(self):
        self.add_action(0, '0', 1, '?', 'R')
        self.add_action(0, '1', 2, '?', 'R')

        self.add_action(1, '1', 2, '0', 'R')
        self.add_action(2, '0', 1, '1', 'R')
        self.add_action(1, '0', 1, '0', 'R')
        self.add_action(2, '1', 2, '1', 'R')

        self.add_action(1, '_', 3, '0', 'R')
        self.add_action(2, '_', 3, '1', 'R')

        self.add_action(3, '_', 4, '_', 'R')
        self.add_action(4, '_', 5, '@', 'R')
        self.add_action(5, '_', 6, self.dotted.get('_'), 'R')
        self.add_action(6, '_', 7, '_', 'R')
        self.add_action(7, '_', 8, '?', 'L')

        self.add_plain_actions(8, 8, 'L')
        self.add_action(8, self.dotted.get('_'), 8, self.dotted.get('_'), 'L')
        self.add_action(8, '@', 8, '@', 'L')

        self.add_action(8, '?', 9, '?', 'R')
        self.add_action(9, '0', 10, self.dotted.get('0'), 'L')
        self.add_action(9, '1', 10, self.dotted.get('1'), 'L')
        self.add_action(10, '?', 11, '?', 'R')    


    def grow_space(self, state):
        self.add_plain_actions(state, state, 'R')
        self.add_dotted_actions(state, state, 'R')
        self.add_action(state, '@', self.next(), '@', 'L')
        self.add_action(self.last(), '_', self.next(), '_', 'R')
        self.add_action(self.last(), '@', self.next(), '_', 'R')

        last = self.last()
        q0 = self.next()
        qA = self.next()
        q1 = self.next()
        qB = self.next()
        q_ = self.next()
        qC = self.next()
        nxt = self.next()

        q_symbols = {q0 : '0', qA : 'A', q1 : '1', qB : 'B', q_ : '_', qC : 'C'}

        for q, s in q_symbols.items():
            self.add_action(last, s, q, '@', 'R')
            self.add_action(q, '?', nxt, s, 'R')

            for qq, ss in q_symbols.items():
                self.add_action(q, ss, qq, s, 'R')

        self.add_action(self.last(), '_', self.next(), '_', 'R')
        self.add_action(self.last(), '_', self.next(), '?', 'L')
        self.add_plain_actions(self.last(), self.last(), 'L')
        self.add_dotted_actions(self.last(), self.last(), 'L')
        self.add_action(self.last(), '@', self.next(), '@', 'R')
        self.add_plain_actions(self.last(), self.last(), 'R')


    def convert_2tape_actions(self, action_tree):
        for state in action_tree:
            self.grow_space(state)

            branch_from = self.last()
            for r2 in action_tree[state]:
                self.add_r2_branch(r2, action_tree.get(state).get(r2), branch_from)          


    def add_r2_branch(self, r2, tree, frm):
        self.add_action(frm, self.dotted.get(r2), self.next(), self.dotted.get(r2), 'L')
        branch_from = self.last()
        self.add_plain_actions(branch_from, branch_from, 'L')
        self.add_action(branch_from, '@', branch_from, '@', 'L')

        for r1 in tree:
            self.add_r1_branch(r1, r2, tree.get(r1), branch_from)


    def add_r1_branch(self, r1, r2, tree, frm):        
        w1, mv1, w2, mv2, next_state = tree

        if next_state == -1:
            # after this action process will terminate   
            # so we no longer care about tape pointers
            self.add_action(frm, self.dotted.get(r1), next_state, self.dotted.get(r1), 'R')  
            return

        self.add_action(frm, self.dotted.get(r1), self.next(), w1, mv1)       
        self.add_plain2dotted_actions(self.last(), self.next(), 'R')
        self.add_plain_actions(self.last(), self.last(), 'R')
        self.add_action(self.last(), '@', self.last(), '@', 'R')
        self.add_action(self.last(), self.dotted.get(r2), self.next(), w2, mv2)
        self.add_plain2dotted_actions(self.last(), self.next(), 'L')
        self.add_plain_actions(self.last(), self.last(), 'L')    
        self.add_dotted_actions(self.last(), self.last(), 'L')      
        self.add_action(self.last(), '@', self.last(), '@', 'L')
        self.add_action(self.last(), '?', next_state, '?', 'R') 


    def __str__(self):
        s = str(len(self.state_reads) + 1)

        for state in sorted(self.state_reads):
            res = ''
            reads = self.state_reads.get(state)
            res += str(len(reads))
            for r in reads:
                next_state, w, movement = self.actions.get((state, r))
                next_state = len(self.state_reads) if next_state == -1 else next_state      # fix accepting state
                res += ' ' + ' '.join([r, str(next_state), w, movement])
            
            s += '\n' + res

        return s
    

# helpers

def fix_symbol(c):
    return '_' if c == '' or c == ' ' else c     


# main

def main():
    n_states = int(input())

    action_tree = {}        # {state : {r2 : {r1 : (w1, mv1, w2, mv2, next_state)}}}

    tm = TM(n_states)
    tm.add_head_chain()
    state_pad = TM.get_state_pad()

    for i in range(n_states - 1):
        actions = input().split(' ')
        n_actions = int(actions[0])
        actions = actions[1:]
        state = i + state_pad
        action_tree[state] = {}
        for _ in range(n_actions):
            next_state = int(actions[2])
            if next_state == n_states - 1:
                next_state = -1
            else:
                next_state += state_pad

            r1 = fix_symbol(actions[0])
            r2 = fix_symbol(actions[1])
            w1 = fix_symbol(actions[3])
            w2 = fix_symbol(actions[4])
            mv1 = fix_symbol(actions[5])
            mv2 = fix_symbol(actions[6])

            if action_tree.get(state).get(r2, None):
                action_tree[state][r2][r1] = (w1, mv1, w2, mv2, next_state)
            else:
                action_tree[state][r2] = {r1 : (w1, mv1, w2, mv2, next_state)}

            actions = actions[7:]

    tm.convert_2tape_actions(action_tree)
    print(tm)

if __name__ == "__main__":
    main()