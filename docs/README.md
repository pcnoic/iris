## TODO

### Sample request for SMS publishing (`aws` provider)

```c
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

### Sample request for Email Publishing (`classic` provider)

```c
curl --location --request POST 'http://localhost:8000/api/v1/message/push' \
--header 'Content-Type: application/json' \
--data-raw '{
    "sender":"emma",
    "targets":["pcnoic@gmail.com"],
    "message":"hello world",
    "protocol":"email",
    "topic":"emma-demo",
    "provider":"classic"
}'
```