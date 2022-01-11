CREATE TABLE nation
(
    nation_id    serial PRIMARY KEY,
    full_name    VARCHAR(1024) UNIQUE,
    abbreviation VARCHAR(255)
);

CREATE TABLE season
(
    season_id  serial PRIMARY KEY,
    start_year INT,
    end_year   INT
);

CREATE TABLE league
(
    league_id serial PRIMARY KEY,
    full_name VARCHAR(255) UNIQUE,
    nation_id INT,
    FOREIGN KEY (nation_id)
        REFERENCES nation (nation_id)
);

CREATE TABLE club
(
    club_id   serial PRIMARY KEY,
    full_name VARCHAR(1024) UNIQUE,
    city      VARCHAR(1024)
);

CREATE TABLE club_league
(
    id        serial PRIMARY KEY,
    club_id   INT,
    league_id INT,
    season_id INT,
    FOREIGN KEY (club_id)
        REFERENCES club (club_id),
    FOREIGN KEY (league_id)
        REFERENCES league (league_id),
    FOREIGN KEY (season_id)
        REFERENCES season (season_id)
);

CREATE TABLE player
(
    player_id      serial PRIMARY KEY,
    full_name      VARCHAR(1024),
    short_name     VARCHAR(255),
    image_link     VARCHAR(2048),
    date_of_birth  DATE,
    nationality_id INT,
    preferred_foot VARCHAR(255),
    weight         INT,
    height         INT,
    sofifa_id      INT UNIQUE,
    FOREIGN KEY (nationality_id)
        REFERENCES nation (nation_id)
);

CREATE TABLE player_club_transfer
(
    id           serial PRIMARY KEY,
    from_club_id INT,
    to_club_id   INT,
    player_id    INT,
    changed_at   DATE,
    fee          NUMERIC(12, 2),
    fee_currency VARCHAR(2),
    is_borrowed  BOOLEAN,
    FOREIGN KEY (from_club_id)
        REFERENCES club (club_id),
    FOREIGN KEY (to_club_id)
        REFERENCES club (club_id),
    FOREIGN KEY (player_id)
        REFERENCES player (player_id)
);

CREATE TABLE position
(
    position_id serial PRIMARY KEY,
    full_name   VARCHAR(1024),
    short_name  VARCHAR(255)
);

CREATE TABLE player_position
(
    player_position_id serial PRIMARY KEY,
    player_id          INT,
    position_id        INT,
    is_main_position   BOOLEAN,
    FOREIGN KEY (player_id)
        REFERENCES player (player_id),
    FOREIGN KEY (position_id)
        REFERENCES position (position_id)
);

CREATE TABLE fifa_scrapper_execution
(
    fifa_scrapper_execution_id serial PRIMARY KEY,
    year_of_fifa               INT,
    data_from_timestamp        DATE,
    executed_at                TIMESTAMP NOT NULL
);

CREATE TABLE attribute
(
    attribute_id serial PRIMARY KEY,
    name         VARCHAR(1024)
);

CREATE TABLE trait
(
    trait_id serial PRIMARY KEY,
    name     VARCHAR(1024)
);

CREATE TABLE player_transfer_data
(
    player_transfer_data_id    serial PRIMARY KEY,
    player_id                  INT,
    rating                     INT,
    potential                  INT,
    value                      NUMERIC(12, 2),
    value_currency             VARCHAR(2),
    wage                       NUMERIC(12, 2),
    wage_currency              VARCHAR(2),
    international_reputation   INT,
    fifa_scrapper_execution_id INT,
    FOREIGN KEY (player_id)
        REFERENCES player (player_id),
    FOREIGN KEY (fifa_scrapper_execution_id)
        REFERENCES fifa_scrapper_execution (fifa_scrapper_execution_id)
);

CREATE TABLE fifa_player_attribute
(
    player_attribute_id        serial PRIMARY KEY,
    player_id                  INT,
    attribute_id               INT,
    attribute_value            INT,
    fifa_scrapper_execution_id INT,
    FOREIGN KEY (player_id)
        REFERENCES player (player_id),
    FOREIGN KEY (attribute_id)
        REFERENCES attribute (attribute_id),
    FOREIGN KEY (fifa_scrapper_execution_id)
        REFERENCES fifa_scrapper_execution (fifa_scrapper_execution_id)
);

CREATE TABLE fifa_player_trait
(
    player_trait_id            serial PRIMARY KEY,
    player_id                  INT,
    trait_id                   INT,
    fifa_scrapper_execution_id INT,
    FOREIGN KEY (player_id)
        REFERENCES player (player_id),
    FOREIGN KEY (trait_id)
        REFERENCES trait (trait_id),
    FOREIGN KEY (fifa_scrapper_execution_id)
        REFERENCES fifa_scrapper_execution (fifa_scrapper_execution_id)
);

CREATE TABLE formation
(
    formation_id serial PRIMARY KEY,
    name         VARCHAR(1024),
    description  VARCHAR
);

CREATE TABLE formation_position
(
    formation_position_id serial PRIMARY KEY,
    formation_id          INT,
    position_id           INT,
    FOREIGN KEY (position_id)
        REFERENCES position (position_id),
    FOREIGN KEY (formation_id)
        REFERENCES formation (formation_id)
);