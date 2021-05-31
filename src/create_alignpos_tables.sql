CREATE DATABASE alignpos;

CREATE USER alignpos IDENTIFIED BY 'valignit@2021';

GRANT ALL PRIVILEGES ON alignpos.* TO 'alignpos';

USE alignpos;

CREATE TABLE `tabItem` (
  `name` varchar(140) NOT NULL,
  `item_code` varchar(140) DEFAULT NULL,
  `item_name` varchar(140) DEFAULT NULL,
  `item_group` varchar(140) DEFAULT NULL,
  `barcode` varchar(140) DEFAULT NULL,
  `uom` varchar(140) DEFAULT NULL,
  `stock` decimal(18,6) DEFAULT NULL,
  `selling_price` decimal(18,6) DEFAULT NULL,
  `maximum_retail_price` decimal(18,6) DEFAULT NULL,
  `cgst_tax_rate` decimal(18,6) DEFAULT NULL,
  `sgst_tax_rate` decimal(18,6) DEFAULT NULL,
  `creation` datetime(6) DEFAULT NULL,
  `modified` datetime(6) DEFAULT NULL,
  `modified_by` varchar(140) DEFAULT NULL,
  `owner` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tabCustomer` (
  `name` varchar(140) NOT NULL,
  `customer_name` varchar(140) DEFAULT NULL,
  `customer_type` varchar(140) DEFAULT NULL,
  `address` varchar(140) DEFAULT NULL,
  `mobile_number` varchar(140) DEFAULT NULL,
  `loyalty_points` int(6) DEFAULT NULL,
  `creation` datetime(6) DEFAULT NULL,
  `modified` datetime(6) DEFAULT NULL,
  `modified_by` varchar(140) DEFAULT NULL,
  `owner` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tabInvoice` (
  `name` varchar(140) NOT NULL,
  `invoice_number` varchar(140) DEFAULT NULL,  
  `posting_date` datetime(6) DEFAULT NULL,
  `customer` varchar(140) DEFAULT NULL,
  `total_amount` decimal(18,6) DEFAULT NULL,  
  `discount_amount` decimal(18,6) DEFAULT NULL,
  `cgst_tax_amount` decimal(18,6) DEFAULT NULL,
  `sgst_tax_amount` decimal(18,6) DEFAULT NULL,
  `invoice_amount` decimal(18,6) DEFAULT NULL,
  `credit_note_amount` decimal(18,6) DEFAULT NULL,
  `credit_note_reference` varchar(140) DEFAULT NULL,
  `loyalty_points_redeemed` int(6) DEFAULT NULL,
  `loyalty_redeemed_amount` decimal(18,6) DEFAULT NULL,
  `paid_amount` decimal(18,6) DEFAULT NULL,
  `home_delivery` int(1) DEFAULT NULL,
  `terminal_id` varchar(140) DEFAULT NULL,  
  `approved_by` varchar(140) DEFAULT NULL,  
  `creation` datetime(6) DEFAULT NULL,
  `modified` datetime(6) DEFAULT NULL,
  `modified_by` varchar(140) DEFAULT NULL,
  `owner` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `FK_tabInvoice_tabCustomer` (`customer`),
  CONSTRAINT `FK_tabInvoice_tabCustomer` FOREIGN KEY (`customer`) REFERENCES `tabCustomer` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tabInvoice Item` (
  `parent` varchar(140) NOT NULL,
  `item_code` varchar(140) NOT NULL,
  `qty` decimal(18,6) DEFAULT NULL,
  `standard_selling_price` decimal(18,6) DEFAULT NULL,
  `applied_selling_price` decimal(18,6) DEFAULT NULL,
  `selling_amount` decimal(18,6) DEFAULT NULL,
  `cgst_tax_amount` decimal(18,6) DEFAULT NULL,
  `sgst_tax_amount` decimal(18,6) DEFAULT NULL,
  `approved_by` varchar(140) DEFAULT NULL,    
   PRIMARY KEY (`parent`,`item_code`),
  KEY `FK_tabInvoice Item_tabItem` (`item_code`),
  CONSTRAINT `FK_tabInvoice Item_tabItem` FOREIGN KEY (`item_code`) REFERENCES `tabItem` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tabInvoice Payment` (
  `parent` varchar(140) DEFAULT NULL,
  `mode_of_payment` varchar(140) DEFAULT NULL,
  `reference_no` varchar(140) DEFAULT NULL,
  `reference_date` date DEFAULT NULL,
  `received_amount` decimal(18,6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tabEstimate` (
  `name` varchar(140) NOT NULL,
  `posting_date` datetime(6) DEFAULT NULL,
  `total_amount` decimal(18,6) DEFAULT NULL,  
  `cgst_tax_amount` decimal(18,6) DEFAULT NULL,
  `sgst_tax_amount` decimal(18,6) DEFAULT NULL,
  `estimate_amount` decimal(18,6) DEFAULT NULL,
  `terminal_id` varchar(140) DEFAULT NULL,  
  `creation` datetime(6) DEFAULT NULL,
  `modified` datetime(6) DEFAULT NULL,
  `modified_by` varchar(140) DEFAULT NULL,
  `owner` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tabEstimate Item` (
  `parent` varchar(140) NOT NULL,
  `item_code` varchar(140) NOT NULL,
  `qty` decimal(18,6) DEFAULT NULL,
  `standard_selling_price` decimal(18,6) DEFAULT NULL,
  `applied_selling_price` decimal(18,6) DEFAULT NULL,
  `selling_amount` decimal(18,6) DEFAULT NULL,
  `cgst_tax_amount` decimal(18,6) DEFAULT NULL,
  `sgst_tax_amount` decimal(18,6) DEFAULT NULL,
   PRIMARY KEY (`parent`,`item_code`),
  KEY `FK_tabEstimate Item_tabItem` (`item_code`),
  CONSTRAINT `FK_tabEstimate Item_tabItem` FOREIGN KEY (`item_code`) REFERENCES `tabItem` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tabUser` (
  `user_id` varchar(140) NOT NULL,
  `password` varchar(140) NOT NULL,
  `role` varchar(140) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tabSettings` (
  `invoice_number_prefix` varchar(140) DEFAULT 'SINV-',
  `last_invoice_number` INT DEFAULT NULL,
  `last_reference_number` INT DEFAULT NULL,
  `estimate_number_prefix` varchar(140) DEFAULT 'EST-',
  `last_estimate_number` INT DEFAULT NULL,
  `conversion_factor` decimal(18,6) DEFAULT NULL  
) ENGINE=InnoDB DEFAULT CHARSET=utf8;