from prefect import task, flow

@task()
def test_task():
    print("prefect task example")

@task()
def test_task2():
    print("prefect task example2")

@flow
def my_flow():
    test_task()
    test_task2()

if __name__ == "__main__":
    my_flow()