#ifndef PACKETCAPTURETHREAD_H
#define PACKETCAPTURETHREAD_H

#include <QMainWindow>
#include <QObject>
#include <QSharedDataPointer>
#include <QWidget>

#include <QThread>
#include <pcap.h>

class PacketCaptureThreadData;

class PacketCaptureThread : public QThread
{
    Q_OBJECT
public:
    //explicit PacketCaptureThread(QObject *parent = nullptr);
    PacketCaptureThread(const QString& deviceName, QObject* parent = nullptr);
    PacketCaptureThread &operator=(const PacketCaptureThread &);
    ~PacketCaptureThread();
    void run() override;
    void stopCapture();
    void setDeviceName(const QString& deviceName);

signals:
    void packetCaptured(const struct pcap_pkthdr* header, const u_char* packetData);

private:
    QSharedDataPointer<PacketCaptureThreadData> data;
    QString deviceName; // Store the selected device name here
    volatile bool stopRequested;
};

#endif // PACKETCAPTURETHREAD_H
