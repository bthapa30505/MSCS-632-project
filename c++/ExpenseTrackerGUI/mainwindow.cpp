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
#include <QMessageBox>
#include "hoverablechartview.h"


struct Expense {
    QDate date;
    double amount;
    QString category;
    QString description;
};

void MainWindow::warn(const QString &message)
{
    QMessageBox::warning(this, "Warning", message);
}


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

    chartView = new HoverableChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);
    ui->chartLayout->addWidget(chartView);

    ui->dateEdit->setDate(QDate::currentDate());
    ui->dateEditTo->setDate(QDate::currentDate());
    ui->dateEditFrom->setDate(QDate(2000, 1, 1));

    loadSampleExpenses();
    updateTable(expenses);
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
    int row = 0;
    for (int i = expenses.size() - 1; i >= 0 ; --i) {
        const Expense &e = expenses[i];

        ui->expenseTable->setItem(row, 0, new QTableWidgetItem(e.date.toString("yyyy-MM-dd")));
        ui->expenseTable->setItem(row, 1, new QTableWidgetItem(QString::number(e.amount, 'f', 2)));
        ui->expenseTable->setItem(row, 2, new QTableWidgetItem(e.category));

        QTableWidgetItem *descItem = new QTableWidgetItem(e.description);
        descItem->setToolTip(e.description);
        ui->expenseTable->setItem(row, 3, descItem);
        row++;
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
    // Hover effect
    for (QPieSlice *slice : series->slices()) {
        connect(slice, &QPieSlice::hovered, this, [=](bool state){
            slice->setExploded(state);
            slice->setLabelVisible(state);
        });
    }
    chart->addSeries(series);
    chart->setTitle("Expense Summary by Category");
    chart->legend()->setAlignment(Qt::AlignRight);

    chartView->setCategoryTotals(categoryTotals);
}


void MainWindow::onAddExpense()
{
    QString amountText = ui->amountEdit->text();
    bool ok;
    double amount = amountText.toDouble(&ok);

    if (!ok || amount <= 0) {
        warn("Please enter a valid positive number for the amount.");
        return;
    }

    QString category = ui->comboBoxCategory->currentText();
    if (category == "Select a category") {
        warn("Please select a valid category.");
        return;
    }

    QDate date = ui->dateEdit->date();
    QString description = ui->descriptionEdit->text();

    addExpense({date, amount, category, description});

    ui->amountEdit->clear();
    ui->descriptionEdit->clear();
}

void MainWindow::loadSampleExpenses() {
    expenses = {
        {QDate(2024, 1, 5), 25.50, "Food", "Lunch at Subway"},
        {QDate(2024, 2, 10), 60.00, "Transport", "Monthly metro card"},
        {QDate(2024, 3, 15), 800.00, "Rent", "March rent"},
        {QDate(2024, 4, 20), 15.75, "Entertainment", "Movie night"},
        {QDate(2024, 5, 3), 30.25, "Food", "Groceries"},
        {QDate(2024, 5, 18), 40.00, "Other", "Gift for friend"},
        {QDate(2024, 6, 1), 900.00, "Rent", "June rent"},
        {QDate(2024, 6, 10), 20.00, "Transport", "Uber ride"},
        {QDate(2024, 7, 4), 35.00, "Entertainment", "Fourth of July BBQ"},
        {QDate::currentDate(), 12.99, "Food", "Coffee and snack"}
    };
}

