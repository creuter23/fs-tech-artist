-- phpMyAdmin SQL Dump
-- version 3.3.10.4
-- http://www.phpmyadmin.net
--
-- Host: rba.thekotsch-war.com
-- Generation Time: Jan 10, 2012 at 05:47 AM
-- Server version: 5.1.53
-- PHP Version: 5.2.17

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `rba_class`
--

-- --------------------------------------------------------

--
-- Table structure for table `Student_info`
--

CREATE TABLE IF NOT EXISTS `Student_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `studentnum` varchar(255) DEFAULT NULL,
  `classnum` int(4) DEFAULT NULL,
  `imname` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `carreergoal` varchar(255) DEFAULT NULL,
  `technical` tinyint(1) DEFAULT '0',
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=64 ;

--
-- Dumping data for table `Student_info`
--

INSERT INTO `Student_info` (`id`, `firstname`, `lastname`, `studentnum`, `classnum`, `imname`, `email`, `carreergoal`, `technical`, `time`) VALUES
(1, 'Margaret', 'Rhoads', '1322452', 1109, 'versesurfer', 'versesurfer6@msn.com', 'Compositing', 0, '2011-08-31 12:12:31'),
(2, 'Daniel', 'Berry', '1513568', 1109, 'danrburr5@me.com', 'danrburr5@yahoo.com', 'Visual Effects', 1, '2011-08-31 12:12:41'),
(3, 'Raymond', 'Rodriguez', '2109916', 1109, 'ethic1989@aol.com', 'raydiantgraphics@gmail.com', 'Visual Effects', 0, '2011-08-31 12:12:49'),
(4, 'James', 'Sasu', '1401297', 1109, 'jimhd797', 'safam007@fullsail.edu', 'Character Modeling', 0, '2011-08-31 12:12:58'),
(5, 'Darren', 'Teo', '947873', 1109, 'rebutted@gmail.com (MSN)', 'darrenteo25@gmail.com', 'Animation', 0, '2011-08-31 12:29:03'),
(6, 'Derek', 'Miller', '2044657', 1109, 'None', 'dmiller892@fullsail.edu', 'Compositing', 1, '2011-08-31 12:13:14'),
(7, 'Caris', 'Frazier', '1882776', 1109, 'fbpjaz', 'caris@fullsail.edu', 'Character Modeling', 0, '2011-08-31 12:13:22'),
(8, 'Cory', 'Beegle', '1804913', 1109, 'SharinganBeegs', 'beegs009@fullsail.edu', 'Compositing', 0, '2011-08-31 12:13:31'),
(9, 'Sara', 'Maneval', '1748498', 1109, 'luv2bannoying', 'luv2bannoying@aol.com', 'Shading and Lighting', 1, '2011-08-31 12:13:41'),
(10, 'Trevor', 'Burdine', '1139786', 1109, 'trevorburdine@me.com', 'tburd428@fullsail.edu', 'Compositing', 1, '2011-08-31 12:13:51'),
(11, 'Jacob', 'Griffith', '875592', 1109, 'jake_griffith@me.com', 'jakegriffith@yahoo.com', 'Character Modeling', 0, '2011-08-31 12:14:03'),
(12, 'Alease', 'Allen', '0001486777', 1109, 'Alease Allen', 'aleaseallen@fullsail.com', 'Environment Modeling', 0, '2011-08-31 12:14:13'),
(13, 'Jeffrey', 'De La Nuez', '1547645', 1109, 'Jeffrey De La Nuez', 'jeffreynuez@yahoo.com', 'Character Modeling', 1, '2011-08-31 12:14:23'),
(14, 'Katie', 'Plamenco', '1538101', 1109, 'KPlamenco@me.com', 'Katiexmae@fullsail.edu', 'Compositing', 0, '2011-08-31 12:14:33'),
(15, 'Daniel', 'Sanchez', '1786261', 1109, 'none', 'dansanchez@fullsail.edu', 'Rigging', 1, '2011-08-31 12:14:42'),
(16, 'Margaret', 'Rhoads', '1322452', 1110, 'versesurfer', 'versesurfer6@msn.com', 'Compositing', 0, '2011-09-26 10:13:06'),
(17, 'john', 'Saunders', '386396', 1109, 'John Saunders', 'jsaunders@fulsail.edu', 'Character Modeling', 0, '2011-09-26 10:15:23'),
(18, 'Shaina', 'Freese', '1533309', 20106, 'none', 'cannibal-crunch@live.com', 'Character Modeling', 1, '2011-09-26 10:18:32'),
(19, 'John', 'Rogeles', '1277920', 1110, 'johnrogeles', 'johnrogeles@yahoo.com', 'Character Modeling', 0, '2011-09-26 10:21:02'),
(20, 'Eva', 'Kovalainen', '1140450', 1110, 'iyaria@me.com', 'evakovalainen@fullsail.edu', 'Compositing', 0, '2011-09-26 10:22:45'),
(21, 'Elizabeth', 'Thomas', '1470014', 1110, 'none', 'edthomas@fullsail.edu', 'Animation', 0, '2011-09-26 10:24:47'),
(22, 'Elizabeth', 'Thomas', '1470014', 1110, 'none', 'edthomas@fullsail.edu', 'Animation', 0, '2011-09-26 10:24:48'),
(23, 'Linda', 'Kim', '1299095', 1110, 'bbi0bbi0@me.com', 'linda.kim92@gmail.com', 'Animation', 1, '2011-09-26 10:25:05'),
(24, 'Michael', 'Shaffer', '1231686', 1110, 'ms15004@me.com', 'ms15004@fullsail.edu', 'Character Modeling', 1, '2011-09-26 10:26:20'),
(25, 'Stephano', 'Cardona', '1192085', 1110, 'scardona92@me.com', 'stephanocardona92@Hotmail.com', 'Compositing', 0, '2011-09-26 10:26:44'),
(26, 'Shaina', 'Freese', '1533309', 1010, 'none', 'russophilia@fullsail.edu', 'Character Modeling', 0, '2011-09-26 10:27:16'),
(27, 'Dana', 'Robins', '1379597', 1109, 'none', 'dana.l.robins@gmail.com', 'Other', 0, '2011-09-26 10:28:42'),
(28, 'Michael', 'Sauer', '1263148', 1110, 'mikejcsauer', 'mikejcsauer@fullsail.edu', 'Animation', 0, '2011-09-26 10:28:44'),
(29, 'Frederick', 'Valle', '1732572', 1110, 'fvalle41@me.com', 'fov41@fullsail.edu', 'Character Modeling', 0, '2011-09-26 10:29:11'),
(30, 'austin', 'morgan', '756397', 1110, 'suntank', 'suntank@gmail.com', 'Animation', 1, '2011-09-26 10:29:43'),
(31, 'Antwan', 'Edwards', '728323', 0, 'none', 'aedwards1123@fullsail.edu', 'Shading and Lighting', 0, '2011-09-26 10:30:55'),
(32, 'Jonathan', 'Rivera', '1553795', 112, 'Jonathan Rivera', 'jrivera18@fullsail.edu', 'Other', 0, '2011-09-26 10:31:02'),
(33, 'Jonathan', 'Rivera', '1553795', 112, 'Jonathan Rivera', 'jrivera18@fullsail.edu', 'Other', 0, '2011-09-26 10:31:03'),
(34, 'Troy', 'Brown', '1695074', 1110, 'None', 'rheilyah@fullsail.edu', 'Character Modeling', 0, '2011-09-26 10:33:35'),
(35, 'Leng', 'Kue', '2105903', 0, 'none', 'lengkue@fullsail.edu', 'Environment Modeling', 1, '2011-09-26 10:33:53'),
(36, 'Noah', 'Buick', '1580315', 1110, 'CommanderWoggles', 'Archidork@me.com', 'Character Modeling', 0, '2011-09-26 10:48:49'),
(37, 'David', 'Ling', '1914979', 1110, 'DLingCadb', 'cadb@fullsail.edu', 'Character Modeling', 1, '2011-09-28 07:04:32'),
(38, 'Mark', 'Kirkland', '1108893', 1110, 'Snipermanjr', 'Ezrahalo@hotmail.com', 'Animation', 0, '2011-09-28 09:20:05'),
(39, 'Bleron', 'Mustafa', '1717862', 1111, 'bleroni888', 'bleroni888@fullsail.edu', 'Rigging', 0, '2011-10-25 14:22:23'),
(40, 'Paulina', 'Cabrera', '1259050', 1111, 'paulinacabrera', 'paulinac@fullsail.edu', 'Other', 1, '2011-10-25 14:23:01'),
(41, 'Jeffrey', 'DaSilva', '826472', 1111, 'none', 'jeffdasilva@fullsail.edu', 'Other', 1, '2011-10-25 14:23:03'),
(42, 'Bryan', 'Strongoli', '1326417', 1110, 'bahahabryan', 'brystrongoli@gmail.com', 'Character Modeling', 0, '2011-10-25 14:23:23'),
(43, 'James', 'Elswick', '1916507', 1111, 'James Elswick', 'jameselswick@fullsail.edu', 'Rigging', 1, '2011-10-25 14:23:25'),
(44, 'Matthew', 'Howell', '1946436', 1111, 'matt_howell@me.com', 'matthowell@fullsail.edu', 'Shading and Lighting', 0, '2011-10-25 14:24:27'),
(45, 'Raymond', 'Chang', '2192384', 1111, 'nismogtrr32', 'nismogtrr32@aim.com', 'Compositing', 0, '2011-10-25 14:24:34'),
(46, 'Katrell I. D.', 'Faison', '1613292', 201009, 'None', 'Rioku914@gmail.com', 'Animation', 0, '2011-10-25 14:26:37'),
(47, 'santiago', 'hoyos', '1926640', 1111, 'none', 'santiagosouth@gmail.com', 'Environment Modeling', 1, '2011-10-25 14:26:58'),
(48, 'Chris', 'Jarrett', '1538325', 11, 'Chris Jarrett', 'chrisrjarrett727@gmail.com', 'Rigging', 0, '2011-10-25 14:28:16'),
(49, 'Robert', 'Walkine', '1842917', 201110, 'None', 'robadubs@hotmail.com', 'Character Modeling', 1, '2011-10-25 14:30:01'),
(50, 'Katrell I. D.', 'Faison', '1613292', 0, 'None', 'Rioku914@gmail.com', 'Rigging', 1, '2011-10-25 14:30:11'),
(51, 'Mike', 'Jone', '2286134', 0, 'mjjones234@me.com', 'mjjones234@fullsail.edu', 'Character Modeling', 0, '2011-10-25 14:30:29'),
(52, 'Nick', 'Mastrofilippo', '940375', 1111, 'none', 'nmastro84@gmail.com', 'Environment Modeling', 1, '2011-10-25 14:30:30'),
(53, 'Christian', 'Taormina', '1213353', 1112, 'okeya45', 'taorminacj@hotmail.com', 'Animation', 0, '2011-11-21 05:58:45'),
(54, 'Jason', 'Dolan', '2017995', 1112, 'none', 'jdd110782@fullsail.edu', 'Character Modeling', 1, '2011-11-21 05:58:50'),
(55, 'Leon', 'Dinh', '0002337297', 1112, 'ce3e3m (AIM)', 'ce3e3m@fullsail.edu', 'Animation', 1, '2011-11-21 06:00:35'),
(56, 'Ashley', 'Larraga', '913593', 1112, 'none', 'Nu4Atrocious@Yahoo.com', 'Character Modeling', 0, '2011-11-21 06:03:38'),
(57, 'Casey', 'Miller', '1434577', 1112, 'none', 'clmsoccerchick@hotmail.com', 'Compositing', 0, '2011-11-21 06:03:40'),
(58, 'Katrell I.', 'Faison', '1613292', 1112, 'Rioku914', 'Rioku914@gmail.com', 'Character Modeling', 1, '2011-11-21 06:09:37'),
(59, 'Chaz', 'Holloway', '1146262', 1201, 'None', 'Stopthatapple@gmail.com', 'Compositing', 1, '2012-01-03 06:21:18'),
(60, 'emanuel', 'poitevien', '1362157', 1201, 'emanuel poitevien', 'carl.poitevien@yahoo.com', 'Visual Effects', 0, '2012-01-03 06:21:50'),
(61, 'Nicholas', 'Mckean', '0001409378', 1201, 'none', 'virtual_greed@live.com', 'Rigging', 1, '2012-01-03 06:22:57'),
(62, 'John Michael', 'Joseph', '1212527', 1201, 'none', 'jmjx@fullsail.edu', 'Rigging', 1, '2012-01-03 06:25:20'),
(63, 'Liz', 'Defilio', '914929', 1201, 'none', 'LDeFilio@fullsail.edu', 'Rigging', 0, '2012-01-04 13:55:53');
