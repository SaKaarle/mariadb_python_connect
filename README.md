# MariaDB Python Connection

Koodin pätkää, 3 pinniä jotka ottaa yhteyden laitteeseen (invasiivinen) tuotantoon tarkoitettuihin laitteisiin
Python skripti on puhdistusta vailla

## Raspberry Pi (3B+)
Raspberryyn on asennettuna Apache 2 serveri, MariaDB/MySQL tietokanta ja phpMyAdmin
 
MariaDB serverin asennus:
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
pip3 install mariadb
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

## SystemD startup konfigurointi

Komento, jolla luodaan "Service"
```
sudo nano /lib/systemd/system/rasplaser.service 
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
 
CTRL - X ja Y ja Enter. Tiedostoon tehdyt muutokset tallennetaan.
