
```bash
redis-server   
```
```bash
celery -A config worker --loglevel=info --pool=solo
```

```bash
celery -A config beat --loglevel=info              
```