from redis import Redis
import rq
queue = rq.Queue('server-task', connection=Redis.from_url('redis://'))
job = queue.enqueue('app.tasks.example', 30)
job.get_id()
