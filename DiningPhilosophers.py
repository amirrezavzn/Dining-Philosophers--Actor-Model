from builtins import print
import pykka
import time
import random
from tkinter import *


class Philosopher(pykka.ThreadingActor):

    def __init__(self, actor_id=1000, left_actor_id=999, right_actor_id=1001, left_fork_state='dirty',
                 right_fork_state='dirty', have_left_fork=False, have_right_fork=False, actor_state='THINKING',
                 actors_num=3):
        super(Philosopher, self).__init__()
        self.actor_id = actor_id
        self.left_actor_id = left_actor_id
        self.right_actor_id = right_actor_id
        self.left_fork_state = left_fork_state
        self.right_fork_state = right_fork_state
        self.have_left_fork = have_left_fork
        self.have_right_fork = have_right_fork
        self.actor_state = actor_state
        self.actors_num = actors_num
        print("philosopher ", actor_id, " has been created!")

    def on_receive(self, message):
        if message == {'msg': 'left_fork_req'}:  # request for left fork
            print('philosopher', self.actor_id, "has requested for the left fork")
            if self.actor_id - 1000 == self.actors_num-1:
                forkid = 1000
            else:
                forkid = self.actor_id + 1
            if self.have_right_fork:
                if get_forkstate(forkid) == "clean":
                    None
                else:
                    set_forkstate(forkid, "clean")
                    set_permission(forkid, True)
            else:
                set_permission(forkid, True)
        elif message == {'msg': 'right_fork_req'}:  # request for right fork
            print('philosopher', self.actor_id, "has requested for the right fork")
            if get_permission(self.actor_id):
                if get_forkstate(self.actor_id) == "clean":
                    None
                else:
                    set_forkstate(self.actor_id, "clean")
                    set_permission(self.actor_id, True)
        elif message == {'msg': 'eating_state'}:
            self.actor_state = 'EATING'

        elif message == {'msg': 'left_fork_clean'}:
            self.left_fork_state = 'clean'

        elif message == {'msg': 'right_fork_clean'}:
            self.right_fork_state = 'clean'

        elif message == {'msg': 'left_fork_dirty'}:
            self.left_fork_state = 'dirty'

        elif message == {'msg': 'right_fork_dirty'}:
            self.right_fork_state = 'dirty'

        elif message == {'msg': 'put_left_fork'}:
            self.have_left_fork = False

        elif message == {'msg': 'put_right_fork'}:
            self.have_right_fork = False

        elif message == {'msg': 'get_left_fork'}:
            self.have_left_fork = True

        elif message == {'msg': 'get_right_fork'}:
            self.have_right_fork = True

        elif message == {'msg': 'thinking_state'}:

            self.actor_state = 'THINKING'
        else:
            print("None!")

    def on_start(self):
        time.sleep(self.actors_num/5)
        print("PHILOSOPHER", self.actor_id, "IS THINKING")
        t = random.uniform(1, 8)   # random sleep time [1:8] sec  (thinking time)
        print("t = ", t)
        time.sleep(t)
        hungry(self.actor_id)


def eating(actrid=1):
    global actorsArr
    global fsize
    global wid
    global height
    global heightph
    global myLabel1
    global myLabel2
    global n
    end = len(actorsArr) - 1
    if actrid == 1000 + end:
        right_act = 1000
    else:
        right_act = actrid + 1

    # self.have_left_fork = False:
    actorsArr[actrid - 1000].tell({'msg': 'put_left_fork'})
    set_permission(actrid, False)
    # self.have_right_fork = False:
    actorsArr[actrid - 1000].tell({'msg': 'put_right_fork'})
    set_permission(right_act, False)

    print("PHILOSOPHER", actrid, "IS EATING")
    # print("                                         ", permission)

    for p in range(n):
        if actrid-1000 == p:
            string = "eating"
            clr = "red"
        else:
            string = "thinking"
            clr = "pink"  
        """myLabel1 = Label(text='Philosopher ' + str(p), fg='white', bg="gray", width=wid, height=heightph,
                         font='Helvetica ' + str(fsize) + ' bold').grid(row=15, column=i)"""
        myLabel2 = Label(text=string, fg='black', bg=clr, width=wid, height=height, borderwidth=0.5, relief="solid",
                         font='Helvetica ' + str(fsize) + ' bold').grid(row=20, column=p)

    # self.actor_state = 'EATING' :
    actorsArr[actrid - 1000].tell({'msg': 'eating_state'})
    # self.left_fork_state = 'dirty':
    actorsArr[actrid - 1000].tell({'msg': 'left_fork_dirty'})
    set_forkstate(actrid, "dirty")
    # self.right_fork_state = 'dirty':
    actorsArr[actrid - 1000].tell({'msg': 'right_fork_dirty'})
    set_forkstate(right_act, "dirty")

    t = random.uniform(1, 8)
    time.sleep(t)     # random time sleep (eating time)
    set_forkstate(actrid, "clean")
    actorsArr[actrid - 1000].tell({'msg': 'left_fork_clean'})
    set_forkstate(right_act, "clean")
    actorsArr[actrid - 1000].tell({'msg': 'right_fork_clean'})
    set_permission(actrid, True)
    actorsArr[actrid - 1000].tell({'msg': 'get_left_fork'})
    set_permission(right_act, True)
    actorsArr[actrid - 1000].tell({'msg': 'get_right_fork'})
    # print("actor", actrid, "is Thinking!")
    # self.actor_state = 'THINKING':
    actorsArr[actrid - 1000].tell({'msg': 'thinking_state'})


def hungry(actorid=1):
    global actorsArr
    print("philosopher", actorid, "is hungry!")

    if actorid == 1000 + len(actorsArr) - 1:
        right_actor = 1000
    else:
        right_actor = actorid + 1
    if actorid == 1000:
        left_actor = 1000 + len(actorsArr) - 1
    else:
        left_actor = actorid - 1
    # print("right actor :", right_actor, "left actor :", left_actor)
    right_fork = right_actor
    left_fork = actorid
    # at the beginning :
    if get_permission(left_fork) and get_permission(right_fork) and ((get_forkstate(left_fork) == "dirty") or
                                                                     (get_forkstate(right_fork) == "dirty")):
        set_permission(left_fork, False)
        set_permission(right_fork, False)
        print("philosopher", actorid, "has got the dirty forks!")
        set_forkstate(left_fork, "clean")
        set_forkstate(right_fork, "clean")
        print("forks ", left_fork, ",", right_fork, "have became clean")
        set_permission(left_fork, True)
        set_permission(right_fork, True)
    elif get_permission(left_fork):
        if get_permission(right_fork):
            eating(actorid)
        else:
            try:  # request to right actor:
                actorsArr[right_actor - 1000].tell({'msg': 'right_fork_req'})
            except Exception as e:
                print(repr(e))
            print("philosopher", actorid, "is waiting for his right fork!")
            while not get_permission(right_fork):
                continue
            # now I have both left and right forks
            print("Philosopher", right_actor, "IS THINKING")
            eating(actorid)
    else:
        # request to left philosopher :
        try:
            actorsArr[left_actor - 1000].tell({'msg': 'left_fork_req'})
        except Exception as e:
            print(repr(e))
        print("philosopher", actorid, "is waiting for  his left fork!")
        while not get_permission(actorid):
            continue
        print("philosopher", actorid, "has got his left fork!")
        # noe I have my left fork   [copy scope above]:
        print("Philosopher", left_actor, "IS THINKING")
        if get_permission(right_fork):
            print("Philosopher", right_actor, "IS THINKING")
            eating(actorid)
        else:
            try:  # request to right actor:
                actorsArr[right_actor - 1000].tell({'msg': 'right_fork_req'})
            except Exception as e:
                print(repr(e))
            print("Philosopher", actorid, "is waiting for his right fork!")
            while not get_permission(right_fork):
                continue
            # now I have both left and right forks
            print("Philosopher", right_actor, "IS THINKING")
            eating(actorid)

    # loop:
    print("PHILOSOPHER", actorid, "IS THINKING")
    t = random.uniform(1, 8)
    # time.sleep(t)
    time.sleep(2)
    hungry(actorid)


def set_permission(actid=1, perm=False):
    global permission
    permission[actid - 1000] = perm
    """global myLabel2
    global n
    s = [False for x in range(n)]
    for j in range(n):
        if j == n-1:
            if (not permission[j]) and (not permission[0]):
                s[j] = True
        else:
            if (not permission[j]) and (not permission[j + 1]):
                s[j] = True

    for p in range(n):
        if s[p]:
            string = "eating"
            clr = "red"
        else:
            string = "thinking"
            clr = "pink"
        myLabel2 = Label(text=string, fg='black', bg=clr, width=wid, height=height, borderwidth=0.5, relief="solid",
                         font='Helvetica ' + str(fsize) + ' bold').grid(row=20, column=p)"""


def get_permission(actid=1):
    global permission

    return permission[actid - 1000]


def set_forkstate(fork_id=1, state=""):
    global forkstate
    forkstate[fork_id - 1000] = state


def get_forkstate(fork_id=1):
    global forkstate
    return forkstate[fork_id - 1000]


if __name__ == '__main__':
    n = int(input("please enter the number of Philosophers :"))
    m = int(input("please enter the time of the process (sec) :"))
    i = 0
    actorsArr = ["" for x in range(n)]
    while i < n:
        # str1 = "Actor" + str(i)
        act_id = i + 1000
        if i == 0:
            left_act_id = 1000 + n - 1
        else:
            left_act_id = act_id - 1
        if i == n - 1:
            right_act_id = 1000
        else:
            right_act_id = act_id + 1

        actorsArr[i] = Philosopher.start(actor_id=act_id, left_actor_id=left_act_id, right_actor_id=right_act_id,
                                         left_fork_state='dirty', right_fork_state='dirty', have_left_fork=False,
                                         have_right_fork=False, actor_state='THINKING', actors_num=n)
        i += 1
    permission = []
    forkstate = []
    y = 0
    while y < n:
        permission.append(True)
        forkstate.append("dirty")
        y += 1

    """time.sleep(m)
    j = 0
    while j < n:
        actorsArr[j].stop()
        j += 1"""
    global fsize
    fsize = 8
    if n > 13:
        fsize = 6
    global wid
    wid = 14
    global height
    height = 2
    global heightph
    heightph = 2
    root = Tk()
    root.title("Dining Philosophers")
    for i in range(n):
        myLabel1 = Label(text='Philosopher ' + str(i), fg='white', bg="gray", width=wid, height=heightph,
                         font='Helvetica ' + str(fsize) + ' bold').grid(row=15, column=i)
        myLabel2 = Label(text='', fg='black', bg="pink", width=wid, height=height, borderwidth=0.5, relief="solid",
                         font='Helvetica ' + str(fsize) + ' bold').grid(row=20, column=i)

    root.mainloop()
