//Input:-

//<placedDate>2022-05-25 00:00:00.0</placedDate>
//Output:-

//"05/25/2022"
//Dataweave Code:-

%dw 2.0
output application/json
var x=(payload.placedDate splitBy(' '))[0]
---
x as Date 