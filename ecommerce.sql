CREATE TABLE IF NOT EXISTS users(
	user_id			INT PRIMARY KEY	AUTOINCREMENT,
	username		VARCHAR	NOT NULL,
	password		VARCHAR	NOT NULL,
	first_name		TEXT	NOT NULL,
	last_name		TEXT	NOT NULL,
	email			VARCHAR	NOT NULL,
	telephone		INT		NOT NULL,
	giftCard_funds	DECIMAL	NOT NULL
);

CREATE TABLE IF NOT EXISTS user_address(
	address_id		INT	PRIMARY KEY	AUTOINCREMENT,
	user_id			INT,
	address_line1	VARCHAR	NOT NULL,
	address_line2	VARCHAR	NOT NULL,
	city			VARCHAR	NOT NULL,
	zipcode			INT		NOT NULL,
	country			VARCHAR	NOT NULL,
	mobilephone		INT		NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE IF NOT EXISTS product_inventory(
	inventoryID		INT	PRIMARY KEY,
	quantity		INT
);

CREATE TABLE IF NOT EXISTS product_catogory(
	categoryID		INT PRIMARY KEY,
	catogoryName	VARCHAR
);

CREATE TABLE IF NOT EXISTS product(
	product_id		INT	PRIMARY KEY,
	productName		VARCHAR,
	SKU				VARCHAR,
	inventoryID		INT,
	categoryID		INT,
	price			DECIMAL,
	FOREIGN KEY (inventoryID) REFERENCES product_inventory (inventoryID),
	FOREIGN KEY (categoryID) REFERENCES product_catogory (categoryID)
);

CREATE TABLE IF NOT EXISTS user_payment(
	payment_id		INT	PRIMARY KEY,
	user_id			INT,
	payment_type	VARCHAR	NOT NULL,
	provider		VARCHAR	NOT NULL,
	account_num		INT		NOT NULL,
	expiredDate		DATE	NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE IF NOT EXISTS payment_details(
	pd_id			INT	PRIMARY KEY,
	order_id		INT,
	total			VARCHAR,
	status			VARCHAR
);

CREATE TABLE IF NOT EXISTS ordered_details(
	order_id		INT	PRIMARY KEY,
	user_id			INT,
	total_cost		DECIMAL,
	pd_id			INT,
	FOREIGN KEY (user_id) REFERENCES users (user_id),
	FOREIGN KEY (pd_id) REFERENCES payment_details (pd_id)
);

CREATE TABLE IF NOT EXISTS ordered_items(
	items_id		INT	PRIMARY KEY,
	ordered_id		INT,
	product_id		INT,
	quantity		INT,
	FOREIGN KEY (ordered_id) REFERENCES ordered_details (order_id),
	FOREIGN KEY (product_id) REFERENCES product (product_id)
	
);

CREATE TABLE IF NOT EXISTS shopping_cart(
	sc_id			INT	PRIMARY KEY,
	user_id			INT,
	total_cost		DECIMAL,
	FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE IF NOT EXISTS cart_items(
	cart_id			INT	PRIMARY KEY,
	session_id		INT,
	product_id		INT,
	quantity		INT,
	FOREIGN KEY (session_id) REFERENCES shopping_cart (sc_id),
	FOREIGN KEY (product_id) REFERENCES product(product_id)
);




