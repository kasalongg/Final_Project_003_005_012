/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.7.2-MariaDB, for Win64 (AMD64)
--
-- Host: 192.168.100.5    Database: sport
-- ------------------------------------------------------
-- Server version	11.8.5-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `athletes`
--

DROP TABLE IF EXISTS `athletes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `athletes` (
  `athletes_id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  PRIMARY KEY (`athletes_id`),
  KEY `fk_athletes_team` (`team_id`),
  CONSTRAINT `fk_athletes_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`)
) ENGINE=InnoDB AUTO_INCREMENT=558 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `athletes`
--

LOCK TABLES `athletes` WRITE;
/*!40000 ALTER TABLE `athletes` DISABLE KEYS */;
INSERT INTO `athletes` VALUES
(380,1,'Tony','Stark'),
(381,1,'Steve','Rogers'),
(382,1,'Bruce','Banner'),
(383,1,'Thor','Odinson'),
(384,1,'Natasha','Romanoff'),
(385,1,'Clint','Barton'),
(386,1,'Wanda','Maximoff'),
(387,1,'Vision','Synthezoid'),
(388,1,'Peter','Parker'),
(389,1,'Sam','Wilson'),
(390,1,'Bucky','Barnes'),
(391,2,'Bruce','Wayne'),
(392,2,'Clark','Kent'),
(393,2,'Diana','Prince'),
(394,2,'Barry','Allen'),
(395,2,'Arthur','Curry'),
(396,2,'Victor','Stone'),
(397,2,'Shazam','Adult'),
(398,2,'John','Stewart'),
(399,2,'Hawkgirl','Thanagar'),
(400,2,'Lex','Luthor'),
(401,2,'Cyborg','Teen'),
(402,3,'Logan','Wolverine'),
(403,3,'Charles','Xavier'),
(404,3,'Erik','Magneto'),
(405,3,'Jean','Grey'),
(406,3,'Scott','Summers'),
(407,3,'Ororo','Munroe'),
(408,3,'Hank','McCoy'),
(409,3,'Raven','Darkholme'),
(410,3,'Kurt','Wagner'),
(411,3,'Bobby','Drake'),
(412,3,'Kitty','Pryde'),
(413,4,'Peter','Quill'),
(414,4,'Gamora','Zen'),
(415,4,'Drax','Destroyer'),
(416,4,'Rocket','Raccoon'),
(417,4,'Groot','Flora'),
(418,4,'Mantis','Empath'),
(419,4,'Nebula','Blue'),
(420,4,'Yondu','Udonta'),
(421,4,'Kraglin','Obfonteri'),
(422,4,'Ego','Celestial'),
(423,4,'Star-Lord','Reborn'),
(424,5,'Frodo','Baggins'),
(425,5,'Samwise','Gamgee'),
(426,5,'Meriadoc','Brandybuck'),
(427,5,'Peregrin','Took'),
(428,5,'Bilbo','Baggins'),
(429,5,'Gollum','Smeagol'),
(430,5,'Aragorn','Elessar'),
(431,5,'Legolas','Greenleaf'),
(432,5,'Gimli','SonofGloin'),
(433,5,'Boromir','Gondor'),
(434,5,'Faramir','Gondor'),
(435,6,'Harry','Potter'),
(436,6,'Hermione','Granger'),
(437,6,'Ron','Weasley'),
(438,6,'Draco','Malfoy'),
(439,6,'Luna','Lovegood'),
(440,6,'Neville','Longbottom'),
(441,6,'Ginny','Weasley'),
(442,6,'Fred','Weasley'),
(443,6,'George','Weasley'),
(444,6,'Severus','Snape'),
(445,6,'Albus','Dumbledore'),
(446,7,'Alan','Grant'),
(447,7,'Ellie','Sattler'),
(448,7,'Ian','Malcolm'),
(449,7,'John','Hammond'),
(450,7,'Lex','Murphy'),
(451,7,'Tim','Murphy'),
(452,7,'Robert','Muldoon'),
(453,7,'Ray','Arnold'),
(454,7,'Dennis','Nedry'),
(455,7,'Henry','Wu'),
(456,7,'Claire','Dearing'),
(457,8,'Dutch','Schaefer'),
(458,8,'Dillon','Predator'),
(459,8,'Anna','Gunn'),
(460,8,'Billy','Spear'),
(461,8,'Blain','Hicks'),
(462,8,'Hawkins','Mac'),
(463,8,'Poncho','Ramirez'),
(464,8,'Mac','Weaver'),
(465,8,'Al','Lopez'),
(466,8,'Tony','Vega'),
(467,8,'Anna','Hudson'),
(468,9,'T\'Challa','BlackPanther'),
(469,9,'Shuri','T\'Challa'),
(470,9,'Okoye','DoraMilaje'),
(471,9,'Nakia','Wakanda'),
(472,9,'M\'Baku','Jabari'),
(473,9,'Everett','Ross'),
(474,9,'Ulysses','Klauw'),
(475,9,'Zuri','Shaman'),
(476,9,'Ramonda','Queen'),
(477,9,'Killmonger','Erik'),
(478,9,'Shuri','Tech'),
(479,10,'Elsa','IceQueen'),
(480,10,'Anna','Princess'),
(481,10,'Kristoff','Ice'),
(482,10,'Sven','Reindeer'),
(483,10,'Olaf','Snowman'),
(484,10,'Hans','Prince'),
(485,10,'Marshmallow','Giant'),
(486,10,'Oaken','Shopkeeper'),
(487,10,'GrandPabbie','TrollKing'),
(488,10,'Bulda','Troll'),
(489,10,'Pabbie','Troll'),
(490,11,'Jack','Sparrow'),
(491,11,'Will','Turner'),
(492,11,'Elizabeth','Swann'),
(493,11,'Hector','Barbossa'),
(494,11,'Joshamee','Gibbs'),
(495,11,'Davy','Jones'),
(496,11,'Bootstrap','Bill'),
(497,11,'Anamaria','Pirate'),
(498,11,'Pintel','Pirate'),
(499,11,'Ragetti','Pirate'),
(500,11,'Cotton','Pirate'),
(501,12,'Kevin','Minion'),
(502,12,'Stuart','Minion'),
(503,12,'Bob','Minion'),
(504,12,'Dave','Minion'),
(505,12,'Carl','Minion'),
(506,12,'Phil','Minion'),
(507,12,'Tim','Minion'),
(508,12,'Jerry','Minion'),
(509,12,'Mark','Minion'),
(510,12,'Tom','Minion'),
(511,12,'Steve','Minion'),
(512,13,'Neo','Anderson'),
(513,13,'Trinity','Matrix'),
(514,13,'Morpheus','Matrix'),
(515,13,'Cypher','Matrix'),
(516,13,'Tank','Matrix'),
(517,13,'Dozer','Matrix'),
(518,13,'Mouse','Matrix'),
(519,13,'Apoc','Matrix'),
(520,13,'Switch','Matrix'),
(521,13,'Smith','Agent'),
(522,13,'Oracle','Matrix'),
(523,14,'Godzilla','Force'),
(524,14,'Mothra','Force'),
(525,14,'Rodan','Force'),
(526,14,'KingGhidorah','Force'),
(527,14,'Mechagodzilla','Force'),
(528,14,'Anguirus','Force'),
(529,14,'JetJaguar','Force'),
(530,14,'Battra','Force'),
(531,14,'Gigan','Force'),
(532,14,'Hedorah','Force'),
(533,14,'SpaceGodzilla','Force'),
(534,15,'Optimus','Prime'),
(535,15,'Bumblebee','Auto'),
(536,15,'Megatron','Decepticon'),
(537,15,'Starscream','Decepticon'),
(538,15,'Ironhide','Auto'),
(539,15,'Ratchet','Auto'),
(540,15,'Jazz','Auto'),
(541,15,'Soundwave','Decepticon'),
(542,15,'Shockwave','Decepticon'),
(543,15,'Grimlock','Dinobot'),
(544,15,'Slag','Dinobot'),
(545,16,'Dom','Cobb'),
(546,16,'Arthur','Nash'),
(547,16,'Eames','Forger'),
(548,16,'Robert','Fischer'),
(549,16,'Mal','Cobb'),
(550,16,'Saito','Business'),
(551,16,'Yusuf','Chemist'),
(552,16,'Nash','Arthur'),
(553,16,'Fischer','Robert'),
(554,16,'Nash','Arthur2'),
(555,16,'Cobb','Dom2'),
(557,38,'Kasalong','Srirapak');
/*!40000 ALTER TABLE `athletes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leaderboard`
--

DROP TABLE IF EXISTS `leaderboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `leaderboard` (
  `leaderboard_id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL,
  `total_gold` int(11) DEFAULT NULL,
  `total_silver` varchar(100) DEFAULT NULL,
  `total_bronze` int(11) DEFAULT NULL,
  `total_score` int(11) DEFAULT NULL,
  PRIMARY KEY (`leaderboard_id`),
  KEY `fk_leaderboard_team` (`team_id`),
  CONSTRAINT `fk_leaderboard_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leaderboard`
--

LOCK TABLES `leaderboard` WRITE;
/*!40000 ALTER TABLE `leaderboard` DISABLE KEYS */;
INSERT INTO `leaderboard` VALUES
(2,1,2,'0',1,7),
(3,2,1,'1',0,5),
(4,3,0,'1',2,4),
(5,4,1,'0',1,5),
(6,1,2,'0',1,7),
(7,2,1,'1',0,5),
(8,3,0,'1',2,4),
(9,4,1,'0',1,5),
(10,1,1,'0',0,3),
(11,2,0,'1',0,2),
(12,3,0,'0',1,1),
(13,4,1,'0',0,3),
(14,5,0,'1',0,2),
(15,6,0,'0',1,1),
(16,7,1,'0',0,3),
(17,8,0,'1',0,2),
(18,9,0,'0',1,1),
(19,10,1,'0',0,3),
(20,11,0,'1',0,2),
(21,12,0,'0',1,1);
/*!40000 ALTER TABLE `leaderboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matches`
--

DROP TABLE IF EXISTS `matches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `matches` (
  `sport_id` int(11) NOT NULL,
  `team_a_id` int(11) NOT NULL,
  `team_b_id` int(11) NOT NULL,
  `match_date` varchar(100) NOT NULL,
  `match_time` varchar(100) NOT NULL,
  `match_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`match_id`),
  KEY `fk_matches_team_b` (`team_b_id`),
  CONSTRAINT `fk_matches_team_b` FOREIGN KEY (`team_b_id`) REFERENCES `teams` (`team_id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matches`
--

LOCK TABLES `matches` WRITE;
/*!40000 ALTER TABLE `matches` DISABLE KEYS */;
INSERT INTO `matches` VALUES
(1,1,2,'2026-04-01','10:00:00',67),
(1,3,4,'2026-04-01','12:00:00',68),
(1,5,6,'2026-04-02','10:00:00',69),
(1,7,8,'2026-04-02','12:00:00',70),
(1,9,10,'2026-04-03','10:00:00',71),
(1,11,12,'2026-04-03','12:00:00',72),
(1,13,14,'2026-04-04','10:00:00',73),
(1,15,16,'2026-04-04','12:00:00',74),
(2,1,3,'2026-04-05','10:00:00',75),
(2,2,4,'2026-04-05','12:00:00',76),
(2,5,7,'2026-04-06','10:00:00',77),
(2,6,8,'2026-04-06','12:00:00',78),
(2,9,11,'2026-04-07','10:00:00',79),
(2,10,12,'2026-04-07','12:00:00',80),
(2,13,15,'2026-04-08','10:00:00',81),
(2,14,16,'2026-04-08','12:00:00',82),
(3,1,4,'2026-04-09','10:00:00',83),
(3,2,3,'2026-04-09','12:00:00',84),
(3,5,8,'2026-04-10','10:00:00',85),
(3,6,7,'2026-04-10','12:00:00',86),
(3,9,12,'2026-04-11','10:00:00',87),
(3,10,11,'2026-04-11','12:00:00',88),
(3,13,16,'2026-04-12','10:00:00',89),
(3,14,15,'2026-04-12','12:00:00',90),
(4,1,5,'2026-04-13','10:00:00',91),
(4,2,6,'2026-04-13','12:00:00',92),
(4,3,7,'2026-04-14','10:00:00',93),
(4,4,8,'2026-04-14','12:00:00',94),
(4,9,13,'2026-04-15','10:00:00',95),
(4,10,14,'2026-04-15','12:00:00',96),
(4,11,15,'2026-04-16','10:00:00',97),
(4,12,16,'2026-04-16','12:00:00',98),
(10,38,5,'2026-01-11','12:00:00',100);
/*!40000 ALTER TABLE `matches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medals`
--

DROP TABLE IF EXISTS `medals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `medals` (
  `medal_id` int(11) NOT NULL AUTO_INCREMENT,
  `team_id` int(11) NOT NULL,
  `sport_id` int(11) NOT NULL,
  `gold_count` int(11) DEFAULT NULL,
  `silver_count` int(11) DEFAULT NULL,
  `bronze_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`medal_id`),
  KEY `fk_medals_sport` (`sport_id`),
  CONSTRAINT `fk_medals_sport` FOREIGN KEY (`sport_id`) REFERENCES `sports` (`sport_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medals`
--

LOCK TABLES `medals` WRITE;
/*!40000 ALTER TABLE `medals` DISABLE KEYS */;
INSERT INTO `medals` VALUES
(7,1,1,1,0,0),
(8,2,1,0,1,0),
(9,3,1,0,0,1),
(10,4,1,1,0,0),
(11,3,4,1,0,0),
(12,4,4,1,0,0),
(13,5,4,0,1,0),
(14,6,4,0,1,0),
(15,7,4,0,0,1),
(16,8,4,0,0,1),
(17,1,1,1,0,0),
(18,2,1,0,1,0),
(19,3,1,0,0,1),
(20,4,2,1,0,0),
(21,5,2,0,1,0),
(22,6,2,0,0,1),
(23,7,3,1,0,0),
(24,8,3,0,1,0),
(25,9,3,0,0,1),
(26,10,4,1,0,0),
(27,11,4,0,1,0),
(28,12,4,0,0,1),
(30,38,10,100,50,25);
/*!40000 ALTER TABLE `medals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sports`
--

DROP TABLE IF EXISTS `sports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `sports` (
  `sport_id` int(11) NOT NULL AUTO_INCREMENT,
  `sport_name` varchar(100) NOT NULL,
  PRIMARY KEY (`sport_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sports`
--

LOCK TABLES `sports` WRITE;
/*!40000 ALTER TABLE `sports` DISABLE KEYS */;
INSERT INTO `sports` VALUES
(1,'Football'),
(2,'Volleyball'),
(3,'Basketball'),
(4,'Tennis'),
(10,'running');
/*!40000 ALTER TABLE `sports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `teams` (
  `team_id` int(11) NOT NULL AUTO_INCREMENT,
  `team_name` varchar(100) NOT NULL,
  PRIMARY KEY (`team_id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams`
--

LOCK TABLES `teams` WRITE;
/*!40000 ALTER TABLE `teams` DISABLE KEYS */;
INSERT INTO `teams` VALUES
(1,'Avengers'),
(2,'Justice League'),
(3,'X-Men'),
(4,'Guardians of the Galaxy'),
(5,'Hobbits'),
(6,'Wizards of Hogwarts'),
(7,'Jurassic Squad'),
(8,'Predator Hunters'),
(9,'Black Panther Crew'),
(10,'Frozen Warriors'),
(11,'Pirates of the Caribbean'),
(12,'Minions United'),
(13,'Matrix Rebels'),
(14,'Godzilla Force'),
(15,'Transformers Team'),
(16,'Inception Dreamers'),
(38,'Kitkat');
/*!40000 ALTER TABLE `teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES
(1,'nuea','Nn123'),
(2,'ploy','Pp123'),
(3,'ken','Kk123'),
(4,'kaitom','Kk123'),
(5,'mek','Mm123'),
(6,'unda','Uu123'),
(7,'nongkun','Nn123'),
(8,'north','Nn123'),
(9,'Kasalong','Kk123');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'sport'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-03-26 14:23:23
