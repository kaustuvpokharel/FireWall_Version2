#include "packetcapturethread.h"

class PacketCaptureThreadData : public QSharedData
{
public:

};

PacketCaptureThread::PacketCaptureThread(const QString& deviceName, QObject* parent)
    : QThread(parent), deviceName(deviceName), stopRequested(false) {}

PacketCaptureThread &PacketCaptureThread::operator=(const PacketCaptureThread &rhs)
{
    if (this != &rhs)
        data.operator=(rhs.data);
    return *this;
}

PacketCaptureThread::~PacketCaptureThread()
{

}

void PacketCaptureThread::run()
{
    char errbuf[PCAP_ERRBUF_SIZE];

    pcap_t* handle = pcap_open_live(deviceName.toStdString().c_str(), BUFSIZ, 0, 1000, errbuf);

    if (handle == nullptr)
    {
        emit packetCaptured(nullptr, nullptr);
        return;
    }

    while (!stopRequested)  // Use an infinite loop
    {
        if (stopRequested)
            break;  // Exit the loop if stop is requested

        struct pcap_pkthdr header;
        const u_char* packetData = pcap_next(handle, &header);

        if (packetData != nullptr)
        {
            emit packetCaptured(&header, packetData);
        }
    }
    qDebug() << "Stop button working";

    pcap_close(handle);
}

void PacketCaptureThread::stopCapture()
{
    stopRequested = true;
}

void PacketCaptureThread::setDeviceName(const QString& deviceName)
{
    this->deviceName = deviceName;
}
