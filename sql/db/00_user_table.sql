CREATE TABLE `consumer` (
  `id` int AUTO_INCREMENT NOT NULL,
  `consumer` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `api_key` varchar(256) NOT NULL,
  `created_on` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (`id`)
);
