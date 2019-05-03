-- select time_to_sec(timediff("2018-02-21 11:03:45", "2018-02-21 11:02:15")) as diff


select a.user_id, a.date_time as session_from, b.date_time as session_to, time_to_sec(timediff(b.date_time, a.date_time)) as seconds
from activity a, activity b
where a.user_id = b.user_id and a.date_time <= b.date_time and
  !exists(select 1 from activity where user_id = a.user_id and date_time > a.date_time and date_time <= b.date_time and action = "open") and
  !exists(select 1 from activity where user_id = a.user_id and date_time >= a.date_time and date_time < b.date_time and action = "close")
order by a.user_id, a.date_time;


-- select
-- if(action = 'open', @row_number:=@row_number+1, @row_number) as num, date_time, user_id, action
-- from
  -- activity,(select @row_number:=0) as t
-- -- where
  -- -- action = "open" or action = "close"
-- order by
  -- user_id, date_time;
