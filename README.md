[![DOI](https://zenodo.org/badge/534218525.svg)](https://zenodo.org/badge/latestdoi/534218525)


![Älykkäät teknologiat](https://storage.googleapis.com/seamk-production/2022/04/2b1d63e0-alykkaat-teknologiat_highres_2022-768x336.jpg)
![ESR](https://storage.googleapis.com/seamk-production/2022/02/da4e4541-eu-lippu-290x300.png) ![Vipuvoimaa](https://storage.googleapis.com/seamk-production/2022/02/8d432b35-vipuvoimaa-eulta-logo-300x212.png) ![ELY-keskus](https://storage.googleapis.com/seamk-production/2021/08/5e942eac-ely-keskus_logo-300x105.png) ![SeAMK](https://storage.googleapis.com/seamk-production/2022/02/79a4ce1b-seamk_vaaka_fi_en_rgb_1200x486-300x122.jpg)

# Laserleikkurin datan keruu ja visualisointi

Yhden piirilevyn tietokone, johon on rakennettu Python sovellus keräämään dataa toisesta laitteesta ja lähettämällä sitä MariaDB / MySQL tietokantaan. Raspberry Pi:stä lähtee kolme GPIO pinniä jotka ottaa yhteyden toiseen laitteeseen. Tässä työssä on otettu yhtyes laitteeseen hyödyntäen releitä jotka sieppaavat signaaleja.
Python koodi on keskeneräinen, mutta käytetään tuotannossa.
Sovelluksia joita käytetään Windows tietokoneella:
- Putty (SSH yhteyden muodostaminen)
- Raspberry Pi Imager (Käyttöjärjestelmän asennus SD-kortille)
- Visual Studio Code
- Python 3.7
- MariaDB (jos tietokanta asennetaan tietokoneelle ja dataa tuodaan Raspberry Pi:stä)
- [MariaDB ODBC Connector 3.1.X](https://mariadb.com/downloads/connectors/connectors-data-access/odbc-connector) (Vaaditaan Power BI:n kanssa, että yhteys voidaan muodostaa)
- HeidiSQL (Asentuu MariaDB sovelluksen yhteydessä halutessa)
- Power BI (Kaavioiden luontiin ja datan visualisointi)

# Julkaisun historiatiedot
Merkittävät muutokset julkaisuun

|pvm|Muutokset|Tekijä|
|---|---|---|
|21.6.2023|Versio 1.0 julkaisu|Saku Kaarlejärvi|
|21.6.2023|Zenodo julkaisu|Saku Kaarlejärvi|
|8.8.2023|Versio 1.1 julkaisu|Saku Kaarlejärvi|

# Sisällysluettelo
- [Julkaisun nimi](#laserleikkurin-datan-keruu-ja-visualisointi)
- [Julkaisun historiatiedot](#julkaisun-historiatiedot)
- [Sisällysluettelo](#sisällysluettelo)
- [Teknologiapilotti](#teknologiapilotti)
- [Hanketiedot](#hanketiedot)
- [Kuvaus](#kuvaus)
- [Tavoitteet](#tavoitteet)
- [Toimenpiteet](#toimenpiteet)
- [Asennus ja käyttö](#asennus-ja-käyttö)
- [Python ohjelman käyttö](#Python-ohjelman-käyttö)
- [Havaitut virheet ja ongelmatilanteet](#HAVAITUT-VIRHEET-JA-ONGELMATILANTEET)
- [Vaatimukset](#laserleikkurin-datan-keruu-ja-visualisointi)
- [Tulokset](#tulokset)
- [Lisenssi](#lisenssi)
- [Tekijät](#tekijät)
 

# Teknologiapilotti
TehoData-hankkeen pilotissa 3 pyrittiin luomaan tuotannon seurannan datankeruu sovellus hyödyntäen yhdenpiirilevyn tietokonetta ja avoimen lähdekoodin tietokantaa.

# Hanketiedot
- Hankkeen nimi: Datasta ketteryyttä ja uutta liiketoimintaa Etelä-Pohjanmaan pk-yrityksiin (TehoData)
- Rahoittaja: Keski-Suomen ELY/ Euroopan sosiaalirahasto ESR
- Aikataulu: 1.9.2021–31.10.2023
Hanke rahoitetaan REACT-EU-välineen määrärahoista osana unionin covid-19-pandemian johdosta toteuttamia toimia.
TehoDatan hankesivut löytyvät osoitteesta [https://projektit.seamk.fi/alykkaat-teknologiat/tehodata/](https://projektit.seamk.fi/alykkaat-teknologiat/tehodata/)

# Kuvaus
Python koodi jolla kerätään dataa lähettämällä sitä MariaDB / MySQL tietokantaan. Raspberry Pi:stä lähtee kolme GPIO pinniä jotka ottaa yhteyden toiseen laitteeseen. Tässä työssä on otettu yhtyes laitteeseen hyödyntäen releitä jotka sieppaavat signaaleja.

# Tavoitteet
Pilotissa kehitettiin sovellusta Raspberry Pi 4 laitteelle jolla pystytään keräämään dataa seuratakseen tuotantoa. Kerättyä dataa pystytään visuaalisesti katsoa kaavioista.

# Toimenpiteet
Raspberry Pi 4 valmisteltiin pilottiyritystä varten tuotannon seurantaan. Kyseiselle Raspberry Pi:lle kehitettiin sovellus jolla pystytään kaappaamaan kolmesta eri pinnistä dataa. Nämä datat tuovat esille, onko laite sammutettu, käynnistetty, odottamassa toimeenpiteitä ja leikkaustilassa. Python -ohjelmointikielellä rakennettu sovellus luo näistä tiedoista dataa joka siirretään pilottiyrityksen omaan MariaDB tietokantaan, jota voidaan visuaalisesti käsitellä eri sovelluksissa. 

# Asennus ja käyttö

## Vaadittavat asennekuset Windows -tietokoneelle
Lista sovelluksista:
- Putty (SSH yhteyden muodostaminen)
- Raspberry Pi Imager (Käyttöjärjestelmän asennus SD-kortille)
- Visual Studio Code tai jokin muu IDE -sovellus
- Python 3.7
- MariaDB (jos tietokanta asennetaan tietokoneelle ja dataa tuodaan Raspberry Pi:stä)
- [MariaDB ODBC Connector 3.1.X](https://mariadb.com/downloads/connectors/connectors-data-access/odbc-connector) (Vaaditaan Power BI:n kanssa, että yhteys voidaan muodostaa)
- HeidiSQL (Asentuu MariaDB sovelluksen yhteydessä halutessa)
- Power BI (Kaavioiden luontiin ja datan visualisointi)

Tästä GitHub repositorista tarpeellisin ladattava on vain [mariadbCon.py](https://github.com/SaKaarle/tehodata-lasercuttingmachine-data-collection/blob/master/mariadbCon.py) -tiedosto joka siirretään Raspberry Pi:lle / yhden piirilevyn tietokoneeseen.


## Raspberry Pi tai vastaava yhden piirilevyn tietokone
Vaatimukset yhden piirilevyn tietokoneelta:
- Vaihtoehtoisesti "Headless" debian käyttöjärjestelmä asennus. Pystytään Raspberry Pi Imager -sovelluksella esiasetukset (WLAN, kieli, käyttäjätili ja salasana) ja VNC yhteydellä etäyhteys laitteeseen.
- Raspberry Pi (2 - 4)
- GPIO pinnejä
- Debian pohjautuva -linux distro.
- Python versio 3.7. Python versio voidaan asentaa 3.10 asti, mutta vaatii vianselvityksiä saadakseen esim. GPIO pinnien toimimaan. Tässä esimerkissä asensin [ohjeiden mukaan Python 3.9.16 version](https://linuxhint.com/update-python-raspberry-pi/)


## MariaDB tietokannan asennus
Raspberry Pi:lle MariaDB/MySQL tietokanta ja tarvittaessa tietokannan hallintaan graafisella käyttöjärjestelmä Apache2 ja phpMyAdmin. 
 
MariaDB serverin asennus Raspberryyn:
```
sudo apt install mariadb-server
```
 
Asennuksen jälkeen on suoritettava MySQL Secure asennus
```
sudo mysql_secure_installation
```
 
Terminaaliin Y/N vastauksia vaatimuksien mukaan.
 
Asennuksen jälkeen kirjaudutaan MariaDB serveriin syötetyillä "root" käyttäjätiedoilla.
```
sudo mysql -u root -p
```
MySQL kysyy asennuksessa syötettyä root -salasanaa. Syöttämällä sen varmistetaan MariaDB toimivuus.
 
## MariaDB databasen luonti

Kirjauduttua sisään MariaDB tietokantaan, voidaan rakentaa oma tietokanta ja taulukko.

```
DROP DATABASE IF EXISTS db_esimerkki;
CREATE DATABASE db_esimerkki;
```
 
Tietokanta "db_esimerkki" on luotu ja sille annetaan seuraavaksi taulukkotiedot.
 
Taulukon voi luoda käyttämällä GUI:ta käyttävää HeidiSQL:ää pöytäkoneella tai asennettaessa PHPMyAdmin ja Raspberry Pi:llä selaimen kautta.
Tässä esimerkissä olen luonut HeidiSQL sovelluksella taulukon ja kopioinut skriptin siitä.
 
Taulukon luonti datasyöttöä varten:

HUOM!

Yleisesti "duration" eli kesto -dataa on hyvä mitata sekuntteina. mariadbCon.py tiedostossa luodaan `"hh:mm:ss"` dataa joka on virheellinen tapa merkata kesto. Power BI:ssä esimerkisi vaaditaan muuttaa "duration" data sekunteiksi pilkkomalla `hh:mm:ss` omiin osiinsa ja käyttämällä laskentakaavioita saadakseen oikean tuloksen ja muuntaa takaisin `hh:mm:ss` muotoon.

```
DROP TABLE if exists laserdata;

CREATE TABLE `laserdata` (
	`machine_id` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`start_time` DATETIME NULL DEFAULT NULL,
	`end_time` DATETIME NULL DEFAULT NULL,
	`duration` VARCHAR(50) NULL DEFAULT NULL,
	`isFault` TINYINT(10) NULL DEFAULT NULL
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;
```
 
MariaDB:n käyttäjän luonti. Root ei ole suotavaa käyttää .
"käyttäjänimi" ja "käyttäjänsalasana" kohdille laitetaan omat halutut tiedot.
 
```
DROP USER IF EXISTS käyttäjänimi;
CREATE USER 'käyttäjänimi'@'%' IDENTIFIED BY 'käyttäjänsalasana';
GRANT SELECT, INSERT, DELETE, UPDATE ON db_esimerkki.laserdata TO 'käyttäjänimi'@'%';
FLUSH PRIVILEGES;
```
Jos yhteysongelmia ilmenee käyttäjätilin kanssa, voidaan kokeilla syöttää oikeus jokaiselle IP osoittelle. Tämä ei ole suositeltavaa tietoturva syistä: `CREATE USER 'käyttäjänimi'@'%.%.%.%' IDENTIFIED BY 'käyttäjänsalasana';` tai syöttää manuaalisesti IP osoite, josta pystytään ottamaan yhteyttä.
Esim. `CREATE USER 'käyttäjänimi'@'192.168.0.21' IDENTIFIED BY 'käyttäjänsalasana';`
Tai reitittimen määrittämästä IP osoite alueelta: `CREATE USER 'käyttäjänimi'@'192.168.0.%' IDENTIFIED BY 'käyttäjänsalasana';`
 

## Raspberry Pi:n vaadittavat asennukset Python Connectorille
```
sudo apt-get install libmariadb3 libmariadb-dev
```
 
## MariaDB pip asennus importattavalle MariaDB paketille
```
#Vanhempi
sudo python3 -m pip install mariadb
```

Jos yrittää asentaa uusinta versiota esim 1.1.6, tulee virhe ilmoitus:

```
  × Getting requirements to build wheel did not run successfully.
  │ exit code: 2
  ╰─> [1 lines of output]
      MariaDB Connector/Python requires MariaDB Connector/C >= 3.3.1, found version 3.1.16
      [end of output]
```
MariaDB 1.0.11 versio on uusin mahdollinen päivitys ARM pohjasille laitteille.
Asentamalla [mariadb==1.0.11](https://mariadb-corporation.github.io/mariadb-connector-python/release.html#mariadb-connector-pyhon-1-0-11) saa viimeisimmän päivityksen Raspberry:lle.

```
sudo python3 -m pip install mariadb==1.0.11
```
 
## phpMyAdmin paketti
```
sudo apt install phpmyadmin
```
 
PHP asennusikkuna kysyy ensimmäisenä, mikä webserver palvelu asennetaan. Tässä esimerkissä Apache2 valitaan välilyönnillä ja siirrytään eteenpäin rivinvaihdolla. Asennus kyselee tietoja ja halutessa syötetään halutut tiedot, kuten PHPMyAdminin salasanat ja muut tärkeät tiedot.
 
Asennuksen jälkeen on muokattava Apache2 konfiguraatiotiedostoa.
 
```
sudo nano /etc/apache2/apache2.conf
```
 
Tekstieditori avaa Apache2.conf tiedoston jonne lisätään pohjalle koodi:
```
Include /etc/phpmyadmin/apache.conf
```
 
CTRL - X ja Y ja Enter. Tiedostoon tehdyt muutokset tallennetaan.
 

Tarvittavat lisäpalvelut on asennettava, että PHPMyAdmin sivusto toimii
```
apt install php7.4 libapache2-mod-php7.4 php7.4-mbstring php7.4-mysql php7.4-curl php7.4-gd php7.4-zip -y  
```
 

Apache2 palvelu on hyvä uudelleen käynnistää komennolla:
```
sudo service apache2 restart
```
 

Komennolla "hostname -I" saadaan selville IP-osoite jolla päästään PHPMyAdmin sivulle. Esimerkkinä tulee näkyviin "192.168.0.21" ja tähän lisätään perään "/phpmyadmin"
``` 
hostname –I

192.168.0.21
```
Selaimeen voidaan syöttää osoite `http://192.168.0.21/phpmyadmin` ja PHPMyAdmin kirjautumisvalikko pitäisi avautua.

## Sovelluksen automaattinen käynnistys
 
Linux Distroille on kehitetty monenlaisia sovelluksen automaattisia käynnistyspalveluita ja käyttäjä itse saa päättää mitä haluaa käyttää tai hyödyntää. Tässä esimerkissä olen käyttänyt SystemD. Vaihtoehtoisesti suosittelen [crontab](https://www.dexterindustries.com/howto/auto-run-python-programs-on-the-raspberry-pi/) yksinkertaisuuden takia. 

## Crontab
 
Crontab on yksinkertainen vaihtoehto laittamaan palveluita käyntiin laitteen käynnistyessä. Ohjeita löytyy erillaisille toiminnoille ja mitä halutaan saavuttaa vaikka Raspberry Pi / SBC käynnistyksessä.
[Asennusohjeita](https://www.dexterindustries.com/howto/auto-run-python-programs-on-the-raspberry-pi/) seuraamalla asennetaan Crontab terminaalista `sudo apt install cron` 
Tässä esimerkissä tein Raspberry Pi OS:n natiiville SystemD palvelulle käynnistyskäskyt.

## SystemD startup konfigurointi
![SystemD config example](https://github.com/SaKaarle/tehodata-lasercuttingmachine-data-collection/blob/master/kuvat/Putty%20Sudo%20Nano%20ikkuna.png)

Jos jostain syystä ei ole asennettuna `systemd` pakettia, se pystytään asentamaan komennolla: `sudo apt install libsystemd-dev` tälläisen paketinasennuksen jälkeen on suositeltavaa käynnistää laite uusiksi

Terminaaliin kirjoitetaan komento, jolla luodaan oma "Service" laitteelle. 
```
sudo nano /lib/systemd/system/rasplaser.service 
```
korvaamalla "rasplaser" voidaan lisätä oma palvelunnimi. esim `sudo nano /lib/systemd/system/omapalvelualoitussovellus.service.`

Tässä esimerkissä loin `rasplaser.service` tiedoston jonne laitetaan halutut komennot ja määritykset käynnistyessä. 
Palvelu tiedostoon `rasplaser.service` lisätään seuraavat komennot:

```
[Unit]
#Human readable name of the unit
Description=Python Script LaserMachine
After=multi-user.target
[Service]
User=pi
Type=idle
ExecStart=/usr/bin/python /home/pi/Desktop/sshVSC/mariadbCon.py
[Install]
WantedBy=multi-user.target
```

HUOM!
 
Kohta `ExecStart=` ja `/home/pi/Desktop/sshVSC/mariadbCon.py` on ohjelmakoodin sijainti. Varmista että sijainti on oikea ja olemassa laitteessa. Muuten sovellus ei tule käynnistymään
 

Tämä on tällä hetkellä minulla toimiva rasplaser.service tiedosto. README:n lopusta löytyy eri vaihtoehtoja ja havaittuja virheitä ja korjausehdotuksia.
 

CTRL - X ja Y ja Enter. Tiedostoon tehdyt muutokset tallennetaan.
 
Oikeudet lukea service käynnistyessä:

```
sudo chmod 755 /home/pi/Desktop/sshVSC/

sudo chmod 644 /lib/systemd/system/rasplaser.service
```

Terminaaliin on syötettävä `sudo systemctl daemon-reload` virkistääkseen käynnistyskomennot Raspberry:stä

```
sudo systemctl daemon-reload
sudo systemctl enable rasplaser
sudo systemctl start rasplaser

```
 
Terminaaliin kirjoitettu `sudo systemctl enable rasplaser` voidaan aktivoida luotu palvelu käynnistykseen.
```
$ sudo systemctl enable rasplaser
Created symlink /etc/systemd/system/multi-user.target.wants/rasplaser.service → /lib/systemd/system/rasplaser.service.

```
Terminaaliin kirjoitettuna `sudo systemctl status rasplaser` nähdään, onko service aktiivinen
 
```
rasplaser.service - Python Script LaserMachine
     Loaded: loaded (/lib/systemd/system/rasplaser.service; disabled; vendor pr>
     Active: active (running) since Tue 2023-04-24 10:21:37 EET; 3s ago
   Main PID: 29502 (python)
      Tasks: 1 (limit: 8986)
        CPU: 134ms
     CGroup: /system.slice/rasplaser.service
             └─29502 /usr/bin/python /home/pi/Desktop/sshVSC/mariadbCon.py

Dec 20 18:21:37 rpam systemd[1]: Started Python Script LaserMachine.

```
Suorittamalla tämän jälkeen `sudo reboot -h now` voidaan uudelleen käynnistyksen jälkeen tarkistaa toimiiko automaattinen palvelunkäynnistys.
Kirjoittamalla uudelleen `sudo systemctl status rasplaser` komentoriville ja tarkista onko palvelu aktiivinen ja mikä "Main PID" palvelulla on. Ylhäällä huomataan palvelun olevan 29502, eli mitä suurempi luku, sitä myöhässä se käynnistyy. Uudelleen käynnistämällä selviää oikea "Main PID" luku.

```
● rasplaser.service - Python Script LaserMachine
     Loaded: loaded (/lib/systemd/system/rasplaser.service; enabled; vendor pre>
     Active: active (running) since Tue 2023-04-24 10:30:28 EEST; 15s ago
   Main PID: 917 (python)
      Tasks: 2 (limit: 1629)
        CPU: 8.463s
     CGroup: /system.slice/rasplaser.service
             └─917 /usr/bin/python /home/pi/Desktop/sshVSC/mariadbCon.py

Apr 25 10:30:28 rpi3B systemd[1]: Started Python Script LaserMachine.

```

# Python ohjelman käyttö

[Tiedosto mariadbCon.py](https://github.com/SaKaarle/tehodata-lasercuttingmachine-data-collection/blob/master/mariadbCon.py) on ladattavissa ja siirrettävissä käyttöönottoa varten määritettyyn kansioon, kuten SystemD esimerkissäni olen käyttänyt `/home/pi/Desktop/sshVSC/mariadbCon.py` osoitetta.
Python koodi tarvitsee muutoksia, jotka on `mariadbCon.py` -tiedostoon merkitty `#` -kommentteina.
 
![Selitys visuaalisesti mikä on kommentti.](https://github.com/SaKaarle/tehodata-lasercuttingmachine-data-collection/blob/master/kuvat/T%C3%A4m%C3%A4%20on%20kommentti.png)
 
Risuaita rivinalussa on kommentti, jota ohjelma ei pysty lukemaan. Sinne voidaan kirjoittaa mitä vain eikä se häiritse ohjelman suorittamista.

Raspberry Pi:n GPIO pinnit selitettynä.
 
![Pinni taulukko Raspberry PI:lle selitettynä](https://cdn.sparkfun.com/assets/learn_tutorials/1/5/9/5/GPIO.png)

Tässä Python ohjelmassa ovat GPIO pinnit 23, 24 ja 25 ovat valittuna. Pinnit ovat järjestysluvuiltaan 16, 18 ja 22. Näihin kytketään kolme kytkintä joilla kerätään tuotantolaitteesta dataa.

| 23 | 24 | 25 |
|---|---|---|
|Laseri päällä|Laite on IDLE -tilassa|Laite on päällä|
 
## Muutoksia ohjelmakoodiin
 
Ohjelmakoodiin on määritettävä muutoksia saadakseen se toimivaksi omaan käyttöön. Lataamalla ja siirtämällä `mariadbCon.py` -tiedoston on varmistettava, että se on [SystemD käynnistyspalvelun mukaisesti](#SystemD-startup-konfigurointi) `rasplaser.service` määritetyssä tiedostopolussa. Muuten ohjelma vain käynnisty ja ei tee mitään. Tätä polkua voidaan muokata omaan haluttuun sijantiin ja on tehtävät tarvittavat muutokset sovelluksen toimivuudeksi.
 

## Tiedostopolun määrittely
 
Python ohjelmassa on rivillä 69 määritetty tiedostopolku alla olevan kuvanmukaisesti:
 
![Tiedostopolku kuvankaappaus](https://github.com/SaKaarle/tehodata-lasercuttingmachine-data-collection/blob/master/kuvat/tiedostopolku.png)
 
## Käyttäjätilikredentiaalit JSON tiedostoon
 
Tiedostopolun määrittelyn jälkeen on luotava kirjautumiskredentiaalit. Luodaan JSON -tiedosto esimerkiksi `userconf.json`. Tekstitiedostoa muokkaamalla pystytään lisäämään `userconf.json` tiedostoon kirjautumiskredentiaalit, jonka ohjelma lukee kirjautuakseen sisään määritettyyn MariaDB -tietokantaan.
 
Tekstitiedostoon lisätään käyttäjätilitiedot `user` ja `password`.
Myös luetaan tiedostosta tietokannan IP-osoite `host` esimerkiksi `192.168.0.21` tai jos Raspberry PI:n omaan MariaDB tietokantaan, niin `localhost`. Tietokannan `port` on vakiona `3306` ja lopuksi määritetään `database` eli tietokanta, johon yhteys muodostetaan. Esimerkissä luotiin tietokanta `db_esimerkki`.
 
Alla on esimerkki tiedostosta `userconf.json`:
``` 
{
    "user": "käyttäjänimi",
    "password": "käyttäjänsalasana",
    "host": "192.168.0.21",
    "port": 3306,
    "database": "db_esimerkki"
}
```

Tiedoston voi ladata [täältä.](https://github.com/SaKaarle/tehodata-lasercuttingmachine-data-collection/blob/master/userconf.json)
Tämän `userconf.json` tiedosto luonnin jälkeen on hyvä varmistaa, että ohjelmakoodi lukee oikean tiedoston saadakseen yhteyden MariaDB -tietokantaan.
Kuvassa on esimerkki, missä pystytään tarkistamaan minkä tiedoston ohjelma lukee.
 
![userconf kredentiaalitiedosto](https://github.com/SaKaarle/tehodata-lasercuttingmachine-data-collection/blob/master/kuvat/MariaDB%20connect.png)
 
Kuvassa ohjelma lukee `jsonPath` määritetystä tiedostopolusta `userconfHome.json` -tiedoston. Tämä pitää varmistaa, että yhteys onnistuu halutulle MariaDB -tietokannalle

 

# Havaitut virheet ja ongelmatilanteet
 
## Palvelu ei käynnisty Raspberry Pi:n yhtyedessä
-Tarkista verkkoyhteys, myös Wi-Fi yhteys jos langatonverkkoyhteys on käytössä.

## Palvelu ei käynnisty laitteen käynnistyksen yhteydessä, mutta käynnistyy `sudo systemctl restart omapalvelu.service` jälkeen.

Tässä on iso selvitys tehty:

```
[Unit]
##Human readable name of the unit
Description=Python Script LaserMachine
After=network.target multi-user.target

[Service]
#User=root
Type=idle
ExecStart=/usr/bin/python3 -u /home/pi/Desktop/sshVSC/mariadbCon.py
WorkingDirectory=/home/pi/Desktop/sshVSC
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```
 
Kokemuksellani, `User=pi` ei aina löydä paketteja, joten voidaan vaihtoehtoisesti käyttää `User=root` käyttäjää
Myös monen ongelmatilanteen jälkeen huomattiin, että lisäämällä rasplaser.service tiedostoon `Restart=on-failure` ja `WorkingDirectory=/home/pi/jokinsijainti` saadaan käynnistys toimimaan. Muista lähteistä löytyy hyvät ohjeet lisätä python skripti ja tärkeät tiedostot "järjestelmän" kansioihin, ettei tarvitse välittää `chmod 755` tai muista oikeuksien lisäämisestä.
 
Näiden lisäksi, [Python pakettien](https://pypi.org/) asennuksia voidaan joutua suorittamaan uudelleen. Paketit saattavat "kadota" tai "hukkua" käyttöoikeuksista JOS käytetään `User=root` käyttäjää palvelukonfiguraatiossa. Uudelleen asennukset on suositeltavaa tehdä `sudo`:lla saadakseen pääkäyttäjä oikeudet ja `python3`:lla varmistetaan että asennetaan oikealle Python versiolle paketit. Esimerkki komento terminaaliin: `sudo python3 -m pip install [package-name]`
 
Minulle ilmeni vastaavia ongelmia ja tiedä tarkempia syitä, mitkä tekijät ovat tuoneet nämä viat vastaan. Tälläisissä projekteissa on myös suotavaa rakentaa `venv` eli [virtuaali ympäristö](https://docs.python.org/3/library/venv.html) jonne asennetaan omat halutut ja tarvittavat paketit, sekä `rasplaser.service` tiedostoon määritetään sijainti mistä tämä sovellus ajetaan hyödyntäen virtuaali ympäristöä. Tässäkin tapauksessa, jos on syötetty arvot `User=root` palvelutiedostoon, on tärkeä myöntää kansiolle `chmod 755` kirjoitus- ja lukuoikeudet.
 
```
[Unit]
#Human readable name of the unit
Description=Python Script LaserMachine
After=multi-user.target
[Service]
User=pi
Type=idle
ExecStart=/usr/bin/python /home/pi/Desktop/sshVSC/mariadbCon.py
[Install]
WantedBy=multi-user.target
```

Viimeisimmässä havainnoissani huomasin virheen ja selvitin, miksei `rasplaser.service` lähtenyt käyntiin. `After=network.target` viivästyttää vielä Python skriptin aktivoinnin, että MariaDB / MySQL Service pystyvät aktivoitumaan. `sudo systemctl status rasplaser` antoi virheeksi, ettei kykenyt lukemaan MariaDB .json tiedosta, jossa on kirjautumistiedot.
 
Myös eri vaihtoehto ongelmien korjaamiseen on asentaa uusi [NetworkManagerin](https://wiki.archlinux.org/title/NetworkManager). Tämä on stabiilimpi ja varmempi nettikonfiguroinneissa ja tulee korvaamaan nykyisen dhcpcd. Tarkemmat asennusohjeet löytyvät [Stack Exchange](https://raspberrypi.stackexchange.com/a/116808) sivustolta, mutta yksinkertaisesti:

```
sudo apt install network-manager network-manager-gnome

sudo systemctl enable NetworkManager
sudo systemctl start NetworkManager
sudo systemctl disable dhcpcd

sudo reboot -h now
```

On tärkeää tarkistaa DHCP -palvelun tila ettei se ole häiritsemässä taustalla.

```
pi@rpi3B:~ $ sudo systemctl status dhcpcd
● dhcpcd.service - DHCP Client Daemon
     Loaded: loaded (/lib/systemd/system/dhcpcd.service; enabled; vendor preset: enabled)
     Active: inactive (dead)
       Docs: man:dhcpcd(8)

```

# Tulokset
Tulossa pian...

# Lisenssi
Dokumentit lisensoitu:
- [![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
  
# Tekijät

Saku Kaarlejärvi
