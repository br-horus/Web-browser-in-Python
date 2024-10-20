
import sys  # HORUS AND MOSTAFA OSMAN
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QToolBar,  # HORUS AND MOSTAFA OSMAN
                             QTabWidget, QAction, QMessageBox, QVBoxLayout,  # HORUS AND MOSTAFA OSMAN
                             QWidget, QLabel, QComboBox, QPushButton)  # HORUS AND MOSTAFA OSMAN
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile  # HORUS AND MOSTAFA OSMAN
from PyQt5.QtCore import QUrl, Qt  # HORUS AND MOSTAFA OSMAN
from PyQt5.QtGui import QIcon  # HORUS AND MOSTAFA OSMAN
import requests  # HORUS AND MOSTAFA OSMAN

class Browser(QMainWindow):  # HORUS AND MOSTAFA OSMAN
    def __init__(self):  # HORUS AND MOSTAFA OSMAN
        super().__init__()  # HORUS AND MOSTAFA OSMAN
        self.setWindowTitle("Web-browser")  # HORUS AND MOSTAFA OSMAN
        self.setGeometry(100, 100, 1200, 800)  # HORUS AND MOSTAFA OSMAN

        # إنشاء علامات التبويب  # HORUS AND MOSTAFA OSMAN
        self.tabs = QTabWidget()  # HORUS AND MOSTAFA OSMAN
        self.tabs.setTabsClosable(True)  # HORUS AND MOSTAFA OSMAN
        self.tabs.tabCloseRequested.connect(self.close_current_tab)  # HORUS AND MOSTAFA OSMAN
        self.setCentralWidget(self.tabs)  # HORUS AND MOSTAFA OSMAN

        # إضافة شريط الأدوات  # HORUS AND MOSTAFA OSMAN
        toolbar = QToolBar()  # HORUS AND MOSTAFA OSMAN
        self.addToolBar(toolbar)  # HORUS AND MOSTAFA OSMAN

        # حقل إدخال URL  # HORUS AND MOSTAFA OSMAN
        self.url_bar = QLineEdit()  # HORUS AND MOSTAFA OSMAN
        self.url_bar.returnPressed.connect(self.navigate_to_url)  # HORUS AND MOSTAFA OSMAN
        toolbar.addWidget(self.url_bar)  # HORUS AND MOSTAFA OSMAN

        # أزرار التحكم  # HORUS AND MOSTAFA OSMAN
        self.add_toolbar_buttons(toolbar)  # HORUS AND MOSTAFA OSMAN

        # إضافة علامة تبويب جديدة عند بدء التشغيل  # HORUS AND MOSTAFA OSMAN
        self.add_new_tab()  # HORUS AND MOSTAFA OSMAN

        # تحسين التصميم  # HORUS AND MOSTAFA OSMAN
        self.setStyleSheet(self.get_stylesheet())  # HORUS AND MOSTAFA OSMAN

        self.bookmarks = {}  # HORUS AND MOSTAFA OSMAN
        self.history = []  # HORUS AND MOSTAFA OSMAN
        self.user_agents = self.load_user_agents()  # HORUS AND MOSTAFA OSMAN

    def load_user_agents(self):  # HORUS AND MOSTAFA OSMAN
        return [  # HORUS AND MOSTAFA OSMAN
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",  # HORUS AND MOSTAFA OSMAN
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",  # HORUS AND MOSTAFA OSMAN
            "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36",  # HORUS AND MOSTAFA OSMAN
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",  # HORUS AND MOSTAFA OSMAN
        ]  # HORUS AND MOSTAFA OSMAN

    def add_toolbar_buttons(self, toolbar):  # HORUS AND MOSTAFA OSMAN
        new_tab_action = QAction("علامة تبويب جديدة", self)  # HORUS AND MOSTAFA OSMAN
        new_tab_action.triggered.connect(self.add_new_tab)  # HORUS AND MOSTAFA OSMAN
        toolbar.addAction(new_tab_action)  # HORUS AND MOSTAFA OSMAN

        reload_action = QAction("إعادة تحميل", self)  # HORUS AND MOSTAFA OSMAN
        reload_action.triggered.connect(self.reload_page)  # HORUS AND MOSTAFA OSMAN
        toolbar.addAction(reload_action)  # HORUS AND MOSTAFA OSMAN

        forward_action = QAction("التقدم إلى الأمام", self)  # HORUS AND MOSTAFA OSMAN
        forward_action.triggered.connect(self.forward_page)  # HORUS AND MOSTAFA OSMAN
        toolbar.addAction(forward_action)  # HORUS AND MOSTAFA OSMAN

        back_action = QAction("التراجع", self)  # HORUS AND MOSTAFA OSMAN
        back_action.triggered.connect(self.back_page)  # HORUS AND MOSTAFA OSMAN
        toolbar.addAction(back_action)  # HORUS AND MOSTAFA OSMAN

        bookmark_action = QAction("إدارة الإشارات المرجعية", self)  # HORUS AND MOSTAFA OSMAN
        bookmark_action.triggered.connect(self.manage_bookmarks)  # HORUS AND MOSTAFA OSMAN
        toolbar.addAction(bookmark_action)  # HORUS AND MOSTAFA OSMAN

        history_action = QAction("تاريخ التصفح", self)  # HORUS AND MOSTAFA OSMAN
        history_action.triggered.connect(self.show_history)  # HORUS AND MOSTAFA OSMAN
        toolbar.addAction(history_action)  # HORUS AND MOSTAFA OSMAN

        settings_action = QAction("إعدادات", self)  # HORUS AND MOSTAFA OSMAN
        settings_action.triggered.connect(self.open_settings)  # HORUS AND MOSTAFA OSMAN
        toolbar.addAction(settings_action)  # HORUS AND MOSTAFA OSMAN

        private_mode_action = QAction("وضع التصفح الخاص", self)  # HORUS AND MOSTAFA OSMAN
        private_mode_action.triggered.connect(self.toggle_private_mode)  # HORUS AND MOSTAFA OSMAN
        toolbar.addAction(private_mode_action)  # HORUS AND MOSTAFA OSMAN

        dev_tools_action = QAction("أدوات المطور", self)  # HORUS AND MOSTAFA OSMAN
        dev_tools_action.triggered.connect(self.open_dev_tools)  # HORUS AND MOSTAFA OSMAN
        toolbar.addAction(dev_tools_action)  # HORUS AND MOSTAFA OSMAN

    def add_new_tab(self):  # HORUS AND MOSTAFA OSMAN
        new_browser = QWebEngineView()  # HORUS AND MOSTAFA OSMAN
        new_browser.setUrl(QUrl("http://www.google.com"))  # HORUS AND MOSTAFA OSMAN
        new_browser.urlChanged.connect(self.update_url_bar)  # HORUS AND MOSTAFA OSMAN
        new_browser.loadFinished.connect(self.update_title)  # HORUS AND MOSTAFA OSMAN
        self.tabs.addTab(new_browser, "علامة تبويب جديدة")  # HORUS AND MOSTAFA OSMAN
        self.tabs.setCurrentWidget(new_browser)  # HORUS AND MOSTAFA OSMAN

    def close_current_tab(self, index):  # HORUS AND MOSTAFA OSMAN
        if self.tabs.count() > 1:  # HORUS AND MOSTAFA OSMAN
            self.tabs.removeTab(index)  # HORUS AND MOSTAFA OSMAN

    def navigate_to_url(self):  # HORUS AND MOSTAFA OSMAN
        url = self.url_bar.text()  # HORUS AND MOSTAFA OSMAN
        if not url.startswith("http"):  # HORUS AND MOSTAFA OSMAN
            url = "http://" + url  # HORUS AND MOSTAFA OSMAN
        self.tabs.currentWidget().setUrl(QUrl(url))  # HORUS AND MOSTAFA OSMAN
        self.history.append(url)  # HORUS AND MOSTAFA OSMAN
        self.update_history()  # HORUS AND MOSTAFA OSMAN

    def update_url_bar(self, q):  # HORUS AND MOSTAFA OSMAN
        self.url_bar.setText(q.toString())  # HORUS AND MOSTAFA OSMAN

    def update_title(self, success):  # HORUS AND MOSTAFA OSMAN
        current_tab = self.tabs.currentWidget()  # HORUS AND MOSTAFA OSMAN
        if success:  # HORUS AND MOSTAFA OSMAN
            title = current_tab.title()  # HORUS AND MOSTAFA OSMAN
            self.setWindowTitle(f"{title} - Web-browser")  # HORUS AND MOSTAFA OSMAN
        else:  # HORUS AND MOSTAFA OSMAN
            self.setWindowTitle("Web-browser - خطأ في تحميل الصفحة")  # HORUS AND MOSTAFA OSMAN

    def manage_bookmarks(self):  # HORUS AND MOSTAFA OSMAN
        bookmarks_window = QWidget()  # HORUS AND MOSTAFA OSMAN
        bookmarks_window.setWindowTitle("إدارة الإشارات المرجعية")  # HORUS AND MOSTAFA OSMAN
        layout = QVBoxLayout()  # HORUS AND MOSTAFA OSMAN

        for folder, urls in self.bookmarks.items():  # HORUS AND MOSTAFA OSMAN
            layout.addWidget(QLabel(f"مجلد: {folder}"))  # HORUS AND MOSTAFA OSMAN
            for url in urls:  # HORUS AND MOSTAFA OSMAN
                layout.addWidget(QLabel(url))  # HORUS AND MOSTAFA OSMAN

        bookmarks_window.setLayout(layout)  # HORUS AND MOSTAFA OSMAN
        bookmarks_window.resize(400, 300)  # HORUS AND MOSTAFA OSMAN
        bookmarks_window.show()  # HORUS AND MOSTAFA OSMAN

    def show_history(self):  # HORUS AND MOSTAFA OSMAN
        history_string = "\n".join(self.history)  # HORUS AND MOSTAFA OSMAN
        if history_string:  # HORUS AND MOSTAFA OSMAN
            QMessageBox.information(self, "تاريخ التصفح", history_string)  # HORUS AND MOSTAFA OSMAN
        else:  # HORUS AND MOSTAFA OSMAN
            QMessageBox.information(self, "تاريخ التصفح", "لا يوجد تاريخ متاح.")  # HORUS AND MOSTAFA OSMAN

    def open_settings(self):  # HORUS AND MOSTAFA OSMAN
        settings_window = QWidget()  # HORUS AND MOSTAFA OSMAN
        settings_window.setWindowTitle("إعدادات المتصفح")  # HORUS AND MOSTAFA OSMAN
        layout = QVBoxLayout()  # HORUS AND MOSTAFA OSMAN

        # قائمة لاختيار بصمة المستخدم  # HORUS AND MOSTAFA OSMAN
        self.user_agent_combo = QComboBox()  # HORUS AND MOSTAFA OSMAN
        self.user_agent_combo.addItems(self.user_agents)  # HORUS AND MOSTAFA OSMAN
        layout.addWidget(QLabel("اختر بصمة المستخدم:"))  # HORUS AND MOSTAFA OSMAN
        layout.addWidget(self.user_agent_combo)  # HORUS AND MOSTAFA OSMAN

        # زر تطبيق البصمة  # HORUS AND MOSTAFA OSMAN
        apply_button = QPushButton("تطبيق البصمة")  # HORUS AND MOSTAFA OSMAN
        apply_button.clicked.connect(self.apply_user_agent)  # HORUS AND MOSTAFA OSMAN
        layout.addWidget(apply_button)  # HORUS AND MOSTAFA OSMAN

        # زر معلومات عن المطور  # HORUS AND MOSTAFA OSMAN
        info_button = QPushButton("معلومات عن المطور")  # HORUS AND MOSTAFA OSMAN
        info_button.clicked.connect(self.show_developer_info)  # HORUS AND MOSTAFA OSMAN
        layout.addWidget(info_button)  # HORUS AND MOSTAFA OSMAN

        settings_window.setLayout(layout)  # HORUS AND MOSTAFA OSMAN
        settings_window.resize(300, 200)  # HORUS AND MOSTAFA OSMAN
        settings_window.show()  # HORUS AND MOSTAFA OSMAN

    def apply_user_agent(self):  # HORUS AND MOSTAFA OSMAN
        selected_user_agent = self.user_agent_combo.currentText()  # HORUS AND MOSTAFA OSMAN
        profile = QWebEngineProfile.defaultProfile()  # HORUS AND MOSTAFA OSMAN
        profile.setHttpUserAgent(selected_user_agent)  # HORUS AND MOSTAFA OSMAN
        QMessageBox.information(self, "بصمة المستخدم", f"تم تغيير بصمة المستخدم إلى:\n{selected_user_agent}")  # HORUS AND MOSTAFA OSMAN

    def toggle_private_mode(self):  # HORUS AND MOSTAFA OSMAN
        current_browser = self.tabs.currentWidget()  # HORUS AND MOSTAFA OSMAN
        if current_browser.isPrivateBrowsing():  # HORUS AND MOSTAFA OSMAN
            current_browser.setPrivateBrowsing(False)  # HORUS AND MOSTAFA OSMAN
            QMessageBox.information(self, "وضع التصفح الخاص", "تم إيقاف وضع التصفح الخاص.")  # HORUS AND MOSTAFA OSMAN
        else:  # HORUS AND MOSTAFA OSMAN
            current_browser.setPrivateBrowsing(True)  # HORUS AND MOSTAFA OSMAN
            QMessageBox.information(self, "وضع التصفح الخاص", "تم تفعيل وضع التصفح الخاص.")  # HORUS AND MOSTAFA OSMAN

    def open_dev_tools(self):  # HORUS AND MOSTAFA OSMAN
        current_browser = self.tabs.currentWidget()  # HORUS AND MOSTAFA OSMAN
        current_browser.page().runJavaScript('window.open("about:blank", "_blank")')  # HORUS AND MOSTAFA OSMAN

    def reload_page(self):  # HORUS AND MOSTAFA OSMAN
        self.tabs.currentWidget().reload()  # HORUS AND MOSTAFA OSMAN

    def forward_page(self):  # HORUS AND MOSTAFA OSMAN
        self.tabs.currentWidget().forward()  # HORUS AND MOSTAFA OSMAN

    def back_page(self):  # HORUS AND MOSTAFA OSMAN
        self.tabs.currentWidget().back()  # HORUS AND MOSTAFA OSMAN

    def update_history(self):  # HORUS AND MOSTAFA OSMAN
        pass  # HORUS AND MOSTAFA OSMAN

    def show_developer_info(self):  # HORUS AND MOSTAFA OSMAN
        info = """### 👋 مرحبًا! أنا @br-horus

- 👨‍💻 **مبرمج ومطور برامج ومواقع**: لدي خبرة واسعة في تطوير البرامج، مواقع الويب، وتطبيقات الديسكتوب باستخدام HTML, CSS, JavaScript, Python، بالإضافة إلى قواعد البيانات SQL ولغات أخرى مثل PHP وNode.js. أيضًا لدي خبرة في العمل باستخدام أطر العمل مثل Django وReact.
- 🌐 **مهندس شبكات واتصالات**: خبير في تصميم وإنشاء الشبكات والخوادم، بما في ذلك إعداد أنظمة التشغيل الخاصة بالخوادم مثل Linux وWindows Server، وتكوين جدران الحماية (Firewalls) وحلول الـ VPN.
- 🔒 **هاكر أخلاقي وبين تيستر**: لدي خبرة في اكتشاف الثغرات الأمنية واستخدام جميع أدوات Kali Linux مثل Metasploit وWireshark، وتطبيق الاختبارات الأمنية على تطبيقات الويب والشبكات لضمان الأمان.
- 🛠️ **DevOps ومهندس سحابي**: لدي خبرة في استخدام أدوات DevOps مثل Docker وKubernetes، وإدارة البنية التحتية السحابية باستخدام AWS وAzure.
- 🎨 **مصمم ومبرمج**: قادر على تصميم المواقع والتطبيقات بواجهات مستخدم مميزة باستخدام أدوات مثل Figma وAdobe XD، وكذلك تطوير الشبكات والخوادم بشكل كامل من الألف إلى الياء.
- 📈 **محلل بيانات**: لدي خبرة في استخدام Python وSQL لتحليل البيانات وإنشاء التقارير الداعمة لاتخاذ القرارات.
- 🤖 **مهتم بالذكاء الاصطناعي والتعلم الآلي**: أعمل على مشاريع تعتمد على تعلم الآلة وتحليل البيانات باستخدام مكتبات مثل TensorFlow وscikit-learn.

### 👋 Hi! I’m @br-horus

- 👨‍💻 **Programmer & Web Developer**: Extensive experience in developingإليك بقية الكود لمتصفح محسّن مع شاشة معلومات عن المطور:

```python
- 🎨 **مصمم ومبرمج**: قادر على تصميم المواقع والتطبيقات بواجهات مستخدم مميزة باستخدام أدوات مثل Figma وAdobe XD، وكذلك تطوير الشبكات والخوادم بشكل كامل من الألف إلى الياء.
- 📈 **محلل بيانات**: لدي خبرة في استخدام Python وSQL لتحليل البيانات وإنشاء التقارير الداعمة لاتخاذ القرارات.
- 🤖 **مهتم بالذكاء الاصطناعي والتعلم الآلي**: أعمل على مشاريع تعتمد على تعلم الآلة وتحليل البيانات باستخدام مكتبات مثل TensorFlow وscikit-learn.

### 👋 Hi! I’m @br-horus

- 👨‍💻 **Programmer & Web Developer**: Extensive experience in developing software, websites, and desktop applications using HTML, CSS, JavaScript, Python, along with SQL databases and other languages such as PHP and Node.js. Also experienced in frameworks like Django and React.
- 🌐 **Network and Communications Engineer**: Expert in designing and setting up networks and servers, including configuring server operating systems like Linux and Windows Server, firewalls, and VPN solutions.
- 🔒 **Ethical Hacker & Pen Tester**: Skilled in vulnerability discovery and utilizing all Kali Linux tools like Metasploit and Wireshark, performing security assessments on web applications and networks to ensure safety.
- 🛠️ **DevOps & Cloud Engineer**: Experienced in using DevOps tools like Docker and Kubernetes, managing cloud infrastructure using AWS and Azure.
- 🎨 **Designer & Coder**: Capable of designing websites and applications with outstanding user interfaces using tools like Figma and Adobe XD, as well as fully developing networks and servers.
- 📈 **Data Analyst**: Skilled in using Python and SQL for data analysis and creating insightful reports to support decision-making.
- 🤖 **AI & Machine Learning Enthusiast**: Working on projects involving machine learning and data analysis using libraries like TensorFlow and scikit-learn.

### 👋 Bonjour! Je suis @br-horus

- 👨‍💻 **Programmeur et Développeur Web** : Expérience étendue dans le développement de logiciels, de sites web et d'applications de bureau utilisant HTML, CSS, JavaScript, Python, ainsi que des bases de données SQL et d'autres langages tels que PHP et Node.js. Expérience également avec des frameworks comme Django et React.
- 🌐 **Ingénieur Réseaux et Communications** : Expert en conception et mise en place de réseaux et serveurs, incluant la configuration des systèmes d'exploitation serveurs tels que Linux et Windows Server, des pare-feux et des solutions VPN.
- 🔒 **Hacker éthique et Testeur de Sécurité** : Compétent dans la découverte de vulnérabilités et l'utilisation des outils Kali Linux comme Metasploit et Wireshark, effectuant des évaluations de sécurité sur des applications web et des réseaux pour garantir la sécurité.
- 🛠️ **DevOps et Ingénieur Cloud** : Expérimenté dans l'utilisation d'outils DevOps tels que Docker et Kubernetes, et dans la gestion de l'infrastructure cloud avec AWS et Azure.
- 🎨 **Concepteur et Programmeur** : Capable de concevoir des sites web et des applications avec des interfaces utilisateur exceptionnelles en utilisant des outils tels que Figma et Adobe XD, ainsi que de développer complètement des réseaux et des serveurs.
- 📈 **Analyste de Données** : Compétent dans l'utilisation de Python et SQL pour l'analyse des données et la création de rapports perspicaces pour soutenir la prise de décision.
- 🤖 **Passionné par l'IA et l'apprentissage automatique** : Travaillant sur des projets impliquant l'apprentissage automatique et l'analyse des données en utilisant des bibliothèques comme TensorFlow et scikit-learn.

### 👋 Привет! Я @br-horus

- 👨‍💻 **Программист и веб-разработчик**: Обширный опыт разработки программного обеспечения, веб-сайтов и десктопных приложений на HTML, CSS, JavaScript, Python, а также с базами данных SQL и другими языками, такими как PHP и Node.js. Также опыт работы с фреймворками Django и React.
- 🌐 **Инженер сетей и коммуникаций**: Эксперт в проектировании и настройке сетей и серверов, включая настройку операционных систем серверов, таких как Linux и Windows Server, брандмауэров и решений VPN.
- 🔒 **Этичный хакер и пентестер**: Опыт в обнаружении уязвимостей и использовании всех инструментов Kali Linux, таких как Metasploit и Wireshark, проведение оценок безопасности веб-приложений и сетей для обеспечения безопасности.
- 🛠️ **DevOps и облачный инженер**: Опыт использования инструментов DevOps, таких как Docker и Kubernetes, управление облачной инфраструктурой с помощью AWS и Azure.
- 🎨 **Дизайнер и программист**: Умею разрабатывать веб-сайты и приложения с отличным пользовательским интерфейсом, используя такие инструменты, как Figma и Adobe XD, а также полностью разрабатывать сети и серверы.
- 📈 **Аналитик данных**: Опыт использования Python и SQL для анализа данных и создания отчетов, поддерживающих принятие решений.
- 🤖 **Увлекаюсь искусственным интеллектом и машинным обучением**: Работаю над проектами, связанными с машинным обучением и анализом данных, используя библиотеки TensorFlow и scikit-learn.

### 👋 Hallo! Ich bin @br-horus

- 👨‍💻 **Programmierer & Webentwickler**: Umfangreiche Erfahrung in der Entwicklung von Software, Websites und Desktop-Anwendungen mit HTML, CSS, JavaScript, Python sowie SQL-Datenbanken und anderen Sprachen wie PHP und Node.js. Auch erfahren in Frameworks wie Django und React.
- 🌐 **Netzwerk- und Kommunikationstechniker**: Experte für die Gestaltung und Einrichtung von Netzwerken und Servern, einschließlich der Konfiguration von Serverbetriebssystemen wie Linux und Windows Server, Firewalls und VPN-Lösungen.
- 🔒 **Ethical Hacker & Pen Tester**: Erfahren in der Entdeckung von Schwachstellen und der Nutzung aller Kali Linux Tools wie Metasploit und Wireshark, Durchführung von Sicherheitsbewertungen für Webanwendungen und Netzwerke zur Gewährleistung der Sicherheit.
- 🛠️ **DevOps & Cloud Engineer**: Erfahrung im Einsatz von DevOps-Tools wie Docker und Kubernetes sowie im Management von Cloud-Infrastrukturen mit AWS und Azure.
- 🎨 **Designer & Programmierer**: Fähig, Websites und Anwendungen mit herausragenden Benutzeroberflächen zu gestalten, unter Verwendung von Tools wie Figma und Adobe XD, sowie Netzwerke und Server vollständig zu entwickeln.
- 📈 **Datenanalyst**: Erfahrung in der Verwendung von Python und SQL zur Datenanalyse und Erstellung aufschlussreicher Berichte zur Unterstützung von Entscheidungsprozessen.
- 🤖 **KI- und Machine-Learning-Enthusiast**: Arbeitet an Projekten, die maschinelles Lernen und Datenanalyse unter Verwendung von Bibliotheken wie TensorFlow und scikit-learn umfassen.
        """
        QMessageBox.information(self, "معلومات عن المطور", info)  # HORUS AND MOSTAFA OSMAN

    def get_stylesheet(self):  # HORUS AND MOSTAFA OSMAN
        return """  # HORUS AND MOSTAFA OSMAN
            QMainWindow {  # HORUS AND MOSTAFA OSMAN
                background-color: #1e1e1e;  # HORUS AND MOSTAFA OSMAN
                color: #ffffff;  # HORUS AND MOSTAFA OSMAN
            }  # HORUS AND MOSTAFA OSMAN
            QLineEdit {  # HORUS AND MOSTAFA OSMAN
                background-color: #2e2e2e;  # HORUS AND MOSTAFA OSMAN
                color: #ffffff;  # HORUS AND MOSTAFA OSMAN
            }  # HORUS AND MOSTAFA OSMAN
            QToolBar {  # HORUS AND MOSTAFA OSMAN
                background-color: #3e3e3e;  # HORUS AND MOSTAFA OSMAN
            }  # HORUS AND MOSTAFA OSMAN
            QPushButton {  # HORUS AND MOSTAFA OSMAN
                background-color: #4e4e4e;  # HORUS AND MOSTAFA OSMAN
                border: none;  # HORUS AND MOSTAFA OSMAN
                color: #ffffff;  # HORUS AND MOSTAFA OSMAN
            }  # HORUS AND MOSTAFA OSMAN
            QPushButton:hover {  # HORUS AND MOSTAFA OSMAN
                background-color: #5e5e5e;  # HORUS AND MOSTAFA OSMAN
            }  # HORUS AND MOSTAFA OSMAN
        """  # HORUS AND MOSTAFA OSMAN

if __name__ == "__main__":  # HORUS AND MOSTAFA OSMAN
    app = QApplication(sys.argv)  # HORUS AND MOSTAFA OSMAN
    window = Browser()  # HORUS AND MOSTAFA OSMAN
    window.show()  # HORUS AND MOSTAFA OSMAN
    sys.exit(app.exec_())  # HORUS AND MOSTAFA OSMAN
