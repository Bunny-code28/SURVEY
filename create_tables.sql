
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    user_id VARCHAR(255),
    password VARCHAR(255),
    name VARCHAR(255),
    email VARCHAR(255)
);

INSERT INTO users VALUES
(1, 'chanduvk133@gmail.com', 'pbkdf2:sha256:260000$YIrm9zkZdkBG41tt$381aa80b5ba388d6fb64f8969707f58f43615eff89d01fed19fa5333820dfebf', 'abhishek', 'chanduvk133@gmail.com'),
(2, 'reni@gmail.com', 'pbkdf2:sha256:260000$Dg9xeDScJWirN0BN$5f8898f418621e253852f7573ca0efb7151204b649c6efa81f2315a4b320f7d9', 'reni', 'reni@gmail.com'),
(3, 'Malik@gmail.com', 'pbkdf2:sha256:260000$RTnjZlK4DMgSy4I3$accb5e01626b2c2d1745d1a157db6a373ebe61729e382736aa003c8eda8cefe6', 'Malik', 'malik@gmail.com'),
(4, 'bunny', 'pbkdf2:sha256:260000$ZbeXFY92wGA5mVA3$aee99bbf9525abb505f31c2a65b7cc4fe6c616622e8a90cff45b4c967fb4793d', 'Abhishek Vijayan', 'bunny@gmail.com'),
(5, 'anandhu@gmail.com', 'pbkdf2:sha256:260000$ux5i3w2KSwyUHctQ$4b9f4f925617b73132827667f6815b8e0ecedc3663642b4b7520c300cf54c420', 'anandhu', 'anandhu@gmail.com'),
(6, 'bunny@gmail.com', 'pbkdf2:sha256:260000$swzERMfSYT0psmzh$5713a138b6b9f566c84d23c6d6530f8c63a1e4c2dc09db3111f50597a4acdd63', 'abhishek', 'chanduvk33@gmail.com'),
(7, 'aprana@gmail.com', 'pbkdf2:sha256:260000$z028T572atTR8tDd$de51cd18fb90f6c729b51f1ed2ce3796ed3d46e6b50b33e1a59acc67eeb8a80c', 'aparna', 'aprana@gmail.com');


CREATE TABLE admin (
    id INTEGER PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255),
    email VARCHAR(255),
    role VARCHAR(50)
);


INSERT INTO admin (username, password, email, role) VALUES
('admin', 'hashed_password_here', 'admin@example.com', 'superadmin');


CREATE TABLE surveys (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    topic VARCHAR(255),
    answers TEXT,
    timestamp DATETIME,
    email VARCHAR(255)
);

INSERT INTO surveys VALUES
(1, 1, 'sports', '{"q1": "rarely", "q2": "football", "q3": "Football", "q4": "No", "q5": "yes"}', '2024-10-17 01:26:11', NULL),
(2, 1, 'sports', '{"q1": "daily", "q2": "football", "q3": "Cricket", "q4": "No", "q5": "no"}', '2024-10-17 01:33:09', NULL),
(3, NULL, 'sports', '{"q1": "weekly", "q2": "football", "q3": "Cricket", "q4": "Yes", "q5": "yes"}', '2024-10-17 02:40:02', 'chanduvk133@gmail.com'),
(4, NULL, 'arts', '{"q1": "weekly", "q2": "paint", "q3": "creating", "q4": "monthly", "q5": "yes"}', '2024-10-17 02:43:46', 'chanduvk133@gmail.com'),
(5, NULL, 'literature', '{"q1": "daily", "q2": "fg", "q3": "physical", "q4": "rarely", "q5": "yes"}', '2024-10-17 02:52:03', 'chanduvk133@gmail.com'),
(6, NULL, 'sports', '{"q1": "weekly", "q2": "football", "q3": "Cricket", "q4": "Maybe", "q5": "yes"}', '2024-10-17 04:15:25', 'chanduvk133@gmail.com'),
(7, NULL, 'arts', '{"q1": "weekly", "q2": "paint", "q3": "creating", "q4": "monthly", "q5": "yes"}', '2024-10-17 04:16:40', 'chanduvk133@gmail.com'),
(8, NULL, 'literature', '{"q1": "weekly", "q2": "fiction", "q3": "physical", "q4": "yearly", "q5": "yes"}', '2024-10-17 05:11:05', 'reni@gmail.com'),
(9, NULL, 'literature', '{"q1": "monthly", "q2": "non fiction", "q3": "physical", "q4": "weekly", "q5": "yes"}', '2024-10-17 05:12:12', 'reni@gmail.com'),
(10, NULL, 'sports', '{"q1": "daily", "q2": "hockey", "q3": "Cricket", "q4": "I don\'t know", "q5": "yes"}', '2024-10-17 05:16:49', 'reni@gmail.com'),
(11, NULL, 'sports', '{"q1": "daily", "q2": "football", "q3": "Cricket", "q4": "No", "q5": "yes"}', '2024-10-17 08:07:39', 'reni@gmail.com'),
(12, NULL, 'literature', '{"q1": "weekly", "q2": "fiction", "q3": "ebooks", "q4": "monthly", "q5": "yes"}', '2024-10-17 08:09:23', 'reni@gmail.com'),
(13, NULL, 'arts', '{"q1": "rarely", "q2": "football", "q3": "creating", "q4": "weekly", "q5": "yes"}', '2024-10-17 08:12:26', 'reni@gmail.com'),
(14, NULL, 'literature', '{"q1": "daily", "q2": "poetry", "q3": "physical", "q4": "monthly", "q5": "yes"}', '2024-10-17 08:18:35', 'reni@gmail.com'),
(15, NULL, 'sports', '{"q1": "daily", "q2": "volleyball", "q3": "Cricket", "q4": "I don\'t know", "q5": "yes"}', '2024-10-17 08:27:58', 'bunny@gmail.com'),
(16, NULL, 'sports', '{"q1": "monthly", "q2": "chess", "q3": "Cricket", "q4": "Yes", "q5": "yes"}', '2024-10-17 08:35:54', 'bunny@gmail.com'),
(17, NULL, 'arts', '{"q1": "daily", "q2": "paint", "q3": "creating", "q4": "weekly", "q5": "yes"}', '2024-10-17 08:38:53', 'bunny@gmail.com'),
(18, NULL, 'sports', '{"q1": "daily", "q2": "carroms", "q3": "Football", "q4": "Maybe", "q5": "yes"}', '2024-10-17 09:00:39', 'bunny@gmail.com'),
(19, NULL, 'literature', '{"q1": "monthly", "q2": "alternate history", "q3": "physical", "q4": "monthly", "q5": "yes"}', '2024-10-17 09:06:34', 'bunny@gmail.com'),
(20, NULL, 'sports', '{"q1": "daily", "q2": "football", "q3": "Cricket", "q4": "Yes", "q5": "yes"}', '2024-10-17 09:44:56', 'malik@gmail.com'),
(21, NULL, 'literature', '{"q1": "monthly", "q2": "fiction", "q3": "physical", "q4": "monthly", "q5": "yes"}', '2024-10-17 09:45:48', 'malik@gmail.com'),
(22, NULL, 'sports', '{"q1": "weekly", "q2": "ski ball", "q3": "Cricket", "q4": "Yes", "q5": "yes"}', '2024-10-17 09:53:46', 'anandhu@gmail.com'),
(23, NULL, 'arts', '{"q1": "weekly", "q2": "football", "q3": "appreciating", "q4": "monthly", "q5": "yes"}', '2024-10-17 10:00:07', 'anandhu@gmail.com'),
(24, NULL, 'literature', '{"q1": "rarely", "q2": "poetry", "q3": "both", "q4": "rarely", "q5": "no"}', '2024-10-17 10:20:18', 'anandhu@gmail.com'),
(25, NULL, 'arts', '{"q1": "weekly", "q2": "paint", "q3": "creating", "q4": "yearly", "q5": "yes"}', '2024-10-17 10:21:02', 'anandhu@gmail.com'),
(26, NULL, 'arts', '{"q1": "rarely", "q2": "paint", "q3": "creating", "q4": "monthly", "q5": "yes"}', '2024-10-22 16:00:43', 'bunny@gmail.com'),
(27, NULL, 'literature', '{"q1": "monthly", "q2": "HISTORY", "q3": "ebooks", "q4": "monthly", "q5": "no"}', '2024-10-22 16:13:26', 'bunny@gmail.com'),
(28, NULL, 'literature', '{"q1": "daily", "q2": "cyrillic", "q3": "ebooks", "q4": "rarely", "q5": "no"}', '2024-10-22 16:32:10', 'bunny@gmail.com'),
(29, NULL, 'sports', '{"q1": "monthly", "q2": "hockey", "q3": "Cricket", "q4": "Yes", "q5": "yes"}', '2024-10-23 03:55:23', 'bunny@gmail.com'),
(30, NULL, 'arts', '{"q1": "rarely", "q2": "contemporary", "q3": "both", "q4": "monthly", "q5": "yes"}', '2024-10-23 05:23:04', 'bunny@gmail.com'),
(31, NULL, 'sports', '{"q1": "rarely", "q2": "skateing", "q3": "Cricket", "q4": "No", "q5": "no"}', '2024-11-07 08:38:55', 'aprana@gmail.com');