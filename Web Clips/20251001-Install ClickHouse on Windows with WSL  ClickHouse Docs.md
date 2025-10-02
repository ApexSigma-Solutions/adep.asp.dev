---
title: 20251001-Install ClickHouse on Windows with WSL | ClickHouse Docs
source: https://clickhouse.com/docs/install/windows
author:
published: 2025-10-01
created: 2025-10-01
description: Install ClickHouse on Windows with WSL
tags:
  - WebClip
status: "[processed][unprocessed]"
---
# Install ClickHouse on Windows with WSL | ClickHouse Docs
## Content

## Requirements

Open Windows PowerShell as administrator and run the following command:

```bash
wsl --install
```

You will be prompted to enter a new UNIX username and password. After you have entered your desired username and password you should see a message similar to:

```bash
Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 5.15.133.1-microsoft-WSL2 x86_64)
```

Run the following command to install ClickHouse via script using curl:

```bash
curl https://clickhouse.com/ | sh
```

If the script has successfully run you will see the message:

```bash
Successfully downloaded the ClickHouse binary, you can run it as:
  ./clickhouse
```

`clickhouse-local` allows you to process local and remote files using ClickHouse's powerful SQL syntax and without the need for configuration. Table data is stored in a temporary location, meaning that after a restart of `clickhouse-local` previously created tables are no longer available.

Run the following command to start [clickhouse-local](https://clickhouse.com/docs/operations/utilities/clickhouse-local):

```bash
./clickhouse
```

Should you wish to persist data, you'll want to run `clickhouse-server`. You can start the ClickHouse server using the following command:

```bash
./clickhouse server
```

With the server up and running, open a new terminal window and run the following command to launch `clickhouse-client`:

```bash
./clickhouse client
```

You will see something like this:

```bash
./clickhouse client
ClickHouse client version 24.5.1.117 (official build).
Connecting to localhost:9000 as user default.
Connected to ClickHouse server version 24.5.1.

local-host :)
```

Table data is stored in the current directory and still available after a restart of ClickHouse server. If necessary, you can pass `-C config.xml` as an additional command line argument to `./clickhouse server` and provide further configuration in a configuration file. All available configuration settings are documented [here](https://clickhouse.com/docs/operations/server-configuration-parameters/settings) and in the [example configuration file template](https://github.com/ClickHouse/ClickHouse/blob/master/programs/server/config.xml).

You are now ready to start sending SQL commands to ClickHouse!

![](https://static.scarf.sh/a.png?x-pxid=e6377503-591b-4886-9398-e69c7fee0b91) ![](https://static.scarf.sh/a.png?x-pxid=e6377503-591b-4886-9398-e69c7fee0b91)

## My Notes

*Add your thoughts and connections here*