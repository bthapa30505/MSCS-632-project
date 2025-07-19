#include "chartpopup.h"
#include <QVBoxLayout>
#include <QScreen>
#include <QApplication>

ChartPopup::ChartPopup(QWidget *parent) : QWidget(parent, Qt::Popup | Qt::FramelessWindowHint)
{
    setAttribute(Qt::WA_DeleteOnClose, false);
    setAttribute(Qt::WA_TranslucentBackground);

    chart = new QChart();
    chartView = new QChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);

    QVBoxLayout *layout = new QVBoxLayout(this);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->addWidget(chartView);

    resize(600, 600);
}

void ChartPopup::setData(const QMap<QString, double> &categoryTotals)
{
    chart->removeAllSeries();

    QPieSeries *series = new QPieSeries();
    for (auto it = categoryTotals.begin(); it != categoryTotals.end(); ++it) {
        series->append(it.key(), it.value());
    }
    chart->addSeries(series);
    chart->setTitle("Expense Breakdown");
}

void ChartPopup::leaveEvent(QEvent *event)
{
    Q_UNUSED(event);
    hide();
    emit popupClosed();
}
