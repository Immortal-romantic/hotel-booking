CREATE TABLE IF NOT EXISTS hotel_rooms (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    price_per_night DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS hotel_rooms_price_idx ON hotel_rooms (price_per_night);
CREATE INDEX IF NOT EXISTS hotel_rooms_created_at_idx ON hotel_rooms (created_at);

CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL REFERENCES hotel_rooms(id) ON DELETE CASCADE,
    date_start DATE NOT NULL,
    date_end DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_dates CHECK (date_end >= date_start)
);

CREATE INDEX IF NOT EXISTS bookings_date_start_idx ON bookings (date_start);
CREATE INDEX IF NOT EXISTS bookings_room_date_start_idx ON bookings (room_id, date_start);
