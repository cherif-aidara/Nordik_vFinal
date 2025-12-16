-- ===========================================
-- EXPORT BASE DE DONNÉES NORDIK ADVENTURES
-- TP#3 - INF23307
-- ===========================================

-- Ce fichier contient la structure et les données de la base de données SQLite
-- Pour l'importer dans MySQL/PostgreSQL, vous devrez adapter les types de données


-- ===========================================
-- Table: django_migrations
-- ===========================================

CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL
);

-- Données pour la table django_migrations
INSERT INTO `django_migrations` VALUES
(1, 'contenttypes', '0001_initial', '2025-11-19 14:02:02.617103'),
(2, 'auth', '0001_initial', '2025-11-19 14:02:02.650344'),
(3, 'admin', '0001_initial', '2025-11-19 14:02:02.707121'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-11-19 14:02:02.762808'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-11-19 14:02:02.801501'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-11-19 14:02:02.843511'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-11-19 14:02:02.886223'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-11-19 14:02:02.913866'),
(9, 'auth', '0004_alter_user_username_opts', '2025-11-19 14:02:02.930146'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-11-19 14:02:02.949530'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-11-19 14:02:02.953083'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-11-19 14:02:02.964773'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-11-19 14:02:02.980397'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-11-19 14:02:02.995308'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-11-19 14:02:03.005677'),
(16, 'auth', '0011_update_proxy_permissions', '2025-11-19 14:02:03.017372'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-11-19 14:02:03.030742'),
(18, 'sessions', '0001_initial', '2025-11-19 14:02:03.040485'),
(19, 'pgi', '0001_initial', '2025-11-19 14:06:11.453063'),
(20, 'stocks', '0001_initial', '2025-12-13 04:52:09.696137'),
(21, 'clients', '0001_initial', '2025-12-13 04:52:09.774608'),
(22, 'finances', '0001_initial', '2025-12-13 04:52:09.831737');


-- ===========================================
-- Table: auth_group_permissions
-- ===========================================

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `group_id` INTEGER NOT NULL,
  `permission_id` INTEGER NOT NULL
);

-- Aucune donnée dans la table auth_group_permissions


-- ===========================================
-- Table: auth_user_groups
-- ===========================================

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `user_id` INTEGER NOT NULL,
  `group_id` INTEGER NOT NULL
);

-- Aucune donnée dans la table auth_user_groups


-- ===========================================
-- Table: auth_user_user_permissions
-- ===========================================

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `user_id` INTEGER NOT NULL,
  `permission_id` INTEGER NOT NULL
);

-- Aucune donnée dans la table auth_user_user_permissions


-- ===========================================
-- Table: django_admin_log
-- ===========================================

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `object_id` TEXT,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` TEXT NOT NULL,
  `content_type_id` INTEGER,
  `user_id` INTEGER NOT NULL,
  `action_time` datetime NOT NULL
);

-- Aucune donnée dans la table django_admin_log


-- ===========================================
-- Table: django_content_type
-- ===========================================

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
);

-- Données pour la table django_content_type
INSERT INTO `django_content_type` VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'pgi', 'productcategory'),
(8, 'pgi', 'supplier'),
(9, 'pgi', 'product'),
(10, 'stocks', 'productcategory'),
(11, 'stocks', 'stockmovement'),
(12, 'stocks', 'supplier'),
(13, 'stocks', 'product'),
(14, 'finances', 'invoice'),
(15, 'finances', 'invoicelineitem'),
(16, 'finances', 'cashflow'),
(17, 'finances', 'expense'),
(18, 'clients', 'client'),
(19, 'clients', 'clientorder'),
(20, 'clients', 'clientinteraction'),
(21, 'clients', 'orderrating'),
(22, 'clients', 'orderlineitem'),
(23, 'clients', 'cart'),
(24, 'clients', 'clientactivitylog'),
(25, 'clients', 'cartitem');


-- ===========================================
-- Table: auth_permission
-- ===========================================

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `content_type_id` INTEGER NOT NULL,
  `codename` varchar(100) NOT NULL,
  `name` varchar(255) NOT NULL
);

-- Données pour la table auth_permission
INSERT INTO `auth_permission` VALUES
(1, 1, 'add_logentry', 'Can add log entry'),
(2, 1, 'change_logentry', 'Can change log entry'),
(3, 1, 'delete_logentry', 'Can delete log entry'),
(4, 1, 'view_logentry', 'Can view log entry'),
(5, 2, 'add_permission', 'Can add permission'),
(6, 2, 'change_permission', 'Can change permission'),
(7, 2, 'delete_permission', 'Can delete permission'),
(8, 2, 'view_permission', 'Can view permission'),
(9, 3, 'add_group', 'Can add group'),
(10, 3, 'change_group', 'Can change group'),
(11, 3, 'delete_group', 'Can delete group'),
(12, 3, 'view_group', 'Can view group'),
(13, 4, 'add_user', 'Can add user'),
(14, 4, 'change_user', 'Can change user'),
(15, 4, 'delete_user', 'Can delete user'),
(16, 4, 'view_user', 'Can view user'),
(17, 5, 'add_contenttype', 'Can add content type'),
(18, 5, 'change_contenttype', 'Can change content type'),
(19, 5, 'delete_contenttype', 'Can delete content type'),
(20, 5, 'view_contenttype', 'Can view content type'),
(21, 6, 'add_session', 'Can add session'),
(22, 6, 'change_session', 'Can change session'),
(23, 6, 'delete_session', 'Can delete session'),
(24, 6, 'view_session', 'Can view session'),
(25, 7, 'add_productcategory', 'Can add Catégorie de produit'),
(26, 7, 'change_productcategory', 'Can change Catégorie de produit'),
(27, 7, 'delete_productcategory', 'Can delete Catégorie de produit'),
(28, 7, 'view_productcategory', 'Can view Catégorie de produit'),
(29, 8, 'add_supplier', 'Can add Fournisseur'),
(30, 8, 'change_supplier', 'Can change Fournisseur'),
(31, 8, 'delete_supplier', 'Can delete Fournisseur'),
(32, 8, 'view_supplier', 'Can view Fournisseur'),
(33, 9, 'add_product', 'Can add Produit'),
(34, 9, 'change_product', 'Can change Produit'),
(35, 9, 'delete_product', 'Can delete Produit'),
(36, 9, 'view_product', 'Can view Produit'),
(37, 10, 'add_productcategory', 'Can add Catégorie de produit'),
(38, 10, 'change_productcategory', 'Can change Catégorie de produit'),
(39, 10, 'delete_productcategory', 'Can delete Catégorie de produit'),
(40, 10, 'view_productcategory', 'Can view Catégorie de produit'),
(41, 11, 'add_stockmovement', 'Can add Mouvement de stock'),
(42, 11, 'change_stockmovement', 'Can change Mouvement de stock'),
(43, 11, 'delete_stockmovement', 'Can delete Mouvement de stock'),
(44, 11, 'view_stockmovement', 'Can view Mouvement de stock'),
(45, 12, 'add_supplier', 'Can add Fournisseur'),
(46, 12, 'change_supplier', 'Can change Fournisseur'),
(47, 12, 'delete_supplier', 'Can delete Fournisseur'),
(48, 12, 'view_supplier', 'Can view Fournisseur'),
(49, 13, 'add_product', 'Can add Produit'),
(50, 13, 'change_product', 'Can change Produit'),
(51, 13, 'delete_product', 'Can delete Produit'),
(52, 13, 'view_product', 'Can view Produit'),
(53, 14, 'add_invoice', 'Can add Facture'),
(54, 14, 'change_invoice', 'Can change Facture'),
(55, 14, 'delete_invoice', 'Can delete Facture'),
(56, 14, 'view_invoice', 'Can view Facture'),
(57, 15, 'add_invoicelineitem', 'Can add Ligne de facture'),
(58, 15, 'change_invoicelineitem', 'Can change Ligne de facture'),
(59, 15, 'delete_invoicelineitem', 'Can delete Ligne de facture'),
(60, 15, 'view_invoicelineitem', 'Can view Ligne de facture'),
(61, 16, 'add_cashflow', 'Can add Flux de trésorerie'),
(62, 16, 'change_cashflow', 'Can change Flux de trésorerie'),
(63, 16, 'delete_cashflow', 'Can delete Flux de trésorerie'),
(64, 16, 'view_cashflow', 'Can view Flux de trésorerie'),
(65, 17, 'add_expense', 'Can add Dépense'),
(66, 17, 'change_expense', 'Can change Dépense'),
(67, 17, 'delete_expense', 'Can delete Dépense'),
(68, 17, 'view_expense', 'Can view Dépense'),
(69, 18, 'add_client', 'Can add Client'),
(70, 18, 'change_client', 'Can change Client'),
(71, 18, 'delete_client', 'Can delete Client'),
(72, 18, 'view_client', 'Can view Client'),
(73, 19, 'add_clientorder', 'Can add Commande client'),
(74, 19, 'change_clientorder', 'Can change Commande client'),
(75, 19, 'delete_clientorder', 'Can delete Commande client'),
(76, 19, 'view_clientorder', 'Can view Commande client'),
(77, 20, 'add_clientinteraction', 'Can add Interaction client'),
(78, 20, 'change_clientinteraction', 'Can change Interaction client'),
(79, 20, 'delete_clientinteraction', 'Can delete Interaction client'),
(80, 20, 'view_clientinteraction', 'Can view Interaction client'),
(81, 21, 'add_orderrating', 'Can add Évaluation de commande'),
(82, 21, 'change_orderrating', 'Can change Évaluation de commande'),
(83, 21, 'delete_orderrating', 'Can delete Évaluation de commande'),
(84, 21, 'view_orderrating', 'Can view Évaluation de commande'),
(85, 22, 'add_orderlineitem', 'Can add Ligne de commande'),
(86, 22, 'change_orderlineitem', 'Can change Ligne de commande'),
(87, 22, 'delete_orderlineitem', 'Can delete Ligne de commande'),
(88, 22, 'view_orderlineitem', 'Can view Ligne de commande'),
(89, 23, 'add_cart', 'Can add Panier'),
(90, 23, 'change_cart', 'Can change Panier'),
(91, 23, 'delete_cart', 'Can delete Panier'),
(92, 23, 'view_cart', 'Can view Panier'),
(93, 24, 'add_clientactivitylog', 'Can add Journal d''activité client'),
(94, 24, 'change_clientactivitylog', 'Can change Journal d''activité client'),
(95, 24, 'delete_clientactivitylog', 'Can delete Journal d''activité client'),
(96, 24, 'view_clientactivitylog', 'Can view Journal d''activité client'),
(97, 25, 'add_cartitem', 'Can add Article de panier'),
(98, 25, 'change_cartitem', 'Can change Article de panier'),
(99, 25, 'delete_cartitem', 'Can delete Article de panier'),
(100, 25, 'view_cartitem', 'Can view Article de panier');


-- ===========================================
-- Table: auth_group
-- ===========================================

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `name` varchar(150) NOT NULL
);

-- Aucune donnée dans la table auth_group


-- ===========================================
-- Table: auth_user
-- ===========================================

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime,
  `is_superuser` bool NOT NULL,
  `username` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` bool NOT NULL,
  `is_active` bool NOT NULL,
  `date_joined` datetime NOT NULL,
  `first_name` varchar(150) NOT NULL
);

-- Données pour la table auth_user
INSERT INTO `auth_user` VALUES
(1, 'pbkdf2_sha256$870000$fpbJlAmO40fDjT09w7MBDn$0N2A3L76gsKpOsfawfhcJzrnB+x8rceQSD7pYUU7UNw=', NULL, 1, 'tass', '', 'hammaditassadit03@gmail.com', 1, 1, '2025-11-19 14:03:17.455274', ''),
(2, 'pbkdf2_sha256$870000$4LCNSg06KSpoxMKjhJL4DG$n5tv/PeOVHKul3ELhrOSUo1z6fVMejjtw8JBuyI0fuY=', NULL, 1, 'hp', '', 'hammaditassadit03@gmail.com', 1, 1, '2025-11-19 14:06:55.015557', '');


-- ===========================================
-- Table: django_session
-- ===========================================

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) PRIMARY KEY NOT NULL,
  `session_data` TEXT NOT NULL,
  `expire_date` datetime NOT NULL
);

-- Aucune donnée dans la table django_session


-- ===========================================
-- Table: pgi_productcategory
-- ===========================================

CREATE TABLE IF NOT EXISTS `pgi_productcategory` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `name` varchar(100) NOT NULL
);

-- Données pour la table pgi_productcategory
INSERT INTO `pgi_productcategory` VALUES
(1, 'Tentes & abris'),
(2, 'Sacs & portage'),
(3, 'Vêtements techniques'),
(4, 'Accessoires & cuisine'),
(5, 'Électronique & navigation');


-- ===========================================
-- Table: pgi_supplier
-- ===========================================

CREATE TABLE IF NOT EXISTS `pgi_supplier` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `name` varchar(150) NOT NULL,
  `code` varchar(50) NOT NULL,
  `default_discount` decimal NOT NULL,
  `delivery_delay_days` integer unsigned NOT NULL
);

-- Données pour la table pgi_supplier
INSERT INTO `pgi_supplier` VALUES
(1, 'AdventureX', 'AX-001', 5, 10),
(2, 'AdventureX', 'AX-002', 5, 14),
(3, 'TrekSupply', 'TS-001', 4, 7),
(4, 'MontNord', 'MN-001', 3, 6),
(5, 'AdventureX', 'AX-003', 5, 9),
(6, 'TrekSupply', 'TS-002', 4, 5),
(7, 'NordPack', 'NP-001', 6, 8),
(8, 'NordPack', 'NP-002', 6, 7),
(9, 'MontNord', 'MN-002', 3, 10),
(10, 'MontNord', 'MN-003', 3, 6),
(11, 'TrekSupply', 'TS-003', 4, 5),
(12, 'TrekSupply', 'TS-004', 4, 9),
(13, 'NordWear', 'NW-001', 5, 6),
(14, 'NordWear', 'NW-002', 5, 6),
(15, 'NordWear', 'NW-003', 5, 8),
(16, 'NordWear', 'NW-004', 5, 8),
(17, 'ArcticLine', 'AL-001', 4, 10),
(18, 'ArcticLine', 'AL-002', 4, 5),
(19, 'ArcticLine', 'AL-003', 4, 6),
(20, 'TrekSupply', 'TS-005', 4, 7),
(21, 'MontNord', 'MN-004', 3, 5),
(22, 'AdventureX', 'AX-004', 5, 6),
(23, 'TrekSupply', 'TS-006', 4, 7),
(24, 'AdventureX', 'AX-005', 5, 8),
(25, 'NordPack', 'NP-003', 6, 6),
(26, 'TechTrail', 'TT-001', 4, 12),
(27, 'TechTrail', 'TT-002', 4, 8),
(28, 'TrekSupply', 'TS-007', 4, 5),
(29, 'TechTrail', 'TT-003', 4, 7),
(30, 'TechTrail', 'TT-004', 4, 5);


-- ===========================================
-- Table: pgi_product
-- ===========================================

CREATE TABLE IF NOT EXISTS `pgi_product` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `sku` varchar(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `purchase_cost` decimal NOT NULL,
  `sale_price` decimal NOT NULL,
  `gross_margin_percent` decimal NOT NULL,
  `quantity_in_stock` integer unsigned NOT NULL,
  `reorder_threshold` integer unsigned NOT NULL,
  `safety_stock` integer unsigned NOT NULL,
  `supplier_discount` decimal NOT NULL,
  `weight_kg` decimal NOT NULL,
  `stock_entry_date` date NOT NULL,
  `warehouse_location` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `category_id` bigint NOT NULL,
  `supplier_id` bigint NOT NULL
);

-- Données pour la table pgi_product
INSERT INTO `pgi_product` VALUES
(1, '2025-11-19 23:46:48.985620', '2025-11-19 23:46:48.985649', 'NC-TNT-001', 'Tente légère 2 places', 145, 299, 51.5, 18, 5, 3, 5, 2.8, '2025-03-02', 'A1', 'active', 1, 1),
(2, '2025-11-19 23:46:49.002683', '2025-11-19 23:46:49.002704', 'NC-TNT-002', 'Tente familiale 6 places', 260, 499, 47.9, 9, 3, 2, 5, 6.5, '2025-02-18', 'A1', 'active', 1, 2),
(3, '2025-11-19 23:46:49.013207', '2025-11-19 23:46:49.013229', 'NC-TNT-003', 'Toile imperméable 3x3 m', 25, 59, 57.6, 25, 8, 5, 4, 1.1, '2025-03-10', 'A2', 'active', 1, 3),
(4, '2025-11-19 23:46:49.024208', '2025-11-19 23:46:49.024227', 'NC-TNT-004', 'Tapis de sol isolant', 18, 39, 53.8, 40, 10, 6, 3, 0.9, '2025-03-05', 'A2', 'active', 1, 4),
(5, '2025-11-19 23:46:49.033017', '2025-11-19 23:46:49.033036', 'NC-TNT-005', 'Abri cuisine pliable', 75, 149, 49.7, 12, 4, 3, 5, 5, '2025-02-20', 'A1', 'active', 1, 5),
(6, '2025-11-19 23:46:49.041907', '2025-11-19 23:46:49.041926', 'NC-TNT-006', 'Mât télescopique alu', 12, 29, 58.6, 30, 10, 6, 4, 0.7, '2025-03-08', 'A3', 'active', 1, 6),
(7, '2025-11-19 23:46:49.053842', '2025-11-19 23:46:49.053859', 'NC-SAC-001', 'Sac à dos 50 L étanche', 65, 139, 53.2, 20, 6, 4, 6, 1.3, '2025-03-12', 'B1', 'active', 2, 7),
(8, '2025-11-19 23:46:49.062017', '2025-11-19 23:46:49.062035', 'NC-SAC-002', 'Sac de jour 25 L', 32, 79, 59.5, 25, 8, 5, 6, 0.9, '2025-03-10', 'B2', 'active', 2, 8),
(9, '2025-11-19 23:46:49.069842', '2025-11-19 23:46:49.069860', 'NC-SAC-003', 'Sac de couchage -10°C', 80, 169, 52.7, 15, 5, 3, 3, 2.2, '2025-02-25', 'B3', 'active', 2, 9),
(10, '2025-11-19 23:46:49.078199', '2025-11-19 23:46:49.078217', 'NC-SAC-004', 'Tapis autogonflant', 25, 59, 57.6, 35, 10, 5, 3, 1.1, '2025-03-05', 'B3', 'active', 2, 10),
(11, '2025-11-19 23:46:49.086037', '2025-11-19 23:46:49.086054', 'NC-SAC-005', 'Housse imperméable sac à dos', 9, 19, 52.6, 40, 10, 6, 4, 0.4, '2025-03-11', 'B2', 'active', 2, 11),
(12, '2025-11-19 23:46:49.094033', '2025-11-19 23:46:49.094051', 'NC-SAC-006', 'Bâtons de marche carbone', 35, 79, 55.7, 18, 5, 3, 4, 0.8, '2025-02-28', 'B1', 'active', 2, 12),
(13, '2025-11-19 23:46:49.106749', '2025-11-19 23:46:49.106767', 'NC-VET-001', 'Chandail thermique homme', 22, 59, 62.7, 50, 15, 10, 5, 0.6, '2025-03-09', 'C1', 'active', 3, 13),
(14, '2025-11-19 23:46:49.114997', '2025-11-19 23:46:49.115016', 'NC-VET-002', 'Chandail thermique femme', 22, 59, 62.7, 48, 15, 10, 5, 0.6, '2025-03-09', 'C1', 'active', 3, 14),
(15, '2025-11-19 23:46:49.123546', '2025-11-19 23:46:49.123565', 'NC-VET-003', 'Pantalon de randonnée homme', 38, 89, 57.3, 30, 8, 4, 5, 0.8, '2025-03-03', 'C2', 'active', 3, 15),
(16, '2025-11-19 23:46:49.132937', '2025-11-19 23:46:49.132954', 'NC-VET-004', 'Pantalon de randonnée femme', 38, 89, 57.3, 32, 8, 4, 5, 0.8, '2025-03-03', 'C2', 'active', 3, 16),
(17, '2025-11-19 23:46:49.141384', '2025-11-19 23:46:49.141402', 'NC-VET-005', 'Manteau coupe-vent', 55, 129, 57.4, 20, 5, 3, 4, 1.1, '2025-02-19', 'C3', 'active', 3, 17),
(18, '2025-11-19 23:46:49.149772', '2025-11-19 23:46:49.149790', 'NC-VET-006', 'Tuque en laine mérinos', 10, 29, 65.5, 40, 10, 6, 4, 0.3, '2025-03-10', 'C4', 'active', 3, 18),
(19, '2025-11-19 23:46:49.157898', '2025-11-19 23:46:49.157918', 'NC-VET-007', 'Gants isolants Hiver+', 18, 45, 60, 25, 8, 4, 4, 0.5, '2025-02-22', 'C4', 'active', 3, 19),
(20, '2025-11-19 23:46:49.169568', '2025-11-19 23:46:49.169586', 'NC-ACC-001', 'Réchaud portatif', 25, 59, 57.6, 20, 5, 3, 4, 0.9, '2025-02-28', 'D1', 'active', 4, 20),
(21, '2025-11-19 23:46:49.178592', '2025-11-19 23:46:49.178610', 'NC-ACC-002', 'Bouteille isotherme 1L', 12, 29, 58.6, 40, 12, 8, 3, 0.4, '2025-03-10', 'D2', 'active', 4, 21),
(22, '2025-11-19 23:46:49.186629', '2025-11-19 23:46:49.186649', 'NC-ACC-003', 'Lampe frontale 300 lumens', 14, 39, 64.1, 35, 10, 6, 5, 0.2, '2025-03-12', 'D3', 'active', 4, 22),
(23, '2025-11-19 23:46:49.196067', '2025-11-19 23:46:49.196085', 'NC-ACC-004', 'Ensemble vaisselle 4 pers.', 20, 49, 59.2, 25, 8, 3, 4, 1.2, '2025-03-06', 'D2', 'active', 4, 23),
(24, '2025-11-19 23:46:49.204028', '2025-11-19 23:46:49.204046', 'NC-ACC-005', 'Filtre à eau compact', 28, 69, 59.4, 18, 5, 3, 5, 0.7, '2025-02-25', 'D3', 'active', 4, 24),
(25, '2025-11-19 23:46:49.212942', '2025-11-19 23:46:49.212959', 'NC-ACC-006', 'Couteau multifonction', 15, 39, 61.5, 28, 10, 6, 6, 0.5, '2025-03-09', 'D4', 'active', 4, 25),
(26, '2025-11-19 23:46:49.225092', '2025-11-19 23:46:49.225110', 'NC-ELE-001', 'Montre GPS plein air', 120, 279, 56.9, 10, 3, 2, 4, 0.9, '2025-02-17', 'E1', 'active', 5, 26),
(27, '2025-11-19 23:46:49.233099', '2025-11-19 23:46:49.233116', 'NC-ELE-002', 'Chargeur solaire 20W', 35, 79, 55.7, 18, 5, 3, 4, 0.6, '2025-03-01', 'E2', 'active', 5, 27),
(28, '2025-11-19 23:46:49.241777', '2025-11-19 23:46:49.241796', 'NC-ELE-003', 'Boussole de précision', 9, 24, 62.5, 40, 12, 8, 4, 0.2, '2025-03-11', 'E3', 'active', 5, 28),
(29, '2025-11-19 23:46:49.251483', '2025-11-19 23:46:49.251501', 'NC-ELE-004', 'Radio météo portable', 22, 49, 55.1, 15, 5, 3, 4, 0.8, '2025-02-28', 'E4', 'active', 5, 29),
(30, '2025-11-19 23:46:49.260337', '2025-11-19 23:46:49.260356', 'NC-ELE-005', 'Lampe USB rechargeable', 11, 25, 56, 35, 10, 6, 4, 0.3, '2025-03-07', 'E5', 'active', 5, 30);


-- ===========================================
-- Table: stocks_productcategory
-- ===========================================

CREATE TABLE IF NOT EXISTS `stocks_productcategory` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` TEXT NOT NULL
);

-- Aucune donnée dans la table stocks_productcategory


-- ===========================================
-- Table: stocks_supplier
-- ===========================================

CREATE TABLE IF NOT EXISTS `stocks_supplier` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `name` varchar(150) NOT NULL,
  `code` varchar(50) NOT NULL,
  `default_discount` decimal NOT NULL,
  `delivery_delay_days` integer unsigned NOT NULL
);

-- Aucune donnée dans la table stocks_supplier


-- ===========================================
-- Table: stocks_product
-- ===========================================

CREATE TABLE IF NOT EXISTS `stocks_product` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `sku` varchar(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` TEXT NOT NULL,
  `image` varchar(100),
  `purchase_cost` decimal NOT NULL,
  `sale_price` decimal NOT NULL,
  `gross_margin_percent` decimal NOT NULL,
  `quantity_in_stock` integer unsigned NOT NULL,
  `reorder_threshold` integer unsigned NOT NULL,
  `safety_stock` integer unsigned NOT NULL,
  `supplier_discount` decimal NOT NULL,
  `weight_kg` decimal NOT NULL,
  `stock_entry_date` date NOT NULL,
  `warehouse_location` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `category_id` bigint NOT NULL,
  `supplier_id` bigint NOT NULL
);

-- Aucune donnée dans la table stocks_product


-- ===========================================
-- Table: stocks_stockmovement
-- ===========================================

CREATE TABLE IF NOT EXISTS `stocks_stockmovement` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `movement_type` varchar(10) NOT NULL,
  `quantity` integer unsigned NOT NULL,
  `reason` varchar(255) NOT NULL,
  `reference` varchar(100) NOT NULL,
  `product_id` bigint NOT NULL
);

-- Aucune donnée dans la table stocks_stockmovement


-- ===========================================
-- Table: clients_client
-- ===========================================

CREATE TABLE IF NOT EXISTS `clients_client` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `address` TEXT NOT NULL,
  `client_type` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `loyalty_score` integer unsigned NOT NULL,
  `satisfaction_score` integer unsigned NOT NULL,
  `total_orders` integer unsigned NOT NULL,
  `total_spent` decimal NOT NULL,
  `last_activity_date` date,
  `notes` TEXT NOT NULL
);

-- Aucune donnée dans la table clients_client


-- ===========================================
-- Table: clients_cart
-- ===========================================

CREATE TABLE IF NOT EXISTS `clients_cart` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `client_id` bigint NOT NULL
);

-- Aucune donnée dans la table clients_cart


-- ===========================================
-- Table: clients_clientactivitylog
-- ===========================================

CREATE TABLE IF NOT EXISTS `clients_clientactivitylog` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `activity_type` varchar(20) NOT NULL,
  `description` TEXT NOT NULL,
  `page_url` varchar(200) NOT NULL,
  `document` varchar(100),
  `client_id` bigint NOT NULL,
  `user_id` INTEGER
);

-- Aucune donnée dans la table clients_clientactivitylog


-- ===========================================
-- Table: clients_clientinteraction
-- ===========================================

CREATE TABLE IF NOT EXISTS `clients_clientinteraction` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `interaction_type` varchar(20) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `description` TEXT NOT NULL,
  `interaction_date` datetime NOT NULL,
  `user_name` varchar(100) NOT NULL,
  `client_id` bigint NOT NULL
);

-- Aucune donnée dans la table clients_clientinteraction


-- ===========================================
-- Table: clients_clientorder
-- ===========================================

CREATE TABLE IF NOT EXISTS `clients_clientorder` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `order_number` varchar(50) NOT NULL,
  `order_date` date NOT NULL,
  `total_amount` decimal NOT NULL,
  `status` varchar(20) NOT NULL,
  `notes` TEXT NOT NULL,
  `client_id` bigint NOT NULL
);

-- Aucune donnée dans la table clients_clientorder


-- ===========================================
-- Table: clients_orderlineitem
-- ===========================================

CREATE TABLE IF NOT EXISTS `clients_orderlineitem` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `quantity` integer unsigned NOT NULL,
  `unit_price` decimal NOT NULL,
  `line_total` decimal NOT NULL,
  `order_id` bigint NOT NULL,
  `product_id` bigint NOT NULL
);

-- Aucune donnée dans la table clients_orderlineitem


-- ===========================================
-- Table: clients_orderrating
-- ===========================================

CREATE TABLE IF NOT EXISTS `clients_orderrating` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `rating` integer unsigned NOT NULL,
  `comment` TEXT NOT NULL,
  `order_id` bigint NOT NULL
);

-- Aucune donnée dans la table clients_orderrating


-- ===========================================
-- Table: clients_cartitem
-- ===========================================

CREATE TABLE IF NOT EXISTS `clients_cartitem` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `quantity` integer unsigned NOT NULL,
  `unit_price` decimal NOT NULL,
  `cart_id` bigint NOT NULL,
  `product_id` bigint NOT NULL
);

-- Aucune donnée dans la table clients_cartitem


-- ===========================================
-- Table: finances_expense
-- ===========================================

CREATE TABLE IF NOT EXISTS `finances_expense` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `supplier_name` varchar(255) NOT NULL,
  `expense_type` varchar(20) NOT NULL,
  `amount` decimal NOT NULL,
  `expense_date` date NOT NULL,
  `due_date` date,
  `status` varchar(20) NOT NULL,
  `reference` varchar(100) NOT NULL,
  `notes` TEXT NOT NULL
);

-- Aucune donnée dans la table finances_expense


-- ===========================================
-- Table: finances_invoice
-- ===========================================

CREATE TABLE IF NOT EXISTS `finances_invoice` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `invoice_number` varchar(50) NOT NULL,
  `client_name` varchar(255) NOT NULL,
  `client_email` varchar(254) NOT NULL,
  `amount` decimal NOT NULL,
  `tps` decimal NOT NULL,
  `tvq` decimal NOT NULL,
  `total_amount` decimal NOT NULL,
  `invoice_date` date NOT NULL,
  `due_date` date NOT NULL,
  `status` varchar(20) NOT NULL,
  `notes` TEXT NOT NULL,
  `client_id` bigint
);

-- Aucune donnée dans la table finances_invoice


-- ===========================================
-- Table: finances_cashflow
-- ===========================================

CREATE TABLE IF NOT EXISTS `finances_cashflow` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `flow_type` varchar(10) NOT NULL,
  `amount` decimal NOT NULL,
  `description` varchar(255) NOT NULL,
  `flow_date` date NOT NULL,
  `related_expense_id` bigint,
  `related_invoice_id` bigint
);

-- Aucune donnée dans la table finances_cashflow


-- ===========================================
-- Table: finances_invoicelineitem
-- ===========================================

CREATE TABLE IF NOT EXISTS `finances_invoicelineitem` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `quantity` integer unsigned NOT NULL,
  `unit_price` decimal NOT NULL,
  `line_total` decimal NOT NULL,
  `invoice_id` bigint NOT NULL,
  `product_id` bigint NOT NULL
);

-- Aucune donnée dans la table finances_invoicelineitem

