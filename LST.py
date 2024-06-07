

import random
from functools import cmp_to_key
from matplotlib import pyplot



class TaskIns(object):

    # Constructor (should only be invoked with keyword parameters)
    def __init__(self, start, end, priority, name):
        self.start = start
        self.end = end
        self.usage = 0
        self.priority = priority
        self.name = int(name)
        self.id = int(random.random() * 10000)

    # Allow an instance to use the cpu (periodic)
    def use(self, usage):
        self.usage += usage
        if self.usage >= self.end - self.start:
            return True
        return False

    # Default representation
    def __repr__(self):
        return str(self.name) + "#" + str(self.id) + " - start: " + str(self.start) + " priority: " + str(self.priority)
        # + budget_text

    # Get name as Name#id
    def get_unique_name(self):
        return str(self.name) + "#" + str(self.id)

# Task types (templates for periodic tasks)


class TaskType(object):

    # Constructor
    def __init__(self, period, release, execution, deadline, name):
        self.period = period
        self.release = release
        self.execution =(int)( execution)
        self.deadline = deadline
        self.name = name

# Priority comparison


def priority_cmp(one, other):
    if one.priority < other.priority:
        return -1
    elif one.priority > other.priority:
        return 1
    return 0

# Deadline monotonic comparison


def tasktype_cmp(self, other):
    if self.deadline < other.deadline:
        return -1
    if self.deadline > other.deadline:
        return 1
    return 0


def plot(sequence_of_process):
    # for i in range(0, len(sequence_of_process)):
    #     print(f"{i}: {sequence_of_process[i]}")
    colors = ['w', 'r', 'b', 'g']
    fig, ax = pyplot.subplots(figsize=(10, 2))
    ax.set_ylim(0, 40)
    ax.set_xlim(0, 30)
    ax.set_xlabel('time')
    ax.set_yticks([12.5, 22.5, 32.5])
    ax.set_yticklabels(['T1', "T2", "T3"])
    a = 0
    for i in sequence_of_process:
        if(i== -1):
            ax.broken_barh([(a, 1)], (i*10, 5), facecolors='w')
            a = a + 1
        else:
            ax.broken_barh([(a, 1)], (i*10, 5), facecolors=colors[i])
            a = a + 1
    pyplot.show()


if __name__ == '__main__':
    # Variables
    
    task_types = []
    tasks = []
    sequence_of_process = []
    # Allocate task types
    task_types.append(TaskType(period=4, release=0,
                               execution=1, deadline=4, name=1))
    task_types.append(TaskType(period=10, release=0,
                               execution=3, deadline=10, name=2))
    task_types.append(TaskType(period=12, release=0,
                               execution=3, deadline=12, name=3))
    task_types = sorted(task_types, key=cmp_to_key(tasktype_cmp))

    period = 29
    # Create task instances
    
    for i in range(0, period):
        for task_type in task_types:
            if (i - task_type.release) % task_type.period == 0 and i >= task_type.release:
                start = i
                end = start + task_type.execution
                priority = start + task_type.deadline - task_type.execution
                tasks.append(TaskIns(start=start, end=end,
                                     priority=priority, name=task_type.name))
        
    # Simulate clock
    clock_step = 1
    for i in range(0, period, clock_step):
        possible = []
        for t in tasks:
            if t.start <= i:
                possible.append(t)
        possible = sorted(possible, key=cmp_to_key(priority_cmp))

        # Select task with highest priority
        if len(possible) > 0:
            on_cpu = possible[0]
            sequence_of_process.append(possible[0].name)
            print(on_cpu.get_unique_name(), " uses the processor. "),
            on_cpu.priority += 1
            if on_cpu.use(clock_step):
                tasks.remove(on_cpu)
                print("Finish!"),
        else:
            print('No task uses the processor. ')
            sequence_of_process.append(-1)
        print("\n")

    # Print remaining periodic tasks

    for p in tasks:
        print(p.get_unique_name() + " is dropped due to overload at time: " + str(i))
    plot(sequence_of_process)
    #plot(sequence_of_process)