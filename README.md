# homer-k8s-operator

This is an experimental kuberentes operator to automate configuration of homer dashbaord:
https://github.com/bastienwirtz/homer


**I use this to learn about operators!!! Do not use in production!!!!!!**

**Idea:**
Every time a annotated servce of type "NodePort" or an "Ingress" with annotation becomes created/updated/deleted
the homer configration will be updated also.


Componentes:
- Homer Deployment
- Homer ConfigMap (autocreated)
- 

