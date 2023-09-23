#include "mainwindow.h"
#include "./ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), handle(nullptr), isCapturing(false), outputFile(nullptr)
    , ui(new Ui::MainWindow)
{

    ui->setupUi(this);

    startButton = ui->startButton;
    stopButton = ui->stopButton;
    saveButton = ui->saveButton;
    outputText = ui->outputText;
    interfaceComboBox = ui->interfaceComboBox;

    connect(startButton, &QPushButton::clicked, this, &MainWindow::startCapture);
    connect(stopButton, &QPushButton::clicked, this, &MainWindow::stopCapture);
    connect(saveButton, &QPushButton::clicked, this, &MainWindow::saveToFile);
    connect(interfaceComboBox, static_cast<void (QComboBox::*)(int)>(&QComboBox::activated), this, &MainWindow::selectInterface);

    captureThread = new PacketCaptureThread("", this); // Initialize the capture thread
    connect(captureThread, &PacketCaptureThread::packetCaptured, this, &MainWindow::packetHandler);

    char errbuf[PCAP_ERRBUF_SIZE];
    if(pcap_findalldevs(&allDevs, errbuf) == -1)
    {
        outputText->append(QString("Error finding the network devices: %1").arg(errbuf));
    }
    else
    {
        pcap_if_t *dev;
        for(dev = allDevs; dev != nullptr; dev = dev->next)
        {
            interfaceComboBox->addItem(dev->name);
        }
    }
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::startCapture()
{
    qInfo()<<("Test case apple passed");
    if(isCapturing || stopping)
    {
        stopCapture();
    }
    if(captureThread ->isRunning())
    {
        captureThread->wait();
    }

    int selectedIndex = interfaceComboBox->currentIndex();
    pcap_if_t *selectedDev = allDevs;
    for(int i = 0; i < selectedIndex; i++)
    {
        selectedDev = selectedDev->next;
    }

    char errbuf[PCAP_ERRBUF_SIZE];

    if(handle)
    {
        pcap_close(handle);
        handle = nullptr;
    }

    handle = pcap_open_live(selectedDev->name, BUFSIZ, 0, 1000, errbuf);
    qInfo()<<("Test case 1 passed");

    if(handle == nullptr)
    {
        qInfo()<<("Test case 2 passed");

        outputText->append(QString("Error opening device: %1").arg(errbuf));
        return;
    }
    qInfo()<<("Test case 3 passed");

    isCapturing = true;
    outputText->append("+++++++++++ Packet started to get captured +++++++++");
    outputText->append("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n");
    qInfo()<<("Test case 4 passed");

    // Start the capture thread and pass the selected device name.
    captureThread->setDeviceName(selectedDev->name); // Use -> operator
    captureThread->start();
    qInfo()<<("Test case 5 passed");

}

void MainWindow::stopCapture()
{
    qDebug() << "Stopping capture...";
    if (!isCapturing || stopping)
        return;

    stopping = true;

    // Stop and reset the capture thread
    captureThread->stopCapture();
    captureThread->wait();
    captureThread->terminate(); // Terminate the thread
    captureThread->deleteLater(); // Delete the thread and free resources
    captureThread = new PacketCaptureThread("", this); // Create a new thread
    connect(captureThread, &PacketCaptureThread::packetCaptured, this, &MainWindow::packetHandler);

    qDebug() << "Capture Thread is stopped";

    pcap_close(handle);

    isCapturing = false;
    stopping = false;

    startButton->setEnabled(true);

    outputText->append("Packet capture stopped.");
    handle = nullptr;
}

void MainWindow::packetHandler(const struct pcap_pkthdr *header, const u_char *packetData)
{
    // Extract Ethernet header information
    const struct ether_header *ethHeader = reinterpret_cast<const struct ether_header*>(packetData);

    // Initialize tcpHeader as nullptr
    const struct tcphdr *tcpHeader = nullptr;

    // Check if the packet is an IP packet (Ethernet type = 0x0800 for IPv4)
    if (ntohs(ethHeader->ether_type) == ETHERTYPE_IP)
    {
        // Extract IP header information
        const struct ip *ipHeader = reinterpret_cast<const struct ip*>(packetData + sizeof(struct ether_header));

        // Get source and destination IP addresses
        char sourceIp[INET_ADDRSTRLEN];
        char destIp[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &(ipHeader->ip_src), sourceIp, INET_ADDRSTRLEN);
        inet_ntop(AF_INET, &(ipHeader->ip_dst), destIp, INET_ADDRSTRLEN);

        // Extract the timestamp and length from the packet header
        const QDateTime timestamp = QDateTime::fromSecsSinceEpoch(header->ts.tv_sec);
        const int length = header->len;

        // Check if it's a TCP packet (IP protocol number = 6 for TCP)
        if (ipHeader->ip_p == IPPROTO_TCP)
        {
            // Extract TCP header information
            tcpHeader = reinterpret_cast<const struct tcphdr*>(packetData + sizeof(struct ether_header) + (ipHeader->ip_hl << 2));
        }

        // Format the packet information
        QString packetInfo =
            QString("Source IP:\t%1\t\tDestination IP:\t%2\n")
                .arg(sourceIp)
                .arg(destIp)
            + QString("Source Port:\t%1\t\tDestination Port:\t%2\n")
                  .arg(tcpHeader ? ntohs(tcpHeader->th_sport) : 0)
                  .arg(tcpHeader ? ntohs(tcpHeader->th_dport) : 0)
            + QString("Timestamp:\t%1\t\tLength:\t%2\n")
                  .arg(timestamp.toString("yyyy-MM-dd hh:mm:ss"))
                  .arg(length)
            + "===============================================================================\n";

        // Output the formatted packet information
        outputText->append(packetInfo);
    }
}

void MainWindow::saveToFile()
{
    if(!isCapturing)
    {
        outputText->append("Capture is not active");
        return;
    }

    QString filePath = QFileDialog::getSaveFileName(this, "Save Captured Packets", ".", "Packet Files (*.pcap)");
    if(!filePath.isEmpty())
    {
        outputFile = fopen(filePath.toStdString().c_str(), "wb");
        if(outputFile)
        {
            outputText->append("Saving captured packets to file...");
        }
        else
        {
            outputText->append("Error opening the output file");
        }
    }
}

void MainWindow::packetHandlerCallback(u_char *userData, const struct pcap_pkthdr *header, const u_char *packetData)
{
    qInfo()<<("Test case 6 passed");

    MainWindow *appInstance = reinterpret_cast<MainWindow *>(userData);
    appInstance->packetHandler(header, packetData);
}

void MainWindow::selectInterface(int index)
{

}
