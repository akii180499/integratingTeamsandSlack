Extract Keys from Nested Objects & Array

// Input:-

// [{
//  "key1": 1,
//  "key2": 2,
//  "key3": [{
//    "Key4": {
//     "key5": 5
//    }
//   },
//   {
//    "key6": 6
//   }
//  ]
// }]
// Output:-

// [
//  "key1",
//  "key2",
//  "key3",
//  "Key4",
//  "key5",
//  "key6"
// ]
Dataweave Code:-

%dw 2.0
output application/json
fun Keys(value: Any, keys = [])
 - -
po