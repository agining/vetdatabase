DROP TABLE BAGLIDIR;
DROP TABLE RANDEVU;
DROP TABLE AMELIYAT;
DROP TABLE HAYVAN;
DROP TABLE SAHIP;
DROP TABLE HEKIM;
DROP TABLE STAJER;

CREATE TABLE HEKIM(
	isim varchar(10) NOT NULL,
	soyisim varchar(12) NOT NULL,
	email varchar(20) UNIQUE,
	sifre varchar(20) NOT NULL,
	num int NOT NULL,
	Primary key(num)
);

CREATE TABLE STAJER(
	isim varchar(10) NOT NULL,
	soyisim varchar(12) NOT NULL,
	email varchar(20) UNIQUE,
	sifre varchar(20) NOT NULL,
	num int NOT NULL,
	Primary key(num)
);

CREATE TABLE SAHIP(
	TC varchar(12) NOT NULL,
	isim varchar(15) NOT NULL,
	soyisim varchar(15) NOT NULL,
	email_address varchar(20) UNIQUE,
	password_hash varchar(20) NOT NULL,
	Primary key(TC)
);

CREATE TABLE HAYVAN(
	hnum int NOT NULL,
	sahip_tc varchar(12) NOT NULL,
	isim varchar(15) NOT NULL,
	tur varchar(15),
	yas int,
	Primary key(hnum),
	Foreign key(sahip_tc) REFERENCES SAHIP(TC) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE BAGLIDIR(
	HekimNo varchar(12) NOT NULL,
	StajerNo varchar(12) NOT NULL,
	Foreign key(HekimNo) REFERENCES HEKIM(num) ON DELETE CASCADE ON UPDATE CASCADE,
	Foreign key(StajerNo) REFERENCES STAJER(num) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE RANDEVU(
	tarih DATE NOT NULL,
	saat varchar(5) NOT NULL,
	Hayvan_no int NOT NULL,
	Hekim_no varchar(12) NOT NULL,
	Foreign key(Hayvan_no) REFERENCES HAYVAN(hnum) ON DELETE CASCADE ON UPDATE CASCADE,
	Foreign key(Hekim_no) REFERENCES HEKIM(num) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE AMELIYAT(
	saat varchar(5),
	tarih DATE,
	Hayvan_no int NOT NULL,
	Hekim_no varchar(12) NOT NULL,
	Foreign key(Hayvan_no) REFERENCES HAYVAN(hnum) ON DELETE CASCADE ON UPDATE CASCADE,
	Foreign key(Hekim_no) REFERENCES HEKIM(num) ON DELETE CASCADE ON UPDATE CASCADE
);
