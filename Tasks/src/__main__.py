from src.tasks.task1 import task1_runner
from src.tasks.task3 import task3_runner
from src.tasks.task5 import task5_runner
from src.tasks.task6 import task6_runner
from src.tasks.task8 import task8_runner

curr_task = 3


def task_runner():
    tasks = {1: task1_runner, 3: task3_runner, 5: task5_runner, 6: task6_runner, 8: task8_runner}
    tasks[curr_task]()


if __name__ == '__main__':
    task_runner()
