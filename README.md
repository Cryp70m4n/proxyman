**Proxyman is an simple API written in python and sqlite which provides you easy way to scrap and manage proxy lists.**


**Consider checking [/examples/usage](https://github.com/Cryp70m4n/proxyman/tree/main/examples/usage) directory to get API usage examples**

**Consider checking [/examples/expansions](https://github.com/Cryp70m4n/proxyman/tree/main/examples/expansions) directory to get ideas related to expansions of API**

| **Endpoints**        | **Parameters**                          | **Methods** |
|----------------------|-----------------------------------------|-------------|
| /api/show_sources    | None                                    | GET         |
| /api/add_source      | source (STRING)                         | POST        |
| /api/remove_source   | source (STRING)                         | POST        |
| /api/refresh_proxies | refreshes (INT)                         | POST        |
| /api/get_proxies     | proxy_type (STRING), proxy_amount (INT) | GET         |


If you have any questions or expension ideas regarding API feel free to contact me by sending email to cryp70m4n@gmail.com.

if you face some bugs while using API please open Issue.

If you make an API improvement which you consider useful please consider sharing it with us by making Pull request.
