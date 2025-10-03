CREATE TABLE IF NOT EXISTS room (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS booking (
    id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL REFERENCES room(id) ON DELETE CASCADE,
    date_start DATE NOT NULL,
    date_end DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_booking_room_dates ON booking(room_id, date_start, date_end);
CREATE INDEX IF NOT EXISTS idx_room_price_created ON room(price, created_at);
