# TÜRKÇE[TR]
# Dağıtık Güvenli Depolama Sistemi (DGDS)

## Proje Hakkında
Bu proje, Hackathon etkinliği için geliştirilmiş, Flask tabanlı bir web uygulamasıdır. Bu sistem, verileri merkezi olmayan bir şekilde kullanıcıların bilgisayarlarında şifreli olarak saklamayı hedeflemektedir. Böylece, veri güvenliği maksimize edilir ve merkezi sistemlerin karşılaştığı riskler azaltılır.

## Projenin Amacı
Merkezi depolama sistemlerinin olası güvenlik risklerini minimize ederek, kullanıcıların bilgisayarları arasında şifreli verilerin güvenli bir şekilde saklanmasını sağlamak.

## Ana Özellikler
- **Veri Şifreleme**: Kullanıcıların bilgisayarlarına parçalı ve şifreli veriler dağıtılır.
- **Dağıtık Saklama**: Her bilgisayar verinin yalnızca parçalarını içerir, böylece tam veriye erişim engellenmiş olur.
- **Blokzincir Entegrasyonu**: Verilerin hangi bilgisayarda saklandığına dair günlükler blokzincir üzerinde güvenli bir şekilde tutulur.

## Teknolojiler
- Flask
- HTML/CSS
- Python
- Blokzincir

## Kurulum Adımları
1. Repo klonlama: `git clone https://github.com/TolgaTD/Hackathon-Team3RG3N3K0N.git`
2. Gerekli kütüphaneleri yükleme: `pip install -r requirements.txt`
3. Uygulamayı çalıştırma: `python app.py`
4. Tarayıcıda uygulamaya erişim: `http://localhost:5000`

## Kullanım Senaryoları
- **Güvenli Dosya Yükleme**: Dosyalarınızı web arayüzünden yükleyebilirsiniz.
- **Güvenli Dosya İndirme**: Yüklenen dosyaların şifreli parçalarını indirebilirsiniz.

## Lisans
Bu proje MIT lisansı altında lisanslanmıştır.


# ENGLISH[EN]
# Distributed Secure Storage System (DGDS)

## About the Project
This project is a Flask-based web application developed for a Hackathon event. It aims to securely store encrypted data on users' computers in a decentralized manner, maximizing data security and minimizing the risks associated with central storage systems.

## Purpose of the Project
To minimize the potential security risks of central storage systems by securely storing encrypted data across users' computers.

## Key Features
- **Data Encryption**: Data is distributed encrypted and in pieces to users' computers.
- **Distributed Storage**: Each computer contains only parts of the data, preventing full data access.
- **Blockchain Integration**: Logs of where data is stored are securely kept on the blockchain.

## Technologies
- Flask
- HTML/CSS
- Python
- Blockchain

## Installation Steps
1. Clone the repository: `git clone https://github.com/TolgaTD/Hackathon-Team3RG3N3K0N.git`
2. Install required libraries: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Access the application in the browser: `http://localhost:5000`

## Usage Scenarios
- **File Upload**: You can upload your files through the web interface.
- **File Download**: You can download the encrypted parts of the uploaded files.

## License
This project is licensed under the MIT License.

