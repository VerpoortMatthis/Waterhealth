-- MySQL Script generated by MySQL Workbench
-- Sun May 29 22:03:22 2022
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema waterhealthDB
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema waterhealthDB
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `waterhealthDB` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
USE `waterhealthDB` ;

-- -----------------------------------------------------
-- Table `waterhealthDB`.`actie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `waterhealthDB`.`actie` (
  `code` INT NOT NULL AUTO_INCREMENT,
  `Beschrijving` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`code`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `waterhealthDB`.`device`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `waterhealthDB`.`device` (
  `onderwerp` VARCHAR(100) NOT NULL,
  `meetapparaat` VARCHAR(100) NOT NULL,
  `deviceid` VARCHAR(45) NOT NULL,
  `meeteenheid` VARCHAR(45) NULL,
  `beschrijving` VARCHAR(45) NULL,
  PRIMARY KEY (`deviceid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


-- -----------------------------------------------------
-- Table `waterhealthDB`.`meting`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `waterhealthDB`.`meting` (
  `volgnummer` INT(11) NOT NULL AUTO_INCREMENT,
  `deviceid` VARCHAR(45) NOT NULL,
  `gemeten_waarde` FLOAT NOT NULL,
  `datum` DATETIME(6) NOT NULL,
  `code` INT NULL,
  PRIMARY KEY (`volgnummer`),
  INDEX `fk_meting_actie` (`code` ASC) VISIBLE,
  INDEX `fk_meting_device1_idx` (`deviceid` ASC) VISIBLE,
  CONSTRAINT `fk_meting_actie`
    FOREIGN KEY (`code`)
    REFERENCES `waterhealthDB`.`actie` (`code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_meting_device1`
    FOREIGN KEY (`deviceid`)
    REFERENCES `waterhealthDB`.`device` (`deviceid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 55
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_unicode_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
