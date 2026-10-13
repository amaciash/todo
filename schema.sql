-- To-Do App: database schema (MySQL 8+)
CREATE DATABASE IF NOT EXISTS todo_db CHARACTER SET utf8mb4;
USE todo_db;

CREATE TABLE IF NOT EXISTS tasks (
  task_id      INT AUTO_INCREMENT PRIMARY KEY,
  title        VARCHAR(200) NOT NULL,
  description  TEXT NULL,
  priority     ENUM('low','medium','high') NOT NULL DEFAULT 'medium',
  status       ENUM('pending','done') NOT NULL DEFAULT 'pending',
  due_date     DATE NULL,
  created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  completed_at DATETIME NULL,
  INDEX idx_status (status),
  INDEX idx_due (due_date)
);
