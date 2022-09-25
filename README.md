# Modbus Payload Converter

|                |                                                                                                         |
| -------------- | ------------------------------------------------------------------------------------------------------- |
| Name           | Modbus Payload Converter                                                                                |
| Version        | v1.0.0                                                                                                  |
| Dockerhub Link | [weevenetwork/modbus-payload-converter](https://hub.docker.com/r/weevenetwork/modbus-payload-converter) |
| authors        | Tomislav Grdenić                                                                                        |

-   [Modbus Payload Converter](#modbus-payload-converter)
    -   [Description](#description)
    -   [Environment Variables](#environment-variables)
        -   [Module Specific](#module-specific)
        -   [Set by the weeve Agent on the edge-node](#set-by-the-weeve-agent-on-the-edge-node)
    -   [Dependencies](#dependencies)
    -   [Input](#input)
    -   [Output](#output)

## Description

The input to the module is the `hex string` or `integer` included in the register(s). According to the user input (type, offset, swap, format), it detects the desired word (or what is defined) and converts it to the desired format.
The payload is split into the selected **type**. Depending on the **offset**, the bit, byte, or word is selected for conversion. Taking into account the **swap**, the bytes are rearranged and the payload is converted according to the **format**.

## Environment Variables

### Module Specific

The following module configurations can be provided in a data service designer section on weeve platform:

| Name         | Environment Variables | type    | Description                                                                                                                             |
| ------------ | --------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Type         | TYPE                  | string  | The payload data is split into the selected type. Type options: bit, byte, word, double-word                                            |
| Offset       | OFFSET                | integer | Which offset bit, or byte, or word, or double word will be converted                                                                    |
| Swap         | SWAP                  | string  | How are bytes rearranged before conversion. Swap options: abcd (no swap), badc (byte swap), cdab (word swap), dcba (byte and word swap) |
| Format       | FORMAT                | string  | Data is converted according to format. Format options: hex-string, integer, float-ieee754, string                                       |
| Input Label  | INPUT_LABEL           | string  | The input label on which data is being converted                                                                                        |
| Output Label | OUTPUT_LABEL          | string  | The output label as which data is dispatched                                                                                            |

### Set by the weeve Agent on the edge-node

Other features required for establishing the inter-container communication between modules in a data service are set by weeve agent.

| Environment Variables | type   | Description                                    |
| --------------------- | ------ | ---------------------------------------------- |
| MODULE_NAME           | string | Name of the module                             |
| MODULE_TYPE           | string | Type of the module (Input, Processing, Output) |
| EGRESS_URLS           | string | HTTP ReST endpoints for the next module        |
| INGRESS_HOST          | string | Host to which data will be received            |
| INGRESS_PORT          | string | Port to which data will be received            |

## Dependencies

```txt
bottle
requests
```

## Input

Input to this module is:

-   array of JSON body objects, example:

```json
[
    {
        "register_address": 0,
        "data": "42fb0000"
    }
]
```

## Output

Output of this module is

-   array of JSON body objects, example:

```json
[
    {
        "output-data": 125.5,
        "timestamp": 1661777292
    }
]
```
