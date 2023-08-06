# Config
---
In order to connect to the UQ servers you need to specify an auth method, auth credentials and the endpoint (server ip + port).
This is done by creating a config object.

There are two ways of creating a config object:

1. Create the config object directly in the code:
   ```
   from uqoclient.client.config import Config
   
   endpoint = "xxx.xxx.xxx.xxx:port" 
   token = "your_token"
   config = Config(method="token", credentials=token, endpoint=endpoint)
   ```
2. Use a config file

   The UQ repository contains a config_prototype.json. Just copy it from the uqclient package somewhere else (e.g. into your project folder), change the token inside the copied config file and create the config object like this:
   ```
   config = Config(config_path="Path\to\the\configfile")
   ```

# FAQ
---
### Python Version / Packages
- Python 3.7
- Module dimod version 0.8.17
### Error messages while solving

If you try to solve a problem with UQ you might run into problems. Please consider updating ALL your python packages that are relevant for UQ. After you have done this, verify that your code is correct. If you still encounter problems, you can contact me (sebastian.zielinski@ifi.lmu.de) and I will try to help you with your problem.
   
