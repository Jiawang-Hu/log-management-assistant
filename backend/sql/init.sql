-- Docker 中 MySQL 首次启动时自动执行。
-- 创建数据库、数据表，并登记一个等待读取宿主机示例日志的服务。

CREATE DATABASE IF NOT EXISTS log_assistant
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE log_assistant;

-- 明确告诉 MySQL：下面 SQL 文件中的字符串使用 UTF-8 编码。
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS log_service (
    id INT NOT NULL AUTO_INCREMENT,
    service_name VARCHAR(100) NOT NULL,
    log_path VARCHAR(500) NOT NULL,
    source_type VARCHAR(30) NOT NULL DEFAULT 'app',
    enabled TINYINT(1) NOT NULL DEFAULT 1,
    status VARCHAR(30) NOT NULL DEFAULT 'error',
    last_read_at DATETIME NULL,
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_service_name (service_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS log_statistics (
    id INT NOT NULL AUTO_INCREMENT,
    service_id INT NOT NULL,
    stat_date DATE NOT NULL,
    error_count INT NOT NULL DEFAULT 0,
    warn_count INT NOT NULL DEFAULT 0,
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_service_date (service_id, stat_date),
    KEY ix_statistics_service_date (service_id, stat_date),
    CONSTRAINT fk_statistics_service
        FOREIGN KEY (service_id)
        REFERENCES log_service (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS log_reader_checkpoint (
    id INT NOT NULL AUTO_INCREMENT,
    service_id INT NOT NULL,
    file_path VARCHAR(500) NOT NULL DEFAULT '',
    offset_position BIGINT NOT NULL DEFAULT 0,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_checkpoint_service (service_id),
    CONSTRAINT fk_checkpoint_service
        FOREIGN KEY (service_id)
        REFERENCES log_service (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO log_service
    (service_name, log_path, source_type, enabled, status)
SELECT
    'CentOS 示例日志',
    '/var/log/app/demo',
    'app',
    1,
    'collecting'
WHERE NOT EXISTS (
    SELECT 1
    FROM log_service
    WHERE service_name = 'CentOS 示例日志'
);
