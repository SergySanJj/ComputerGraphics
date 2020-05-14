from src.tasks.task1 import task1_runner
from src.tasks.task5 import task5_runner

curr_task = 1


def task_runner():
    tasks = {1: task1_runner, 5: task5_runner, }
    tasks[curr_task]()


if __name__ == '__main__':
    task_runner()
