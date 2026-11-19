# SQL Server connection settings

The application now has a **Database Settings** page in the left navigation.

1. Select the ODBC driver installed on this computer.
2. Enter the SQL Server host/instance (for example `HOSTNAME\\SQLEXPRESS` or `192.168.1.20,1433`).
3. Enter the database name.
4. Choose Windows Authentication or SQL Server Authentication.
5. Click **Test Connection**, then **Save Settings**.

The application stores the profile under `%APPDATA%\\BarcodePrintingSystem\\sql_connection.json`. SQL passwords are protected with Windows DPAPI through `pywin32`, so they are tied to the Windows user account and computer that saved them. A saved password will not automatically decrypt under another Windows account or on another PC; enter it again there.

For another computer to connect to a SQL Server instance, that computer must have a compatible Microsoft SQL Server ODBC driver, network access to the SQL Server, and valid SQL permissions. For remote connections, configure SQL Server TCP/IP, firewall access, and authentication on the SQL Server host. Windows Authentication across computers may require domain/workgroup and account configuration; SQL Server Authentication is often simpler for separate PCs when permitted by the database administrator.

On first successful connection, the app checks/creates its `dbo.PrintHistory` and `dbo.PrintQueue` tables. The SQL login therefore needs permission to create tables the first time, or an administrator must create those tables in advance.
