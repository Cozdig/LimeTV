
```bash
redis-server   
```
```bash
celery -A config worker -l INFO -P eventlet
```

```bash
celery -A config beat -l INFO             
```

```bash
celery -A config flower --port=5555
```