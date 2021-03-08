-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 08, 2021 at 06:49 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `securitylogin`
--

-- --------------------------------------------------------

--
-- Table structure for table `horoscopes`
--

CREATE TABLE `horoscopes` (
  `id` int(11) NOT NULL,
  `horoscopeName` varchar(255) NOT NULL,
  `dateToday` varchar(255) NOT NULL,
  `color` varchar(255) NOT NULL,
  `compatibility` varchar(255) NOT NULL,
  `luckyNumber` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `horoscopes`
--

INSERT INTO `horoscopes` (`id`, `horoscopeName`, `dateToday`, `color`, `compatibility`, `luckyNumber`, `description`) VALUES
(1, 'AQUARIUS', 'March 8, 2021', 'Peach', 'Capricorn', '71', 'Someone from your past is checking back in with you over some shared experience or memory. It may not be through normal channels, so open yourself up to alternatives as much as you can.'),
(3, 'so', 'po', 'sd', 'cap', '1', 'somewhre'),
(12, 'des', 'March 09, 2021', 'des', 'des', 'des', 'Des'),
(13, 'aquarius', 'March 09, 2021', 'Peach', 'Capricorn', '71', 'Someone from your past is checking back in with you over some shared experience or memory. It may not be through normal channels, so open yourself up to alternatives as much as you can.'),
(14, 'aquarius', 'March 09, 2021', 'Peach', 'Capricorn', '71', 'Someone from your past is checking back in with you over some shared experience or memory. It may not be through normal channels, so open yourself up to alternatives as much as you can.');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `horoscopes`
--
ALTER TABLE `horoscopes`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `horoscopes`
--
ALTER TABLE `horoscopes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
