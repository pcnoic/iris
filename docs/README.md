## TODO

### Sample request

```curl
curl --location --request POST 'http://localhost:8000/api/v1/message/push' \
--header 'Content-Type: application/json' \
--data-raw '{
    "sender":"emma",
    "targets":["+306977084226"],
    "message":"hello",
    "protocol":"sms",
    "topic":"emma-demo",
    "provider":"aws"
}'
```
