#!/usr/bin/env python3

import datetime
import pickle
import os

def getNewMark():
    points = input('Zdobyte punkty: ')
    pool = input('Pula powiększona o: ')
    category = input('Kategoria oceny: ')
    comment = input('Komentarz: (jedna linia) ')
    return (points, pool, category, comment)


class Mark:
    def __init__(self, points, pool, category, comment):
        self.points = points
        self.pool = pool
        self.category = category
        self.comment = comment


class Report:
    def __init__(self, reportCreationTime, date, slot, present,
                        teacherPresent, revoked, additional, teacher,
                        group, comment, marks):
        self.reportCreationTime = reportCreationTime
        self.date = date
        self.slot = slot
        self.present = present
        self.teacherPresent = teacherPresent
        self.revoked = revoked
        self.additional = additional
        self.teacher = teacher
        self.group = group
        self.comment = comment
        self.marks = marks

reports = []


def tryMigration1():
    store = []
    result = []
    try:
        with open('/home/evil/raporty', 'rb') as inputFile:
            store = pickle.load(inputFile)
    except IOError:
        pass
    for (reportCreationTime, date, slot, present, teacherPresent,
            revoked, additional, teacher, group, comment, marks) in store:
                newMarks = []
                for (points, pool, category, comment) in marks:
                    newMarks.append(Mark(points, pool, category, comment))
                result.append(Report(
                                     reportCreationTime, date, slot, present,
                                     teacherPresent, revoked, additional,
                                     teacher, group, comment, newMarks))
    return result


def main():
    store = []
    try:
        with open('/home/evil/raporty', 'rb') as inputFile:
            store = pickle.load(inputFile)
    except IOError:
        print(' Baza jest tworzona')
    while True:
        x = input('Dodać kolejny raport? [t/N] ')
        if len(x) < 1 or x[0].lower() != 't':
            break
        reportCreationTime = datetime.datetime.now()
        x = input('Data: (dd-mm-rrrr) [dzisiaj] ')
        if len(x) == 0:
            date = datetime.date.today()
        else:
            x = x.split('-')
            date = datetime.date(int(x[2]), int(x[1]), int(x[0]))
        slot = input('Godzina rozpoczęcia zajęć: ')
        present = input('Czy byłeś obecny? [T/opis] ')
        if len(present) < 1:
            present = 'Tak'
        teacherPresent = input('Czy nauczyciel był obecny? [T/opis] ')
        if len(teacherPresent) < 1:
            teacherPresent = 'Tak'
        revoked = input('Czy zajęcia zostały odwołane? [N/opis] ')
        if len(revoked) < 1:
            revoked = 'Nie'
        additional = input('Czy zajęcia były dodatkowe [N/opis] ')
        if len(additional) < 1:
            additional = 'Nie'
        teacher = input('Nauczyciel: ')
        group = input('Przedmiot i grupa: ')
        comment = input('Komentarz: (jedna linia) ')
        marks = []
        while True:
            x = input('Czy chcesz dodać ocene? [t/N] ')
            if len(x) < 1 or x[0].lower() != 't':
                break
            marks.append(getNewMark())

        print()
        print('Raport stworzono: ', reportCreationTime)
        print('Data:             ', date)
        print('Godzina:          ', slot)
        print('Obecny :          ', present)
        print('Nauczyciel obecny:', teacherPresent)
        print('Odwołane:         ', revoked)
        print('Dodatkowe:        ', additional)
        print('Nauczyciel:       ', teacher)
        print('Grupa:            ', group)
        print('Komentarz:        ', comment)
        print('Oceny:')
        for (points, pool, category, comment) in marks:
            print(points, '/', pool, ' - ', category, sep='')
            print('Komentarz:', comment)
        x = input('Dodać do bazy? [T/n]: ')
        if len(x) >= 1 and x[0].lower() != 't':
            continue
        store.append((reportCreationTime, date, slot, present, teacherPresent, revoked, additional, teacher, group, comment, marks))

    x = input('Czy chcesz wyświetlić zawartość bazy? [t/N] ')
    if len(x) >= 1 and x[0].lower() == 't':
        for (reportCreationTime, date, slot, present, teacherPresent, revoked, additional, teacher, group, comment, marks) in store:
            print()
            print('Raport stworzono: ', reportCreationTime)
            print('Data:             ', date)
            print('Godzina:          ', slot)
            print('Obecny :          ', present)
            print('Nauczyciel obecny:', teacherPresent)
            print('Odwołane:         ', revoked)
            print('Dodatkowe:        ', additional)
            print('Nauczyciel:       ', teacher)
            print('Grupa:            ', group)
            print('Komentarz:        ', comment)
            print('Oceny:')
            for (points, pool, category, comment) in marks:
                print(points, '/', pool, ' - ', category, sep='')
                print('Komentarz:', comment)
    with open('/home/evil/raporty', 'wb') as outputFile:
        pickle.dump(store, outputFile, protocol=3)

if __name__ == "__main__":
    main()
