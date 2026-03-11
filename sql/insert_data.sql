-- Luxury Home Decor BI — Seed Data

-- CATEGORIES
INSERT INTO luxury.categories (name) VALUES
('Furniture'),('Lighting'),('Textiles'),('Accessories'),('Outdoor');

-- PRODUCTS (15 luxury items)
INSERT INTO luxury.products (name, category_id, collection, price, cost) VALUES
('Milano Sofa 3-Seater', 1, 'Milano', 4500.00, 1800.00),
('Paris Armchair Gold', 1, 'Paris', 2200.00, 850.00),
('Dubai King Bed Frame', 1, 'Dubai', 6800.00, 2500.00),
('Crystal Chandelier L', 2, 'Crystal', 3200.00, 1100.00),
('Marble Coffee Table', 1, 'Milano', 1800.00, 600.00),
('Velvet Curtains Set', 3, 'Paris', 950.00, 280.00),
('Luxury Rug 3x4m', 3, 'Dubai', 2400.00, 800.00),
('Gold Wall Mirror XXL', 4, 'Paris', 1200.00, 400.00),
('Outdoor Lounge Set', 5, 'Outdoor', 5500.00, 2100.00),
('Silk Cushion Set x4', 3, 'Milano', 380.00, 120.00),
('Crystal Table Lamp', 2, 'Crystal', 890.00, 310.00),
('Velvet Dining Chair x2', 1, 'Paris', 1600.00, 580.00),
('Dubai Wardrobe 4-Door', 1, 'Dubai', 8200.00, 3100.00),
('Decorative Vase Gold', 4, 'Milano', 420.00, 130.00),
('Outdoor Parasol Luxury', 5, 'Outdoor', 1900.00, 720.00);

-- CUSTOMERS
INSERT INTO luxury.customers (full_name, email, phone, city, country, type) VALUES
('Ahmed Mansouri', 'ahmed@vip.com', '+971501234567', 'Dubai', 'UAE', 'VIP'),
('Sophie Laurent', 'sophie@lux.fr', '+33612345678', 'Paris', 'France', 'VIP'),
('James Whitfield', 'james@uk.com', '+447891234567', 'London', 'UK', 'Regular'),
('Fatima Al-Rashid', 'fatima@sa.com', '+966501234567', 'Riyadh', 'Saudi Arabia', 'VIP'),
('Marco Rossi', 'marco@it.com', '+393312345678', 'Milan', 'Italy', 'Regular'),
('Nadia Benali', 'nadia@dz.com', '+213551234567', 'Algiers', 'Algeria', 'New'),
('Chen Wei', 'chen@cn.com', '+8613812345678', 'Shanghai', 'China', 'VIP'),
('Emma Johnson', 'emma@us.com', '+12125551234', 'New York', 'USA', 'Regular'),
('Khalid Ibrahim', 'khalid@kw.com', '+96550123456', 'Kuwait City', 'Kuwait', 'VIP'),
('Laura Martinez', 'laura@es.com', '+34612345678', 'Madrid', 'Spain', 'New');

-- SALESPERSONS
INSERT INTO luxury.salespersons (full_name, region, email) VALUES
('Rym Bouaziz', 'North Africa', 'rym@luxdecor.com'),
('Taher Slim', 'Europe', 'taher@luxdecor.com'),
('Sara Mansour', 'Gulf Region', 'sara@luxdecor.com'),
('Karim Djebali', 'North Africa', 'karim@luxdecor.com');

-- TARGETS (2025)
INSERT INTO luxury.targets (salesperson_id, month, year, target_amount) VALUES
(1,1,2025,50000),(1,2,2025,55000),(1,3,2025,60000),(1,4,2025,65000),(1,5,2025,65000),(1,6,2025,70000),
(2,1,2025,70000),(2,2,2025,75000),(2,3,2025,80000),(2,4,2025,80000),(2,5,2025,85000),(2,6,2025,85000),
(3,1,2025,90000),(3,2,2025,95000),(3,3,2025,100000),(3,4,2025,100000),(3,5,2025,105000),(3,6,2025,110000),
(4,1,2025,45000),(4,2,2025,50000),(4,3,2025,55000),(4,4,2025,55000),(4,5,2025,60000),(4,6,2025,60000);

-- SALES (Jan-Jun 2025)
INSERT INTO luxury.sales (product_id,customer_id,salesperson_id,quantity,unit_price,total_amount,sale_date,region,city) VALUES
(1,1,3,2,4500,9000,'2025-01-05','Gulf Region','Dubai'),
(3,4,3,1,6800,6800,'2025-01-10','Gulf Region','Riyadh'),
(4,2,2,1,3200,3200,'2025-01-15','Europe','Paris'),
(2,5,2,3,2200,6600,'2025-01-20','Europe','Milan'),
(5,7,2,2,1800,3600,'2025-01-22','Europe','Shanghai'),
(11,9,3,2,890,1780,'2025-01-28','Gulf Region','Kuwait City'),
(7,9,3,1,2400,2400,'2025-02-03','Gulf Region','Kuwait City'),
(8,3,2,2,1200,2400,'2025-02-08','Europe','London'),
(1,6,1,1,4500,4500,'2025-02-12','North Africa','Algiers'),
(6,10,1,4,950,3800,'2025-02-18','Europe','Madrid'),
(9,1,3,1,5500,5500,'2025-02-25','Gulf Region','Dubai'),
(12,2,2,4,1600,6400,'2025-02-27','Europe','Paris'),
(2,4,3,2,2200,4400,'2025-03-01','Gulf Region','Riyadh'),
(10,8,2,6,380,2280,'2025-03-05','Europe','New York'),
(3,7,2,1,6800,6800,'2025-03-10','Europe','Shanghai'),
(5,2,2,1,1800,1800,'2025-03-15','Europe','Paris'),
(4,9,3,2,3200,6400,'2025-03-20','Gulf Region','Kuwait City'),
(13,4,3,1,8200,8200,'2025-03-25','Gulf Region','Riyadh'),
(14,1,3,3,420,1260,'2025-03-28','Gulf Region','Dubai'),
(1,2,2,1,4500,4500,'2025-04-02','Europe','Paris'),
(7,5,2,2,2400,4800,'2025-04-08','Europe','Milan'),
(9,1,3,2,5500,11000,'2025-04-12','Gulf Region','Dubai'),
(11,7,2,3,890,2670,'2025-04-18','Europe','Shanghai'),
(6,3,2,5,950,4750,'2025-04-22','Europe','London'),
(8,9,3,1,1200,1200,'2025-04-27','Gulf Region','Kuwait City'),
(2,4,3,3,2200,6600,'2025-05-03','Gulf Region','Riyadh'),
(4,2,2,1,3200,3200,'2025-05-09','Europe','Paris'),
(15,1,3,1,1900,1900,'2025-05-14','Gulf Region','Dubai'),
(10,6,1,8,380,3040,'2025-05-19','North Africa','Algiers'),
(3,9,3,1,6800,6800,'2025-05-24','Gulf Region','Kuwait City'),
(5,7,2,3,1800,5400,'2025-06-01','Europe','Shanghai'),
(12,4,3,4,1600,6400,'2025-06-05','Gulf Region','Riyadh'),
(1,8,2,1,4500,4500,'2025-06-10','Europe','New York'),
(14,2,2,5,420,2100,'2025-06-15','Europe','Paris'),
(9,1,3,1,5500,5500,'2025-06-20','Gulf Region','Dubai');

-- INVENTORY
INSERT INTO luxury.inventory (product_id, quantity, min_stock, reorder_point) VALUES
(1,8,3,5),(2,15,5,8),(3,4,3,5),(4,2,3,5),
(5,12,4,7),(6,20,5,10),(7,6,3,6),(8,9,4,7),
(9,3,2,4),(10,25,8,12),(11,7,3,6),(12,11,4,8),
(13,2,2,3),(14,30,10,15),(15,5,3,5);

-- STOCK MOVEMENTS
INSERT INTO luxury.stock_movements (product_id,movement_type,quantity,movement_date,reason) VALUES
(1,'IN',10,'2025-01-01','Restock'),(1,'OUT',2,'2025-01-05','Sale'),
(3,'IN',5,'2025-01-01','Restock'),(3,'OUT',1,'2025-01-10','Sale'),
(4,'IN',5,'2025-01-01','Restock'),(4,'OUT',3,'2025-03-20','Sale'),
(9,'IN',4,'2025-01-01','Restock'),(9,'OUT',1,'2025-02-25','Sale'),
(13,'IN',3,'2025-02-01','Restock'),(13,'OUT',1,'2025-03-25','Sale'),
(1,'OUT',1,'2025-04-02','Sale'),(7,'OUT',2,'2025-04-08','Sale'),
(6,'IN',10,'2025-04-01','Restock'),(6,'OUT',5,'2025-04-22','Sale'),
(2,'IN',5,'2025-05-01','Restock'),(2,'OUT',3,'2025-05-03','Sale'),
(14,'IN',20,'2025-03-01','Restock'),(14,'OUT',8,'2025-06-15','Sale');

-- REVIEWS
INSERT INTO luxury.reviews (product_id,customer_id,rating,comment,review_date) VALUES
(1,1,5,'Absolutely stunning sofa, worth every penny!','2025-01-20'),
(3,4,5,'Perfect for our master bedroom, luxurious feel','2025-01-25'),
(4,2,4,'Beautiful chandelier, delivery took long','2025-02-01'),
(2,5,5,'Excellent quality, very elegant','2025-02-10'),
(7,9,4,'Great rug, colors are vibrant','2025-03-01'),
(9,1,5,'Best outdoor set I have ever owned','2025-03-10'),
(6,3,4,'Great curtains, easy to install','2025-04-15'),
(1,2,5,'Second sofa I bought, still perfect quality','2025-05-01'),
(5,7,4,'Marble table looks amazing in our living room','2025-05-20'),
(13,4,5,'Dubai wardrobe is massive and stunning','2025-04-05');
