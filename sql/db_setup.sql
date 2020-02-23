CREATE TABLE IF NOT EXISTS satellites (
`id` VARCHAR(10) NOT NULL,
`name` VARCHAR(255) NOT NULL,
`measurement` VARCHAR(255) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8
;

CREATE TABLE IF NOT EXISTS file_import (
`id` INT NOT NULL,
`filename` VARCHAR(255) NOT NULL,
`start_dt` DATETIME NOT NULL,
`end_dt` DATETIME NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8
;

CREATE TABLE IF NOT EXISTS sat_data (
`id` INT NOT NULL,
`file_import_id` INT NOT NULL,
`satellite_id` VARCHAR(10) NOT NULL,
`measurement_dt` DATETIME NOT NULL,
`ionosphere` FLOAT DEFAULT NULL,
`ndvi` FLOAT DEFAULT NULL,
`radiation` FLOAT DEFAULT NULL,
`measurement` VARCHAR(255) DEFAULT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8
;
