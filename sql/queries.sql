-- Player with highest wage per country
SELECT c.nationality_id, n.full_name,
       AVG(ptd.wage) as avg_wage,
       AVG(ptd.rating) as avg_rating,
       AVG(ptd.value) as avg_value,
       COUNT(ptd.player_id)
FROM player_club_transfer
         LEFT JOIN (
-- Last transfer date of player
    SELECT player_id, MAX(changed_at) as last_transfer_date
    FROM player_club_transfer
    GROUP BY player_id
) as last_transfer on last_transfer.player_id = player_club_transfer.player_id
         LEFT JOIN club c on player_club_transfer.to_club_id = c.club_id
         LEFT JOIN nation n on c.nationality_id = n.nation_id
         LEFT JOIN player_transfer_data ptd on player_club_transfer.player_id = ptd.player_id
WHERE last_transfer.last_transfer_date = player_club_transfer.changed_at
GROUP BY c.nationality_id, n.full_name
ORDER BY AVG(ptd.wage) DESC

-- Actual club for player
SELECT player_club_transfer.player_id, to_club_id
FROM player_club_transfer
         LEFT JOIN (
-- Last transfer date of player
    SELECT player_id, MAX(changed_at) as last_transfer_date
    FROM player_club_transfer
    GROUP BY player_id
) as last_transfer on last_transfer.player_id = player_club_transfer.player_id

WHERE last_transfer.last_transfer_date = player_club_transfer.changed_at
ORDER BY player_club_transfer.player_id

-- Actual league for club
SELECT club_league.club_id, MIN(club_league.league_id)
FROM club_league
         LEFT JOIN league l on l.league_id = club_league.league_id
WHERE season_id = 1 AND l.competition_type = 'domestic_cup'
GROUP BY club_league.club_id



-----------------------------------------------------------------
-- Traits per Position Cluster
-----------------------------------------------------------------

-- GK
SELECT t.trait_id, t.name,
       COUNT(fpt.player_id) as number_of_traits_per_position
from player
         left join player_transfer_data ptd on player.player_id = ptd.player_id
         left join fifa_player_trait fpt on player.player_id = fpt.player_id
         left join trait t on fpt.trait_id = t.trait_id
         left join player_position pp on player.player_id = pp.player_id
         left join position p on pp.position_id = p.position_id
Where t.trait_id is not null
  AND (p.short_name = 'GK')
group by t.trait_id, t.name
order by t.trait_id

-- CB
SELECT t.trait_id, t.name,
       COUNT(fpt.player_id) as number_of_traits_per_position
from player
         left join player_transfer_data ptd on player.player_id = ptd.player_id
         left join fifa_player_trait fpt on player.player_id = fpt.player_id
         left join trait t on fpt.trait_id = t.trait_id
         left join player_position pp on player.player_id = pp.player_id
         left join position p on pp.position_id = p.position_id
Where t.trait_id is not null
  AND (p.short_name = 'CB')
group by t.trait_id, t.name
order by t.trait_id

-- Außenverteidiger
SELECT t.trait_id, t.name,
       COUNT(fpt.player_id) as number_of_traits_per_position
from player
         left join player_transfer_data ptd on player.player_id = ptd.player_id
         left join fifa_player_trait fpt on player.player_id = fpt.player_id
         left join trait t on fpt.trait_id = t.trait_id
         left join player_position pp on player.player_id = pp.player_id
         left join position p on pp.position_id = p.position_id
Where t.trait_id is not null
  AND (p.short_name = 'RB' OR p.short_name = 'LB'
    OR p.short_name = 'LBW' OR p.short_name = 'RBW')
group by t.trait_id, t.name
order by t.trait_id

-- Zentrales Mittelfeld
SELECT t.trait_id, t.name,
       COUNT(fpt.player_id) as number_of_traits_per_position
from player
         left join player_transfer_data ptd on player.player_id = ptd.player_id
         left join fifa_player_trait fpt on player.player_id = fpt.player_id
         left join trait t on fpt.trait_id = t.trait_id
         left join player_position pp on player.player_id = pp.player_id
         left join position p on pp.position_id = p.position_id
Where t.trait_id is not null
  AND (p.short_name = 'CDM' OR p.short_name = 'CM')
group by t.trait_id, t.name
order by t.trait_id

-- Außenspieler
SELECT t.trait_id, t.name,
       COUNT(fpt.player_id) as number_of_traits_per_position
from player
         left join player_transfer_data ptd on player.player_id = ptd.player_id
         left join fifa_player_trait fpt on player.player_id = fpt.player_id
         left join trait t on fpt.trait_id = t.trait_id
         left join player_position pp on player.player_id = pp.player_id
         left join position p on pp.position_id = p.position_id
Where t.trait_id is not null
  AND (p.short_name = 'LM' OR p.short_name = 'LW'
    OR p.short_name = 'RW' OR p.short_name = 'RM')
group by t.trait_id, t.name
order by t.trait_id

-- Stürmer
SELECT t.trait_id, t.name,
       COUNT(fpt.player_id) as number_of_traits_per_position
from player
         left join player_transfer_data ptd on player.player_id = ptd.player_id
         left join fifa_player_trait fpt on player.player_id = fpt.player_id
         left join trait t on fpt.trait_id = t.trait_id
         left join player_position pp on player.player_id = pp.player_id
         left join position p on pp.position_id = p.position_id
Where t.trait_id is not null
  AND (p.short_name = 'CAM' OR p.short_name = 'CF'
    OR p.short_name = 'ST')
group by t.trait_id, t.name
order by t.trait_id


-- For Clustering of traits
SELECT t.trait_id, t.name,
       avg(rating) as avg_rating,
       avg(value) as avg_value,
       avg(date_part('year', AGE(date_of_birth))) as avg_age
from player
         left join player_transfer_data ptd on player.player_id = ptd.player_id
         left join fifa_player_trait fpt on player.player_id = fpt.player_id
         left join trait t on fpt.trait_id = t.trait_id
Where t.trait_id is not null
group by t.trait_id, t.name
order by t.trait_id

-----------------------------------------------------------------
-- Rating, Value, age per Position Cluster
-----------------------------------------------------------------

SELECT p.position_id, p.short_name,
       avg(rating) as avg_rating,
       avg(value) as avg_value,
       avg(date_part('year', AGE(date_of_birth))) as avg_age
from player
         left join player_transfer_data ptd on player.player_id = ptd.player_id
         left join player_position pp on player.player_id = pp.player_id
         left join position p on pp.position_id = p.position_id
where pp.is_main_position = true
group by p.position_id, p.full_name


----------------------------------------------------------------
-- Alter = Spielerfahrung ?
----------------------------------------------------------------
SELECT date_part('year', AGE(date_of_birth)) as age,
       avg(minutes_played) as avg_minutes_played,
       avg(appearances) as avg_appearances,
       avg(CASE
               WHEN appearances != 0 THEN minutes_played/appearances
               ELSE 0
           END) as avg_minutes_player_per_appearance,
       avg(lineups) as avg_lineups
FROM player
         LEFT JOIN appearance a on player.player_id = a.player_id

GROUP BY date_part('year', AGE(date_of_birth))
ORDER BY date_part('year', AGE(date_of_birth))

----------------------------------------------------------------
-- Wage and value per rating
----------------------------------------------------------------
SELECT rating,
       avg(value) as avg_value,
       min(value) as min_value,
       max(value) as max_value,
       avg(wage) as avg_wage,
       min(wage) as min_wage,
       max(wage) as max_wage
FROM player_transfer_data
         LEFT JOIN player p on p.player_id = player_transfer_data.player_id
GROUP BY rating
ORDER BY rating

-- Price diffrence for one trade and one position cluster //Beispeilhaft für ein paar Trades und positionen machen
SELECT player_with_trade.rating,
       player_with_trade.avg_value                                  as player_with_trade_avg_value,
       player_without_trade.avg_value                               as player_without_trade_avg_value,
       player_with_trade.avg_value - player_without_trade.avg_value as difference,
       player_with_trade.number_of_player                           as number_of_player_with_trade,
       player_without_trade.number_of_player                        as number_of_player_without_trade
FROM (SELECT rating,
             avg(value)              as avg_value,
             count(player.player_id) as number_of_player
      from player
               left join player_transfer_data ptd on player.player_id = ptd.player_id
               left join fifa_player_trait fpt on player.player_id = fpt.player_id
               left join trait t on fpt.trait_id = t.trait_id
               left join player_position pp on player.player_id = pp.player_id
               left join position p on pp.position_id = p.position_id
      Where t.trait_id = 9
        AND (p.short_name = 'LM' OR p.short_name = 'LW'
          OR p.short_name = 'RW' OR p.short_name = 'RM')
      group by rating
      order by rating) as player_with_trade
         LEFT JOIN
     (SELECT rating,
             avg(value)                       as avg_value,
             count(relevant_player.player_id) as number_of_player
      from ((SELECT player.player_id from player)
            EXCEPT
            (SELECT except_player_with_trait.player_id
             from player as except_player_with_trait
                      left join fifa_player_trait fpt on except_player_with_trait.player_id = fpt.player_id
             WHERE fpt.trait_id = 9)) as relevant_player
               left join player_transfer_data ptd on relevant_player.player_id = ptd.player_id
               left join player_position pp on relevant_player.player_id = pp.player_id
               left join position p on pp.position_id = p.position_id
      WHERE (p.short_name = 'LM' OR p.short_name = 'LW'
          OR p.short_name = 'RW' OR p.short_name = 'RM')
      group by rating
      order by rating) as player_without_trade on player_with_trade.rating = player_without_trade.rating
