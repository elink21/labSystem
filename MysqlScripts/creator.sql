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