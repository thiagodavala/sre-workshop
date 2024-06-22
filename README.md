# SRE Workshop

## Petshop System

### Apps

- petshop (main)
- pets
- customers

All applications implement Open Telemetry and are configured to send information locally to Signoz.io

## Test with Locust

```
docker run -p 8089:8089 -v $PWD/locust:/mnt/locust locustio/locust -f /mnt/locust/locustfile.py --host http://localhost:8000 --autostart
```

## TODO

- Adicionar logs nas tentativas de login, expor no log o login... User XXX tried to login (flag o nome do endpoint somente o valor depois do base_url/)
- criar um endpoint que retona erro, e usa um feature flag para ativar ou desligar um recurso, usar um outro endpoint para ativar a feature flag com uma chave e o endpoint passa a funcionar. (quando funcionar o retorno é a flag.)

```
curl -X POST "http://<seu-servidor>/pets/history/flag" -H "Content-Type: application/json" -d '{"value": true, "key": "FDASF$Q"}'
```

liga a feature

pets/history/flag

	"value":true,
	"key":"FDASF$Q"