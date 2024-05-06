create TABLE log_date(
    id integer PRIMARY KEY AUTOINCREMENT,
    entry_date DATE NOT NULL
);

create TABLE food(
    id integer PRIMARY KEY AUTOINCREMENT,
    name text not null,
    fat integer not NULL,
    protein integer not null,
    carbs integer not null,
    calories integer not null
);


create TABLE food_date(
    food_id integer not NULL,
    log_date_id integer not null,
    PRIMARY key(food_id, log_date_id)
);