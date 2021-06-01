-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 21, 2021 at 06:39 PM
-- Server version: 10.4.18-MariaDB
-- PHP Version: 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `judy-chatbot`
--

-- --------------------------------------------------------

--
-- Table structure for table `categorie`
--

CREATE TABLE `categorie` (
  `id` int(11) NOT NULL,
  `nom` varchar(255) NOT NULL,
  `img` varchar(255) NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `categorie`
--

INSERT INTO `categorie` (`id`, `nom`, `img`, `description`) VALUES
(1, 'Liquide Vaisselle', 'https://www.judy.tn/wp-content/uploads/2015/07/liquide_vaiselle__6.jpg', 'Un bon nettoyant vaisselle manuel, doit éliminer efficacement les saletés même les plus tenaces'),
(2, 'les Désinfectants', 'https://www.judy.tn/wp-content/uploads/2019/01/jav-ext.png', 'Un simple nettoyage de votre maison élimine la poussière, les taches de graisse et autres saletés '),
(3, 'Les sols et surfaces', 'https://www.judy.tn/wp-content/uploads/2020/03/sols-et-surfaces-brise_795x510.png', 'ces produits vous accompagnent au quotidien pour nettoyer tous vos vitres, sols et surfaces lavables'),
(4, 'Les nettoyants multi-usages', 'https://www.judy.tn/wp-content/uploads/2015/07/nett22.jpg', 'Judy Nettoyant est un produit qui nettoie vraiment tout dans la maison : linge, vaisselle, sols'),
(5, 'Le linge', 'https://www.judy.tn/wp-content/uploads/2019/10/moquette-mauve-1.jpg', 'Une formule professionnelle qui vous permet de nettoyer et de raviver les couleurs de vos tapis'),
(6, 'Les sanitaires', 'https://www.judy.tn/wp-content/uploads/2019/01/Sdet.png', 'ces produits éliminent parfaitement les matières organiques et les mauvaises odeurs ');

-- --------------------------------------------------------

--
-- Table structure for table `client`
--

CREATE TABLE `client` (
  `id` int(11) NOT NULL,
  `nom` varchar(60) NOT NULL,
  `prenom` varchar(60) NOT NULL,
  `date_naissance` date NOT NULL,
  `tel` int(11) NOT NULL,
  `email` varchar(120) NOT NULL,
  `adresse` varchar(255) NOT NULL,
  `ville` varchar(60) NOT NULL,
  `pays` varchar(60) NOT NULL,
  `etat` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `client`
--

INSERT INTO `client` (`id`, `nom`, `prenom`, `date_naissance`, `tel`, `email`, `adresse`, `ville`, `pays`, `etat`) VALUES
(1, 'ons', 'chawach', '1780-05-19', 51375495, 'ghedcjj@gmail.com', 'sxjj', 'jkzsh', 'zsdjhk', 1);

-- --------------------------------------------------------

--
-- Table structure for table `gamme`
--

CREATE TABLE `gamme` (
  `id` int(11) NOT NULL,
  `id_categorie` int(11) NOT NULL,
  `nom` varchar(60) NOT NULL,
  `img` varchar(255) NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `gamme`
--

INSERT INTO `gamme` (`id`, `id_categorie`, `nom`, `img`, `description`) VALUES
(1, 1, 'Judy Vaisselle', 'https://www.judy.tn/wp-content/uploads/2015/11/slide_vassl1.png', 'Judy Vaisselle nettoie et dégraisse en profondeur toute la vaisselle.\r\n'),
(2, 2, 'Judy Javel', 'https://www.judy.tn/wp-content/uploads/2019/09/javel1.jpg', 'Judy Javel désinfecte totalement la maison, blanchit le linge et élimine les mauvaises odeurs. Avec '),
(3, 2, 'Judy Clorogel', 'https://www.judy.tn/wp-content/uploads/2020/01/GM.png', 'Judy Clorogel  permet de blanchir, désodoriser, détacher et dégraisser en apportant une fraîcheur '),
(4, 3, 'Judy Sols & Surfaces\r\n', 'https://www.judy.tn/wp-content/uploads/2020/01/sfgm.png', 'Judy Sols & Surfaces nettoie et parfume toutes les surfaces lavables de la maison sols, sanitaires, '),
(5, 3, 'Judy Décapant\r\n', 'https://www.judy.tn/wp-content/uploads/2016/03/decapant1.jpg', 'Judy Décapant nettoie, détache et rénove les sols en carrelage, il élimine les voiles de ciments'),
(6, 3, 'Judy Nettoyant Vitres\r\n', 'https://www.judy.tn/wp-content/uploads/2015/11/vire250ml.jpg', 'Judy Nettoyant vitres assure à vos vitres une brillance sans précédent.'),
(7, 4, 'Judy Nettoyant\r\n', 'https://www.judy.tn/wp-content/uploads/2016/03/savon.jpg', 'Judy Nettoyant nettoie vraiment tout dans la maison : linge, vaisselle, sanitaire, sols et surface'),
(8, 4, 'Judy Nettoyant Extra Fort\r\n', 'https://www.judy.tn/wp-content/uploads/2019/02/netg.png', 'Judy Nettoyant  Extra Fort  est conçu pour le nettoyage de toute la maison: vaisselle,  linge, sol'),
(9, 5, 'Judy Linge\r\n', 'https://www.judy.tn/wp-content/uploads/2019/02/lingeg1.png', 'Judy Linge au savon, assure la propreté du linge aussi bien en lavage manuel ou dans une machine '),
(10, 5, 'Judy Linge Automatique', 'https://www.judy.tn/wp-content/uploads/2020/03/g.png', 'Judy Linge Automatique nettoie et parfume tous les types de tissus, il confère de la douceur au linge'),
(11, 6, 'Judy Déboucheur\r\n', 'https://www.judy.tn/wp-content/uploads/2016/09/Deboucheur2.jpg', 'Judy Déboucheur évite les engorgements, détruit les matières organiques et les cheveux qui obstruent'),
(12, 6, 'Judy Détartrant\r\n', 'https://www.judy.tn/wp-content/uploads/2015/11/peche.jpg', 'Judy Détartrant adhère parfaitement à la paroi des toilettes pour un détartrage maximal. ');

-- --------------------------------------------------------

--
-- Table structure for table `produit`
--

CREATE TABLE `produit` (
  `id` int(11) NOT NULL,
  `id_gamme` int(11) NOT NULL,
  `nom` varchar(60) NOT NULL,
  `img` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `qte_stock` int(11) NOT NULL,
  `prix_unitaire` int(11) NOT NULL,
  `volume_bouteille` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `produit`
--

INSERT INTO `produit` (`id`, `id_gamme`, `nom`, `img`, `description`, `qte_stock`, `prix_unitaire`, `volume_bouteille`) VALUES
(1, 1, 'Judy Vaisselle 650 mL Parfumée citron', 'https://www.savanna.tn/92227-medium_default/judy-liquide-vaisselle-mains-citron-580ml.jpg', 'Judy Vaisselle nettoie et dégraisse en profondeur toute la vaisselle.\r\n', 5000, 1500, '650'),
(2, 1, 'Judy Vaisselle 1.25 L parfumée citron', 'https://www.judy.tn/wp-content/uploads/2015/11/slide_vassl1.png', 'Judy Vaisselle nettoie et dégraisse en profondeur toute la vaisselle.\r\n', 5000, 2200, '1'),
(3, 1, 'Judy Vaisselle 5L parfumée citron', 'https://www.judy.tn/wp-content/uploads/2016/03/vaisselle3l.jpg', 'Judy Vaisselle nettoie et dégraisse en profondeur toute la vaisselle.\r\n', 3000, 5000, '5'),
(4, 1, 'Judy Vaisselle 650 mL parfumée Pomme\r\n', 'https://www.judy.tn/wp-content/uploads/2015/11/slide_vassl2.png', 'Judy Vaisselle nettoie et dégraisse en profondeur toute la vaisselle.\r\n', 5000, 1500, '650'),
(5, 1, 'Judy Vaisselle 1.25L parfumée Pomme\r\n', 'https://www.judy.tn/wp-content/uploads/2015/11/slide_vassl2.png', 'Judy Vaisselle nettoie et dégraisse en profondeur toute la vaisselle.\r\n', 5000, 2200, '1'),
(6, 1, 'Judy Vaisselle 650mL parfumée Framboise\r\n', 'https://www.savanna.tn/48625/judy-liquide-vaisselles-mains-framboise-325ml.jpg', 'Judy Vaisselle nettoie et dégraisse en profondeur toute la vaisselle.\r\n', 5000, 1500, '650'),
(7, 1, 'Judy Vaisselle 1.25L parfumée Framboise\r\n', 'https://www.judy.tn/wp-content/uploads/2015/11/slide_vassl3.png', 'Judy Vaisselle nettoie et dégraisse en profondeur toute la vaisselle.\r\n', 2000, 2200, '1'),
(8, 2, 'Judy Javel 1.5L\r\n', 'https://www.judy.tn/wp-content/uploads/2019/09/javel1.jpg', 'Judy Javel désinfecte totalement la maison, blanchit le linge et élimine les mauvaises odeurs.', 6000, 1400, '2'),
(9, 2, 'Judy Javel 3L\r\n', 'https://www.judy.tn/wp-content/uploads/2019/09/javel4.jpg', 'Judy Javel désinfecte totalement la maison, blanchit le linge et élimine les mauvaises odeurs.', 3000, 4000, '3'),
(10, 2, 'Judy Javel 4.75L\r\n', 'https://mountik.com/1939-large_default/javel-judy-475l.jpg', 'Judy Javel désinfecte totalement la maison, blanchit le linge et élimine les mauvaises odeurs.', 5000, 6000, '5'),
(11, 3, 'Judy Clorogel 800mL\r\n', 'https://www.judy.tn/wp-content/uploads/2020/01/GM.png', 'Judy Clorogel permet de blanchir, désodoriser, détacher et dégraisser en apportant une fraîcheur agréable à la maison.', 2000, 1350, '800'),
(12, 4, 'Judy Sols & Surfaces Citron 0.8L\r\n', 'https://www.judy.tn/wp-content/uploads/2018/12/sf21.png', 'Judy Sols & Surfaces nettoie et parfume toutes les surfaces lavables de la maison sols, sanitaires, cuisinières, meubles de jardin…', 5000, 1400, '1'),
(13, 4, 'Judy Sols & Surfaces Citron 1.2L', 'https://shopline.tn/wp-content/uploads/2021/03/Judy-Nettoyant-Sols-et-Surfaces-Citron.png', 'Judy Sols & Surfaces nettoie et parfume toutes les surfaces lavables de la maison sols, sanitaires, cuisinières, meubles de jardin…', 2000, 2100, '1'),
(14, 4, 'Judy Sols & Surfaces Lavande 0.8L', 'https://must-clean.tn/wp-content/uploads/2021/02/Judy-Sols-Surfaces-Lavande-0.8L-600x600.png', 'Judy Sols & Surfaces nettoie et parfume toutes les surfaces lavables de la maison sols, sanitaires, cuisinières, meubles de jardin…', 2000, 1400, '1'),
(15, 4, 'Judy Sols & Surfaces Brise 800mL', 'https://www.savanna.tn/92366/judy-nettoyant-sol-et-surface-brise-800ml.jpg', 'Judy Sols & Surfaces nettoie et parfume toutes les surfaces lavables de la maison sols, sanitaires, cuisinières, meubles de jardin…', 6000, 1400, '1'),
(16, 5, 'Judy Décapant 1L', 'https://tdiscount.tn/22240-original/decapant-judy-1l-.jpg', 'Judy Décapant nettoie, détache et rénove les sols en carrelage, il élimine les voiles de ciments, les restes de mortier, les traces de chaux et le tartre. ', 1500, 2000, '1'),
(17, 5, 'Judy Décapant 5L', 'https://www.savanna.tn/92335-large_default/judy-decapant-nettoyant-sol-5l.jpg', 'Judy Décapant nettoie, détache et rénove les sols en carrelage, il élimine les voiles de ciments, les restes de mortier, les traces de chaux et le tartre. ', 5000, 4700, '5'),
(18, 6, 'Judy Nettoyant Vitres 250mL', 'https://www.judy.tn/wp-content/uploads/2015/11/vire250ml.jpg', 'Judy Nettoyant vitres assure à vos vitres une brillance sans précédent.', 5000, 1600, '250'),
(19, 6, 'Judy Nettoyant Vitres 500mL', 'https://tdiscount.tn/22324-large_default/nettoyant-vitre-triple-action-recharge-bleu-judy-500-ml.jpg', 'Judy Nettoyant vitres assure à vos vitres une brillance sans précédent.', 3000, 1950, '500'),
(20, 6, 'judy nettoyant vitres 5l', 'https://www.talos.tn/29231-large_default/judy-vitre-5l.jpg', 'Judy Nettoyant vitres assure à vos vitres une brillance sans précédent.', 6000, 3800, '5'),
(21, 7, 'Judy Nettoyant Parfumée Océan 1.5L', 'https://www.savanna.tn/92319/judy-nettoyant-multi-usage-ocean-15l.jpg', 'Judy Nettoyant nettoie vraiment tout dans la maison : linge, vaisselle, sanitaire, sols et surfaces, meubles de jardin …', 2000, 2400, '2'),
(22, 7, 'Judy Nettoyant Parfumée Océan 3L', 'https://www.savanna.tn/92320-medium_default/judy-nettoyant-multi-usage-ocean-3l.jpg', 'Judy Nettoyant nettoie vraiment tout dans la maison : linge, vaisselle, sanitaire, sols et surfaces, meubles de jardin …', 2000, 4500, '3'),
(23, 7, 'Judy Nettoyant Parfumée Citron 1.5L', 'https://clickandcollect.monoprix.tn/ennasr/44445-home_default/nettoyant-multiusage.jpg', 'Judy Nettoyant nettoie vraiment tout dans la maison : linge, vaisselle, sanitaire, sols et surfaces, meubles de jardin …', 3000, 2400, '2'),
(24, 7, 'Judy Nettoyant Parfumée Citron 3L', 'https://tdiscount.tn/22204-original/nettoyant-citron-judy-3-l.jpg', 'Judy Nettoyant nettoie vraiment tout dans la maison : linge, vaisselle, sanitaire, sols et surfaces, meubles de jardin …', 3000, 4500, '3'),
(25, 8, 'Judy Nettoyant Extra Fort\r\n', 'https://www.judy.tn/wp-content/uploads/2019/02/netg.png', 'Judy Nettoyant  Extra Fort  est conçu pour le nettoyage de toute la maison: vaisselle,  linge, sols, sanitaires… Il dégraisse et parfume, tout en gardant la douceur de vos mains.', 3000, 3200, '3'),
(26, 9, 'Judy Linge 2L', 'https://www.savanna.tn/92292-medium_default/judy-lessive-linge-mains-et-machine-semi-automatique-2l.', 'Judy Linge au savon, assure la propreté du linge aussi bien en lavage manuel ou dans une machine semi automatique.\r\n', 3000, 1900, '1'),
(27, 9, 'Judy Linge 4L', 'https://www.livrini.tn/public/uploads/1587480709-h-250-lingeg1.png', 'Judy Linge au savon, assure la propreté du linge aussi bien en lavage manuel ou dans une machine semi automatique.\r\n', 2000, 5500, '4'),
(28, 10, 'Judy Linge Automatique 3L', 'https://www.judy.tn/wp-content/uploads/2020/03/g.png', 'Judy Linge Automatique est un détergent liquide destiné au lavage automatique ou manuel de tout type de linge. Judy Linge Automatique nettoie et parfume tous les types de tissus, ', 5000, 5000, '3'),
(29, 11, 'judy déboucheur 300g', 'https://tdiscount.tn/22278-original/deboucheur-judy-300-g.jpg', 'Judy Déboucheur évite les engorgements, détruit les matières organiques et les cheveux qui obstruent vos canalisations. Avec Judy Déboucheur finit les mauvaises odeurs !', 3000, 2400, '300'),
(30, 11, 'judy déboucheur 1L', 'https://www.judy.tn/wp-content/uploads/2016/09/Deboucheur2.jpg', 'Judy Déboucheur évite les engorgements, détruit les matières organiques et les cheveux qui obstruent vos canalisations. Avec Judy Déboucheur finit les mauvaises odeurs !', 2100, 3100, '1'),
(31, 12, 'Judy Détartrant Marine 500mL', 'https://capcomshop.com/wp-content/uploads/2018/01/marine-1.jpg', 'Judy Détartrant adhère parfaitement à la paroi des toilettes pour un détartrage maximal. ', 3000, 3400, '500'),
(32, 12, 'Judy Détartrant Marine 750mL', 'https://www.savanna.tn/92391-large_default/judy-gel-detartrant-3en1-750ml.jpg', 'Judy Détartrant adhère parfaitement à la paroi des toilettes pour un détartrage maximal. ', 2000, 4500, '750'),
(33, 12, 'Judy Détartrant Floral 500mL', 'https://capcomshop.com/wp-content/uploads/2018/01/floral-1.jpg ', 'Judy Détartrant adhère parfaitement à la paroi des toilettes pour un détartrage maximal. ', 3000, 3400, '500'),
(34, 12, 'Judy Détartrant Pêche 500 mL', 'https://tdiscount.tn/22255-home_default/detartrant-peche-judy-500-ml.jpg', 'Judy Détartrant adhère parfaitement à la paroi des toilettes pour un détartrage maximal. ', 2000, 2800, '500');

-- --------------------------------------------------------

--
-- Table structure for table `question`
--

CREATE TABLE `question` (
  `id` int(11) NOT NULL,
  `id_client` int(11) NOT NULL,
  `contenu_question` text NOT NULL,
  `date_creation` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `reclamation`
--

CREATE TABLE `reclamation` (
  `id` int(11) NOT NULL,
  `id_client` int(11) NOT NULL,
  `sens` varchar(10) NOT NULL,
  `contenu` text NOT NULL,
  `date_creation` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categorie`
--
ALTER TABLE `categorie`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `gamme`
--
ALTER TABLE `gamme`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_categorie` (`id_categorie`);

--
-- Indexes for table `produit`
--
ALTER TABLE `produit`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_gamme` (`id_gamme`);

--
-- Indexes for table `question`
--
ALTER TABLE `question`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_client` (`id_client`);

--
-- Indexes for table `reclamation`
--
ALTER TABLE `reclamation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_client` (`id_client`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categorie`
--
ALTER TABLE `categorie`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `client`
--
ALTER TABLE `client`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `gamme`
--
ALTER TABLE `gamme`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `produit`
--
ALTER TABLE `produit`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `question`
--
ALTER TABLE `question`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `reclamation`
--
ALTER TABLE `reclamation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `gamme`
--
ALTER TABLE `gamme`
  ADD CONSTRAINT `gamme_ibfk_1` FOREIGN KEY (`id_categorie`) REFERENCES `categorie` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `produit`
--
ALTER TABLE `produit`
  ADD CONSTRAINT `produit_ibfk_1` FOREIGN KEY (`id_gamme`) REFERENCES `gamme` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `question`
--
ALTER TABLE `question`
  ADD CONSTRAINT `question_ibfk_1` FOREIGN KEY (`id_client`) REFERENCES `client` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
