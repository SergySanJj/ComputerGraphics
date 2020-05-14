from src.tasks.task1 import task1_runner
from src.tasks.task5 import task5_runner
from src.tasks.task6 import task6_runner

curr_task = 6


def task_runner():
    tasks = {1: task1_runner, 5: task5_runner, 6: task6_runner}
    tasks[curr_task]()


if __name__ == '__main__':
    task_runner()
