
### vector table
drop table if exists vec1;
create table vec1 ( key: fid uuid, value: v vector(10, 'manhatten_fraction_byte,manhatten_fraction_short, cosine_fraction_byte,cosine_fraction_float'), fname char(64) );
expect words "vec1 vector fid fname manhatten";
desc vec1;

drop index if exists vec1_idx1 on vec1;
create index vec1_idx1 on vec1( v, fid, fname );
expect words "vec1_idx1 vec1 vector";
desc vec1_idx1;

drop index if exists vec1_idx2 on vec1;
create index vec1_idx2 on vec1( fname, fid );
expect words "vec1_idx2 fname fid vec1";
desc vec1_idx2;


insert into vec1 values ( '0.2, 0.4, 0.2, 0.3, 0.7, 0.3, 0.81, 0.34', 'photo1.jpg' );
expect putvalue fid1;
select fid as fid1 from test.vec1.vec1_idx2 where fname='photo1.jpg';
print fid1;

expect putvalue vid1;
select v as vid1 from vec1 where fid=$getvalue(fid1)$;
print vid1;

insert into vec1 values ( '0.8, 0.4, 0.2, 0.3, 0.7, 0.03, 0.3, 0.41', 'photo2.jpg' );
insert into vec1 values ( '0.6, 0.2, 0.2, 0.3, 0.7, 0.3, 0.1, 0.4', 'photo3.jpg' );
insert into vec1 values ( '0.6, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.4', 'photo4.jpg' );
insert into vec1 values ( '0.2, -0.2, 0.2, 0.3, -0.3, 0.3, 0.03, 0.4', 'photo5.jpg' );
insert into vec1 values ( '0.02, -0.02, 0.02, 0.13, 0.23, -0.1, 0.03, 0.2', 'photo6.jpg' );
insert into vec1 values ( '0.05, 0.07, 0.02, 0.53, 0.23, -0.1, 0.23, 0.2', 'photo7.jpg' );
insert into vec1 values ( '0.5, 0.27, 0.02, 0.53, 0.23, -0.5, 0.43, 0.1', 'photo8.jpg' );

expect rows 8;
select * from vec1;

expect rows 1;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=manhatten_fraction_byte') from vec1;

expect rows 1;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=manhatten_fraction_short') from vec1;

expect rows 1;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=manhatten_fraction_byte,output_vector=yes') from vec1;

expect rows 1;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=manhatten_fraction_short,output_vector=yes') from vec1;

expect rows 1;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=cosine_fraction_float,output_vector=yes') from vec1;

expect rows 8;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=10,type=cosine_fraction_float') from vec1 where fname like 'pho%';

update vec1 set v:vector='0.501,0.071,0.051,0.001,0,0.8,0,0' where fid=$getvalue(fid1)$;

update vec1 set v:vector='$getnqvalue(vid1)$:0.201,0.501,0.701,0.031,0.3,0.12,-0.2,-0.3' where 1;

select vector(v, 'type=manhatten_fraction_short') from vec1 where fid=$getvalue(fid1)$;
select vector(v, 'type=manhatten_fraction_byte') from vec1 where fid=$getvalue(fid1)$;

#delete from vec1 where fid=$getvalue(fid1)$;


quit;
