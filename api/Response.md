[API categories](API-categories.md) | [API index](API-index.md)


# Response (object)

This object is passed as parameter to [RequestHandler](RequestHandler.md).OnBeforeResourceLoad().


Table of contents:
* [Methods](#methods)
  * [IsReadOnly](#isreadonly)
  * [GetStatus](#getstatus)
  * [SetStatus](#setstatus)
  * [GetStatusText](#getstatustext)
  * [SetStatusText](#setstatustext)
  * [GetMimeType](#getmimetype)
  * [SetMimeType](#setmimetype)
  * [GetHeaderByName](#getheaderbyname)
  * [SetHeaderByName](#setheaderbyname)
  * [GetHeaderMap](#getheadermap)
  * [GetHeaderMultimap](#getheadermultimap)
  * [SetHeaderMap](#setheadermap)
  * [SetHeaderMultimap](#setheadermultimap)


## Methods


### IsReadOnly

| | |
| --- | --- |
| __Return__ | bool |

Returns true if this object is read-only.


### GetStatus

| | |
| --- | --- |
| __Return__ | int |

Get the response status code.


### SetStatus

| Parameter | Type |
| --- | --- |
| status | int |
| __Return__ | void |

Set the response status code.


### GetStatusText

| | |
| --- | --- |
| __Return__ | string |

Get the response status text.


### SetStatusText

| Parameter | Type |
| --- | --- |
| statusText | string |
| __Return__ | void |

Set the response status text.


### GetMimeType

| | |
| --- | --- |
| __Return__ | string |

Get the response mime type.


### SetMimeType

| Parameter | Type |
| --- | --- |
| mimeType | string |
| __Return__ | void |

Set the response mime type.


### GetHeaderByName

| Parameter | Type |
| --- | --- |
| name | string |
| __Return__ | string |

Get the value for the specified response header field.


### SetHeaderByName

| Parameter | Type |
| --- | --- |
| name | string |
| value | string |
| override | bool |
| __Return__ | void |

Set the header |name| to |value|. If |overwrite| is true any existing
values will be replaced with the new value. If |overwrite| is false any
existing values will not be overwritten.


### GetHeaderMap

| Parameter | Type |
| --- | --- |
| __Return__ | dict |

Get all header fields with duplicate keys overwritten by last.


### GetHeaderMultimap

| Parameter | Type |
| --- | --- |
| __Return__ | list |

Get all header fields. Returns list of tuples (name, value). Headers may have duplicate keys, if you want to ignore duplicates use GetHeaderMap().


### SetHeaderMap

| Parameter | Type |
| --- | --- |
| headerMap | dict |
| __Return__ | void |

Set all header fields.


### SetHeaderMultimap

| Parameter | Type |
| --- | --- |
| headerMultimap | list |
| __Return__ | void |

Set all header fields. `headerMultimap` must be a list of tuples (name, value).
