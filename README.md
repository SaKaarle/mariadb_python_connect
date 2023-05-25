# MariaDB Python Connection

Python koodi jolla kerätään dataa lähettämällä sitä MariaDB / MySQL tietokantaan. Raspberry Pi:stä lähtee kolme GPIO pinniä jotka ottaa yhteyden toiseen laitteeseen. Tässä työssä on otettu yhtyes laitteeseen hyödyntäen releitä jotka sieppaavat signaaleja.
Python koodi on keskeneräinen, mutta käytetään tuotannossa.
Sovelluksia joita käytetään:
- Putty
- Visual Studio Code
- MariaDB
- (MariaDB ODBC Connector 3.1.X)[https://mariadb.com/downloads/connectors/connectors-data-access/odbc-connector]
- HeidiSQL
- Power BI

## Raspberry Pi tai vastaava yhden piirilevyn tietokone
Vaatimukset yhden piirilevyn tietokoneelta:
- Raspberry Pi (2 - 4)
- GPIO pinnejä
- Debian pohjautuva -linux distro.
- Python versio 3.9

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
 
MariaDB databasen luonti:
 
```
DROP DATABASE IF EXISTS db_esimerkki;
CREATE DATABASE db_esimerkki;
```
 
Tietokanta "db_esimerkki" on luotu ja sille annetaan seuraavaksi taulukkotiedot.
 
Taulukon voi luoda käyttämällä GUI:ta käyttävää HeidiSQL:ää pöytäkoneella tai asennettaessa PHPMyAdmin ja Raspberry Pi:llä selaimen kautta.
Tässä esimerkissä olen luonut HeidiSQL sovelluksella taulukon ja kopioinut skriptin siitä.
 
Taulukon luonti datasyöttöä varten:
```
DROP TABLE if exists laserdata;

CREATE TABLE `laserdata` (
	`machine_id` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`start_time` DATETIME NULL DEFAULT NULL,
	`end_time` DATETIME NULL DEFAULT NULL,
	`duration` TIME NULL DEFAULT NULL,
	`isFault` TINYINT(1) NULL DEFAULT NULL
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

Raspberry Pi:n vaadittavat asennukset Python Connectorille
```
sudo apt-get install libmariadb3 libmariadb-dev
```
 
MariaDB pip asennus importattavalle MariaDB paketille
```
#Vanhempi
sudo python3 -m pip install mariadb
```
Jos yrittää asentaa uusinta versiota esim 1.1.6, tulee virhe ilmoitus:

```
#MariaDB 1.0.11 versio on uusin mahdollinen päivitys ARM pohjasille laitteille.
  × Getting requirements to build wheel did not run successfully.
  │ exit code: 2
  ╰─> [1 lines of output]
      MariaDB Connector/Python requires MariaDB Connector/C >= 3.3.1, found version 3.1.16
      [end of output]
```

Asentamalla [mariadb==1.0.11](https://mariadb-corporation.github.io/mariadb-connector-python/release.html#mariadb-connector-pyhon-1-0-11) saa viimeisimmän päivityksen Raspberry:lle.

```
sudo python3 -m pip install mariadb==1.0.11
```
 
PHP paketti
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

# Sovelluksen automaattinen käynnistys
 
Linux Distroille on kehitetty monenlaisia sovelluksen automaattisia käynnistyspalveluita ja käyttäjä itse saa päättää mitä haluaa käyttää tai hyödyntää. Tässä esimerkissä olen käyttänyt SystemD. Vaihtoehtoisesti suosittelen [crontab](https://www.dexterindustries.com/howto/auto-run-python-programs-on-the-raspberry-pi/) yksinkertaisuuden takia. 

## Crontab
 
Crontab on yksinkertainen vaihtoehto laittamaan palveluita käyntiin laitteen käynnistyessä. Ohjeita löytyy erillaisille toiminnoille ja mitä halutaan saavuttaa vaikka Raspberry Pi / SBC käynnistyksessä.
[Asennusohjeita](https://www.dexterindustries.com/howto/auto-run-python-programs-on-the-raspberry-pi/) seuraamalla asennetaan Crontab terminaalista `sudo apt install cron` 
Tässä esimerkissä tein Raspberry Pi OS:n natiiville SystemD palvelulle käynnistyskäskyt.

## SystemD startup konfigurointi

Jos jostain syystä ei ole asennettuna `systemd` pakettia, se pystytään asentamaan komennolla: `sudo apt install libsystemd-dev` tälläisen paketinasennuksen jälkeen on suositeltavaa käynnistää laite uusiksi

Komento, jolla luodaan oma "Service". 
```
sudo nano /lib/systemd/system/rasplaser.service 
```
korvaamalla "rasplaser" voidaan lisätä oma palvelunnimi. esim `sudo nano /lib/systemd/system/omapalvelualoitussovellus.service.`

Tiedostoon rasplaser.service lisätään seuraavat komennot:

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
 
Toinen vaihtoehto ongelmien korjaamiseen on asentaa uusi [NetworkManagerin](https://wiki.archlinux.org/title/NetworkManager). Tämä on stabiilimpi ja varmempi nettikonfiguroinneissa ja tulee korvaamaan nykyisen dhcpcd. Tarkemmat asennusohjeet löytyvät [Stack Exchange](https://raspberrypi.stackexchange.com/a/116808) sivustolta, mutta yksinkertaisesti:

 

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

Viimeisimmässä muokkauksessani löysin mahdollisen syyn, miksei `rasplaser.service` lähtenyt käyntiin. `After=network.target` viivästyttää vielä Python skriptin aktivoinnin, että MariaDB / MySQL Service pystyvät aktivoitumaan. `sudo systemctl status rasplaser` antoi virheeksi, ettei kykenyt lukemaan MariaDB .json tiedosta, jossa on kirjautumistiedot.
 

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

