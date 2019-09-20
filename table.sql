SELECT 'Create Table fund_morningstar...';
DROP TABLE IF EXISTS `fund_morningstar`;
CREATE TABLE IF NOT EXISTS `fund_morningstar`
(
    `fund_code`         varchar(32)    DEFAULT ''  NOT NULL,
    `fund_name`         varchar(32)    DEFAULT ''  NOT NULL,
    `fund_type`         varchar(32)    DEFAULT ''  NOT NULL,
    `fund_rate_3`       int            DEFAULT 0   NOT NULL,
    `fund_rate_5`       int            DEFAULT 0   NOT NULL,
    `net_value`         decimal(20, 4) DEFAULT 0.0 NOT NULL,
    `daily_change`      decimal(20, 4) DEFAULT 0.0 NOT NULL,
    `returns_curr_year` decimal(20, 4) DEFAULT 0.0 NOT NULL,
    PRIMARY KEY (fund_code)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

SELECT 'Create Table fund_morningstar_select...';
DROP TABLE IF EXISTS `fund_morningstar_select`;
CREATE TABLE IF NOT EXISTS `fund_morningstar_select`
(
    `fund_code`             varchar(32)    DEFAULT ''  NOT NULL,
    `fund_name`             varchar(32)    DEFAULT ''  NOT NULL,
    `fund_type`             varchar(32)    DEFAULT ''  NOT NULL,
    `fund_rate_3`           int            DEFAULT 0   NOT NULL,
    `fund_rate_5`           int            DEFAULT 0   NOT NULL,
    `net_value`             decimal(20, 4) DEFAULT 0.0 NOT NULL,
    `daily_change`          decimal(20, 4) DEFAULT 0.0 NOT NULL,
    `returns_curr_year`     decimal(20, 4) DEFAULT 0.0 NOT NULL,

    `foundation_date`       varchar(32)    DEFAULT ''  NOT NULL,
    `subscribe_status`      varchar(32)    DEFAULT ''  NOT NULL,
    `redeem_status`         varchar(32)    DEFAULT ''  NOT NULL,
    `initial_purchase_base` varchar(32)    DEFAULT ''  NOT NULL,
    `front_load_fee`        varchar(32)    DEFAULT ''  NOT NULL,
    `defer_load_fee`        varchar(32)    DEFAULT ''  NOT NULL,
    `redemption_fee`        varchar(32)    DEFAULT ''  NOT NULL,
    `management_fee`        varchar(32)    DEFAULT ''  NOT NULL,
    `custodial_fee`         varchar(32)    DEFAULT ''  NOT NULL,
    `distribution_fee`      varchar(32)    DEFAULT ''  NOT NULL,

    `stock_percent`         varchar(32)    DEFAULT ''  NOT NULL,
    `bond_percent`          varchar(32)    DEFAULT ''  NOT NULL,
    `top10_stock_percent`   varchar(32)    DEFAULT ''  NOT NULL,
    `top5_bond_percent`     varchar(32)    DEFAULT ''  NOT NULL,
    `net_asset`             varchar(32)    DEFAULT ''  NOT NULL,
    PRIMARY KEY (fund_code)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;