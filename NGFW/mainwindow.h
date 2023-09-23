#ifndef MAINWINDOW_H
#define MAINWINDOW_H


#include "QtWidgets/qcombobox.h"
#include "QtWidgets/qtextedit.h"
#include "packetcapturethread.h"
#include <QMainWindow>


//Manually added libraries here
#include <QFileDialog>
#include <pcap.h>

#include <netinet/in.h>        // For struct ip
#include <netinet/ip.h>        // For struct ip
#include <netinet/if_ether.h>  // For struct ether_header
#include <netinet/tcp.h>       // For struct tcphdr
#include <arpa/inet.h>         // For inet_ntop
#include <pcap.h>              // For struct pcap_pkthdr
#include <QDateTime>           // For QDateTime
#include <QString>

#include <QTcpSocket>
#include <QJsonObject>
#include <QJsonDocument>
#include <QTextCursor>
#include <QColor>


QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void startCapture();
    void stopCapture();
    void packetHandler(const struct pcap_pkthdr *header, const u_char *packetData);
    void saveToFile();
    void selectInterface(int index);
    void sendPacketDataToPython(const QByteArray &packetData);
private:
    Ui::MainWindow *ui;
    QPushButton *startButton;
    QPushButton *stopButton;
    QPushButton *saveButton;
    QTextEdit *outputText;
    QComboBox *interfaceComboBox;
    pcap_if_t *allDevs;
    pcap_t *handle;
    bool isCapturing;
    FILE *outputFile;
    PacketCaptureThread *captureThread;

    bool stopping;


    static void packetHandlerCallback(u_char *userData, const struct pcap_pkthdr *header, const u_char *packetData);
};

#endif // MAINWINDOW_H
