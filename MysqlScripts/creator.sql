CREATE DATABASE `culab`;
use 'culab';


CREATE TABLE `items` (
 `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
 `patrimonialNumber` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
 `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
 `brand` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
 `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
 `stock` int(11) NOT NULL,
 PRIMARY KEY (`id`),
 UNIQUE KEY `items_patrimonialnumber_unique` (`patrimonialNumber`)
);

CREATE TABLE `lendings` (
 `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
 `lendingDate` date NOT NULL,
 `accountNumber` int(20) COLLATE utf8mb4_unicode_ci NOT NULL,
 `patrimonialNumber` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
 PRIMARY KEY (`id`),
 UNIQUE KEY `lendings_patrimonialnumber_unique` (`patrimonialNumber`)
);

CREATE TABLE `historialLendings` (
 `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
 `lendingDate` date NOT NULL,
 `returnDate` date NOT NULL,
 `accountNumber` int(20) COLLATE utf8mb4_unicode_ci NOT NULL,
 `patrimonialNumber` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
 PRIMARY KEY (`id`),
 UNIQUE KEY `lendings_patrimonialnumber_unique` (`patrimonialNumber`)
);


CREATE TABLE `students` (
 `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
 `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
 `accountNumber` int(20) COLLATE utf8mb4_unicode_ci NOT NULL,
 `career` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
 PRIMARY KEY (`id`),
 UNIQUE KEY `students_accountnumber_unique` (`accountNumber`)
);


