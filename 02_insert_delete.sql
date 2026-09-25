-- DELETE 3 test/dummy rows seeded by generator 
DELETE
FROM bookings
WHERE is_test = 1;

--DELETE if records already exists
DELETE
FROM bookings
WHERE booking_id IN ('B9001', 'B9002', 'B9003');
-- INSERT exactly 3 new bookings
-- (each references a real partner already in clean partners table, in that partner's own city and category)
INSERT
INTO bookings
VALUES('B9001','P009','Mumbai','Deep Home Cleaning','2026-03-31',3400,0,0,0),
('B9002','P041','Chennai','Plumbing','2026-03-31',706,0,0,0),
('B9003','P035','Hyderabad','Electrical Repair','2026-03-31',980,0,0,0);

-- Total bookings: 600
-- Total amount_inr: ₹10,47,973
SELECT COUNT(*) total_bookings, SUM(amount_inr) total_revenue_inr
FROM bookings;