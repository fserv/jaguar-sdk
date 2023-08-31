
###################################################################################################################
### sensor or car identity with uuid, name, model, and geo-location
drop table if exists iot;
create table if not exists iot ( key:  id uuid, value: name char(16), type char(8), model char(8), year date, lonlat point(srid:wgs84) );
insert into iot values ( 'MON1_SEAT', 'SENS', 'SZTM0001', '2000-01-23', point(-122.335167 47.608013) );
insert into iot values ( 'MON2_PORT', 'SENS', 'SZTM0001', '2000-01-24', point(-122.6784 45.5152) );
insert into iot values ( 'MON3_SANF', 'SENS', 'SZTM0002', '2000-01-25', point(-122.4194 37.7749) );
insert into iot values ( 'MON4_CHCG', 'SENS', 'SZTM0003', '2000-02-03', point(-87.6198 41.8781) );

insert into iot values ( 'CAR1', 'CAR', 'TESLA3', '2010-02-03' );
insert into iot values ( 'CAR2', 'CAR', 'TESLAS', '2010-03-03' );
insert into iot values ( 'CAR3', 'CAR', 'TESLAX', '2010-04-03' );
insert into iot values ( 'CAR4', 'CAR', 'TESLAY', '2010-05-03' );

insert into iot values ( 'DRONE1', 'DRONE', 'XYZ1', '2015-02-03' );
insert into iot values ( 'DRONE2', 'DRONE', 'XYZ2', '2015-03-03' );
insert into iot values ( 'DRONE3', 'DRONE', 'XYZ3', '2016-04-03' );
insert into iot values ( 'DRONE4', 'DRONE', 'XYZ4', '2018-05-03' );

expect rows 12;
select * from iot;

### range within 100 meters
expect rows 1;
select * from iot where distance(lonlat, point(-122.335167 47.608013)) < 100;

expect value cnt 1;
select count(1) cnt from iot where distance(lonlat, point(-122.335167 47.608013)) < 100;

expect rows 1;
select * from iot where distance(lonlat, point(-122.335167 47.618013)) < 10000;

expect rows 1;
select * from iot where type='SENS' and distance(lonlat, point(-122.335167 47.618013)) < 10000;

select count(*) cnt from iot where type='SENS';

expect rows 4;
select * from iot where type='SENS';

expect value cnt 4;
select count(1) cnt from iot where type='SENS';

expect rows 2;
select * from iot where type='SENS' and distance(lonlat, point(-122.335167 47.618013)) < 1000000;

### sensors with distance within 3000 kilometers
expect rows 4;
select * from iot where type='SENS' and year >= '2000-01-01' and  distance(lonlat, point(-122.335167 47.618013)) < 3000000;


expect putvalue car1id;
select id car1id from iot where name='CAR1';
print car1id;

expect putvalue car2id;
select id car2id from iot where name='CAR2';
print car2id;


###################################################################################################################
### iot  motion status
drop table if exists iotstatus;
create table if not exists iotstatus ( key: id char(32), ts timestamp, value: type char(8), tmp smallint, speed smallint, lonlat point(srid:wgs84) );

drop index if exists statidx on iotstatus;
create index statidx on iotstatus(key: ts, id, value: type, tmp, speed);

insert into iotstatus (id, type, tmp, speed, lonlat ) values ( $getvalue(car1id)$, 'CAR', 20, 60, point(-122.335167 47.608013) );
insert into iotstatus (id, type, tmp, speed, lonlat ) values ( $getvalue(car1id)$, 'CAR', 24, 50, point(-122.336168 47.608114) );
insert into iotstatus (id, type, tmp, speed, lonlat ) values ( $getvalue(car1id)$, 'CAR', 26, 55, point(-122.337169 47.608215) );
insert into iotstatus (id, type, tmp, speed, lonlat ) values ( $getvalue(car1id)$, 'CAR', 27, 65, point(-122.337369 47.608516) );

expect rows 4;
select * from iotstatus;

select avg(tmp) avgtmp from iotstatus where id=$getvalue(car1id)$;
select min(tmp) mintmp from iotstatus where id=$getvalue(car1id)$;
select max(tmp) maxtmp from iotstatus where id=$getvalue(car1id)$;
select stddev(tmp) stdevtmp from iotstatus where id=$getvalue(car1id)$;

select avg(speed) avgspeed from iotstatus where id=$getvalue(car1id)$;
select max(speed) maxspeed from iotstatus where id=$getvalue(car1id)$;
select min(speed) minpeed from iotstatus where id=$getvalue(car1id)$;


select * from test.iotstatus.statidx;

### get all data of all things within a time interval
select * from test.iotstatus.statidx where ts >= '2022-01-01 00:00:01' and ts <= '2023-07-08 11:01:01';

### get all data of all things within a time interval
select * from test.iotstatus.statidx where  ts >= '2022-01-01 00:00:01' and ts <= '2023-07-08 11:01:01';

### get average temperature of all things during a time interval
select avg(tmp) avgtmp from test.iotstatus.statidx where ts >= '2022-01-01 00:00:01' and ts <= '2023-07-08 11:01:01';

### get maximum temperature of all things during a time interval
select max(tmp) maxtmp from test.iotstatus.statidx where ts >= '2022-01-01 00:00:01' and ts <= '2023-07-08 11:01:01';

### get minimum temperature of all things during a time interval
select min(tmp) mintmp from test.iotstatus.statidx where ts >= '2022-01-01 00:00:01' and ts <= '2023-07-08 11:01:01';

### get standard deviation of temperature fluctuation of all things during a time interval
select stddev(tmp) as stddevtmp from test.iotstatus.statidx where ts >= '2022-01-01 00:00:01' and ts <= '2023-07-08 11:01:01';

### get maximum temperature of all cars during a time interval
select max(tmp) maxtmp from test.iotstatus.statidx where type = 'CAR' and  ts >= '2022-01-01 00:00:01' and ts <= '2023-07-08 11:01:01';



###################################################################################################################
### communication messages between things

drop table if exists iotmessage;
create table if not exists iotmessage ( key: id uuid, value: from char(32), to char(32), data char(64) );

drop index if exists msgidx on iotmessage;
create index msgidx on iotmessage(key: from, to, id );

insert into iotmessage values ($getvalue(car1id)$, $getvalue(car2id)$, 'Hello, are you there?');
insert into iotmessage values ($getvalue(car2id)$, $getvalue(car1id)$, 'I am here, where are you?');
insert into iotmessage values ($getvalue(car1id)$, $getvalue(car2id)$, 'I am near Sunnyvale');
insert into iotmessage values ($getvalue(car2id)$, $getvalue(car1id)$, 'Let us meet at Sunnyvale');

expect rows 4;
select * from iotmessage;

expect rows 4;
select uuidtime(id), from, to, data from iotmessage;

expect rows 4;
select uuidtime(id), from, to, data from iotmessage where uuidtime(id) >= '2022-07-19 04:12:00.422028';

expect rows 4;
select * from test.iotmessage.msgidx;

expect rows 2;
select * from test.iotmessage.msgidx where from=$getvalue(car1id)$ and to=$getvalue(car2id)$;

