


create table if not exists employee(
  emp_id varchar(5) primary key not null,
  emp_name varchar(10) not null, 
  machine_id varchar(30) not null,
  machinename tinytext not null,
  salary integer not null
);

insert into employee(emp_id, emp_name,machine_id, machinename, salary) values("A001","Pranav", "P0001","VirtualConveyer Freight500", 98000);

insert into employee(emp_id, emp_name,machine_id, machinename, salary) values("A0002","Madhav","P0002","VirtualConveyer Freight500", 99000);

insert into employee(emp_id, emp_name,machine_id, machinename, salary) values("A0003","Gopal","P0003","Cross palletron 3000", 99000);

insert into employee(emp_id, emp_name,machine_id, machinename, salary) values("A0004","Laxman","P0004","Cross palletron 4000", 97000);

insert into employee(emp_id, emp_name,machine_id, machinename, salary) values("A0005","Lucky","P0005","BX100S", 96000);

insert into employee(emp_id, emp_name,machine_id, machinename, salary) values("A0006","Tanishq","P0006","ZX12OS",100000);



CREATE TABLE IF NOT EXISTS MachineInventory(
  MachineId          VARCHAR(5) PRIMARY KEY,
  MachineName        TINYTEXT NOT NULL,
  Manufacturer       TINYTEXT NOT NULL,
  MachineDescription TEXT NOT NULL,
  AmountAvailable    INTEGER NOT NULL
);

INSERT INTO MachineInventory (MachineId, MachineName, Manufacturer, MachineDescription, AmountAvailable) VALUES(
  "P0001",
  "VirtualConveyor Freight500",
  "FetchRobotics",
  "Used for pallet transport",
  25
);
INSERT INTO MachineInventory (MachineId, MachineName, Manufacturer, MachineDescription, AmountAvailable) VALUES(
  "P0002",
  "VirtualConveyor Freight1500",
  "FetchRobotics",
  "Used for pallet transport",
  15
);
INSERT INTO MachineInventory (MachineId, MachineName, Manufacturer, MachineDescription, AmountAvailable) VALUES(
  "P0003",
  "Cross Palletron 3000",
  "Cross",
  "Used for palletizing and depalletizing",
  2
);
INSERT INTO MachineInventory (MachineId, MachineName, Manufacturer, MachineDescription, AmountAvailable) VALUES(
  "P0004",
  "Cross Palletron 4000",
  "Cross",
  "Used for palletizing and depalletizing",
  3
);
INSERT INTO MachineInventory (MachineId, MachineName, Manufacturer, MachineDescription, AmountAvailable) VALUES(
  "P0005",
  "BX100S",
  "Kawasaki Robotics",
  "Used for Spot welding",
  6
);
INSERT INTO MachineInventory (MachineId, MachineName, Manufacturer, MachineDescription, AmountAvailable) VALUES(
  "P0006",
  "ZX130S",
  "Kawasaki Robotics",
  "Used for Spot welding",
  6
);
desc MachineInventory;


select * from MachineInventory;




create table Comp_Inventory(c_no int,c_name varchar(30),no_inventory int,no_ordered int,factory_name varchar(20));


insert into Comp_Inventory values(1271,"chassis",30000,10000,"FORD UP");
insert into Comp_Inventory values(1324,"dashboard",20000,NULL,"FORD TN");
insert into Comp_Inventory values(1325,"engine",10000,5000,"FORD HARYANA");
insert into Comp_Inventory values(1328,"gearbox",50000,32000,"FORD HARYANA");
insert into Comp_Inventory values(1364,"front_axle",25000,25000,"FORD CHENNAI");
insert into Comp_Inventory values(1434,"rear_axle",15000,32000,"FORD KOLKATA");

alter table Comp_Inventory add primary key(c_no);
select * from Comp_Inventory;
desc Comp_Inventory;

create table emp_info(emp_id varchar(5) primary key not null, emp_name varchar(10) not null,  machine_id varchar(30) not null, machinename tinytext not null, salary integer not null);

insert into emp_info(emp_id, emp_name,machine_id, machinename, salary) values("A001","Pranav", "P0001","VirtualConveyer Freight500", 98000);

insert into emp_info(emp_id, emp_name,machine_id, machinename, salary) values("A0002","Madhav","P0002","VirtualConveyer Freight500", 99000);

insert into emp_info(emp_id, emp_name,machine_id, machinename, salary) values("A0003","Gopal","P0003","Cross palletron 3000", 99000);

insert into emp_info(emp_id, emp_name,machine_id, machinename, salary) values("A0004","Laxman","P0004","Cross palletron 4000", 97000);

insert into emp_info(emp_id, emp_name,machine_id, machinename, salary) values("A0005","Lucky","P0005","BX100S", 96000);

insert into emp_info(emp_id, emp_name,machine_id, machinename, salary) values("A0006","Tanishq","P0006","ZX12OS",100000);