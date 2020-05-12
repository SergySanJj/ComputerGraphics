from src.task1.task1 import task1_runner

curr_task = 0


def task_runner():
    tasks = [task1_runner]
    tasks[curr_task]()


if __name__ == '__main__':
    task_runner()
