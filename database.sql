-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 10, 2026 at 06:36 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lumera_beauty`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_users`
--

CREATE TABLE `admin_users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_users`
--

INSERT INTO `admin_users` (`id`, `name`, `email`, `password_hash`) VALUES
(1, 'Admin Luméra', 'admin@lumera.com', 'scrypt:32768:8:1$yr3kRJgU01KRzH3z$01f47ab2fef66dc725e56612797f9fb0f99774b02d847a616b06ee38666ce2190a836552129e3cee0d83901afc2e7de3003b4f0a1c31224e3179602b8aa0e3ef');

-- --------------------------------------------------------

--
-- Table structure for table `brands`
--

CREATE TABLE `brands` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `brands`
--

INSERT INTO `brands` (`id`, `name`) VALUES
(2, 'Emina'),
(10, 'Glad2Glow'),
(6, 'Himvera'),
(4, 'Make Over'),
(9, 'Makeup Forever'),
(7, 'Nivea'),
(11, 'Sea Makeup'),
(5, 'Skintific'),
(3, 'Somethinc'),
(8, 'Streax'),
(1, 'Wardah');

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`) VALUES
(3, 'Bodycare'),
(4, 'Haircare'),
(2, 'Makeup'),
(1, 'Skincare');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `brand_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  `volume` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `image_color` varchar(30) DEFAULT NULL,
  `image_icon` varchar(50) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `is_new` tinyint(1) DEFAULT 0,
  `created_at` datetime DEFAULT current_timestamp(),
  `discount` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `brand_id`, `category_id`, `price`, `stock`, `volume`, `description`, `image_color`, `image_icon`, `image`, `is_new`, `created_at`, `discount`) VALUES
(5, '5X Ceramide Barrier Moisture Gel', 5, 1, 120000, 12, '40 g', 'Gel moisturizer dengan 5X Ceramide untuk memperkuat skin barrier dan menjaga hidrasi kulit sepanjang hari.', '#F3C6D3', 'serum', 'skintific_5x_ceramide_toner.jpg', 0, '2026-07-08 12:40:28', 0),
(6, 'Instaperfect Matte Set', 1, 2, 98000, 23, '1 set', 'Set makeup matte lengkap untuk hasil wajah flawless tahan lama sepanjang hari.', '#F3C6D3', 'serum', 'Instaperfect_Matte_Set.jpg', 0, '2026-07-08 12:40:28', 0),
(7, 'Acnessentials Face Wash Gel', 3, 1, 45000, 43, '100 ml', 'Facial wash gel yang membantu membersihkan wajah dari kotoran dan minyak berlebih tanpa membuat kulit kering.', '#F3C6D3', 'serum', 'Acnessentials_Face_Wash_Gel.jpg', 0, '2026-07-08 12:40:28', 0),
(8, 'Perfect Shield Sunscreen SPF 50 PA+++', 1, 1, 65000, 40, '35 ml', 'Sunscreen ringan dengan SPF 45 PA+++ yang melindungi kulit dari sinar UV sekaligus melembapkan wajah.', '#F3C6D3', 'serum', 'Perfect_Shield_Sunscreen_SPF50.jpg', 0, '2026-07-08 12:40:28', 0),
(9, 'Ceramic Matte Lipcream', 4, 2, 39000, 60, '5 ml', 'Lip cream dengan warna-warna cantik dan formula matte yang nyaman di bibir.', '#F3C6D3', 'serum', 'Ceramic_Matte_Lipcream.jpg', 0, '2026-07-08 12:40:28', 0),
(10, 'Barrier Balance Moisturizer', 5, 1, 98000, 12, '30 g', 'Moisturizer harian untuk memperbaiki dan menjaga keseimbangan skin barrier.', '#F3C6D3', 'serum', 'Barrier_Balance_Moisturizer.jpg', 0, '2026-07-08 12:40:28', 0),
(11, 'Glow Maker Serum', 10, 1, 79000, 18, '20 ml', 'Serum pencerah dengan kandungan Vitamin C untuk kulit tampak lebih glowing.', '#F3C6D3', 'serum', 'Body_serum.jpg', 0, '2026-07-08 12:40:28', 0),
(12, 'Velvet Matte Foundation', 9, 2, 145000, 8, '1 palette', 'Eyeshadow palette dengan warna-warna pigmented dan blendable untuk tampilan mata sehari-hari maupun acara spesial.', '#F3C6D3', 'serum', 'Velvet_Matte_Foundation.jpg', 0, '2026-07-08 12:40:28', 0),
(13, 'Streax Professional Vitariche Gloss Hair Serum', 8, 4, 55000, 26, '60 ml', 'Hair serum yang melembutkan dan melindungi rambut dari kerusakan akibat panas.', '#F3C6D3', 'serum', 'Streax_Professional_Vitariche_Gloss_Hair_Serum.jpg', 0, '2026-07-08 12:40:28', 0),
(14, 'Nivea Extra White Instant Glow', 7, 3, 42000, 4, '100 ml', 'Body lotion dengan aroma lembut yang melembapkan kulit tubuh sepanjang hari.', '#F3C6D3', 'serum', 'Nivea_Extra_White_Instant_Glow.jpg', 0, '2026-07-08 12:40:28', 0),
(15, 'Aloe Hydrating', 6, 1, 38000, 10, '100 ml', 'Toner dengan ekstrak aloe vera untuk menyegarkan dan melembapkan kulit wajah.', '#F3C6D3', 'serum', 'Himvera.jpg', 0, '2026-07-08 12:40:28', 0),
(18, 'Liquid Blush', 11, 2, 66000, 29, '6ml', 'Sea Makeup Vibrant Flushed Liquid Blush On Cair – Cream Blush On Pipi Tahan Lama, Blush On Cream Warna Natural, Blush On Cair 4 Pilihan Warna.', '#F3C6D3', 'serum', 'Liquid_Blush.jpg', 1, '2026-07-09 19:35:39', 0),
(19, 'Wardah UV Shield Acne Calming Sunscreen Moisturizer SPF 35 PA+++', 1, 1, 40000, 0, '25 gr', 'WARDAH UV SHIELD ACNE CALMING SUNSCREEN MOISTURIZER SPF 35 PA++ SUNSCREEN YANG DIFORMULASIKAN KHUSUS UNTUK KULIT BERMINYAK DAN ACNE-PRONE SKIN Sunscreen Moisturizer SPF 35 PA+++ nyaman dan ringan digunakan setiap hari, diformulasikan khusus untuk kulit wajah berminyak dan rentan berjerawat. Mengandung Salicylic Acid, Panthenol, dan Vitamin B3 yang dapat membantu melawan bakteri penyebab jerawat. - Lightweight - Fresh & Watery Texture - Non-Comedogenic - Non-Acnegenic - Dermatologically Tested - No Alcohol - No Fragrance - No White Cast - Invisible Finish', '#F3C6D3', 'serum', 'wardah_sunscreen_35.jpg', 1, '2026-07-09 19:52:47', 0),
(20, 'SKINTIFIC - 10% Niacinamide Brightening Serum', 5, 1, 180000, 15, '20 ml', 'Serum Mencerahkan Dark Spot Tumpas Komedo anti aging Whitening Brightening anti acne Eksfoliasi Mengangkat Sel Kulit Mati Exfoliating with MSH Niacinamide Arbutin Acid Ceramide Centella. 10% Niacinamide Brightening Serum Serum pencerah dengan kandungan Niacinamide dan Alpha arbutin yang bekerja secara efektif mencerahkan kulit wajah. Dengan kandungan ceramide yang dapat menjaga dan menutrisi skin barrier sehingga kulit tidak hanya terlihat cerah dan merata namun juga bersih. Ukuran: 20 ml Νο ΒΡΟΜ: NA11231900093 Manfaat: • Membantu mencerahkan kulit wajah •Membantu merawat skin barrier kulit •Membantu menyamarkan bekas jerawat Hero Ingredients: Niacinamide: membantu mencerahkan kulit wajah Alpha Arbutin: membantu efektivitas niacinamide dan mencerahkan kulit', '#F3C6D3', 'serum', 'Skintific_Brightening_Booster.jpg', 1, '2026-07-09 19:57:31', 0),
(21, 'Skintific All Day Light Sunscreen Spf50 Pa++++ - Sunscreen Spray Anti Uv Wajah/Body Spray', 5, 1, 200000, 10, '50 ml', '●Melindungi kulit dari paparan UVA UVB \r\n\r\n●Memproteksi tanpa rasa greasy dan tanpa merusak makeup\r\n\r\n●Menjadikan kulit terasa segar setelah diaplikasikan\r\n\r\n●Tanpa whitecast dan travel-friendly\r\n\r\n\r\nHero Ingredients:\r\n\r\nCentella : Suplemen kolagen kulit untuk anti inflamasi', '#F3C6D3', 'serum', 'skintific_sunscreen_spray.webp', 1, '2026-07-09 20:04:22', 0);

-- --------------------------------------------------------

--
-- Table structure for table `stock_movements`
--

CREATE TABLE `stock_movements` (
  `id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `type` enum('masuk','keluar') DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `note` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stock_movements`
--

INSERT INTO `stock_movements` (`id`, `product_id`, `type`, `quantity`, `note`, `created_at`) VALUES
(3, 5, 'masuk', 25, 'Restock', '2026-07-08 12:40:28'),
(5, 12, 'keluar', 20, 'Penjualan toko', '2026-07-08 12:40:28'),
(6, 5, 'keluar', 1, 'Penjualan INV20260708214508', '2026-07-08 21:45:08'),
(7, 5, 'keluar', 1, 'Penjualan INV20260708214738', '2026-07-08 21:47:38'),
(8, 5, 'keluar', 1, 'Penjualan INV20260708220519', '2026-07-08 22:05:19'),
(9, 5, 'keluar', 1, 'Penjualan INV20260708221406', '2026-07-08 22:14:06'),
(10, 5, 'keluar', 1, 'Penjualan INV20260708221517', '2026-07-08 22:15:17'),
(11, 5, 'keluar', 1, 'Penjualan INV20260708221836', '2026-07-08 22:18:36'),
(12, 5, 'keluar', 1, 'Penjualan INV20260708221852', '2026-07-08 22:18:52'),
(13, 15, 'masuk', 10, '', '2026-07-08 22:25:41'),
(14, 5, 'keluar', 5, 'Penjualan INV20260708224705', '2026-07-08 22:47:06'),
(15, 6, 'keluar', 7, 'Penjualan INV20260709180312', '2026-07-09 18:03:12'),
(16, 8, 'masuk', 100, '', '2026-07-09 18:14:37'),
(17, 18, 'keluar', 1, 'Penjualan INV20260709221011', '2026-07-09 22:10:11'),
(18, 13, 'keluar', 1, 'Penjualan INV20260709221011', '2026-07-09 22:10:11'),
(19, 7, 'keluar', 1, 'Penjualan INV20260709221554', '2026-07-09 22:15:54'),
(20, 19, 'keluar', 1, 'Penjualan INV20260709225104', '2026-07-09 22:51:04'),
(21, 12, 'keluar', 2, 'Penjualan INV20260709225104', '2026-07-09 22:51:04'),
(22, 7, 'keluar', 6, 'Penjualan INV20260709225104', '2026-07-09 22:51:04'),
(23, 8, 'keluar', 10, '', '2026-07-09 22:55:21'),
(24, 11, 'masuk', 10, '', '2026-07-09 22:56:56'),
(25, 8, 'keluar', 50, 'Penjualan INV20260709234531', '2026-07-09 23:45:31'),
(26, 7, 'keluar', 1, 'Penjualan INV20260710000906', '2026-07-10 00:09:06'),
(27, 5, 'keluar', 1, 'Penjualan INV20260710001014', '2026-07-10 00:10:14');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `invoice` varchar(30) NOT NULL,
  `customer_name` varchar(100) DEFAULT NULL,
  `total` int(11) NOT NULL,
  `payment_method` enum('Cash','Transfer','QRIS') DEFAULT 'Cash',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `subtotal` int(11) NOT NULL DEFAULT 0,
  `discount` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `invoice`, `customer_name`, `total`, `payment_method`, `created_at`, `subtotal`, `discount`) VALUES
(2, 'INV20260708214508', 'Umum', 120000, 'Cash', '2026-07-08 14:45:08', 0, 0),
(3, 'INV20260708214738', 'Umum', 120000, 'Cash', '2026-07-08 14:47:38', 0, 0),
(9, 'INV20260708224705', 'Umum', 600000, 'Cash', '2026-07-08 15:47:05', 0, 0),
(10, 'INV20260709180312', 'Umum', 686000, 'Cash', '2026-07-09 11:03:12', 0, 0),
(11, 'INV20260709221011', 'Umum', 121000, 'Cash', '2026-07-09 15:10:11', 121000, 0),
(13, 'INV20260709225104', 'm', 600000, 'Cash', '2026-07-09 15:51:04', 0, 0),
(14, 'INV20260709234531', 'Umum', 3250000, 'Cash', '2026-07-09 16:45:31', 0, 0),
(15, 'INV20260710000906', 'Umum', 45000, 'Cash', '2026-07-09 17:09:06', 0, 0),
(16, 'INV20260710001014', 'Umum', 120000, 'Cash', '2026-07-09 17:10:14', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `transaction_items`
--

CREATE TABLE `transaction_items` (
  `id` int(11) NOT NULL,
  `transaction_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `qty` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `subtotal` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transaction_items`
--

INSERT INTO `transaction_items` (`id`, `transaction_id`, `product_id`, `qty`, `price`, `subtotal`) VALUES
(1, 2, 5, 1, 120000, 120000),
(2, 3, 5, 1, 120000, 120000),
(8, 9, 5, 5, 120000, 600000),
(9, 10, 6, 7, 98000, 686000),
(10, 11, 18, 1, 66000, 66000),
(11, 11, 13, 1, 55000, 55000),
(13, 13, 19, 1, 40000, 40000),
(14, 13, 12, 2, 145000, 290000),
(15, 13, 7, 6, 45000, 270000),
(16, 14, 8, 50, 65000, 3250000),
(17, 15, 7, 1, 45000, 45000),
(18, 16, 5, 1, 120000, 120000);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_users`
--
ALTER TABLE `admin_users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `brands`
--
ALTER TABLE `brands`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `brand_id` (`brand_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `stock_movements`
--
ALTER TABLE `stock_movements`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `invoice` (`invoice`);

--
-- Indexes for table `transaction_items`
--
ALTER TABLE `transaction_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `transaction_id` (`transaction_id`),
  ADD KEY `product_id` (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin_users`
--
ALTER TABLE `admin_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `brands`
--
ALTER TABLE `brands`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `stock_movements`
--
ALTER TABLE `stock_movements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `transaction_items`
--
ALTER TABLE `transaction_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`brand_id`) REFERENCES `brands` (`id`),
  ADD CONSTRAINT `products_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`);

--
-- Constraints for table `stock_movements`
--
ALTER TABLE `stock_movements`
  ADD CONSTRAINT `stock_movements_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Constraints for table `transaction_items`
--
ALTER TABLE `transaction_items`
  ADD CONSTRAINT `transaction_items_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `transactions` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `transaction_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
