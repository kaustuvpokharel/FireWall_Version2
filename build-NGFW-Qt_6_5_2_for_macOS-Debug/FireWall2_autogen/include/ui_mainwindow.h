/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 6.5.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QHBoxLayout *horizontalLayout;
    QVBoxLayout *verticalLayout;
    QHBoxLayout *horizontalLayout_2;
    QLabel *w;
    QLabel *label_3;
    QSpacerItem *horizontalSpacer;
    QLabel *Y;
    QLabel *label_4;
    QSpacerItem *horizontalSpacer_2;
    QLabel *R;
    QLabel *label_5;
    QTextEdit *outputText;
    QVBoxLayout *verticalLayout_2;
    QSpacerItem *verticalSpacer;
    QLabel *label;
    QLabel *label_2;
    QComboBox *interfaceComboBox;
    QLabel *label_6;
    QPushButton *startButton;
    QPushButton *stopButton;
    QPushButton *saveButton;
    QHBoxLayout *horizontalLayout_4;
    QSpacerItem *verticalSpacer_2;
    QMenuBar *menubar;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName("MainWindow");
        MainWindow->setEnabled(true);
        MainWindow->resize(976, 537);
        QFont font;
        font.setFamilies({QString::fromUtf8(".AppleSystemUIFont")});
        MainWindow->setFont(font);
        MainWindow->setDocumentMode(false);
        MainWindow->setDockNestingEnabled(false);
        MainWindow->setUnifiedTitleAndToolBarOnMac(false);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName("centralwidget");
        horizontalLayout = new QHBoxLayout(centralwidget);
        horizontalLayout->setObjectName("horizontalLayout");
        verticalLayout = new QVBoxLayout();
        verticalLayout->setObjectName("verticalLayout");
        horizontalLayout_2 = new QHBoxLayout();
        horizontalLayout_2->setObjectName("horizontalLayout_2");
        w = new QLabel(centralwidget);
        w->setObjectName("w");
        w->setMaximumSize(QSize(46, 23));
        w->setPixmap(QPixmap(QString::fromUtf8("../../../Documents/QT_learn/Firewall2/Resources/W.png")));
        w->setScaledContents(true);

        horizontalLayout_2->addWidget(w);

        label_3 = new QLabel(centralwidget);
        label_3->setObjectName("label_3");
        QFont font1;
        font1.setFamilies({QString::fromUtf8("Poppins")});
        font1.setPointSize(15);
        label_3->setFont(font1);

        horizontalLayout_2->addWidget(label_3);

        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer);

        Y = new QLabel(centralwidget);
        Y->setObjectName("Y");
        Y->setMaximumSize(QSize(46, 23));
        Y->setPixmap(QPixmap(QString::fromUtf8("../../../Documents/QT_learn/Firewall2/Resources/Y.png")));
        Y->setScaledContents(true);

        horizontalLayout_2->addWidget(Y);

        label_4 = new QLabel(centralwidget);
        label_4->setObjectName("label_4");
        label_4->setFont(font1);

        horizontalLayout_2->addWidget(label_4);

        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

        horizontalLayout_2->addItem(horizontalSpacer_2);

        R = new QLabel(centralwidget);
        R->setObjectName("R");
        R->setMaximumSize(QSize(46, 23));
        R->setPixmap(QPixmap(QString::fromUtf8("../../../Documents/QT_learn/Firewall2/Resources/R.png")));
        R->setScaledContents(true);

        horizontalLayout_2->addWidget(R);

        label_5 = new QLabel(centralwidget);
        label_5->setObjectName("label_5");
        label_5->setFont(font1);
        label_5->setScaledContents(false);

        horizontalLayout_2->addWidget(label_5);


        verticalLayout->addLayout(horizontalLayout_2);

        outputText = new QTextEdit(centralwidget);
        outputText->setObjectName("outputText");

        verticalLayout->addWidget(outputText);


        horizontalLayout->addLayout(verticalLayout);

        verticalLayout_2 = new QVBoxLayout();
        verticalLayout_2->setObjectName("verticalLayout_2");
        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout_2->addItem(verticalSpacer);

        label = new QLabel(centralwidget);
        label->setObjectName("label");
        label->setMaximumSize(QSize(300, 300));
        label->setPixmap(QPixmap(QString::fromUtf8("../../../Documents/QT_learn/Firewall2/Resources/logo.png")));
        label->setScaledContents(true);
        label->setAlignment(Qt::AlignCenter);
        label->setWordWrap(false);
        label->setOpenExternalLinks(false);
        label->setTextInteractionFlags(Qt::LinksAccessibleByMouse);

        verticalLayout_2->addWidget(label);

        label_2 = new QLabel(centralwidget);
        label_2->setObjectName("label_2");
        QFont font2;
        font2.setFamilies({QString::fromUtf8("Poppins")});
        font2.setPointSize(18);
        font2.setBold(true);
        label_2->setFont(font2);

        verticalLayout_2->addWidget(label_2);

        interfaceComboBox = new QComboBox(centralwidget);
        interfaceComboBox->setObjectName("interfaceComboBox");
        QFont font3;
        font3.setFamilies({QString::fromUtf8("Poppins")});
        interfaceComboBox->setFont(font3);

        verticalLayout_2->addWidget(interfaceComboBox);

        label_6 = new QLabel(centralwidget);
        label_6->setObjectName("label_6");

        verticalLayout_2->addWidget(label_6);

        startButton = new QPushButton(centralwidget);
        startButton->setObjectName("startButton");
        QFont font4;
        font4.setFamilies({QString::fromUtf8("Poppins")});
        font4.setPointSize(14);
        startButton->setFont(font4);

        verticalLayout_2->addWidget(startButton);

        stopButton = new QPushButton(centralwidget);
        stopButton->setObjectName("stopButton");
        stopButton->setFont(font4);

        verticalLayout_2->addWidget(stopButton);

        saveButton = new QPushButton(centralwidget);
        saveButton->setObjectName("saveButton");

        verticalLayout_2->addWidget(saveButton);

        horizontalLayout_4 = new QHBoxLayout();
        horizontalLayout_4->setObjectName("horizontalLayout_4");

        verticalLayout_2->addLayout(horizontalLayout_4);

        verticalSpacer_2 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

        verticalLayout_2->addItem(verticalSpacer_2);


        horizontalLayout->addLayout(verticalLayout_2);

        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName("menubar");
        menubar->setGeometry(QRect(0, 0, 976, 22));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName("statusbar");
        MainWindow->setStatusBar(statusbar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "FIREWALL.2", nullptr));
        w->setText(QString());
        label_3->setText(QCoreApplication::translate("MainWindow", "Safe", nullptr));
        Y->setText(QString());
        label_4->setText(QCoreApplication::translate("MainWindow", "Flag", nullptr));
        R->setText(QString());
        label_5->setText(QCoreApplication::translate("MainWindow", "Unsafe", nullptr));
        label->setText(QString());
        label_2->setText(QCoreApplication::translate("MainWindow", "Select your Network Interface:", nullptr));
        label_6->setText(QString());
        startButton->setText(QCoreApplication::translate("MainWindow", "Start", nullptr));
        stopButton->setText(QCoreApplication::translate("MainWindow", "Stop", nullptr));
        saveButton->setText(QCoreApplication::translate("MainWindow", "Save To File", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
