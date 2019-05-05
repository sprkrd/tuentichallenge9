select distinct
  a.user_id,
  date_format(a.date_time, '%Y-%m-%d %H:%i:%S') as session_from,
  date_format(b.date_time, '%Y-%m-%d %H:%i:%S') as session_to,
  time_to_sec(timediff(b.date_time, a.date_time)) as seconds,
  (select count(1) from activity where user_id = a.user_id and date_time >= a.date_time and date_time <= b.date_time) as num_actions
from activity a, activity b
where a.user_id = b.user_id and a.date_time <= b.date_time and
  not exists(select 1 from activity where user_id = a.user_id and date_time > a.date_time and date_time <= b.date_time and action = "open") and
  not exists(select 1 from activity where user_id = a.user_id and date_time >= a.date_time and date_time < b.date_time and action = "close") and
  not exists(
    select 1
    from activity c, activity d
    where a.user_id = c.user_id and a.user_id = d.user_id and c.date_time <= d.date_time and
      not exists(select 1 from activity where user_id = c.user_id and date_time > c.date_time and date_time <= d.date_time and action = "open") and
      not exists(select 1 from activity where user_id = c.user_id and date_time >= c.date_time and date_time < d.date_time and action = "close") and
      (
        (a.date_time > c.date_time and b.date_time <= d.date_time)
        or
        (a.date_time >= c.date_time and b.date_time < d.date_time)
      )
  )
order by user_id, session_from;
