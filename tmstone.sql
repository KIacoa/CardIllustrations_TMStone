create table race
(
 id varchar(4) primary key check(id like 'r%'),
 name varchar(32) unique not null,
 strength1 int not null,
 strength2 int not null ,
 strength3 int not null
);
create table main_hero
(
 id varchar(8) primary key check(id like 'mc%'),
 name varchar(32) unique not null,
 hp int,
 attack int,
 strength1_dev int,
 strength2_dev int,
 strength3_dev int,
 race_id varchar(4),
 img varchar(64),
 foreign key(race_id) references race(id)
)
drop table main_hero
create table exclusive_servant
(
 id varchar(8) primary key check(id like 'es%'),
 name varchar(32) unique not null,
 type varchar(16) not null check(type in('equipment','servant','skill')) default 'servant',
 hp int ,
 attack int,
 strength int,
 effect varchar(256),
 m_id varchar(8) not null,
 race_id varchar(4), 
 img varchar(64),
 foreign key(m_id) references main_hero(id) 
 foreign key(race_id) references race(id)
)
drop table exclusive_servant
create table skill
(
 id varchar(8) primary key check(id like 'cs%'),
 name varchar(32) unique not null,
 description varchar(256) not null,
 consumption int,
 cd int,
 use_condition varchar(256),
 holder_id varchar(8)
)
create table quality
(
 id varchar(4) primary key check(id like 'q%'),
 name varchar(32) unique not null,
 consumption int 
)
drop table servant
drop table magic
drop table trap
drop table equipment
create table servant
(
 id varchar(8) primary key check(id like 's%'),
 name varchar(32) unique not null,
 is_hero tinyint not null default 0,
 hp int ,
 attack int,
 strength int,
 race_id varchar(4), 
 quality_id varchar(4), 
 img varchar(64),
 foreign key(race_id) references race(id)
 foreign key(quality_id) references quality(id)
)
create table magic
(
 id varchar(8) primary key check(id like 'm%'),
 name varchar(32) unique not null,
 quality_id varchar(4),
 img varchar(64),
 foreign key(quality_id) references quality(id)
)
create table trap
(
 id varchar(8) primary key check(id like 't%'),
 name varchar(32) unique not null,
 quality_id varchar(4),
 img varchar(64),
 foreign key(quality_id) references quality(id)
)
create table equipment_type
(
 id varchar(4) primary key check(id like 'et%'),
 name varchar(32) unique not null,
 consumption int,
 description varchar(256)
)
create table equipment
(
 id varchar(8) primary key check(id like 'e%'),
 name varchar(32) unique not null,
 attack_add int,
 type_id varchar(4),
 quality_id varchar(4),
 img varchar(64),
 foreign key(quality_id) references quality(id)
 foreign key(type_id) references equipment_type(id)
)
create table effect
(
 id varchar(8) primary key check(id like 'ce%'),
 name varchar(32) unique not null,
 condition varchar(256),
 description varchar(256),
 card_id varchar(8)
)
create table card1
(
 id int,
 c_id varchar(8),
 is_environment tinyint default 1,
 primary key(id)
 auto_increment(id)
)
insert into race(id,name,strength1,strength2,strength3) values('r001','人族',2,5,7)
insert into race(id,name,strength1,strength2,strength3) values('r002','兽族',3,7,9)
insert into race(id,name,strength1,strength2,strength3) values('r003','机械',8,8,8)
insert into race(id,name,strength1,strength2,strength3) values('r004','亚人族',3,6,8)
insert into race(id,name,strength1,strength2,strength3) values('r005','巨人族',4,8,11)
insert into race(id,name,strength1,strength2,strength3) values('r006','无',5,6,7)
insert into race(id,name,strength1,strength2,strength3) values('r007','植物',2,4,8)
insert into race(id,name,strength1,strength2,strength3) values('r008','不死族',4,6,7)
insert into race(id,name,strength1,strength2,strength3) values('r009','怪兽',7,7,7)
insert into race(id,name,strength1,strength2,strength3) values('r010','恶魔',3,5,8)
insert into main_hero(id,name,hp,attack,strength1_dev,strength2_dev,strength3_dev,race_id,img) 
values('mc000001','乌龟',45,1,1,0,0,'r002','image/mc1')
insert into main_hero(id,name,hp,attack,strength1_dev,strength2_dev,strength3_dev,race_id,img) 
values('mc000002','火枪手',40,2,0,0,0,'r001','image/mc2')
insert into main_hero(id,name,hp,attack,strength1_dev,strength2_dev,strength3_dev,race_id,img) 
values('mc000003','人鱼公主',40,1,0,0,0,'r004','image/mc3')
insert into main_hero(id,name,hp,attack,strength1_dev,strength2_dev,strength3_dev,race_id,img) 
values('mc000004','暮塔旅行者',40,1,0,-1,0,'r001','image/mc4')
insert into main_hero(id,name,hp,attack,strength1_dev,strength2_dev,strength3_dev,race_id,img) 
values('mc000005','巨人国王',50,3,0,0,1,'r005','image/mc5')
insert into main_hero(id,name,hp,attack,strength1_dev,strength2_dev,strength3_dev,race_id,img) 
values('mc000006','机械刽子手',40,1,0,0,0,'r003','image/mc6')
insert into main_hero(id,name,hp,attack,strength1_dev,strength2_dev,strength3_dev,race_id,img) 
values('mc000007','花',40,1,0,0,0,'r007','image/mc7')
insert into main_hero(id,name,hp,attack,strength1_dev,strength2_dev,strength3_dev,race_id,img) 
values('mc000008','古代文字',40,1,0,0,0,'r006','image/mc8')
insert into main_hero(id,name,hp,attack,strength1_dev,strength2_dev,strength3_dev,race_id,img) 
values('mc000009','气师',40,1,0,0,0,'r001','image/mc9')
insert into main_hero(id,name,hp,attack,strength1_dev,strength2_dev,strength3_dev,race_id,img) 
values('mc000010','幻想世界小孩',40,0,2,0,0,'r001','image/mc10')

insert into exclusive_servant(id,name,type,hp,attack,strength,effect,m_id,race_id,img)
values('es000001','小鱼','servant',20,1,4,null,'mc000001','r002','image/es1')
insert into exclusive_servant(id,name,type,hp,attack,strength,effect,m_id,race_id,img)
values('es000002','后勤部队','servant',20,1,4,null,'mc000002','r001','image/es2')
insert into exclusive_servant(id,name,type,hp,attack,strength,effect,m_id,race_id,img)
values('es000003','浮灵','servant',20,1,4,null,'mc000003','r004','image/es3')
insert into exclusive_servant(id,name,type,hp,attack,strength,effect,m_id,race_id,img)
values('es000004','书童','servant',20,0,4,null,'mc000004','r001','image/es4')
insert into exclusive_servant(id,name,type,hp,attack,strength,effect,m_id,race_id,img)
values('es000005','巨人侍卫','servant',25,2,5,null,'mc000005','r005','image/es5')
insert into exclusive_servant(id,name,type,hp,attack,strength,effect,m_id,race_id,img)
values('es000006','刽子手斩刃','equipment',null,1,4,'武器仆从无法被拆卸','mc000006',null,'image/es6')
insert into exclusive_servant(id,name,type,hp,attack,strength,effect,m_id,race_id,img)
values('es000007','草','servant',20,0,4,null,'mc000007','r007','image/es7')
insert into exclusive_servant(id,name,type,hp,attack,strength,effect,m_id,race_id,img)
values('es000008','远古文字','skill',null,null,4,'技能仆从使主角色直接习得对应技能，并获得其属性','mc000008',null,'image/es8')
insert into exclusive_servant(id,name,type,hp,attack,strength,effect,m_id,race_id,img)
values('es000009','气功秘籍','skill',null,null,4,'技能仆从使主角色直接习得对应技能，并获得其属性','mc000009',null,'image/es9')
insert into exclusive_servant(id,name,type,hp,attack,strength,effect,m_id,race_id,img)
values('es000010','幻想怪兽','servant',20,1,4,null,'mc000010','r002','image/es10')
select * from skill
insert into skill(id,name,description,consumption,cd,use_condition,holder_id)
values('cs000001','背甲','该技能为被动技能，使乌龟受到伤害-1',null,null,'无','mc000001')
insert into skill(id,name,description,consumption,cd,use_condition,holder_id)
values('cs000002','龟缩','该技能为持续技能，开启时生效，再次释放关闭，使乌龟背甲的效果提升至受到伤害-2，但造成伤害-2',null,null,'进化1','mc000001')
insert into skill(id,name,description,consumption,cd,use_condition,holder_id)
values('cs000003','叼','该技能为主动技能，抽取对方一张牌，若在连续的两回合内均使用此技能，第二次使用时的消耗体力+1/+2/+3...，无限叠加。每隔一回合不适用此技能，此技能的体力消耗-2',2,0,'进化2','mc000001')
insert into skill(id,name,description,consumption,cd,use_condition,holder_id)
values('cs000004','巨型龟','该技能为主动技能，是乌龟的血量和血量上限+10，且使乌龟免疫控制效果，持续至对局结束，仅能使用一次',0,999,'进化3','mc000001')
insert into skill(id,name,description,consumption,cd,use_condition,holder_id)
values('cs000005','瞄准','该技能为主动技能，使目标受到火枪手的伤害+2，仅作用于下一次由火枪手造成的伤害（非持续伤害）',1,1,'进化1','mc000002')
insert into skill(id,name,description,consumption,cd,use_condition,holder_id)
values('cs000006','人鱼海域','该技能为被动技能，每当有任意一个单位被选定为任意角色打出除病毒外卡牌的对象时，该牌造成效果后，作为一个标记放在被选定单位的状态栏',null,null,'无','mc000003')
insert into skill(id,name,description,consumption,cd,use_condition,holder_id)
values('cs000007','元素碎片','该技能为主动技能，消耗暮塔旅行者1血量，造成2点任意属性元素伤害，每回合可使用两次，且两回合不能使用同种属性',1,0,'进化1','mc000004')
insert into skill(id,name,description,consumption,cd,use_condition,holder_id)
values('cs000008','斩首','该技能为主动技能，战场上一旦有血量低于3的非英雄单位，即可对其直接斩杀',0,1,'进化1','mc000006')
insert into skill(id,name,description,consumption,cd,use_condition,holder_id)
values('cs000009','光合作用','该技能为被动技能，在白天，恢复花4点生命；在黑夜，对所有其他角色造成1伤害',null,null,'无','mc000007')
insert into skill(id,name,description,consumption,cd,use_condition,holder_id)
values('cs000010','文字魔法·火','该技能为主动技能，对一个单位造成3伤害，并点燃4回合',2,2,'进化2','mc000008')
insert into skill(id,name,description,consumption,cd,use_condition,holder_id)
values('cs000011','文字魔法·水','该技能为主动技能，对一个单位造成2伤害，并其阵营所有单位额外造成1伤害',2,2,'进化1','mc000008')
insert into skill(id,name,description,consumption,cd,use_condition,holder_id)
values('cs000012','高强度引燃','该技能为被动技能，使小孩的引燃对目标造成额外1点伤害，并延长1回合',null,null,'进化1','mc000010')
insert into skill(id,name,description,consumption,cd,use_condition,holder_id)
values('cs000013','文字魔法·痛苦','该技能为主动技能，使指定角色每回合掉4血，直至死亡',6,15,'无','es000008')
insert into skill(id,name,description,consumption,cd,use_condition,holder_id)
values('cs000014','进化之实','该技能为主动技能，使小鱼直接死亡，且无法复活，使乌龟恢复10生命，并增加5血量上限，且使乌龟受到所有的持续伤害-1',0,0,'无','es000001')
insert into skill(id,name,description,consumption,cd,use_condition,holder_id)
values('cs000015','碎石散弹','该技能为主动技能，对一个阵营的所有单位造成1伤害，并使他们下次行动消耗体力+1持续一回合',3,3,'无','es000002')
select *from quality
insert into quality(id,name,consumption)
values('q001','基础',1)
insert into quality(id,name,consumption)
values('q002','普通',1)
insert into quality(id,name,consumption)
values('q003','稀有',2)
insert into quality(id,name,consumption)
values('q004','史诗',3)
insert into quality(id,name,consumption)
values('q005','传说',4)
select * from equipment_type
insert into equipment_type(id,name,consumption,description)
values('et01','轻型武器',0,'每个人只能最多同时使用两把轻型武器')
insert into equipment_type(id,name,consumption,description)
values('et02','重型武器',1,'每个人只能同时使用一把重型武器')
insert into equipment_type(id,name,consumption,description)
values('et03','寄生武器',0,'寄生武器与其他武器的使用均不冲突')
insert into equipment_type(id,name,consumption,description)
values('et04','远程武器',0,'在使用远程武器时，不能使用其他类型武器')
insert into equipment_type(id,name,consumption,description)
values('et05','防具',0,'所有已装备防具不能超过两件')
select * from servant
select * from race
insert into servant(id,name,is_hero,hp,attack,strength,race_id,quality_id,img)
values('s0000001','骷髅',0,5,1,2,'r008','q002','image/s1')
insert into servant(id,name,is_hero,hp,attack,strength,race_id,quality_id,img)
values('s0000002','攻击图腾',0,5,0,0,'r006','q002','image/s2')
insert into servant(id,name,is_hero,hp,attack,strength,race_id,quality_id,img)
values('s0000003','暗裔·巨刃',1,20,2,3,'r010','q004','image/s3')
insert into servant(id,name,is_hero,hp,attack,strength,race_id,quality_id,img)
values('s0000004','邪恶老树精·凯凯',0,10,1,3,'r009','q003','image/s4')
insert into servant(id,name,is_hero,hp,attack,strength,race_id,quality_id,img)
values('s0000005','骑蝇',0,10,2,2,'r010','q003','image/s5')
insert into servant(id,name,is_hero,hp,attack,strength,race_id,quality_id,img)
values('s0000006','防御图腾',0,5,0,0,'r006','q003','image/s6')
insert into servant(id,name,is_hero,hp,attack,strength,race_id,quality_id,img)
values('s0000007','铁甲骑士',0,10,2,1,'r001','q003','image/s7')
insert into servant(id,name,is_hero,hp,attack,strength,race_id,quality_id,img)
values('s0000008','幼龙',1,15,1,2,'r002','q004','image/s8')
insert into servant(id,name,is_hero,hp,attack,strength,race_id,quality_id,img)
values('s0000009','铁牛',1,20,2,2,'r004','q004','image/s9')
insert into servant(id,name,is_hero,hp,attack,strength,race_id,quality_id,img)
values('s0000010','拉格里尼的傻瓜巨人',0,20,3,4,'r005','q004','image/s10')
select * from magic
select * from quality
insert into magic(id,name,quality_id,img) values('m0000001','水弹','q001','image/m1')
insert into magic(id,name,quality_id,img) values('m0000002','引燃','q002','image/m2')
insert into magic(id,name,quality_id,img) values('m0000003','治疗','q001','image/m3')
insert into magic(id,name,quality_id,img) values('m0000004','圣疗术','q005','image/m4')
insert into magic(id,name,quality_id,img) values('m0000005','大地震击','q004','image/m5')
insert into magic(id,name,quality_id,img) values('m0000006','除你武器','q003','image/m6')
insert into magic(id,name,quality_id,img) values('m0000007','沉默','q003','image/m7')
insert into magic(id,name,quality_id,img) values('m0000008','雷击','q003','image/m8')
insert into magic(id,name,quality_id,img) values('m0000009','急速冷却','q003','image/m9')
insert into magic(id,name,quality_id,img) values('m0000010','生而平等','q004','image/m10')
insert into magic(id,name,quality_id,img) values('m0000011','乱斗','q003','image/m11')
insert into magic(id,name,quality_id,img) values('m0000012','深渊的交杖','q004','image/m12')
select * from trap
insert into trap(id,name,quality_id,img) values('t0000001','法术失效','q003','image/t1')
insert into trap(id,name,quality_id,img) values('t0000002','法术反制','q004','image/t2')
insert into trap(id,name,quality_id,img) values('t0000003','盾反','q002','image/t3')
insert into trap(id,name,quality_id,img) values('t0000004','复制器皿','q005','image/t4')
insert into trap(id,name,quality_id,img) values('t0000005','龙蛋','q003','image/t5')
insert into trap(id,name,quality_id,img) values('t0000006','受击嘲讽','q003','image/t6')
insert into trap(id,name,quality_id,img) values('t0000007','引火自焚','q003','image/t7')
insert into trap(id,name,quality_id,img) values('t0000008','免死令牌','q004','image/t8')
insert into trap(id,name,quality_id,img) values('t0000009','吸星大法','q004','image/t9')
insert into trap(id,name,quality_id,img) values('t0000010','伤害转移','q003','image/t10')
select * from equipment
select * from equipment_type
insert into equipment(id,name,attack_add,type_id,quality_id,img)
values('e0000001','海妖三叉戟',2,'et02','q003','image/e1')
insert into equipment(id,name,attack_add,type_id,quality_id,img)
values('e0000002','潦草的头盔',0,'et05','q002','image/e2')
insert into equipment(id,name,attack_add,type_id,quality_id,img)
values('e0000003','银白双刀',1,'et01','q003','image/e3')
insert into equipment(id,name,attack_add,type_id,quality_id,img)
values('e0000004','巨型属性盾',0,'et05','q003','image/e4')
insert into equipment(id,name,attack_add,type_id,quality_id,img)
values('e0000005','塔林克匕首',1,'et02','q004','image/e5')
insert into equipment(id,name,attack_add,type_id,quality_id,img)
values('e0000006','玛尔角弓·聚合',1,'et04','q004','image/e6')
insert into equipment(id,name,attack_add,type_id,quality_id,img)
values('e0000007','黑龙巨剑',3,'et02','q004','image/e7')
insert into equipment(id,name,attack_add,type_id,quality_id,img)
values('e0000008','阿托利亚·荣耀骑士剑',1,'et01','q004','image/e8')
insert into equipment(id,name,attack_add,type_id,quality_id,img)
values('e0000009','阿托利亚·荣耀骑士甲',0,'et05','q004','image/e9')
insert into equipment(id,name,attack_add,type_id,quality_id,img)
values('e0000010','阿托利亚·荣耀骑士盾',0,'et05','q004','image/e10')
select * from effect
select * from magic
select * from servant
select * from trap
insert into effect(id,name,condition,description,card_id)
values('ce000001','水弹','打出卡牌时','对一个单位造成1点水属性伤害','m0000001')
insert into effect(id,name,condition,description,card_id)
values('ce000002','圣疗术','打出卡牌时','恢复30生命值，并使其本回合受到伤害-1','m0000004')
insert into effect(id,name,condition,description,card_id)
values('ce000003','大地震击','打出卡牌时','对一个阵营的所有单位造成3伤害，并使他们无法进行普通攻击持续一回合','m0000005')
insert into effect(id,name,condition,description,card_id)
values('ce000004','生而平等','打出卡牌时','使场上所有主角色的生命上限等于你的生命上限','m0000010')
insert into effect(id,name,condition,description,card_id)
values('ce000005','攻击图腾','仆从存活时','使本阵营的所有单位造成伤害+1','s0000002')
insert into effect(id,name,condition,description,card_id)
values('ce000006','继承','仆从存活时','当主角色死亡时，继承他的50%最大生命值和体力','s0000003')
insert into effect(id,name,condition,description,card_id)
values('ce000007','奥术精通','仆从存活时','本阵营的所有单位法术伤害+1','s0000005')
insert into effect(id,name,condition,description,card_id)
values('ce000008','生命汲取','仆从存活时','没进行两次攻击，会对下一次攻击充能，在攻击时，吸取对方3生命值和2体力，仆从首次被召唤时，直接获取一次充能','s0000004')
insert into effect(id,name,condition,description,card_id)
values('ce000009','法术反制','被法术击中时','使该法术的对象改变为施法者','t0000002')
insert into effect(id,name,condition,description,card_id)
values('ce000010','龙蛋','累积受到6伤害时','使进行最后一击的实施者中毒一回合，并让你召唤你的专属仆从','t0000005')
insert into effect(id,name,condition,description,card_id)
values('ce000011','海妖三叉戟','进行普通攻击时','当你使用该武器攻击一个单位时，会使你下一次使用该武器攻击次单位的伤害+1，此效果不会叠加','e0000001')
select * from card
insert into card(id,c_id,is_environment)
values(1,'mc000001',1);
insert into card(id,c_id,is_environment)
values(2,'mc000002',1);
insert into card(id,c_id,is_environment)
values(3,'mc000003',1);
insert into card(id,c_id,is_environment)
values(4,'mc000004',1);
insert into card(id,c_id,is_environment)
values(5,'mc000005',1);
insert into card(id,c_id,is_environment)
values(6,'mc000006',1);
insert into card(id,c_id,is_environment)
values(7,'mc000007',1);
insert into card(id,c_id,is_environment)
values(8,'mc000008',1);
insert into card(id,c_id,is_environment)
values(9,'mc000009',1);
insert into card(id,c_id,is_environment)
values(10,'mc000010',1);
insert into card(id,c_id,is_environment)
values(11,'es000001',1);
insert into card(id,c_id,is_environment)
values(12,'es000002',1);
insert into card(id,c_id,is_environment)
values(13,'es000003',1);
insert into card(id,c_id,is_environment)
values(14,'es000004',1);
insert into card(id,c_id,is_environment)
values(15,'es000005',1);
insert into card(id,c_id,is_environment)
values(16,'es000006',1);
insert into card(id,c_id,is_environment)
values(17,'es000007',1);
insert into card(id,c_id,is_environment)
values(18,'es000008',1);
insert into card(id,c_id,is_environment)
values(19,'es000009',1);
insert into card(id,c_id,is_environment)
values(20,'es000010',1);
insert into card(id,c_id,is_environment)
values(21,'s0000001',1);
insert into card(id,c_id,is_environment)
values(22,'s0000002',1);
insert into card(id,c_id,is_environment)
values(23,'s0000003',1);
insert into card(id,c_id,is_environment)
values(24,'s0000004',1);
insert into card(id,c_id,is_environment)
values(25,'s0000005',1);
insert into card(id,c_id,is_environment)
values(26,'s0000006',1);
insert into card(id,c_id,is_environment)
values(27,'s0000007',1);
insert into card(id,c_id,is_environment)
values(28,'s0000008',1);
insert into card(id,c_id,is_environment)
values(29,'s0000009',1);
insert into card(id,c_id,is_environment)
values(30,'s0000010',1);
insert into card(id,c_id,is_environment)
values(31,'m0000001',1);
insert into card(id,c_id,is_environment)
values(32,'m0000002',1);
insert into card(id,c_id,is_environment)
values(33,'m0000003',1);
insert into card(id,c_id,is_environment)
values(34,'m0000004',1);
insert into card(id,c_id,is_environment)
values(35,'m0000005',1);
insert into card(id,c_id,is_environment)
values(36,'m0000006',1);
insert into card(id,c_id,is_environment)
values(37,'m0000007',1);
insert into card(id,c_id,is_environment)
values(38,'m0000008',1);
insert into card(id,c_id,is_environment)
values(39,'m0000009',1);
insert into card(id,c_id,is_environment)
values(40,'m0000010',1);
insert into card(id,c_id,is_environment)
values(41,'t0000001',1);
insert into card(id,c_id,is_environment)
values(42,'t0000002',1);
insert into card(id,c_id,is_environment)
values(43,'t0000003',1);
insert into card(id,c_id,is_environment)
values(44,'t0000004',1);
insert into card(id,c_id,is_environment)
values(45,'t0000005',1);
insert into card(id,c_id,is_environment)
values(46,'t0000006',1);
insert into card(id,c_id,is_environment)
values(47,'t0000007',1);
insert into card(id,c_id,is_environment)
values(48,'t0000008',1);
insert into card(id,c_id,is_environment)
values(49,'t0000009',1);
insert into card(id,c_id,is_environment)
values(50,'t0000010',1);
insert into card(id,c_id,is_environment)
values(51,'e0000001',1);
insert into card(id,c_id,is_environment)
values(52,'e0000002',1);
insert into card(id,c_id,is_environment)
values(53,'e0000003',1);
insert into card(id,c_id,is_environment)
values(54,'e0000004',1);
insert into card(id,c_id,is_environment)
values(55,'e0000005',1);
insert into card(id,c_id,is_environment)
values(56,'e0000006',1);
insert into card(id,c_id,is_environment)
values(57,'e0000007',1);
insert into card(id,c_id,is_environment)
values(58,'e0000008',1);
insert into card(id,c_id,is_environment)
values(59,'e0000009',1);
insert into card(id,c_id,is_environment)
values(60,'e0000010',1);


--视图
create view legend_magic
as 
select id,name
from magic as m where m.quality_id =
(
 select quality.id from quality where quality.name='传说'
)
create view epic_magic
as 
select id,name
from magic as m where m.quality_id =
(
 select quality.id from quality where quality.name='史诗'
)
select * from legend_magic
--触发器
create trigger card_synchronisation
on card
after insert
as
begin
	declare @card_id int
	declare @content_id varchar(8)
	declare @msg varchar(256)
	select @card_id=id,@content_id=c_id from inserted
	if not exists(select * from main_hero where id=@content_id)
	and not exists(select * from exclusive_servant where id=@content_id)
	and not exists(select * from servant where id=@content_id)
	and not exists(select * from magic where id=@content_id)
	and not exists(select * from trap where id=@content_id)
	and not exists(select * from equipment where id=@content_id)
	begin
		rollback transaction
		set @msg='所有的卡牌内容里均为找到，编号为'+@content_id+'的内容'
		raiserror(@msg,1,1)
	end
end
*/