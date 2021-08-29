# Notification System 

Just an attempt.

![image-20210829194335413](C:\Users\utkar\AppData\Roaming\Typora\typora-user-images\image-20210829194335413.png)



List of services

1. **Database** : Contains Assignment and Student data.
2. **Polling Service** : It will collect data in batches from the database and pass on to the distributed queue in certain time intervals, in a throttled way. It can have temporary cache to maintain already processed events. It will keep track of checkpoint of processed entries. It will add the entries in the distributed queue when its appropriate time to start processing the notification request, by looking at the deadline of the assignment.
3. **Distributed Queue** :  It will store the events which could be accessed by multiple notification services.
4. **Notification Services** : It will take tasks from the distributed queue and send the notifications accordingly.