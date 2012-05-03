#!/usr/bin/env python3

import datetime
import pickle
import os


class Mark:
    def __init__(self, points, pool, category, comment):
        self.points = points
        self.pool = pool
        self.category = category
        self.comment = comment


def getNewMark():
    points = input('Zdobyte punkty: ')
    pool = input('Pula powiększona o: ')
    category = input('Kategoria oceny: ')
    comment = input('Komentarz: (jedna linia) ')
    return Mark(points, pool, category, comment)


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

migration1 = False


def tryMigration1():
    store = []
    result = []
    try:
        with open('/home/evil/raporty', 'rb') as inputFile:
            store = pickle.load(inputFile)
        global migration1
        migration1 = True
        print('Wykonano migrację 1')
        for (reportCreationTime, date, slot, present, teacherPresent,
                revoked, additional, teacher, group, comment, marks) in store:
                    newMarks = []
                    for (points, pool, category, comment) in marks:
                        newMarks.append(Mark(points, pool, category, comment))
                    result.append(Report(
                                        reportCreationTime, date, slot,
                                        present, teacherPresent, revoked,
                                        additional, teacher, group, comment,
                                        newMarks))
    except IOError:
        pass
    return result


def storeData(data):
    with open('/home/evil/Studia/raporty', 'wb') as outputFile:
        pickle.dump(data, outputFile, protocol=3)
    global migration1
    if migration1:
        os.remove('/home/evil/raporty')


def loadData(data):
    try:
        with open('/home/evil/Studia/raporty', 'rb') as inputFile:
            newData = pickle.load(inputFile)
            data.extend(newData)
    except IOError:
        pass
    except EOFError:
        print('EOF <- plik wygląda na przycięty')
        raise
    return data


def main():
    store = tryMigration1()
    store = loadData(store)
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
        for mark in marks:
            print(mark.points, '/', mark.pool, ' - ', mark.category, sep='')
            print('Komentarz:', mark.comment)
        x = input('Dodać do bazy? [T/n]: ')
        if len(x) >= 1 and x[0].lower() != 't':
            continue
        store.append(Report(reportCreationTime, date, slot, present,
                             teacherPresent, revoked, additional, teacher,
                             group, comment, marks))

    x = input('Czy chcesz wyświetlić zawartość bazy? [t/N] ')
    if len(x) >= 1 and x[0].lower() == 't':
        for report in store:
            print()
            print('Raport stworzono: ', report.reportCreationTime)
            print('Data:             ', report.date)
            print('Godzina:          ', report.slot)
            print('Obecny :          ', report.present)
            print('Nauczyciel obecny:', report.teacherPresent)
            print('Odwołane:         ', report.revoked)
            print('Dodatkowe:        ', report.additional)
            print('Nauczyciel:       ', report.teacher)
            print('Grupa:            ', report.group)
            print('Komentarz:        ', report.comment)
            print('Oceny:')
            for mark in report.marks:
                print(mark.points, '/', mark.pool, ' - ',
                          mark.category, sep='')
                print('Komentarz:', mark.comment)
    storeData(store)

if __name__ == "__main__":
    main()
