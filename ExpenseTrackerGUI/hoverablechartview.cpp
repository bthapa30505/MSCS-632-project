#include "hoverablechartview.h"
#include "chartpopup.h"
#include <QEvent>
#include <QApplication>
#include <QScreen>

HoverableChartView::HoverableChartView(QChart *chart, QWidget *parent)
    : QChartView(chart, parent)
{
    setAttribute(Qt::WA_Hover);

    popup = new ChartPopup();
    popup->hide();

    connect(popup, &ChartPopup::popupClosed, [this]() {
        this->setVisible(true);
    });
}

HoverableChartView::~HoverableChartView()
{
    if (popup) {
        popup->hide();
        delete popup;
        popup = nullptr;
    }
}

void HoverableChartView::setCategoryTotals(const QMap<QString, double> &totals)
{
    currentData = totals;
    if (popup)
        popup->setData(totals);
}

bool HoverableChartView::event(QEvent *event)
{
    if (event->type() == QEvent::HoverEnter) {
        // Hide this small chart
        this->setVisible(false);

        // Center popup on screen
        QRect screenRect = QApplication::primaryScreen()->geometry();
        popup->move(screenRect.center() - QPoint(popup->width()/2, popup->height()/2));

        // Update popup data & show it
        popup->setData(currentData);
        popup->show();

        return true;
    }
    else if (event->type() == QEvent::HoverLeave) {
        // Hide popup & show this chart again
        if (popup->isVisible())
            popup->hide();
        this->setVisible(true);

        return true;
    }

    return QChartView::event(event);
}
