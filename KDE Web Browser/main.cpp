#include <QApplication>
#include <QMainWindow>
#include <QLineEdit>
#include <QVBoxLayout>
#include <QPushButton>
#include <QHBoxLayout>
#include <QTabWidget>
#include <QWebEngineView>
#include <QWebEngineProfile>
#include <QWebEngineSettings>
#include <QWebEngineUrlRequestInterceptor>
#include <QDialog>
#include <QCheckBox>
#include <QFormLayout>
#include <QLabel>
#include <QDir>
#include <QUdpSocket>
#include <QTextEdit>
#include <QInputDialog>
#include <QMessageBox>
#include <QSettings>

// Port für den lokalen KWeb Messenger
const quint16 CHAT_PORT = 45454;

// --- ADBLOCKER CORE ---
class KWebAdBlocker : public QWebEngineUrlRequestInterceptor {
public:
    KWebAdBlocker(bool &adblockEnabled) : m_enabled(adblockEnabled) {}
    void interceptRequest(QWebEngineUrlRequestInfo &info) override {
        if (!m_enabled) return;
        QString url = info.requestUrl().toString().toLower();
        if (url.contains("ads.") || url.contains("/ads/") ||
            url.contains("analytics.") || url.contains("telemetry") ||
            url.contains("doubleclick.net") || url.contains("adservice") ||
            url.contains("google-analytics") || url.contains("adsystem")) {
            info.block(true);
        }
    }
private:
    bool &m_enabled;
};

// --- LOKALER MESSENGER WIDGET ---
class KWebMessenger : public QWidget {
    // Q_OBJECT hier entfernt, um den MOC-Fehler bei Standalone-Dateien zu umgehen!
public:
    KWebMessenger(const QString &username, QWidget *parent = nullptr) : QWidget(parent), m_username(username) {
        QVBoxLayout *layout = new QVBoxLayout(this);
        
        chatDisplay = new QTextEdit(this);
        chatDisplay->setReadOnly(true);
        chatDisplay->setStyleSheet("background-color: #171a1f; color: #eff0f1; border: 1px solid #76797c; border-radius: 4px;");
        
        QHBoxLayout *inputLayout = new QHBoxLayout();
        messageInput = new QLineEdit(this);
        messageInput->setPlaceholderText("Nachricht schreiben...");
        QPushButton *sendBtn = new QPushButton("Senden", this);
        
        inputLayout->addWidget(messageInput);
        inputLayout->addWidget(sendBtn);
        
        layout->addWidget(new QLabel("<b>KWeb Privater Local Messenger (RAM-Only)</b>"));
        layout->addWidget(chatDisplay);
        layout->addLayout(inputLayout);
        
        udpSocket = new QUdpSocket(this);
        udpSocket->bind(CHAT_PORT, QUdpSocket::ShareAddress);
        
        // Da wir kein Q_OBJECT nutzen, binden wir die Funktionen direkt via C++ Lambda oder Pointer ein
        connect(sendBtn, &QPushButton::clicked, this, &KWebMessenger::sendMessage);
        connect(messageInput, &QLineEdit::returnPressed, this, &KWebMessenger::sendMessage);
        connect(udpSocket, &QUdpSocket::readyRead, this, &KWebMessenger::processPendingDatagrams);

        chatDisplay->append("<i>System: Als " + m_username + " dem Chat beigetreten.</i>");
    }

    void sendMessage() {
        QString text = messageInput->text().trimmed();
        if (text.isEmpty()) return;
        
        QString fullMsg = m_username + ": " + text;
        QByteArray datagram = fullMsg.toUtf8();
        
        udpSocket->writeDatagram(datagram, QHostAddress::Broadcast, CHAT_PORT);
        messageInput->clear();
    }

    void processPendingDatagrams() {
        while (udpSocket->hasPendingDatagrams()) {
            QByteArray datagram;
            datagram.resize(udpSocket->pendingDatagramSize());
            udpSocket->readDatagram(datagram.data(), datagram.size());
            chatDisplay->append(QString::fromUtf8(datagram));
        }
    }

private:
    QString m_username;
    QUdpSocket *udpSocket;
    QTextEdit *chatDisplay;
    QLineEdit *messageInput;
};

// --- DAS HAUPTFENSTER ---
class KWebWindow : public QMainWindow {
    Q_OBJECT
public:
    KWebWindow() {
        setWindowTitle("KWeb Browser");
        resize(1280, 720);

        styleStr =
        "QMainWindow { background-color: #232629; color: #eff0f1; }"
        "QWidget { background-color: #232629; color: #eff0f1; font-family: 'Noto Sans', sans-serif; }"
        "QLineEdit { background-color: #31363b; color: #eff0f1; border: 1px solid #76797c; padding: 6px; border-radius: 4px; }"
        "QPushButton { background-color: #31363b; color: #eff0f1; border: 1px solid #76797c; padding: 6px 12px; border-radius: 4px; }"
        "QPushButton:hover { background-color: #4d545a; border: 1px solid #3daee9; }"
        "QTabWidget::panel { border: 1px solid #76797c; background-color: #232629; }"
        "QTabBar::tab { background-color: #31363b; color: #eff0f1; border: 1px solid #76797c; padding: 8px 16px; border-top-left-radius: 4px; border-top-right-radius: 4px; }"
        "QTabBar::tab:selected { background-color: #232629; border-bottom: 1px solid #232629; font-weight: bold; color: #3daee9; }";

        this->setStyleSheet(styleStr);

        ncbd_enabled = true;
        ntbd_enabled = true;
        adblock_enabled = true;
        force_dark_enabled = true;

        startPage = "file://" + QDir::cleanPath(QCoreApplication::applicationDirPath() + "/../web/index.html");
        applyPrivacySettings();
        checkUsernameSession();

        QWidget *centralWidget = new QWidget(this);
        QVBoxLayout *mainLayout = new QVBoxLayout(centralWidget);

        QHBoxLayout *controlsLayout = new QHBoxLayout();
        QPushButton *backButton = new QPushButton("<", this);
        QPushButton *forwardButton = new QPushButton(">", this);
        QPushButton *reloadButton = new QPushButton("⟳", this);
        addressBar = new QLineEdit(this);
        QPushButton *msgButton = new QPushButton("💬 Chat", this);
        QPushButton *newTabButton = new QPushButton("+ Tab", this);
        QPushButton *settingsButton = new QPushButton("⚙", this);

        controlsLayout->addWidget(backButton);
        controlsLayout->addWidget(forwardButton);
        controlsLayout->addWidget(reloadButton);
        controlsLayout->addWidget(addressBar);
        controlsLayout->addWidget(msgButton);
        controlsLayout->addWidget(newTabButton);
        controlsLayout->addWidget(settingsButton);

        mainLayout->addLayout(controlsLayout);

        tabWidget = new QTabWidget(this);
        tabWidget->setTabsClosable(true);
        mainLayout->addWidget(tabWidget);

        setCentralWidget(centralWidget);

        connect(newTabButton, &QPushButton::clicked, this, [this]() { createNewTab(QUrl(startPage)); });
        connect(msgButton, &QPushButton::clicked, this, &KWebWindow::openMessengerTab);
        connect(tabWidget, &QTabWidget::tabCloseRequested, this, &KWebWindow::closeTab);
        connect(addressBar, &QLineEdit::returnPressed, this, &KWebWindow::handleUrlInput);
        connect(backButton, &QPushButton::clicked, this, [this]() { if (currentBrowser()) currentBrowser()->back(); });
        connect(forwardButton, &QPushButton::clicked, this, [this]() { if (currentBrowser()) currentBrowser()->forward(); });
        connect(reloadButton, &QPushButton::clicked, this, [this]() { if (currentBrowser()) currentBrowser()->reload(); });
        connect(settingsButton, &QPushButton::clicked, this, &KWebWindow::openSettingsDialog);
        connect(tabWidget, &QTabWidget::currentChanged, this, [this](int index) {
            if (index >= 0 && currentBrowser()) addressBar->setText(currentBrowser()->url().toString());
        });

        createNewTab(QUrl(startPage));
    }

private:
    QTabWidget *tabWidget;
    QLineEdit *addressBar;
    QString styleStr;
    QString startPage;
    QString currentUsername;
    bool ncbd_enabled, ntbd_enabled, adblock_enabled, force_dark_enabled;

    QWebEngineView* currentBrowser() { return qobject_cast<QWebEngineView*>(tabWidget->currentWidget()); }

    void checkUsernameSession() {
        QSettings sessionFile("/tmp/kweb_session.conf", QSettings::IniFormat);
        QString lastUser = sessionFile.value("session/lastUser", "Techx32_test").toString();

        QMessageBox::StandardButton reply;
        reply = QMessageBox::question(this, "KWeb Session", 
                                      QString("War dein Username in der letzten Sitzung %1?").arg(lastUser),
                                      QMessageBox::Yes | QMessageBox::No);
        
        if (reply == QMessageBox::Yes) {
            currentUsername = lastUser;
        } else {
            bool ok;
            QString text = QInputDialog::getText(this, "KWeb Messenger",
                                                 "Neuen Usernamen eingeben:", QLineEdit::Normal,
                                                 "KWebUser", &ok);
            currentUsername = (ok && !text.trimmed().isEmpty()) ? text.trimmed() : "Anonym";
            sessionFile.setValue("session/lastUser", currentUsername);
        }
    }

    void openMessengerTab() {
        KWebMessenger *messenger = new KWebMessenger(currentUsername, this);
        int index = tabWidget->addTab(messenger, "💬 KWeb Chat");
        tabWidget->setCurrentIndex(index);
    }

    void applyPrivacySettings() {
        QWebEngineProfile *profile = QWebEngineProfile::defaultProfile();
        profile->setPersistentCookiesPolicy(ncbd_enabled ? QWebEngineProfile::NoPersistentCookies : QWebEngineProfile::AllowPersistentCookies);
        if (ntbd_enabled && !profile->httpUserAgent().contains("DNT=1")) {
            profile->setHttpUserAgent(profile->httpUserAgent() + " (DNT: 1)");
        }
        static KWebAdBlocker *interceptor = new KWebAdBlocker(adblock_enabled);
        profile->setUrlRequestInterceptor(interceptor);
        profile->settings()->setAttribute(QWebEngineSettings::ForceDarkMode, force_dark_enabled);
    }

    void createNewTab(const QUrl &url) {
        QWebEngineView *browser = new QWebEngineView(this);
        browser->load(url);
        int index = tabWidget->addTab(browser, "Lädt...");
        tabWidget->setCurrentIndex(index);

        connect(browser, &QWebEngineView::loadFinished, this, [this, browser](bool ok) {
            int idx = tabWidget->indexOf(browser);
            if (idx != -1 && ok) {
                QString pageTitle = browser->title().trimmed();
                tabWidget->setTabText(idx, pageTitle.isEmpty() ? "KWeb" : pageTitle);
            }
        });

        connect(browser, &QWebEngineView::titleChanged, this, [this, browser](const QString &title) {
            int idx = tabWidget->indexOf(browser);
            if (idx != -1 && !title.isEmpty()) tabWidget->setTabText(idx, title);
        });

        connect(browser, &QWebEngineView::urlChanged, this, [this, browser](const QUrl &newUrl) {
            if (tabWidget->currentWidget() == browser) addressBar->setText(newUrl.toString());
        });
    }

    void closeTab(int index) {
        if (tabWidget->count() > 1) {
            QWidget *widget = tabWidget->widget(index);
            tabWidget->removeTab(index);
            delete widget;
        }
    }

    void handleUrlInput() {
        if (!currentBrowser()) return;
        QString input = addressBar->text().trimmed();
        if (input.contains(".") && !input.contains(" ")) {
            if (!input.startsWith("http") && !input.startsWith("file")) input = "https://" + input;
            currentBrowser()->load(QUrl(input));
        } else {
            currentBrowser()->load(QUrl("https://www.google.com/search?q=" + QUrl::toPercentEncoding(input)));
        }
    }

    void openSettingsDialog() {
        QDialog dialog(this);
        dialog.setWindowTitle("KWeb Einstellungen");
        dialog.resize(500, 400);
        dialog.setStyleSheet(styleStr);

        QVBoxLayout *dialogLayout = new QVBoxLayout(&dialog);
        QTabWidget *settingsTabs = new QTabWidget(&dialog);

        QWidget *genWidget = new QWidget();
        QFormLayout *genLayout = new QFormLayout(genWidget);
        QLineEdit *homeInput = new QLineEdit(startPage);
        genLayout->addRow("Startseite:", homeInput);
        genWidget->setLayout(genLayout);

        QWidget *noFlagsWidget = new QWidget();
        QVBoxLayout *nfVBox = new QVBoxLayout(noFlagsWidget);
        QCheckBox *ncbdCB = new QCheckBox("NCBD (No Cookies By Default)");
        ncbdCB->setChecked(ncbd_enabled);
        QCheckBox *ntbdCB = new QCheckBox("NTBD (No Tracking By Default)");
        ntbdCB->setChecked(ntbd_enabled);
        QCheckBox *adblockCB = new QCheckBox("Integrierter AdBlocker aktiv");
        adblockCB->setChecked(adblock_enabled);
        QCheckBox *darkModeCB = new QCheckBox("Dark Mode für alle Webseiten erzwingen");
        darkModeCB->setChecked(force_dark_enabled);

        nfVBox->addWidget(ncbdCB);
        nfVBox->addWidget(ntbdCB);
        nfVBox->addWidget(adblockCB);
        nfVBox->addWidget(darkModeCB);
        nfVBox->addStretch();

        settingsTabs->addTab(genWidget, "Allgemein");
        settingsTabs->addTab(noFlagsWidget, "No-Flags");

        dialogLayout->addWidget(settingsTabs);
        QPushButton *saveBtn = new QPushButton("Speichern");
        dialogLayout->addWidget(saveBtn);

        connect(saveBtn, &QPushButton::clicked, &dialog, [&]() {
            ncbd_enabled = ncbdCB->isChecked();
            ntbd_enabled = ntbdCB->isChecked();
            adblock_enabled = adblockCB->isChecked();
            force_dark_enabled = darkModeCB->isChecked();
            startPage = homeInput->text();
            applyPrivacySettings();
            dialog.accept();
        });
        dialog.exec();
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    KWebWindow window;
    window.show();
    return app.exec();
}

#include "main.moc"
