# Useful Commands for EC2, Systemd, Logs & PostgreSQL (RDS)

## Systemd – Services verwalten

```bash
sudo systemctl start <service-name>
sudo systemctl stop <service-name>
sudo systemctl restart <service-name>
sudo systemctl status <service-name>
sudo journalctl -u <service-name> -f
```
## RDS PSQL

```bash
psql -h <rds-endpoint> -U <db-user> -d <database-name> // use postgres as database-name (default database in case no other was created)
\c <database> // access database
\dt // show relations
\d // access relation
```

