#ifndef EXPENSE_H
#define EXPENSE_H

struct Expense {
    QDate date;
    double amount;
    QString category;
    QString description;
};


#endif // EXPENSE_H
