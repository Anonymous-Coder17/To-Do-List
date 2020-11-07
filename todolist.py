from sqlalchemy import create_engine, Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class ToDoList:
    def __init__(self):
        self.engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.today = datetime.today().date()
        Base.metadata.create_all(self.engine)

    def main(self):
        while True:
            print("1) Today's tasks")
            print("2) Week's tasks")
            print("3) All tasks")
            print("4) Missed tasks")
            print("5) Add task")
            print("6) Delete task")
            print("0) Exit")
            menu = input()

            if menu == '1':
                print(f"\nToday {self.today.day} {self.today.strftime('%b')}:")
                self.tasks_today(datetime.today().date())
            elif menu == '2':
                self.tasks_week()
            elif menu == '3':
                self.all_tasks()
            elif menu == '4':
                self.del_missed()
            elif menu == '5':
                self.add_task()
            elif menu == '6':
                self.del_task()
            elif menu == '0':
                print("Bye!")
                quit()

    def tasks_today(self, date):
        tasks = self.session.query(Table).filter(Table.deadline == date).all()

        if not tasks:
            print('Nothing to do!')
        else:
            for n, task in enumerate(tasks):
                print(f"{n + 1}. {task}")
        print()

    def tasks_week(self):
        weekday = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: 'Sunday'}

        for i in range(7):
            day = self.today + timedelta(days=i)
            print(f"{weekday[day.weekday()]} {day.day} {day.strftime('%b')}:")
            self.tasks_today(day)

    def all_tasks(self):
        print("\nAll tasks:")
        tasks = self.session.query(Table).order_by(Table.deadline).all()

        for n, task in enumerate(tasks):
            date = task.deadline
            print(f"{n+1}. {task}. {date.day} {date.strftime('%b')}")
        print()

    def add_task(self):
        new_row = Table(task=input("\nEnter task\n"),
                        deadline=datetime.strptime(input("Enter deadline\n"), '%Y-%m-%d'))
        self.session.add(new_row)
        self.session.commit()
        print("The task has been added!\n")

    def del_missed(self):
        tasks = self.session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        print("\nMissed tasks:")

        if tasks:
            for n, task in enumerate(tasks):
                print(f"{n+1}. {task}")
        else:
            print("Nothing is missed!")
        print()

    def del_task(self):
        tasks_to_del = self.session.query(Table).filter(Table.deadline <= datetime.today().date()).all()
        print("\nChoose the number of the task you want to delete:")

        if tasks_to_del:
            for n, task in enumerate(tasks_to_del):
                print(f"{n+1}. {task}")
            choice = int(input())
            task = tasks_to_del[choice-1]
            self.session.delete(task)
            self.session.commit()
            print("The task has been deleted!\n")
        else:
            print("Nothing to delete\n")


ToDoList().main()
