POST /api/v1/test/signin/


```http
   ### REQUEST
   POST http://localhost:8080/api/v1/test/signin/
   {
     "name": "Pitossomo",
     "email": "pitossomos@hmail.com" 
   }
   
   ### RESPONSE
   set-cookie: refresh-token=...
   {
     "name": "Pitossomo",
     "email": "pitossomos@hmail.com" 
   }

   ### Expect code 201 and info about the new user
   POST http://localhost:5001/user
   Content-Type: application/json

   {
     "name": "Pitossomo",
     "email": "pitossomos@hmail.com" 
   }
   
   ### Expect code 400
   POST http://localhost:5001/user
   Content-Type: application/json

   { 
     "name": "",
     "email": "" 
   }
   ```