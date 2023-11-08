
### vector table
drop store if exists vec1;
create store vec1 ( key: zid zuid, value: v vector(10, 'manhatten_fraction_byte,manhatten_fraction_short, cosine_fraction_byte,cosine_fraction_float'), fname char(64) );
expect words "vec1 vector zid fname manhatten";
desc vec1;

insert into vec1 values ( '0.2, 0.4, 0.2, 0.3, 0.7, 0.3, 0.81, 0.34', 'photo1.jpg' );
expect putvalue fid1;
select zid as fid1 from test.vec1.v_zid_idx where fname='photo1.jpg';
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
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=manhatten_fraction_byte,with_vector=yes') from vec1;

expect rows 1;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=manhatten_fraction_short,with_vector=yes') from vec1;

expect rows 1;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=5,type=cosine_fraction_float,with_vector=yes') from vec1;

## todo bug
expect rows 8;
select similarity(v, '0.1, 0.2, 0.3, 0.4, 0.5, 0.3, 0.1', 'topk=10,type=cosine_fraction_float') from vec1 where fname like 'pho%';

update vec1 set v:vector='0.501,0.071,0.051,0.001,0,0.8,0,0' where fid=$getvalue(fid1)$;

update vec1 set v:vector='$getnqvalue(vid1)$:0.201,0.501,0.701,0.031,0.3,0.12,-0.2,-0.3' where 1;

select vector(v, 'type=manhatten_fraction_short') from vec1 where fid=$getvalue(fid1)$;
select vector(v, 'type=manhatten_fraction_byte') from vec1 where fid=$getvalue(fid1)$;

#delete from vec1 where fid=$getvalue(fid1)$;

select anomalous(v, '0.1, 0.2, 0.9, 0.9, 0.9, 0.3, 0.8, 0.1, 0.2, 0.1', 'type=cosine_fraction_float,sigmas=4,activation=[0.3:20;1.3:10]') from vec1;


quit;
