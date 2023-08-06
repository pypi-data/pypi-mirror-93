# Compatibility
This library is compatible with stream-sea versions 4.0 <= v < 5.0

# API Reference
#### publish(*, remote_host, remote_port, secure, client_id, client_secret, stream, payload)
Publish a message to a stream.
- `remote_host: str` - The DNS name of the remote server
- `remote_port: str` - The port of the remote server
- `secure: bool` - If true, TLS is used
- `client_id: str` - The client ID
- `client_secret: str` - The client secret used to authenticate the client
- `stream: str` - The name of the stream to publish to
- `payload: Any` - The message payload to send

#### describe_stream(*, remote_host, remote_port, secure, client_id, client_secret, stream)
Read a schema definition for a stream
- `remote_host: str` - The DNS name of the remote server
- `remote_port: str` - The port of the remote server
- `secure: bool` - If true, TLS is used
- `client_id: str` - The client ID
- `client_secret: str` - The client secret used to authenticate the client
- `stream: str` - The name of the stream

#### define_stream(*, remote_host, remote_port, secure, client_id, client_secret, stream, schema)
Write a schema definition for a stream
- `remote_host: str` - The DNS name of the remote server
- `remote_port: str` - The port of the remote server
- `secure: bool` - If true, TLS is used
- `client_id: str` - The client ID
- `client_secret: str` - The client secret used to authenticate the client
- `stream: str` - The name of the stream
- `schema: SchemaDefinition` - Schema definition

If a schema definition with the same name and version number already exists, the existing definition will not be overwritten.

#### get_schema_versions_vector(*, remote_host, remote_port, secure, client_id, client_secret, streams)
Read the version numbers for multiple streams
- `remote_host: str` - The DNS name of the remote server
- `remote_port: str` - The port of the remote server
- `secure: bool` - If true, TLS is used
- `client_id: str` - The client ID
- `client_secret: str` - The client secret used to authenticate the client
- `streams: [str]` - The names of the streams

This function will return an array `ret_val` with the same length as `streams`. For every `i`, if the stream with name `streams[i]` exists, then the value of `ret_val[i]` will be that stream's version number. If the stream with name `streams[i]` does not exist, then the value of `ret_val[i]` will be `None`.

#### SchemaDefinition
The `SchemaDefinition` class defines a schema for a stream.
The `SchemaDefinition` class has the following fields:
- `name: str` - The name of the schema. Currently the name of the schema must be equal to the name of the stream.
- `version: str` - The version number of the schema.
- `fields` - The set of fields in the schema. Fields are treated as an unordered set, so the order of this array does not matter.

The following field types are supported:
- `FieldType.STRING` - Any string
- `FieldType.FLOAT` - Any JSON-serializable floating point value
- `FieldType.INTEGER` - Any JSON-serializable integer
- `FieldType.DATE` - A UTC date string in the format "YYYY-MM-DDTHH:mm:ssZ"
- `FieldType.STRING_ARRAY` - An array of `FieldType.STRING`
- `FieldType.FLOAT_ARRAY` - An array of `FieldType.FLOAT`
- `FieldType.INTEGER_ARRAY` - An array of `FieldType.INTEGER`
- `FieldType.DATE_ARRAY` - An array of `FieldType.DATE`
- `FieldType.ENUM` - A string restricted to a finite set of values
- `FieldType.OBJECT` - A JSON object
- `FieldType.OBJECT_ARRAY` - An array of `FieldType.OBJECT`

# Stream-sea-client Developer Documentation

## Tooling
- Developer tooling can be installed with `pip install -r dev-requirements.txt`
- The project uses `pycodestyle` as a linter. To lint the project, run `pycodestyle ./`
## Stream-sea wire protocol

### Websocket layer
- The stream-sea wire protocol is built on top of the Websocket protocol
- The protocol is initiated by the client establishing a Websocket connection to the server
- As long as the Websocket connection is open, it is the server's responsibility to send Websocket ping messages
at least every 30 seconds to avoid idle connections being closed
- Once a connection is established, the client and server communicate by exchanging Websocket data messages, which will be referred to as just *messages* for the rest of this spec.
- Every message is a JSON object serialized to a string

### Message structure
- Each message has an `id` field of JSON type `number` and a `action` field of JSON type `string`. Here is an example message:
```
{
  "id": 2,
  "action": "subscription",
  "streamName": "boiler_data",
  "payload": {
    "temperature": 92,
    "pressure": 3002
  }
}
```
- The client must send the first message with `id` equal to `1`, and must increase `id` by 1 for each subsequent message
- Each message `x` sent by the server is a response to an earlier message `y` sent by the client. `x` must have the same values of `id` and `action` as `y`
- For some messages `y` sent by the client, the server can reply with multiple messages `x1, x2, ...`. These must all have the same values of `id` and `action` as `y`

### Authentication Request Message
- The client-sent message with `id = 1` must be an Authentication Request message
- Client-sent messages with `id > 1` must not be Authentication Request messages
- An Authentication Request message has an `action` field with value `"authenticate"`
- An Authentication Request message must have a `payload` field of JSON type `object`
- Stream-sea supports two authentication methods: Basic and JWT
- In order to authenticate with the Basic method, the `payload` of the Authentication Request message must have the following fields:
  - A `type` field with value `"basic"`
  - A `clientId` field of JSON type `string`
  - A `clientSecret` field of JSON type `string`
- In order to authenticate with the Basic method, the `payload` of the Authentication Request message must have the following fields:
  - A `type` field with value `"jwt"`
  - A `clientId` field of JSON type `string`
  - A `jwt` field of JSON type `string` containing the stream-sea JWT
- The server must respond to an Authentication Request message with exactly one Authentication Response message

### Authentication Response Message
- An Authentication Response message has an `action` field with value `"authenticate"`
- An Authentication Response message must have a `success` field of JSON type `boolean` which will indicate whether authentication was successful
- If authentication was unsuccessful, the client must close the connection and must not send any more messages

### Subscription Request Message
- The client may subscribe by sending a Subscription Request message
- A Subscription Request message has an `action` field with value `"subscribe"`
- A Subscription Request message has a `payload` field of JSON type `string`. The value of this field must be the name of the stream to subscribe to.
- A Subscription Request message may have a `groupId` field of JSON type `string`. If set, the value of this field must be a UUID in RFC 4122 format (also known as the 8-4-4-4-12 format).
- A Subscription Request message may have multiple responses. The first response must be a Subscription Response message. Each subsequent response must be a Message Delivery message.

### Subscription Response Message
- A Subscription Response message has an `action` field with value `"subscribe"`
- A Subscription Response message has a `streamName` field of JSON type `string`. The value of this field is the name of the stream that was subscribed to.

### Message Delivery
- A Message Delivery message has an `action` field with value `"subscribe"`
- A Message Delivery message has a `payload` field of JSON type `object`. This value of this field is the user-defined message object.

### Example of stream-sea wire protocol exchange

The client authenticates and subscribes to the stream `boiler_data`
The server delivers two messages from the `boiler_data` stream.

```
# client -> server
{
  "id":1,
  "action": "authenticate",
  "payload": {
    "type": "basic"
    "clientId": "abc",
    "clientSecret": "def123"
  }
}

# client <- server
{
  "id": 1,
  "action": "authenticate",
  "success": true,
  "payload": {
    "jailId": "some_jail"
  }
}

# client -> server
{
  "id": 2,
  "action": "subscribe",
  "payload": "boiler_data"
}

# client <- server
{
  "id": 2,
  "action": "subscription",
  "success": true,
  "streamName": "boiler_data",
  "payload":2
}

# client <- server
{
  "id": 2,
  "action": "subscription",
  "streamName": "boiler_data",
  "payload": {
    "temperature": 91,
    "pressure": 3001
  }
}

# client <- server
{
  "id": 2,
  "action": "subscription",
  "streamName": "boiler_data",
  "payload": {
    "temperature": 92,
    "pressure": 3002
  }
}
```
