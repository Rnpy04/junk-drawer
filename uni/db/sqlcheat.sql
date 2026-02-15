-- انتخاب تمام ستون‌ها
SELECT * 
FROM table_name;

-- شرط با AND / OR
SELECT *
FROM table_name
WHERE column1 = 'value' AND column2 > 100;

-- مرتب‌سازی
SELECT *
FROM table_name
ORDER BY column1 ASC, column2 DESC;

-- محدود کردن تعداد نتایج
SELECT *
FROM table_name
LIMIT 10;


-- تعداد رکوردها
SELECT COUNT(*) FROM table_name;

-- مجموع، میانگین، بیشینه و کمینه
SELECT SUM(column1), AVG(column1), MAX(column1), MIN(column1)
FROM table_name;

-- گروه‌بندی
SELECT column1, COUNT(*)
FROM table_name
GROUP BY column1;

-- شرط روی گروه
SELECT column1, COUNT(*)
FROM table_name
GROUP BY column1
HAVING COUNT(*) > 5;


-- INNER JOIN
SELECT a.column1, b.column2
FROM table1 a
INNER JOIN table2 b
ON a.id = b.fk_id;

-- LEFT JOIN
SELECT a.column1, b.column2
FROM table1 a
LEFT JOIN table2 b
ON a.id = b.fk_id;

-- RIGHT JOIN
SELECT a.column1, b.column2
FROM table1 a
RIGHT JOIN table2 b
ON a.id = b.fk_id;

-- FULL OUTER JOIN
SELECT a.column1, b.column2
FROM table1 a
FULL OUTER JOIN table2 b
ON a.id = b.fk_id;


-- زیرکوئری در SELECT
SELECT name,
       (SELECT MAX(salary) FROM employees) AS max_salary
FROM employees;

-- زیرکوئری در WHERE
SELECT name
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- زیرکوئری با IN
SELECT name
FROM employees
WHERE department_id IN (SELECT id FROM departments WHERE name = 'IT');


-- ردیف‌بندی
SELECT name, salary,
       ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rn
FROM employees;

-- EXISTS
SELECT name FROM employees e
WHERE EXISTS (SELECT 1 FROM departments d WHERE d.id = e.department_id AND d.name = 'IT');

-- رتبه‌بندی
SELECT name, salary,
       RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rnk
FROM employees;

-- جمع تجمعی
SELECT name, salary,
       SUM(salary) OVER (PARTITION BY department_id ORDER BY salary) AS cumulative_salary
FROM employees;


-- تعریف CTE
WITH dept_avg AS (
    SELECT department_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department_id
)
SELECT e.name, e.salary, d.avg_salary
FROM employees e
JOIN dept_avg d
ON e.department_id = d.department_id;


-- اضافه کردن داده
INSERT INTO table_name (column1, column2)
VALUES ('value1', 100);

-- به‌روزرسانی داده
UPDATE table_name
SET column1 = 'new_value'
WHERE column2 > 100;

-- حذف داده
DELETE FROM table_name
WHERE column1 = 'value';


-- ایجاد جدول
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    salary DECIMAL(10,2),
    department_id INT
);

-- افزودن ستون
ALTER TABLE employees
ADD COLUMN hire_date DATE;

-- حذف جدول
DROP TABLE employees;


-- رشته‌ای
SELECT UPPER(name), LOWER(name), LENGTH(name)
FROM employees;

-- تاریخ
SELECT NOW(), DATE_ADD(NOW(), INTERVAL 7 DAY), DATE_FORMAT(NOW(), '%Y-%m-%d');

-- شرطی
SELECT CASE WHEN salary > 5000 THEN 'High' ELSE 'Low' END AS salary_level
FROM employees;

WITH RECURSIVE EmployeeHierarchy AS (
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN EmployeeHierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM EmployeeHierarchy;

-- ایجاد ایندکس
CREATE INDEX idx_salary ON employees(salary);

-- ترکیبی
CREATE INDEX idx_dept_salary ON employees(department_id, salary);

-- بررسی برنامه اجرایی
EXPLAIN SELECT * FROM employees WHERE salary > 5000;
