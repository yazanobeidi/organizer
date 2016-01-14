#!/usr/bin/env python

__author__ = 'yazan'

import argparse
import pdb

class Organizer(object):
    def __init__(self):
        self.tasks = []
        self.modified = False
        self.loadSavedData()

    def __del__(self):
        print 'Closing organizer.'
        if self.modified: self.saveData()

    def start(self):
        print 'Welcome to Organizer.'
        parser = argparse.ArgumentParser(description='Python based text organizer. v0.0.1')
        parser.add_argument('-p', '--peek', action='store_true', help='quickly peek at top 5 tasks')
        parser.add_argument('-v', '--viewall', action='store_true', help='view all tasks')
        parser.add_argument('-r', '--remove', action='store_true', help='flag task removal')
        parser.add_argument('task', action='store', nargs='?', help='task name to add')
        parser.add_argument('duedate', type=str, nargs='?', help='task due date')
        args = parser.parse_args()
        if args.peek:
            print 'Peeking ..'
            self.peek()

        elif args.viewall:
            print 'Viewing all ..'
            self.viewAll()

        elif args.remove:
            print 'Removing task: ' + args.task
            if args.task == 'ALLTASKS':
                self.removeAllTasks()
            
            else: self.removeTask(args.task)

        else:
            print 'Adding task: ' + args.task + ' with due date: ' + args.duedate
            self.addTask(args.task, args.duedate)

    def loadSavedData(self):
        with open('savedata/savedata.txt', 'r+') as f:
            for line in f:    
                name, date = str.split(line,'$')
                self.tasks.append(Task(name.rstrip(), date.rstrip()))

    def saveData(self):
        with open('savedata/savedata.txt', 'w+') as f:
            data = ''
            for num, task in enumerate(self.tasks,0):
                data += self.tasks[num].getTask() + '$' + self.tasks[num].getDueDate() + '\n'

            f.write(data.rstrip())
            print 'Saved data... Goodbye.'

    def display(self, topten=False, withdates=False):
        for num, task in enumerate(self.tasks,1):
            if withdates: print task.getTask() + '\tDue ' + task.getDueDate() 
            else: print task.getTask()
            
            if topten and num > 5: return

    def addTask(self, task, duedate):
        self.tasks.append(Task(task, duedate))
        self.modified = True

    def peek(self):
        self.display(topten=True)

    def viewAll(self):
        self.display(withdates=True)

    def removeTask(self, task):
        if task in self.getAllTasks():
            self.tasks.remove(self.getTaskByName(task))
            print task + ' removed.'
            self.modified = True
        
        else: print task + ' is not in list of tasks.'

    def removeAllTasks(self):
        self.tasks = []
        self.modified = True

    def getAllTasks(self):
        for task in self.tasks: yield task.getTask()

    def getTaskByName(self, taskname):
        for task in self.tasks:
            if task.getTask() == taskname: return task


class Task(object):
    def __init__(self, name, duedate):
        self.task = name
        self.due_date = duedate

    def getTask(self):
        return self.task

    def getDueDate(self):
        return self.due_date


if __name__ == "__main__":
    organizer = Organizer()
    organizer.start()
