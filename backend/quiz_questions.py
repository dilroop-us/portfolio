SQL_QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "Select all columns from the skills table",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM skills",
        "category": "Basic SELECT"
    },
    {
        "id": 2,
        "question": "Select only the name and category columns from the skills table",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT name, category FROM skills",
        "category": "Basic SELECT"
    },
    {
        "id": 3,
        "question": "Find all skills where proficiency is greater than 80",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM skills WHERE proficiency > 80",
        "category": "WHERE Clause"
    },
    {
        "id": 4,
        "question": "Find all projects with status 'Production'",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM projects WHERE status = 'Production'",
        "category": "WHERE Clause"
    },
    {
        "id": 5,
        "question": "Count the total number of skills",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT COUNT(*) FROM skills",
        "category": "Aggregate Functions"
    },
    {
        "id": 6,
        "question": "Find all skills ordered by years_experience in descending order",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM skills ORDER BY years_experience DESC",
        "category": "ORDER BY"
    },
    {
        "id": 7,
        "question": "Select all projects from year 2024",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM projects WHERE year = '2024'",
        "category": "WHERE Clause"
    },
    {
        "id": 8,
        "question": "Find the skill with the highest proficiency",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM skills ORDER BY proficiency DESC LIMIT 1",
        "category": "ORDER BY & LIMIT"
    },
    {
        "id": 9,
        "question": "Count how many contact messages are unread (read = false)",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT COUNT(*) FROM contact_messages WHERE read = false",
        "category": "Aggregate Functions"
    },
    {
        "id": 10,
        "question": "Find all skills in the 'Backend' category",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM skills WHERE category = 'Backend'",
        "category": "WHERE Clause"
    },
    {
        "id": 11,
        "question": "Get the average proficiency of all skills",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT AVG(proficiency) FROM skills",
        "category": "Aggregate Functions"
    },
    {
        "id": 12,
        "question": "Find all projects ordered by title alphabetically",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM projects ORDER BY title ASC",
        "category": "ORDER BY"
    },
    {
        "id": 13,
        "question": "Select skills with years_experience between 2 and 4",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM skills WHERE years_experience BETWEEN 2 AND 4",
        "category": "BETWEEN"
    },
    {
        "id": 14,
        "question": "Find all challenges with 'Hard' difficulty",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM challenges WHERE difficulty = 'Hard'",
        "category": "WHERE Clause"
    },
    {
        "id": 15,
        "question": "Count the number of skills by category",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT category, COUNT(*) FROM skills GROUP BY category",
        "category": "GROUP BY"
    },
    {
        "id": 16,
        "question": "Find the most recent contact message",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM contact_messages ORDER BY created_at DESC LIMIT 1",
        "category": "ORDER BY & LIMIT"
    },
    {
        "id": 17,
        "question": "Select all skills with proficiency equal to 100",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM skills WHERE proficiency = 100",
        "category": "WHERE Clause"
    },
    {
        "id": 18,
        "question": "Find distinct categories from the skills table",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT DISTINCT category FROM skills",
        "category": "DISTINCT"
    },
    {
        "id": 19,
        "question": "Get the sum of years_experience for all skills",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT SUM(years_experience) FROM skills",
        "category": "Aggregate Functions"
    },
    {
        "id": 20,
        "question": "Find all chat messages created today",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT * FROM chat_messages WHERE DATE(created_at) = CURRENT_DATE",
        "category": "Date Functions"
    },
    {
        "id": 21,
        "question": "Select skills where name contains 'SQL'",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM skills WHERE name LIKE '%SQL%'",
        "category": "LIKE Pattern Matching"
    },
    {
        "id": 22,
        "question": "Find the minimum proficiency value across all skills",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT MIN(proficiency) FROM skills",
        "category": "Aggregate Functions"
    },
    {
        "id": 23,
        "question": "Count total projects grouped by status",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT status, COUNT(*) FROM projects GROUP BY status",
        "category": "GROUP BY"
    },
    {
        "id": 24,
        "question": "Find all skills ordered by proficiency and years_experience",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM skills ORDER BY proficiency DESC, years_experience DESC",
        "category": "Multiple ORDER BY"
    },
    {
        "id": 25,
        "question": "Select top 3 skills by proficiency",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM skills ORDER BY proficiency DESC LIMIT 3",
        "category": "ORDER BY & LIMIT"
    },
    {
        "id": 26,
        "question": "Find contact messages from gmail.com email addresses",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM contact_messages WHERE email LIKE '%@gmail.com'",
        "category": "LIKE Pattern Matching"
    },
    {
        "id": 27,
        "question": "Get the maximum years_experience value",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT MAX(years_experience) FROM skills",
        "category": "Aggregate Functions"
    },
    {
        "id": 28,
        "question": "Find all projects NOT in 'Development' status",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM projects WHERE status != 'Development'",
        "category": "NOT Operator"
    },
    {
        "id": 29,
        "question": "Count skills with proficiency above 70",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT COUNT(*) FROM skills WHERE proficiency > 70",
        "category": "COUNT with WHERE"
    },
    {
        "id": 30,
        "question": "Find all challenges in 'Database' category",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM challenges WHERE category = 'Database'",
        "category": "WHERE Clause"
    },
    {
        "id": 31,
        "question": "Select skills where category is either 'Frontend' or 'Backend'",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM skills WHERE category IN ('Frontend', 'Backend')",
        "category": "IN Operator"
    },
    {
        "id": 32,
        "question": "Find chat sessions that expire in the future",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT * FROM chat_sessions WHERE expires_at > NOW()",
        "category": "Date Comparisons"
    },
    {
        "id": 33,
        "question": "Get average proficiency grouped by category",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT category, AVG(proficiency) FROM skills GROUP BY category",
        "category": "GROUP BY with Aggregates"
    },
    {
        "id": 34,
        "question": "Find all projects created this year (2025)",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM projects WHERE year = '2025'",
        "category": "WHERE Clause"
    },
    {
        "id": 35,
        "question": "Select contact messages ordered by created_at ascending",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM contact_messages ORDER BY created_at ASC",
        "category": "ORDER BY"
    },
    {
        "id": 36,
        "question": "Count distinct challenge difficulties",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT COUNT(DISTINCT difficulty) FROM challenges",
        "category": "COUNT DISTINCT"
    },
    {
        "id": 37,
        "question": "Find skills with proficiency less than or equal to 50",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM skills WHERE proficiency <= 50",
        "category": "WHERE Clause"
    },
    {
        "id": 38,
        "question": "Get the oldest project by created_at",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM projects ORDER BY created_at ASC LIMIT 1",
        "category": "ORDER BY & LIMIT"
    },
    {
        "id": 39,
        "question": "Find all skills where name starts with 'P'",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM skills WHERE name LIKE 'P%'",
        "category": "LIKE Pattern Matching"
    },
    {
        "id": 40,
        "question": "Count contact messages grouped by read status",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT read, COUNT(*) FROM contact_messages GROUP BY read",
        "category": "GROUP BY"
    },
    {
        "id": 41,
        "question": "Find skills with years_experience greater than 3",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM skills WHERE years_experience > 3",
        "category": "WHERE Clause"
    },
    {
        "id": 42,
        "question": "Select the 5 most recent chat messages",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM chat_messages ORDER BY created_at DESC LIMIT 5",
        "category": "ORDER BY & LIMIT"
    },
    {
        "id": 43,
        "question": "Find projects where title contains 'API'",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM projects WHERE title LIKE '%API%'",
        "category": "LIKE Pattern Matching"
    },
    {
        "id": 44,
        "question": "Get total count of all projects",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT COUNT(*) FROM projects",
        "category": "Aggregate Functions"
    },
    {
        "id": 45,
        "question": "Find all challenges ordered by difficulty",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM challenges ORDER BY difficulty",
        "category": "ORDER BY"
    },
    {
        "id": 46,
        "question": "Select skills where proficiency is NOT 100",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM skills WHERE proficiency != 100",
        "category": "NOT Operator"
    },
    {
        "id": 47,
        "question": "Count chat messages by username",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT username, COUNT(*) FROM chat_messages GROUP BY username",
        "category": "GROUP BY"
    },
    {
        "id": 48,
        "question": "Find contact messages with company name provided (NOT NULL)",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM contact_messages WHERE company IS NOT NULL",
        "category": "NULL Checks"
    },
    {
        "id": 49,
        "question": "Get skills with proficiency between 80 and 95",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM skills WHERE proficiency BETWEEN 80 AND 95",
        "category": "BETWEEN"
    },
    {
        "id": 50,
        "question": "Find the newest chat session",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM chat_sessions ORDER BY created_at DESC LIMIT 1",
        "category": "ORDER BY & LIMIT"
    },
    {
        "id": 51,
        "question": "Select all projects where uptime is NOT NULL",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM projects WHERE uptime IS NOT NULL",
        "category": "NULL Checks"
    },
    {
        "id": 52,
        "question": "Count total chat messages",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT COUNT(*) FROM chat_messages",
        "category": "Aggregate Functions"
    },
    {
        "id": 53,
        "question": "Find all skills with category 'DevOps'",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM skills WHERE category = 'DevOps'",
        "category": "WHERE Clause"
    },
    {
        "id": 54,
        "question": "Get distinct project years",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT DISTINCT year FROM projects",
        "category": "DISTINCT"
    },
    {
        "id": 55,
        "question": "Find challenges where title ends with 'Query'",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM challenges WHERE title LIKE '%Query'",
        "category": "LIKE Pattern Matching"
    },
    {
        "id": 56,
        "question": "Count projects by year",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT year, COUNT(*) FROM projects GROUP BY year",
        "category": "GROUP BY"
    },
    {
        "id": 57,
        "question": "Find skills ordered by name alphabetically",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM skills ORDER BY name ASC",
        "category": "ORDER BY"
    },
    {
        "id": 58,
        "question": "Get the second most proficient skill",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT * FROM skills ORDER BY proficiency DESC LIMIT 1 OFFSET 1",
        "category": "LIMIT & OFFSET"
    },
    {
        "id": 59,
        "question": "Find contact messages where email ends with '.com'",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM contact_messages WHERE email LIKE '%.com'",
        "category": "LIKE Pattern Matching"
    },
    {
        "id": 60,
        "question": "Select chat sessions created in the last 24 hours",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT * FROM chat_sessions WHERE created_at > NOW() - INTERVAL '24 hours'",
        "category": "Date Intervals"
    },
    {
        "id": 61,
        "question": "Count challenges by category",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT category, COUNT(*) FROM challenges GROUP BY category",
        "category": "GROUP BY"
    },
    {
        "id": 62,
        "question": "Find all projects with NULL latency",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM projects WHERE latency IS NULL",
        "category": "NULL Checks"
    },
    {
        "id": 63,
        "question": "Get skills where proficiency is 85 or 90",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM skills WHERE proficiency IN (85, 90)",
        "category": "IN Operator"
    },
    {
        "id": 64,
        "question": "Find the total number of chat sessions",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT COUNT(*) FROM chat_sessions",
        "category": "Aggregate Functions"
    },
    {
        "id": 65,
        "question": "Select projects ordered by status, then by title",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM projects ORDER BY status, title",
        "category": "Multiple ORDER BY"
    },
    {
        "id": 66,
        "question": "Find skills with years_experience of exactly 3",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM skills WHERE years_experience = 3",
        "category": "WHERE Clause"
    },
    {
        "id": 67,
        "question": "Get average years_experience for all skills",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT AVG(years_experience) FROM skills",
        "category": "Aggregate Functions"
    },
    {
        "id": 68,
        "question": "Find all unread contact messages",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM contact_messages WHERE read = false",
        "category": "WHERE Clause"
    },
    {
        "id": 69,
        "question": "Count distinct challenge categories",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT COUNT(DISTINCT category) FROM challenges",
        "category": "COUNT DISTINCT"
    },
    {
        "id": 70,
        "question": "Select top 5 projects by created_at (newest first)",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM projects ORDER BY created_at DESC LIMIT 5",
        "category": "ORDER BY & LIMIT"
    },
    {
        "id": 71,
        "question": "Find skills where name is exactly 'Python'",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM skills WHERE name = 'Python'",
        "category": "WHERE Clause"
    },
    {
        "id": 72,
        "question": "Get sum of proficiency values for Backend skills",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT SUM(proficiency) FROM skills WHERE category = 'Backend'",
        "category": "Aggregate with WHERE"
    },
    {
        "id": 73,
        "question": "Find chat messages containing the word 'hello'",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM chat_messages WHERE content LIKE '%hello%'",
        "category": "LIKE Pattern Matching"
    },
    {
        "id": 74,
        "question": "Count projects with non-null throughput",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT COUNT(*) FROM projects WHERE throughput IS NOT NULL",
        "category": "COUNT with WHERE"
    },
    {
        "id": 75,
        "question": "Find challenges with difficulty in ('Easy', 'Medium')",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM challenges WHERE difficulty IN ('Easy', 'Medium')",
        "category": "IN Operator"
    },
    {
        "id": 76,
        "question": "Select skills with proficiency above average",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT * FROM skills WHERE proficiency > (SELECT AVG(proficiency) FROM skills)",
        "category": "Subqueries"
    },
    {
        "id": 77,
        "question": "Get the oldest contact message",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM contact_messages ORDER BY created_at ASC LIMIT 1",
        "category": "ORDER BY & LIMIT"
    },
    {
        "id": 78,
        "question": "Find all projects from years before 2024",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM projects WHERE year < '2024'",
        "category": "WHERE Clause"
    },
    {
        "id": 79,
        "question": "Count skills where proficiency equals years_experience * 25",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT COUNT(*) FROM skills WHERE proficiency = years_experience * 25",
        "category": "Calculated WHERE"
    },
    {
        "id": 80,
        "question": "Find distinct usernames from chat messages",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT DISTINCT username FROM chat_messages",
        "category": "DISTINCT"
    },
    {
        "id": 81,
        "question": "Get max proficiency by category",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT category, MAX(proficiency) FROM skills GROUP BY category",
        "category": "GROUP BY with Aggregates"
    },
    {
        "id": 82,
        "question": "Find projects where status is 'Production' or 'Staging'",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM projects WHERE status IN ('Production', 'Staging')",
        "category": "IN Operator"
    },
    {
        "id": 83,
        "question": "Select contact messages that have been read",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM contact_messages WHERE read = true",
        "category": "WHERE Clause"
    },
    {
        "id": 84,
        "question": "Count chat sessions by username",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT username, COUNT(*) FROM chat_sessions GROUP BY username",
        "category": "GROUP BY"
    },
    {
        "id": 85,
        "question": "Find skills where name does NOT contain 'Script'",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM skills WHERE name NOT LIKE '%Script%'",
        "category": "NOT LIKE"
    },
    {
        "id": 86,
        "question": "Get minimum proficiency by category",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT category, MIN(proficiency) FROM skills GROUP BY category",
        "category": "GROUP BY with Aggregates"
    },
    {
        "id": 87,
        "question": "Find all challenges NOT in 'Database' category",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM challenges WHERE category != 'Database'",
        "category": "NOT Operator"
    },
    {
        "id": 88,
        "question": "Select projects with both throughput AND latency values",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM projects WHERE throughput IS NOT NULL AND latency IS NOT NULL",
        "category": "AND Operator"
    },
    {
        "id": 89,
        "question": "Count total number of challenges",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT COUNT(*) FROM challenges",
        "category": "Aggregate Functions"
    },
    {
        "id": 90,
        "question": "Find chat messages from the oldest to newest",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT * FROM chat_messages ORDER BY created_at ASC",
        "category": "ORDER BY"
    },
    {
        "id": 91,
        "question": "Get skills with proficiency exactly 90 AND years_experience > 2",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM skills WHERE proficiency = 90 AND years_experience > 2",
        "category": "AND Operator"
    },
    {
        "id": 92,
        "question": "Find contact messages without a company name",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM contact_messages WHERE company IS NULL",
        "category": "NULL Checks"
    },
    {
        "id": 93,
        "question": "Select top 3 challenges by title alphabetically",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM challenges ORDER BY title ASC LIMIT 3",
        "category": "ORDER BY & LIMIT"
    },
    {
        "id": 94,
        "question": "Count skills with proficiency >= 80 OR years_experience >= 4",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT COUNT(*) FROM skills WHERE proficiency >= 80 OR years_experience >= 4",
        "category": "OR Operator"
    },
    {
        "id": 95,
        "question": "Find projects where year is between '2020' and '2023'",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM projects WHERE year BETWEEN '2020' AND '2023'",
        "category": "BETWEEN"
    },
    {
        "id": 96,
        "question": "Get average proficiency for skills with years_experience > 2",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT AVG(proficiency) FROM skills WHERE years_experience > 2",
        "category": "Aggregate with WHERE"
    },
    {
        "id": 97,
        "question": "Find all expired chat sessions",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT * FROM chat_sessions WHERE expires_at < NOW()",
        "category": "Date Comparisons"
    },
    {
        "id": 98,
        "question": "Select skills where category is 'Frontend' AND proficiency > 85",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM skills WHERE category = 'Frontend' AND proficiency > 85",
        "category": "AND Operator"
    },
    {
        "id": 99,
        "question": "Count projects grouped by year, ordered by year descending",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT year, COUNT(*) FROM projects GROUP BY year ORDER BY year DESC",
        "category": "GROUP BY with ORDER BY"
    },
    {
        "id": 100,
        "question": "Find the skill with minimum years_experience",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM skills ORDER BY years_experience ASC LIMIT 1",
        "category": "ORDER BY & LIMIT"
    },
    {
        "id": 101,
        "question": "Get total proficiency points for all skills combined",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT SUM(proficiency) FROM skills",
        "category": "Aggregate Functions"
    },
    {
        "id": 102,
        "question": "Find contact messages from today",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT * FROM contact_messages WHERE DATE(created_at) = CURRENT_DATE",
        "category": "Date Functions"
    },
    {
        "id": 103,
        "question": "Select categories with average proficiency above 85",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT category FROM skills GROUP BY category HAVING AVG(proficiency) > 85",
        "category": "HAVING Clause"
    },
    {
        "id": 104,
        "question": "Find projects where description contains 'scalable'",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM projects WHERE description LIKE '%scalable%'",
        "category": "LIKE Pattern Matching"
    },
    {
        "id": 105,
        "question": "Count skills by category, showing only categories with more than 1 skill",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT category, COUNT(*) FROM skills GROUP BY category HAVING COUNT(*) > 1",
        "category": "HAVING Clause"
    },
    {
        "id": 106,
        "question": "Find all skills, showing name and proficiency percentage (proficiency as is)",
        "difficulty": "easy",
        "points": 10,
        "expected_query": "SELECT name, proficiency FROM skills",
        "category": "Basic SELECT"
    },
    {
        "id": 107,
        "question": "Get chat sessions that are still active (not expired)",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT * FROM chat_sessions WHERE expires_at > NOW()",
        "category": "Date Comparisons"
    },
    {
        "id": 108,
        "question": "Find skills with proficiency NOT between 50 and 80",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT * FROM skills WHERE proficiency NOT BETWEEN 50 AND 80",
        "category": "NOT BETWEEN"
    },
    {
        "id": 109,
        "question": "Select the 3 oldest projects",
        "difficulty": "medium",
        "points": 20,
        "expected_query": "SELECT * FROM projects ORDER BY created_at ASC LIMIT 3",
        "category": "ORDER BY & LIMIT"
    },
    {
        "id": 110,
        "question": "Count challenges grouped by difficulty, ordered by count descending",
        "difficulty": "hard",
        "points": 30,
        "expected_query": "SELECT difficulty, COUNT(*) FROM challenges GROUP BY difficulty ORDER BY COUNT(*) DESC",
        "category": "GROUP BY with ORDER BY"
    }
]
