```
 ___ ___       _______ _______ ___      _______ __                __   
|   Y   .--.--|   _   |   _   |   |    |   _   |  |--.-----.-----|  |_ 
|.      |  |  |   1___|.  |   |.  |    |   1___|     |  -__|  -__|   _|
|. \_/  |___  |____   |.  |   |.  |___ |____   |__|__|_____|_____|____|
|:  |   |_____|:  1   |:  1   |:  1   ||:  1   |                       
|::.|:. |     |::.. . |::..   |::.. . ||::.. . |                       
`--- ---'     `-------`----|:.`-------'`-------'                       
                           `--'                                        

[!] MySQL Sheet.

```

```
usage: mysqlsheet.py [-h] -f FILE [-b BUFFER] [-u USER] [-p PASSWORD] [--host HOST] [--port PORT] -d DATABASE -t TABLE [-m MAX]

dump big xlsheet in mysql table

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  big xlsheet file path
  -b BUFFER, --buffer BUFFER
                        file buffuer in bytes default buffer size is 4096
  -u USER, --user USER  mysql username default user is root
  -p PASSWORD, --password PASSWORD
                        mysql password default is empty
  --host HOST           mysql hostname default is localhost
  --port PORT           database port number default is 3306
  -d DATABASE, --database DATABASE
                        mysql database name
  -t TABLE, --table TABLE
                        mysql table name
  -m MAX, --max MAX     max record push concurrently in msyql
```