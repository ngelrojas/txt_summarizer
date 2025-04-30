### TEXT SUMMARIZER

#### SUMMARY
- text summarizer is a project to summarizer documents like pdf files

## settings
#### create migrations
```
  alembic revision --autogenerate -m "<your custom message>"
```
#### create table
- ```
  alembic upgrade head
  ```
#### check tables created
- ```
  sqlite3 summarize.db ".tables"
```