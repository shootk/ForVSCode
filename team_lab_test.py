import simpleai.search as ss
import urllib.request
import time

token = "DJeZ6T7qWrt0a3dcPkmPFpSddQCPXNFl"


def query(url):
    time.sleep(1)
    res = urllib.request.urlopen(url)
    return res.read()


class CustomProblem(ss.SearchProblem):
    def set_target(self):
        self.target_string = 'a'
        self.max_length = 1

    def actions(self, cur_state):
        if len(cur_state) < 50:
            alphabets = 'abcd'
            return list(alphabets)

        else:
            return []

    def result(self, cur_state, action):
        return cur_state + action

    def is_goal(self, cur_state):
        if len(cur_state) >= int(50):
            url = "https://runner.team-lab.com/q?token=%s&str=%s" % (
                token, cur_state)
            result = query(url)
            print(result)
            if int(result) >= int(2500):
                return True
            else:
                return False
        else:
            if (self.max_length < len(cur_state)):
                url = "https://runner.team-lab.com/q?token=%s&str=%s" % (
                    token, cur_state)
                result = query(url)
                self.max_length = len(cur_state)
            return False

    def heuristic(self, cur_state):
        if len(cur_state) < 8:
            url = "https://runner.team-lab.com/q?token=%s&str=%s" % (
                token, cur_state)
            result = query(url)
        else:
            url = "https://runner.team-lab.com/q?token=%s&str=%s" % (
                token, cur_state[-8:-1])
            result = query(url)
        print(result, len(cur_state))

        return int(2500) - int(result)


problem = CustomProblem()
problem.set_target()
problem.initial_state = 'a'

output = ss.greedy(problem)
