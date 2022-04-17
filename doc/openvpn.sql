/*
Target Server Type    : SQLite
Target Server Version : 30706
File Encoding         : 65001

Date: 2022-02-27 23:09:32
*/

PRAGMA foreign_keys = OFF;

-- ----------------------------
-- Table structure for "main"."t_admin"
-- ----------------------------
CREATE TABLE "t_admin" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"username"  TEXT NOT NULL,
"password"  TEXT NOT NULL,
"token"  TEXT
);

-- ----------------------------
-- Records of t_admin
-- ----------------------------
INSERT INTO "main"."t_admin" VALUES (1, 'admin', 'e10adc3949ba59abbe56e057f20f883e', 'YWRtaW4xNjQ1OTczODE4LjY4MTI5NTY=');

-- ----------------------------
-- Table structure for "main"."t_logs"
-- ----------------------------
CREATE TABLE "t_logs" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"username"  TEXT NOT NULL,
"timeunix"  TEXT NOT NULL,
"local"  TEXT NOT NULL,
"remote"  TEXT NOT NULL,
"trusted_ip"  TEXT NOT NULL,
"trusted_port"  TEXT NOT NULL,
"logintime"  TEXT,
"logouttime"  TEXT,
"received"  INTEGER,
"sent"  INTEGER
);

-- ----------------------------
-- Records of t_logs
-- ----------------------------

-- ----------------------------
-- Table structure for "main"."t_smtp"
-- ----------------------------
CREATE TABLE "t_smtp" (
"id"  INTEGER NOT NULL,
"server"  TEXT,
"ssl"  INTEGER,
"port"  INTEGER,
"user"  TEXT,
"password"  TEXT
);

-- ----------------------------
-- Records of t_smtp
-- ----------------------------
INSERT INTO "main"."t_smtp" VALUES (1, '', 0, 25, '', '');

-- ----------------------------
-- Table structure for "main"."t_user"
-- ----------------------------
CREATE TABLE "t_user" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"username"  TEXT NOT NULL,
"password"  TEXT NOT NULL,
"email"  TEXT,
"active"  INTEGER NOT NULL,
"expire"  TEXT NOT NULL,
"firewall"  TEXT,
"send"  INTEGER NOT NULL DEFAULT 0
);

-- ----------------------------
-- Table structure for "main"."t_warn"
-- ----------------------------
CREATE TABLE "t_warn" (
"id"  INTEGER NOT NULL,
"status"  INTEGER NOT NULL,
"send_time"  INTEGER NOT NULL,
"send_msg"  TEXT,
"admin_status"  INTEGER NOT NULL,
"admin_email"  TEXT,
"admin_msg"  TEXT
);

-- ----------------------------
-- Records of t_warn
-- ----------------------------
INSERT INTO "main"."t_warn" VALUES (1, 1, 1, '{username}:
       你的VPN用户在 {time} 到期，如果需要继续使用VPN，请向管理员申请续期。', 1, '', null);