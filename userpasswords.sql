-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 16, 2021 at 11:08 AM
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
-- Table structure for table `userpasswords`
--

CREATE TABLE `userpasswords` (
  `id` int(11) NOT NULL,
  `userid` int(11) NOT NULL,
  `password` varchar(150) DEFAULT NULL,
  `created_at` date NOT NULL DEFAULT current_timestamp(),
  `isActive` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `userpasswords`
--

INSERT INTO `userpasswords` (`id`, `userid`, `password`, `created_at`, `isActive`) VALUES
(3, 4, 'pbkdf2:sha256:150000$e6BzEobj$b27aef2964326a778ca8873fa0d5c43937986533a945cd4b8877f8d88109a56f', '2021-02-14', 1),
(4, 5, 'pbkdf2:sha256:150000$OcgZDBKq$a977a321be61c4395a0e60eb0261e2287fba0189c77aa4b46b38403612934624', '2021-02-15', 1),
(7, 8, 'pbkdf2:sha256:150000$plLGhilp$93ae0d257f26bb39a019fced76a6fef3053007c9d7bbd4c03c6b1c089e953645', '2021-02-15', 1),
(10, 7, 'pbkdf2:sha256:150000$trxzezGQ$a078409c8e92cb374321812130d0c363fd0ae9f099e9a2bce6d120a43cd8e988', '2021-02-15', 0),
(11, 7, 'pbkdf2:sha256:150000$mNcovhrE$7d284bd4333c0193afda7d6d529fae390df9411d2e54fa62d853c2483d9b154a', '2021-02-15', 0),
(12, 7, 'pbkdf2:sha256:150000$0pTBYzzH$092d07c26bf690351089c00875f7b400657e7509f94045828f8be4b2015de96b', '2021-02-15', 0),
(13, 7, 'pbkdf2:sha256:150000$IFjicllq$3346cc403bd6ea6fdb106ceaea43fc9ad13fc59252add1a74d4560420cbb4838', '2021-02-15', 0),
(14, 7, 'pbkdf2:sha256:150000$nS9PNzQi$a1f7486070dbb09f7e29182d90ae921a12c35b020d786203781b86949e1d6ddb', '2021-02-15', 0),
(15, 7, 'pbkdf2:sha256:150000$KFi3tLJb$5247c877a9d193af63017b7acb201c124c465025c6473253267342bf3eddfbd1', '2021-02-15', 1),
(16, 9, 'pbkdf2:sha256:150000$1FfWKx2O$c014e21d6632c811fdb1412b3962e931b433bc2ac38555b8cb12310a3935b057', '2021-01-26', 1),
(18, 11, 'pbkdf2:sha256:150000$N4dDqQ07$8864a1b1d798f142af9bd684de4555fd6678f9cdcb6a7cd3efda0c0396a4024d', '2021-01-01', 0),
(19, 11, 'pbkdf2:sha256:150000$nHqK849H$c47de6ba7045e43c6b529962868cdbf6a63e20c08c09315faf4f855c01ec95e8', '2021-02-16', 1),
(20, 12, 'pbkdf2:sha256:150000$7i6cmt7i$4c53ff7fa9d84e115981e786de90cc3a6d7004dff69e3b4a115b1fbf21b8d8fc', '2021-02-16', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `userpasswords`
--
ALTER TABLE `userpasswords`
  ADD PRIMARY KEY (`id`),
  ADD KEY `userid` (`userid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `userpasswords`
--
ALTER TABLE `userpasswords`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `userpasswords`
--
ALTER TABLE `userpasswords`
  ADD CONSTRAINT `userpasswords_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
