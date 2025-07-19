#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QTableWidgetItem>
#include <QDate>
#include <QDebug>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QtCharts/QChartView>
#include <QtCharts/QPieSeries>
#include <QtCharts/QPieSlice>
#include <QGroupBox>


struct Expense {
    QDate date;
    double amount;
    QString category;
    QString description;
};

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    ui->comboBoxCategory->addItems({"Select a category", "Food", "Transport", "Rent", "Entertainment", "Other"});

    connect(ui->filterButton, &QPushButton::clicked, this, &MainWindow::applyFilters);
    connect(ui->addButton, &QPushButton::clicked, this, &MainWindow::onAddExpense);

    ui->expenseTable->setColumnCount(4);
    ui->expenseTable->setHorizontalHeaderLabels({"Date", "Amount", "Category", "Description"});
    ui->expenseTable->horizontalHeader()->setSectionResizeMode(3, QHeaderView::Stretch);

    chart = new QChart();
    chartView = new QChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);
    ui->chartLayout->addWidget(chartView);

    ui->dateEdit->setDate(QDate::currentDate());
    ui->dateEditTo->setDate(QDate::currentDate());
    ui->dateEditFrom->setDate(QDate(2000, 1, 1));

    // Load with no data initially
    applyFilters();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::addExpense(const Expense &exp)
{
    expenses.emplace_back(exp);
    updateTable(expenses);
}

void MainWindow::applyFilters()
{
    QVector<Expense> filtered;

    QDate fromDate = ui->dateEditFrom->date();
    QDate toDate = ui->dateEditTo->date();
    QString selectedCategory = ui->comboBoxCategory->currentText();

    for (const Expense& exp : expenses) {
        if (exp.date < fromDate || exp.date > toDate)
            continue;

        if (selectedCategory != "All" && exp.category != selectedCategory)
            continue;

        filtered.append(exp);
    }

    updateTable(filtered);
}

void MainWindow::updateTable(const QVector<Expense>& expenses)
{
    filteredExpenses = expenses; // Update the class-level filtered copy

    ui->expenseTable->setRowCount(expenses.size());

    for (int i = 0; i < expenses.size(); ++i) {
        const Expense &e = expenses[i];

        ui->expenseTable->setItem(i, 0, new QTableWidgetItem(e.date.toString("yyyy-MM-dd")));
        ui->expenseTable->setItem(i, 1, new QTableWidgetItem(QString::number(e.amount, 'f', 2)));
        ui->expenseTable->setItem(i, 2, new QTableWidgetItem(e.category));

        QTableWidgetItem *descItem = new QTableWidgetItem(e.description);
        descItem->setToolTip(e.description);
        ui->expenseTable->setItem(i, 3, descItem);
    }

    updateSummary();
}

void MainWindow::updateSummary()
{
    double total = 0.0;
    QMap<QString, double> categoryTotals;

    for (const Expense &e : filteredExpenses) {
        total += e.amount;
        categoryTotals[e.category] += e.amount;
    }

    QString html = "<h3>Total Expenses: $" + QString::number(total, 'f', 2) + "</h3><ul>";
    for (auto it = categoryTotals.begin(); it != categoryTotals.end(); ++it) {
        html += "<li><b>" + it.key() + ":</b> $" + QString::number(it.value(), 'f', 2) + "</li>";
    }
    html += "</ul>";
    ui->summaryLabel->setText(html);
    ui->summaryLabel->setTextFormat(Qt::RichText);
    ui->summaryLabel->adjustSize();

    chart->removeAllSeries();
    QPieSeries *series = new QPieSeries();
    for (auto it = categoryTotals.begin(); it != categoryTotals.end(); ++it) {
        series->append(it.key(), it.value());
    }
    chart->addSeries(series);
    chart->setTitle("Expense Breakdown");
}

void MainWindow::onAddExpense()
{
    QDate date = ui->dateEdit->date();
    double amount = ui->amountEdit->text().toDouble();
    QString category = ui->comboBoxCategory->currentText();
    QString description = ui->descriptionEdit->text();

    if (category == "Select a category") return; // Skip "All" for entry
    if (amount <= 0) return;

    addExpense({date, amount, category, description});

    ui->amountEdit->clear();
    ui->descriptionEdit->clear();
}
