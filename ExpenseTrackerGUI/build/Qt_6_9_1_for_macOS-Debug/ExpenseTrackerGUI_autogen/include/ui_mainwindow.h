/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 6.9.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QDateEdit>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTableWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QLineEdit *amountEdit;
    QLineEdit *descriptionEdit;
    QComboBox *comboBoxCategory;
    QDateEdit *dateEdit;
    QPushButton *addButton;
    QTableWidget *expenseTable;
    QLabel *label;
    QLabel *label_2;
    QLabel *label_3;
    QLabel *label_4;
    QDateEdit *dateEditFrom;
    QDateEdit *dateEditTo;
    QComboBox *comboBoxFilterCategory;
    QLabel *label_6;
    QLineEdit *lineEdit;
    QLabel *label_7;
    QLabel *label_8;
    QLabel *label_9;
    QLabel *label_10;
    QLabel *label_11;
    QLineEdit *lineEditAmount_2;
    QPushButton *filterButton;
    QLabel *summaryLabel;
    QWidget *verticalLayoutWidget;
    QVBoxLayout *chartLayout;
    QMenuBar *menubar;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName("MainWindow");
        MainWindow->resize(800, 677);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName("centralwidget");
        amountEdit = new QLineEdit(centralwidget);
        amountEdit->setObjectName("amountEdit");
        amountEdit->setGeometry(QRect(90, 40, 113, 21));
        descriptionEdit = new QLineEdit(centralwidget);
        descriptionEdit->setObjectName("descriptionEdit");
        descriptionEdit->setGeometry(QRect(110, 70, 461, 21));
        comboBoxCategory = new QComboBox(centralwidget);
        comboBoxCategory->setObjectName("comboBoxCategory");
        comboBoxCategory->setGeometry(QRect(322, 30, 151, 32));
        dateEdit = new QDateEdit(centralwidget);
        dateEdit->setObjectName("dateEdit");
        dateEdit->setGeometry(QRect(560, 40, 110, 22));
        addButton = new QPushButton(centralwidget);
        addButton->setObjectName("addButton");
        addButton->setGeometry(QRect(610, 70, 100, 32));
        expenseTable = new QTableWidget(centralwidget);
        expenseTable->setObjectName("expenseTable");
        expenseTable->setGeometry(QRect(-10, 200, 821, 261));
        label = new QLabel(centralwidget);
        label->setObjectName("label");
        label->setGeometry(QRect(40, 40, 58, 16));
        label_2 = new QLabel(centralwidget);
        label_2->setObjectName("label_2");
        label_2->setGeometry(QRect(40, 70, 71, 16));
        label_3 = new QLabel(centralwidget);
        label_3->setObjectName("label_3");
        label_3->setGeometry(QRect(260, 40, 58, 16));
        label_4 = new QLabel(centralwidget);
        label_4->setObjectName("label_4");
        label_4->setGeometry(QRect(520, 40, 41, 16));
        dateEditFrom = new QDateEdit(centralwidget);
        dateEditFrom->setObjectName("dateEditFrom");
        dateEditFrom->setGeometry(QRect(80, 170, 110, 22));
        dateEditFrom->setDateTime(QDateTime(QDate(1999, 12, 1), QTime(5, 0, 0)));
        dateEditTo = new QDateEdit(centralwidget);
        dateEditTo->setObjectName("dateEditTo");
        dateEditTo->setGeometry(QRect(230, 170, 110, 22));
        comboBoxFilterCategory = new QComboBox(centralwidget);
        comboBoxFilterCategory->setObjectName("comboBoxFilterCategory");
        comboBoxFilterCategory->setGeometry(QRect(410, 160, 91, 32));
        label_6 = new QLabel(centralwidget);
        label_6->setObjectName("label_6");
        label_6->setGeometry(QRect(30, 140, 131, 16));
        lineEdit = new QLineEdit(centralwidget);
        lineEdit->setObjectName("lineEdit");
        lineEdit->setGeometry(QRect(0, 110, 801, 20));
        label_7 = new QLabel(centralwidget);
        label_7->setObjectName("label_7");
        label_7->setGeometry(QRect(40, 170, 41, 16));
        label_8 = new QLabel(centralwidget);
        label_8->setObjectName("label_8");
        label_8->setGeometry(QRect(200, 170, 41, 16));
        label_9 = new QLabel(centralwidget);
        label_9->setObjectName("label_9");
        label_9->setGeometry(QRect(20, 0, 131, 16));
        label_10 = new QLabel(centralwidget);
        label_10->setObjectName("label_10");
        label_10->setGeometry(QRect(350, 170, 58, 16));
        label_11 = new QLabel(centralwidget);
        label_11->setObjectName("label_11");
        label_11->setGeometry(QRect(500, 170, 58, 16));
        lineEditAmount_2 = new QLineEdit(centralwidget);
        lineEditAmount_2->setObjectName("lineEditAmount_2");
        lineEditAmount_2->setGeometry(QRect(550, 170, 113, 21));
        filterButton = new QPushButton(centralwidget);
        filterButton->setObjectName("filterButton");
        filterButton->setGeometry(QRect(680, 160, 61, 32));
        summaryLabel = new QLabel(centralwidget);
        summaryLabel->setObjectName("summaryLabel");
        summaryLabel->setGeometry(QRect(67, 470, 291, 151));
        verticalLayoutWidget = new QWidget(centralwidget);
        verticalLayoutWidget->setObjectName("verticalLayoutWidget");
        verticalLayoutWidget->setGeometry(QRect(410, 460, 371, 191));
        chartLayout = new QVBoxLayout(verticalLayoutWidget);
        chartLayout->setObjectName("chartLayout");
        chartLayout->setContentsMargins(0, 0, 0, 0);
        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName("menubar");
        menubar->setGeometry(QRect(0, 0, 800, 24));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName("statusbar");
        MainWindow->setStatusBar(statusbar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        addButton->setText(QCoreApplication::translate("MainWindow", "Add Expense", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "Amount", nullptr));
        label_2->setText(QCoreApplication::translate("MainWindow", "Description", nullptr));
        label_3->setText(QCoreApplication::translate("MainWindow", "Category", nullptr));
        label_4->setText(QCoreApplication::translate("MainWindow", "Date", nullptr));
        comboBoxFilterCategory->setCurrentText(QString());
        comboBoxFilterCategory->setPlaceholderText(QCoreApplication::translate("MainWindow", "All", nullptr));
        label_6->setText(QCoreApplication::translate("MainWindow", "Filter & Search", nullptr));
        label_7->setText(QCoreApplication::translate("MainWindow", "From:", nullptr));
        label_8->setText(QCoreApplication::translate("MainWindow", "To:", nullptr));
        label_9->setText(QCoreApplication::translate("MainWindow", "Add New Expenses", nullptr));
        label_10->setText(QCoreApplication::translate("MainWindow", "Category:", nullptr));
        label_11->setText(QCoreApplication::translate("MainWindow", "Search:", nullptr));
        filterButton->setText(QCoreApplication::translate("MainWindow", "Search", nullptr));
        summaryLabel->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
