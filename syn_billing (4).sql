-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 08, 2024 at 05:00 PM
-- Server version: 8.0.36-0ubuntu0.22.04.1
-- PHP Version: 8.1.2-1ubuntu2.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `syn_billing`
--

-- --------------------------------------------------------

--
-- Table structure for table `class`
--

CREATE TABLE `class` (
  `id` int DEFAULT NULL,
  `stu_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `md_branch`
--

CREATE TABLE `md_branch` (
  `id` int NOT NULL,
  `comp_id` int NOT NULL COMMENT 'md_company->id',
  `branch_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `branch_address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `location` int NOT NULL,
  `contact_person` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone_no` bigint DEFAULT NULL,
  `email_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_dt` datetime DEFAULT NULL,
  `modified_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modified_dt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `md_branch`
--

INSERT INTO `md_branch` (`id`, `comp_id`, `branch_name`, `branch_address`, `location`, `contact_person`, `phone_no`, `email_id`, `created_by`, `created_dt`, `modified_by`, `modified_dt`) VALUES
(1, 1, 'BARAHAT', 'Bharat,Bihar', 0, 'BARAHAT', 7369000516, 'barahat@gmail.com', 'admin', '2024-01-31 17:53:22', NULL, NULL),
(2, 2, 'Dum Dum', NULL, 4, 'Utsab', 8240378957, '', NULL, NULL, NULL, NULL),
(3, 3, 'Garia', 'Garia 5-6 bus stand', 4, 'Sayantika', 1234567890, '', NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `md_company`
--

CREATE TABLE `md_company` (
  `id` int NOT NULL,
  `company_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `location` int NOT NULL,
  `contact_person` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone_no` bigint DEFAULT NULL,
  `email_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `logo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `web_portal` enum('Y','N') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'N',
  `active_flag` enum('Y','N') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'Y',
  `created_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_dt` datetime DEFAULT NULL,
  `modified_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modified_dt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `md_company`
--

INSERT INTO `md_company` (`id`, `company_name`, `address`, `location`, `contact_person`, `phone_no`, `email_id`, `logo`, `web_portal`, `active_flag`, `created_by`, `created_dt`, `modified_by`, `modified_dt`) VALUES
(1, 'OM TRADERS', 'Ashirwad Bhawan, G. C. Banarjee Road, Bhikhanpur,Bhagalpur, Bihar- 812001', 0, 'Abhijeet', 7008893051, 'purdcsltd@gmail.com', '', 'N', 'Y', 'admin', '2024-01-31 17:50:48', NULL, NULL),
(2, 'Sunny Variety', 'Dum Dum\r\nKolkata - 700028', 4, 'Sunny', 9831887194, '', '', 'Y', 'Y', NULL, NULL, NULL, NULL),
(3, 'Sayantika tea stall', 'Garia\r\nKolkata - 700028', 4, 'Sayantika', 1234567890, '', '', 'Y', 'Y', NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `md_container`
--

CREATE TABLE `md_container` (
  `sl_no` int NOT NULL,
  `container_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `modified_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modified_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `md_header_footer`
--

CREATE TABLE `md_header_footer` (
  `comp_id` int NOT NULL,
  `header1` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `on_off_flag1` enum('Y','N') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'N',
  `header2` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `on_off_flag2` enum('Y','N') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'N',
  `footer1` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'N',
  `on_off_flag3` enum('Y','N') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'N',
  `footer2` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `on_off_flag4` enum('Y','N') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'N',
  `created_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `modified_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modified_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `md_header_footer`
--

INSERT INTO `md_header_footer` (`comp_id`, `header1`, `on_off_flag1`, `header2`, `on_off_flag2`, `footer1`, `on_off_flag3`, `footer2`, `on_off_flag4`, `created_by`, `created_at`, `modified_by`, `modified_at`) VALUES
(1, 'Welcome Back', 'Y', 'Your Receipt', 'Y', 'Thank You!', 'Y', 'Visit Again...', 'Y', 'Soumya', '2024-03-01 05:25:04', 'admin', '2024-02-02 06:35:41'),
(2, 'Welcome Shop', 'Y', 'Ganapatay Namah', 'Y', 'Hola', 'Y', 'Have a nice day!', 'Y', 'Tan', '2024-02-19 05:39:25', 'admin', '2024-02-02 06:35:41'),
(3, 'Welcome', 'Y', 'HGHG', 'Y', 'KKLMM', 'Y', 'JNKM', 'Y', 'BJHBN', '2024-02-15 04:21:22', 'admin', '2024-02-02 06:35:41');

-- --------------------------------------------------------

--
-- Table structure for table `md_items`
--

CREATE TABLE `md_items` (
  `id` bigint NOT NULL,
  `comp_id` int NOT NULL,
  `hsn_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `item_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `unit_id` int DEFAULT NULL,
  `container_id` int DEFAULT NULL,
  `created_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_dt` datetime DEFAULT NULL,
  `modified_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modified_dt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `md_items`
--

INSERT INTO `md_items` (`id`, `comp_id`, `hsn_code`, `item_name`, `description`, `unit_id`, `container_id`, `created_by`, `created_dt`, `modified_by`, `modified_dt`) VALUES
(1, 1, '18061000', 'Emami Rice Bran Oil', 'aa', 3, 0, '8910792003', '2024-01-31 17:54:00', 'Rupsa Chatterjee', '2024-03-05 16:45:33'),
(2, 1, '08041020', 'Lux Soap', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(3, 1, '18061000', 'Tata Mung Daal 500gm', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(4, 1, '18061000', 'Coca Cola 1Ltr', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(5, 1, '18061000', 'Cadbury Dairy Milk', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'Soumya', '2024-03-06 13:19:40'),
(6, 1, '18061001', 'Fortune Soya Chunks', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(7, 1, '8041021', 'Amul Chocolate Dark', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(8, 1, '18061000', 'Amul Chocolate Milk', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(9, 1, '18061000', 'Cadbury Dairy Milk Gold', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(10, 1, '18061000', 'Sprite 700ml', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(11, 1, '18061002', 'Amul Chocolate Peanut', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(12, 1, '8041022', 'Amul Milk', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(13, 1, '18061000', 'Modern Bread', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(14, 1, '18061000', 'Britania Thin', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(15, 1, '18061000', 'Gooday biscuits', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(16, 1, '18061003', 'Bapuji Cakes', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(17, 2, '18061000', 'Emami Rice Bran Oil-500L', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(18, 2, '08041020', 'Lux Soap', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(19, 2, '18061000', 'Tata Mung Daal 1kg', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(20, 2, '18061000', 'Diet Coca Cola 1Ltr', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(21, 2, '18061000', 'Cadbury Dairy Milk 40rs', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(22, 2, '18061001', 'Fortune Soya Chunks', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(23, 2, '8041021', 'Amul Chocolate Dark', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(24, 2, '18061000', 'Amul Chocolate Milk', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(25, 2, '18061000', 'Cadbury Dairy Milk Gold', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(26, 2, '18061000', 'Sprite 1ltr', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(27, 2, '18061002', 'Amul Chocolate Peanut', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(28, 2, '8041022', 'Amul Milk', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(29, 2, '18061000', 'Modern Bread-small', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(30, 2, '18061000', 'Britania Thin', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(31, 2, '18061000', 'Gooday biscuits', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(32, 2, '18061003', 'Bapuji Cakes', 'aa', 0, 0, '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(39, 1, '12345678', 'Salt', NULL, 0, NULL, '8910792003', '2024-02-23 12:43:03', NULL, NULL),
(40, 2, '12345677', 'Sugar', NULL, 0, NULL, '8910792003', '2024-02-23 12:50:14', NULL, NULL),
(41, 1, '1213214', 'Rooh Afza 1L', NULL, 0, NULL, '8910792003', '2024-02-23 12:54:13', NULL, NULL),
(42, 1, '1213214', 'Rooh Afza 1L', NULL, 0, NULL, '8910792003', '2024-02-23 13:43:56', NULL, NULL),
(43, 1, '1213214', 'Rooh Afza 1L', NULL, 0, NULL, '8910792003', '2024-02-23 13:44:04', NULL, NULL),
(44, 1, '1324565', 'gbhfghfghfg', NULL, 0, NULL, '8910792003', '2024-02-23 14:57:18', NULL, NULL),
(45, 1, '134566', 'Lays Sizzling Hot 40gm', NULL, 0, NULL, '8910792003', '2024-02-23 15:38:47', NULL, NULL),
(46, 1, '123456', 'Kaveri Gulab Jal 700ml', NULL, 0, NULL, '8910792003', '2024-02-26 15:37:59', NULL, NULL),
(47, 1, '15804', 'Chings Catchup 250ml', NULL, 0, NULL, '8910792003', '2024-02-29 16:56:53', NULL, NULL),
(48, 1, '90000', 'Dabur Honey', NULL, 4, NULL, '8910792003', '2024-03-05 15:30:17', NULL, NULL),
(49, 1, '10001', 'Paper Roll 2', NULL, 5, NULL, '8910792003', '2024-03-05 15:47:30', 'Soumya', '2024-03-05 16:54:13'),
(50, 1, '11111111', 'Kurkure Red 40', NULL, 5, NULL, '8910792003', '2024-03-05 16:56:02', NULL, NULL),
(51, 1, '0001121', 'Keventers Milk 500ml', NULL, 4, NULL, '8910792003', '2024-03-06 13:04:26', NULL, NULL),
(52, 1, '126484', 'Dairy Milk Silk', NULL, 4, NULL, '8910792003', '2024-03-06 13:27:29', 'Soumya', '2024-03-06 13:29:33'),
(54, 1, '1101010', 'Frooti 200ml', NULL, 5, NULL, '8910792003', '2024-03-07 17:38:47', NULL, NULL),
(55, 1, '800807', 'Corn Flakes', NULL, 4, NULL, '8910792003', '2024-03-07 17:47:07', NULL, NULL),
(56, 1, '548000', 'Go Cheese 🧀', NULL, 5, NULL, '8910792003', '2024-03-07 17:49:15', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `md_item_rate`
--

CREATE TABLE `md_item_rate` (
  `id` bigint NOT NULL,
  `item_id` bigint NOT NULL,
  `price` decimal(10,2) NOT NULL DEFAULT '0.00',
  `discount` decimal(10,2) NOT NULL DEFAULT '0.00',
  `cgst` decimal(10,2) NOT NULL DEFAULT '0.00',
  `sgst` decimal(10,2) NOT NULL DEFAULT '0.00',
  `created_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_dt` datetime DEFAULT NULL,
  `modified_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modified_dt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `md_item_rate`
--

INSERT INTO `md_item_rate` (`id`, `item_id`, `price`, `discount`, `cgst`, `sgst`, `created_by`, `created_dt`, `modified_by`, `modified_dt`) VALUES
(1, 1, '323.00', '0.00', '0.00', '0.00', '8910792003', '2024-01-31 17:54:00', 'Rupsa Chatterjee', '2024-03-05 16:45:33'),
(2, 2, '10.85', '0.00', '5.00', '5.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(3, 3, '89.00', '5.00', '5.00', '5.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(4, 4, '55.74', '2.00', '5.00', '5.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(5, 5, '150.00', '0.00', '0.00', '0.00', '8910792003', '2024-01-31 17:54:00', 'Soumya', '2024-03-06 13:19:40'),
(6, 6, '98.54', '1.00', '12.00', '12.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(7, 7, '10.00', '0.00', '12.00', '12.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(8, 8, '22.00', '0.00', '12.00', '12.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(9, 9, '45.46', '0.00', '12.00', '12.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(10, 10, '30.00', '0.00', '5.00', '5.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(11, 11, '50.00', '0.25', '5.00', '5.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(12, 12, '29.00', '0.00', '5.00', '5.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(13, 13, '48.71', '0.50', '5.00', '5.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(14, 14, '60.00', '0.00', '28.00', '28.00', '8910792003', '2024-01-31 17:54:00', 'Soumya', '2024-02-28 17:21:13'),
(15, 15, '5.00', '0.00', '18.00', '18.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(16, 16, '10.00', '0.00', '12.00', '12.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(17, 17, '50.00', '0.00', '5.00', '5.00', '8910792003', '2024-01-31 17:54:00', 'Tan', '2024-02-19 16:39:45'),
(18, 18, '10.85', '0.00', '5.00', '5.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(19, 19, '89.00', '5.00', '5.00', '5.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(20, 20, '55.74', '2.00', '5.00', '5.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(21, 21, '20.00', '0.00', '5.00', '5.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(22, 22, '98.54', '1.00', '12.00', '12.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(23, 23, '10.00', '0.00', '12.00', '12.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(24, 24, '22.00', '0.00', '12.00', '12.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(25, 25, '45.46', '0.00', '12.00', '12.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(26, 26, '30.00', '0.00', '5.00', '5.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(27, 27, '50.00', '0.25', '5.00', '5.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(28, 28, '29.00', '0.00', '5.00', '5.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(29, 29, '48.71', '0.50', '5.00', '5.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(30, 30, '52.00', '0.00', '28.00', '28.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(31, 31, '5.00', '0.00', '18.00', '18.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(32, 32, '10.00', '0.00', '12.00', '12.00', '8910792003', '2024-01-31 17:54:00', 'admin', '2024-01-31 17:54:00'),
(36, 39, '100.00', '10.00', '3.00', '3.00', '8910792003', '2024-02-23 12:43:03', NULL, NULL),
(37, 40, '150.00', '15.00', '5.00', '5.00', '8910792003', '2024-02-23 12:50:14', NULL, NULL),
(38, 41, '150.00', '5.00', '18.00', '18.00', '8910792003', '2024-02-23 12:54:13', 'Soumya', '2024-02-23 12:55:40'),
(39, 42, '120.00', '0.00', '5.00', '5.00', '8910792003', '2024-02-23 13:43:56', NULL, NULL),
(40, 43, '120.00', '0.00', '5.00', '5.00', '8910792003', '2024-02-23 13:44:04', NULL, NULL),
(41, 44, '123.00', '2.00', '5.00', '5.00', '8910792003', '2024-02-23 14:57:18', NULL, NULL),
(42, 45, '60.00', '10.00', '18.00', '18.00', '8910792003', '2024-02-23 15:38:47', 'Soumya', '2024-02-23 15:53:34'),
(43, 46, '150.00', '20.00', '5.00', '5.00', '8910792003', '2024-02-26 15:37:59', 'Soumya', '2024-02-26 15:46:23'),
(44, 47, '140.00', '0.00', '0.00', '0.00', '8910792003', '2024-02-29 16:56:53', NULL, NULL),
(45, 48, '250.00', '0.00', '0.00', '0.00', '8910792003', '2024-03-05 15:30:17', NULL, NULL),
(46, 49, '200.00', '10.00', '18.00', '18.00', '8910792003', '2024-03-05 15:47:30', 'Soumya', '2024-03-05 16:54:13'),
(47, 50, '200.00', '5.00', '5.00', '5.00', '8910792003', '2024-03-05 16:56:02', NULL, NULL),
(48, 51, '250.00', '0.00', '0.00', '0.00', '8910792003', '2024-03-06 13:04:26', NULL, NULL),
(49, 52, '200.00', '0.00', '0.00', '0.00', '8910792003', '2024-03-06 13:27:29', 'Soumya', '2024-03-06 13:29:33'),
(51, 54, '20.00', '0.00', '0.00', '0.00', '8910792003', '2024-03-07 17:38:47', NULL, NULL),
(52, 55, '200.00', '0.00', '0.00', '0.00', '8910792003', '2024-03-07 17:47:07', NULL, NULL),
(53, 56, '140.00', '0.00', '0.00', '0.00', '8910792003', '2024-03-07 17:49:15', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `md_location`
--

CREATE TABLE `md_location` (
  `sl_no` int NOT NULL,
  `location_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `modified_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modified_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `md_location`
--

INSERT INTO `md_location` (`sl_no`, `location_name`, `created_by`, `created_at`, `modified_by`, `modified_at`) VALUES
(1, 'Bhubhaneshwar', NULL, NULL, NULL, NULL),
(2, 'Puri', NULL, NULL, NULL, NULL),
(3, 'Cuttack', NULL, NULL, NULL, NULL),
(4, 'Kolkata', NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `md_receipt_settings`
--

CREATE TABLE `md_receipt_settings` (
  `comp_id` int NOT NULL,
  `rcpt_type` enum('P','S','B') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `gst_flag` enum('Y','N') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'N',
  `unit_flag` enum('Y','N') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'N',
  `cust_inf` enum('Y','N') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'N',
  `pay_mode` enum('Y','N') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'N',
  `discount_flag` enum('Y','N') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'Y',
  `stock_flag` enum('Y','N') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'Y',
  `discount_type` enum('P','A') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'P->Percent\r\nA->Amount',
  `price_type` enum('A','M') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'A' COMMENT 'A->Auto,M->Manual',
  `created_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `modified_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modified_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `md_receipt_settings`
--

INSERT INTO `md_receipt_settings` (`comp_id`, `rcpt_type`, `gst_flag`, `unit_flag`, `cust_inf`, `pay_mode`, `discount_flag`, `stock_flag`, `discount_type`, `price_type`, `created_by`, `created_at`, `modified_by`, `modified_at`) VALUES
(1, 'P', 'Y', 'Y', 'Y', 'Y', 'Y', 'N', 'P', 'A', 'Soumya', '2024-02-02 00:17:42', 'Soumya', '2024-03-08 05:16:30'),
(2, 'P', 'Y', 'N', 'Y', 'Y', 'Y', 'Y', 'A', 'A', 'Sayantika', '2024-02-02 00:54:52', 'Sayantika', '2024-02-22 12:12:04'),
(3, 'B', 'Y', 'N', 'Y', 'Y', 'Y', 'Y', 'P', 'A', 'admin', '2024-02-02 00:54:52', 'admin', '2024-02-02 00:54:58');

-- --------------------------------------------------------

--
-- Table structure for table `md_unit`
--

CREATE TABLE `md_unit` (
  `sl_no` int NOT NULL,
  `comp_id` int DEFAULT NULL,
  `unit_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `modified_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modified_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `md_unit`
--

INSERT INTO `md_unit` (`sl_no`, `comp_id`, `unit_name`, `created_by`, `created_at`, `modified_by`, `modified_at`) VALUES
(1, 1, 'Kg', 'Soumya', '2024-03-05 10:14:53', NULL, NULL),
(2, 1, 'G', 'Soumya', '2024-03-05 10:14:58', NULL, NULL),
(3, 1, 'Lt', 'Soumya', '2024-03-05 10:15:05', 'Soumya', '2024-03-06 05:57:11'),
(4, 1, 'Pc', 'Soumya', '2024-03-05 10:15:20', NULL, NULL),
(5, 1, 'Pkt', 'Soumya', '2024-03-05 10:15:32', NULL, NULL),
(6, 1, 'Mt', 'Soumya', '2024-03-05 10:15:53', NULL, NULL),
(7, 1, 'Cm', 'Soumya', '2024-03-05 10:15:57', NULL, NULL),
(8, 1, 'Ml', 'Soumya', '2024-03-06 05:49:08', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `md_user`
--

CREATE TABLE `md_user` (
  `id` int NOT NULL,
  `comp_id` int NOT NULL COMMENT 'md_company -> id',
  `br_id` int NOT NULL COMMENT 'md_branch -> id',
  `user_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `user_type` enum('A','U','M') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'U' COMMENT 'A-> Admin, U-> User',
  `user_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `phone_no` bigint NOT NULL,
  `email_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `device_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `active_flag` enum('Y','N') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'Y',
  `created_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_dt` datetime DEFAULT NULL,
  `modified_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modified_dt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `md_user`
--

INSERT INTO `md_user` (`id`, `comp_id`, `br_id`, `user_name`, `user_type`, `user_id`, `phone_no`, `email_id`, `device_id`, `password`, `active_flag`, `created_by`, `created_dt`, `modified_by`, `modified_dt`) VALUES
(1, 2, 2, 'Sayantika', 'M', '6295825458', 6295825458, 'san@mail.com', '954', '$2b$12$s2e7EHu/FMPiHDk8R5wSsONFvnmEQHCYOiDySIrrlWm5ba7k99xOm', 'Y', 'Sayantika', '2024-02-01 10:56:34', NULL, NULL),
(5, 1, 1, 'Soumya', 'M', '8910792003', 8910792003, 'san1@mail.com', '9540', '$2b$12$N8i5EnxN.byXzoZINrKMrOw5HKDHt5D86BXusl4yGdnX5QNoWAJsS', 'Y', 'Sayantika', '2024-02-01 10:56:34', NULL, NULL),
(6, 1, 0, 'Tanmoy', 'A', '9831887194', 9831887194, 'mondal.tanmoy@synergicsoftek.com', '0', '1234', 'Y', 'Sayantika', '2024-02-01 10:56:34', NULL, NULL),
(10, 1, 1, 'Tan', 'M', '8240378957', 8240378957, 'san@mail.com', '954', '$2b$12$9J.cA/q5pbOFz3cK26D3X.z6tsGrKYSYshJEk3cDhcDpHr0zI4tZW', 'Y', 'Sayantika', '2024-02-01 10:56:34', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `md_version`
--

CREATE TABLE `md_version` (
  `sl_no` int NOT NULL,
  `version_no` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `url` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `md_version`
--

INSERT INTO `md_version` (`sl_no`, `version_no`, `url`) VALUES
(1, '1.1', 'https://www.google.com/');

-- --------------------------------------------------------

--
-- Table structure for table `td_item_purchase`
--

CREATE TABLE `td_item_purchase` (
  `id` bigint NOT NULL,
  `comp_id` int NOT NULL,
  `br_id` int NOT NULL,
  `receipt_no` int NOT NULL,
  `item_id` bigint NOT NULL,
  `tnx_date` date NOT NULL,
  `price` float(10,2) NOT NULL DEFAULT '0.00',
  `qty` int NOT NULL DEFAULT '0',
  `created_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_dt` datetime DEFAULT NULL,
  `modified_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modified_dt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `td_item_sale`
--

CREATE TABLE `td_item_sale` (
  `receipt_no` bigint NOT NULL,
  `comp_id` int NOT NULL,
  `br_id` int NOT NULL,
  `item_id` bigint NOT NULL,
  `trn_date` date NOT NULL,
  `price` decimal(10,2) NOT NULL DEFAULT '0.00',
  `dis_pertg` decimal(10,2) NOT NULL DEFAULT '0.00',
  `discount_amt` decimal(10,2) NOT NULL DEFAULT '0.00',
  `cgst_prtg` decimal(10,2) NOT NULL DEFAULT '0.00',
  `cgst_amt` decimal(10,2) NOT NULL DEFAULT '0.00',
  `sgst_prtg` decimal(10,2) NOT NULL DEFAULT '0.00',
  `sgst_amt` decimal(10,2) NOT NULL DEFAULT '0.00',
  `qty` int NOT NULL DEFAULT '0',
  `created_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_dt` datetime DEFAULT NULL,
  `modified_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modified_dt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `td_item_sale`
--

INSERT INTO `td_item_sale` (`receipt_no`, `comp_id`, `br_id`, `item_id`, `trn_date`, `price`, `dis_pertg`, `discount_amt`, `cgst_prtg`, `cgst_amt`, `sgst_prtg`, `sgst_amt`, `qty`, `created_by`, `created_dt`, `modified_by`, `modified_dt`) VALUES
(1707982491, 1, 1, 1, '2024-02-15', '100.00', '10.00', '10.00', '5.00', '5.00', '5.00', '5.00', 1, '8910792003', '2024-02-15 13:04:51', NULL, NULL),
(1707982491, 1, 1, 3, '2024-02-15', '89.00', '5.00', '4.45', '5.00', '4.45', '5.00', '4.45', 1, '8910792003', '2024-02-15 13:04:51', NULL, NULL),
(1707982491, 1, 1, 7, '2024-02-15', '10.00', '0.00', '0.00', '12.00', '1.20', '12.00', '1.20', 1, '8910792003', '2024-02-15 13:04:51', NULL, NULL),
(1708080999, 1, 1, 1, '2024-02-16', '200.00', '20.00', '40.00', '12.00', '24.00', '12.00', '24.00', 1, '8910792003', '2024-02-16 16:26:39', NULL, NULL),
(1708081018, 1, 1, 11, '2024-02-16', '50.00', '0.25', '0.13', '5.00', '2.50', '5.00', '2.50', 1, '8910792003', '2024-02-16 16:26:57', NULL, NULL),
(1708318748, 1, 1, 1, '2024-02-19', '200.00', '20.00', '40.00', '12.00', '24.00', '12.00', '24.00', 1, '8910792003', '2024-02-19 10:29:07', NULL, NULL),
(1708321727, 1, 1, 1, '2024-02-19', '200.00', '20.00', '200.00', '12.00', '120.00', '12.00', '120.00', 5, '8910792003', '2024-02-19 11:18:47', NULL, NULL),
(1708321727, 1, 1, 7, '2024-02-19', '10.00', '0.00', '0.00', '12.00', '1.20', '12.00', '1.20', 1, '8910792003', '2024-02-19 11:18:47', NULL, NULL),
(1708321727, 1, 1, 11, '2024-02-19', '50.00', '0.25', '0.25', '5.00', '5.00', '5.00', '5.00', 2, '8910792003', '2024-02-19 11:18:47', NULL, NULL),
(1708321755, 1, 1, 3, '2024-02-19', '89.00', '5.00', '4.45', '5.00', '4.45', '5.00', '4.45', 1, '8910792003', '2024-02-19 11:19:14', NULL, NULL),
(1708325680, 1, 1, 11, '2024-02-19', '50.00', '0.25', '0.13', '5.00', '2.50', '5.00', '2.50', 1, '8910792003', '2024-02-19 12:24:39', NULL, NULL),
(1708340832, 2, 2, 17, '2024-02-19', '100.00', '0.00', '0.00', '5.00', '5.00', '5.00', '5.00', 1, '8240378957', '2024-02-19 16:37:12', NULL, NULL),
(1708340832, 2, 2, 18, '2024-02-19', '10.85', '0.00', '0.00', '5.00', '1.09', '5.00', '1.09', 2, '8240378957', '2024-02-19 16:37:12', NULL, NULL),
(1708340832, 2, 2, 27, '2024-02-19', '50.00', '0.25', '0.13', '5.00', '2.50', '5.00', '2.50', 1, '8240378957', '2024-02-19 16:37:12', NULL, NULL),
(1708502138, 1, 1, 1, '2024-02-21', '200.00', '20.00', '40.00', '12.00', '24.00', '12.00', '24.00', 1, '8910792003', '2024-02-21 13:25:38', NULL, NULL),
(1708502138, 1, 1, 4, '2024-02-21', '55.74', '2.00', '2.23', '5.00', '5.57', '5.00', '5.57', 2, '8910792003', '2024-02-21 13:25:38', NULL, NULL),
(1708510305, 1, 1, 14, '2024-02-21', '52.00', '0.00', '0.00', '28.00', '14.56', '28.00', '14.56', 1, '8910792003', '2024-02-21 15:41:45', NULL, NULL),
(1708510593, 1, 1, 11, '2024-02-21', '50.00', '0.25', '0.13', '5.00', '2.50', '5.00', '2.50', 1, '8910792003', '2024-02-21 15:46:33', NULL, NULL),
(1708511825, 1, 1, 4, '2024-02-21', '55.74', '2.00', '1.11', '5.00', '2.79', '5.00', '2.79', 1, '8910792003', '2024-02-21 16:07:04', NULL, NULL),
(1708511825, 1, 1, 14, '2024-02-21', '52.00', '0.00', '0.00', '28.00', '29.12', '28.00', '29.12', 2, '8910792003', '2024-02-21 16:07:04', NULL, NULL),
(1708511858, 1, 1, 5, '2024-02-21', '20.00', '0.00', '0.00', '5.00', '4.00', '5.00', '4.00', 4, '8910792003', '2024-02-21 16:07:37', NULL, NULL),
(1708511858, 1, 1, 6, '2024-02-21', '98.54', '1.00', '1.97', '12.00', '23.65', '12.00', '23.65', 2, '8910792003', '2024-02-21 16:07:37', NULL, NULL),
(1708513751, 1, 1, 2, '2024-02-21', '10.85', '0.00', '0.00', '5.00', '0.54', '5.00', '0.54', 1, '8910792003', '2024-02-21 16:39:10', NULL, NULL),
(1708513779, 1, 1, 3, '2024-02-21', '89.00', '5.00', '8.90', '0.00', '0.00', '0.00', '0.00', 2, '8910792003', '2024-02-21 16:39:38', NULL, NULL),
(1708513811, 1, 1, 7, '2024-02-21', '10.00', '0.00', '0.00', '12.00', '2.40', '12.00', '2.40', 2, '8910792003', '2024-02-21 16:40:10', NULL, NULL),
(1708596612, 1, 1, 11, '2024-02-22', '50.00', '23.00', '23.00', '5.00', '5.00', '5.00', '5.00', 2, '8910792003', '2024-02-22 15:40:11', NULL, NULL),
(1708596899, 1, 1, 4, '2024-02-22', '55.74', '2.00', '1.11', '5.00', '2.79', '5.00', '2.79', 1, '8910792003', '2024-02-22 15:44:58', NULL, NULL),
(1708596899, 1, 1, 6, '2024-02-22', '98.54', '3.00', '2.96', '12.00', '11.82', '12.00', '11.82', 1, '8910792003', '2024-02-22 15:44:58', NULL, NULL),
(1708597154, 1, 1, 11, '2024-02-22', '50.00', '0.25', '0.25', '5.00', '5.00', '5.00', '5.00', 2, '8910792003', '2024-02-22 15:49:13', NULL, NULL),
(1708597230, 1, 1, 1, '2024-02-22', '150.00', '5.00', '7.50', '18.00', '27.00', '18.00', '27.00', 1, '8910792003', '2024-02-22 15:50:30', NULL, NULL),
(1708597582, 1, 1, 2, '2024-02-22', '10.85', '0.00', '0.00', '5.00', '0.54', '5.00', '0.54', 1, '8910792003', '2024-02-22 15:56:22', NULL, NULL),
(1708597836, 1, 1, 2, '2024-02-22', '10.85', '0.00', '0.00', '5.00', '0.54', '5.00', '0.54', 1, '8910792003', '2024-02-22 16:00:35', NULL, NULL),
(1708598416, 1, 1, 2, '2024-02-22', '10.85', '0.00', '0.00', '5.00', '1.09', '5.00', '1.09', 2, '8910792003', '2024-02-22 16:10:15', NULL, NULL),
(1708598416, 1, 1, 6, '2024-02-22', '98.54', '90.00', '177.37', '12.00', '23.65', '12.00', '23.65', 2, '8910792003', '2024-02-22 16:10:15', NULL, NULL),
(1708598749, 1, 1, 6, '2024-02-22', '98.54', '1.00', '492.70', '12.00', '5912.40', '12.00', '5912.40', 500, '8910792003', '2024-02-22 16:15:49', NULL, NULL),
(1708598749, 1, 1, 11, '2024-02-22', '50.00', '0.25', '112.50', '5.00', '2250.00', '5.00', '2250.00', 900, '8910792003', '2024-02-22 16:15:49', NULL, NULL),
(1708603021, 1, 1, 1, '2024-02-22', '150.00', '0.00', '5.00', '18.00', '27.00', '18.00', '27.00', 1, '8910792003', '2024-02-22 17:27:00', NULL, NULL),
(1708603021, 1, 1, 3, '2024-02-22', '89.00', '0.00', '5.00', '5.00', '4.45', '5.00', '4.45', 1, '8910792003', '2024-02-22 17:27:00', NULL, NULL),
(1708603021, 1, 1, 6, '2024-02-22', '98.54', '0.00', '1.00', '12.00', '23.65', '12.00', '23.65', 2, '8910792003', '2024-02-22 17:27:00', NULL, NULL),
(1708603021, 1, 1, 11, '2024-02-22', '50.00', '0.00', '0.25', '5.00', '5.00', '5.00', '5.00', 2, '8910792003', '2024-02-22 17:27:00', NULL, NULL),
(1708603021, 1, 1, 12, '2024-02-22', '29.00', '0.00', '0.00', '5.00', '1.45', '5.00', '1.45', 1, '8910792003', '2024-02-22 17:27:00', NULL, NULL),
(1708603437, 2, 2, 17, '2024-02-22', '50.00', '0.00', '0.00', '5.00', '2.50', '5.00', '2.50', 1, '6295825458', '2024-02-22 17:33:57', NULL, NULL),
(1708603437, 2, 2, 22, '2024-02-22', '98.54', '0.00', '1.00', '12.00', '236.50', '12.00', '236.50', 20, '6295825458', '2024-02-22 17:33:57', NULL, NULL),
(1708603765, 2, 2, 19, '2024-02-22', '89.00', '0.00', '5.00', '0.00', '0.00', '0.00', '0.00', 21, '6295825458', '2024-02-22 17:39:24', NULL, NULL),
(1708672060, 1, 1, 4, '2024-02-23', '55.74', '2.00', '1.11', '5.00', '2.79', '5.00', '2.79', 1, '8910792003', '2024-02-23 12:37:39', NULL, NULL),
(1708672060, 1, 1, 6, '2024-02-23', '98.54', '20.00', '98.54', '12.00', '59.12', '12.00', '59.12', 5, '8910792003', '2024-02-23 12:37:39', NULL, NULL),
(1708672060, 1, 1, 11, '2024-02-23', '50.00', '0.25', '0.13', '5.00', '2.50', '5.00', '2.50', 1, '8910792003', '2024-02-23 12:37:39', NULL, NULL),
(1708684020, 1, 1, 45, '2024-02-23', '60.00', '5.00', '6.00', '18.00', '21.60', '18.00', '21.60', 2, '8910792003', '2024-02-23 15:56:59', NULL, NULL),
(1708950410, 1, 1, 1, '2024-02-26', '165.00', '0.00', '5.00', '0.00', '29.70', '0.00', '29.70', 1, '8910792003', '2024-02-26 17:56:50', NULL, NULL),
(1708950410, 1, 1, 3, '2024-02-26', '89.00', '0.00', '5.00', '0.00', '4.45', '0.00', '4.45', 1, '8910792003', '2024-02-26 17:56:50', NULL, NULL),
(1708950410, 1, 1, 11, '2024-02-26', '50.00', '0.00', '0.25', '0.00', '5.00', '0.00', '5.00', 2, '8910792003', '2024-02-26 17:56:50', NULL, NULL),
(1708950614, 1, 1, 3, '2024-02-26', '89.00', '0.00', '5.00', '0.00', '4.45', '0.00', '4.45', 1, '8910792003', '2024-02-26 18:00:14', NULL, NULL),
(1708950614, 1, 1, 4, '2024-02-26', '55.74', '0.00', '2.00', '0.00', '2.79', '0.00', '2.79', 1, '8910792003', '2024-02-26 18:00:14', NULL, NULL),
(1708950614, 1, 1, 6, '2024-02-26', '98.54', '0.00', '1.00', '0.00', '11.82', '0.00', '11.82', 1, '8910792003', '2024-02-26 18:00:14', NULL, NULL),
(1708950614, 1, 1, 8, '2024-02-26', '22.00', '0.00', '0.00', '0.00', '2.64', '0.00', '2.64', 1, '8910792003', '2024-02-26 18:00:14', NULL, NULL),
(1708951194, 1, 1, 1, '2024-02-26', '165.00', '5.00', '8.25', '18.00', '29.70', '18.00', '29.70', 1, '8910792003', '2024-02-26 18:09:53', NULL, NULL),
(1708951194, 1, 1, 11, '2024-02-26', '50.00', '0.25', '0.13', '5.00', '2.50', '5.00', '2.50', 1, '8910792003', '2024-02-26 18:09:53', NULL, NULL),
(1708951194, 1, 1, 46, '2024-02-26', '150.00', '20.00', '30.00', '5.00', '7.50', '5.00', '7.50', 1, '8910792003', '2024-02-26 18:09:53', NULL, NULL),
(1709010412, 1, 1, 1, '2024-02-27', '165.00', '5.00', '16.50', '18.00', '59.40', '18.00', '59.40', 2, '8910792003', '2024-02-27 10:36:52', NULL, NULL),
(1709010412, 1, 1, 2, '2024-02-27', '10.85', '0.00', '0.00', '5.00', '0.54', '5.00', '0.54', 1, '8910792003', '2024-02-27 10:36:52', NULL, NULL),
(1709010412, 1, 1, 46, '2024-02-27', '150.00', '20.00', '30.00', '5.00', '7.50', '5.00', '7.50', 1, '8910792003', '2024-02-27 10:36:52', NULL, NULL),
(1709014348, 1, 1, 13, '2024-02-27', '48.71', '0.50', '0.24', '5.00', '2.44', '5.00', '2.44', 1, '8910792003', '2024-02-27 11:42:28', NULL, NULL),
(1709014348, 1, 1, 15, '2024-02-27', '5.00', '0.00', '0.00', '18.00', '0.90', '18.00', '0.90', 1, '8910792003', '2024-02-27 11:42:28', NULL, NULL),
(1709028630, 1, 1, 1, '2024-02-27', '165.00', '0.00', '5.00', '0.00', '0.00', '0.00', '0.00', 2, '8910792003', '2024-02-27 15:40:29', NULL, NULL),
(1709028630, 1, 1, 2, '2024-02-27', '10.85', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', 1, '8910792003', '2024-02-27 15:40:29', NULL, NULL),
(1709028630, 1, 1, 4, '2024-02-27', '55.74', '0.00', '2.00', '0.00', '0.00', '0.00', '0.00', 1, '8910792003', '2024-02-27 15:40:29', NULL, NULL),
(1709120855, 1, 1, 1, '2024-02-28', '165.00', '5.00', '8.25', '18.00', '29.70', '18.00', '29.70', 1, '8910792003', '2024-02-28 17:17:34', NULL, NULL),
(1709120855, 1, 1, 14, '2024-02-28', '52.00', '10.00', '10.40', '28.00', '29.12', '28.00', '29.12', 2, '8910792003', '2024-02-28 17:17:34', NULL, NULL),
(1709121628, 1, 1, 3, '2024-02-28', '89.00', '5.00', '4.45', '0.00', '0.00', '0.00', '0.00', 1, '8910792003', '2024-02-28 17:30:27', NULL, NULL),
(1709121628, 1, 1, 41, '2024-02-28', '150.00', '5.00', '7.50', '0.00', '0.00', '0.00', '0.00', 1, '8910792003', '2024-02-28 17:30:27', NULL, NULL),
(1709184595, 1, 1, 1, '2024-02-29', '165.00', '5.00', '8.25', '0.00', '0.00', '0.00', '0.00', 1, '8910792003', '2024-02-29 10:59:55', NULL, NULL),
(1709205718, 1, 1, 16, '2024-02-29', '14.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', 2, '8910792003', '2024-02-29 16:51:58', NULL, NULL),
(1709272394, 1, 1, 3, '2024-03-01', '89.00', '5.00', '4.45', '5.00', '4.45', '5.00', '4.45', 1, '8910792003', '2024-03-01 11:23:13', NULL, NULL),
(1709272394, 1, 1, 6, '2024-03-01', '98.54', '1.00', '0.99', '12.00', '11.82', '12.00', '11.82', 1, '8910792003', '2024-03-01 11:23:13', NULL, NULL),
(1709272394, 1, 1, 11, '2024-03-01', '50.00', '0.50', '0.50', '5.00', '5.00', '5.00', '5.00', 2, '8910792003', '2024-03-01 11:23:13', NULL, NULL),
(1709272394, 1, 1, 13, '2024-03-01', '48.71', '0.50', '0.24', '5.00', '2.44', '5.00', '2.44', 1, '8910792003', '2024-03-01 11:23:13', NULL, NULL),
(1709272394, 1, 1, 14, '2024-03-01', '60.00', '0.00', '0.00', '28.00', '16.80', '28.00', '16.80', 1, '8910792003', '2024-03-01 11:23:13', NULL, NULL),
(1709272394, 1, 1, 46, '2024-03-01', '150.00', '20.00', '30.00', '5.00', '7.50', '5.00', '7.50', 1, '8910792003', '2024-03-01 11:23:13', NULL, NULL),
(1709531784, 1, 1, 4, '2024-03-04', '55.74', '2.00', '2.23', '5.00', '5.57', '5.00', '5.57', 2, '8910792003', '2024-03-04 11:26:23', NULL, NULL),
(1709531784, 1, 1, 13, '2024-03-04', '48.71', '0.50', '0.24', '5.00', '2.44', '5.00', '2.44', 1, '8910792003', '2024-03-04 11:26:23', NULL, NULL),
(1709532529, 1, 1, 6, '2024-03-04', '98.54', '1.00', '0.99', '12.00', '11.82', '12.00', '11.82', 1, '8910792003', '2024-03-04 11:38:48', NULL, NULL),
(1709533108, 1, 1, 3, '2024-03-04', '89.00', '5.00', '8.90', '5.00', '8.90', '5.00', '8.90', 2, '8910792003', '2024-03-04 11:48:28', NULL, NULL),
(1709535650, 1, 1, 5, '2024-03-04', '20.00', '0.00', '0.00', '5.00', '1.00', '5.00', '1.00', 1, '8910792003', '2024-03-04 12:30:50', NULL, NULL),
(1709535821, 1, 1, 5, '2024-03-04', '20.00', '0.00', '0.00', '5.00', '1.00', '5.00', '1.00', 1, '8910792003', '2024-03-04 12:33:40', NULL, NULL),
(1709540150, 1, 1, 1, '2024-03-04', '200.00', '0.00', '5.00', '0.00', '0.00', '0.00', '0.00', 1, '8910792003', '2024-03-04 13:45:49', NULL, NULL),
(1709551159, 1, 1, 3, '2024-03-04', '89.00', '5.00', '4.45', '5.00', '4.45', '5.00', '4.45', 1, '8910792003', '2024-03-04 16:49:19', NULL, NULL),
(1709614557, 1, 1, 48, '2024-03-05', '345.00', '43.00', '0.00', '5.00', '40.00', '5.00', '40.00', 4, '8910792003', '2024-03-05 10:25:56', NULL, NULL),
(1709701219, 1, 1, 1, '2024-03-06', '323.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', 1, '8910792003', '2024-03-06 10:30:19', NULL, NULL),
(1709701219, 1, 1, 2, '2024-03-06', '10.85', '0.00', '0.00', '5.00', '0.54', '5.00', '0.54', 1, '8910792003', '2024-03-06 10:30:19', NULL, NULL),
(1709701219, 1, 1, 11, '2024-03-06', '50.00', '0.25', '0.13', '5.00', '2.50', '5.00', '2.50', 1, '8910792003', '2024-03-06 10:30:19', NULL, NULL),
(1709701219, 1, 1, 14, '2024-03-06', '60.00', '0.00', '0.00', '28.00', '16.80', '28.00', '16.80', 1, '8910792003', '2024-03-06 10:30:19', NULL, NULL),
(1709799062, 1, 1, 7, '2024-03-07', '10.00', '0.00', '0.00', '12.00', '2.40', '12.00', '2.40', 2, '8910792003', '2024-03-07 13:41:01', NULL, NULL),
(1709800879, 1, 1, 1, '2024-03-07', '323.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', 5, '8910792003', '2024-03-07 14:11:19', NULL, NULL),
(1709800879, 1, 1, 10, '2024-03-07', '30.00', '0.00', '0.00', '5.00', '148.50', '5.00', '148.50', 99, '8910792003', '2024-03-07 14:11:19', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `td_receipt`
--

CREATE TABLE `td_receipt` (
  `receipt_no` bigint NOT NULL,
  `trn_date` date NOT NULL,
  `price` decimal(10,2) NOT NULL DEFAULT '0.00',
  `discount_amt` decimal(10,2) NOT NULL DEFAULT '0.00',
  `cgst_amt` decimal(10,2) NOT NULL DEFAULT '0.00',
  `sgst_amt` decimal(10,2) NOT NULL DEFAULT '0.00',
  `amount` decimal(10,2) NOT NULL DEFAULT '0.00',
  `round_off` decimal(10,2) NOT NULL DEFAULT '0.00',
  `net_amt` decimal(10,2) NOT NULL DEFAULT '0.00',
  `pay_mode` enum('C','U','D','') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'C->Cash,U->UPI,D->Card',
  `received_amt` decimal(10,2) NOT NULL DEFAULT '0.00',
  `pay_dtls` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `cust_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone_no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `gst_flag` enum('Y','N') COLLATE utf8mb4_general_ci DEFAULT NULL,
  `discount_type` enum('P','A') COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_dt` datetime DEFAULT NULL,
  `modified_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modified_dt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `td_receipt`
--

INSERT INTO `td_receipt` (`receipt_no`, `trn_date`, `price`, `discount_amt`, `cgst_amt`, `sgst_amt`, `amount`, `round_off`, `net_amt`, `pay_mode`, `received_amt`, `pay_dtls`, `cust_name`, `phone_no`, `gst_flag`, `discount_type`, `created_by`, `created_dt`, `modified_by`, `modified_dt`) VALUES
(1708318748, '2024-02-19', '200.00', '40.00', '24.00', '24.00', '208.00', '0.00', '208.00', 'C', '500.00', 'something P', 'Fudud', '5655356898', NULL, NULL, '8910792003', '2024-02-19 10:29:07', NULL, NULL),
(1708321727, '2024-02-19', '1110.00', '200.25', '126.20', '126.20', '1162.15', '-0.15', '1162.00', 'C', '2000.00', 'something P', 'Rifjcvj', '1335576898', NULL, NULL, '8910792003', '2024-02-19 11:18:47', NULL, NULL),
(1708321755, '2024-02-19', '89.00', '4.45', '4.45', '4.45', '93.45', '-0.45', '93.00', 'D', '0.00', 'something P', 'Etggh', '5458099523', NULL, NULL, '8910792003', '2024-02-19 11:19:14', NULL, NULL),
(1708340832, '2024-02-19', '171.70', '0.13', '8.59', '8.59', '188.74', '0.26', '189.00', 'C', '500.00', 'something P', 'Tanmoy', '1234567890', NULL, NULL, '8240378957', '2024-02-19 16:37:12', NULL, NULL),
(1708502138, '2024-02-21', '311.48', '42.23', '29.57', '29.57', '328.40', '-0.40', '328.00', 'C', '500.00', 'something P', 'Lopkhdd', '1234567890', NULL, NULL, '8910792003', '2024-02-21 13:25:38', NULL, NULL),
(1708510593, '2024-02-21', '50.00', '0.13', '2.50', '2.50', '54.87', '0.13', '55.00', 'D', '0.00', 'something P', 'Gzhhs', '0643543346', NULL, NULL, '8910792003', '2024-02-21 15:46:33', NULL, NULL),
(1708511825, '2024-02-21', '159.74', '1.11', '31.91', '31.91', '222.44', '-0.44', '222.00', 'U', '0.00', 'something P', '', '', NULL, NULL, '8910792003', '2024-02-21 16:07:04', NULL, NULL),
(1708511858, '2024-02-21', '277.08', '1.97', '27.65', '27.65', '330.41', '-0.41', '330.00', 'D', '0.00', 'something P', 'Itgk', '6657800088', NULL, NULL, '8910792003', '2024-02-21 16:07:37', NULL, NULL),
(1708513751, '2024-02-21', '10.85', '0.00', '0.54', '0.54', '11.93', '0.07', '12.00', 'D', '0.00', 'something P', '', '', NULL, NULL, '8910792003', '2024-02-21 16:39:10', NULL, NULL),
(1708513779, '2024-02-21', '178.00', '8.90', '0.00', '0.00', '169.10', '-0.10', '169.00', 'D', '0.00', 'something P', '', '', NULL, NULL, '8910792003', '2024-02-21 16:39:38', NULL, NULL),
(1708513811, '2024-02-21', '20.00', '0.00', '2.40', '2.40', '24.80', '0.20', '25.00', 'C', '50.00', 'something P', '', '', NULL, NULL, '8910792003', '2024-02-21 16:40:10', NULL, NULL),
(1708596612, '2024-02-22', '100.00', '23.00', '5.00', '5.00', '87.00', '0.00', '87.00', 'U', '0.00', 'something P', '', '', NULL, NULL, '8910792003', '2024-02-22 15:40:11', NULL, NULL),
(1708596899, '2024-02-22', '154.28', '4.07', '14.61', '14.61', '179.43', '-0.43', '179.00', 'D', '0.00', 'something P', 'Hola', '1234567908', NULL, NULL, '8910792003', '2024-02-22 15:44:58', NULL, NULL),
(1708597154, '2024-02-22', '100.00', '0.25', '5.00', '5.00', '109.75', '0.25', '110.00', 'C', '100.00', 'something P', '', '', NULL, NULL, '8910792003', '2024-02-22 15:49:13', NULL, NULL),
(1708597230, '2024-02-22', '150.00', '7.50', '27.00', '27.00', '196.50', '0.50', '197.00', 'C', '200.00', 'something P', '', '', NULL, NULL, '8910792003', '2024-02-22 15:50:30', NULL, NULL),
(1708597582, '2024-02-22', '10.85', '0.00', '0.54', '0.54', '11.93', '0.07', '12.00', 'D', '0.00', 'something P', '', '', NULL, NULL, '8910792003', '2024-02-22 15:56:22', NULL, NULL),
(1708597836, '2024-02-22', '10.85', '0.00', '0.54', '0.54', '11.93', '0.07', '12.00', 'C', '50.00', 'something P', '', '', NULL, NULL, '8910792003', '2024-02-22 16:00:35', NULL, NULL),
(1708598416, '2024-02-22', '218.78', '177.37', '24.73', '24.73', '90.88', '0.12', '91.00', 'C', '100.00', 'something P', 'Lol', '1234567890', NULL, NULL, '8910792003', '2024-02-22 16:10:15', NULL, NULL),
(1708598749, '2024-02-22', '94270.00', '605.20', '8162.40', '8162.40', '109989.60', '0.40', '109990.00', 'U', '0.00', 'something P', '', '', NULL, NULL, '8910792003', '2024-02-22 16:15:49', NULL, NULL),
(1708603021, '2024-02-22', '565.08', '11.25', '61.55', '61.55', '676.93', '0.07', '677.00', 'C', '1000.00', 'something A', 'Jokey', '8910797943', NULL, NULL, '8910792003', '2024-02-22 17:27:00', NULL, NULL),
(1708603437, '2024-02-22', '2020.80', '1.00', '239.00', '239.00', '2497.79', '0.21', '2498.00', 'C', '2500.00', 'something A', 'Rupsa', '7357357657', NULL, NULL, '6295825458', '2024-02-22 17:33:57', NULL, NULL),
(1708603765, '2024-02-22', '1869.00', '5.00', '0.00', '0.00', '1864.00', '0.00', '1864.00', 'C', '2000.00', 'something A', '', '', NULL, NULL, '6295825458', '2024-02-22 17:39:24', NULL, NULL),
(1708672060, '2024-02-23', '598.44', '99.78', '64.41', '64.41', '627.48', '-0.48', '627.00', 'C', '700.00', 'something P', 'Epsilon', '0101010101', NULL, NULL, '8910792003', '2024-02-23 12:37:39', NULL, NULL),
(1708684020, '2024-02-23', '120.00', '6.00', '21.60', '21.60', '157.20', '-0.20', '157.00', 'D', '0.00', 'something P', 'Shubham', '7542320507', NULL, NULL, '8910792003', '2024-02-23 15:56:59', NULL, NULL),
(1708950410, '2024-02-26', '354.00', '12.95', '39.15', '39.15', '419.35', '-0.35', '419.00', 'C', '500.00', 'something A', '', '1111111111', NULL, NULL, '8910792003', '2024-02-26 17:56:50', NULL, NULL),
(1708950614, '2024-02-26', '265.28', '6.55', '21.70', '21.70', '302.13', '-0.13', '302.00', 'C', '300.00', 'something A', '', '1234567890', NULL, NULL, '8910792003', '2024-02-26 18:00:14', NULL, NULL),
(1708951194, '2024-02-26', '365.00', '38.38', '39.70', '39.70', '406.02', '-0.02', '406.00', 'C', '500.00', 'something P', 'William Shake', '9000000000', NULL, NULL, '8910792003', '2024-02-26 18:09:53', NULL, NULL),
(1709010412, '2024-02-27', '490.85', '46.50', '67.44', '67.44', '579.24', '-0.24', '579.00', 'C', '600.00', 'something P', 'Wyehhg', '125', NULL, NULL, '8910792003', '2024-02-27 10:36:52', NULL, NULL),
(1709014348, '2024-02-27', '53.71', '0.24', '3.34', '3.34', '60.14', '-0.14', '60.00', 'D', '0.00', 'something P', '', '1111111111', NULL, NULL, '8910792003', '2024-02-27 11:42:28', NULL, NULL),
(1709028630, '2024-02-27', '396.59', '7.00', '0.00', '0.00', '389.59', '0.41', '390.00', 'C', '400.00', 'something A', '', '9000000000', NULL, NULL, '8910792003', '2024-02-27 15:40:29', NULL, NULL),
(1709120855, '2024-02-28', '269.00', '18.65', '58.82', '58.82', '367.99', '0.01', '368.00', 'C', '500.00', 'something P', 'Debashish', '1234567890', NULL, NULL, '8910792003', '2024-02-28 17:17:34', NULL, NULL),
(1709121628, '2024-02-28', '239.00', '11.95', '0.00', '0.00', '227.05', '-0.05', '227.00', 'C', '300.00', 'something P', '', '1111111111', NULL, NULL, '8910792003', '2024-02-28 17:30:27', NULL, NULL),
(1709184595, '2024-02-29', '165.00', '8.25', '0.00', '0.00', '156.75', '0.25', '157.00', 'C', '200.00', 'something P', '', '6464664646', NULL, NULL, '8910792003', '2024-02-29 10:59:55', NULL, NULL),
(1709205718, '2024-02-29', '28.00', '0.00', '0.00', '0.00', '28.00', '0.00', '28.00', 'U', '0.00', 'something P', 'Muhammad Ali', '5802963044', NULL, NULL, '8910792003', '2024-02-29 16:51:58', NULL, NULL),
(1709272394, '2024-03-01', '546.25', '36.18', '48.01', '48.01', '606.09', '-0.09', '606.00', 'D', '0.00', 'something P', 'Kyzgsthan', '1234567890', NULL, NULL, '8910792003', '2024-03-01 11:23:13', NULL, NULL),
(1709535821, '2024-03-04', '20.00', '0.00', '1.00', '1.00', '22.00', '0.00', '22.00', 'D', '0.00', 'something P', '', '1234545488', 'Y', 'P', '8910792003', '2024-03-04 12:33:40', NULL, NULL),
(1709701219, '2024-03-06', '443.85', '0.13', '19.84', '19.84', '483.41', '-0.41', '483.00', 'D', '0.00', 'something P', '', '5695656502', 'Y', 'P', '8910792003', '2024-03-06 10:30:19', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `td_receipt_cancel_new`
--

CREATE TABLE `td_receipt_cancel_new` (
  `cancel_rcpt_id` int NOT NULL,
  `receipt_no` bigint NOT NULL,
  `trn_date` date NOT NULL,
  `price` decimal(10,2) NOT NULL DEFAULT '0.00',
  `discount_amt` decimal(10,2) NOT NULL DEFAULT '0.00',
  `cgst_amt` decimal(10,2) NOT NULL DEFAULT '0.00',
  `sgst_amt` decimal(10,2) NOT NULL DEFAULT '0.00',
  `amount` decimal(10,2) NOT NULL DEFAULT '0.00',
  `round_off` decimal(10,2) NOT NULL DEFAULT '0.00',
  `net_amt` decimal(10,2) NOT NULL DEFAULT '0.00',
  `pay_mode` enum('C','U','D','') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'C->Cash,U->UPI,D->Card',
  `received_amt` decimal(10,2) NOT NULL DEFAULT '0.00',
  `pay_dtls` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `cust_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone_no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `gst_flag` enum('Y','N') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `discount_type` enum('P','A') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_dt` datetime DEFAULT NULL,
  `modified_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modified_dt` datetime DEFAULT NULL,
  `cancelled_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cancelled_dt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `td_receipt_cancel_new`
--

INSERT INTO `td_receipt_cancel_new` (`cancel_rcpt_id`, `receipt_no`, `trn_date`, `price`, `discount_amt`, `cgst_amt`, `sgst_amt`, `amount`, `round_off`, `net_amt`, `pay_mode`, `received_amt`, `pay_dtls`, `cust_name`, `phone_no`, `gst_flag`, `discount_type`, `created_by`, `created_dt`, `modified_by`, `modified_dt`, `cancelled_by`, `cancelled_dt`) VALUES
(1, 1708081018, '2024-02-16', '50.00', '0.13', '2.50', '2.50', '54.87', '0.13', '55.00', 'C', '100.00', 'something P', 'Oyogdvbd', '2361097640', NULL, NULL, '8910792003', '2024-02-16 16:26:57', NULL, NULL, '8910792003', '2024-03-05 11:46:13'),
(2, 1708325680, '2024-02-19', '50.00', '0.13', '2.50', '2.50', '54.87', '0.13', '55.00', 'U', '0.00', 'something P', 'Etug', '5688808780', NULL, NULL, '8910792003', '2024-02-19 12:24:39', NULL, NULL, '8910792003', '2024-03-05 11:48:44'),
(3, 1708510305, '2024-02-21', '52.00', '0.00', '14.56', '14.56', '81.12', '-0.12', '81.00', 'C', '100.00', 'something P', 'Puhdnd', '1334516400', NULL, NULL, '8910792003', '2024-02-21 15:41:45', NULL, NULL, '8910792003', '2024-03-05 13:55:18'),
(4, 1709540150, '2024-03-04', '200.00', '5.00', '0.00', '0.00', '195.00', '0.00', '195.00', 'D', '0.00', 'something A', '', '5555555555', 'N', 'A', '8910792003', '2024-03-04 13:45:49', NULL, NULL, '8910792003', '2024-03-05 17:07:06'),
(5, 1709551159, '2024-03-04', '89.00', '4.45', '4.45', '4.45', '93.45', '-0.45', '93.00', 'D', '0.00', 'something P', '', '6865353565', 'Y', 'P', '8910792003', '2024-03-04 16:49:19', NULL, NULL, '8910792003', '2024-03-05 17:06:54'),
(6, 1709799062, '2024-03-07', '20.00', '0.00', '2.40', '2.40', '24.80', '0.20', '25.00', 'C', '50.00', 'something P', '', '9831887194', 'Y', 'P', '8910792003', '2024-03-07 13:41:01', NULL, NULL, '8910792003', '2024-03-07 16:35:17'),
(7, 1709800879, '2024-03-07', '4585.00', '0.00', '148.50', '148.50', '4882.00', '0.00', '4882.00', 'D', '0.00', 'something P', '', '2135464810', 'Y', 'P', '8910792003', '2024-03-07 14:11:19', NULL, NULL, '8910792003', '2024-03-07 16:21:55'),
(9, 1709805406, '2024-03-07', '501.00', '8.90', '8.90', '8.90', '509.90', '0.10', '510.00', 'C', '550.00', 'something P', 'Trolol', '0098000808', 'Y', 'P', '8910792003', '2024-03-07 15:26:46', NULL, NULL, '8910792003', '2024-03-08 12:20:15'),
(10, 1709720760, '2024-03-06', '667.70', '323.00', '1.09', '1.09', '346.87', '0.13', '347.00', 'U', '0.00', 'something P', '', '8961492920', 'Y', 'P', '8910792003', '2024-03-06 15:56:00', NULL, NULL, '8910792003', '2024-03-08 12:25:21'),
(11, 1709540992, '2024-03-04', '56.00', '5.25', '0.00', '0.00', '50.75', '0.25', '51.00', 'C', '100.00', 'something A', '', '1010100101', 'N', 'A', '8910792003', '2024-03-04 13:59:52', NULL, NULL, '8910792003', '2024-03-08 12:35:11'),
(12, 1709540992, '2024-03-04', '56.00', '5.25', '0.00', '0.00', '50.75', '0.25', '51.00', 'C', '100.00', 'something A', '', '1010100101', 'N', 'A', '8910792003', '2024-03-04 13:59:52', NULL, NULL, '8910792003', '2024-03-08 12:54:16'),
(13, 1709540992, '2024-03-04', '56.00', '5.25', '0.00', '0.00', '50.75', '0.25', '51.00', 'C', '100.00', 'something A', '', '1010100101', 'N', 'A', '8910792003', '2024-03-04 13:59:52', NULL, NULL, '8910792003', '2024-03-08 13:06:38'),
(14, 1709883585, '2024-03-08', '3230.00', '0.00', '0.00', '0.00', '3230.00', '0.00', '3230.00', 'U', '0.00', 'something P', 'Arydjd', '1234564000', 'Y', 'P', '8910792003', '2024-03-08 13:09:44', NULL, NULL, '8910792003', '2024-03-08 13:09:59'),
(15, 1709883715, '2024-03-08', '3876.00', '0.00', '0.00', '0.00', '3876.00', '0.00', '3876.00', 'C', '5000.00', 'something P', '', '2548040000', 'Y', 'P', '8910792003', '2024-03-08 13:11:54', NULL, NULL, '8910792003', '2024-03-08 13:12:33');

-- --------------------------------------------------------

--
-- Table structure for table `td_stock`
--

CREATE TABLE `td_stock` (
  `comp_id` int NOT NULL,
  `br_id` int NOT NULL,
  `item_id` int NOT NULL,
  `stock` int DEFAULT NULL,
  `created_by` varchar(50) DEFAULT NULL,
  `created_dt` datetime DEFAULT NULL,
  `modified_by` varchar(50) DEFAULT NULL,
  `modified_dt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `td_stock`
--

INSERT INTO `td_stock` (`comp_id`, `br_id`, `item_id`, `stock`, `created_by`, `created_dt`, `modified_by`, `modified_dt`) VALUES
(1, 1, 1, 23, '8910792003', NULL, '8910792003', '2024-03-08 13:12:33'),
(1, 1, 2, 40, '8910792003', NULL, '8910792003', '2024-03-08 12:25:21'),
(1, 1, 3, 14, '8910792003', NULL, '8910792003', '2024-03-08 12:20:15'),
(1, 1, 4, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 5, 0, '8910792003', NULL, NULL, NULL),
(1, 1, 6, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 7, 25, '8910792003', NULL, '8910792003', '2024-03-07 12:33:48'),
(1, 1, 8, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 9, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 10, 149, '8910792003', NULL, '8910792003', '2024-03-07 11:51:42'),
(1, 1, 11, 17, '8910792003', NULL, '8910792003', '2024-03-08 13:06:38'),
(1, 1, 12, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 13, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 14, 14, '8910792003', NULL, NULL, NULL),
(1, 1, 15, 0, '8910792003', NULL, NULL, NULL),
(1, 1, 16, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 39, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 41, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 42, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 43, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 44, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 45, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 46, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 47, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 48, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 49, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 50, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 51, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 52, 13, '8910792003', NULL, NULL, NULL),
(1, 1, 54, 0, '8910792003', '2024-03-07 17:38:47', NULL, NULL),
(1, 1, 55, 0, '8910792003', '2024-03-07 17:47:07', NULL, NULL),
(1, 1, 56, 0, '8910792003', '2024-03-07 17:49:15', NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `md_branch`
--
ALTER TABLE `md_branch`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `md_company`
--
ALTER TABLE `md_company`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `md_container`
--
ALTER TABLE `md_container`
  ADD PRIMARY KEY (`sl_no`);

--
-- Indexes for table `md_header_footer`
--
ALTER TABLE `md_header_footer`
  ADD PRIMARY KEY (`comp_id`);

--
-- Indexes for table `md_items`
--
ALTER TABLE `md_items`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `md_item_rate`
--
ALTER TABLE `md_item_rate`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `md_location`
--
ALTER TABLE `md_location`
  ADD PRIMARY KEY (`sl_no`);

--
-- Indexes for table `md_receipt_settings`
--
ALTER TABLE `md_receipt_settings`
  ADD PRIMARY KEY (`comp_id`);

--
-- Indexes for table `md_unit`
--
ALTER TABLE `md_unit`
  ADD PRIMARY KEY (`sl_no`);

--
-- Indexes for table `md_user`
--
ALTER TABLE `md_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `md_version`
--
ALTER TABLE `md_version`
  ADD PRIMARY KEY (`sl_no`);

--
-- Indexes for table `td_item_purchase`
--
ALTER TABLE `td_item_purchase`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `td_item_sale`
--
ALTER TABLE `td_item_sale`
  ADD PRIMARY KEY (`receipt_no`,`item_id`);

--
-- Indexes for table `td_receipt`
--
ALTER TABLE `td_receipt`
  ADD PRIMARY KEY (`receipt_no`);

--
-- Indexes for table `td_receipt_cancel_new`
--
ALTER TABLE `td_receipt_cancel_new`
  ADD PRIMARY KEY (`cancel_rcpt_id`);

--
-- Indexes for table `td_stock`
--
ALTER TABLE `td_stock`
  ADD PRIMARY KEY (`comp_id`,`br_id`,`item_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `md_branch`
--
ALTER TABLE `md_branch`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `md_company`
--
ALTER TABLE `md_company`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `md_container`
--
ALTER TABLE `md_container`
  MODIFY `sl_no` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `md_items`
--
ALTER TABLE `md_items`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT for table `md_item_rate`
--
ALTER TABLE `md_item_rate`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;

--
-- AUTO_INCREMENT for table `md_location`
--
ALTER TABLE `md_location`
  MODIFY `sl_no` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `md_unit`
--
ALTER TABLE `md_unit`
  MODIFY `sl_no` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `md_user`
--
ALTER TABLE `md_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `md_version`
--
ALTER TABLE `md_version`
  MODIFY `sl_no` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `td_item_purchase`
--
ALTER TABLE `td_item_purchase`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `td_receipt_cancel_new`
--
ALTER TABLE `td_receipt_cancel_new`
  MODIFY `cancel_rcpt_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
