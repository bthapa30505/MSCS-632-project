#include <QVector>
#include <QtCharts>
#include "hoverablechartview.h"


struct Expense;

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    void addExpense(const Expense &exp);
    void onAddExpense();
    void applyFilters();
    void updateTable(const QVector<Expense>& expenses);
    void updateSummary();
    void loadSampleExpenses();
    void warn(const QString &message);

private:
    Ui::MainWindow *ui;

    QVector<Expense> expenses;
    QVector<Expense> filteredExpenses;

    QChart *chart;
    HoverableChartView *chartView;

};
