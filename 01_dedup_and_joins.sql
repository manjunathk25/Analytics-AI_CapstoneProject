-- Query to detect and list every duplicated partner_id
SELECT partner_id, COUNT(*) AS duplicate_count
FROM partners_import
GROUP BY partner_id
HAVING COUNT(*) > 1;

-- DROP table if it already exists from previous run
DROP TABLE IF EXISTS partners;

-- Build clean partners table by collapsing exact-duplicate rows
CREATE TABLE partners AS
SELECT partner_id, city, primary_category, rating, active, days_since_onboarding
FROM partners_import
GROUP BY partner_id, city, primary_category, rating, active, days_since_onboarding;

-- INNER JOIN to confirm every booking resolves to a valid partner
SELECT b.booking_id, b.partner_id, p.city, p.primary_category
FROM bookings b
INNER JOIN partners p
ON b.partner_id = p.partner_id;

-- LEFT JOIN to find any category that as never received any bookings
SELECT c.category zero_bookings_category
FROM categories c
LEFT JOIN bookings b
ON c.category = b.category
WHERE b.booking_id IS NULL;

-- LEFT JOIN to find any partner who as never received any bookings
SELECT p.partner_id zero_bookings_partner
FROM partners p
LEFT JOIN bookings b
ON p.partner_id = b.partner_id
WHERE b.booking_id IS NULL;

-- For zero booking categories,
-- COUNT(*) returns 1 because it counts un-matched row itself, whereas
-- COUNT(b.booking_id) returns 0 because b.booking_id is NULL
SELECT c.category, COUNT(*) total_rows, COUNT(b.booking_id) matched_bookings_count
FROM categories c
LEFT JOIN bookings b
ON c.category = b.category
GROUP BY c.category;