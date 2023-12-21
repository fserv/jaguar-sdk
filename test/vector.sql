
### vector table
drop store if exists vec1;
create store vec1 ( v vector(10, 'manhatten_fraction_byte,manhatten_fraction_short, cosine_fraction_byte,cosine_fraction_float'), fname char(64), a int );
expect words "vec1 vector zid fname manhatten";
desc vec1;

insert into vec1 values ( '0.2, 0.4, 0.2, 0.3, 0.7, 0.3, 0.81, 0.34', 'photo1.jpg', '1' );
expect putvalue fid1;
select zid as fid1 from test.vec1.v_zid_idx;
print fid1;

expect putvalue vid1;
select v as vid1 from vec1 where zid=$getvalue(fid1)$;
print vid1;

insert into vec1 values ( '0.8, 0.4, 0.2, 0.3, 0.7, 0.03, 0.3, 0.41', 'photo2.jpg', '2' );
insert into vec1 values ( '0.6, 0.2, 0.2, 0.3, 0.7, 0.3, 0.1, 0.4', 'photo3.jpg', '3' );
insert into vec1 values ( '0.6, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.4', 'photo4.jpg', '4' );
insert into vec1 values ( '0.2, -0.2, 0.2, 0.3, -0.3, 0.3, 0.03, 0.4', 'photo5.jpg', '5' );
insert into vec1 values ( '0.02, -0.02, 0.02, 0.13, 0.23, -0.1, 0.03, 0.2', 'photo6.jpg', '5' );
insert into vec1 values ( '0.05, 0.07, 0.02, 0.53, 0.23, -0.1, 0.23, 0.2', 'photo7.jpg', '5' );
insert into vec1 values ( '0.5, 0.27, 0.02, 0.53, 0.23, -0.5, 0.43, 0.1', 'photo8.jpg', '5' );

expect rows 8;
select * from vec1;

expect json_rows 5;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=manhatten_fraction_byte') from vec1;

expect json_rows 5;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=manhatten_fraction_short') from vec1;

expect json_rows 5;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=manhatten_fraction_byte,with_vector') from vec1;

expect json_rows 5;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=manhatten_fraction_short,with_vector') from vec1;

expect json_rows 5;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=cosine_fraction_float,with_vector') from vec1;

expect json_rows 0;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=cosine_fraction_float,minute_cutoff=2') from vec1;

expect json_rows 0;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=cosine_fraction_float,hour_cutoff=1') from vec1;

expect json_rows 0;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=cosine_fraction_float,day_cutoff=2') from vec1;

expect json_rows 0;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=cosine_fraction_float,week_cutoff=1') from vec1;

sleep 65;

select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=cosine_fraction_float,minute_decay_rate=0.41') from vec1;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=cosine_fraction_float,minute_decay_rate=0.41,decay_mode=E') from vec1;

expect json_rows 4;
select similarity(v, '1.0,1.0,1.0,1.0,1.0,1.0,0.0', 'fetch_k=9, topk=7, type=cosine_fraction_float,with_text,score_threshold=-1.0,metadata=a') from vec1 where a='5';

expect json_rows 8;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=10,type=cosine_fraction_float') from vec1 where fname like 'pho%';

update vec1 set v:vector='0.501,0.071,0.051,0.001,0,0.8,0,0' where zid=$getvalue(fid1)$;

update vec1 set v:vector='$getnqvalue(vid1)$:0.201,0.501,0.701,0.031,0.3,0.12,-0.2,-0.3' where 1;

select vector(v, 'type=manhatten_fraction_short') from vec1 where zid=$getvalue(fid1)$;
select vector(v, 'type=manhatten_fraction_byte') from vec1 where zid=$getvalue(fid1)$;

#delete from vec1 where zid=$getvalue(fid1)$;

select anomalous(v, '0.1, 0.2, 0.9, 0.9, 0.9, 0.3, 0.8, 0.1, 0.2, 0.1', 'type=cosine_fraction_float,sigmas=4,activation=[0.3:20&1.3:10]') from vec1;

show tab;
help;

quit;
