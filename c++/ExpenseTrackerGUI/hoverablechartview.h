#ifndef HOVERABLECHARTVIEW_H
#define HOVERABLECHARTVIEW_H

#include <QtCharts/QChartView>

class ChartPopup;

class HoverableChartView : public QChartView
{
    Q_OBJECT
public:
    explicit HoverableChartView(QChart *chart, QWidget *parent = nullptr);
    ~HoverableChartView();

protected:
    bool event(QEvent *event) override;

private:
    ChartPopup *popup = nullptr;
    QMap<QString, double> currentData;
public slots:
    void setCategoryTotals(const QMap<QString, double> &totals);
};

#endif // HOVERABLECHARTVIEW_H
