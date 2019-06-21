import invokust

settings = invokust.create_settings(
    locustfile='websocket_locust_v2.py',
    host='https://www.websocket.org',
    num_clients=1,
    hatch_rate=1,
    run_time='3m'
    )

loadtest = invokust.LocustLoadTest(settings)
loadtest.run()
print(loadtest.stats())
