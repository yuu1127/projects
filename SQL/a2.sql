--assignment2

create or replace view Q1(Name)
as
select pe.name from person pe,proceeding pr
where pr.EditorId = pe.PersonId
group by pe.PersonId
;

create or replace view Q2(Name)
as
select pe.name from person pe,proceeding pr,RelationPersonInProceeding rpip
where pr.EditorId = pe.PersonId and rpip.PersonId = pe.PersonId
group by pe.PersonId
;

create or replace view Q3(Name)
as
select pe.name
from person pe
    join RelationPersonInProceeding rpip on (rpip.PersonId = pe.PersonId)
    join Inproceeding inpr on (inpr.InproceedingId = rpip.InProceedingId)
    join proceeding pr on (pr.ProceedingId = inpr.ProceedingId)
    where pr.EditorId = pe.PersonId
    Group by pe.PersonId
;

create or replace view Q4(Title)
as
select inpr.Title
from person pe
    join RelationPersonInProceeding rpip on (rpip.PersonId = pe.PersonId)
    join Inproceeding inpr on (inpr.InproceedingId = rpip.InProceedingId)
    join proceeding pr on (pr.ProceedingId = inpr.ProceedingId)
    where pr.EditorId = pe.PersonId
    Group by inpr.InProceedingId
;


create or replace view Q5(Title)
as
select inpr.title
from Inproceeding inpr
    join RelationPersonInProceeding rpip on(inpr.InproceedingId = rpip.InproceedingId)
    join Person pe on(pe.PersonId = rpip.PersonId)
where pe.Name like '%Clark'
;

create or replace view Q6(Year,Title)
as
select pr.Year,count(*) from Proceeding pr
  join Publisher pu on(pr.PublisherId = pu.PublisherId)
  and pr.year is not NULL
  group by pr.Year
  order by pr.Year
;

create or replace view pub_cnt
as
select pu.Name,count(*)
from Publisher pu
  join Proceeding pr on(pr.PublisherId = pu.PublisherId)
  group by pu.name
;

create or replace view Q7(Name)
as
select pub_cnt.Name
from pub_cnt
  where pub_cnt.count = (select max(pub_cnt.count) from pub_cnt)
;

create or replace view co_authorships
as
select pe.PersonId,count(inpr.InProceedingId)
from Person pe
join RelationPersonInProceeding rpip on(pe.PersonId = rpip.PersonId)
join InProceeding inpr on(inpr.InProceedingId = rpip.InProceedingId)
  group by pe.PersonId
;

-- if = 1 different answer
create or replace view co_authors
as
select inpr.InProceedingId,count(pe.PersonId)
from Person pe
join RelationPersonInProceeding rpip on(pe.PersonId = rpip.PersonId)
join InProceeding inpr on(rpip.InProceedingId = inpr.InProceedingId)
  group by inpr.InProceedingId
having count(pe.PersonId) > 1
;

create or replace view Q8_1
as
select pe.PersonId,pe.Name,count(co.InProceedingId)
from Person pe
    join RelationPersonInProceeding rpip on(rpip.PersonId = pe.PersonId)
    join co_authors co on (rpip.InProceedingId = co.InProceedingId)
    Group by pe.PersonId;

create or replace view Q8(Name)
as
select Name
from Q8_1
where count = (select max(count) from Q8_1)
;

--where pe.PersonId =
--(select max(co_authorships.count) from co_authorships)
-- if = 1 different answer
create or replace view solo_author
as
select inpr.InProceedingId,count(pe.PersonId)
from Person pe
join RelationPersonInProceeding rpip on(pe.PersonId = rpip.PersonId)
join InProceeding inpr on(rpip.InProceedingId = inpr.InProceedingId)
  group by inpr.InProceedingId
having count(pe.personId) = 1
;


create or replace view Q9_1
as
select pe.PersonId,pe.Name
from Person pe
    join RelationPersonInProceeding rpip on(pe.PersonId = rpip.PersonId)
Except
select pe.PersonId,pe.Name
from Person pe
  join Q8_1 on(Q8_1.personId = pe.PersonId)
;

create or replace view Q9(Name)
as
select Name
from Q9_1
;


create or replace view Q10_1
as
(select pe.PersonId,pe.Name,count(rpip2.PersonId) as Total
from person pe
join RelationPersonInProceeding rpip1 on(pe.PersonId = rpip1.PersonId)
join RelationPersonInProceeding rpip2 on(rpip1.InProceedingId = rpip2.InProceedingId)
where rpip1.PersonId != rpip2.PersonId
Group by pe.PersonId)
UNION
(select Q9_1.PersonId,Q9_1.Name,COALESCE(0) as Total
from Q9_1)
order by Total desc,Name asc
;

create or replace view Q10(Name,Total)
as
select Name,Total
from Q10_1;

--=とinの違い
create or replace view Q11_0
as
select pe.PersonId,rpip.InProceedingId
from Person pe
join RelationPersonInProceeding rpip on(rpip.PersonId = pe.PersonId)
where pe.Name like 'Richard %'
;

create or replace view Q11_1
as
select pe.PersonId
from person pe
join RelationPersonInProceeding rpip on(pe.PersonId = rpip.PersonId)
join InProceeding inpr on(inpr.InProceedingId = rpip.InProceedingId)
where inpr.InProceedingId in
(select InProceedingId
from Q11_0)
Except
select PersonId from Q11_0
;

create or replace view Q11_2
as
select pe.PersonId
from person pe
join RelationPersonInProceeding rpip on(pe.PersonId = rpip.PersonId)
where rpip.InProceedingId in
(select rpip2.InProceedingId
from Q11_1 r
join RelationPersonInProceeding rpip2 on(rpip2.PersonId = r.PersonId))
Group by pe.PersonId
;

create or replace view Q11_3
as
select pe.PersonId
from Person pe
join RelationPersonInProceeding rpip on(pe.PersonId = rpip.PersonId)
join InProceeding inpr on(inpr.InProceedingId = rpip.InProceedingId)
Except
(select PersonId
from Q11_0
Union
select PersonId
from Q11_1
Union
select PersonId
from Q11_2)
;

create or replace view Q11(Name)
as
select pe.Name
from Person pe
join RelationPersonInProceeding rpip on(pe.PersonId = rpip.PersonId)
join Q11_3 re on(re.PersonId = pe.PersonId)
Group by pe.PersonId;
--where rpip.InProceedingId Not in
--(select rpip.InProceedingId from RelationPersonInProceeding rpip
--where rpip.PersonId in
--(select pe.PersonId
--from Person pe where pe.Name like 'Richard%'));



create or replace view Q12_R
as
WITH RECURSIVE re as(
  select pe.PersonId
  from Person pe
  join RelationPersonInProceeding rpip on(rpip.PersonId = pe.PersonId)
  where pe.Name like 'Richard %'
  Group by pe.PersonId
  UNION
  select pe.personId
  from Person pe
  join RelationPersonInProceeding rpip1 on(rpip1.PersonId = pe.PersonId)
  join RelationPersonInProceeding rpip2 on(rpip1.InProceedingId = rpip2.InProceedingId)
  join re on(re.PersonId = rpip2.PersonId)
)select * from re
;

create or replace view Q12(Name)
as
select pe.Name
from Person pe
join Q12_R R on(R.personID = pe.PersonId)
where pe.Name not like 'Richard %'
Group by pe.PersonId;


create or replace view name_year
as
select pe.PersonId,pr.Year
from Person pe
    join RelationPersonInProceeding rpip on (rpip.PersonId = pe.PersonId)
    join InProceeding inpr on (inpr.InProceedingId = rpip.InProceedingId)
    left join Proceeding pr on (pr.ProceedingId = inpr.ProceedingId)
;

create or replace view Q13(Author,Total,FirstYear,LastYear)
as
select pe.Name as Author,count(*) as Total,COALESCE(min(ny.year),'unknown') as FirstYear,COALESCE(max(ny.year),'unknown') as LastYear
from name_year ny
join Person pe on(ny.PersonId = pe.PersonId)
Group by pe.PersonId
Order by Total,Author
;

--group by must be primary key

create or replace view author_name
as
select pe.PersonId,pe.Name
from Person pe
    join RelationPersonInProceeding rpip on (rpip.PersonId = pe.PersonId)
;

create or replace view editor_name
as
select pe.PersonId,pe.Name
from Person pe
    join Proceeding pr on (pr.EditorId = pe.PersonId)
;

create or replace view Q14(Total)
as
select count(distinct pe.PersonId)
from Person pe
    join RelationPersonInProceeding  rpip on(pe.PersonId = rpip.PersonId)
    join InProceeding inpr on(rpip.InProceedingId = inpr.InProceedingId)
    left join Proceeding pr on(pr.ProceedingId = inpr.ProceedingId)
    where inpr.Title ilike '%data%'
    or pr.Title ilike '%data%'
;

create or replace view Q15(EditorName,Title,PublisherName,Year,Total)
as
select pe.Name,pr.Title,pu.Name,pr.Year,count(inpr.InProceedingId)
from Proceeding pr
    join Person pe on(pe.PersonId = pr.EditorId)
    join Publisher pu on(pu.PublisherId = pr.PublisherId)
    join InProceeding inpr on(pr.ProceedingId = inpr.InProceedingId)
    Group by pr.ProceedingId,pe.Name,pe.PersonId,pu.PublisherId
;


create or replace view non_editor_author
as
select pe.PersonId,pe.Name
from Person pe
    left outer join Proceeding pr on(pr.EditorId = pe.PersonId)
    where pr.EditorId is NULL
;

create or replace view Q16_1
as
select pe1.personId
from Q9_1 pe1
Except
select pe.personId
from Person pe
join Proceeding pr on(pr.EditorId = pe.PersonId)
;

create or replace view Q16(Name)
as
select pe.name
from Person pe
join Q16_1 pe1 on(pe1.PersonId = pe.PersonId)
Group by pe.PersonId
;

create or replace view Q17(Name,Total)
as
select pe.Name,count(inpr.ProceedingId) as Total
from Person pe
    join RelationPersonInProceeding rpip on(Pe.PersonId = rpip.PersonId)
    join InProceeding inpr on(inpr.InProceedingId = rpip.InProceedingId
    and inpr.ProceedingId is not NULL)
    Group by pe.PersonId
    Order by Total desc,pe.Name asc
;

create or replace view Q18(MinPub,AvgPub,MaxPub)
as
select Min(Total),round(Avg(Total)),Max(Total)
from Q17
;

create or replace view Q19(MinPub,AvgPub,MaxPub)
as
select Min(P.Total),round(Avg(P.Total)),Max(P.Total)
from (select pr.ProceedingId,count(inpr.InProceedingId) as Total
  from Proceeding pr
  left outer join inProceeding inpr on(pr.ProceedingId = inpr.ProceedingId)
  Group by pr.ProceedingId) as P
;


--Q20
create or replace function
  checkauthor() returns trigger
as $$
begin
  if not exists(select rpip.InProceedingId
  from RelationPersonInProceeding rpip
  join Proceeding pr on(pr.EditorId = New.PersonId)
  where rpip.InProceedingId = New.InProceedingId)
  Then
    raise exception 'Invalid Input';
  end if;
  return New;
end;
$$ language 'plpgsql';

create trigger limitauthor
before insert or update on RelationPersonInProceeding
for each row
execute procedure checkauthor();


--Q21
create or replace function
  check_ed_au() returns trigger
as $$
begin
  if not Exists(select pr.ProceedingId
    from proceeding pr
    join InProceeding inpr on(inpr.proceedingId = new.proceedingId)
    join RelationPersonInProceeding rpip on(inpr.InProceedingId = rpip.InProceedingId)
    join Person pe on(rpip.PersonId = pe.PersonId)
    where inpr.ProceedingId is not NuLL)
    Then
    raise exception 'Invalid Input';
    end if;
    return New;
end;
$$ language 'plpgsql';

create trigger limitproceeding
before insert or update on Proceeding
for each row
execute procedure check_ed_au();

--Q22
create or replace function
  check_au_ed() returns trigger
as $$
begin
if not Exists(select inpr.InProceedingId
    from inproceeding inpr
    join RelationPersonInProceeding rpip on(New.InProceedingId = rpip.InProceedingId)
    join Person pe on(rpip.PersonId = pe.PersonId)
    join Proceeding pr on(pr.EditorId = pe.PersonId)
    where inpr.ProceedingId is not NuLL)
    Then
    raise exception 'Invalid Input';
    end if;
    return New;
end;
$$ language 'plpgsql';


create trigger limitinproceeding
before insert or update on RelationPersonInProceeding
for each row
execute procedure check_au_ed();
