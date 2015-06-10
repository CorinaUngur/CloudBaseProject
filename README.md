# CloudBaseProject
<h3>Components:<br></h3>
<b>*client/send.Agent: <br></b>
  -superclass wich takes care of the communication between the agent and the controller<br>
  -should be extended by subclasses that define the table structure and name<br>
<br>
<b>*client/periodicagent.PeriodicAgent:<br></b>
  -extends send.Agent<br>
  -should be extended by agents that want to send periodically the data to the controller<br>
  -sets the period in the constructor, the default period being 30 seconds<br>
<br>
<b>*client/agentcpu.AgentCpu, agentdiskspace.AgentDiskSpace:<br></b>
  -extend periodicagent.PeriodicAgent<br>
  -define a start_process method that collects the data and sends tot the controller in a while loop<br>
<br>
<b>*server/receive.Controller:<br></b>
  -takes care of the comunication with the agent and uses dbmanager.DBManager to acces/store/manipulate the data<br>
  <br>
<b>*server/dbmanager.DBManager:<br></b>
  -uses sqlachemy<br>
  -has services of inserting into, selecting and creating tables<br>
<br>
<h3>Usage <br></h3>
<b>*start the controller:<br></b>
from receive import *<br>
ctr = Controller()<br>
ctr.start()<br>
<br>
<b>*start an agent:<br></b>
from agentcpu import *<br>
a = AgentCpu()<br>
a.start_process()<br>
<br>
<b>*start an agent that will collect an data at 10 seconds interval<br></b>
from agentdiskspace import *<br>
a = AgentDiskSpace(10)<br>
a.start_process()<br>
<br>
<b>*to create a new periodic agent:<br></b>
-define a tablename and a table structure<br>
-extend periodicagent.PeriodicAgent<br>
-call the super constructor giving it the argument table_structure<br>
-table_structure will look like: [table_name, {column1:type1, column2:type2, ... }]<br>
-implement a method that will call \__start_process\__(values) with the values colected by your agent<br>
-values will be represented by a dict where keys = column names and values = values for specific columns<br>


  
