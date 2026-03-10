// Input
// [
//   {"name": "Ravi", "accountNumber": "1234567890"},
//   {"name": "Sneha", "accountNumber": "9876543210"}
// ]

// Output:
// [
//   {"name": "Ravi", "accountNumber": "****7890"},
//   {"name": "Sneha", "accountNumber": "****3210"}
// ]

%dw 2.0
output application/json
---
%dw 2.0
import * from dw::util::Values
output application/json
---
payload map (item) -> {
  item.name,
  accountNumber: mask(item.accountNumber, "*", 4)
}