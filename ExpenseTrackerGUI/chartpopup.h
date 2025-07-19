#ifndef CHARTPOPUP_H
#define CHARTPOPUP_H

#include <QWidget>
#include <QtCharts/QChartView>
#include <QtCharts/QPieSeries>

class ChartPopup : public QWidget
{
    Q_OBJECT
public:
    explicit ChartPopup(QWidget *parent = nullptr);

    void setData(const QMap<QString, double>& categoryTotals);

protected:
    void leaveEvent(QEvent *event) override;

signals:
    void popupClosed();

private:
    QChartView *chartView;
    QChart *chart;
};

#endif // CHARTPOPUP_H
