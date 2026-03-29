# Installation

## Requirements:

- Docker
- Python
- Two machines (one to run the server and one to do the onboarding)
- A domain name that you own
- A machine that can host this with the following ports exposed (INTERNALLY in YOUR network):
```
443
8883
```

## Docker Setup

1. You should clone this repository:

`git clone https://github.com/Python-roborock/local_roborock_server`

2. Change into the project folder.

```bash
cd roborock_local_server
```

3. Install the local project environment.

```bash
uv sync
```

4. Run the setup wizard.

```bash
uv run roborock-local-server configure
```

The wizard asks only for:

- your `stack_fqdn` (this is your URL for your server. It MUST start with 'api-')
- embedded MQTT or your own broker
- whether to use Cloudflare DNS-01 auto-renew
- your admin password

It then writes `config.toml` for you, generates `admin.password_hash`, generates `admin.session_secret`, and if you chose Cloudflare it also writes `secrets/cloudflare_token`.

5. If you chose external MQTT, fill in `broker.host` in `config.toml` before starting the stack. See: [Custom MQTT](#Custom_mqtt)

6. If you skipped Cloudflare, put your certificate files in `data/certs/fullchain.pem` and `data/certs/privkey.pem`. See: [Custom cert](#custom_cert)

7. Decide on your url. it must start with 'api-'. Set the DNS record on your network to resolve your url to your server.

If your server is 'api-roborock.example.com', you should set the following DNS records to resolve to your server ip:
'api-roborock.example.com'
'mqtt-roborock.example.com'

7. Now you can start the container by running:
`docker-compose up -d --build`

8.