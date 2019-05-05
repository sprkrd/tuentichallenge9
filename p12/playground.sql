select
  @row_number:=@row_number+1 as row_number, date_time, user_id, action
from
  activity,(select @row_number:=0) as t
order by
  user_id, date_time;

-- with act_with_transitions as (
  -- select
    -- *,
    -- (prev_action is null or prev_action = 'close' or action = 'open') as session_begin,
    -- (next_action is null or next_action = 'open' or action = 'close') as session_end
  -- from (
    -- select
      -- *,
      -- lag(action,1) over (partition by user_id order by date_time) as prev_action,
      -- lead(action,1) over (partition by user_id order by date_time) as next_action
    -- from activity) as t
-- )
-- select
  -- a.user_id,
  -- a.date_time as session_from,
  -- b.date_time as session_to,
  -- time_to_sec(timediff(b.date_time, a.date_time)) as seconds,
  -- (select count(1) from activity where user_id = a.user_id and date_time between a.date_time and b.date_time) as num_actions
-- from
  -- act_with_transitions a, act_with_transitions b
-- where
  -- a.user_id = b.user_id and
  -- a.session_begin and
  -- b.session_end and
  -- a.date_time <= b.date_time and
  -- not exists(
    -- select 1
    -- from act_with_transitions
    -- where date_time > a.date_time and date_time < b.date_time and
          -- (session_begin or session_end)
  -- )
-- order by user_id, session_from;

-- select distinct user_id, session_from, session_to, seconds, num_actions
-- from (
  -- select
    -- a.user_id,
    -- a.date_time as session_from,
    -- b.date_time as session_to,
    -- time_to_sec(timediff(b.date_time, a.date_time)) as seconds,
    -- (select count(1) from activity where user_id = a.user_id and date_time >= a.date_time and date_time <= b.date_time) as num_actions
  -- from activity a, activity b
  -- where a.user_id = b.user_id and a.date_time <= b.date_time and
    -- not exists(select 1 from activity where user_id = a.user_id and date_time > a.date_time and date_time <= b.date_time and action = "open") and
    -- not exists(select 1 from activity where user_id = a.user_id and date_time >= a.date_time and date_time < b.date_time and action = "close")
-- ) as intervals
-- where not exists(
  -- select 1
  -- from activity a, activity b
  -- where intervals.user_id = a.user_id and intervals.user_id = b.user_id and a.date_time <= b.date_time and
    -- not exists(select 1 from activity where user_id = a.user_id and date_time > a.date_time and date_time <= b.date_time and action = "open") and
    -- not exists(select 1 from activity where user_id = a.user_id and date_time >= a.date_time and date_time < b.date_time and action = "close") and
    -- (
      -- (intervals.session_from > a.date_time and intervals.session_to <= b.date_time)
      -- or
      -- (intervals.session_from >= a.date_time and intervals.session_to < b.date_time)
    -- )
-- )
-- order by user_id, session_from;

-- select distinct
  -- a.user_id,
  -- a.date_time as session_from,
  -- b.date_time as session_to,
  -- time_to_sec(timediff(b.date_time, a.date_time)) as seconds,
  -- (select count(1) from activity where user_id = a.user_id and date_time >= a.date_time and date_time <= b.date_time) as num_actions
-- from activity a, activity b
-- where a.user_id = b.user_id and a.date_time <= b.date_time and
  -- not exists(select 1 from activity where user_id = a.user_id and date_time > a.date_time and date_time <= b.date_time and action = "open") and
  -- not exists(select 1 from activity where user_id = a.user_id and date_time >= a.date_time and date_time < b.date_time and action = "close") and
  -- not exists(
    -- select 1
    -- from activity c, activity d
    -- where a.user_id = c.user_id and a.user_id = d.user_id and c.date_time <= d.date_time and
      -- not exists(select 1 from activity where user_id = c.user_id and date_time > c.date_time and date_time <= d.date_time and action = "open") and
      -- not exists(select 1 from activity where user_id = c.user_id and date_time >= c.date_time and date_time < d.date_time and action = "close") and
      -- (
        -- (a.date_time > c.date_time and b.date_time <= d.date_time)
        -- or
        -- (a.date_time >= c.date_time and b.date_time < d.date_time)
      -- )
  -- );

